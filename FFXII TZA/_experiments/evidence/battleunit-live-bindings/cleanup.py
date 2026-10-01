"""After owned-process exit, preserve changed working config and restore verified originals."""
from pathlib import Path
import difflib, hashlib, json, shutil, sys, time
root=Path(__file__).resolve().parent
repo=root.parents[4]
sys.path.insert(0,str(repo/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
assert not rt.list_processes(), 'Do not restore files while a game is running'
before=json.loads((root/'save-before.json').read_text())
source=Path(before['source']).resolve()
backup=Path(before['backup']).resolve()
assert source==Path.home()/'Documents/My Games/FINAL FANTASY XII THE ZODIAC AGE'
assert backup==repo/'Database/Tools/work/ASTRA/BU-BINDING-20260913-save-backup'
def census(path):
    return {str(p.relative_to(path)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            for p in path.rglob('*') if p.is_file()}
assert census(backup)==before['files']
now=census(source)
assert set(now)==set(before['files']), 'Unexpected new/missing file requires review'
changed=[n for n in now if now[n]!=before['files'][n]]
assert changed==['76561198045890736\\GameSetting.ini'],changed
name=changed[0]
orig=(backup/name).read_text()
current=(source/name).read_text()
delta=''.join(difflib.unified_diff(orig.splitlines(True),current.splitlines(True),fromfile='original',tofile='working'))
# Reviewed after ordinary exit: other five pre-exit display differences reverted.
allowed={'LUIDLow'}
def pairs(t):return dict(l.split('=',1) for l in t.splitlines() if '=' in l)
a,b=pairs(orig),pairs(current)
assert set(a)==set(b) and {k for k in a if a[k]!=b[k]}==allowed
preserved=repo/'Database/Tools/work/ASTRA/BU-BINDING-20260913-config-before-restore.ini'
assert not preserved.exists()
shutil.copy2(source/name,preserved)
assert hashlib.sha256(preserved.read_bytes()).hexdigest()==now[name]['sha256']
shutil.copy2(backup/name,source/name)
after=census(source)
assert after==before['files']
assert not rt.list_processes()
receipt=dict(at=time.time(),status='RESTORED',processes=[],changed=changed,
             preserved_working_config=str(preserved),changed_keys=sorted(allowed),diff=delta,
             files=after,backup_unchanged=True)
(root/'cleanup.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(delta)
print('All26 original hashes restored; no FF12 remains; backup unchanged.')
