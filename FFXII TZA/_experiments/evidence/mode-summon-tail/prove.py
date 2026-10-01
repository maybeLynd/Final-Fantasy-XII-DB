"""Exact immediate tail effects, with the unclosed native suffix explicit."""
import argparse,hashlib,importlib.util,json,re,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;T=P.parent if(P.parent/'validate-title-source-annotations.py').exists() else P/'dependencies'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(src,out):
 if out.exists():raise RuntimeError('immutable result exists')
 inputs=[]
 for tag,driver,source in [('capture-01','capture.py','source-01.json'),('stack-capture-01','capture-stack-probe.py','stack-probe-source-01.json')]:
  st=json.loads((src/(tag+'.status.json')).read_text())
  if st.get('exit')!=0 or st.get('terminal') is not True or st.get('exception') is not None or st['driver_sha256']!=sha(src/driver) or not(src/(tag+'.stdout')).read_bytes() or(src/(tag+'.stderr')).read_bytes():raise RuntimeError('upstream capture failed/incomplete '+tag)
  v=json.loads((src/source).read_text())
  if v.get('wrapper_complete') is not True or v['wrapper_sha256']!=sha(src/driver):raise RuntimeError('mixed/incomplete source wrapper')
  inputs.append(v)
 V=load('summon_tail_rolecheck',T/'validate-title-source-annotations.py');annotations=[V.validate(v) for v in inputs]
 G=load('summon_tail_cfg',T/'prove_owner_reload_order.py')
 if sha(T/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':raise RuntimeError('graph changed')
 raw=(G.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise RuntimeError('wrong original image')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,offset in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
  raise RuntimeError('unbacked source')
 ranges=[r for v in inputs for r in v['ranges']]
 if[(r['start'],r['end_exclusive']) for r in ranges]!=[('0x313550','0x31358a'),('0x35c620','0x35c62c'),('0x273e30','0x273ebc'),('0x808f10','0x808f61')]:raise RuntimeError('required source population changed')
 for r in ranges:
  lo=int(r['start'],16);hi=int(r['end_exclusive'],16)
  if bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(lo,hi-lo):raise RuntimeError('original byte mismatch')
 ix={int(i['pc'],16):i for r in ranges for i in r['instructions']}
 pins=[(0x313550,'mov','r8, qword ptr [rip + 0x2babc39]'),(0x313557,'mov','edx, dword ptr [r8 + 0x5b04]'),(0x31355e,'mov','eax, edx'),(0x313560,'and','eax, 1'),(0x313563,'cmp','eax, ecx'),(0x313565,'je','0x313589'),(0x313567,'test','ecx, ecx'),(0x313569,'je','0x31357a'),(0x31356b,'or','edx, 1'),(0x31356e,'mov','dword ptr [r8 + 0x5b04], edx'),(0x313575,'jmp','0x35c620'),(0x31357a,'and','edx, 0xfffffffe'),(0x31357d,'mov','dword ptr [r8 + 0x5b04], edx'),(0x313584,'jmp','0x35c620'),(0x313589,'ret',''),(0x35c620,'lea','rcx, [rip + 0x1f6dde1]'),(0x35c627,'jmp','0x273e30'),(0x273e50,'mov','eax, 0x1210'),(0x273e55,'call','0x808f10'),(0x273e5a,'sub','rsp, rax'),(0x273e92,'xor','eax, eax'),(0x273e9e,'mov','qword ptr [rcx], rax'),(0x273ea7,'mov','qword ptr [rcx + 8], rax'),(0x273eab,'mov','rdi, rcx'),(0x273eae,'mov','qword ptr [rcx + 0x10], rax'),(0x273eb5,'mov','qword ptr [rcx + 0x18], rax')]
 for pc,m,a in pins:
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('tail/receiver/store operation changed '+hex(pc))
 graphs=[]
 for r,tail in [(ranges[0],'0x35c620'),(ranges[1],'0x273e30')]:
  local={int(i['pc'],16):i for i in r['instructions']};g=G.graph(local,int(r['start'],16),int(r['end_exclusive'],16),tail=tail)
  if g['calls']:raise RuntimeError('unexpected setter/thunk call')
  graphs.append({'entry':r['start'],'visited':len(g['visited']),'returns':[hex(i) for i in g['returns']],'tails':[{'pc':hex(i),'target':tail} for i in g['tails']]})
 if len(graphs[0]['tails'])!=2 or len(graphs[1]['tails'])!=1:raise RuntimeError('tail graph incomplete')
 probe=ranges[3]['instructions']
 # Original helper touches R10/R11/RSP, readsRAX/GS and stack pages; it has
 # no call or RCX/RDX/RAX destination. We do not erase BND prefixes or claim
 # an unmodified generic CFG proves their MPX/OS behavior.
 for i in probe:
  if i['mnemonic']=='call' or re.search(r'\b(?:[re]cx|[re]dx|cl|ch|dl|dh)\b',i['args']):raise RuntimeError('stack probe receiver/flags dependency changed')
  if i['args'].split(',')[0] in ['rax','eax','ax','al','ah'] and i['mnemonic'] not in ['cmp','test']:raise RuntimeError('stack probe size register changed')
 if probe[-1]['mnemonic']!='bnd ret' or sum(i['mnemonic'].startswith('bnd ') for i in probe)!=3:raise RuntimeError('stack probe boundary/prefix changed')
 prefix=ranges[2]['instructions']
 if [(i['pc'],i['args']) for i in prefix if i['mnemonic']=='call']!=[('0x273e55','0x808f10')] or any(i['mnemonic'].startswith('j') for i in prefix):raise RuntimeError('prefix control boundary changed')
 stores=[]
 for pc in [0x273e9e,0x273ea7,0x273eae,0x273eb5]:
  m=ix[pc]['memory'][0]
  if m['role']!='w' or m['base']!='rcx' or m['index'] or m['size']!=8:raise RuntimeError('receiver store classification changed')
  stores.append({'pc':hex(pc),'receiver':'0x22ca408','offset':m['displacement'],'bytes':8,'value':0})
 if [s['offset'] for s in stores]!=[0,8,16,24]:raise RuntimeError('zero span changed')
 partitions=[]
 for oldbit in [0,1]:
  for amin,amax in [(0,0),(1,1),(2,0xffffffff)]:
   ret=amin==amax==oldbit;newbit=oldbit if ret else int(amin!=0)
   partitions.append({'old_bit':oldbit,'raw_ecx_min':amin,'raw_ecx_max':amax,'store_and_tail':not ret,'result_bit':newbit,'bit_value_changes':newbit!=oldbit})
 result={'producer_complete':True,'method':'A STATIC_ONLY native branch/store proof; no game or machine-code execution','driver_sha256':sha(Path(__file__)),'source_pins':[{'path':n,'sha256':sha(src/n)} for n in ['source-01.json','stack-probe-source-01.json']],'annotation_prerequisites':annotations,'instruction_assertions':len(pins),'graphs':graphs,
 'raw_argument_partitions':partitions,'boundary_countermodel':{'old_flags':1,'raw_ecx':2,'new_flags':1,'store_and_tail':True,'interpretation':'Under raw32 ABI, same bit value still writes/tails; not proof that a natural caller supplies2 or that a declared0/1 API accepts it.'},
 'stack_probe':'Verified original81B helper has no RCX/RDX references orRAX destination/calls. BND prefixes retained, no MPX/OS execution claim. Normal return/valid private stack/pages/no interference remain premises.',
 'immediate_receiver_stores':stores,'receiver_zero_interval':['0x22ca408','0x22ca428'],'native_suffix_entry':'0x273ebc','full_initializer_effects_closed':False,
 'established':['Changed rawcomparison path forwards updatedDWORD inEDX but replacesRCX with static022CA408 receiver','Given successful original stackprobe/privateframe/validreceiver, original initializer prefix clears32bytes of thatreceiver before the uncapturedsuffix','A stubbed35C620 or273E30 records call interception only and does not establish these native effects','RawECX outside0/1 can trigger same-bit store/tail; conditional argument0/1 unchanged-mode guarantee remains valid'],
 'unresolved':['Full273E30 semantic meaning/effects/any laternotifications/flags use','Natural receiver lifetime/type/initialization/caller argumentdomain','Full suffix callees/aliasing/OS-stack fault behavior/MPX state','Mode1-to-Esper type coupling and wholeOV42/21 naturaladmission'],
 'limits':'Prefix source effect only, not executed native receiver writes, whole notify refutation or action consequence. No old mode-bit campaigns repeated. A label may include notifications later; immediate original memory mutation must remain explicit.'}
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'producer_complete':True,'native_prefix_zero_bytes':32,'receiver':'0x22ca408','pins':len(pins),'full_suffix_closed':False,'raw_argument_countermodel':'same bit/rawECX2 still tails; not executed'}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--src',type=Path,default=P);a=ap.parse_args();main(a.src,a.output)
