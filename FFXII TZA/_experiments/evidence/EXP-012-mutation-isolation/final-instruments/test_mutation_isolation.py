"""Regression controls for source contamination and manufactured mutation passes."""
from pathlib import Path
import os
import csv
import subprocess
import sys
import tempfile
import time
import unittest

import mutation_test as m


class IsolationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='astra-mutation-test-')
        self.base=Path(self.temp.name).resolve()
        self.root=self.base/'production'
        self.files={
            'Game/Math/angle_wrap.c':b'#include "angle_wrap.h"\r\nint value = LIMIT;\r\n',
            'Game/Math/angle_wrap.h':b'#define LIMIT 3\r\n',
            'Tests/Differential/angle_wrap_driver.c':b'#include "../../Game/Math/angle_wrap.h"\nint main(void){return 0;}\n',
            'Tests/Differential/diff_angle_wrap.py':b'print("RESULT: CALCULATION PARITY")\n',
        }
        for rel,b in self.files.items():
            f=self.root/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
        self.snapshot=m.snapshot_inputs(self.root,'Game/Math/angle_wrap.c','angle_wrap_driver.c','diff_angle_wrap.py')

    def tearDown(self):
        assert self.base.parent==Path(tempfile.gettempdir()).resolve()
        self.temp.cleanup()

    def assert_clean(self):
        for rel,b in self.files.items():self.assertEqual((self.root/rel).read_bytes(),b)
        self.assertEqual(list((self.base/'scratch').iterdir()),[])

    def evaluate(self,name,target,mutated,build_fn):
        return m.evaluate_case(self.snapshot,self.base/'scratch',self.base/name,'angle_wrap','unused',1,
                               target,mutated,baseline_hash='base',build_fn=build_fn,
                               harness_fn=lambda *a:'FAIL')

    def test_failed_compile_cannot_contaminate_next_file(self):
        seen=[]
        def build(work,*args):
            seen.append(work)
            self.assertNotEqual(work,self.root)
            return None
        a=self.evaluate('invalid-c','Game/Math/angle_wrap.c',b'not C;',build)
        self.assertEqual(a['status'],'NO_BUILD');self.assert_clean()
        def next_build(work,*args):
            self.assertEqual((work/'Game/Math/angle_wrap.c').read_bytes(),self.files['Game/Math/angle_wrap.c'])
            self.assertEqual((work/'Game/Math/angle_wrap.h').read_bytes(),b'#define LIMIT 4\n')
            self.assertNotEqual(work,seen[0])
            return 'changed'
        b=self.evaluate('header','Game/Math/angle_wrap.h',b'#define LIMIT 4\n',next_build)
        self.assertEqual(b['status'],'FAIL');self.assert_clean()

    def test_interruption_cleans_case_and_preserves_exact_crlf(self):
        def interrupt(work,*args):
            self.assertEqual((work/'Game/Math/angle_wrap.c').read_bytes(),b'interrupted mutant')
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            self.evaluate('interrupt','Game/Math/angle_wrap.c',b'interrupted mutant',interrupt)
        self.assert_clean()

    @unittest.skipUnless(os.name=='nt' and Path(m.VCVARS).exists(),'MSVC control requires Windows compiler')
    def test_actual_compilation_failure_cleans_case(self):
        r=self.evaluate('compile','Game/Math/angle_wrap.c',b'!! this is deliberately invalid C !!\n',m.build)
        self.assertEqual(r['status'],'NO_BUILD');self.assert_clean()
        self.assertTrue((self.base/'compile/build.json').is_file())

    def test_empty_partial_invalid_or_timeout_cannot_pass(self):
        def records(*s):return [dict(status=x) for x in s]
        for total,selected,rs in [(0,0,[]),(1,1,records('NO_BUILD')),(1,1,records('EQUIVALENT')),
                                  (2,1,records('FAIL')),(2,2,records('FAIL')),
                                  (2,2,records('FAIL','TIMEOUT')),(2,2,records('FAIL','INVALID'))]:
            with self.subTest(results=rs):self.assertNotEqual(m.campaign_verdict(total,selected,rs)[1],0)
        self.assertEqual(m.campaign_verdict(2,2,records('FAIL','NO_BUILD')),('PASS',0))
        self.assertEqual(m.campaign_verdict(2,1,records('PASS')),('FAIL_INCOMPLETE',1))

    def test_unknown_failure_and_empty_success_are_invalid(self):
        def result(code,text='',err='',timeout=False):return dict(exit_code=code,stdout=text,stderr=err,timed_out=timeout)
        for r in [result(0),result(1,'something failed'),result(2,'RESULT: MISMATCH'),
                  result(1,'','Traceback'),result(0,'RESULT: MATCH','INVALID:')]:
            self.assertEqual(m.harness_verdict(r),'INVALID')
        self.assertEqual(m.harness_verdict(result(1,'RESULT: MISMATCH')),'FAIL')
        self.assertEqual(m.harness_verdict(result(0,'RESULT: MATCH')),'PASS')
        self.assertEqual(m.harness_verdict(result(1,timeout=True)),'TIMEOUT')

    def test_timeout_reaps_owned_process(self):
        start=time.monotonic()
        result=m.run_process([sys.executable,'-c','import time; time.sleep(30)'],self.base,0.1)
        self.assertLess(time.monotonic()-start,10,'timeout waited for natural exit instead of reaping')
        self.assertTrue(result['timed_out'])
        self.assertIsNotNone(result['exit_code'])

    @unittest.skipUnless(os.name=='nt','Windows process-tree control')
    def test_timeout_reaps_descendant(self):
        pidfile=self.base/'child.pid'
        script=('import subprocess,sys,time; from pathlib import Path; '
                'p=subprocess.Popen([sys.executable,"-c","import time; time.sleep(30)"]); '
                'Path('+repr(str(pidfile))+').write_text(str(p.pid)); time.sleep(30)')
        started=time.monotonic()
        r=m.run_process([sys.executable,'-c',script],self.base,0.7)
        self.assertTrue(r['timed_out']);self.assertLess(time.monotonic()-started,10)
        pid=pidfile.read_text()
        rows=csv.reader(subprocess.check_output(['tasklist','/FI','PID eq '+pid,'/FO','CSV','/NH'],text=True).splitlines())
        self.assertFalse(any(len(row)>1 and row[1]==pid for row in rows),'descendant survived cleanup')


if __name__=='__main__':unittest.main()
