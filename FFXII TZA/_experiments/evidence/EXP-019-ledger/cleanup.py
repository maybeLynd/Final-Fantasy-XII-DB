"""Close only the asserted owned reference, restore exact backed-up files, verify census."""
import hashlib,json,sys,time,shutil,difflib
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parents[3]/'Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
before=json.loads((root/'save-before.json').read_text());source=Path(before['source']);backup=Path(before['backup'])
def census(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
assert census(backup)==before['files']
procs=rt.list_processes();assert len(procs)==1 and procs[0]['pid']==12200
exited,left=rt.close_all(timeout=5);remaining=rt.list_processes()
receipt=dict(unix=time.time(),before_processes=procs,exited=exited,left=left,remaining=remaining)
(root/'close-receipt.json').write_text(json.dumps(receipt,indent=2));assert not left and not remaining
current=census(source);assert set(current)==set(before['files'])
changes=[name for name,h in current.items() if h!=before['files'][name]]
assert changes==['76561198045890736\\GameSetting.ini'],changes
name=changes[0];a=(backup/name).read_text();b=(source/name).read_text()
diff=list(difflib.unified_diff(a.splitlines(),b.splitlines(),lineterm=''))
assert a.replace('LUIDLow=79439','LUIDLow=78642')==b,diff
assert census(source)==current
shutil.copy2(backup/name,source/name)
after=census(source);assert after==before['files']
(root/'save-restored.json').write_text(json.dumps(dict(changed=changes,diff=diff,before_restore=current,after_restore=after,verified_files=len(after),no_extra_files=True),indent=2))
print('Closed owned PID; restored and verified',len(after),'files')
