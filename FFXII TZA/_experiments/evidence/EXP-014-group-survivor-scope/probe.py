"""Affected generated mutants 47/69 against exact bkei/flag boundaries; no source-tree writes."""
from pathlib import Path
import hashlib
import json
import struct
import sys
import tempfile

root=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(root/'Database/Tools/work/ASTRA/python-libs'),str(root/'Reconstruction/Tests'),
              str(root/'Reconstruction/Tests/Differential')]
import mutation_test as m
import diff_group_completion as d
import unicorn

out=Path(__file__).resolve().parent
run=out/'boundary-run'
run.mkdir(exist_ok=False)
exe=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe')
rd=d.read_exe(exe)
snapshot=m.snapshot_inputs(root/'Reconstruction',*m.PILOTS['group_completion'][:3])
for rel,data in snapshot.items():
    p=run/'inputs'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
receipt=dict(status='INCOMPLETE',reference_sha256=d.REFERENCE_SHA256,unicorn=unicorn.__version__,
             instruments={str(Path(x.__file__).relative_to(root)):hashlib.sha256(Path(x.__file__).read_bytes()).hexdigest() for x in [m,d]},
             probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=[])
unit,p10,p698=d.UNITS_VA,0x10200000,0x10300000
fixtures={}
for name,rec_len,ledger_len in [('bkei-boundary',0xF8,24),('flag-boundary',0x100,17)]:
    ledger=bytearray(ledger_len);struct.pack_into('<Q',ledger,0,2)
    u=bytearray(d.U_ARM+1)
    for off,value in [(d.U_P10,p10),(d.U_MAP,d.MAPS_VA),(d.U_P698,p698),(d.U_FLAGS,1<<47)]:
        struct.pack_into('<Q',u,off,value)
    u[d.U_GROUP]=1;u[d.U_ARM]=1
    rec=bytearray(rec_len);struct.pack_into('<H',rec,0xF6,1)
    fixtures[name]=[(d.LEDGER_BASE,ledger),(unit,u),(d.MAPS_VA,bytearray([2,0,1])),
                    (p10,rec),(p698,bytearray([0,0,0,0,0,1]))]
manifest_root=root/'Database/FFXII TZA/_experiments/evidence/EXP-012-mutation-isolation/group-campaign'
target='Game/Spawn/group_completion.c'
try:
    for label,index in [('baseline',None),('index-47',47),('index-69',69)]:
        case_dir=run/label;case_dir.mkdir()
        mutant=None if index is None else (manifest_root/('case-%05d'%index)/'mutated-source.txt').read_bytes()
        if mutant is not None:(case_dir/'mutated-source.txt').write_bytes(mutant)
        with m.isolated_case(snapshot,Path(tempfile.gettempdir())/'ffxii-mutation-cases',target if mutant else None,mutant) as work:
            driver_hash=m.build(work,target,'group_completion_driver.c','boundary.exe',case_dir)
            assert driver_hash
            for name,regions in fixtures.items():
                f=case_dir/name;f.mkdir()
                packed=struct.pack('<I',len(regions))+b''.join(struct.pack('<QI',va,len(data))+data for va,data in regions)
                (f/'regions.bin').write_bytes(packed);(f/'cases.txt').write_text('%X\n'%unit)
                original,post=d.run_emulated(rd,regions,[unit])
                assert original[0]['return']==1 and len(original[0]['calls'])==4
                assert original[0]['calls'][-1]['args']==[unit,0x2005,0]
                assert post[0][1][16]==1
                (f/'original-records.json').write_text(json.dumps(original,indent=2)+'\n')
                (f/'original-post.bin').write_bytes(b''.join(data for va,data in post))
                proc=m.run_process([str(work/'Tests/Differential/boundary.exe'),str((f/'regions.bin').resolve()),
                     str((f/'cases.txt').resolve()),str((f/'driver-post.bin').resolve())],work,30)
                (f/'driver-process.json').write_text(json.dumps(proc,indent=2)+'\n')
                assert proc['exit_code']==0 and not proc['timed_out']
                candidate,footer=d.parse_driver(proc['stdout'],[unit])
                bad=d.compare_records(candidate,original,1)
                same=(f/'driver-post.bin').read_bytes()==(f/'original-post.bin').read_bytes()
                observed=dict(candidate=label,fixture=name,index=index,driver_sha256=driver_hash,
                              source_sha256=hashlib.sha256((work/target).read_bytes()).hexdigest(),
                              mismatched_cases=bad,final_bytes_equal=same,
                              original_return=original[0]['return'],candidate_return=candidate[0]['return'])
                receipt['results'].append(observed)
                expected=(index==47 and name=='bkei-boundary') or (index==69 and name=='flag-boundary')
                assert bool(bad or not same)==expected,observed
        assert not work.exists()
    receipt['production_inputs_stable']=all((root/'Reconstruction'/rel).read_bytes()==data for rel,data in snapshot.items())
    assert receipt['production_inputs_stable']
    receipt['status']='TWO_AFFECTED_MUTANTS_DETECTED_WITH_CROSS_CONTROLS'
finally:
    (run/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['status'],len(receipt['results']),'comparisons')
