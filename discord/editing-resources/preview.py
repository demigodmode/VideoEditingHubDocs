#!/usr/bin/env python3
"""Build resource cards; explicitly opt into publishing to the fixed review forum.

BOT_TOKEN is read only with --publish-preview. No webhook secrets are persisted.
The state journal must be retained across runs. An interrupted POST leaves a
pending marker: inspect Discord and reconcile IDs before retrying, never clear
that marker blindly. This publisher cannot target the public resources forum.
"""
import argparse
import copy
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

GUILD = '732343015711965204'
FORUM = '1480680276446154983'
WEBHOOK_NAME = 'VEH Resources Preview'
NAMES = {'resolve': 'DaVinci Resolve', 'premiere': 'Premiere Pro',
         'after-effects': 'After Effects', 'scene-packs': 'Scene Packs', 'general': 'General Resources'}
JUMP = re.compile(r'\[\[JUMP:([a-z0-9-]+)\]\]')


GUIDE = re.compile(r'\[\[GUIDE:([a-z0-9-]+)\]\]')


def resolve(value, thread, ids, threads=None):
    if isinstance(value, str):
        def replace(match):
            slug = match.group(1)
            if slug not in ids:
                raise ValueError('Unknown jump target: ' + slug)
            return f'https://discord.com/channels/{GUILD}/{thread}/{ids[slug]}'
        def replace_guide(match):
            key = match.group(1)
            if not threads or key not in threads:
                raise ValueError('Unknown guide target: ' + key)
            return f'https://discord.com/channels/{GUILD}/{threads[key]}'
        return GUIDE.sub(replace_guide, JUMP.sub(replace, value))
    if isinstance(value, list):
        return [resolve(v, thread, ids, threads) for v in value]
    if isinstance(value, dict):
        return {k: resolve(v, thread, ids, threads) for k, v in value.items()}
    return value


def validate(payload):
    count = chars = 0
    def walk(nodes):
        nonlocal count, chars
        for node in nodes:
            count += 1
            if node['type'] == 10:
                chars += len(node['content'])
            if node['type'] == 2 and not 1 <= len(node.get('label', '')) <= 80:
                raise ValueError('Button label must be 1 to 80 characters')
            if node['type'] == 1 and not 1 <= len(node.get('components', [])) <= 5:
                raise ValueError('Button rows must have 1 to 5 buttons')
            walk(node.get('components', []))
            if 'accessory' in node:
                walk([node['accessory']])
    walk(payload['components'])
    if chars > 4000:
        raise ValueError(f'Message exceeds 4000 characters: {chars}')
    if count > 40:
        raise ValueError(f'Message exceeds 40 components: {count}')
    if payload.get('flags') != 32768 or payload.get('allowed_mentions') != {'parse': []}:
        raise ValueError('Expected V2 message with mentions disabled')
    if any(token in json.dumps(payload) for token in ('[[JUMP:', '[[GUIDE:')):
        raise ValueError('Unresolved jump target')
    return chars, count


def build():
    root = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location('docs_build', root.parent / '_engine' / 'build.py')
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    result = {}
    for key in NAMES:
        meta, entries = engine.load_content(root / key)
        result[key] = []
        for entry in entries:
            _, slug, accent, title, footer, body, *button = entry
            payload = engine.build_one(meta['brand'], accent or meta['default_accent'], title, footer, body,
                                       button[0] if button else None)
            if not result[key] and meta.get('navigation'):
                components = payload['components'][0]['components']
                navigation = [{'type': 10, 'content': '**Browse this guide**'}]
                buttons = [{'type': 2, 'style': 5, 'label': label, 'url': ('[[GUIDE:' + target[1:] if target.startswith('@') else '[[JUMP:' + target) + ']]'}
                           for label, target in meta['navigation']]
                for offset in range(0, len(buttons), 5):
                    navigation.append({'type': 1, 'components': buttons[offset:offset + 5]})
                navigation.append(engine.sep())
                # The last component is the branded footer. Its preceding divider
                # also separates the index introduction from the navigation.
                components[-1:-1] = navigation
            result[key].append((slug, payload))
    check_cards(result)
    return result


def check_cards(cards):
    for key, entries in cards.items():
        if key not in NAMES or not entries:
            raise ValueError('Unknown or empty resource guide')
        ids = {slug: '9' * 20 for slug, _ in entries}
        if len(ids) != len(entries):
            raise ValueError('Duplicate card slug')
        for _, payload in entries:
            validate(resolve(payload, '9' * 20, ids, {name: '9' * 20 for name in cards}))


class API:
    def __init__(self, token):
        self.token = token
        self.webhook = None
    def call(self, method, path, data=None, webhook=False):
        headers = {'User-Agent': 'VEH-Resources-Preview/1.0', 'Content-Type': 'application/json'}
        if not webhook:
            headers['Authorization'] = 'Bot ' + self.token
        prefix = self.webhook if webhook else ''
        request = urllib.request.Request('https://discord.com/api/v10' + prefix + path,
                                         data=json.dumps(data).encode() if data is not None else None,
                                         headers=headers, method=method)
        for attempt in range(5):
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and attempt < 4:
                    try:
                        delay = float(json.load(exc)['retry_after'])
                    except (ValueError, KeyError, TypeError):
                        raise RuntimeError('Discord rate limit response was invalid') from None
                    if 0 <= delay <= 60:
                        time.sleep(delay + 0.2)
                        continue
                # Never stringify HTTPError: it contains the secret webhook URL.
                raise RuntimeError(f'Discord {method} failed (HTTP {exc.code}); inspect state before retrying') from None
            except (urllib.error.URLError, TimeoutError, OSError):
                raise RuntimeError('Discord request interrupted; inspect pending state before retrying') from None
        raise RuntimeError('Discord retry limit reached')


def save(path, state):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    temp.replace(path)


def publish(api, cards, state_path):
    check_cards(cards)
    state_path = Path(state_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    # Protect the read / publish / save sequence against concurrent invocations.
    with state_path.with_suffix('.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = json.loads(state_path.read_text()) if state_path.exists() else {
            'forum_id': FORUM, 'guild_id': GUILD, 'guides': {}}
        if state.get('forum_id') != FORUM or state.get('guild_id') != GUILD:
            raise ValueError('State destination is not the preview forum')
        if state.get('pending'):
            raise ValueError('A pending POST needs manual reconciliation before retrying')
        forum = api.call('GET', '/channels/' + FORUM)
        if forum.get('id') != FORUM or forum.get('guild_id') != GUILD or forum.get('type') != 15:
            raise ValueError('Live destination is not the expected preview forum')
        # Validate all persisted threads and messages BEFORE any mutations.
        for guide in state['guides'].values():
            thread = api.call('GET', '/channels/' + guide['thread_id'])
            if thread.get('parent_id') != FORUM or thread.get('guild_id') != GUILD or thread.get('type') != 11:
                raise ValueError('Saved thread destination is outside the preview forum')
            for mid in guide['messages'].values():
                message = api.call('GET', f"/channels/{guide['thread_id']}/messages/{mid}")
                if message.get('channel_id') != guide['thread_id'] or message.get('webhook_id') != state.get('webhook_id'):
                    raise ValueError('Saved message destination or webhook does not match')
        me = api.call('GET', '/users/@me')
        hooks = api.call('GET', '/channels/' + FORUM + '/webhooks')
        eligible = [h for h in hooks if h.get('name') == WEBHOOK_NAME and h.get('user', {}).get('id') == me['id']
                    and h.get('channel_id') == FORUM and h.get('guild_id') == GUILD and h.get('type') == 1]
        if state.get('webhook_id'):
            eligible = [h for h in eligible if h['id'] == state['webhook_id']]
            if not eligible:
                raise ValueError('Saved preview webhook no longer exists')
        if len(eligible) > 1:
            raise ValueError('Multiple preview webhooks require reconciliation')
        if eligible:
            hook = eligible[0]
        else:
            state['pending'] = {'operation': 'create-webhook'}
            save(state_path, state)
            hook = api.call('POST', '/channels/' + FORUM + '/webhooks', {'name': WEBHOOK_NAME})
        if hook.get('channel_id') != FORUM or hook.get('guild_id') != GUILD or not hook.get('token'):
            raise ValueError('Invalid preview webhook response')
        state['webhook_id'] = hook['id']
        state.pop('pending', None)
        save(state_path, state)
        api.webhook = '/webhooks/' + hook['id'] + '/' + hook['token']
        for key, entries in cards.items():
            guide = state['guides'].get(key)
            for slug, payload in entries:
                if guide and slug in guide['messages']:
                    continue
                # Index is finalized after its destinations exist. No broken jump
                # links or misleading destinations appear during creation.
                initial = copy.deepcopy(payload)
                # Engine clearing fields are for converting legacy messages.
                # New V2 webhook posts must omit legacy content and embeds.
                initial.pop('content', None)
                initial.pop('embeds', None)
                if any(token in json.dumps(initial) for token in ('[[JUMP:', '[[GUIDE:')):
                    initial['components'] = [{'type': 17, 'components': [{'type': 10, 'content':
                        '# ' + NAMES[key] + '\nPreparing this guide…'}]}]
                query = '?wait=true&with_components=true'
                if guide:
                    query += '&thread_id=' + guide['thread_id']
                else:
                    initial['thread_name'] = NAMES[key] + ' — Resources Preview'
                state['pending'] = {'operation': 'create-message', 'guide': key, 'slug': slug}
                save(state_path, state)
                sent = api.call('POST', query, initial, webhook=True)
                if not guide:
                    guide = {'thread_id': sent['channel_id'], 'messages': {}}
                    state['guides'][key] = guide
                if sent.get('channel_id') != guide['thread_id'] or sent.get('webhook_id') != hook['id']:
                    raise ValueError('Unexpected webhook message destination')
                guide['messages'][slug] = sent['id']
                state.pop('pending', None)
                save(state_path, state)
        # Resolve cross-guide navigation only after every thread exists.
        threads = {key: guide['thread_id'] for key, guide in state['guides'].items()}
        for key, entries in cards.items():
            guide = state['guides'][key]
            for slug, payload in entries:
                final = resolve(payload, guide['thread_id'], guide['messages'], threads)
                final.pop('content', None)
                final.pop('embeds', None)
                validate(final)
                api.call('PATCH', f"/messages/{guide['messages'][slug]}?thread_id={guide['thread_id']}&with_components=true",
                         final, webhook=True)
            guide['status'] = 'ready'
            save(state_path, state)
        return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish-preview', action='store_true')
    parser.add_argument('--state', type=Path, default=Path('local_docs/editing-resources/preview-state.json'))
    args = parser.parse_args()
    cards = build()
    for key, entries in cards.items():
        ids = {slug: '9' * 20 for slug, _ in entries}
        for slug, payload in entries:
            chars, count = validate(resolve(payload, '9' * 20, ids, {name: '9' * 20 for name in cards}))
            print(f'{key}/{slug}: {chars} chars, {count} components')
    if args.publish_preview:
        token = os.environ.get('BOT_TOKEN')
        if not token:
            raise ValueError('BOT_TOKEN is required for preview publication')
        state = publish(API(token), cards, args.state)
        for key, guide in state['guides'].items():
            print(f"{NAMES[key]}: https://discord.com/channels/{GUILD}/{guide['thread_id']}")


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as exc:
        raise SystemExit(str(exc)) from None
