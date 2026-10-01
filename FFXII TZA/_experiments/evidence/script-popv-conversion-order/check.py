import hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());code=(R/'original-popv256.bin').read_bytes();store=(R/'original194.bin').read_bytes();table=(R/'original-table24.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes()
assert len(code)==256 and sha(code)==raw['reference']['popv_sha256'] and sha(store)==raw['reference']['store_sha256'] and sha(table)==raw['reference']['table_sha256'] and sha(policy)==raw['reference']['access_adapter_sha256']
roles=types.ModuleType('roles');exec(compile(policy,'retained shared reviewed adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x267e60)}
for pc,m,a in [(0x267e84,'movsx','r8d, word ptr [rsp + 0x34]'),(0x267e8c,'sub','r8d, 1'),(0x267e90,'je','0x267ef2'),(0x267f1a,'mov','dword ptr [rsp + 0x50], eax'),(0x267f37,'call','0x26d530'),(0x267f4c,'cvttss2si','eax, dword ptr [rbx + rdx*4 + 0x184]'),(0x267f55,'jmp','0x267f1a')]:assert (ii[pc].mnemonic,ii[pc].op_str)==(m,a),(hex(pc),ii[pc].op_str)
assert roles.op_kind(ii[0x267f1a],ii[0x267f1a].operands[0],0)=='w'
assert roles.op_kind(ii[0x267f4c],ii[0x267f4c].operands[1],1)=='r'
targets=[0x120000+x for x in struct.unpack('<6I',table)];assert len(targets)==6 and all(0x26d530<=a<0x26d5f2 for a in targets)
allowed=set(raw['reference']['stage_allowed_pcs']);assert raw['reference']['stage_entry']=='0x267ef2' and raw['reference']['stage_stop']=='0x267f1e'
specs=[(2,'3fe00000',0,1,False,'01000000','01'),(2,'4effffff',0,1,False,'80ffff7f','ff'),(2,'4f000000',0,1,False,'00000080','00'),(2,'4effffff',3,1,False,'80ffff7f','0080'),(2,'4f000000',3,1,False,'00000080','0180'),(1,'7fffffff',0,1,False,'ffffff7f','ff'),(2,'3fe00000',0,0,False,'00000000','00'),(2,'3fe00000',0,1,True,'02000000','02')]
assert len(raw['cases'])==len(specs) and len(specs)>0
observations=[]
for c,s in zip(raw['cases'],specs):
 tag,bits,width,depth,mutated,value,dest=s;assert (c['tag'],c['input_bits'],c['width'],c['depth'],c['mutated'])==(tag,bits,width,depth,mutated)
 assert c['initial']['mxcsr']=='0x1f80' and c['initial']['entry']=='0x267ef2' and c['initial']['stop']=='0x267f1e'
 p=c['conversion'];a=c['after'];assert p['pc']=='0x267f1e' and a['pc']==c['initial']['return_sentinel'] and p['rsp']==a['rsp']==c['initial']['rsp'] and p['depth']==0
 assert p['value_bits']==value,'Original conversion boundary bits'
 rec=bytearray.fromhex(c['initial']['record']);rec[32:36]=bytes.fromhex(value);assert p['record']==a['record']==rec.hex(),'Exact only record+20 stage change'
 ram=bytearray.fromhex(c['initial']['ram']);ram[0x100:0x104]=b'\0'*4;assert p['ram']==ram.hex(),'Conversion depth decrement only RAM change'
 ram[0x900:0x900+len(bytes.fromhex(dest))]=bytes.fromhex(dest);assert a['ram']==ram.hex(),'Exact downstream store/guard effects'
 expected=bytearray(code)
 if mutated:expected[0x267f4c-0x267e60+2]=0x2d
 assert c['running_hex']==a['running_popv']==expected.hex() and a['store']==store.hex() and a['table']==table.hex() and a['return_sentinel']==struct.pack('<Q',int(c['initial']['return_sentinel'],16)).hex()
 v=[x for x in c['visits'] if x['phase']=='conversion'];st=[x for x in c['visits'] if x['phase']=='store'];assert v and st and len(v)<=32 and len(st)<=64 and all(x['pc'] in allowed for x in v) and st[0]['pc']=='0x26d530'
 if tag==2 and depth:
  assert any(x['pc']=='0x267f4c' for x in v),'Actual conversion executed'
  if mutated:assert any(x['hex']=='f30f2d849384010000' for x in v),'Actual private opcode executed'
 if tag==1:assert any(x['pc']=='0x267f57' for x in v) and not any(x['pc']=='0x267f4c' for x in v)
 if depth==0:assert not any(x['pc'] in ['0x267f4c','0x267f57'] for x in v),'Empty path did not read payload'
 sw=[x for x in c['writes'] if x['phase']=='store'];cw=[x for x in c['writes'] if x['phase']=='conversion'];assert len(sw)==1 and sw[0]['hex']==dest and sw[0]['address']=='0x40000900' and len(cw)==(2 if depth else 1)
 if '--fault-direct-float-clamp' in sys.argv and bits=='4f000000' and width==0:assert dest=='ff','Direct real-float saturation contradicts original converted dword'
 if '--fault-round-not-truncate' in sys.argv and bits=='3fe00000' and depth and not mutated:assert value=='02000000','Original CVTT truncation differs rounding detector'
 if '--fault-accept-rounding-mutation' in sys.argv and mutated:assert value==raw['cases'][0]['conversion']['value_bits'],'Private rounding mutation changes original result'
 observations.append(dict(tag=tag,depth=depth,float32_bits_or_int_bits=bits,width=width,intervention='privateCVTT->CVT' if mutated else 'originalinstructions/injectedentry-state',converted_dword_little_endian=value,destination_little_endian=dest,stage_instructions=len(v),store_instructions=len(st),guest_mxcsr_after=p['mxcsr']))
result=dict(status='INTEGER_CONVERSION_PRECEDES_WIDTH_SATURATION',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=observations,interpretation='Under injected validtag2/integer-kind/MXCSR1F80 gueststate, originalCVTT convertsfloat32 1.75 to1, largestbelow2^31 to7FFFFF80, +2^31 to80000000; originalstore interprets signedinput thenclamps: u8 +2^31 inputstores00, s16stores8001 ratherthan8000 frombelowboundary. Originaltag1 rawINT_MAXstoresFF; emptystackzero. ExplicitprivateCVTT->CVT makes1.75->2/store02, notshippingbehavior. Staticoriginalkindbranch/write+20/storecall establishes intendedlocalorder, notfullnormalVMcaller/live reachability.',limits='Two bounded original operations composed by injectedentryABI. Fullresolver/notification omitted atboundaries, nostubs, no fullPOPVexecution orlivegame/nativeCPU/unmaskedexceptions/MXCSRflagsparity. Actualbankstate/lifetime/callerreachability andcallbackbeforestoreeffects OPEN. Masked conversion sentinel notproofnativeexceptionstatus. No sourcechanged/realfloatclampreplacement/generalfloatdomain claim. Independentacceptance/consumer incorporation pending; PC OFF/S19/fullL1+L2 NOT_MET')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS70 exact original conversion bits thenstore; injected boundaries, no callback/live',flush=True)
