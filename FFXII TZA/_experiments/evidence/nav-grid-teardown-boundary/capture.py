"""A navigation teardown request/lifetime boundary; no machine-code execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,why=team.board_status(team.BOARD);assert ok,why;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-GRID-TEARDOWN-BOUNDARY');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
p=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');pol=Path(roles.__file__);(R/'shipping-reader.py').write_bytes(p.read_bytes());(R/'reg_tracking.py').write_bytes(pol.read_bytes())
tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,provider_files=[dict(path=str(Path(x).resolve()),bytes=Path(x).stat().st_size,sha256=sha(Path(x).read_bytes())) for x in [capstone.__file__,capstone._cs._name]])
sp=importlib.util.spec_from_file_location('rd',p);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);d,ss=rd.load_image();assert sha(d)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};bodies=[]
for a,n,name in [(0x392710,45,'teardown'),(0x3844F0,5,'release-thunk'),(0x3697F0,13,'raw-release-entry'),(0x861EC0,6,'memset-thunk')]:
    b=rd.img_rd(d,ss,a,n);seq=list(cs.disasm(b,a));assert sum(i.size for i in seq)==n and seq[-1].mnemonic==('ret' if n==13 else 'jmp');(R/(name+'.bin')).write_bytes(b)
    records=[]
    for i in seq:
        records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
    bodies.append(dict(name=name,entry=hex(a),bytes=n,sha256=sha(b),instructions=records));ii.update({i.address:i for i in seq})
pe=struct.unpack_from('<I',d,0x3C)[0];pr,ps=struct.unpack_from('<II',d,pe+24+112+24);pd=rd.img_rd(d,ss,rd.IMG_LO+pr,ps);ext=[]
for j in range(0,ps-11,12):
    a,e,u=struct.unpack_from('<III',pd,j)
    if a+rd.IMG_LO==0x392710:ext.append(dict(directory_rva=hex(pr),record_offset=j,record_hex=pd[j:j+12].hex(),entry=hex(a+rd.IMG_LO),end=hex(e+rd.IMG_LO)))
assert len(ext)==1 and ext[0]['end']=='0x39273d'
parent=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-allocation-return-boundary');pa=json.loads((parent/'result.json').read_text());binding=pa['memset_import'];(R/'allocation-parent-result.json').write_bytes((parent/'result.json').read_bytes());(R/'allocation-parent-manifest.json').write_bytes((parent/'manifest.json').read_bytes())
for ak,bk in [('descriptor_va','descriptor_hex'),('lookup_va','lookup_hex'),('name_va','name_hex'),('dll_va','dll_hex')]:
    b=bytes.fromhex(binding[bk]);assert rd.img_rd(d,ss,int(binding[ak],16),len(b))==b
raw=dict(reference=dict(exe_sha256=sha(d),base=hex(rd.IMG_LO),reader_sha256=sha(p.read_bytes()),policy_sha256=sha(pol.read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),tools=tools,bodies=bodies,extent=ext[0],memset_import=binding)
(W/'raw-source.json').write_text(json.dumps(raw,indent=2)+'\n')
def rip(pc):
    i=ii[pc];o=next(o for o in i.operands if o.type==capstone.CS_OP_MEM and o.mem.base==capstone.x86_const.X86_REG_RIP);return i.address+i.size+o.mem.disp
assert rip(0x392714)==0x2AEE0A0 and ii[0x39271B].op_str=='rcx, rcx' and ii[0x39271E].mnemonic=='je' and ii[0x39271E].operands[0].imm==0x392725 and ii[0x392720].operands[0].imm==0x3844F0
assert ii[0x3844F0].operands[0].imm==0x3697F0 and ii[0x3697F0].op_str=='rcx, rcx' and ii[0x3697F3].operands[0].imm==0x3697FC and ii[0x3697F5].op_str=='edx, edx' and ii[0x3697F7].operands[0].imm==0x369860
assert ii[0x392725].op_str=='edx, edx' and ii[0x392727].mnemonic=='lea' and rip(0x392727)==0x2AEE060 and roles.op_kind(ii[0x392727],ii[0x392727].operands[1],1)=='addr'
assert ii[0x39272E].op_str=='r8d, 0x460' and ii[0x392738].operands[0].imm==0x861EC0
base=0x2AEE060;end=base+0x460;assert end==0x2AEE4C0 and base+0x60==0x2AEE0C0 and not base<=0x2AEDFB0<end
code=(R/'teardown.bin').read_bytes();bm=bytearray(code);p0=0x39271E-0x392710;assert bm[p0]==0x74;bm[p0]=0x75;(R/'labelled-release-je-to-jne.bin').write_bytes(bm)
small=bytearray(code);p0=0x39272E-0x392710;assert small[p0:p0+2]==bytes.fromhex('41b8');small[p0+2:p0+6]=struct.pack('<I',0x60);(R/'labelled-parameter-only-clear.bin').write_bytes(small)
mi=next(i for i in cs.disasm(bm,0x392710) if i.address==0x39271E);si=next(i for i in cs.disasm(small,0x392710) if i.address==0x39272E)
assert mi.mnemonic=='jne' and mi.operands[0].imm==0x392725 and si.op_str=='r8d, 0x60' and sha(bm)!=sha(code) and sha(small)!=sha(code)
refs=[]
for name,path,kind in [('nav-types-preimage.tsv','Database/FFXII TZA/_types/types.tsv','types'),('nav-fields-preimage.tsv','Database/FFXII TZA/_types/fields.tsv','fields'),('known-release-primary.md','Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md','release')]:
    b=Path(path).read_bytes();lines=b.splitlines(keepends=True)
    if kind=='types':kept=lines[0]+b''.join(x for x in lines[1:] if x.startswith((b'NavGridParams\t',b'NavSlotPointerArray\t')))
    elif kind=='fields':kept=lines[0]+b''.join(x for x in lines[1:] if x.startswith(b'NavGridParams\t'))
    else:
        i=next(j for j,x in enumerate(lines) if b'The release front' in x);kept=b''.join(lines[max(0,i-1):i+17])
    assert kept;(R/name).write_bytes(kept);refs.append(dict(path=path,full_source_sha256=sha(b),retained=name,retained_sha256=sha(kept),scope=kind))
assert b'THE HEAP BLOCK IS A DIFFERENT QUESTION AND IS OPEN' in (R/'nav-types-preimage.tsv').read_bytes() and b'003697F0' in (R/'known-release-primary.md').read_bytes()
for x in tools['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
result=dict(method='A exact teardown/release-entry request/control and typed clear-range calculation, no original/native/emulator/live execution',reference=raw['reference'],driver_sha256=raw['driver_sha256'],source_bindings=dict(heap_cell='0x2aee0a0',guard='0x39271e',release_call='0x392720',release_entry='0x3697f0',deeper_release_dispatch='0x369860',clear_destination=hex(base),clear_bytes=0x460,clear_end_exclusive=hex(end),mask_cell_offset=0x50,parameter_span_bytes=0x60,following_span_start='0x2aee0c0',following_span_bytes=0x400,nav_root_02AEDFB0_in_clear_range=False),controls=dict(branch=dict(original_null_skips_release=True,private_null_reaches_release=mi.mnemonic=='jne',same_target=True),clear_span=dict(original_covers_table_head=base+0x60<end,private_parameter_only_excludes_table_head=base+0x60==base+si.operands[1].imm),immutable_source_refuses_both=sha(bm)!=sha(code) and sha(small)!=sha(code)),consumers=refs,interpretation='On normal entry with a nonzero current heap cell, source routes it to known raw-pointer release; after conforming return, or directly if zero, source tailrequests zero fill of02AEE060..02AEE4C0. Covers whole60Bparams and400Bstarting at pointertablehead. Doesnotclear navroot02AEDFB0. This is a source-known teardown route, not actualdeallocation/clearedbytes or free-beforeeveryrebuild guarantee.',limits='Native release/CRT effects, header/arena invariants and actualinitializedpointer values unobserved. Clear400B beginning at arrayhead is physicalrequest range, not proof128logicalslots/capacity/elementcountbound/allrange semanticlayout. Originalno-clear-on-four-specific-routes finding notautomatically disproved or sharedproducerdeclared defective; ownermust evaluate this additionalroute. Repeatedrebuildrelease ordering, no-leak, rootclear-versuspack-unload ordering/reentrancy/threadatomicity remainopen.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('CAPTURE_TEARDOWN_SOURCE guarded rawrelease-route then460Bimagezero request; rootoutside; control excludesarrayhead; no native release/clear/order or128capacity proof')
