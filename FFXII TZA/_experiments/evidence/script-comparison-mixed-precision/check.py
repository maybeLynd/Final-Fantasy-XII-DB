import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());code=(R/'compare413.bin').read_bytes();assert len(code)==413 and sha(code)==raw['reference']['code_sha256']
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
policy=(R/'reg_tracking.py').read_bytes();assert sha(policy)==raw['reference']['adapter_sha256'];roles=types.ModuleType('roles');exec(compile(policy,'actual shared access-role adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(code,0x25d740));d={i.address:i for i in ii};assert sum(i.size for i in ii)==413
assert [(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str) for i in ii]==[(x['pc'],x['hex'],x['mnemonic'],x['args']) for x in raw['instructions']]
for i,x in zip(ii,raw['instructions']):
 assert sorted(roles.written(i))==x['written'];assert [roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]==[m['kind'] for m in x['memory']]
expected={0x25d74f:('mov','edi, 1'),0x25d754:('cmp','edx, 2'),0x25d757:('jge','0x25d7a1'),0x25d7a1:('lea','eax, [rdx - 1]'),0x25d7a7:('lea','eax, [rdx - 2]'),0x25d7aa:('movzx','r8d, byte ptr [rcx + rbx + 4]'),0x25d7b3:('movzx','eax, byte ptr [rcx + rbx + 4]'),0x25d7b8:('cmp','r8d, eax'),0x25d7bb:('jne','0x25d760'),0x25d7bd:('cmp','r8d, edi'),0x25d7c0:('jne','0x25d760'),0x25d7d8:('mov','dword ptr [rbx], eax'),0x25d81e:('mov','ebp, dword ptr [rbx + rdx*4 + 0x184]'),0x25d7fb:('mov','dword ptr [rbx], eax'),0x25d832:('mov','esi, dword ptr [rbx + rdx*4 + 0x184]'),0x25d839:('cmp','esi, ebp'),0x25d83b:('jne','0x25d854'),0x25d83d:('xor','eax, eax'),0x25d857:('cmp','esi, ebp'),0x25d859:('cmovl','edi, eax'),0x25d85c:('mov','eax, edi'),0x25d77c:('mov','dword ptr [rbx], eax'),0x25d793:('movss','xmm7, dword ptr [rbx + rdx*4 + 0x184]'),0x25d860:('movd','xmm7, dword ptr [rbx + rdx*4 + 0x184]'),0x25d869:('cvtdq2ps','xmm7, xmm7'),0x25d883:('mov','dword ptr [rbx], eax'),0x25d892:('movss','xmm6, dword ptr [rbx + rdx*4 + 0x184]'),0x25d89d:('movd','xmm6, dword ptr [rbx + rdx*4 + 0x184]'),0x25d8a6:('cvtdq2ps','xmm6, xmm6'),0x25d8b2:('ucomiss','xmm6, xmm7'),0x25d8b5:('jp','0x25d8d0'),0x25d8b7:('jne','0x25d8d0'),0x25d8b9:('xor','eax, eax'),0x25d8d3:('comiss','xmm7, xmm6'),0x25d8d6:('cmova','edi, eax')}
for pc,pair in expected.items():assert (d[pc].mnemonic,d[pc].op_str)==pair,(hex(pc),pair)
assert roles.op_kind(d[0x25d7d8],d[0x25d7d8].operands[0],0)=='w'
assert roles.op_kind(d[0x25d7a1],d[0x25d7a1].operands[1],1)=='addr'
assert roles.op_kind(d[0x25d81e],d[0x25d81e].operands[1],1)=='r'
# Focused RMW adapter control on private instruction bytes, not shipping behavior.
rmw=next(cs.disasm(bytes.fromhex('830001'),0));assert roles.op_kind(rmw,rmw.operands[0],0)=='rw'
prior=json.loads((R/'prior72-result.json').read_text());praw=(R/'prior72-feasibility-raw.json').read_bytes();assert sha(praw)==prior['raw_sha256']=='fbbcf528c88c546a4f8da82b70dd7b740e2567d5634db07b5151547126b96439'
pm=json.loads((R/'prior72-manifest.json').read_text());members={m['path']:m for m in pm['members']}
for n in ['result.json','feasibility-raw.json','runner-adapted.py']:assert sha((R/('prior72-'+n)).read_bytes())==members[n]['sha256']
assert prior['state_label_correction']['status']=='ADDITIVE_INPUT_LABEL_CORRECTION_NOT_RECAPTURE';assert 'source/invocation-derived' in prior['state_label_correction']['limits']
obs=prior['observations'];assert [(o['input_signed'],o['mxcsr'],o['float32_bits']) for o in obs]==[(16777217,'0x1f80','4B800000'),(16777217,'0x5f80','4B800001')]
assert json.loads(praw)['instructions']['CVTDQ2PS']=='0f5bc0' and d[0x25d869].bytes.hex()=='0f5bff' and d[0x25d8a6].bytes.hex()=='0f5bf6'
f32=lambda bits:struct.unpack('<f',struct.pack('<I',int(bits,16)))[0]
sgn=lambda a,b:(a>b)-(a<b)
pred=[]
for o in obs:
 rc=o['mxcsr'];promoted=f32(o['float32_bits']);assert promoted==o['float32_value']
 pred.extend([dict(name='both-int-boundary',tags=[1,1],left=16777217,right=16777216,mxcsr=rc,predicted_return=sgn(16777217,16777216)),dict(name='mixed-boundary',tags=[1,2],left=16777217,right_float_bits='4B800000',mxcsr=rc,converted_left_bits=o['float32_bits'],predicted_return=sgn(promoted,16777216)),dict(name='mixed-reverse',tags=[2,1],left_float_bits='4B800000',right=16777217,mxcsr=rc,converted_right_bits=o['float32_bits'],predicted_return=sgn(16777216,promoted)),dict(name='exact-control',tags=[1,2],left=123,right_float_bits='42F80000',mxcsr=rc,predicted_return=sgn(123,f32('42F80000')))])
assert [p['predicted_return'] for p in pred]==[1,0,0,-1,1,1,-1,-1]
if '--fault-always-float' in sys.argv:assert pred[0]['predicted_return']==pred[1]['predicted_return'],'Both-int fast path retains distinctions lost by float promotion'
if '--fault-always-nearest' in sys.argv:assert pred[1]['predicted_return']==pred[5]['predicted_return'],'Mixed conditional result depends on supplied rounding mode'
if '--fault-reversed-order' in sys.argv:assert pred[5]['predicted_return']==pred[6]['predicted_return'],'Compare order is first/lower operand versus popped/top operand'
result=dict(status='CONDITIONAL_TYPED_COMPARISON_PRECISION',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),source_facts=['Depth>=2 inspects top and preceding tags; only equal tags1 choose signed integer path','Top payload goes EBP or XMM7; preceding/lower payload goes ESI or XMM6; comparisons return sign(lower versus top)','Both-int CMP ESI,EBP bypasses float conversion; mixed tag1 is MOVD/CVTDQ2PS, tag2 MOVSS','Float equality UCOMISS XMM6,XMM7; COMISS XMM7,XMM6 and CMOVA choose -1 when top > lower; otherwise +1'],conditional_predictions=pred,retained72_initial_state_limits=prior['state_label_correction'],interpretation='For supplied valid depth2 and finite boundary values, original source plus retained conversion bits predicts both-int 16777217 versus16777216 =>+1 in RN/RU; mixed int/float =>0 RN,+1 RU, reverse =>0 RN,-1 RU. Thus type-dispatch and MXCSR matter to comparison. No new comparator execution claimed.',consumer_change='Preserve signed int fast path versus mixed float promotion, exact instruction order/operand direction and supplied RC. Add boundary discriminator to typed comparator specification; do not apply all-float or always-nearest model. Actual mixed comparator execution, authored values/game RC/native flags and full caller remain open.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS78 original dispatch and retained conversion conditional predictions; STATIC_ONLY',flush=True)
