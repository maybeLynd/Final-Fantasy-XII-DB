"""Bounded original cache normalizer/lookup/fill fragments; no process state."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
out = W/'filecache-key-boundaries-source-02.json'
if out.exists():
    raise ValueError('immutable source exists; reconcile')
spec = importlib.util.spec_from_file_location('existing_key_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.RANGES = [(0x20c440,0x20c551), (0x1d6b40,0x1d6b62),
            (0x1d6d20,0x1d6d6f)]
sys.argv = [sys.argv[0],str(out)]
C.main()
raw = json.loads(out.read_text())
spec = importlib.util.spec_from_file_location('existing_key_annotation', W/'validate-title-source-annotations.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
raw.update(wrapper_complete=True, annotation_prerequisite=V.validate(raw),
           invocation_driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           limits='Declared normal fragments only, no CRT effects, all insertion paths, initialized cache or natural reachability')
# Data identity supplements the complete declared wrapper fragments; no strings guessed.
import struct
data = C.EXE.read_bytes()
if hashlib.sha256(data).hexdigest() != C.SHA:
    raise ValueError('reference moved before literal qualification')
pe = struct.unpack_from('<I',data,60)[0]
opt = struct.unpack_from('<H',data,pe+20)[0]
sections = [struct.unpack_from('<IIII',data,pe+24+opt+40*k+8)
            for k in range(struct.unpack_from('<H',data,pe+6)[0])]
literals = []
for va,expected in [(0x905ec0,b'/hostapp/'),(0x905ecc,b'/app0/'),(0x905ed4,b'/host/')]:
    for vs,rva,size,offset in sections:
        if C.BASE+rva <= va and va+len(expected)+1 <= C.BASE+rva+size:
            blob=data[offset+va-C.BASE-rva:offset+va-C.BASE-rva+len(expected)+1]
            break
    else:
        raise ValueError('unbacked prefix literal')
    if blob != expected+b'\0':
        raise ValueError('original prefix literal changed')
    literals.append({'va':hex(va),'bytes':blob.hex(),'sha256':hashlib.sha256(blob).hexdigest()})
raw['prefix_literals'] = literals
raw['boundary_correction'] = 'Source01 normalizer prologue was physical-only/incomplete. Source02 follows actual fallthrough/null target through RET20C550; adjacent20C560 excluded. Old three complete lookup/fill bodies retained in01, not recaptured.'
out.write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
for r in raw['ranges']:
    print('RANGE',r['start'],r['end_exclusive'],r['sha256'])
    for i in r['instructions']:
        print(i['pc'],i['mnemonic'],i['args'])
