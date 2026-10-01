import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text())
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==raw['reference']['adapter_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'actual shared access-role adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;d={}
for block in raw['blocks']:
 b=(R/block['path']).read_bytes();assert len(b)==block['bytes'] and sha(b)==block['sha256'];ii=list(cs.disasm(b,int(block['pc'],16)));assert sum(i.size for i in ii)==len(b);d.update({i.address:i for i in ii})
 assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in ii]==[(x['pc'],x['hex'],x['mnemonic'],x['args']) for x in block['instructions']]
 for i,x in zip(ii,block['instructions']):
  assert sorted(roles.written(i))==x['written'];assert [roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]==[m['kind'] for m in x['memory']]
for n,key in [('dispatch4.bin','table_sha256'),('descriptor24.bin','descriptor_sha256'),('name32.bin','name_sha256')]:assert sha((R/n).read_bytes())==raw['reference'][key]
assert 0x120000+struct.unpack('<I',(R/'dispatch4.bin').read_bytes())[0]==0x25f0ac;assert struct.unpack_from('<Q',(R/'descriptor24.bin').read_bytes(),8)[0]==int(raw['reference']['name_address'],16);assert (R/'name32.bin').read_bytes().split(b'\0')[0]==b'OPDIV'
assert sha((R/'consumer-before.md').read_bytes())==raw['consumer']['sha256']
expected={0x25e555:('mov','ebp, 1'),0x25e55f:('xorps','xmm7, xmm7'),0x25f0af:('call','0x267560'),0x25f0b4:('test','eax, eax'),0x25f0b6:('je','0x25f0e3'),0x25f0d1:('test','ebx, ebx'),0x25f0d3:('je','0x25e682'),0x25f0d9:('cdq',''),0x25f0da:('idiv','ebx'),0x25f111:('movss','xmm6, dword ptr [r10 + rdx*4 + 0x184]'),0x25f11d:('movd','xmm6, dword ptr [r10 + rdx*4 + 0x184]'),0x25f127:('cvtdq2ps','xmm6, xmm6'),0x25f164:('movss','xmm0, dword ptr [r10 + rdx*4 + 0x184]'),0x25f197:('ucomiss','xmm6, xmm7'),0x25f19a:('jp','0x25f1a3'),0x25f19c:('jne','0x25f1a3'),0x25f19e:('movaps','xmm0, xmm7'),0x25f1a1:('jmp','0x25f1a7'),0x25f1a3:('divss','xmm0, xmm6'),0x25f1b3:('mov','byte ptr [rax + r10 + 4], 2'),0x25f1c7:('movss','dword ptr [r10 + rax*4 + 0x184], xmm0'),0x25e682:('xor','r11d, r11d'),0x25e685:('mov','ecx, r11d'),0x25e688:('jmp','0x25e68f')}
for pc,pair in expected.items():assert (d[pc].mnemonic,d[pc].op_str)==pair,(hex(pc),pair)
assert roles.op_kind(d[0x25f1c7],d[0x25f1c7].operands[0],0)=='w';assert roles.op_kind(d[0x25f111],d[0x25f111].operands[1],1)=='r';assert roles.op_kind(d[0x25f0b8],d[0x25f0b8].operands[1],1)=='addr'
rmw=next(cs.disasm(bytes.fromhex('830001'),0));assert roles.op_kind(rmw,rmw.operands[0],0)=='rw'
states=[dict(name='ordered-equal',pf=0,zf=1),dict(name='ordered-unequal',pf=0,zf=0),dict(name='unordered',pf=1,zf=1)]
for x in states:x['source_path']='DIVSS' if x['pf'] or not x['zf'] else 'replace-xmm0-with-xmm7'
assert [x['source_path'] for x in states]==['replace-xmm0-with-xmm7','DIVSS','DIVSS']
if '--fault-drop-parity' in sys.argv:assert [x['source_path'] for x in states]==['DIVSS' if not x['zf'] else 'replace-xmm0-with-xmm7' for x in states],'JP distinguishes unordered from zero/equal before JNE'
if '--fault-reverse-divide' in sys.argv:assert d[0x25f1a3].op_str=='xmm6, xmm0','DIVSS uses lower/dividend XMM0 divided by top/divisor XMM6'
if '--fault-integer-zero-flags' in sys.argv:assert (d[0x25f197].mnemonic,d[0x25f19a].mnemonic)==('test','je'),'Floating predicate is UCOMISS+JP/JNE, not integer TEST/JE'
result=dict(status='ZERO_OR_UNORDERED_HYPOTHESIS_REFUTED_BY_SOURCE',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),source_predicate='DIVSS if PF=1 or ZF=0 after UCOMISS divisor XMM6 versus baseline XMM7; replace dividend XMM0 with XMM7 only if PF=0 and ZF=1',conditional_flag_calculations=states,initialization='Original local interpreter setup MOV EBP1 at25E555 and XORPS XMM7,XMM7 at25E55F; not observed actual caller/native callback preservation',interpretation='Original JP25F19A explicitly keeps unordered out of ordered-equal zero-result branch. Under supplied/locally source-backed +0 baseline, ordered zero divisor substitutes +0, ordered nonzero and unordered reach DIVSS. No actual OPDIV arithmetic or native exception behavior observed.',consumer_change='Qualify BF-1 floating zero guard with exact UCOMISS/JP/JNE predicate and dividend/divisor order. Canonical zero guard is supported, no claimed regression. Future replacement/control must preserve parity distinction; no expensive NaN guard runtime test required for this scoped source question.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS79 exact OPDIV identity/source guard distinguishes unordered; STATIC_ONLY',flush=True)
