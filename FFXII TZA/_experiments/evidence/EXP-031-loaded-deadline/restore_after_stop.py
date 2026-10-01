"""Restore the interrupted session after inspecting the extra window-position diff.

The ordinary cleanup closed the owned process, then rejected extra config changes
before copying any files. Preserve changed configuration in ignored scratch first.
"""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[3]/'Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
assert not rt.list_processes(), 'reference still running'
before=json.loads((HERE/'save-before.json').read_text())
source,backup=Path(before['source']),Path(before['backup'])
def census(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}
assert census(backup)==before['files']
current=census(source)
assert set(current)==set(before['files'])
changes=[name for name in current if current[name]!=before['files'][name]]
assert changes==['76561198045890736\\GameSetting.ini'],changes
allowed={'LUIDLow','WindowPosX','WindowPosY','LastX','LastY'}
diffs={}
for name in changes:
    old=(backup/name).read_text().splitlines()
    new=(source/name).read_text().splitlines()
    assert [x for x in old if x.split('=',1)[0] not in allowed]==[
        x for x in new if x.split('=',1)[0] not in allowed]
    diffs[name]=list(difflib.unified_diff(old,new,lineterm=''))
preserve=HERE.parents[3]/'Tools/work/ASTRA/EXP031-config-before-restore'
preserve.mkdir(exist_ok=False)
for name in changes:
    dest=preserve/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source/name,dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==current[name]
assert census(source)==current
for name in changes:shutil.copy2(backup/name,source/name)
after=census(source)
assert after==before['files']
receipt=dict(verified_files=len(after),changes=changes,diffs=diffs,
             preserved=str(preserve),before_restore=current,after=after,no_extra_files=True,
             ordinary_cleanup='closed target; rejected extra window geometry before restoring')
with (HERE/'save-restored.json').open('x') as stream:json.dump(receipt,stream,indent=2)
print('PASS: reference absent;26 originals restored; changed config preserved')
