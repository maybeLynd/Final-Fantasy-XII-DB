"""Close only EXP028's owned reference and restore verified save/config changes."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[3] / 'Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt

before = json.loads((root / 'save-before.json').read_text())
source, backup = Path(before['source']), Path(before['backup'])
def census(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}
assert census(backup) == before['files']
processes = rt.list_processes()
assert len(processes)==1 and processes[0]['pid']==35836
exited, left = rt.close_all(timeout=5)
remaining = rt.list_processes()
(root / 'close-receipt.json').write_text(json.dumps(dict(unix=time.time(), before=processes, exited=exited, left=left, remaining=remaining), indent=2))
assert not left and not remaining
current = census(source)
assert set(current)==set(before['files'])
changes = [name for name in current if current[name]!=before['files'][name]]
diffs = {}
for name in changes:
    assert Path(name).name == 'GameSetting.ini', changes
    a, b = (backup/name).read_text(), (source/name).read_text()
    diffs[name] = list(difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm=''))
    # Only the known adapter identity rewrite is allowed without a separate review.
    assert [s for s in a.splitlines() if not s.startswith('LUIDLow=')] == [s for s in b.splitlines() if not s.startswith('LUIDLow=')], diffs
assert census(source)==current
for name in changes:
    shutil.copy2(backup/name, source/name)
after=census(source)
assert after==before['files']
(root/'save-restored.json').write_text(json.dumps(dict(changes=changes,diffs=diffs,after=after,verified_files=len(after),no_extra_files=True),indent=2))
print('Closed PID35836; exact save/config restoration:',len(after),'files',changes)
