"""Source obligations and illustrative calculations, NEVER an execution receipt."""
import copy,hashlib,json,sys
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
s=json.loads((W/'source.json').read_text())
assert s['method'].startswith('A STATIC_ONLY')
assert s['ff12']['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
imp=s['ff12']['import_witness'];assert imp['iat']=='0x8c2c10' and imp['name']=='_fdclass' and imp['dll']=='api-ms-win-crt-math-l1-1-0.dll'
assert bytes.fromhex(imp['hint_name_hex'])[2:]==b'_fdclass\0'
assert bytes.fromhex(imp['dll_name_hex'])==imp['dll'].encode()+b'\0'
for d in s['dependencies']:assert sha((W/'retained'/d['retained']).read_bytes())==d['sha256']
nav=json.loads((W/'retained/nav-source.json').read_text());assert nav['imports'][0]==imp
ni={int(i['pc'],16):i for i in nav['body']['instructions']}
# Identify the two indirect calls by original decoded IAT target bytes, not naming.
calls=[i for i in nav['body']['instructions'] if i['op']=='call' and i['bytes'] in ['ff15ccec5300','ff15b6ec5300']]
assert len(calls)==2
for i in calls:
 p=int(i['pc'],16);n=ni[p+6]
 assert n['bytes']=='6683f802' and n['op']=='cmp' and n['args']=='ax, 2'
 assert ni[p+10]['op']=='je'
gen=(W/'retained/exp131-gen_bodies.py').read_text()
assert 'NaN 2, +-inf 1, finite -1,' in gen and 'denormal -2, zero 0' in gen
assert 'Scripted boundaries (NOT executed)' in gen

def obligations(h):
 assert h['sha256']=='5c52e3a303baaac0e0af8bd9b96134993da34bc9d834a31ef37e1d2cdc7fe192'
 assert h['export']['name']=='_fdclass' and not h['export']['forwarded'] and h['export']['rva']==0x5f410
 b=bytes.fromhex(h['body_hex']);assert len(b)==65 and sha(b)==h['body_sha256']
 ii=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in Cs(CS_ARCH_X86,CS_MODE_64).disasm(b,0x5f410)]
 assert ii==h['instructions'] and b''.join(bytes.fromhex(i['bytes']) for i in ii)==b
 assert len(ii)==21
 expected={0x5f410:('660f7ec1','movd'),0x5f414:('8bc1','mov'),0x5f416:('250000807f','and'),0x5f41b:('3d0000807f','cmp'),0x5f420:('750e','jne'),0x5f422:('f7c1ffff7f00','test'),0x5f428:('7510','jne'),0x5f42a:('b801000000','mov'),0x5f42f:('c3','ret'),0x5f430:('85c0','test'),0x5f432:('740c','je'),0x5f434:('b8ffffffff','mov'),0x5f439:('c3','ret'),0x5f43a:('b802000000','mov'),0x5f43f:('c3','ret'),0x5f440:('f7c1ffffff7f','test'),0x5f446:('7503','jne'),0x5f448:('33c0','xor'),0x5f44a:('c3','ret'),0x5f44b:('b8feffffff','mov'),0x5f450:('c3','ret')}
 assert {(int(i['pc'],16)):(i['bytes'],i['op']) for i in ii}==expected
 pcs=set(expected)
 for i in ii:
  if i['op'] in ['je','jne']:assert int(i['args'],16) in pcs
 assert all('[' not in i['args'] and i['op'] not in ['call','jmp','ldmxcsr','stmxcsr'] for i in ii)
 return ii
ii=obligations(s['host'])
# The exhaustive *symbolic partition* follows pinned masks/branches, not this
# model agreeing with itself. These examples illustrate each partition edge.
def conditional(bits):
 e=bits&0x7f800000;m=bits&0x7fffff
 if e==0x7f800000:return 2 if m else 1
 if e:return -1
 return -2 if bits&0x7fffffff else 0
inputs=[0,0x80000000,1,0x80000001,0x007fffff,0x807fffff,0x00800000,0x80800000,0x3f800000,0xbf800000,0x7f7fffff,0xff7fffff,0x7f800000,0xff800000,0x7f800001,0xff800001,0x7fc00000,0xffc00000,0x7fffffff,0xffffffff]
want=[0,0,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,1,1,2,2,2,2,2,2]
assert [conditional(b) for b in inputs]==want
kills=[]
for name,old,new in [('wrong-mantissa-mask','f7c1ffff7f00','f7c1ffff3f00'),('wrong-NaN-return','b802000000','b803000000'),('branch-outside-body','7510','757f')]:
 h=copy.deepcopy(s['host']);assert h['body_hex'].count(old)==1
 h['body_hex']=h['body_hex'].replace(old,new);h['body_sha256']=sha(bytes.fromhex(h['body_hex']))
 h['instructions']=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in Cs(CS_ARCH_X86,CS_MODE_64).disasm(bytes.fromhex(h['body_hex']),0x5f410)]
 try:obligations(h)
 except AssertionError:kills.append(dict(name=name,verdict='REJECTED_SOURCE_OBLIGATION'))
 else:raise AssertionError('invalid source accepted '+name)
result=dict(verdict='PASS_STATIC_HOST_DEPENDENCY',source_sha256=sha((W/'source.json').read_bytes()),body_bytes=65,decoded_instructions=21,return_sites=5,partition=[dict(exponent='all ones',mantissa='nonzero',signed_return=2),dict(exponent='all ones',mantissa='zero',signed_return=1),dict(exponent='neither zero nor all ones',mantissa='any',signed_return=-1),dict(exponent='zero',mantissa='nonzero',signed_return=-2),dict(exponent='zero',mantissa='zero',signed_return=0)],examples=[dict(bits=f'{b:08x}',signed_return=r,method='conditional source calculation; NOT executed') for b,r in zip(inputs,want)],controls=kills,established='Identified installed CRT leaf copies raw binary32 low XMM0 bits with MOVD and classifies through integer masks. All signs share the partition; both quiet/signaling NaN payloads map to2. No FP arithmetic, memory operands or MXCSR read/write in this complete body. EAX immediates expose low AX signed-short codes used by original GGRID AX==2 gate.',limits='STATIC_ONLY host DLL source proof. Not actual FF12 process binding, native execution/FP flag observation, universal CRT version semantics, live reachability or native effects elsewhere. Retained bridge already declares these class codes; no defect or wholesale native promotion.')
if '--derive' in sys.argv:
 assert not (W/'manifest.json').exists() and not (W/'result.json').exists()
 (W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
else:assert json.loads((W/'result.json').read_text())==result
if (W/'manifest.json').exists():
 manifest=json.loads((W/'manifest.json').read_text());members=manifest['members'];assert members
 actual={p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=W/'manifest.json'}
 assert actual=={d['path'] for d in members}
 for d in members:
  b=(W/d['path']).read_bytes();assert len(b)==d['bytes'] and sha(b)==d['sha256']
print(result['verdict'],'five exact source partitions; controls',len(kills),'no execution',flush=True)
