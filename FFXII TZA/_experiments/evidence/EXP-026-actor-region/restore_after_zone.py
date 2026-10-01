"""Restore the explicitly authorized zone autosave after the conservative cleanup stopped."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[3] / 'Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
assert not rt.list_processes()
before = json.loads((root / 'save-before.json').read_text())
source, backup = Path(before['source']), Path(before['backup'])
def census(p):
    return {str(f.relative_to(p)): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in p.rglob('*') if f.is_file()}
assert census(backup) == before['files']
current = census(source)
assert set(current) == set(before['files'])
changes = [n for n in current if current[n] != before['files'][n]]
assert set(changes) == {'76561198045890736\\FFXII_000', '76561198045890736\\GameSetting.ini'}
ini = '76561198045890736\\GameSetting.ini'
a, b = (backup / ini).read_text(), (source / ini).read_text()
assert [s for s in a.splitlines() if not s.startswith('LUIDLow=')] == [s for s in b.splitlines() if not s.startswith('LUIDLow=')]
preserved = backup.parent / 'EXP026-zone-autosave-before-restore'
assert not preserved.exists()
preserved.mkdir()
for name in changes:
    shutil.copy2(source / name, preserved / Path(name).name)
assert census(source) == current
for name in changes:
    shutil.copy2(backup / name, source / name)
after = census(source)
assert after == before['files']
(root / 'save-restored.json').write_text(json.dumps(dict(
    initial_cleanup='Closed owned PID11300, then rejected changed FFXII_000 before restoring any file',
    changes=changes, changed_hashes={n: current[n] for n in changes},
    preserved_changed_files=str(preserved),
    ini_diff=list(difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm='')),
    after=after, verified_files=len(after), no_extra_files=True), indent=2)+'\n', encoding='utf-8')
print('PASS restored all', len(after), 'files; changed zone autosave preserved in ignored scratch')
