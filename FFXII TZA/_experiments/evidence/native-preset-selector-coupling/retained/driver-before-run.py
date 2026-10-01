"""A one original353B three-selector recipe; no code execution or type guess."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-NATIVE-PRESET-SELECTOR-COUPLING');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not (W/'raw.json').exists();R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('rd',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
P=Path('Database/FFXII TZA/_experiments/evidence/uc1-257-single-extent');m=json.loads((P/'manifest.json').read_text())
for x in m['members']:
 data=(P/x['path']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
parent=json.loads((P/'raw.json').read_text());code=bytes.fromhex(parent['observation']['raw_hex']);assert code==rd.img_rd(image,ss,0x712180,353)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x712180));by_pc={i.address:i for i in ins};assert len(ins)==82 and sum(i.size for i in ins)==353 and not any(i.mnemonic=='call' for i in ins)
tools=dict(python=sys.version,python_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),bytes=Path(p).stat().st_size,sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name,roles.__file__]])
records=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str,memory=[dict(operand=j,size=o.size,base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),disp=o.mem.disp,kind=roles.op_kind(i,o,j)) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in ins]
targets={}
for pc in [0x712195,0x7121B8,0x7121D9,0x712248]:
 i=by_pc[pc];o=next(o for o in i.operands if o.type==capstone.CS_OP_MEM);assert i.reg_name(o.mem.base)=='rip';targets[hex(pc)]=i.address+i.size+o.mem.disp
assert [targets[hex(pc)] for pc in [0x712195,0x7121B8,0x7121D9,0x712248]]==[0x1F3C5B0,0xD9F05E,0x1F3C5F0,0x1F3C820]
tables=[]
for name,a,stride,count in [('first',0x1F3C5B0,8,8),('second',0x1F3C5F0,28,20),('third',0x1F3C820,56,10)]:
 b=rd.img_rd(image,ss,a,stride*count);(R/(name+'.bin')).write_bytes(b)
 tables.append(dict(name=name,entry=hex(a),stride=stride,rows=count,raw_hex=b.hex(),sha256=sha(b),words=[list(struct.unpack_from('<'+'I'*(stride//4),b,stride*j)) for j in range(count)],limits='Rows bounded by original selector upper caps and constant address/stride, not a named runtime resource/default or field-type interpretation'))
flag=rd.img_rd(image,ss,0xD9F05E,1)
pe=struct.unpack_from('<I',image,0x3C)[0];num=struct.unpack_from('<H',image,pe+6)[0];opt=struct.unpack_from('<H',image,pe+20)[0];sections=[]
for j in range(num):
 off=pe+24+opt+j*40;vs,va,rs,ro=struct.unpack_from('<IIII',image,off+8);sections.append(dict(name=image[off:off+8].rstrip(b'\0').decode(),entry=hex(0x120000+va),virtual_bytes=vs,raw_bytes=rs,raw_offset=ro,characteristics=hex(struct.unpack_from('<I',image,off+36)[0])))
mapping=[]
for a,n in [(0x712180,353),(0xD9F05E,1),(0x1F3C5B0,64),(0x1F3C5F0,560),(0x1F3C820,560)]:
 s=next(s for s in sections if int(s['entry'],16)<=a and a+n<=int(s['entry'],16)+min(s['virtual_bytes'],s['raw_bytes']));mapping.append(dict(entry=hex(a),bytes=n,section=s,file_offset=s['raw_offset']+a-int(s['entry'],16)))
for name,path in [('shipping-reader.py',rp),('reg_tracking.py',Path(roles.__file__)),('extent-raw.json',P/'raw.json'),('extent-manifest.json',P/'manifest.json')]: (R/name).write_bytes(path.read_bytes())
(R/'original353.bin').write_bytes(code);(R/'mode-byte.bin').write_bytes(flag)
private=bytearray(code);off=0x71222A-0x712180;assert private[off:off+3]==bytes.fromhex('448bca');private[off:off+3]=b'\x90'*3
control=list(cs.disasm(private,0x712180));assert sum(i.size for i in control)==353
raw=dict(method='A original353B instructions/table bytes/access/layout/branch recipe; private source-only bypass control, no execution',driver_sha256=sha(Path(__file__).read_bytes()),reference=dict(exe_sha256=sha(image),body_sha256=sha(code),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),reader_sha256=sha(rp.read_bytes()),policy_sha256=sha(Path(roles.__file__).read_bytes())),tools=tools,source=records,targets={p:hex(a) for p,a in targets.items()},tables=tables,mode_byte=dict(entry='0xd9f05e',file_hex=flag.hex(),limits='File sample and section backing only; runtime meaning/initialization/value stability unproved'),mappings=mapping,control=dict(name='private-remove-negative-third-fallback',entry='0x71222a',original_hex='448bca',private_hex=bytes(private).hex(),private_sha256=sha(private),decoded=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in control]),limits='Only this leaf/source/table bounded selector recipe. Object/system identity, scalar semantic types, runtime byteflag/memory initialization/caller occurrence/lifetime/alias constraints unassigned. Current FABLE/SPEC/FRONTIER admission conditions untouched. Model/control below are A computations, not native/isolated/live observations.',cleanup='Read-only reference and published54 inputs, ownedW/E only; PC OFF/noFF12/input/memory/save/config/reference/peer writes, S19budgetunchanged/fullL1+L2NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
for p in tools['providers']:assert sha(Path(p['path']).read_bytes())==p['sha256']
assert next(x for x in records if x['pc']=='0x7121a7')['memory'][0]['kind']=='w' and next(x for x in records if x['pc']=='0x712195')['memory'][0]['kind']=='addr'
print('RETAINED56 source/table/section/shareddefault roles; no native meaning accepted',flush=True)
print('table first2rows',[(x['name'],x['words'][:2]) for x in tables]);print('second defaultwords',[x[4] for x in tables[1]['words']],flush=True)
