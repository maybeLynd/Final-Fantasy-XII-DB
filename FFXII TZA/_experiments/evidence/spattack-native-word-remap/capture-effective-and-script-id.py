"""OV42: where do the effective and script presentation action ids come from?

Bounded source discovery, not dynamic reachability or an indirect-call census.
Reuses the verified original-byte capture and actual reviewed role adapter.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('verified_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
raw = C.EXE.read_bytes()
if hashlib.sha256(raw).hexdigest() != C.SHA: raise ValueError('wrong reference EXE')
p = struct.unpack_from('<I',raw,0x3c)[0]
optional = struct.unpack_from('<H',raw,p+20)[0]
sections = [struct.unpack_from('<IIII',raw,p+24+optional+40*i+8)
            for i in range(struct.unpack_from('<H',raw,p+6)[0])]
def read(va,n):
    for vs,sva,rs,ro in sections:
        if C.BASE+sva <= va and va+n <= C.BASE+sva+rs:
            return raw[ro+va-C.BASE-sva:ro+va-C.BASE-sva+n]
    raise ValueError('unbacked source')
text = sections[0]
blob = read(C.BASE+text[1],text[2])
def candidates(target):
    return [C.BASE+text[1]+i for i,b in enumerate(blob[:-4])
            if b == 0xe8 and C.BASE+text[1]+i+5+struct.unpack_from('<i',blob,i+1)[0] == target]
# A shipped direct-call positive controls the discovery calculation itself.
if 0x25daed not in candidates(0x32fc30): raise ValueError('known-positive rel32 detector failed')
target = 0x30eea0
sites = candidates(target)
if not sites: raise ValueError('missing admission callers, not impossibility proof')
a,n = struct.unpack_from('<II',raw,p+24+112+3*8)
pd = list(struct.iter_unpack('<III',read(C.BASE+a,n)))
fragments = []
for pc in sites:
    rows = [(b+C.BASE,e+C.BASE,u+C.BASE) for b,e,u in pd if b+C.BASE <= pc < e+C.BASE]
    if len(rows) != 1: raise ValueError('ambiguous/missing exception fragment')
    start,end,uw = rows[0]
    if pc+5-start > 0x8000: raise ValueError('bounded source budget exceeded')
    fragments.append(dict(call_pc=hex(pc),fragment_start=hex(start),fragment_end=hex(end),unwind=hex(uw)))
C.RANGES = [(0x387090,0x387125),(0x30eea0,0x30ef17)] + sorted(set((int(r['fragment_start'],16),int(r['call_pc'],16)+5) for r in fragments))
C.main()
out = pathlib.Path(sys.argv[1]); result = json.loads(out.read_text())
ins = {int(i['pc'],16):i for s in result['ranges'] for i in s['instructions']}
for r in fragments:
    i = ins.get(int(r['call_pc'],16))
    if not i or (i['mnemonic'],i['args']) != ('call','0x30eea0'):
        raise ValueError('unaligned source candidate; invalidate capture')
result.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    direct_call_sites=fragments, discovery_positive='original call25DAED ->32FC30 detected',
    limits='first section E8 candidates validated through pdata prefixes; no full CFG, indirect-call or natural-path closure')
out.write_text(json.dumps(result,indent=2)+'\n')
print('CAPTURED',len(fragments),'decoded admission-call prefixes; natural action admission OPEN')
