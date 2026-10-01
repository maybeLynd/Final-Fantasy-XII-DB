"""Restore the verified LUIDLow-only delta after the owned test process exits."""
from pathlib import Path
import sys,json,hashlib,time
E=Path(__file__).resolve().parent;repo=E.parents[5]
sys.path.insert(0,str(repo/'Database/Tools/analysis-kit/gfz-scripts'));import ffxii_runtime as rt
assert not rt.list_processes()
before=json.loads((E/'save-before.json').read_text());checked=json.loads((E/'cleanup-before.json').read_text())
source=Path(before['source']);backup=Path(before['backup']);sha=lambda b:hashlib.sha256(b).hexdigest()
def census(root):return {str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in root.rglob('*') if p.is_file()}
assert census(backup)==before['files'] and census(source)==checked['working']
n=r'76561198045890736\GameSetting.ini';assert checked['changed']==[n]
a=(backup/n).read_bytes();b=(source/n).read_bytes()
assert b==a.replace(b'LUIDLow=79439',b'LUIDLow=84456') and a.count(b'LUIDLow=79439')==1
assert Path(checked['preserved_working_config']).read_bytes()==b
assert not rt.list_processes();(source/n).write_bytes(a)
restored=census(source);assert restored==census(backup)==before['files'] and len(restored)==26
result=dict(at=time.time(),status='RESTORED',processes=rt.list_processes(),files=restored,backup_unchanged=True,changed=[n],changed_keys=['LUIDLow'],preserved_working_config=checked['preserved_working_config'],pc_control='Ended: node_repl kernel reset after process exit',authorization='ACTIVE: latest explicit user renewal; no new stop/takeover this run')
assert not result['processes']
with (E/'cleanup.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print('RESTORED: all26 original hashes and backup verified, no FF12 process, PC control ended.')
