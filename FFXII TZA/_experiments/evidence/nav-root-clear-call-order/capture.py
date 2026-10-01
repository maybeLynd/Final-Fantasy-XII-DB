"""A one normal caller's source call order; no code execution/state observation."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-ROOT-CLEAR-CALL-ORDER');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
p=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');pol=Path(roles.__file__);(R/'shipping-reader.py').write_bytes(p.read_bytes());(R/'reg_tracking.py').write_bytes(pol.read_bytes())
tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,provider_files=[dict(path=str(Path(x).resolve()),bytes=Path(x).stat().st_size,sha256=sha(Path(x).read_bytes())) for x in [capstone.__file__,capstone._cs._name]])
sp=importlib.util.spec_from_file_location('rd',p);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};bodies=[]
for a,n,name in [(0x2341C0,62,'area-caller'),(0x383A20,12,'root-clear')]:
    b=rd.img_rd(image,ss,a,n);seq=list(cs.disasm(b,a));assert sum(i.size for i in seq)==n and seq[-1].mnemonic==('jmp' if n==62 else 'ret');(R/(name+'.bin')).write_bytes(b)
    records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    bodies.append(dict(name=name,entry=hex(a),bytes=n,sha256=sha(b),instructions=records));ii.update({i.address:i for i in seq})
pe=struct.unpack_from('<I',image,0x3C)[0];pr,ps=struct.unpack_from('<II',image,pe+24+112+24);pd=rd.img_rd(image,ss,rd.IMG_LO+pr,ps);ext=[]
for j in range(0,ps-11,12):
    a,e,u=struct.unpack_from('<III',pd,j)
    if a+rd.IMG_LO==0x2341C0:ext.append(dict(directory_rva=hex(pr),record_offset=j,record_hex=pd[j:j+12].hex(),entry=hex(a+rd.IMG_LO),end=hex(e+rd.IMG_LO)))
assert len(ext)==1 and ext[0]['end']=='0x2341fe'
parent=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-teardown-boundary');pa=json.loads((parent/'raw-source.json').read_text());tb=next(b for b in pa['bodies'] if b['name']=='teardown');assert rd.img_rd(image,ss,0x392710,45)==(parent/'retained/teardown.bin').read_bytes() and sha((parent/'retained/teardown.bin').read_bytes())==tb['sha256']
(R/'teardown-parent-raw.json').write_bytes((parent/'raw-source.json').read_bytes());(R/'teardown-parent-manifest.json').write_bytes((parent/'manifest.json').read_bytes())
raw=dict(reference=dict(exe_sha256=sha(image),base=hex(rd.IMG_LO),reader_sha256=sha(p.read_bytes()),policy_sha256=sha(pol.read_bytes()),parent_raw_sha256=sha((R/'teardown-parent-raw.json').read_bytes()),parent_manifest_sha256=sha((R/'teardown-parent-manifest.json').read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),tools=tools,bodies=bodies,extent=ext[0])
(W/'raw-source.json').write_text(json.dumps(raw,indent=2)+'\n')
caller=[i for a,i in ii.items() if 0x2341C0<=a<0x2341FE];assert not any(i.mnemonic.startswith('j') for i in caller[:-1]) and caller[-1].operands[0].imm==0x2FA470
calls=[dict(pc=hex(i.address),target=hex(i.operands[0].imm)) for i in caller if i.mnemonic=='call'];assert len(calls)==8
assert ii[0x2341C9].operands[0].imm==0x383A20 and ii[0x2341D0].operands[0].imm==0x306570 and ii[0x2341D5].operands[0].imm==0x392710
store=ii[0x383A20];o=store.operands[0];assert store.mnemonic=='mov' and o.type==capstone.CS_OP_MEM and o.size==8 and roles.op_kind(store,o,0)=='w' and store.address+store.size+o.mem.disp==0x2AEDFB0 and store.operands[1].imm==0
code=(R/'area-caller.bin').read_bytes();mut=bytearray(code)
for pc,target in [(0x2341C9,0x392710),(0x2341D5,0x383A20)]:
    j=pc-0x2341C0;assert mut[j]==0xE8;mut[j+1:j+5]=struct.pack('<i',target-(pc+5))
(R/'labelled-swapped-call-targets.bin').write_bytes(mut)
mii=list(cs.disasm(mut,0x2341C0));mcall=[(i.address,i.operands[0].imm) for i in mii if i.mnemonic=='call'];roots=[pc for pc,target in mcall if target==0x383A20];grids=[pc for pc,target in mcall if target==0x392710]
assert roots==[0x2341D5] and grids==[0x2341C9] and roots[0]>grids[0] and sha(mut)!=sha(code)
fp=Path('Database/FFXII TZA/_types/types.tsv');b=fp.read_bytes();lines=b.splitlines(keepends=True);kept=lines[0]+b''.join(x for x in lines[1:] if x.startswith(b'NavRunStateBlock\t'));assert b'002341C0' in kept and b'00392710' in kept;(R/'root-type-preimage.tsv').write_bytes(kept)
for x in tools['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
result=dict(method='A one verifiednormalcaller and source store/order controls, no original/native/emulator/live execution',reference=raw['reference'],driver_sha256=raw['driver_sha256'],calls=calls,normal_order=dict(root_clear_call='0x2341c9',grid_teardown_call='0x2341d5',intervening_call='0x2341d0',intervening_target='0x306570',root_store_cell='0x2aedfb0',root_store_bytes=8,root_store_value=0,tail='0x2fa470'),control=dict(private_root_call='0x2341d5',private_grid_call='0x2341c9',private_order_reversed=True,immutable_source_binding_refuses=sha(mut)!=sha(code)),consumer=dict(path=fp.as_posix(),full_source_sha256=sha(b),retained_sha256=sha(kept)),interpretation='At normalentry with preceding/intervening calls returning conformingly, direct call383A20 precedes call392710. Rootzero leaf and gridteardown source matchthe same reference. This narrows a localcall-order fact only; an opaque interveningcall can rebind/schedule, so stablezero/readiness/normalruntimeordering notproved.',limits='First30FE60, intervening306570, latercalls/tail nativeeffects unproved, including root rebind/transitive packunload/callbacks. This is not wholecallerclosure/dynamicreachability or universal rootclear-beforepackunload/everyrebuild/no-leak/exclusivity/atomicity proof. Sibling2368D0 distinctsource notrecaptured/censused; actuallive state scheduling remainsopen.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('CAPTURE_ROOT_CALL_ORDER normaldirectrootclear call beforegridteardown, interveningopaque306570 preventszero-stability inference; swappedtarget sourcecontrol reversesorder; no live lifetime proof')
