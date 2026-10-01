import ast,hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());source=(R/'fable-array-clamp-primary.py').read_bytes();code=(R/'resolver591.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes();ref=raw['reference'];assert sha(source)==ref['consumer_primary_sha256'] and sha(code)==ref['original_source_sha256'] and sha(policy)==ref['adapter_sha256']
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='clamp');assert sha(ast.dump(fn,include_attributes=True).encode())==ref['consumer_function_ast_sha256'];ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'unchanged original consumer clamp','exec'),ns)
roles=types.ModuleType('roles');exec(compile(policy,'shared reviewed adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x262440)}
assert ii[0x262513].bytes.hex()=='8d46ff' and ii[0x262513].op_str=='eax, [rsi - 1]' and ii[0x262513].operands[0].size==4 and roles.op_kind(ii[0x262513],ii[0x262513].operands[1],1)=='addr'
assert ii[0x262516].op_str=='ecx, esi' and ii[0x262518].mnemonic=='cmovl' and ii[0x262518].op_str=='eax, ecx' and ii[0x262510].op_str=='ecx, eax' and ii[0x262510].mnemonic=='cmovns'
assert raw['consumer_default']['returncode']==0 and 'FAILS 0' in raw['consumer_default']['stdout'],'Actual unchanged producer default is green despite missed boundary'
signed=lambda n:struct.unpack('<i',struct.pack('<I',n&0xffffffff))[0]
controls=[];mismatches=[]
for c in raw['cases']:
 i,d=c['index'],c['dimension'];assert -(1<<31)<=i<(1<<31) and -(1<<31)<=d<(1<<31);lower=max(i,0);upper=signed(d-1);pred=lower if lower<d else upper;actual=ns['clamp'](i,d)
 assert actual==c['actual_original_fable_model'] and pred==c['source_predicted_signed_clamped'] and f'{(d-1)&0xffffffff:08x}'==c['decoded_lea_upper_bits']
 corrected=lower if lower<d else signed(d-1);assert corrected==pred
 if d==-2147483648:assert actual==-2147483649 and pred==2147483647;mismatches.append(c)
 else:assert actual==pred;controls.append(c)
 if '--fault-real-number-dim-minus-one' in sys.argv:assert actual==pred,'Actual consumer unbounded subtraction disagrees with original32bit boundary'
 if '--fault-accept-green-default' in sys.argv and d==-2147483648:assert raw['consumer_default']['returncode']!=0,'Green default does not cover the signed-min dimension'
assert len(mismatches)==3 and len(controls)==5
result=dict(status='CONSUMER_NEGATIVE_DIMENSION_RULE_MISSES_SIGNED_MIN_WRAP',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),boundary_mismatches=mismatches,unchanged_domain_controls=controls,actual_default_green=raw['consumer_default'],producer_fix='Preserve originalwidth: lower=max(signed32index,0); upper=signed32(low32(dim-1)); choose lower iff signedlower<signeddimension else upper. Add signedMIN/MIN+1 controls to actualproducer/check/default and affectedcontract/prose, notonly resulttext.',interpretation='The positive-dimension edgeclamp anddim0 resultremainvalid; FABLEproducer/canonicalunqualified negative-dimension formula extrapolates past signed32MIN. OriginalLEAupper wraps80000000-1 to7FFFFFFF, signedCMOVL false forlower>=0 againstnegativeMIN; predictedindex2147483647, NOTPython-2147483649. This is conditionalstaticinstruction analysis plus actualconsumerexecution, notFF12execution/asset/gamefault.',limits=raw['limits']+' Ownercorrection/consumeragreement/independentacceptance pending; original publishedproducer/raw immutable, nopeeredit.')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS73 actual default misses signedMIN32bitLEA boundary; staticonly',flush=True)
