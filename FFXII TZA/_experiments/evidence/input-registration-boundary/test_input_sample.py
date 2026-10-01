"""Byte/identity controls only. This does not execute FF12 or certify live detection."""
import struct
import unittest
import input_sample as sample


class Reader:
    def __init__(self):
        # Deliberately above 4GiB: a narrowed pointer must not pass this fixture.
        self.manager, self.backend, self.device = 0x123000000, 0x234000000, 0x345000000
        self.array = self.device + 0x30
        raw = bytearray(256)
        raw[36], raw[49], raw[255] = 1, 0x7F, 0x80
        self.memory = {
            sample.MANAGER: struct.pack('<Q', self.manager),
            self.manager + 0xDF8: struct.pack('<Q', self.backend),
            self.backend + 0x118: struct.pack('<Q', self.device),
            sample.FRAME: struct.pack('<I', 0xFFFFFFFE), self.array: bytes(raw),
        }
        self.calls = []

    def read(self, address, size):
        self.calls.append((address, size))
        return self.memory[address]


class Controls(unittest.TestCase):
    def test_distinctive_raw_bytes_and_high_pointer(self):
        reader = Reader()
        row = sample.snapshot(reader)
        self.assertEqual(row['status'], 'STABLE_CHAIN')
        self.assertEqual(row['array_address'], reader.array)
        self.assertEqual(bytes.fromhex(row['raw']), reader.memory[reader.array])
        self.assertEqual(row['nonzero_indices'], [36, 49, 255])
        self.assertEqual(reader.calls, [(sample.FRAME, 4), (sample.MANAGER, 8),
            (reader.manager + 0xDF8, 8), (reader.backend + 0x118, 8),
            (reader.array, 256), (sample.MANAGER, 8), (reader.manager + 0xDF8, 8),
            (reader.backend + 0x118, 8), (sample.FRAME, 4)])

    def test_zero_is_preserved_without_negative_verdict(self):
        reader = Reader()
        reader.memory[reader.array] = bytes(256)
        row = sample.snapshot(reader)
        self.assertEqual(row['nonzero_indices'], [])
        self.assertEqual(row['status'], 'STABLE_CHAIN')
        self.assertNotIn('registered', row)

    def test_changed_chain_retains_original_bytes(self):
        reader = Reader()
        original_read = reader.read
        def read(address, size):
            if address == reader.backend + 0x118 and len(reader.calls) > 4:
                reader.memory[address] = struct.pack('<Q', reader.device + 0x1000)
            return original_read(address, size)
        reader.read = read
        row = sample.snapshot(reader)
        self.assertEqual(row['status'], 'CHANGED_CHAIN')
        self.assertEqual(row['array_address_after'], reader.array + 0x1000)
        self.assertEqual(bytes.fromhex(row['raw']), reader.memory[reader.array])

    def test_null_and_partial_reads_rejected(self):
        for address_kind, raw in [('manager', bytes(8)), ('device', b'\x01' * 7),
                                  ('array', bytes(255)), ('array', None)]:
            reader = Reader()
            address = dict(manager=sample.MANAGER, device=reader.backend + 0x118,
                           array=reader.array)[address_kind]
            reader.memory[address] = raw
            with self.subTest(address_kind=address_kind, raw_type=type(raw).__name__):
                with self.assertRaises(ValueError):
                    sample.snapshot(reader)


if __name__ == '__main__':
    unittest.main(verbosity=2)
