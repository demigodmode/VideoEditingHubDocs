import copy
import importlib.util
import tempfile
import io
import urllib.error
from unittest.mock import patch
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load():
    path = ROOT / 'preview.py'
    assert path.exists(), 'preview publisher has not been implemented'
    spec = importlib.util.spec_from_file_location('preview', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class FakeAPI:
    def __init__(self, p):
        self.p = p
        self.messages = {}
        self.threads = {}
        self.calls = []
        self.counter = 2000000000000000000
        self.fail_post = False
        self.hook_exists = True
    def call(self, method, path, data=None, webhook=False):
        self.calls.append((method, path, copy.deepcopy(data)))
        if path == '/channels/' + self.p.FORUM:
            return {'id': self.p.FORUM, 'guild_id': self.p.GUILD, 'type': 15}
        if path == '/users/@me':
            return {'id': 'bot'}
        if path == '/channels/' + self.p.FORUM + '/webhooks':
            if method == 'GET':
                return [] if not self.hook_exists else [{'id': 'wh', 'token': 'secret', 'type': 1, 'channel_id': self.p.FORUM, 'guild_id': self.p.GUILD, 'user': {'id': 'bot'}, 'name': self.p.WEBHOOK_NAME}]
            if method == 'POST':
                self.hook_exists = True
                return {'id': 'wh', 'token': 'secret', 'type': 1, 'channel_id': self.p.FORUM, 'guild_id': self.p.GUILD}
        if method == 'GET' and path.startswith('/channels/'):
            parts = path.split('/')
            if len(parts) == 3:
                return self.threads[parts[2]]
            return self.messages[parts[4]]
        if method == 'POST' and webhook:
            if self.fail_post:
                raise RuntimeError('uncertain delivery')
            self.counter += 1
            mid = str(self.counter)
            if 'thread_name' in data:
                tid = mid
                self.threads[tid] = {'id': tid, 'parent_id': self.p.FORUM, 'guild_id': self.p.GUILD, 'type': 11}
            else:
                tid = path.split('thread_id=')[1].split('&')[0]
            result = dict(data, id=mid, channel_id=tid, webhook_id='wh')
            self.messages[mid] = result
            return result
        if method == 'PATCH' and webhook:
            mid = path.split('/messages/')[1].split('?')[0]
            self.messages[mid].update(copy.deepcopy(data))
            return self.messages[mid]
        raise AssertionError((method, path))

def cards():
    def payload(text):
        return {'content': '', 'embeds': [], 'flags': 32768, 'allowed_mentions': {'parse': []}, 'components': [{'type': 17, 'components': [{'type': 10, 'content': text}]}]}
    return {'resolve': [('index', payload('[Start]([[JUMP:start-here]])')), ('start-here', payload('Learn here'))]}

class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.p = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / 'state.json'
        self.api = FakeAPI(self.p)
    def test_preview_creates_once_and_resolves_links_in_correct_thread(self):
        self.p.publish(self.api, cards(), self.state)
        posts = sum(c[0] == 'POST' for c in self.api.calls)
        self.p.publish(self.api, cards(), self.state)
        self.assertEqual(posts, sum(c[0] == 'POST' for c in self.api.calls))
        first = next(iter(self.api.messages.values()))
        text = first['components'][0]['components'][0]['content']
        self.assertIn('/' + self.p.GUILD + '/' + first['channel_id'] + '/', text)
        self.assertNotIn('[[JUMP:', text)
        self.assertNotIn('secret', self.state.read_text())
    def test_new_v2_posts_omit_legacy_message_fields(self):
        self.p.publish(self.api, cards(), self.state)
        for method, path, data in self.api.calls:
            if method == 'POST' and 'wait=true' in path:
                self.assertNotIn('content', data)
                self.assertNotIn('embeds', data)

    def test_first_run_creates_dedicated_preview_webhook(self):
        self.api.hook_exists = False
        self.p.publish(self.api, cards(), self.state)
        hook_calls = [c for c in self.api.calls if c[0] == 'POST' and c[1].endswith('/webhooks')]
        self.assertEqual(1, len(hook_calls))
        self.assertEqual('/channels/' + self.p.FORUM + '/webhooks', hook_calls[0][1])
        self.assertEqual({'name': self.p.WEBHOOK_NAME}, hook_calls[0][2])
        self.assertNotIn('secret', self.state.read_text())

    def test_cross_guide_links_wait_until_target_thread_exists(self):
        source = cards()
        source['resolve'][0][1]['components'][0]['components'][0]['content'] += ' [[GUIDE:general]]'
        source['general'] = [('index', copy.deepcopy(source['resolve'][1][1]))]
        state = self.p.publish(self.api, source, self.state)
        thread = state['guides']['general']['thread_id']
        mid = state['guides']['resolve']['messages']['index']
        rendered = self.api.messages[mid]['components'][0]['components'][0]['content']
        self.assertIn('/' + self.p.GUILD + '/' + thread, rendered)
        self.assertNotIn('[[GUIDE:', rendered)
        before = len(self.api.messages)
        self.p.publish(self.api, source, self.state)
        self.assertEqual(before, len(self.api.messages))

    def test_wrong_forum_state_is_rejected_before_network(self):
        self.state.write_text('{"forum_id": "1284644414173483040", "guild_id": "' + self.p.GUILD + '"}')
        with self.assertRaisesRegex(ValueError, 'destination'):
            self.p.publish(self.api, cards(), self.state)
        self.assertEqual([], self.api.calls)
    def test_uncertain_post_blocks_retry_to_prevent_duplicates(self):
        self.api.fail_post = True
        with self.assertRaises(RuntimeError):
            self.p.publish(self.api, cards(), self.state)
        self.api.fail_post = False
        previous = len(self.api.calls)
        with self.assertRaisesRegex(ValueError, 'pending'):
            self.p.publish(self.api, cards(), self.state)
        self.assertEqual(previous, len(self.api.calls))
    def test_message_outside_preview_thread_cannot_be_edited(self):
        self.p.publish(self.api, cards(), self.state)
        thread = next(iter(self.api.threads.values()))
        thread['parent_id'] = '1284644414173483040'
        self.api.calls.clear()
        with self.assertRaisesRegex(ValueError, 'destination'):
            self.p.publish(self.api, cards(), self.state)
        self.assertFalse(any(c[0] in ('PATCH', 'POST') for c in self.api.calls))
    def test_limits_and_missing_jumps_fail_before_publication(self):
        bad = cards()
        bad['resolve'][0][1]['components'][0]['components'][0]['content'] = 'x' * 4001
        with self.assertRaisesRegex(ValueError, '4000'):
            self.p.publish(self.api, bad, self.state)
        with self.assertRaisesRegex(ValueError, 'jump'):
            self.p.resolve(cards()['resolve'][0][1], 'thread', {})
        self.assertEqual([], self.api.calls)

class HTTPTests(unittest.TestCase):
    def test_http_failure_never_exposes_webhook_token(self):
        p = load()
        api = p.API('BOT_SECRET')
        api.webhook = '/webhooks/123/WEBHOOK_SECRET'
        error = urllib.error.HTTPError('https://discord.com/api/v10/webhooks/123/WEBHOOK_SECRET',
                                       400, 'bad request', {}, io.BytesIO(b'{}'))
        with patch.object(p.urllib.request, 'urlopen', side_effect=error):
            with self.assertRaisesRegex(RuntimeError, 'HTTP 400') as ctx:
                api.call('POST', '?wait=true', {}, webhook=True)
        error.close()
        self.assertNotIn('SECRET', str(ctx.exception))
    def test_every_guide_index_has_consistent_section_link_buttons(self):
        p = load()
        expected = {'resolve': 7, 'premiere': 4, 'after-effects': 4, 'scene-packs': 8, 'general': 7}
        for key, entries in p.build().items():
            components = entries[0][1]['components'][0]['components']
            self.assertTrue(any(c.get('content') == '**Browse this guide**' for c in components), key)
            rows = [c for c in components if c['type'] == 1]
            buttons = [b for row in rows for b in row['components']]
            self.assertEqual(expected[key], len(buttons), key)
            self.assertTrue(all(1 <= len(row['components']) <= 5 for row in rows))
            self.assertTrue(all(1 <= len(b['label']) <= 80 for b in buttons))
            self.assertTrue(all(b['style'] == 5 and b['url'].startswith(('[[JUMP:', '[[GUIDE:')) for b in buttons))
            self.assertFalse(any('[[JUMP:' in c.get('content', '') for c in components))

    def test_component_limit_counts_nested_components(self):
        p = load()
        payload = cards()['resolve'][1][1]
        payload['components'][0]['components'] = [{'type': 14}] * 40
        with self.assertRaisesRegex(ValueError, '40 components'):
            p.validate(payload)
    def test_links_are_counted_after_expansion(self):
        p = load()
        payload = cards()['resolve'][0][1]
        payload['components'][0]['components'][0]['content'] = 'x' * 3950 + '[[JUMP:start-here]]'
        with self.assertRaisesRegex(ValueError, '4000'):
            p.check_cards({'resolve': [('index', payload), cards()['resolve'][1]]})

if __name__ == '__main__':
    unittest.main()
