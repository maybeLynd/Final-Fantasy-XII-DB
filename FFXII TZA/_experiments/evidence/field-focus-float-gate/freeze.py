import hashlib,json,shutil,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/field-focus-float-gate')
assert not P.exists();subprocess.run([sys.executable,str(W/'check.py')],check=True)
# Supplement timing is explicit; do not retroactively certify capture-time DLL identity.
dll=Path(capstone._cs._name)
(W/'tool-identity-supplement.json').write_text(json.dumps(dict(timing='After source/checker-control derivation, before freeze; not capture-time proof',capstone_dll_path=str(dll),bytes=dll.stat().st_size,sha256=hashlib.sha256(dll.read_bytes()).hexdigest()),indent=2)+'\n')
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
for n in ('PLAN.md','README.md','architecture.json','derive.py','check.py','result.json','freeze.py','tool-identity-supplement.json'):shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained')
receipts=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  filtered=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();unfiltered=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert filtered==unfiltered,p
  receipts.append(dict(path=p.relative_to(P).as_posix(),git_blob=filtered))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=receipts),indent=2)+'\n')
m=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(P.rglob('*')) if p.is_file() and '__pycache__' not in p.parts];assert m
(P/'manifest.json').write_text(json.dumps(dict(members=m,limits='Source/ISA/Python checker-control only; no FF12 original-code/native/live execution, actual MXCSR or accumulator-domain proof'),indent=2)+'\n')
subprocess.run([sys.executable,str(P/'check.py')],check=True);print('Frozen exact byte-safe field gate',len(m),'members',flush=True)
