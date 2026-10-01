"""Two original node helpers for the selected removal closure, no bulk census."""
import hashlib, importlib.util, json, pathlib, struct, sys
import capstone

W=pathlib.Path(__file__).resolve().parent
ROOT=W.parents[4]
out=W/'texture-async-removal-helpers-source-01.json'
if out.exists():raise ValueError('immutable source exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
if hashlib.sha256(d).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong original image')
pe=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,pe+6)[0];opt=struct.unpack_from('<H',d,pe+20)[0]
sections=[struct.unpack_from('<IIII',d,pe+24+opt+40*k+8) for k in range(ns)]


def read(a,n):
    for vs,va,rs,ro in sections:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole range lacks raw backing')


rva,size=struct.unpack_from('<II',d,pe+24+112+3*8)
if not size or size%12:raise ValueError('incomplete exception directory')
pd=[tuple(v+0x120000 for v in struct.unpack('<III',read(0x120000+rva+12*k,12))) for k in range(size//12)]
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
extents=[]
for entry in (0x16d6d0,0x16da60):
    containing=[t for t in pd if t[0]<=entry<t[1]]
    if containing:raise ValueError('helper is not the expected no-unwind leaf; use actual root/chain evidence')
    decoded=list(cs.disasm(read(entry,0x1000),entry))
    boundary=next((k for k,i in enumerate(decoded) if i.mnemonic=='int3'),None)
    if boundary is None or boundary==0 or decoded[boundary-1].mnemonic!='ret':raise ValueError('no qualified return/padding boundary')
    end=decoded[boundary].address
    padding=0
    while padding<64 and read(end+padding,1)==b'\xcc':padding+=1
    if not padding:raise ValueError('original helper padding absent')
    extents.append(dict(start=hex(entry),end_exclusive=hex(end),padding=read(end,padding).hex()))
spec=importlib.util.spec_from_file_location('removal_helpers_shared_capture',W/'capture-index-path.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.RANGES=[(int(t['start'],16),int(t['end_exclusive'],16)) for t in extents];sys.argv=[sys.argv[0],str(out)];C.main()
raw=json.loads(out.read_text())
spec=importlib.util.spec_from_file_location('removal_helpers_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
spec=importlib.util.spec_from_file_location('removal_helpers_cfg',W/'prove-title-queue-consumption.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
ix={int(i['pc'],16):i for q in raw['ranges'] for i in q['instructions']}
cfgs=[P.closed(ix,int(t['start'],16),int(t['end_exclusive'],16)) for t in extents]
raw.update(wrapper_complete=True,leaves=extents,normal_cfg_preparation=cfgs,
           annotation_prerequisite=S.validate(raw),invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
           limits='Two shipping no-unwind helper extents, original return/CC boundary and all-normal-CFG closure. Pointer provenance/native semantics/independent acceptance are separate; no game/original-code execution.')
out.write_text(json.dumps(raw,indent=2)+'\n')
print('Retained two branch-closed original node helpers',[(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']], 'calls', [g['calls'] for g in cfgs])
