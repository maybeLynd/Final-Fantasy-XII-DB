"""Deploy one reviewed Start=P binding only after a fresh verified backup."""
import hashlib, json, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parents[4]
sys.path.insert(0,str(repo/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
import team
board=json.loads(team.BOARD.read_text())
assert any(t['id']=='FABLE-REQ-ASTRA-OLD-SAVE-LOAD' and t['agent']=='ASTRA' and t['status']=='ACTIVE' and any(r['key']=='@runtime' for r in t.get('claimed_resources',t['resources'])) for t in board['tasks'])
assert not rt.list_processes()
before=json.loads((root/'save-before.json').read_text())
source=Path(before['source']); backup=Path(before['backup'])
def census(p):
    return {str(f.relative_to(p)):dict(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in p.rglob('*') if f.is_file()}
assert census(source)==census(backup)==before['files']
prior=root.parent/'old-save-same-process/next-start-binding'
original=(prior/'original-keymap.ini').read_bytes()
candidate=(prior/'candidate-keymap.ini').read_bytes()
pre=json.loads((prior/'preflight.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(original)==pre['source_sha256'] and sha(candidate)==pre['candidate_sha256']
target=source/'76561198045890736/keymap.ini'
assert target.read_bytes()==original
assert not (root/'deployment.json').exists()
target.write_bytes(candidate)
assert target.read_bytes()==candidate and not rt.list_processes()
after=census(source)
changed=[n for n in after if after[n]!=before['files'][n]]
assert changed==['76561198045890736\\keymap.ini']
(root/'deployment.json').write_text(json.dumps(dict(at=time.time(),intervention='Only Keyboard2 Start=0 ->43 (P); primary Escape/stop guard intact',target=str(target),before_sha256=sha(original),after_sha256=sha(candidate),changed=changed,files_after=after),indent=2)+'\n')
print('Disposable Start=P deployed; actual Pause acceptance remains to be observed.')
