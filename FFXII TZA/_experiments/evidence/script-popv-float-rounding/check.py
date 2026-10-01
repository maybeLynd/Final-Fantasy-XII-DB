import ast,hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'feasibility-raw.json').read_text());assert raw['status']=='FEASIBLE_DIRECTED_ROUNDING_VALUE_DISCRIMINATOR'
source=(R/'original70-capture.py').read_bytes();assert sha(source)==raw['source_sha256'];fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='run');assert sha(ast.dump(fn,include_attributes=True).encode())==raw['original_runner_ast_sha256']
assert (W/'runner-original70.py').read_text()==ast.unparse(fn)+'\n' and sha((W/'runner-adapted.py').read_text().rstrip('\n').encode())==raw['adapted_runner_sha256']
code=(R/'original-popv256.bin').read_bytes();store=(R/'original194.bin').read_bytes();table=(R/'original-table24.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes();ref=raw['source_identity'];assert sha(code)==ref['popv_sha256'] and sha(store)==ref['store_sha256'] and sha(table)==ref['table_sha256'] and sha(policy)==ref['access_adapter_sha256']
roles=types.ModuleType('roles');exec(compile(policy,'retained shared adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x267e60)}
assert ii[0x267e84].op_str=='r8d, word ptr [rsp + 0x34]' and ii[0x267e8c].op_str=='r8d, 1' and ii[0x267e96].op_str=='0x267f1e'
assert ii[0x267ec9].bytes.hex()==raw['instructions']['MOVD']=='660f6e849384010000' and ii[0x267ed2].bytes.hex()==raw['instructions']['CVTDQ2PS']=='0f5bc0'
assert roles.op_kind(ii[0x267ec9],ii[0x267ec9].operands[1],1)=='r' and roles.op_kind(ii[0x267ed5],ii[0x267ed5].operands[0],0)=='w'
assert len(raw['cases'])==2 and raw['input_signed']==16777217 and raw['values']==['0000804b','0100804b']
obs=[]
for c,mx,expected in zip(raw['cases'],['0x1f80','0x5f80'],['0000804b','0100804b']):
 assert c['initial']['mxcsr']=='0x1f80' and (int(c['conversion']['mxcsr'],16)&0x6000)==(int(mx,16)&0x6000) and (c['tag'],c['depth'],c['width'],c['mutated'])==(1,1,5,False)
 ram=bytearray.fromhex(c['initial']['ram']);assert struct.unpack_from('<i',ram,0x100)[0]==1 and ram[0x104]==1 and struct.unpack_from('<i',ram,0x284)[0]==16777217
 rec=bytearray.fromhex(c['initial']['record']);assert struct.unpack_from('<H',rec,4)[0]==2 and struct.unpack_from('<I',rec,24)[0]==0x58000000 and struct.unpack_from('<Q',rec,16)[0]==0x40000900 and struct.unpack_from('<i',rec,28)[0]==0
 p=c['conversion'];a=c['after'];assert p['value_bits']==expected and p['pc']=='0x267f1e' and a['pc']=='0x60000200' and p['rsp']==a['rsp']=='0x60001800' and p['depth']==0
 rec[32:36]=bytes.fromhex(expected);assert p['record']==a['record']==rec.hex();ram[0x100:0x104]=b'\0'*4;assert p['ram']==ram.hex();ram[0x900:0x904]=bytes.fromhex(expected);assert a['ram']==ram.hex()
 assert c['running_hex']==a['running_popv']==code.hex() and a['store']==store.hex() and a['table']==table.hex() and a['return_sentinel']==struct.pack('<Q',0x60000200).hex()
 v=[x for x in c['visits'] if x['phase']=='conversion'];st=[x for x in c['visits'] if x['phase']=='store'];assert v and st and len(v)<=32 and len(st)<=64 and v[0]['pc']=='0x267e9c' and st[0]['pc']=='0x26d530'
 assert any(x['pc']=='0x267ec9' for x in v) and any(x['pc']=='0x267ed2' for x in v) and not any(x['pc'] in ['0x267ee2','0x267ee7','0x267ef2','0x267f4c'] for x in v),'Actual selected int-to-float route, no error/other-kind path'
 for x in v:assert ii[int(x['pc'],16)].bytes.hex()==x['hex']
 cw=[x for x in c['writes'] if x['phase']=='conversion'];sw=[x for x in c['writes'] if x['phase']=='store'];assert len(cw)==2 and len(sw)==1 and sw[0]['size']==4 and sw[0]['hex']==expected
 if '--fault-always-nearest' in sys.argv:assert p['value_bits']=='0000804b','Directed RC changes original float conversion value'
 if '--fault-preserve-int-bits' in sys.argv:assert p['value_bits']=='01000001','Original CVTDQ2PS converts integer bits before storing float'
 if '--fault-use-original-state-label' in sys.argv:assert c['initial']['mxcsr']==mx,'Original second-case input label is stale and needs additive correction'
 obs.append(dict(input_signed=16777217,mxcsr=mx,rounding='nearest-even' if mx=='0x1f80' else 'toward-positive-infinity',float32_bits=f'{struct.unpack("<I",bytes.fromhex(expected))[0]:08X}',float32_value=struct.unpack('<f',bytes.fromhex(expected))[0],original_stage_instructions=len(v),original_store_instructions=len(st),guest_mxcsr_after=p['mxcsr']))
correction=json.loads((W/'state-metadata-correction.json').read_text());assert [x['mxcsr'] for x in correction['normalized_initial']]==['0x1f80','0x5f80'];assert 'u.reg_write(UC_X86_REG_R8D, 1)' in (W/'runner-adapted.py').read_text() and 'u.reg_write(UC_X86_REG_MXCSR, mxcsr)' in (W/'runner-adapted.py').read_text()
result=dict(state_label_correction=correction,status='FLOAT_KIND_COERCION_DEPENDS_ON_MXCSR_RC',method=raw['method'],raw_sha256=sha((W/'feasibility-raw.json').read_bytes()),observations=obs,interpretation='For tested signed16777217 under injectedfloat-kind path/kind2/descriptor58000000, originalMOVD/CVTDQ2PS/MOVSS thenoriginalwidth5store yields4B800000 (16777216) atmaskedRN1F80 and4B800001 (16777218) atmaskedRU5F80. Only initialRC differs. An alwaysnearest hostcast/rawbitcopy is insufficient for bitexactreconstruction ofthiscoercion. These two controls settlethisclaim, no extra cases required.',limits='Originalboundedemulatorstages/composedstore underinjectedstate/entryABI, notfullPOPV/resolver/lookup/nativeCPU/game/callerreachability/validshippedcombination/bankinit/lifetime. No nativeMXCSRflag/status orunmaskedexceptions parity; negative/directeddown/otherfloatdomain nottested.70integercases notrerun. Independentacceptance/consumer incorporation pending. PC OFF/S19/fullL1+L2 NOT_MET')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS72 two original float coercion RC controls settle tested claim, no new guest execution',flush=True)
