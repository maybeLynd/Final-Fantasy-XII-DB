"""Bounded B execution of two shipping FF12 memory-reader functions.

Reuse spawn_manager_probe.py's Unicorn ABI/code/memory tracing design.
No stubs, live process, filesystem calls, saves or PC input. All state is injected.
"""
import hashlib,json,struct,sys
from pathlib import Path
sys.path.insert(0,'Database/Tools/work/ASTRA/python-libs')
import unicorn
from unicorn.x86_const import *
W=Path('Database/Tools/work/ASTRA');ns={}
s=(W/'spawn_storage_completion_primary.py').read_text()
exec(compile(s.split('for a in (')[0],'<existing shipping PE reader>','exec'),ns)
cat={}
for n,a in [('adapters',0x862590),('file',0x866A00)]:
 j=json.loads((W/('spawn-storage-completion-'+n+'.json')).read_text());assert j['exe_sha256']==ns['sha']
 cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
code={};instructions=set()
for a,b in cat.items():
 o=ns['off'](a-ns['ib']);d=ns['raw'][o:o+b['bytes']]
 assert hashlib.sha256(d).hexdigest()==b['sha256']
 assert d==b''.join(bytes.fromhex(i['bytes']) for i in b['instructions'])
 code[a]=d;instructions.update(int(i['address'],16) for i in b['instructions'])
ENTRY=0x862590;SP=0x60001808;STOP=0x70000000
HANDLE,SOURCE,DEST=0x30001000,0x30002000,0x30003000
VECTOR,RESULT,HANDLE_GLOBAL=0x1F44D40,0x2EAF8E0,0x2EAF8E8
NV=(UC_X86_REG_RBX,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15)
def d(v):return struct.pack('<I',v&0xffffffff)
def q(v):return struct.pack('<Q',v&0xffffffffffffffff)
def run(name,available,request,cursor,fd,expected_copy,expected_result):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
 payload=bytes(range(0x31,0x51));sentinel=b'\xC7'*48
 injected=[(HANDLE,d(cursor)+d(1)+b'\xA5'*24),(SOURCE,payload),(DEST,sentinel),
  (VECTOR,q(SOURCE)+q(SOURCE+available)+q(SOURCE+len(payload))),
  (RESULT,d(0x12345678)),(HANDLE_GLOBAL,q(HANDLE))]
 pages=set(range(0x60000000,0x60003000,4096))
 for a,b in [*code.items(),*injected]:pages.update(range(a&~4095,(a+len(b)+4095)&~4095,4096))
 for a in pages:u.mem_map(a,4096)
 for a,b in [*code.items(),*injected]:u.mem_write(a,b)
 saved={r:0xA100000000000000+i for i,r in enumerate(NV)}
 saved.update({UC_X86_REG_XMM6+i:0x123456789ABCDEF0123456789ABCDEF^i for i in range(10)})
 for r,v in saved.items():u.reg_write(r,v)
 for r,v in [(UC_X86_REG_RSP,SP),(UC_X86_REG_EFLAGS,2),(UC_X86_REG_MXCSR,0x1F80),
             (UC_X86_REG_RCX,fd),(UC_X86_REG_RDX,DEST),(UC_X86_REG_R8,request)]:u.reg_write(r,v)
 u.mem_write(SP,q(STOP))
 regions=[(HANDLE,32),(SOURCE,len(payload)),(DEST,len(sentinel)),(VECTOR,24),(RESULT,4),(HANDLE_GLOBAL,8)]
 before={hex(a):bytes(u.mem_read(a,n)).hex() for a,n in regions}
 events=[];visited=[];invalid=[];boundaries=[]
 def on_code(uc,a,n,_):
  visited.append(hex(a));assert a in instructions,hex(a)
  if a in (ENTRY,0x866A00):boundaries.append(dict(entry=hex(a),event_index=len(events),rcx=hex(uc.reg_read(UC_X86_REG_RCX)),rdx=hex(uc.reg_read(UC_X86_REG_RDX)),r8=hex(uc.reg_read(UC_X86_REG_R8)),rsp=hex(uc.reg_read(UC_X86_REG_RSP))))
 def memory(uc,access,a,n,v,_):
  if 0x60000000<=a and a+n<=0x60003000:return
  events.append([hex(uc.reg_read(UC_X86_REG_RIP)),'W' if access==unicorn.UC_MEM_WRITE else 'R',hex(a),n,
   int(v&((1<<(n*8))-1)).to_bytes(n,'little').hex() if access==unicorn.UC_MEM_WRITE else bytes(uc.mem_read(a,n)).hex()])
 def bad(uc,access,a,n,v,_):invalid.append([hex(uc.reg_read(UC_X86_REG_RIP)),access,hex(a),n]);return False
 u.hook_add(unicorn.UC_HOOK_CODE,on_code)
 u.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)
 u.hook_add(unicorn.UC_HOOK_MEM_INVALID,bad)
 error=None
 try:u.emu_start(ENTRY,STOP,count=5000)
 except (unicorn.UcError,AssertionError) as e:error=str(e)
 after={hex(a):bytes(u.mem_read(a,n)).hex() for a,n in regions}
 expected_dest=expected_copy+sentinel[len(expected_copy):]
 return dict(name=name,injected=dict(available=available,request=request,cursor=cursor,fd=fd),before=before,after=after,
  expected=dict(destination=expected_dest.hex(),cursor=cursor+len(expected_copy),result=hex(expected_result&0xffffffff)),
  observed=dict(return_eax=hex(u.reg_read(UC_X86_REG_EAX)),cursor=struct.unpack('<I',u.mem_read(HANDLE,4))[0],result=hex(struct.unpack('<I',u.mem_read(RESULT,4))[0])),
  memory=events,visited=visited,boundaries=boundaries,invalid=invalid,error=error,
  returned=error is None and u.reg_read(UC_X86_REG_RIP)==STOP,stack_ok=u.reg_read(UC_X86_REG_RSP)==SP+8,
  nonvolatile_ok=all(u.reg_read(r)==v for r,v in saved.items()),code_unchanged=all(bytes(u.mem_read(a,len(b)))==b for a,b in code.items()),
  checks=dict(destination=after[hex(DEST)]==expected_dest.hex(),cursor=struct.unpack('<I',u.mem_read(HANDLE,4))[0]==cursor+len(expected_copy),
   return_value=u.reg_read(UC_X86_REG_EAX)==expected_result&0xffffffff,result=struct.unpack('<I',u.mem_read(RESULT,4))[0]==expected_result&0xffffffff,
   immutable=all(after[hex(a)]==before[hex(a)] for a in (SOURCE,VECTOR,HANDLE_GLOBAL)),
   handle_tail=bytes(u.mem_read(HANDLE+4,28))==bytes.fromhex(before[hex(HANDLE)])[4:],
   native_callee_reached=('0x866a00' in visited)==(fd==0)))
cases=[]
def case(*args):
 r=run(*args);cases.append(r)
 if not(r['returned'] and r['stack_ok'] and r['nonvolatile_ok'] and r['code_unchanged'] and not r['invalid'] and all(r['checks'].values())):
  (W/'spawn-storage-short-read-incomplete.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8',newline='\n')
  raise AssertionError((r['name'],r['error'],r['checks']))
 print(r['name'],r['observed'], 'writes',sum(e[1]=='W' for e in r['memory']))
case('full-read-positive',8,8,0,0,b'12345678',8)
case('short-prefix-positive',3,8,0,0,b'123',0)
if '--feasibility' not in sys.argv:
 case('empty-buffer-control',0,8,0,0,b'',0)
 case('offset-full-control',12,4,2,0,b'3456',4)
 case('past-end-control',4,8,8,0,b'',0)
 case('nonzero-fd-refusal',8,8,0,1,b'',-4)
 case('zero-request-boundary',8,0,0,0,b'',0)
out=dict(exe_sha256=ns['sha'],entry=hex(ENTRY),bodies=[dict(address=hex(a),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()) for a,b in code.items()],
 probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),unicorn_version=unicorn.__version__,
 method='B isolated original-code execution',live_game=False,stubs={},
 limits=['Injected initialized vector, opaque handle/cursor, destination sentinel and Windows x64 ABI; no original initialization, filesystem or scheduling executed.',
 'Only862590 and866A00 shipping instructions execute. Native open, container transformation, close and outer completion are not executed.',
 'This proves partial-copy effects and result encoding for these entries. A failure becoming parent success is conditional source analysis, not an observed live malformed-save load.',
 'Non-stack reads/writes, native call entries, full code identity, return/ABI and unchanged regions retained. No actual save or game process opened.'],cases=cases)
assert cases
p=W/('spawn-storage-short-read-feasibility.json' if '--feasibility' in sys.argv else 'spawn-storage-short-read-execution.json')
p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Saved',p,len(cases))
