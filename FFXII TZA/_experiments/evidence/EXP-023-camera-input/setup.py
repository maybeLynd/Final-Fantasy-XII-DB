"""Back up the complete save tree and launch one asserted clean reference."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

root = Path(__file__).resolve().parent
repo = root.parents[4]
sys.path.insert(0, str(repo / 'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
import team

board = json.loads(team.BOARD.read_text())
assert any(t['id']=='ASTRA-CAMERA-INPUT-RUNTIME' and t['status']=='ACTIVE' and t['agent']=='ASTRA' for t in board['tasks'])
assert not rt.list_processes()
source = Path.home() / 'Documents/My Games/FINAL FANTASY XII THE ZODIAC AGE'
backup = repo / 'Database/Tools/work/ASTRA/EXP023-save-backup'
assert not backup.exists()
files = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in source.rglob('*') if p.is_file()}
assert len(files) == 26
shutil.copytree(source, backup)
assert files == {str(p.relative_to(backup)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in backup.rglob('*') if p.is_file()}
(root / 'save-before.json').write_text(json.dumps(dict(source=str(source), backup=str(backup), files=files), indent=2))
env, report = rt.resolve_environment()
assert env and env['build_ok'] and env['clean']
pid, error = rt.launch(env, 60)
(root / 'launch.json').write_text(json.dumps(dict(unix=time.time(), pid=pid, error=error, environment=report), indent=2))
assert pid and not error
print('Owned reference PID', pid)
