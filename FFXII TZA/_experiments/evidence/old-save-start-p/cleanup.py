"""Preserve reviewed working changes, then restore this run's fresh originals."""
from pathlib import Path
import difflib, hashlib, json, shutil, sys, time
root=Path(__file__).resolve().parent
repo=root.parents[4]
sys.path.insert(0,str(repo/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
assert not rt.list_processes(), 'Never restore a running game'
before=json.loads((root/'save-before.json').read_text())
source=Path(before['source']).resolve(); backup=Path(before['backup']).resolve()
assert source==Path.home()/'Documents/My Games/FINAL FANTASY XII THE ZODIAC AGE'
assert backup==repo/'Database/Tools/work/ASTRA/OLD-SAVE-START-P-20260921-save-backup'
def census(path):
    return {str(p.relative_to(path)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in path.rglob('*') if p.is_file()}
assert census(backup)==before['files']
now=census(source)
assert set(now)==set(before['files']), 'New/missing files require explicit review'
changed=[n for n in now if now[n]!=before['files'][n]]
allowed={'76561198045890736\\keymap.ini','76561198045890736\\GameSetting.ini'}
assert set(changed)<=allowed,changed
diffs={}
for n in changed:
    a=(backup/n).read_bytes(); b=(source/n).read_bytes()
    if n.endswith('keymap.ini'):
        assert b==(root.parent/'old-save-same-process/next-start-binding/candidate-keymap.ini').read_bytes()
    else:
        pairs=lambda raw:dict(l.split('=',1) for l in raw.decode().splitlines() if '=' in l)
        pa,pb=pairs(a),pairs(b)
        assert set(pa)==set(pb) and {k for k in pa if pa[k]!=pb[k]}<={'LUIDLow'}
    diffs[n]=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='original',tofile='working'))
preserve=repo/'Database/Tools/work/ASTRA/OLD-SAVE-START-P-20260921-working-before-restore'
assert not preserve.exists()
preserve.mkdir()
for n in changed:
    dst=preserve/n; dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source/n,dst)
    assert hashlib.sha256(dst.read_bytes()).hexdigest()==now[n]['sha256']
assert census(source)==now, 'Concurrent file change; stop before restoration'
for n in changed:shutil.copy2(backup/n,source/n)
after=census(source)
assert after==before['files'] and census(backup)==before['files'] and not rt.list_processes()
(root/'cleanup.json').write_text(json.dumps(dict(at=time.time(),status='RESTORED',processes=[],changed=changed,diffs=diffs,preserved=str(preserve),files=after,backup_unchanged=True),indent=2)+'\n')
print('All original hashes restored; preserved working changes:',changed)
