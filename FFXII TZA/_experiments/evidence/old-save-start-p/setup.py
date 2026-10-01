"""Existing EXP031 backup/environment method, with observed FF12 cloud disabled."""
import hashlib, json, shutil, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parents[4]
sys.path.insert(0,str(repo/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
import team
board=json.loads(team.BOARD.read_text())
assert any(t['id']=='FABLE-REQ-ASTRA-OLD-SAVE-LOAD' and t['agent']=='ASTRA' and t['status']=='ACTIVE' and any(r['key']=='@runtime' for r in t.get('claimed_resources',t['resources'])) for t in board['tasks'])
assert not rt.list_processes(), 'Do not adopt or close an existing game'
cloud=json.loads((root/'cloud-before.json').read_text())
assert cloud['cloudEnabled'] is False and cloud['launchOptions']==''
source=Path.home()/'Documents/My Games/FINAL FANTASY XII THE ZODIAC AGE'
backup=repo/'Database/Tools/work/ASTRA/OLD-SAVE-START-P-20260921-save-backup'
assert not backup.exists()
def census(path):
    return {str(p.relative_to(path)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            for p in path.rglob('*') if p.is_file()}
files=census(source)
assert len(files)>0
assert files['76561198045890736\\FFXII_000']['sha256']=='859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825'
assert files['76561197960267366\\FFXII_004']['sha256']=='8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc'
assert files['76561198045890736\\keymap.ini']['sha256']=='8d98f85e0b571d819dc155c8774aad553f6e6119d6ede1cdd62245cfb9f6cf6d'
shutil.copytree(source,backup)
assert files==census(backup)==census(source)
(root/'save-before.json').write_text(json.dumps(dict(at=time.time(),source=str(source),backup=str(backup),files=files,
    protection='Backup is the preserved original; live save path is the disposable working copy. FF12 cloud is already OFF. Restore all changed working files after process exit before any later sync.'),indent=2))
env,report=rt.resolve_environment()
assert env and env['build_ok'] and env['clean']
(root/'environment.json').write_text(json.dumps(dict(at=time.time(),chosen=env,report=report),indent=2))
assert not rt.list_processes()
print(len(files),'original file hashes backed up and verified; Cloud OFF. Reference:',env['exe'])
