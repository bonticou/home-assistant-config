"""Safety boundaries and failure recovery for the administrative bridge."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('admin', ROOT / 'addons/codex_ha_admin/server.py')
admin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admin)
client_spec = importlib.util.spec_from_file_location('client', ROOT / 'tools/ha_admin_mcp.py')
client = importlib.util.module_from_spec(client_spec)
client_spec.loader.exec_module(client)


class AdminTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = self.root / 'config'
        self.config.mkdir()
        self.data = self.root / 'data'
        self.data.mkdir()
        for name, value in [('CONFIG', self.config), ('DATA', self.data)]:
            p = patch.object(admin, name, value)
            p.start(); self.addCleanup(p.stop)
        self.file = self.config / 'scripts.yaml'
        self.file.write_text('old: {}\n')
        self.before = self.file.read_bytes()
        self.check = patch.object(admin, 'config_check', return_value={'result': 'ok'})
        self.mock_check = self.check.start(); self.addCleanup(self.check.stop)
        self.reload = patch.object(admin, 'reload_domains', return_value={})
        self.mock_reload = self.reload.start(); self.addCleanup(self.reload.stop)

    def plan(self, content='new: {}\n'):
        return admin.prepare([{'path': 'scripts.yaml', 'content': content,
                               'expected_sha256': admin.digest(self.before)}])['plan_id']

    def test_path_and_symlink_boundaries(self):
        for name in ['../configuration.yaml', '/config/scripts.yaml', '.storage/auth',
                     'secrets.yaml', 'tools/run.py', 'dashboards/../scripts.yaml']:
            with self.assertRaises(ValueError): admin.safe_path(name)
        (self.config / 'dashboards').symlink_to(self.root)
        with self.assertRaises(ValueError): admin.safe_path('dashboards/test.yaml')

    def test_prepare_does_not_write_and_checks_drift_and_yaml(self):
        plan = self.plan()
        self.assertEqual(self.file.read_bytes(), self.before)
        self.assertEqual(admin.get_plan(plan)['status'], 'prepared')
        self.file.write_text('external: {}\n')
        with self.assertRaises(ValueError): self.plan()
        self.file.write_bytes(self.before)
        with self.assertRaises(Exception): self.plan('broken: [')

    def test_apply_rejects_stale_hash_and_unsupported_reload_before_writing(self):
        plan = self.plan()
        with self.assertRaises(ValueError): admin.apply_plan(plan, ['homeassistant'])
        self.assertEqual(self.file.read_bytes(), self.before)
        self.file.write_text('external: {}\n')
        with self.assertRaises(ValueError): admin.apply_plan(plan, [])
        self.assertEqual(self.file.read_text(), 'external: {}\n')

    def test_apply_validates_and_rollback_restores(self):
        plan = self.plan()
        result = admin.apply_plan(plan, ['script'])
        self.assertEqual(result['status'], 'applied')
        self.assertEqual(self.file.read_text(), 'new: {}\n')
        self.assertEqual(self.mock_check.call_count, 2)
        admin.rollback(plan, ['script'])
        self.assertEqual(self.file.read_bytes(), self.before)

    def test_validation_failure_restores_without_reload(self):
        plan = self.plan()
        self.mock_check.side_effect = [{'result': 'ok'}, ValueError('invalid config')]
        result = admin.apply_plan(plan, ['script'])
        self.assertEqual(result['status'], 'validation_failed_restored')
        self.assertEqual(self.file.read_bytes(), self.before)
        self.mock_reload.assert_not_called()

    def test_external_change_blocks_rollback(self):
        plan = self.plan()
        admin.apply_plan(plan, [])
        self.file.write_text('external: {}\n')
        with self.assertRaises(ValueError): admin.rollback(plan, [])
        self.assertEqual(self.file.read_text(), 'external: {}\n')

    def test_interrupted_batch_is_recoverable_and_blocks_new_deploys(self):
        plan_id = self.plan()
        plan = admin.get_plan(plan_id)
        plan['status'] = 'applying'; admin.save_plan(plan)
        admin.write_version(plan['files'][0], 'after')
        self.assertEqual(admin.pending_recovery(), [plan_id])
        with self.assertRaises(ValueError): self.plan()
        admin.rollback(plan_id, [])
        self.assertEqual(self.file.read_bytes(), self.before)
        self.assertEqual(admin.pending_recovery(), [])

    def test_new_file_removed_on_rollback(self):
        plan = admin.prepare([{'path': 'dashboards/test.yaml', 'content': 'views: []\n',
                               'expected_sha256': None}])['plan_id']
        admin.apply_plan(plan, [])
        self.assertTrue((self.config / 'dashboards/test.yaml').exists())
        admin.rollback(plan, [])
        self.assertFalse((self.config / 'dashboards/test.yaml').exists())

    def test_expired_plan_and_duplicate_files_rejected(self):
        plan_id = self.plan()
        plan = admin.get_plan(plan_id); plan['created'] = 0; admin.save_plan(plan)
        with self.assertRaises(ValueError): admin.apply_plan(plan_id, [])
        item = {'path': 'scripts.yaml', 'content': 'new: {}\n', 'expected_sha256': admin.digest(self.before)}
        with self.assertRaises(ValueError): admin.prepare([item, item])

    def test_protocol_and_redaction(self):
        result = client.handle({'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18'}})
        self.assertEqual(result['result']['protocolVersion'], '2025-06-18')
        self.assertIsNone(client.handle({'method': 'notifications/initialized'}))
        tools = client.handle({'id': 2, 'method': 'tools/list'})['result']['tools']
        self.assertEqual(len(tools), 10)
        redacted = admin.redact({'access_token': 'secret', 'log': 'Authorization: Bearer abc.xyz'})
        self.assertNotIn('secret', json.dumps(redacted))
        self.assertNotIn('abc.xyz', json.dumps(redacted))


if __name__ == '__main__':
    unittest.main()
