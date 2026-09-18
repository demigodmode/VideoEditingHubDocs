import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from test_preview import FakeAPI, ROOT

sys.path.insert(0, str(ROOT))
import public as p

class PublicAPI(FakeAPI):
    def __init__(self):
        super().__init__(p)
        for guide in p.initial_state()['guides'].values():
            tid = guide['thread_id']
            self.threads[tid] = {'id': tid, 'parent_id': p.FORUM, 'guild_id': p.GUILD, 'type': 11}
            for mid in guide['messages'].values():
                self.messages[mid] = {'id': mid, 'channel_id': tid, 'webhook_id': p.WEBHOOK_ID,
                                      'embeds': [{'title': 'legacy'}], 'content': 'legacy'}
        self.messages['member'] = {'id': 'member', 'content': 'Keep this reply'}
    def call(self, method, path, data=None, webhook=False):
        if path == '/channels/' + p.FORUM + '/webhooks':
            self.calls.append((method, path, copy.deepcopy(data)))
            assert method == 'GET'
            return [{'id': p.WEBHOOK_ID, 'token': 'secret', 'channel_id': p.FORUM,
                     'guild_id': p.GUILD, 'type': 1, 'name': 'Video Editing Hub', 'avatar': 'veh-logo'}]
        result = super().call(method, path, data, webhook)
        if method == 'POST' and webhook:
            result['webhook_id'] = p.WEBHOOK_ID
        return result

class PublicTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / 'state.json'
        self.api = PublicAPI()
    def test_migration_preserves_ids_member_reply_and_clears_embeds(self):
        original = p.initial_state()
        member = copy.deepcopy(self.api.messages['member'])
        state = p.publish(self.api, p.build(), self.state)
        self.assertEqual(member, self.api.messages['member'])
        for key, guide in original['guides'].items():
            for slug, mid in guide['messages'].items():
                self.assertEqual(mid, state['guides'][key]['messages'][slug])
                self.assertEqual([], self.api.messages[mid]['embeds'])
                self.assertEqual(32768, self.api.messages[mid]['flags'])
        self.assertEqual(5, len(state['guides']))
        posts = sum(c[0] == 'POST' for c in self.api.calls)
        p.publish(self.api, p.build(), self.state)
        self.assertEqual(posts, sum(c[0] == 'POST' for c in self.api.calls))
        self.assertNotIn('secret', self.state.read_text())
    def test_preview_state_rejected_before_network(self):
        self.state.write_text(json.dumps({'forum_id':'1480680276446154983','guild_id':p.GUILD}))
        with self.assertRaises(ValueError): p.publish(self.api,p.build(),self.state)
        self.assertEqual([],self.api.calls)
    def test_wrong_owner_blocks_all_writes(self):
        self.api.messages['1285033213294547005']['webhook_id'] = 'other'
        with self.assertRaises(ValueError): p.publish(self.api,p.build(),self.state)
        self.assertFalse(any(c[0] != 'GET' for c in self.api.calls))
    def test_pending_delivery_blocks_retry(self):
        self.api.fail_post=True
        with self.assertRaises(RuntimeError): p.publish(self.api,p.build(),self.state)
        before=len(self.api.calls)
        with self.assertRaisesRegex(ValueError,'pending'): p.publish(self.api,p.build(),self.state)
        self.assertEqual(before,len(self.api.calls))
