"""Scoped S19 read-only pool observer, reusing EXP081's validated query/read path.
No debugger, memory writes, native game calls, suspended threads or UI control.
"""
import ctypes, hashlib, json, struct, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
KIT=ROOT/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(KIT))
import runtime_probe as rp
import ffxii_runtime as rt
import team
label=sys.argv[1];assert label in ('title','field')
out=HERE/(label+('-access-qualified' if '--access-qualified' in sys.argv else '')+'-raw.json');assert not out.exists(),'preserve raw attempt'
owner=json.loads((HERE/'process.json').read_text())
r={'status':'INVALID','label':label,'start_unix':time.time(),'pid':owner['pid'],
 'method':'C read-only original process; no debugger or interventions','samples':[],
 'tool_hashes':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [Path(__file__),KIT/'runtime_probe.py',KIT/'ffxii_runtime.py']}}
h=None
def lifetime(handle):
 a,b,c,d=(ctypes.c_ulonglong() for _ in range(4))
 assert rp.k32.GetProcessTimes(handle,ctypes.byref(a),ctypes.byref(b),ctypes.byref(c),ctypes.byref(d))
 return a.value
try:
 b=json.loads(team.BOARD.read_text());team.validate(b)
 assert any(t['id']=='ASTRA-BODYPOOL-LIVE-FIRST-STATE' and t['agent']=='ASTRA' and t['status']=='ACTIVE'
            and any(x['key']=='@runtime' for x in t.get('claimed_resources',t['resources'])) for t in b['tasks'])
 rp.k32.OpenProcess.restype=ctypes.c_void_p
 rp.k32.CloseHandle.argtypes=[ctypes.c_void_p]
 rp.k32.ReadProcessMemory.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
 rp.psapi.EnumProcessModules.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong,ctypes.POINTER(ctypes.c_ulong)]
 rp.k32.GetProcessTimes.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
 assert rt.list_processes()==[{'pid':owner['pid'],'path':owner['path']}],'designated process identity changed'
 raw=Path(owner['path']).read_bytes();r['exe_sha256']=hashlib.sha256(raw).hexdigest();assert r['exe_sha256']==rt.AUTHORITY_SHA256
 h=rp.k32.OpenProcess(rp.PROCESS_QUERY_INFORMATION|rp.PROCESS_VM_READ,False,owner['pid']);assert h
 r['creation_filetime']=lifetime(h);assert r['creation_filetime']==owner['creation_filetime']
 r['image_base']=rp.module_base(h);assert r['image_base']==0x120000
 rd=rp.Probe(h)
 r['positive']=rd.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES));assert r['positive']==rp.CONTROL_BYTES;r['positive']=r['positive'].hex()
 r['null_rejected']=rd.read(0,16) is None;assert r['null_rejected']
 r['debugger_present']=ctypes.c_int();assert rp.k32.CheckRemoteDebuggerPresent(ctypes.c_void_p(h),ctypes.byref(r['debugger_present']))
 r['debugger_present']=bool(r['debugger_present'].value);assert not r['debugger_present']
 verdict,hits,mods=rt.classify(owner['pid']);r.update(module_verdict=verdict,watched_modules=hits,modules_before=mods);assert verdict=='clean' and mods
 pe=struct.unpack_from('<I',raw,0x3c)[0];table=pe+24+struct.unpack_from('<H',raw,pe+20)[0]
 text=[]
 for k in range(struct.unpack_from('<H',raw,pe+6)[0]):
  o=table+k*40
  if raw[o:o+8].rstrip(b'\0')==b'.text':
   vs,va,rs,ro=struct.unpack_from('<IIII',raw,o+8);text.append((0x120000+va,raw[ro:ro+min(vs,rs)]))
 assert len(text)==1
 r['text_identity']=[]
 def check_text(phase):
  a,expected=text[0];actual=rd.read(a,len(expected));assert actual==expected
  r['text_identity'].append({'phase':phase,'address':a,'bytes':len(expected),'sha256':hashlib.sha256(actual).hexdigest(),'matches':True})
 check_text('before')
 for index in range(2):
  s={'index':index,'start_unix':time.time(),'reads':[]};r['samples'].append(s)
  def read(name,a,n):
   assert 0<n<=0x10000
   b=rd.read(a,n);assert b is not None and len(b)==n
   s['reads'].append({'name':name,'address':a,'size':n,'hex':b.hex(),'sha256':hashlib.sha256(b).hexdigest(),'at':time.time()});return b
  read('tick_before',0x22c252c,8)
  read('pool_control_before',0x2b57cc0,16)
  read('pool_before',0x2b4e4c0,128*0x130)
  read('pool_after',0x2b4e4c0,128*0x130)
  read('pool_control_after',0x2b57cc0,16)
  read('tick_after',0x22c252c,8)
  s['end_unix']=time.time()
 check_text('after')
 verdict,hits,mods=rt.classify(owner['pid']);r.update(module_verdict_after=verdict,watched_modules_after=hits,modules_after=mods);assert verdict=='clean' and mods==r['modules_before']
 assert lifetime(h)==r['creation_filetime'] and rd.read(rp.CONTROL_ADDR,len(rp.CONTROL_BYTES))==rp.CONTROL_BYTES
 r['status']='RAW_READS_PENDING_STATE_HEALTH_AND_REDUCTION'
finally:
 if isinstance(r.get('positive'),bytes):r['positive']=r['positive'].hex()
 if isinstance(r.get('debugger_present'),ctypes.c_int):r['debugger_present']=r['debugger_present'].value
 if h:r['read_handle_closed']=bool(rp.k32.CloseHandle(h))
 r['end_unix']=time.time();out.write_bytes((json.dumps(r,indent=2)+'\n').encode())
 print(r['status'],str(out))
