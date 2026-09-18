#!/usr/bin/env python3
"""Publish approved resource guides to the fixed public forum, preserving original IDs.

Requires --publish-public and a persistent journal. Preview publication remains
separate. Never discard a pending operation: reconcile its message ID first.
"""
import argparse
import copy
import fcntl
import json
import os
from pathlib import Path
from preview import API, GUILD, NAMES, build, check_cards, resolve, save, validate

FORUM = '1284644414173483040'
WEBHOOK_ID = '1284707991332847687'


def initial_state():
    return {'forum_id': FORUM, 'guild_id': GUILD, 'webhook_id': WEBHOOK_ID,
            'guides': {
                'resolve': {'thread_id': '1288518149506863227', 'messages': {
                    'start-here': '1288518149506863227',
                    'video-tools': '1288522017468846224',
                    'delivery-tools': '1288522416326312007'}},
                'premiere': {'thread_id': '1285022716331819030', 'messages': {
                    'index': '1285022716331819030',
                    'assets': '1285033213294547005',
                    'learn-a-skill': '1285034520747184230'}},
                'scene-packs': {'thread_id': '1346261762063863880', 'messages': {
                    'index': '1346261762063863880'}}}}


def publish(api, cards, state_path):
    check_cards(cards)
    state_path = Path(state_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    # Protect the read / publish / save sequence against concurrent invocations.
    with state_path.with_suffix('.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = json.loads(state_path.read_text()) if state_path.exists() else initial_state()
        if state.get('forum_id') != FORUM or state.get('guild_id') != GUILD:
            raise ValueError('State destination is not the public resources forum')
        if state.get('pending'):
            raise ValueError('A pending POST needs manual reconciliation before retrying')
        forum = api.call('GET', '/channels/' + FORUM)
        if forum.get('id') != FORUM or forum.get('guild_id') != GUILD or forum.get('type') != 15:
            raise ValueError('Live destination is not the expected public resources forum')
        # Validate all persisted threads and messages BEFORE any mutations.
        for guide in state['guides'].values():
            thread = api.call('GET', '/channels/' + guide['thread_id'])
            if thread.get('parent_id') != FORUM or thread.get('guild_id') != GUILD or thread.get('type') != 11:
                raise ValueError('Saved thread destination is outside the public resources forum')
            for mid in guide['messages'].values():
                message = api.call('GET', f"/channels/{guide['thread_id']}/messages/{mid}")
                if message.get('channel_id') != guide['thread_id'] or message.get('webhook_id') != state.get('webhook_id'):
                    raise ValueError('Saved message destination or webhook does not match')
        hooks = api.call('GET', '/channels/' + FORUM + '/webhooks')
        eligible = [h for h in hooks if h.get('id') == WEBHOOK_ID
                    and h.get('channel_id') == FORUM and h.get('guild_id') == GUILD
                    and h.get('type') == 1 and h.get('token')]
        if len(eligible) != 1 or state.get('webhook_id') != WEBHOOK_ID:
            raise ValueError('Original public webhook is unavailable or state differs')
        hook = eligible[0]
        if hook.get('name') != 'Video Editing Hub' or not hook.get('avatar'):
            raise ValueError('Public webhook must use Video Editing Hub branding and its logo')
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
                    initial['thread_name'] = NAMES[key] if key == 'general' else NAMES[key] + ' Resources'
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
                # Explicitly clear classic fields when converting original messages.
                final['content'] = ''
                final['embeds'] = []
                validate(final)
                api.call('PATCH', f"/messages/{guide['messages'][slug]}?thread_id={guide['thread_id']}&with_components=true",
                         final, webhook=True)
            guide['status'] = 'ready'
            save(state_path, state)
        return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish-public', action='store_true')
    parser.add_argument('--state', type=Path, required=True)
    args = parser.parse_args()
    cards = build()
    if not args.publish_public:
        print('Validated', sum(map(len, cards.values())), 'cards; no Discord changes.')
        return
    if not args.state.exists():
        raise ValueError('Use the existing public state journal; do not initialize a replacement')
    token = os.environ.get('BOT_TOKEN')
    if not token:
        raise ValueError('BOT_TOKEN is required')
    state = publish(API(token), cards, args.state)
    for key, guide in state['guides'].items():
        print(NAMES[key], 'https://discord.com/channels/' + GUILD + '/' + guide['thread_id'])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as exc:
        raise SystemExit(str(exc)) from None
