"""Retain existing physical bytes/receipts; no original recapture."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;old=P.parent/'ov42-gauge-callback-binding'
out=P/'retained'
if out.exists():raise ValueError('existing retained input: never overwrite')
out.mkdir();rows=[]
for name in ['handler-extents-01.json','handler-extents-01.status.json','handler-extents-01.stdout','handler-extents-01.stderr',
             'prepare-handler-extents.py','lookup-primary-handler-01.json','lookup-secondary-handler-01.json','source-01.json']:
    data=(old/name).read_bytes();(out/name).write_bytes(data)
    rows.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),origin=str((old/name).resolve())))
(out/'inputs.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Retained8 exact input/receipt files; no capture or execution')
