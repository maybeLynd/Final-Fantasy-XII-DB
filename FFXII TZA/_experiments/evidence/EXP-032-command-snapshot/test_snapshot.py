"""Synthetic byte controls only; no game-state validation."""
import struct
import unittest
from command_snapshot import FRAME,snapshot


class Reader:
    def __init__(self,kind='normal'):
        self.kind=kind
        self.reads=[]
        self.header=bytearray(24)
        self.header[0]=1
        struct.pack_into('<Q',self.header,16,0x456789AB)
        self.blocks=bytearray(48)
        struct.pack_into('<I',self.blocks,0,0xDDBBCCAA)
        struct.pack_into('<Q',self.blocks,8,0xFEDCBA9876543210)
        struct.pack_into('<I',self.blocks,16,0x87654321)
        struct.pack_into('<H',self.blocks,20,0xBEEF)
        struct.pack_into('<Q',self.blocks,32,0x0123456789ABCDEF)
        struct.pack_into('<I',self.blocks,40,0xAABBCCDD)
        struct.pack_into('<H',self.blocks,44,0x1234)
    def read(self,address,size):
        self.reads.append((address,size))
        if address==FRAME:
            return struct.pack('<I',11 if self.kind=='crossed' and len(self.reads)>1 else 10)
        if address==0x1000:
            if self.kind=='reused' and len(self.reads)>2:self.header[16]^=1
            return bytes(self.header)
        if address==0x1EA9:return b'\x01' if self.kind=='slot' else b'\x00'
        if address==0x16B4:return b'\x05\xAA\x09'
        if address==0x1700:
            if self.kind=='short':return bytes(self.blocks[:-1])
            if self.kind=='unreadable':return None
            return bytes(self.blocks)
        raise AssertionError((address,size))


class Tests(unittest.TestCase):
    def test_widths_offsets_and_shadow_are_distinct(self):
        reader=Reader()
        r=snapshot(reader,0x1000,0,0x456789AB)
        self.assertEqual(r['live']['action_context'],0xFEDCBA9876543210)
        self.assertEqual(r['live']['target_focus_handle'],0x87654321)
        self.assertEqual(r['live']['action_id'],0xBEEF)
        self.assertEqual(r['shadow']['action_context'],0x0123456789ABCDEF)
        self.assertEqual(r['shadow']['target_focus_handle'],0xAABBCCDD)
        self.assertEqual(r['shadow']['action_id'],0x1234)
        self.assertEqual((r['action_phase'],r['unnamed_6b6']),(5,9))
        self.assertEqual(reader.reads,[(FRAME,4),(0x1000,24),(0x1EA9,1),(0x16B4,3),
                                       (0x1700,48),(0x1000,24),(0x1EA9,1),(FRAME,4)])
    def test_invalid_reads_and_identity_never_return_snapshot(self):
        for kind in ['short','unreadable','reused','slot']:
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                snapshot(Reader(kind),0x1000,0,0x456789AB)
    def test_cross_frame_is_retained_not_hidden(self):
        r=snapshot(Reader('crossed'),0x1000,0,0x456789AB)
        self.assertEqual((r['frame_before'],r['frame_after']),(10,11))
        self.assertTrue(r['crossed_frame'])
    def test_sentinel_and_shadow_persistence_without_cancellation_claim(self):
        for context in [0,0xFFFFFFFFFFFFFFFF]:
            reader=Reader()
            struct.pack_into('<Q',reader.blocks,8,context)
            r=snapshot(reader,0x1000,0,0x456789AB)
            self.assertTrue(r['live']['context_is_sentinel'])
            self.assertFalse(r['shadow']['context_is_sentinel'])


if __name__=='__main__':unittest.main()
