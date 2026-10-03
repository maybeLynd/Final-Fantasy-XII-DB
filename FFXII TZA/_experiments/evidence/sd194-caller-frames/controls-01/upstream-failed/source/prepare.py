"""Reuse physical PE/unwind preparation for only the missing caller bodies."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
W=P.parent
backend=W/'ov42-gauge-callback-binding/prepare-handler-extents.py'
raw=backend.read_bytes();source=raw.decode()
old="({'lookup-primary-handler-01.json':['0x29b7d0','0x29b7d1'],'lookup-secondary-handler-01.json':['0x29b810','0x29b811']}[n])"
new="({'sd194-caller-frame-lookup-01.json':['0x331990','0x331991'],'sd194-load-frame-lookup-01.json':['0x378a60','0x378a61']}[n])"
for previous,current in [(old,new),
 ("lookups=['lookup-primary-handler-01.json','lookup-secondary-handler-01.json']","lookups=['sd194-caller-frame-lookup-01.json','sd194-load-frame-lookup-01.json']"),
 ("for entry in [0x29b7d0,0x29b810]:","for entry in [0x331990,0x378a60]:")]:
    if source.count(previous)!=1:raise ValueError('exact reused preparation changed')
    source=source.replace(previous,current)
namespace=dict(__name__='scoped_frame_preparation',__file__=str(Path(__file__)))
exec(compile(source,str(backend),'exec'),namespace)
namespace['main']()
output=P/sys.argv[1]
record=json.loads(output.read_text())
record.update(reused_preparation_sha256=hashlib.sha256(raw).hexdigest(),specialized_source_sha256=hashlib.sha256(source.encode()).hexdigest())
output.write_text(json.dumps(record,indent=2)+'\n')
