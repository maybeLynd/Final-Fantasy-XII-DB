import ctypes
import struct
import unittest
from types import SimpleNamespace
from stack_receipt import snapshot


class Tests(unittest.TestCase):
    def test_exact_bytes_and_high_bits(self):
        words=[0xFEDCBA9876543210,0,1,2,3,4,5,0xFFFFFFFFFFFFFFFF]
        def read(handle,address,buffer,size,count):
            self.assertEqual((handle,address,size),(7,0x1000,64))
            ctypes.memmove(buffer,struct.pack('<8Q',*words),64)
            count._obj.value=64
            return 1
        result=snapshot(SimpleNamespace(ReadProcessMemory=read),7,0x1000)
        self.assertEqual(result['status'],'READ')
        self.assertEqual(result['qwords'],words)
        self.assertEqual(result['raw'],struct.pack('<8Q',*words).hex())

    def test_invalid_range_does_not_read(self):
        for address in (None,0,-1,2**64-63,2**64):
            self.assertEqual(snapshot(None,7,address)['status'],'INVALID')

    def test_api_exception_and_impossible_count(self):
        def throwing(*args):raise OSError('fixture')
        def excessive(handle,address,buffer,size,count):
            count._obj.value=65
            return 1
        for read in (throwing,excessive):
            result=snapshot(SimpleNamespace(ReadProcessMemory=read),7,0x1000)
            self.assertEqual(result['status'],'INVALID')
            self.assertNotIn('top_qword',result)


if __name__=='__main__':unittest.main(verbosity=2)
