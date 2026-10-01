"""A: original retained metadata and shipping resolver disassembly, never executed."""
import hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u=lambda b,o:struct.unpack_from('<I',b,o)[0]
if (W/'raw.json').exists():
 subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team,reg_tracking as roles
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-VARIABLE-NAME-BINDING');assert t['agent']=='ASTRA' and t['status']=='ACTIVE'
assert not R.exists();R.mkdir()
P=Path('Database/FFXII TZA/_experiments/evidence/sn1-named-entry-line-convention');parent=json.loads((P/'raw.json').read_text());files=[]
for m in ['ctrl','btlctrl','evctrl','mapctrl']:
 for ext in ['dbg','ebp','sbn']:
  data=(P/'retained'/(m+'.'+ext)).read_bytes();ref=next(x for x in parent['reference']['files'] if (x['module'],x['extension'])==(m,ext));assert sha(data)==ref['sha256'] and len(data)==ref['bytes'];(R/(m+'.'+ext)).write_bytes(data);files.append(ref)
(R/'parent61-raw.json').write_bytes((P/'raw.json').read_bytes());(R/'parent61-result.json').write_bytes((P/'result.json').read_bytes());(R/'selected-sbn-functions.py').write_bytes((P/'retained/selected-sbn-functions.py').read_bytes())
for n,p in [('variables-primary-before.md','Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md'),('debug-primary-before.md','Database/FFXII TZA/01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md'),('front-tables-primary.py','Database/FFXII TZA/_index/candidates/sn1-layouts/sn1_front_tables.py')]: (R/n).write_bytes(Path(p).read_bytes())
reader=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');(R/'shipping-reader.py').write_bytes(reader.read_bytes());(R/'reg_tracking.py').write_bytes(Path(roles.__file__).read_bytes())
spec=importlib.util.spec_from_file_location('rd',reader);rd=importlib.util.module_from_spec(spec);spec.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
code=rd.img_rd(image,ss,0x262440,591);(R/'resolver591.bin').write_bytes(code);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
instructions=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str,memory=[dict(operand=j,kind=roles.op_kind(i,o,j),base=i.reg_name(o.mem.base),index=i.reg_name(o.mem.index),scale=o.mem.scale,disp=o.mem.disp) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]) for i in cs.disasm(code,0x262440)]
assert sum(len(bytes.fromhex(i['hex'])) for i in instructions)==591
g={'struct':struct};exec(compile((R/'selected-sbn-functions.py').read_bytes(),'retained parser','exec'),g)
def source(m,block,line):
 s=(R/(m+'.sbn')).read_bytes();bo,be=g['sbn_blocks'](s)[block];L,bases,starts,te=g['sbn_group_read'](s,bo);a=starts[line-1];return dict(block=block,physical_line=line,offset=a,hex=s[a:s.index(b'\0',a,be)].hex(),text=s[a:s.index(b'\0',a,be)].decode('cp932'))
cases=[]
for m,pc,idx,block,line,name,kind in [('evctrl',16,0x61,0,960,'test_load_flg','assignment'),('btlctrl',531,0x0d,2,4,'loop_flg','assignment'),('btlctrl',537,0x0e,2,5,'mapjump_menu_flg','assignment'),('mapctrl',729,0x52,0,388,'test','dvar'),('mapctrl',736,0x20,0,389,'mp_debugmenu_flg','dvar')]:
 bind=next(x for x in parent['bindings'] if x['module']==m and x['scope']==1);e=(R/(m+'.ebp')).read_bytes();off=bind['code_start']+pc;size=6 if kind=='assignment' else 7
 cases.append(dict(module=m,pc=pc,index=idx,code_offset=off,code_hex=e[off:off+size].hex(),kind=kind,source=source(m,block,line),expected_source_name=name,source_relation='Retained61 literal/operation anchor' if m!='evctrl' else 'Adjacent assignment source candidate; pc16 and call22 share logical q0 tag417, source assignment logical416. Group attribution remains non-singular.'))
tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,providers=[dict(path=str(Path(p).resolve()),sha256=sha(Path(p).read_bytes())) for p in [capstone.__file__,capstone._cs._name]],access_policy_sha256=sha(Path(roles.__file__).read_bytes()),access_invocation='Every decoded memory operand uses reg_tracking.op_kind directly; no raw access flag classifier')
raw=dict(method='A exact retained original metadata, source and shipping resolver disassembly; no original-code/emulated/native/live execution',reference=dict(parent=P.as_posix(),parent_manifest_sha256=sha((P/'manifest.json').read_bytes()),files=files,exe_sha256=sha(image),base=hex(rd.IMG_LO),reader_sha256=sha(reader.read_bytes()),resolver_address='0x262440',resolver_bytes=591,resolver_sha256=sha(code)),tools=tools,driver_sha256=sha(Path(__file__).read_bytes()),resolver=instructions,cases=cases,limits='Five exact operand/source candidates, four module counts and native descriptor table indexing. Metadata pairing not original compiler/writer universal proof, effects, values or lifetime. Source attribution/grouping ambiguity persists; no new whole-VBF provenance audit. PC OFF/S19 unchanged/fullL1+L2 NOT_MET')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print('CAPTURE65 original metadata five candidates; reducer required',flush=True)
subprocess.run([sys.executable,str(W/'check.py')],check=True)
