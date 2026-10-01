"""A original population source, conditional count domains; no code execution."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
from source_rules import facts,conditional_tail,check_extent
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NAV-POPULATION-ID-DOMAINS');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
R.mkdir(exist_ok=False)
for n in ['capture.py','source_rules.py']:(R/('driver-before-run.py' if n=='capture.py' else 'source-rules-before-run.py')).write_bytes((W/n).read_bytes())
p=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');pol=Path(roles.__file__)
(R/'shipping-reader.py').write_bytes(p.read_bytes());(R/'reg_tracking.py').write_bytes(pol.read_bytes())
tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,provider_files=[dict(path=str(Path(x).resolve()),bytes=Path(x).stat().st_size,sha256=sha(Path(x).read_bytes())) for x in [capstone.__file__,capstone._cs._name]])
sp=importlib.util.spec_from_file_location('rd',p);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={};bodies=[]
for a,n,name in [(0x392740,702,'populator'),(0x32A6B0,14,'registry-count-getter')]:
 b=rd.img_rd(image,ss,a,n);seq=list(cs.disasm(b,a));assert sum(i.size for i in seq)==n and seq[-1].mnemonic=='ret';(R/(name+'.bin')).write_bytes(b);records=[]
 for i in seq:
  records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand_index=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM],written=sorted(roles.written(i))))
 bodies.append(dict(name=name,entry=hex(a),bytes=n,sha256=sha(b),instructions=records));ii.update({i.address:i for i in seq})
pe=struct.unpack_from('<I',image,0x3c)[0];pr,ps=struct.unpack_from('<II',image,pe+24+112+24);pd=rd.img_rd(image,ss,rd.IMG_LO+pr,ps);ext=[]
for j in range(0,ps-11,12):
 a,e,u=struct.unpack_from('<III',pd,j)
 if a+rd.IMG_LO<0x3929FE and e+rd.IMG_LO>0x392740:
  head=rd.img_rd(image,ss,u+rd.IMG_LO,4);flags=head[0]>>3;off=4+((head[2]+1)//2)*4
  ub=rd.img_rd(image,ss,u+rd.IMG_LO,off+(12 if flags==4 else 4))
  ext.append(dict(directory_rva=hex(pr),record_offset=j,record_hex=pd[j:j+12].hex(),entry=hex(a+rd.IMG_LO),end=hex(e+rd.IMG_LO),unwind=hex(u+rd.IMG_LO),flags=flags,unwind_hex=ub.hex(),chain=[hex(v+rd.IMG_LO) for v in struct.unpack_from('<III',ub,off)] if flags==4 else None))
parent=Path('Database/FFXII TZA/_experiments/evidence/nav-grid-teardown-boundary/raw-source.json');(R/'teardown-parent-raw.json').write_bytes(parent.read_bytes())
raw=dict(reference=dict(exe_sha256=sha(image),base=hex(rd.IMG_LO),reader_sha256=sha(p.read_bytes()),policy_sha256=sha(pol.read_bytes()),parent_raw_sha256=sha(parent.read_bytes())),driver_sha256=sha((W/'capture.py').read_bytes()),rules_sha256=sha((W/'source_rules.py').read_bytes()),tools=tools,bodies=bodies,extents=ext)
(W/'raw-source.json').write_text(json.dumps(raw,indent=2)+'\n')
check_extent(ext)
root_only_refused=False
try:check_extent(ext[:1])
except AssertionError:root_only_refused=True
assert root_only_refused
code=(R/'populator.bin').read_bytes();f=facts(code);assert f['pointer_limit']==128
assert roles.op_kind(ii[0x392777],ii[0x392777].operands[0],0)=='w' and roles.op_kind(ii[0x3928B9],ii[0x3928B9].operands[0],0)=='rw' and roles.op_kind(ii[0x3927E0],ii[0x3927E0].operands[1],1)=='addr'
g=ii[0x32A6B0];o=g.operands[1];assert g.address+g.size+o.mem.disp==0x209A670 and ii[0x32A6B7].op_str=='eax, dword ptr [rax + 0x22c]'
assert all(i.mnemonic=='mov' and not roles.written(i).intersection({'rcx'}) for i in [ii[0x32A6B0],ii[0x32A6B7]])
mut=bytearray(code);j=0x3927FF-0x392740;assert mut[j:j+5]==bytes.fromhex('bd80000000');mut[j+1:j+5]=struct.pack('<I',129);(R/'labelled-pointer-limit-129.bin').write_bytes(mut);fm=facts(mut);assert fm['pointer_limit']==129 and fm['authored_base']==129
no=bytearray(code);j=0x392991-0x392740;assert no[j]==0xE8;no[j:j+5]=b'\x90'*5;(R/'labelled-single-count-read.bin').write_bytes(no);fn=facts(no);assert not fn['conditional_second_getter']
cases=[conditional_tail(f,a,b) for a,b in [(127,127),(128,129),(127,129),(-1,2),(0,-1)]]
assert cases[2]['last_id']==288 and conditional_tail(fn,127,129)['last_id']==286
cons=[]
for path,keep,name in [('Database/FFXII TZA/_types/fields.tsv',lambda l:l.startswith(b'NavGridParams\t') and l.split(b'\t')[1] in [b'0x058',b'0x05C'],'grid-count-fields-preimage.tsv'),('Database/FFXII TZA/_types/types.tsv',lambda l:l.startswith(b'NavSlotPointerArray\t'),'pointer-type-preimage.tsv')]:
 fp=Path(path);b=fp.read_bytes();lines=b.splitlines(keepends=True);k=lines[0]+b''.join(x for x in lines[1:] if keep(x));assert len(k.splitlines())>1;(R/name).write_bytes(k);cons.append(dict(path=path,full_source_sha256=sha(b),retained=name,retained_sha256=sha(k)))
for x in tools['provider_files']:assert sha(Path(x['path']).read_bytes())==x['sha256']
result=dict(method='A source-derived ID domains and conditional returned-value examples, no original/native/emulator/live execution',reference=raw['reference'],driver_sha256=raw['driver_sha256'],rules_sha256=raw['rules_sha256'],source_facts=f,getter=dict(root_cell='0x209a670',count_offset='0x22c',source_reads_only=True,requires_valid_pointer=True),domains=dict(pointer_list='IDs0..127 under normal entry, valid memory/conforming opaque returns/no unexpected counter mutation; reset count first and test signed count against128 before store/increment',authored='IDs128..159: unsigned min(header+24,32) records, IDsadvance even skipped record kinds; no pointer-list count increment in this loop',registry='IDs160..287 only under stable appropriate count across the two getter reads; first>=128 uses128, first<128 uses second result unchecked and skips if second<=0'),conditional_examples=cases,controls=dict(private_pointer_limit=fm['pointer_limit'],private_authored_base=fm['authored_base'],original_inconsistent_last_id=288,single_read_control_last_id=286,immutable_source_refuses_both=sha(mut)!=sha(code) and sha(no)!=sha(code)),consumers=cons,limits='Source extent is not whole caller closure. Opaque callees may mutate globals/reenter; no all-write census or exclusivity proof. Getter reads valid registry pointer/count but source is not initialization or cross-read identity/atomicity proof. Conditional first127/second129 is not an observed concurrent change/native fault/bug. IDs mark via392200 calls; its full native spatial effects not executed. No all-state memory safety, actual game population/maxima or fixed portable capacity claim.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('CAPTURE_NAV_POPULATION IDs0..127 list +128..159 authored +160..287 registry CONDITIONAL; two getter reads can use unchecked second count, labelledsource control discriminates; no live race proof')
