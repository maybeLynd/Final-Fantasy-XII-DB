"""Bounded source-level controls for the previously collapsed callback observations.

Every build uses its own copied inputs and outputs. This does not invoke the known
unsafe general mutation_test.py. These targeted controls are not a complete campaign.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

root = Path(__file__).resolve().parents[5]
p = argparse.ArgumentParser()
p.add_argument('--out',type=Path,required=True,help='new directory for this bounded run')
evidence = p.parse_args().out.resolve()
evidence.mkdir(parents=True,exist_ok=False)
scratch = root/'Database/Tools/work/ASTRA/group-validator'
scratch.mkdir(parents=True, exist_ok=True)
vc = Path(r'C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat')
exe = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
recon = 'Game/Spawn/group_completion.c'
paths = [recon, 'Game/Spawn/group_completion.h','Tests/Differential/group_completion_driver.c']
originals = {p:(root/'Reconstruction'/p).read_bytes() for p in paths}
source = originals[recon].decode()
first = 'hooks->on_complete_prologue(hooks->ctx, 0x00307140u, 1);'
second = 'hooks->on_complete_prologue(hooks->ctx, 0x00238B70u, 1);'
third = 'hooks->on_complete_prologue(hooks->ctx, 0x00238AE0u, 1);'
variants = {
    'baseline': source,
    'swap-prologue-order': source.replace(first,'PLACEHOLDER').replace(second,first).replace('PLACEHOLDER',second),
    'omit-third-call': source.replace(third,''),
    'duplicate-first-call': source.replace(first,first+'\n        '+first),
    'wrong-prologue-argument': source.replace(first,first.replace(', 1)',', 2)')),
    'wrong-callee': source.replace('0x00238AE0u','0x00238AF0u'),
    'wrong-dispatch-unit': source.replace('hooks->ctx, unit_va, GROUP_EVENT','hooks->ctx, unit_va + 1, GROUP_EVENT'),
    'wrong-dispatch-third-argument': source.replace('GROUP_EVENT_ARM_A, 0)','GROUP_EVENT_ARM_A, 1)').replace('GROUP_EVENT_ARM_B, 0)','GROUP_EVENT_ARM_B, 1)'),
}
assert all(s != source for n,s in variants.items() if n != 'baseline')
record = dict(start_unix=time.time(), scope='targeted callback controls, not a complete mutation campaign',
              cases=[],status='INCOMPLETE')
env = os.environ.copy()
env['PYTHONPATH'] = str(root/'Database/Tools/work/ASTRA/python-libs')
try:
    for name, text in variants.items():
        dest = evidence/name
        dest.mkdir(exist_ok=False)
        item = dict(name=name,status='INCOMPLETE')
        record['cases'].append(item)
        with tempfile.TemporaryDirectory(prefix=name+'-',dir=scratch) as tmp:
            work = Path(tmp)
            for rel,b in originals.items():
                p = work/rel;p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(text.encode() if rel == recon else b)
            src = work/recon
            (dest/'mutated-source.c').write_bytes(src.read_bytes())
            driver = work/'group-driver.exe'
            command = ('@echo off\ncall "%s" >nul\n'
                       'cl /nologo /W4 /O2 /Brepro /D_CRT_SECURE_NO_WARNINGS /Fe:"%s" "%s" "%s" /link /Brepro\n') % (
                       vc,driver,work/'Tests/Differential/group_completion_driver.c',src)
            bat = work/'build.bat';bat.write_text(command,encoding='ascii')
            (dest/'build.bat').write_bytes(bat.read_bytes())
            build = subprocess.run([str(bat)],cwd=work,capture_output=True,text=True)
            (dest/'build-stdout.txt').write_text(build.stdout,encoding='utf-8')
            (dest/'build-stderr.txt').write_text(build.stderr,encoding='utf-8')
            item.update(build_exit=build.returncode,source_hashes={rel:hashlib.sha256((work/rel).read_bytes()).hexdigest() for rel in paths})
            if build.returncode or not driver.exists():
                item['status']='INVALID_NONCOMPILING'
                raise RuntimeError('control does not compile: '+name)
            item['driver_sha256']=hashlib.sha256(driver.read_bytes()).hexdigest()
            cmd=[sys.executable,str(root/'Reconstruction/Tests/Differential/diff_group_completion.py'),
                 '--exe',str(exe),'--driver',str(driver),'--out',str(dest/'run')]
            run=subprocess.run(cmd,cwd=work,env=env,capture_output=True,text=True)
            (dest/'comparison-stdout.txt').write_text(run.stdout,encoding='utf-8')
            (dest/'comparison-stderr.txt').write_text(run.stderr,encoding='utf-8')
            receipt=json.loads((dest/'run/receipt.json').read_text())
            item.update(command=cmd,exit_code=run.returncode,status=receipt['status'])
            assert receipt['identities'][str(driver)]==item['driver_sha256']
            expected=('MATCH',0) if name=='baseline' else ('MISMATCH',1)
            assert (item['status'],item['exit_code'])==expected,(name,item)
            print(name,item['status'],flush=True)
        assert not work.exists(), 'isolated case not cleaned'
    record['status']='TARGETED_CONTROLS_PASSED'
finally:
    record['end_unix']=time.time()
    record['production_sources_unchanged']=all((root/'Reconstruction'/rel).read_bytes()==b for rel,b in originals.items())
    (evidence/'controls.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
assert record['production_sources_unchanged']
