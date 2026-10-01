"""Selected original boot/bank constructor/reserve protocol; Method A only.
Capture uses the reviewed shared adapter and validates its actual invocation.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=W/'renderer-queue-initialization-source-02.json'
if out.exists():raise ValueError('immutable source exists; never recapture in place')
image=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(image).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('reference changed')
pe=struct.unpack_from('<I',image,60)[0];ns=struct.unpack_from('<H',image,pe+6)[0];opt=struct.unpack_from('<H',image,pe+20)[0]
sections=[struct.unpack_from('<IIII',image,pe+24+opt+40*k+8) for k in range(ns)]
def read(a,n):
    for vs,va,rs,ro in sections:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return image[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('unbacked source')
rva,size=struct.unpack_from('<II',image,pe+24+112+3*8)
if not size or size%12:raise ValueError('exception directory incomplete')
pd=[tuple(v+0x120000 for v in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
roots=[(0x189000,0x189083),(0x184F20,0x18506F),(0x184CB0,0x184CDF),
       (0x808FE4,0x809052),(0x186CD0,0x1871A8)]
receipts=[]
for a,b in roots:
    entries=[e for e in pd if e[0]==a and e[1]==b]
    if len(entries)!=1:raise ValueError('exact selected normal root changed '+hex(a))
    receipts.append(entries[0])
# Reserve's real normal body is five contiguous chained pdata regions.
chain=[];cursor=0x188640
for e in sorted(e for e in pd if e[0]<0x188721 and e[1]>0x188640):
    if e[0]!=cursor:raise ValueError('reserve normal-chain gap/overlap')
    cursor=e[1];hdr=read(e[2],4);flags=hdr[0]>>3;nc=hdr[2]
    row=dict(pdata=e,flags=flags)
    if flags&4:
        row['chain']=tuple(v+0x120000 for v in struct.unpack('<III',read(e[2]+4+2*((nc+1)&~1),12)))
        if row['chain'] not in [r['pdata'] for r in chain]:raise ValueError('unbound reserve unwind chain')
    elif chain or flags:raise ValueError('unexpected reserve root/handler')
    chain.append(row)
if cursor!=0x188721 or len(chain)!=5:raise ValueError('reserve normal chain incomplete')
receipts += [x['pdata'] for x in chain]
sp=importlib.util.spec_from_file_location('capture',W/'capture-index-path.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
C.RANGES=roots+[(0x188640,0x188721),(0x1EDF00,0x1EDF0E)]
sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text())
sp=importlib.util.spec_from_file_location('annotations',W/'validate-title-source-annotations.py')
S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S)
raw.update(wrapper_complete=True,pdata_entries=receipts,normal_chains=chain,leaf_extent=dict(start='0x1edf00',end_exclusive='0x1edf0e',basis='Exact14B original straight line endsRET; not invented pdata'),
           annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Source identity/local initialization protocol only; indirect guard/allocator/helper effects, actual heap state and natural scheduling remain unproved. Full local CFG proof required before semantic conclusions.')
out.write_text(json.dumps(raw,indent=2)+'\n')
print('CAPTURED seven original spans; normal-root/leaf identities and actual shared-role controls verified')
