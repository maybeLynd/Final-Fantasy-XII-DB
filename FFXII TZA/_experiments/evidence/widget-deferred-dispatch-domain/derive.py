"""A: retained source, bounded branch calculations and private Python producer controls.
No original FF12 instruction execution, emulation, native calls or game access.
"""
import builtins,contextlib,hashlib,importlib.util,io,json,struct,subprocess,sys,datetime
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;ROOT=Path.cwd().resolve();sha=lambda b:hashlib.sha256(b).hexdigest()
REF=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
CHECK=ROOT/'Database/FFXII TZA/_index/candidates/mapscreen-child-widget/child_widget.py'
FIELDS=ROOT/'Database/FFXII TZA/_types/fields.tsv'
BASE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ENTRY=0x244DD0;SIZE=301
def off(raw,a):
 pe=struct.unpack_from('<I',raw,60)[0];n=struct.unpack_from('<H',raw,pe+6)[0];op=struct.unpack_from('<H',raw,pe+20)[0]
 for j in range(n):
  vs,va,rs,ro=struct.unpack_from('<IIII',raw,pe+24+op+j*40+8)
  if 0x120000+va<=a<0x120000+va+rs:return a-0x120000-va+ro
 raise AssertionError(hex(a))
def producer_child(case):
 raw=REF.read_bytes();assert sha(raw)==BASE;original=raw
 p=off(raw,0x244E66);assert raw[p:p+2]==bytes.fromhex('7305')
 if case!='canonical-baseline':raw=raw[:p]+b'\x72'+raw[p+1:]
 source=(W/'retained/producer.py').read_bytes();code=source
 if case=='private-mutant-certified-identity':
  assert source.count(BASE.encode())==1;code=source.replace(BASE.encode(),sha(raw).encode())
 else:assert case in ('canonical-baseline','unchanged-image-guard-negative')
 fields=(W/'retained/producer-field-projection.tsv').read_bytes();realopen=builtins.open;reads=[]
 def supplied(path,mode='r',*args,**kwargs):
  path=Path(path).resolve()
  if path==REF:assert mode=='rb';reads.append(dict(path=str(path),sha256=sha(raw)));return io.BytesIO(raw)
  if path==FIELDS:assert mode=='rb';reads.append(dict(path=str(path),sha256=sha(fields),scope='Exact current Widget and MapScreenContainer rows only; all other types ignored by producer S'));return io.BytesIO(fields)
  raise AssertionError('Unexpected producer input '+str(path))
 out=io.StringIO();rc=None
 with contextlib.redirect_stdout(out):
  builtins.open=supplied
  try:exec(compile(code,str(CHECK),'exec'),dict(__file__=str(CHECK),__name__='__main__'))
  except SystemExit as e:rc=e.code
  finally:builtins.open=realopen
 assert rc is not None
 print(json.dumps(dict(case=case,exit=rc,stdout=out.getvalue(),reads=reads,source_sha256=sha(source),invoked_source_sha256=sha(code),source_change='Only reference hash literal changed to actual private mutated-image SHA; arithmetic/branch/field obligations unchanged' if code!=source else None,reference_sha256=sha(raw),reference_original_sha256=BASE,patch=None if raw==original else dict(va='0x244e66',file_offset=p,before='73',after='72'),cleanup='builtins.open restored in finally, child exits; no file or game mutation')))
if '--child' in sys.argv:producer_child(sys.argv[-1]);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,detail=team.board_status(team.BOARD);assert ok,detail;b=json.loads(team.BOARD.read_text());t=next(t for t in b['tasks'] if t['id']=='ASTRA-WIDGET-DEFERRED-DISPATCH-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA';assert not (W/'result.json').exists()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py');assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('shipping_reader',rp);reader=importlib.util.module_from_spec(sp);sp.loader.exec_module(reader);image,ss=reader.load_image();assert sha(image)==BASE
prior=Path('Database/FFXII TZA/_experiments/evidence/spawn-widget-teardown/primary.json');pb=prior.read_bytes();pd=json.loads(pb);assert pd['exe_sha256']==BASE
body=next(x for x in pd['bodies'] if int(x['address'],16)==ENTRY)
code=b''.join(bytes.fromhex(i['bytes']) for i in body['instructions']);assert len(code)==body['bytes']==SIZE and sha(code)==body['sha256']=='24c646adcf49060e7fc09e19b0c2ae75077a9c7e0ea7d2c2a09daad9d139b454' and code==reader.img_rd(image,ss,ENTRY,SIZE)
pe=struct.unpack_from('<I',image,60)[0];rv,n=struct.unpack_from('<II',image,pe+24+112+3*8);pdata=reader.img_rd(image,ss,0x120000+rv,n)
prows=[(a+0x120000,z+0x120000,u+0x120000) for a,z,u in struct.iter_unpack('<III',pdata) if a+0x120000<ENTRY+SIZE and z+0x120000>ENTRY]
assert [(a,z) for a,z,u in prows]==[(0x244DD0,0x244E4B),(0x244E4B,0x244E62),(0x244E62,0x244E80),(0x244E80,0x244ED7),(0x244ED7,0x244EFD)]
unwind=[]
for a,z,u in prows:
 header=reader.img_rd(image,ss,u,4);flags=header[0]>>3;count=header[2];length=4+((2*count+3)//4)*4
 assert header[0]&7==1
 raw=reader.img_rd(image,ss,u,length+(12 if flags&4 else 0));chain=tuple(x+0x120000 for x in struct.unpack_from('<III',raw,length)) if flags&4 else None
 assert (flags==0 and (a,z,u)==prows[0] and chain is None) or (flags==4 and chain==prows[0])
 unwind.append(dict(start=hex(a),end_exclusive=hex(z),unwind=hex(u),raw_hex=raw.hex(),flags=flags,chain=None if chain is None else [hex(x) for x in chain]))
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
def bind(raw):
 ii={i.address:i for i in cs.disasm(raw,ENTRY)};assert sum(i.size for i in ii.values())==SIZE
 for a,h in {0x244DD0:'4885c9',0x244DD3:'0f8423010000',0x244E17:'8b5340',0x244E1A:'f6c201',0x244E1D:'750d',0x244E1F:'83637cf1',0x244E23:'834b7c01',0x244E27:'e9b3000000',0x244E2F:'c1e11c',0x244E32:'c1f91c',0x244E37:'740e',0x244E39:'83e902',0x244E3C:'7424',0x244E3E:'83f901',0x244E41:'0f85b0000000',0x244E62:'0fbae210',0x244E66:'7305',0x244E68:'33c9',0x244E6A:'894b70',0x244E73:'03c0',0x244E75:'2b4370',0x244E78:'2b4374',0x244E7B:'894374',0x244E7E:'eb57',0x244ED7:'83637cf4',0x244EDB:'834b7c04',0x244EDF:'834b7c30',0x244EE3:'488b03',0x244EE6:'4885c0',0x244EE9:'740c',0x244EEB:'488d150672bc01',0x244EF5:'ffd0',0x244EFC:'c3'}.items():assert ii[a].bytes.hex()==h,(hex(a),'original branch binding')
 for a,d in [(0x244DD3,0x244EFC),(0x244E1D,0x244E2C),(0x244E27,0x244EDF),(0x244E37,0x244E47),(0x244E3C,0x244E62),(0x244E41,0x244EF7),(0x244E66,0x244E6D),(0x244E7E,0x244ED7),(0x244EE9,0x244EF7)]:assert ii[a].operands[0].imm==d
 return ii
ii=bind(code)
def route(raw,flags40,flags7c,tick=100,duration=10,start=20,handler=True):
 it={i.address:i for i in cs.disasm(raw,ENTRY)};mode=flags7c&15;mode=mode-16 if mode>=8 else mode;after=flags7c;delay=duration;deadline=start;zeroed=False
 if not flags40&1:
  arm='bit0-clear-special-tail';after=(after&0xFFFFFFF1)|1;tail=True
 elif mode==0 or mode==3:
  # Complete dispatch analyzed, selection/arithmetic is reused from37, not calculated again.
  arm='schedule';after=(after&0xFFFFFFF4)|4;tail=True;delay=None;deadline=tick
 elif mode==2:
  arm='rebase';carry=bool(flags40&0x10000);skip_zero=(not carry) if it[0x244E66].mnemonic=='jae' else carry
  if not skip_zero:delay=0;zeroed=True
  deadline=(2*tick-delay-start)&0xFFFFFFFF;after=(after&0xFFFFFFF4)|4;tail=True
 else:
  arm='early-return';tail=False
 # Private default-JNE->JE source interpretation: mode1 newly falls into schedule, mode3 bails.
 if flags40&1 and it[0x244E41].mnemonic=='je' and mode not in (0,2):
  tail=mode!=3;arm='schedule' if tail else 'early-return';after=((flags7c&0xFFFFFFF4)|4) if tail else flags7c;delay=None if tail else duration;deadline=tick if tail else start
 if tail:after|=0x30
 return dict(flags40=f'{flags40:08X}',flags7c=f'{flags7c:08X}',signed_low_nibble=mode,arm=arm,zeroed70=zeroed,conditional_duration70=delay,conditional_deadline74=deadline,flags7c_after_local=f'{after:08X}',shared_tail_reached=tail,indirect_call_site_reached=tail and handler,handler_present=handler,scope='Host/source conditional branch calculation; no original instruction/callback execution')
cases=[route(code,1,m) for m in range(16)]
special=route(code,0,2);rebase_clear=route(code,1,2);rebase_set=route(code,0x10001,2);nullhandler=route(code,0,2,handler=False)
assert [c['signed_low_nibble'] for c in cases]==list(range(8))+list(range(-8,0)) and [m for m,c in enumerate(cases) if c['shared_tail_reached']]==[0,2,3]
assert rebase_clear['conditional_deadline74']==170 and not rebase_clear['zeroed70'] and rebase_set['conditional_deadline74']==180 and rebase_set['zeroed70']
assert special['flags7c_after_local']=='00000031' and special['conditional_duration70']==10 and special['conditional_deadline74']==20 and not nullhandler['indirect_call_site_reached']
mutants=[]
for name,pc,offset,value,test_flags,test_mode in [('reversed-bit16-zero-branch',0x244E66,0,0x72,0x10001,2),('inverted-default-return',0x244E41,1,0x84,1,1)]:
 mut=bytearray(code);mut[pc-ENTRY+offset]=value;rejected=False
 try:bind(bytes(mut))
 except AssertionError:rejected=True
 assert rejected;before=route(code,test_flags,test_mode);after=route(mut,test_flags,test_mode);assert before!=after
 mutants.append(dict(name=name,pc=hex(pc),mutant_body_hex=bytes(mut).hex(),original_binding_rejected=rejected,baseline=before,private_source_calculation=after))
R=W/'retained';R.mkdir(exist_ok=False);(R/'source.bin').write_bytes(code);(R/'prior-body.json').write_text(json.dumps(body,indent=2)+'\n');(R/'shipping-reader.py').write_bytes(rp.read_bytes())
(R/'extent-proof.json').write_text(json.dumps(dict(ranges=unwind,interpretation='Five contiguous .pdata ranges cover the complete retained301B; four UNW_FLAG_CHAININFO records point to the first123B root. One root row is not the whole logical body.',format_source='https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64?view=msvc-170'),indent=2)+'\n')
(R/'initial-failed-derive.py').write_bytes((W/'initial-failed-derive.py').read_bytes());(R/'initial-failure.json').write_bytes((W/'initial-failure.json').read_bytes())
oldconst=Path('Database/FFXII TZA/_experiments/evidence/spawn-widget-teardown/constants.json');ocb=oldconst.read_bytes();oc=json.loads(ocb);assert oc['exe_sha256']==BASE;constant=next(x for x in oc['records'] if int(x['address'],16)==0x1E0C0F8);cb=bytes.fromhex(constant['raw_hex']);assert reader.img_rd(image,ss,0x1E0C0F8,len(cb))==cb and struct.unpack('<QQQ',cb)==(15,0,0);assert ii[0x244EEB].address+ii[0x244EEB].size+ii[0x244EEB].operands[1].mem.disp==0x1E0C0F8;(R/'notification-record.bin').write_bytes(cb)
paths={'widget-contract.md':'Database/FFXII TZA/16-UI/Widget-Object-Model/CONTRACT-widget-object.md','layout-entry.md':'Database/FFXII TZA/16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md','producer.py':CHECK.relative_to(ROOT).as_posix()}
pre=[]
for name,p in paths.items():
 data=Path(p).read_bytes();(R/name).write_bytes(data);pre.append(dict(path=p,sha256=sha(data)))
fields=FIELDS.read_bytes();projection=b''.join(line for line in fields.splitlines(keepends=True) if line.split(b'\t')[0] in (b'Widget',b'MapScreenContainer'));assert projection and b'Widget\t0x070\t' in projection;(R/'producer-field-projection.tsv').write_bytes(projection)
(R/'field-preimage.json').write_text(json.dumps(dict(source_path=FIELDS.relative_to(ROOT).as_posix(),whole_source_sha256=sha(fields),projection_sha256=sha(projection),scope='Exact full rows of the only two types used by producer S; not whole types validation'),indent=2)+'\n')
controls=[]
for name in ('canonical-baseline','unchanged-image-guard-negative','private-mutant-certified-identity'):
 p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',name],capture_output=True,text=True,timeout=30);assert p.returncode==0 and not p.stderr,(name,p.stdout,p.stderr);controls.append(json.loads(p.stdout))
assert controls[0]['exit']==controls[2]['exit']==0 and controls[1]['exit']==2 and all('PASS  G' in c['stdout'] and 'FAILS 0' in c['stdout'] for c in (controls[0],controls[2])) and 'REFUSED' in controls[1]['stdout']
contract=(R/'widget-contract.md').read_text();page=(R/'layout-entry.md').read_text();assert 'clear). Mode **1** bails' in contract and 'clears `[+0x70]` when bit 16 is set' in page and 'The tail always ORs `0x34`' in page
dll=Path(capstone._cs._name);result=dict(method='A retained original301B source/branch calculations + actual Python producer input controls, zero FF12/original-code/native/emulator/live executions',reference=dict(exe_sha256=BASE,entry=hex(ENTRY),bytes=SIZE,body_sha256=sha(code),pe_ranges=unwind,reader_sha256=sha(rp.read_bytes()),prior_primary_path=prior.as_posix(),prior_primary_sha256=sha(pb),prior_constants_path=oldconst.as_posix(),prior_constants_sha256=sha(ocb),original_retained_body_sha256=body['sha256']),tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),capstone=capstone.__version__,capstone_dll=dict(path=str(dll),sha256=sha(dll.read_bytes()))),driver_sha256=sha(Path(__file__).read_bytes()),instructions=[dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in ii.values()],active_gate_modes=cases,controls=dict(bit0_clear=special,mode2_bit16_clear=rebase_clear,mode2_bit16_set=rebase_set,null_handler=nullhandler),mutants=mutants,producer_controls=controls,consumer_preimages=pre,interpretation='At stable post-prefix snapshot: flags40 bit0clear skips mode switch, forces low nibble1 and OR30, preserves+70/+74, conditionally reaches15 call. Bit0set modes0/3schedule, mode2rebase, all other signed low nibble values return beforetail. Mode2 bit16SET zeroes+70 before deadline, bit16clear preserves it. Both schedule/rebase normalize low nibble4 then OR30. Nullhandler suppresses call. Widget contract clear-polarity is refuted; layout page bit-set is correct, its universalOR34/getter/divide60 wording is overbroad. Existing child_widget G checks width/arithmetic/stores but not bit16 branch: exact image guard correctly refuses changedsource; private hash-pin-adjusted mutant stillGpass. Request focused owner source regression; canonicalindex not regressed.',limits='No native effects of prefix calls, getter, callback, actual caller/initialization/scheduling/cadence/presentation or valid-mode occurrence proved. Nullself returns before prefix from exactsource; all modeled nonnull paths first write+ B8/call predicates, so earlyreturn is not wholefunction no-effect. Nonvolatile ABI/stable readable widget and completed calls assumed. No37timer replay, broad mode taxonomy, runtime callback acceptance or live menu/load progress claim.',cleanup='Private Python input bytes only; certified image unchanged; open restored on every child path; PC OFF, no game/peer/save/config writes; consumers/independent acceptance pending')
assert sha(REF.read_bytes())==BASE;(W/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('Derived exact deferred dispatch: mode2 bit16SET zeroesdelay; bit0clear state1 tail; active modes only0/2/3 tail. Producer integrity rejects mutant, G obligation still passes private properly identified source mutation.',flush=True)
