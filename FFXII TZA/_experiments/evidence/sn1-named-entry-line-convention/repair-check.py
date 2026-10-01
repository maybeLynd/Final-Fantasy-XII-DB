import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;p=W/'check.py';old=p.read_bytes();a=b"ent=struct.unpack('<IHHIIIIIIHH',bytes.fromhex(bind['entry_hex']))";z=b"ent=struct.unpack_from('<IHHIIIIIIHH',bytes.fromhex(bind['entry_hex']));assert not any(bytes.fromhex(bind['entry_hex'])[36:])"
assert old.count(a)==1 and not (W/'result.json').exists()
q=W/'retained/check-before-entry-extent-fix.py';assert not q.exists();q.write_bytes(old)
assert p.read_bytes()==old;p.write_bytes(old.replace(a,z))
(W/'failure.json').write_text(json.dumps(dict(first_capture='INVALID_BYTECODE_BINDING_PRECONDITION; known evctrl shared tail incorrectly decoded contiguously, raw/result absent. Old driver/source nine inputs retained, later three added without replacing preimages.',diagnostic='diagnostic.json first mismatch6130 in evctrl1; corrected directory bound6130 and omitted144B/48marks; exceptional q1 names remain unaccepted',first_reducer='INVALID_ENTRY_EXTENT_UNPACK; struct layout36B, retained physical directory entry48B. unpack exact rejected trailing12B padding before any result.',repair='Read first36B using unpack_from and separately require remaining12B zero; old checker retained, no original input recapture.',old_checker_sha256=hashlib.sha256(old).hexdigest(),new_checker_sha256=hashlib.sha256(p.read_bytes()).hexdigest()),indent=2)+'\n')
