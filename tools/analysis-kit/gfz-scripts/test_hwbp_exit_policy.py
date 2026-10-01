"""Setup failure controls; live debugger-loss evidence is separate in EXP-017."""
import contextlib
import ctypes
import io
import unittest
from unittest.mock import patch

import hwbp


class API:
    def __init__(self, attach=1, policy=1, detach=1):
        self.results = [attach, policy, detach]
        self.calls = []

    def call(self, name, value, index):
        self.calls.append((name, value))
        ctypes.set_last_error([5, 6, 87][index])
        return self.results[index]

    def DebugActiveProcess(self, pid):
        return self.call('attach', pid, 0)

    def DebugSetProcessKillOnExit(self, flag):
        return self.call('policy', flag, 1)

    def DebugActiveProcessStop(self, pid):
        return self.call('detach', pid, 2)


class Setup(unittest.TestCase):
    def test_success_connects_before_setting_policy(self):
        api = API()
        with patch.object(hwbp, 'k32', api):
            hwbp.attach_with_exit_policy(123)
        self.assertEqual(api.calls, [('attach', 123), ('policy', False)])

    def test_attach_failure_never_sets_policy_or_detaches(self):
        api = API(attach=0)
        with patch.object(hwbp, 'k32', api), self.assertRaises(OSError) as caught:
            hwbp.attach_with_exit_policy(123)
        self.assertEqual(caught.exception.errno, 5)
        self.assertEqual(api.calls, [('attach', 123)])

    def test_policy_failure_aborts_main_before_context_or_event_work(self):
        api = API(policy=0)
        output = io.StringIO()
        with patch.object(hwbp, 'k32', api), patch.object(hwbp, 'cpu_seconds', return_value=0), \
                patch('sys.argv', ['hwbp', '--pid', '123', '--no-arm']), \
                contextlib.redirect_stderr(output), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(hwbp.main(), 3)
        self.assertEqual(api.calls, [('attach', 123), ('policy', False), ('detach', 123)])
        self.assertIn('detached before event/context work', output.getvalue())

    def test_policy_and_detach_errors_both_survive(self):
        api = API(policy=0, detach=0)
        with patch.object(hwbp, 'k32', api), self.assertRaises(OSError) as caught:
            hwbp.attach_with_exit_policy(123)
        self.assertEqual(caught.exception.errno, 6)
        self.assertIn('detach also failed (87)', str(caught.exception))


if __name__ == '__main__':
    unittest.main(verbosity=2)
