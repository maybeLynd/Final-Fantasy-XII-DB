"""Injected short-read/wrong-code controls: release the key and reject invalid evidence."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import step

root=Path(__file__).resolve().parent
cases=[]

class CleanupControls(unittest.TestCase):
    def run_case(self,mode):
        sent=[];closed=[]
        class Reader:
            handle=1
            calls=0
            def __init__(self,pid):pass
            def read(self,a,n):return step.rp.CONTROL_BYTES
            def held(self):
                self.calls+=1
                if mode=='short' and self.calls==11:raise ValueError('injected short read')
                raw=bytearray(256)
                if sent and sent[-1] is False:raw[78 if mode=='wrong' else 64]=1
                return 0x1000,bytes(raw)
            def close(self):closed.append(True)
        with tempfile.TemporaryDirectory() as scratch:
            out=Path(scratch)/'receipt.json'
            argv=['step.py','--pid','1','--key','Right','--hold','.01','--out',str(out)]
            with patch.object(sys,'argv',argv),patch.object(step,'Reader',Reader), \
                 patch.object(step.rp,'find_process',return_value=[(1,r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')]), \
                 patch.object(step.rp,'module_base',return_value=step.rp.IMAGE_BASE), \
                 patch.object(step.wf,'windows_of',return_value=[(1,'fake control',1280,720)]), \
                 patch.object(step.wf,'focus',return_value=(True,1)), \
                 patch.object(step.key_packet.probe.u32,'GetForegroundWindow',return_value=1), \
                 patch.object(step.key_packet,'send_key',side_effect=lambda vk,up:sent.append(up)):
                if mode=='valid':step.main()
                else:
                    with self.assertRaises((ValueError,AssertionError)):step.main()
            record=json.loads(out.read_text())
            self.assertEqual(sent,[False,True]);self.assertEqual(closed,[True])
            self.assertEqual(record['status'],'CONTROLLED_PULSE' if mode=='valid' else 'INCOMPLETE')
            cases.append(dict(mode=mode,send_up_sequence=sent,closed=closed,status=record['status'],error=record.get('error')))
    def test_short_read_releases_and_rejects(self):self.run_case('short')
    def test_wrong_code_releases_and_rejects(self):self.run_case('wrong')
    def test_expected_code_positive(self):self.run_case('valid')

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CleanupControls))
    (root/'step-cleanup-controls.json').write_text(json.dumps(dict(success=result.wasSuccessful(),cases=cases,input_events_delivered=0,method='Injected reader/focus/process controls; SendInput replaced by recorder'),indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
