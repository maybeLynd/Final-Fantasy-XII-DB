import ast,hashlib,json,struct,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text());ref=raw['reference'];code=(R/'original-popv256.bin').read_bytes();store=(R/'original194.bin').read_bytes();table=(R/'original-table24.bin').read_bytes();policy=(R/'reg_tracking.py').read_bytes();source=(R/'fable-float-primary.py').read_bytes();assert sha(code)==ref['code_sha256'] and sha(store)==ref['store_sha256'] and sha(table)==ref['table_sha256'] and sha(policy)==ref['adapter_sha256'] and sha(source)==ref['consumer_sha256'] and sha((R/'runner.py').read_bytes())==ref['runner_sha256']
roles=types.ModuleType('roles');exec(compile(policy,'shared reviewed adapter source','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii={i.address:i for i in cs.disasm(code,0x267e60)}
assert ii[0x267ed2].bytes.hex()=='0f5bc0' and roles.op_kind(ii[0x267ec9],ii[0x267ec9].operands[1],1)=='r' and roles.op_kind(ii[0x267ed5],ii[0x267ed5].operands[0],0)=='w'
tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cvt');bits=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='bits' for t in n.targets));assert sha(ast.dump(fn,include_attributes=True).encode())==ref['consumer_cvt_ast_sha256'];ns=dict(struct=struct);exec(compile(ast.Module(body=[bits,fn],type_ignores=[]),'actual unchanged FABLE bits/cvt helper','exec'),ns)
assert raw['input_signed']==-16777219 and len(raw['cases'])==2 and raw['consumer_original_default']['returncode']==0 and 'FAILS 0' in raw['consumer_original_default']['stdout']
assert 'positive values' in source.decode(),'Preserve declared bounded helper comment; no false prior general acceptance'
expected={'RN':('0x1f80','020080cb',-16777220.0),'RU':('0x5f80','010080cb',-16777218.0)};obs=[]
for c,mode in zip(raw['cases'],['RN','RU']):
 mx,value,number=expected[mode];assert c['initial']['mxcsr']==mx and c['initial']['kind_selector_r8d']==1 and (c['tag'],c['width'],c['depth'],c['mutated'])==(1,5,1,False)
 ram=bytearray.fromhex(c['initial']['ram']);assert struct.unpack_from('<i',ram,0x100)[0]==1 and ram[0x104]==1 and struct.unpack_from('<i',ram,0x284)[0]==-16777219
 rec=bytearray.fromhex(c['initial']['record']);assert struct.unpack_from('<H',rec,4)[0]==2 and struct.unpack_from('<I',rec,24)[0]==0x58000000 and struct.unpack_from('<Q',rec,16)[0]==0x40000900
 p=c['conversion'];a=c['after'];assert p['value_bits']==value and p['pc']=='0x267f1e' and a['pc']=='0x60000200' and p['rsp']==a['rsp']=='0x60001800' and p['depth']==0
 rec[32:36]=bytes.fromhex(value);assert p['record']==a['record']==rec.hex();ram[0x100:0x104]=b'\0'*4;assert p['ram']==ram.hex();ram[0x900:0x904]=bytes.fromhex(value);assert a['ram']==ram.hex()
 assert c['running_hex']==a['running_popv']==code.hex() and a['store']==store.hex() and a['table']==table.hex() and a['return_sentinel']==struct.pack('<Q',0x60000200).hex()
 v=[x for x in c['visits'] if x['phase']=='conversion'];st=[x for x in c['visits'] if x['phase']=='store'];assert v and st and len(v)<=32 and len(st)<=64 and v[0]['pc']=='0x267e9c' and st[0]['pc']=='0x26d530' and any(x['pc']=='0x267ed2' for x in v)
 for x in v:assert ii[int(x['pc'],16)].bytes.hex()==x['hex'] and ii[int(x['pc'],16)].mnemonic!='call'
 cw=[x for x in c['writes'] if x['phase']=='conversion'];sw=[x for x in c['writes'] if x['phase']=='store'];assert len(cw)==2 and len(sw)==1 and sw[0]['hex']==value and sw[0]['size']==4
 actual_bits=struct.unpack('<I',bytes.fromhex(value))[0];actual_value=struct.unpack('<f',bytes.fromhex(value))[0];model=ns['cvt'](-16777219,mode);assert f'{model:08X}'==raw['consumer_negative_model'][mode] and actual_value==number
 if mode=='RN':assert model==actual_bits==0xcb800002
 else:assert model==0xcb800003 and actual_bits==0xcb800001
 if '--fault-positive-bit-order-for-negative' in sys.argv:assert model==actual_bits,'Positive-domain RU bitincrement cannot be reused for negativeinput'
 if '--fault-rounded-value-is-more-negative' in sys.argv and mode=='RU':assert actual_value<-16777219,'Original RU moves thisnegativeinput numericallyup'
 if '--fault-positive-default-proves-negative' in sys.argv and mode=='RU':assert raw['consumer_original_default']['returncode']!=0,'Green default covers positive-domain fixtures, not thisnegative extension'
 obs.append(dict(input_signed=-16777219,mxcsr=mx,mode=mode,original_guest_converted_and_stored_bits=f'{actual_bits:08X}',original_guest_value=actual_value,actual_existing_consumer_helper_bits=f'{model:08X}',same=actual_bits==model,guest_mxcsr_after=p['mxcsr']))
result=dict(status='NEGATIVE_RU_NUMERIC_UP_REQUIRES_REVERSED_BIT_DIRECTION',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=obs,interpretation='For testednegative16777219 atfloat-kindstage, originalguest RNstoresCB800002(-16777220), RUstoresCB800001(-16777218). ExistingFABLEhelpercomment explicitlypositive-domainRU; callingitoutside thatdomain returnsCB800003(-16777222). ItsunchangeddefaultpositivefixturesPASS. Acceptedpositive72 remainsvalid; do not extrapolatehelpertoall signedinputs withoutdomainenforcement orsign-aware bitneighbor correction.',consumer_change='Preserve newnegative originalobservations/limits. For broaderreconstructioncontract, correctRU bitneighbor by sign or enforce positivehelperdomain andkeepnegativeextensionopenuntilincorporated; addactualdefault/domaincontrols andaffectedprose/spec, not justresulttext. Not allnegativeinputs/directions/nativeflags proved.',limits=raw['limits']+' Consumer incorporation/independentacceptance pending; nopeeredit/publishedinput rewrite.')
p=W/'result.json';out=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==out,'Frozen result differs'
else:p.write_bytes(out)
print('PASS75 two newnegativeoriginal RC states/consumerpositive-domain limit',flush=True)
