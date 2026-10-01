"""Restore only the inspected LUIDLow change after the owned FF12 has exited."""
from pathlib import Path
import hashlib
import json
import sys
import time

E = Path(__file__).resolve().parent
REPO = E.parents[4]
sys.path.insert(0, str(REPO/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt

def census(root):
    return {str(p.relative_to(root)): dict(bytes=p.stat().st_size,
            sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob('*') if p.is_file()}

assert not rt.list_processes()
before = json.loads((E/'save-before.json').read_text())
checked = json.loads((E/'cleanup-before.json').read_text())
source, backup = Path(before['source']), Path(before['backup'])
assert census(backup) == before['files']
assert census(source) == checked['working']
n = r'76561198045890736\GameSetting.ini'
assert checked['changed'] == [n]
old, new = (backup/n).read_bytes(), (source/n).read_bytes()
assert old.count(b'LUIDLow=79439') == 1
assert new == old.replace(b'LUIDLow=79439', b'LUIDLow=78748')
preserved = REPO/'Database/Tools/work/ASTRA/PHYRE-STARTUP-config-before-restore.ini'
assert preserved.read_bytes() == new
assert not rt.list_processes()
(source/n).write_bytes(old)
restored = census(source)
assert restored == census(backup) == before['files'] and len(restored) == 26
exe = Path(json.loads((E/'process.json').read_text())['path'])
assert hashlib.sha256(exe.read_bytes()).hexdigest() == rt.AUTHORITY_SHA256
result = dict(at=time.time(), status='RESTORED', processes=rt.list_processes(), files=restored,
              backup_unchanged=True, changed=[n], changed_keys=['LUIDLow'],
              preserved_working_config=str(preserved), reference_exe_sha256=rt.AUTHORITY_SHA256,
              pc_control='Ended: node_repl reset after verified exit; no subsequent UI control',
              observer_handles='Every memory-reading attempt closed its query/read handle; failed module census opened none',
              authorization='ACTIVE; no new stop/takeover, no automatic relaunch')
assert not result['processes']
with (E/'cleanup.json').open('x', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print('RESTORED: all 26 originals/backups match; reference intact; no FF12; PC control off.')
