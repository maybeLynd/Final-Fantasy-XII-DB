"""OV42: original presentation-slot action-id store and direct argument sources.
Bounded original source; a supplied id is not proof that play supplies it.
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verified_capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
raw=C.EXE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=C.SHA:raise ValueError('reference EXE')
p=struct.unpack_from('<I',raw,0x3c)[0];optional=struct.unpack_from('<H',raw,p+20)[0]
sections=[struct.unpack_from('<IIII',raw,p+24+optional+i*40+8)
          for i in range(struct.unpack_from('<H',raw,p+6)[0])]
def read(va,n):
    for vs,sva,rs,ro in sections:
        if C.BASE+sva<=va and va+n<=C.BASE+sva+rs:
            return raw[ro+va-C.BASE-sva:ro+va-C.BASE-sva+n]
    raise ValueError('unbacked original span')
text=sections[0];blob=read(C.BASE+text[1],text[2])
def candidates(target):
    return [C.BASE+text[1]+i for i,b in enumerate(blob[:-4]) if b==0xe8 and
            C.BASE+text[1]+i+5+struct.unpack_from('<i',blob,i+1)[0]==target]
if 0x25daed not in candidates(0x32fc30):raise ValueError('known-positive discovery failed')
sites=candidates(0x30d070)
if not sites:raise ValueError('no source caller, not empty proof')
a,n=struct.unpack_from('<II',raw,p+24+112+3*8)
pd=list(struct.iter_unpack('<III',read(C.BASE+a,n)))
fragments=[]
for pc in sites:
    matches=[(b+C.BASE,e+C.BASE,u+C.BASE) for b,e,u in pd if b+C.BASE<=pc<e+C.BASE]
    if len(matches)!=1:raise ValueError('ambiguous/missing source boundary')
    start,end,uw=matches[0]
    if pc+5-start>0x8000:raise ValueError('bounded input budget exceeded')
    fragments.append(dict(call_pc=hex(pc),fragment_start=hex(start),fragment_end=hex(end),unwind=hex(uw)))
C.RANGES=[(0x30d070,0x30d155)]+sorted(set((int(s['fragment_start'],16),int(s['call_pc'],16)+5) for s in fragments))
C.main()
out=pathlib.Path(sys.argv[1]);r=json.loads(out.read_text())
ins={int(i['pc'],16):i for s in r['ranges'] for i in s['instructions']}
for s in fragments:
    i=ins.get(int(s['call_pc'],16))
    if not i or (i['mnemonic'],i['args'])!=('call','0x30d070'):raise ValueError('unaligned source caller')
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         direct_call_sites=fragments,
         limits='original allocator span and decoded first-section direct-call prefixes; no indirect/whole-CFG or natural selection proof')
out.write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURED slot allocator and',len(fragments),'direct argument prefixes; natural eligibility OPEN')
