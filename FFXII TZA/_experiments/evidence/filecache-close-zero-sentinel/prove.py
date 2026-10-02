"""Original Close local partitions; IsOpen counterexample from retained predicate."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G,predicate):
 expected='''59bd46|mov|rbx, rcx
59bd49|mov|rcx, qword ptr [rcx + 0x30]
59bd4d|test|rcx, rcx
59bd50|je|0x59bd5f
59bd52|call|0x2150d0
59bd57|mov|qword ptr [rbx + 0x30], 0
59bd5f|mov|rdx, qword ptr [rbx + 0x40]
59bd63|test|rdx, rdx
59bd66|jle|0x59bd78
59bd68|mov|ecx, dword ptr [rbx + 0x48]
59bd6b|call|0x1d6aa0
59bd70|mov|qword ptr [rbx + 0x40], 0xffffffffffffffff
59bd78|mov|al, 1
59bd7f|ret|'''
 for l in expected.splitlines():
  pc,m,a=l.split('|');pc=int(pc,16)
  if pc not in ix or (ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('Close phase changed '+hex(pc))
 for pc,base,off,size,role in [(0x59bd49,'rcx',0x30,8,'r'),(0x59bd57,'rbx',0x30,8,'w'),(0x59bd5f,'rbx',0x40,8,'r'),(0x59bd70,'rbx',0x40,8,'w')]:
  ms=ix[pc]['memory']
  if len(ms)!=1 or(ms[0]['base'],ms[0]['displacement'],ms[0]['size'],ms[0]['role'],ms[0]['index'] or None)!=(base,off,size,role,None):raise RuntimeError('Close backing width/role changed')
 allg=G.graph(ix,0x59bd40,0x59bd80)
 if allg['visited']!=set(ix) or allg['returns']!=[0x59bd7f]:raise RuntimeError('Close CFG incomplete')
 if not G.dominates(allg,0x59bd78,0x59bd7f):raise RuntimeError('AL return not common to all paths')
 import capstone
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 for pc in sorted(ix):
  if 0x59bd49<=pc<0x59bd7e:
   i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
   if {i.reg_name(r) for r in wr}&{'rbx','ebx','bx','bl','bh'}:raise RuntimeError('Close object carrier changed')
 if allg['edges'][0x59bd78]!=[0x59bd7a] or any(ix[pc]['mnemonic'] not in ['add','pop','ret'] for pc in ix if 0x59bd7a<=pc<0x59bd80):raise RuntimeError('postAL return boundary changed')
 rows=[]
 for buffer_nonzero in [False,True]:
  for cache_positive in [False,True]:
   g=G.graph(ix,0x59bd40,0x59bd80,fixed={0x59bd50:not buffer_nonzero,0x59bd66:not cache_positive})
   wantcalls=([(0x59bd52,'0x2150d0')] if buffer_nonzero else [])+([(0x59bd6b,'0x1d6aa0')] if cache_positive else [])
   writes=[{'pc':hex(pc),'offset':m['displacement'],'bytes':m['size']} for pc in sorted(g['visited']) for m in ix[pc]['memory'] if m['role'] in ['w','rw'] and m['base']!='rsp']
   wantwrites=([{'pc':'0x59bd57','offset':0x30,'bytes':8}] if buffer_nonzero else [])+([{'pc':'0x59bd70','offset':0x40,'bytes':8}] if cache_positive else [])
   if g['calls']!=wantcalls or writes!=wantwrites or g['returns']!=[0x59bd7f]:raise RuntimeError('Close branch effects changed')
   rows.append({'buffer30_nonzero':buffer_nonzero,'cache40_signed_positive':cache_positive,'calls':g['calls'],'own_backing_writes':writes,'AL':1})
 # TEST setsOF0; JLE takesZF1 orSF!=OF. Thus the64-bit cache test is signed<=0.
 mask=(1<<64)-1;signmodels=[]
 for u in [0,1,(1<<63)-1,1<<63,mask-1,mask]:
  signed=u if u<(1<<63) else u-(1<<64);taken=(u==0)or(bool(u>>63)!=False)
  if taken!=(signed<=0):raise RuntimeError('TEST/JLE sign proof failed')
  signmodels.append({'QWORD40':u,'signed64':signed,'skips_release_and_reset':taken})
 if predicate['zero_view_witness']['AL']!=1 or predicate['zero_view_witness']['QWORD40']!=0:raise RuntimeError('retained zero sentinel discriminator missing')
 zero=next(r for r in rows if not r['buffer30_nonzero'] and not r['cache40_signed_positive'])
 if zero['calls'] or zero['own_backing_writes']:raise RuntimeError('zero-view Close is not no-helper/no-write')
 return {'Close_partitions':rows,'signed_cache_guard':{'instruction':'TEST RDX,RDX; JLE','condition':'signed64(cache40)<=0 skipsrelease andreset','boundary_models':signmodels,'limits':'Fixed-width source arithmetic, not six native pointer values sampled'},'post_Close_zero':{'pre':{'QWORD28':mask,'QWORD30':0,'QWORD40':0},'Close_AL':1,'Close_calls':[],'Close_own_nonstack_writes':[],'post':{'QWORD28':mask,'QWORD30':0,'QWORD40':0},'then_IsOpen_AL':1,'claim_refuted':'NormalCloseAL1 universally implies IsOpenAL0','limits':'Conditional readableinput/source sequence; no actual caller invocation, naturalallocationNULL or gameplay consequence observed'},'other_limit':'Close body has no own28access; when30=0 and40<=0 it callsnohelpers regardless of28. A non-sentinel28 is another mathematical witness, not an observed Win32handle or leak. Helperarms require normalABI/returns/nativeeffect premises.'}
def main():
 for f,pin in [('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
 s=json.loads((P/'capture-01.status.json').read_text());x=json.loads((P/'source-01.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required Close capture failed')
 if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/'capture.py') or x['driver_sha256']!=sha(P/'capture-index-path.py'):raise RuntimeError('actual Close capture incomplete')
 lineage=json.loads((P/'parent-identities.json').read_text());d=P/'retained-open';mpin='7479a4f8d544249b398a57419aab50ac4296bc14eb717c4517cd478320ad2f45'
 if lineage['manifest_sha256']!=mpin or sha(d/'manifest.json')!=mpin:raise RuntimeError('retained predicate manifest changed')
 mf={m['path']:m for m in json.loads((d/'manifest.json').read_text())['members']}
 for tag,driver in [('capture-01','capture.py'),('prove-01','prove.py')]:
  s=json.loads((d/(tag+'.status.json')).read_text())
  if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(d/driver) or not(d/(tag+'.stdout')).read_bytes() or(d/(tag+'.stderr')).read_bytes():raise RuntimeError('required retained predicate invocation failed')
 v=json.loads((d/'result-01.json').read_text())
 if v.get('producer_complete') is not True or v['driver_sha256']!=sha(d/'prove.py'):raise RuntimeError('required retained predicate result incomplete')
 for r in lineage['files']:
  if sha(d/r['path'])!=r['sha256'] or(r['path']!='manifest.json' and r['sha256']!=mf[r['path']]['sha256']):raise RuntimeError('retained predicate identity changed')
 V=load('roles','validate-title-source-annotations.py');G=load('graph','prove_owner_reload_order.py');names=['source-01.json','retained-open/source-01.json'];sources=[json.loads((P/n).read_text()) for n in names];ann=[V.validate(q) for q in sources]
 raw=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise RuntimeError('original image changed')
 pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0];secs=[struct.unpack_from('<IIII',raw,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
 def read(a,n):
  for vs,rva,size,off in secs:
   if 0x120000+rva<=a and a+n<=0x120000+rva+size:return raw[off+a-0x120000-rva:off+a-0x120000-rva+n]
  raise RuntimeError('unbacked original range')
 locals=[]
 for q,expected in zip(sources,[(0x59bd40,0x59bd80),(0x59d920,0x59d93b)]):
  if q['exe_sha256']!=PIN or q.get('wrapper_complete') is not True or len(q['ranges'])!=1:raise RuntimeError('wrong original source population')
  r=q['ranges'][0];a,b=int(r['start'],16),int(r['end_exclusive'],16)
  if(a,b)!=expected or bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
  locals.append({int(i['pc'],16):i for i in r['instructions']})
 M=load('retained_getter','retained-open/prove.py');predicate=M.getter(locals[1],G)
 if predicate!={k:q for k,q in v['facts'].items() if k!='conditional_composition'}:raise RuntimeError('retained predicate rederivation differs')
 facts=derive(locals[0],G,predicate)
 result={'producer_complete':True,'method':'A STATIC_ONLY Closebranch effects and sentinelpostcondition counterexample','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,'source_pins':[{'path':n,'sha256':sha(P/n)} for n in names],'annotation_prerequisites':ann,'new_original_bytes':64,'retained_predicate':{'lineage':lineage,'getter_driver_sha256':sha(d/'prove.py'),'use':'Purecheckedoriginaloperation predicate reused; not original-code execution or independent acceptance'},'facts':facts,'limits':['Validreadablerecord/privateframe/normalexecution for no-helper path; helperarms additionallynormalABI/returns/nativeeffects/noalias/nointerference.','Fourlogicalsourcepartitions/signedboundarymodels are mathematics, not native/live runs. No currentcaller or naturalallocationfailure/actualClose/IsOpen observed.','No leak/lifetime/allwriter/resourcecardinality/actualWin32handle/readfault/scheduling proof. AL-only returns, not fullRAX. Parentpendingacceptance remainsqualified.'],'cleanup':'Onlyownedoffline files; no game/PC/native/instrument/save/config/reference/peer changes.'}
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise RuntimeError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED CloseAL1 leaveszero cacheview andIsOpenAL1 onnohelper path; STATIC_ONLY')
if __name__=='__main__':main()
