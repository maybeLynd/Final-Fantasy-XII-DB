"""Offline control boundaries; fake memory/time, real on-disk authority bytes."""
import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

import observe as observer


class Clock:
    def __init__(self):
        self.now = 0

    def read(self):
        return self.now

    def sleep(self, duration):
        self.now += duration


def observation(hp=103, unit=100, actor=200):
    player = dict(unit=unit, actor=actor, hp=hp)
    return dict(status='CONSISTENT_SAMPLE', player_before=player,
                player_after=[copy.deepcopy(player)], target_before=None, target_after=None)


class CaptureTests(unittest.TestCase):
    def run_case(self, rows, seconds=.15):
        clock = Clock()
        samples = iter(rows)
        return observer.capture(None, lambda *a, **k: next(samples), seconds, 0, 35,
                                clock=clock.read, sleep=clock.sleep)

    def test_bounded_positive_preserves_selected_sample(self):
        row = observation()
        result = self.run_case([row] * 4)
        self.assertEqual(result['status'], 'OBSERVED')
        self.assertEqual(len(result['samples']), 3)
        self.assertEqual(result['samples'][0]['observation'], row)

    def test_health_loss_and_floor_stop_immediately(self):
        for rows in ([observation(), observation(102)], [observation(34)]):
            result = self.run_case(rows)
            self.assertEqual(result['status'], 'HEALTH_STOP')
            self.assertEqual(len(result['samples']), len(rows))
        row = observation()
        row['player_after'][0]['hp'] = 102
        self.assertEqual(self.run_case([row])['status'], 'HEALTH_STOP')

    def test_player_reuse_between_samples_is_invalid(self):
        result = self.run_case([observation(), observation(unit=101)])
        self.assertEqual(result['status'], 'INVALID')
        self.assertIn('identity changed', result['error'])

    def test_ambiguous_missing_and_unreadable_fail(self):
        rows = [observation(), observation(), observation()]
        rows[0]['status'] = 'AMBIGUOUS_SELECTION'
        rows[1]['player_after'] = []
        rows[2]['player_before']['hp'] = None
        for row in rows:
            result = self.run_case([row])
            self.assertEqual(result['status'], 'INVALID')
            self.assertEqual(len(result['samples']), 1)
        self.assertEqual(self.run_case([])['status'], 'INVALID')

    def test_duration_and_zero_samples_fail(self):
        for duration in (0, -1, 5.01, float('nan'), float('inf')):
            self.assertEqual(self.run_case([], duration)['status'], 'INVALID')
        ticks = iter([0, 1])
        result = observer.capture(None, None, .1, 0, 35, clock=lambda: next(ticks))
        self.assertEqual(result['status'], 'INVALID')
        self.assertIn('no samples', result['error'])

    def test_sample_cap_even_if_clock_stalls(self):
        result = observer.capture(None, lambda *a, **k: observation(), 5, 0, 35,
                                  clock=lambda: 0, sleep=lambda x: None)
        self.assertEqual(len(result['samples']), 100)
        self.assertTrue(result['sample_cap_reached'])

    def test_cli_failure_receipt_and_exclusive_output_without_os_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'invalid.json'
            with patch('sys.argv', ['observe.py', '--pid', '1', '--seconds', '0', '--out', str(output)]):
                self.assertEqual(observer.main(), 3)
                self.assertEqual(json.loads(output.read_text())['status'], 'INVALID')
                original = output.read_bytes()
                with self.assertRaises(FileExistsError):
                    observer.main()
                self.assertEqual(output.read_bytes(), original)


class QualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = observer.EXE.read_bytes()
        pe = struct.unpack_from('<I', cls.raw, 0x3C)[0]
        count = struct.unpack_from('<H', cls.raw, pe + 6)[0]
        table = pe + 24 + struct.unpack_from('<H', cls.raw, pe + 20)[0]
        cls.memory = {0x1CCD300: b'\x19\x93\r\n\x1a\n'}
        for n in range(count):
            offset = table + n * 40
            if cls.raw[offset:offset + 8].rstrip(b'\0') == b'.text':
                virtual, rva, size, disk = struct.unpack_from('<4I', cls.raw, offset + 8)
                cls.text_address = 0x120000 + rva
                cls.memory[cls.text_address] = cls.raw[disk:disk + min(virtual, size)]

    def qualify(self, raw=None, base=0x120000, verdict='clean', modules=None, memory=None):
        data = self.memory if memory is None else memory
        class Reader:
            def read(self, address, size):
                return data[address][:size]
        return observer.qualify(Reader(), self.raw if raw is None else raw, base, verdict,
                                [{'name': 'synthetic inventory'}] if modules is None else modules,
                                0x1CCD300, self.memory[0x1CCD300])

    def test_real_disk_bytes_positive_against_fake_memory(self):
        result = self.qualify()
        self.assertEqual(result['code_identity'][0]['bytes'], 7996981)
        self.assertEqual(result['code_identity'][0]['live_sha256'], observer.TEXT_SHA)

    def test_executable_base_and_module_failures(self):
        for kwargs in (dict(raw=self.raw[:-1]), dict(base=0), dict(verdict='contaminated'), dict(modules=[])):
            with self.subTest(kwargs=list(kwargs)), self.assertRaises(ValueError):
                self.qualify(**kwargs)

    def test_control_short_and_changed_live_text_fail(self):
        for address, replacement in ((0x1CCD300, b'bad'), (self.text_address, b''),
                                     (self.text_address, b'X' + self.memory[self.text_address][1:])):
            data = dict(self.memory)
            data[address] = replacement
            with self.subTest(address=address, size=len(replacement)), self.assertRaises(ValueError):
                self.qualify(memory=data)

    def test_pinned_dependencies_and_source_receipts(self):
        self.assertTrue(observer.receipts())
        with patch.object(observer, 'sha', return_value='changed'):
            with self.assertRaisesRegex(ValueError, 'dependency changed'):
                observer.receipts()


if __name__ == '__main__':
    unittest.main(verbosity=2)
