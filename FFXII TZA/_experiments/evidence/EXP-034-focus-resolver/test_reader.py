"""Compare read helper with all saved original-chain fixtures, plus read failures."""
import json
from pathlib import Path
import struct
import unittest
from reader_resolver import resolve


class Reader:
    def __init__(self,p):
        self.memory={}
        slot=0x2098E10+p['manager']*0x288
        for address,fmt,value in [(0x2089340,'<B',p['gate']),(slot+8,'<Q',p['vector']),
            (slot,'<Q',p['storage']),(slot+0x20,'<i',p['capacity']),(slot+0x10,'<B',p['enabled']),
            (0x50000000,'<i',p['count']),(0x50000010,'<Q',p['entry']),
            (0x50001016,'<H',p['word']),(0x50001030,'<Q',p['unit'])]:
            self.memory[address]=struct.pack(fmt,value)
    def read(self,address,size):return self.memory.get(address)


class Tests(unittest.TestCase):
    def cases(self):return json.loads(Path(__file__).with_name('result.json').read_text())['results']
    def test_matches_all_original_return_values(self):
        for case in self.cases():
            with self.subTest(case=case['name']):
                result=resolve(Reader(case['fixture']),case['handle'])
                self.assertEqual(result['unit'],case['actual'])
                self.assertEqual(result['actor'],case['resolved_actors'][0] if case['resolved_actors'] else 0)
    def test_unreadable_and_short_discriminator_are_errors(self):
        case=self.cases()[0]
        for value in [None,b'\x07']:
            r=Reader(case['fixture']);r.memory[0x50001016]=value
            with self.assertRaises(ValueError):resolve(r,case['handle'])
    def test_invalid_handle_width_rejected(self):
        for handle in [-1,0x100000000]:
            with self.assertRaises(ValueError):resolve(None,handle)


if __name__=='__main__':unittest.main()
