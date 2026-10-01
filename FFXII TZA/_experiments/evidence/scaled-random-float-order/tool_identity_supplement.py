"""Additive post-capture binary provenance; never rewrite raw observations."""
import datetime,hashlib,json
from pathlib import Path
import capstone,unicorn
import unicorn.unicorn_py3.unicorn as backend
W=Path(__file__).resolve().parent;s=json.loads((W/'raw.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(Path(unicorn.__file__).read_bytes())==s['tools']['unicorn_module_sha256']
rows=[]
for label,p in [('unicorn',Path(backend.uclib._name)),('capstone',Path(capstone._cs._name))]:
 rows.append(dict(label=label,path=str(p),bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mtime_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()))
p=W/'tool-identity-supplement.json';assert not p.exists()
p.write_text(json.dumps(dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),binaries=rows,
 provenance='Exact loaded-library paths/hashes recorded AFTER capture, matching pinned package/module identities. Original driver/observations unchanged. No install/tool changes during capture; this is additive current provenance, not an invented pre-run hash receipt.',
 limits='Versions/interpreter/module/driver were pinned in the original capture. DLL hashes supplemented afterward; repeatability consumers must verify these binaries before any genuinely needed future run.'),indent=2)+'\n')
print('Additive exact loaded DLL identity recorded; post-capture timing disclosed, raw capture unchanged.',flush=True)
