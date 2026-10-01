"""Correct the failed 40B-leaf assumption using current extent and original pdata."""
import ast,hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained'
assert not (W/'intervening-body.json').exists() and not (R/'intervening-body963.bin').exists()
identity=json.loads((W/'raw.json').read_bytes())['identity']
for s in identity['sources']:
 if s['copy'] in ['shipping-reader.py','reg_tracking.py']:assert hashlib.sha256((R/s['copy']).read_bytes()).hexdigest()==s['sha256']
catalog=Path('Database/Tools/work/graph/functions.tsv');blob=catalog.read_bytes()
line=next(x for x in blob.decode('utf-8').splitlines() if x.startswith('002E45E0\t'));p=line.split('\t');assert p[1]=='Movement_UpdateSteeringTowardTarget' and int(p[2])==963
tree=ast.parse((R/'shipping-reader.py').read_text('utf-8'))
ns={'EXE':identity['exe']['path'],'SHA':identity['exe']['sha256'],'IMG_LO':0x120000,'hashlib':hashlib,'struct':struct}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['load_image','img_rd']],type_ignores=[]),'original certified reader functions','exec'),ns)
image,sections=ns['load_image']();rd=lambda a,n:ns['img_rd'](image,sections,a,n)
code=rd(0x2e45e0,963);roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'shared reviewed adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ins=list(cs.disasm(code,0x2e45e0));assert sum(i.size for i in ins)==963
rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'written':sorted(roles.written(i)),'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
pe=struct.unpack_from('<I',image,0x3c)[0];opt=pe+24;assert struct.unpack_from('<H',image,opt)[0]==0x20b
rv,sz=struct.unpack_from('<II',image,opt+112+3*8);assert sz>0 and sz%12==0
table=rd(0x120000+rv,sz);entries=[]
for j in range(sz//12):
 record=table[j*12:j*12+12];start,end,uw=struct.unpack('<III',record);start+=0x120000;end+=0x120000
 if start<0x2e45e0+963 and end>0x2e45e0:
  head=rd(0x120000+uw,4);flags=head[0]>>3;n=((4+head[2]*2+3)//4)*4;tail=12 if flags&4 else 4 if flags&3 else 0
  entries.append({'table_pc':hex(0x120000+rv+j*12),'begin':hex(start),'end':hex(end),'bytes':end-start,'unwind_rva':hex(uw),'raw_runtime_function':record.hex(),'raw_unwind_info':rd(0x120000+uw,n+tail).hex(),'flags':flags})
assert entries and any(e['begin']=='0x2e45e0' and e['bytes']==40 for e in entries)
out={'method':'A corrected original full963B and original exception-directory entries, no guest/native/live execution','entry':'002E45E0','sha256':hashlib.sha256(code).hexdigest(),'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'adapter_sha256':hashlib.sha256((R/'reg_tracking.py').read_bytes()).hexdigest(),'exe_sha256':identity['exe']['sha256'],'catalog':{'path':catalog.as_posix(),'sha256':hashlib.sha256(blob).hexdigest(),'selected_line':line},'exception_directory':{'rva':hex(rv),'bytes':sz,'table_sha256':hashlib.sha256(table).hexdigest(),'selected_entries':entries},'instructions':rows,'initial_failure':'Initial source probe assumed complete40B leaf/no nonvolatile writes. Failed at write-set predicate before saving raw; INVALID, original driver/terminal preserved. New source capture uses current963B extent and retains raw BEFORE semantic acceptance; previous delta/caller/sqrt captures unchanged.','limits':'Physical extent/fragment and direct source control flow only. No full call closure, imported effects, initialized pointer values or dynamic class stability proof.'}
assert hashlib.sha256(catalog.read_bytes()).hexdigest()==out['catalog']['sha256']
assert hashlib.sha256(Path(ns['EXE']).read_bytes()).hexdigest()==identity['exe']['sha256']
(R/'intervening-body963.bin').write_bytes(code);(W/'intervening-body.json').write_bytes((json.dumps(out,indent=2)+'\n').encode())
print(json.dumps({'retained_full_bytes':963,'runtime_function_entries':entries,'calls':[x for x in rows if x['mnemonic']=='call'],'return_pcs':[x['pc'] for x in rows if x['mnemonic']=='ret'],'status':'SOURCE_CAPTURE_ONLY_NOT_SEMANTIC_CLOSURE'},indent=2))
