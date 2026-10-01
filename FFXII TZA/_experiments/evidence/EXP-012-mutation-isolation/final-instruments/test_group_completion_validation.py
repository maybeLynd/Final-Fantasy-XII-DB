"""Adversarial controls for the differential instrument, not a model of group semantics."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import diff_group_completion as d


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(case=0, unit=d.UNITS_VA, **{'return': 1}, memory='0000000000000001',
                           calls=[dict(target=a, args=[1], memory='0000000000000002') for a in d.STUBS[:3]] +
                           [dict(target=d.DISPATCH_VA,args=[d.UNITS_VA,0x2005,0],memory='0000000000000001')])

    def output(self, records):
        return 'SCHEMA GROUP_COMPLETION_V2\n'+'\n'.join(json.dumps(r) for r in records)+'\nDIGEST 0000000000000001\n'

    def test_census_before_pairing(self):
        valid = self.output([self.record])
        self.assertEqual(d.parse_driver(valid,[d.UNITS_VA])[0],[self.record])
        for text in [self.output([]),self.output([self.record,self.record]),valid+'junk\n',
                     valid.replace('DIGEST 0000000000000001\n',''),valid.replace('V2','V1')]:
            with self.subTest(text=text),self.assertRaises(ValueError):
                d.parse_driver(text,[d.UNITS_VA])
        for got,want,n in [([],[],0),([],[self.record],1),([self.record],[],1)]:
            with self.assertRaises(ValueError):d.compare_records(got,want,n)

    def test_each_callback_dimension_is_observed(self):
        mutations=[]
        r=deepcopy(self.record);r['calls'][0],r['calls'][1]=r['calls'][1],r['calls'][0];mutations.append(r)
        r=deepcopy(self.record);r['calls'].pop(1);mutations.append(r)
        r=deepcopy(self.record);r['calls'].insert(1,deepcopy(r['calls'][0]));mutations.append(r)
        for path,value in [('target',0x1234),('args',[2]),('memory','0000000000000003')]:
            r=deepcopy(self.record);r['calls'][0][path]=value;mutations.append(r)
        for args in [[d.UNITS_VA+1,0x2005,0],[d.UNITS_VA,0x2008,0],[d.UNITS_VA,0x2005,1]]:
            r=deepcopy(self.record);r['calls'][-1]['args']=args;mutations.append(r)
        for key,value in [('return',0),('memory','0000000000000004')]:
            r=deepcopy(self.record);r[key]=value;mutations.append(r)
        for r in mutations:
            with self.subTest(record=r):self.assertEqual(d.compare_records([r],[self.record],1),[0])

    def test_order_identity_not_just_count(self):
        r=deepcopy(self.record);r['case']=1
        with self.assertRaises(ValueError):d.parse_driver(self.output([r]),[d.UNITS_VA])
        r=deepcopy(self.record);r['unit']+=1
        with self.assertRaises(ValueError):d.parse_driver(self.output([r]),[d.UNITS_VA])

    def test_wrong_integer_return_is_mismatch_not_invalid_output(self):
        r=deepcopy(self.record);r['return']=2
        got,_=d.parse_driver(self.output([r]),[d.UNITS_VA])
        self.assertEqual(d.compare_records(got,[self.record],1),[0])

    def test_instruction_exhaustion_is_not_return(self):
        regions=[(d.LEDGER_BASE,bytearray(8))]
        def loop(va,n):return (b'\xEB\xFE'+b'\x90'*n)[:n]
        with self.assertRaisesRegex(ValueError,'return boundary'):
            d.run_emulated(loop,regions,[0],instruction_limit=10)
        def ret(va,n):return b'\xC3'+b'\x90'*(n-1)
        records,_=d.run_emulated(ret,regions,[0],instruction_limit=10)
        self.assertEqual(len(records),1)
        def invalid(va,n):return (b'\x0F\x0B'+b'\x90'*n)[:n]
        with self.assertRaisesRegex(ValueError,'invalid emulation'):
            d.run_emulated(invalid,regions,[0],instruction_limit=10)

    def test_reference_identity_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'wrong.exe';p.write_bytes(b'MZ wrong reference')
            with self.assertRaisesRegex(ValueError,'identity mismatch'):d.read_exe(p)


if __name__ == '__main__':unittest.main()
