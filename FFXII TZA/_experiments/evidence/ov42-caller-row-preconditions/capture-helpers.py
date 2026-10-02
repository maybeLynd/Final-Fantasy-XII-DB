"""The two missing terminal helpers only; retained caller/switch stay retained."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
def main():
 s=json.loads((P/'helper-extents-01.status.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s.get('driver_sha256')!=sha(P/'prepare-helper-extents.py') or not(P/'helper-extents-01.stdout').read_bytes() or(P/'helper-extents-01.stderr').read_bytes():raise ValueError('required successful current extent invocation')
 e=json.loads((P/'helper-extents-01.json').read_text())
 if e.get('complete') is not True or e.get('driver_sha256')!=sha(P/'prepare-helper-extents.py'):raise ValueError('incomplete/stale physical extent')
 for n,span in [('helper-retained-lookup-02.json',['0x305430','0x305480']),('slot-transition-retained-lookup-01.json',['0x30d160','0x30d1a0'])]:
  v=json.loads((P/n).read_text())
  if v.get('complete') is not True or v.get('requested')!=span or v.get('driver_sha256')!='3ee7b1d08a9857dba896f77a3ba3bd238e850d6a4fb5bfe556cfcb78b37008dd' or v.get('matches')!=[]:raise ValueError('required exact preparation lookup failed/retained source exists')
 if [(b['entry'],b['end_exclusive'],b['bytes']) for b in e['bodies']]!=[('0x305430','0x305635',517),('0x30d160','0x30d54c',1004)]:raise ValueError('physical helper population differs')
 if sha(P/'capture-index-path.py')!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497':raise ValueError('reviewed capture changed')
 spec=importlib.util.spec_from_file_location('reviewed_capture',P/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
 C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
 C.RANGES=[(0x305430,0x305635),(0x30d160,0x30d54c)]
 output=P/sys.argv[1];sys.argv=[sys.argv[0],str(output)];C.main()
 x=json.loads(output.read_text());x.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),limits='Original helper code only, complete decoding. No execution/native helper effects or natural row binding. Retained2034-byte caller and52-byte switch not recaptured.')
 output.write_text(json.dumps(x,indent=2)+'\n')
if __name__=='__main__':main()
