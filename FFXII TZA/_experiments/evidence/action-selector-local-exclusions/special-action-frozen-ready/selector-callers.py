"""OV42: bounded rel32 caller discovery and .pdata-prefix input slices.
Pattern candidates are checked as decoded calls at shipping fragment boundaries.
This is not an indirect-call census or a proof of all argument value domains.
Reuse the identity-checked original-byte capture and reviewed role adapter.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
path=W/'capture-index-path.py'
spec=importlib.util.spec_from_file_location('verified_capture',path)
capture=importlib.util.module_from_spec(spec);spec.loader.exec_module(capture)
raw=capture.EXE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=capture.SHA: raise ValueError('wrong EXE')
p=struct.unpack_from('<I',raw,0x3c)[0]; opt=struct.unpack_from('<H',raw,p+20)[0]
sections=[struct.unpack_from('<IIII',raw,p+24+opt+40*i+8) for i in range(struct.unpack_from('<H',raw,p+6)[0])]
def read(va,n):
    for vs,sva,rs,ro in sections:
        if capture.BASE+sva<=va and va+n<=capture.BASE+sva+rs:
            return raw[ro+va-capture.BASE-sva:ro+va-capture.BASE-sva+n]
    raise ValueError('unbacked read')
a,n=struct.unpack_from('<II',raw,p+24+112+3*8)
unwind=list(struct.iter_unpack('<III',read(capture.BASE+a,n)))
text=sections[0]; blob=read(capture.BASE+text[1],text[2]);target=0x32fc30
sites=[];fragments=set()
for i,b in enumerate(blob[:-4]):
    if b!=0xe8:continue
    pc=capture.BASE+text[1]+i
    if pc+5+struct.unpack_from('<i',blob,i+1)[0]!=target:continue
    entry=next(((b+capture.BASE,e+capture.BASE,u+capture.BASE) for b,e,u in unwind if b+capture.BASE<=pc<e+capture.BASE),None)
    if entry is None: raise ValueError('candidate lacks .pdata boundary: %x'%pc)
    start,end,up=entry
    # Decode the prefix through the candidate call; later fragment bytes may
    # contain inline data. This establishes argument setup only, not a CFG.
    if end-start>0x10000:raise ValueError('capture budget exceeded')
    sites.append(dict(call_pc=hex(pc),fragment_start=hex(start),fragment_end=hex(end),unwind=hex(up)))
    fragments.add((start,pc+5))
if not sites:raise ValueError('no candidates; missing known positive')
if not any(x['call_pc']=='0x25daed' for x in sites):raise ValueError('missing known positive')
capture.RANGES=sorted(fragments)
print('Preflight candidate sites',json.dumps(sites),flush=True)
capture.main()
out=pathlib.Path(sys.argv[1]); result=json.loads(out.read_text())
instructions={int(x['pc'],16):x for r in result['ranges'] for x in r['instructions']}
for site in sites:
    ins=instructions.get(int(site['call_pc'],16))
    if not ins or ins['mnemonic']!='call' or ins['args']!='0x32fc30':raise ValueError('unaligned raw call candidate')
result.update(selector_discovery_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
              capture_module_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),direct_call_sites=sites,
              limitation='direct E8 sites in first file section only; decoded pdata prefixes through call, not full CFG/logical functions/indirect targets')
out.write_text(json.dumps(result,indent=2)+'\n')
print('Verified rel32 sites',len(sites),'shipping fragments',len(fragments),'natural selector bounds OPEN')
