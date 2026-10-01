"""Existing EXP031 backup/environment method, with observed FF12 cloud disabled."""
import hashlib, json, shutil, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parents[5]
sys.path.insert(0,str(repo/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
import team
board=json.loads(team.BOARD.read_text())
assert any(t['id']=='ASTRA-INPUT-REGISTRATION-LIVE' and t['agent']=='ASTRA' and t['status']=='ACTIVE' for t in board['tasks'])
assert not rt.list_processes(), 'Do not adopt or close an existing game'
cloud=json.loads((root/'cloud-before.json').read_text())
assert cloud['cloudEnabled'] is False and cloud['launchOptions']==''
source=Path.home()/'Documents/My Games/FINAL FANTASY XII THE ZODIAC AGE'
backup=repo/'Database/Tools/work/ASTRA/INPUT-TITLE-RENEWED-20260913-save-backup'
assert not backup.exists()
def census(path):
    return {str(p.relative_to(path)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            for p in path.rglob('*') if p.is_file()}
files=census(source)
assert len(files)>0
shutil.copytree(source,backup)
assert files==census(backup)==census(source)
(root/'save-before.json').write_text(json.dumps(dict(at=time.time(),source=str(source),backup=str(backup),files=files,
    protection='Backup is the preserved original; live save path is the disposable working copy. FF12 cloud is already OFF. Restore all changed working files after process exit before any later sync.'),indent=2))
env,report=rt.resolve_environment()
assert env and env['build_ok'] and env['clean']
(root/'environment.json').write_text(json.dumps(dict(at=time.time(),chosen=env,report=report),indent=2))
assert not rt.list_processes()
print(len(files),'original file hashes backed up and verified; Cloud OFF. Reference:',env['exe'])
