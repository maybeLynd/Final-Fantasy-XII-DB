"""Original Read source partitions; IsOpen counterexample from retained predicate."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;ROOT=next(q for q in P.parents if(q/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def derive(ix,G,predicate):
 expected="""59d4b4|mov|rax, qword ptr [rcx + 0x30]
59d4b8|test|rax, rax
59d4bb|je|0x59d4ca
59d4bd|mov|rcx, rax
59d4c0|call|0x2150e0
59d4ca|mov|dword ptr [rsp + 0x40], eax
59d4ce|test|r8d, r8d
59d4d1|je|0x59d507
59d4d3|mov|r10, qword ptr [rcx + 0x28]
59d4d7|cmp|r10, -1
59d4db|je|0x59d4f9
59d4ea|call|qword ptr [rip + 0x324c50]
59d4f0|mov|eax, dword ptr [rsp + 0x40]
59d4f9|mov|rcx, qword ptr [rcx + 0x40]
59d4fd|test|rcx, rcx
59d500|jle|0x59d507
59d50b|ret|"""
 for l in expected.splitlines():
  pc,m,a=l.split('|');pc=int(pc,16)
  if pc not in ix or(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,a):raise RuntimeError('Read source operation changed '+hex(pc))
 for pc,base,off,size,role in [(0x59d4b4,'rcx',0x30,8,'r'),(0x59d4d3,'rcx',0x28,8,'r'),(0x59d4f9,'rcx',0x40,8,'r'),(0x59d4ca,'rsp',0x40,4,'w'),(0x59d4f0,'rsp',0x40,4,'r')]:
  ms=ix[pc]['memory']
  if len(ms)!=1 or(ms[0]['base'],ms[0]['displacement'],ms[0]['size'],ms[0]['role'],ms[0]['index'] or None)!=(base,off,size,role,None):raise RuntimeError('Read field/count width or role changed')
 if ix[0x59d4ea]['memory'][0]['rip_target']!='0x8c2140':raise RuntimeError('read IAT slot changed')
 whole=G.graph(ix,0x59d4b0,0x59d50c)
 if whole['visited']!=set(ix) or whole['returns']!=[0x59d4c9,0x59d4f8,0x59d50b]:raise RuntimeError('Read original CFG incomplete')
 if any(m['role'] in ['w','rw'] and m['base']!='rsp' for i in ix.values() for m in i['memory']):raise RuntimeError('Read new ownobject write requires analysis')
 import capstone
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 rows=[]
 for name,fixed,calls,ret,fullzero in [
  ('buffer-first',{0x59d4bb:False},[(0x59d4c0,'0x2150e0')],0x59d4c9,False),
  ('no-buffer-zero-bytecount',{0x59d4bb:True,0x59d4d1:True},[],0x59d50b,True),
  ('Win32-read-count',{0x59d4bb:True,0x59d4d1:False,0x59d4db:False},[(0x59d4ea,'qword ptr [rip + 0x324c50]')],0x59d4f8,False),
  ('cache-positive-read',{0x59d4bb:True,0x59d4d1:False,0x59d4db:True,0x59d500:False},[(0x59d502,'0x1d6ca0')],0x59d50b,False),
  ('cache-nonpositive-no-read',{0x59d4bb:True,0x59d4d1:False,0x59d4db:True,0x59d500:True},[],0x59d50b,True)]:
  g=G.graph(ix,0x59d4b0,0x59d50c,fixed=fixed)
  if g['calls']!=calls or g['returns']!=[ret]:raise RuntimeError('Read partition calls/returns changed '+name)
  if fullzero:
   for pc in sorted(g['visited']):
    if pc<=0x59d4b4:continue
    i=next(cs.disasm(bytes.fromhex(ix[pc]['bytes']),pc));_,wr=i.regs_access()
    if {i.reg_name(r) for r in wr}&{'rax','eax','ax','al','ah'}:raise RuntimeError('Readzero value carrier changed')
   if not G.dominates(g,0x59d4b4,ret) or g['calls']:raise RuntimeError('Readzero precondition changed')
  rows.append({'name':name,'fixed_source_branches':{hex(k):v for k,v in fixed.items()},'calls':g['calls'],'return':hex(ret),'fullRAX_zero_under_buffer30_zero':fullzero,'source_sites':[hex(pc) for pc in sorted(g['visited'])]})
 # TEST RCX setsOF0; JLE skipscachecall for every signednonpositive QWORD40.
 if whole['edges'][0x59d4ea]!=[0x59d4f0] or whole['edges'][0x59d4f0]!=[0x59d4f4]:raise RuntimeError('API-return count overwrite changed')
 if predicate['zero_view_witness']['AL']!=1 or predicate['zero_view_witness']['QWORD40']!=0:raise RuntimeError('retained open counterexample lost')
 return {'source_partitions':rows,'zero_view_read_witness':{'record28':'FFFFFFFFFFFFFFFF','record30':0,'record40':0,'IsOpen_AL':1,'Read_fullRAX':0,'Read_calls':[],'requested_bytes':'zero or nonzeroR8D; both paths proved','limits':'Conditional source sequence withvalidreadablerecord/privateframe/normalexecution. No naturally reached failure/actualRead/I/O/readfault/leak/scheduling observation.'},'Read_return_width':'No-call arms preservefullRAX0 fromQWORDbuffer30 load. Otherreturns are nativehelper/API-count dependent; notALbool.', 'Win32_arm':'After normalIATcall, DWORDcallerstack40 is loadedintoEAX, unconditionallyreplacingAPIreturn; wrapper returnscount, notAPI BOOL. No actualDLLbinding/APIerror-bytecount semantics inferred.', 'native_limits':'2150E0 and1D6CA0 nativeeffects/lifetime/actualread outcomes remainopaque. Win32 arm initializedstackDWORD40 fromEAX0 underbuffer30zero; API/count effects are external.', 'consumer_qualification':'IsOpentrue doesnotcertifyreader entry orbytes; sourcefallback/zero-bytecount canreturn0withnoIO. Fivepartitions are sourceanalysis, not executedcalls orgamecases.'}

def import_declaration(raw,read,pe):
 def u32(a):return struct.unpack('<I',read(a,4))[0]
 def u64(a):return struct.unpack('<Q',read(a,8))[0]
 def cstring(a):
  out=bytearray()
  for k in range(512):
   c=read(a+k,1)[0]
   if c==0:return out.decode('ascii')
   out.append(c)
  raise RuntimeError('unbounded import name')
 optional=pe+24
 if struct.unpack_from('<H',raw,optional)[0]!=0x20b or struct.unpack_from('<Q',raw,optional+24)[0]!=0x120000:raise RuntimeError('PE64 import basis changed')
 imp,size=struct.unpack_from('<II',raw,optional+112+8);found=[]
 for pos in range(0,size,20):
  d=struct.unpack('<IIIII',read(0x120000+imp+pos,20))
  if d==(0,0,0,0,0):break
  lookup,stamp,forwarder,name_rva,iat=d;lookup=lookup or iat
  for k in range(4096):
   entry=u64(0x120000+lookup+8*k)
   if not entry:break
   if 0x120000+iat+8*k==0x8c2140:
    if entry>>63:raise RuntimeError('namedread import becameordinal')
    found.append({'DLL':cstring(0x120000+name_rva),'name':cstring(0x120000+entry+2),'IAT':'0x8c2140','hint_name':hex(0x120000+entry),'lookup_file_QWORD':entry,'limits':'ShippingPEdeclaration only, not liveboundDLL/API effects.'})
  else:raise RuntimeError('unterminated import lookup')
 if len(found)!=1:raise RuntimeError('shipping read import notunique')
 return found[0]
def main():
 for f,pin in [('validate-title-source-annotations.py','7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13'),('prove_owner_reload_order.py','43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864')]:
  if sha(P/f)!=pin:raise RuntimeError('reviewed dependency changed')
 s=json.loads((P/'capture-01.status.json').read_text());x=json.loads((P/'source-01.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise RuntimeError('required Read capture failed')
 if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/'capture.py') or x['driver_sha256']!=sha(P/'capture-index-path.py'):raise RuntimeError('actual Read capture incomplete')
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
 for q,expected in zip(sources,[(0x59d4b0,0x59d50c),(0x59d920,0x59d93b)]):
  if q['exe_sha256']!=PIN or q.get('wrapper_complete') is not True or len(q['ranges'])!=1:raise RuntimeError('wrong original source population')
  r=q['ranges'][0];a,b=int(r['start'],16),int(r['end_exclusive'],16)
  if(a,b)!=expected or bytes.fromhex(''.join(i['bytes'] for i in r['instructions']))!=read(a,b-a):raise RuntimeError('original byte mismatch')
  locals.append({int(i['pc'],16):i for i in r['instructions']})
 M=load('retained_getter','retained-open/prove.py');predicate=M.getter(locals[1],G)
 if predicate!={k:q for k,q in v['facts'].items() if k!='conditional_composition'}:raise RuntimeError('retained predicate rederivation differs')
 facts=derive(locals[0],G,predicate)
 declaration=import_declaration(raw,read,pe)
 if declaration['name']!='ReadFile':raise RuntimeError('shipping read import identity changed')
 facts['shipping_read_import']=declaration
 result={'producer_complete':True,'method':'A STATIC_ONLY Read source/bytecount branches and zero-view counterexample','driver_sha256':sha(Path(__file__)),'exe_sha256':PIN,'source_pins':[{'path':n,'sha256':sha(P/n)} for n in names],'annotation_prerequisites':ann,'new_original_bytes':92,'retained_predicate':{'lineage':lineage,'getter_driver_sha256':sha(d/'prove.py'),'use':'Purecheckedoriginaloperation predicate reused; not original-code execution or independent acceptance'},'facts':facts,'limits':['Validreadablerecord/privateframe/normalexecution for no-helper path; helperarms additionallynormalABI/returns/nativeeffects/noalias/nointerference.','Five logical Read source partitions are static analysis, not native/live runs. No current caller, natural allocation failure or actual Read/IsOpen sequence observed.','No leak/lifetime/allwriter/resourcecardinality/actualWin32handle/readfault/scheduling proof. FullRAX zero proved only on no-call arms; other return values depend on opaque helpers/API count. Read is not the AL-only IsOpen predicate. Parent independent acceptance remains pending.'],'cleanup':'Onlyownedoffline files; no game/PC/native/instrument/save/config/reference/peer changes.'}
 out=P/(sys.argv[1] if len(sys.argv)>1 else 'result-01.json')
 if out.exists():raise RuntimeError('immutable result exists')
 out.write_bytes((json.dumps(result,indent=2)+'\n').encode());print('PROVED IsOpenacceptedzero view Readfullzero/noIO source path; STATIC_ONLY')
if __name__=='__main__':main()
