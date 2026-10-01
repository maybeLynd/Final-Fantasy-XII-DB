"""Disposable Python checker controls; no FF12 instruction execution or file writes."""
import contextlib,hashlib,io,json,os,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
ROOT=Path.cwd().resolve();REF=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
P=Path('Database/FFXII TZA/_index/candidates/matrix-alias-consumers/alias_check.py')
PAGE=Path('Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md')
BASE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def child(case):
 import builtins,struct
 raw=REF.read_bytes();assert sha(raw)==BASE
 original=raw
 if case=='wrong-image-identity':
  b=bytearray(raw);b[0x28]^=1;raw=bytes(b)
 else:assert case=='canonical-baseline'
 pe=struct.unpack_from('<I',raw,60)[0];n=struct.unpack_from('<H',raw,pe+6)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
 secs=[struct.unpack_from('<IIII',raw,pe+24+opt+40*j+8) for j in range(n)]
 def span(buf,va,size):
  for vs,rva,rs,ro in secs:
   if 0x120000+rva<=va<0x120000+rva+rs:
    off=va-0x120000-rva+ro;return buf[off:off+size]
  raise AssertionError(hex(va))
 bodies=[]
 for va,size in [(0x217060,235),(0x202b70,31)]:
  a=span(original,va,size);b=span(raw,va,size);assert a==b
  bodies.append(dict(va=hex(va),bytes=size,sha256=sha(b),unchanged=True))
 checker=(W/'retained/alias_check.py').read_bytes();page=(W/'retained/primitives.md').read_bytes()
 accesses=[];real_open=builtins.open
 def supplied(file,mode='r',*args,**kw):
  p=Path(file).resolve()
  if p==REF:
   assert mode=='rb';accesses.append(dict(path=str(p),mode=mode,supplied='disposable image bytes'));return io.BytesIO(raw)
  if p==ROOT/PAGE:
   assert mode=='r' and kw.get('encoding')=='utf-8';accesses.append(dict(path=str(p),mode=mode,supplied='canonical page bytes'));return io.StringIO(page.decode('utf-8'))
  raise AssertionError('Unexpected checker file read: '+str(p))
 stdout=io.StringIO();code=None
 with contextlib.redirect_stdout(stdout):
  builtins.open=supplied
  try:exec(compile(checker,str(ROOT/P),'exec'),dict(__file__=str(ROOT/P),__name__='__main__'))
  except SystemExit as e:code=e.code
  finally:builtins.open=real_open
 assert code is not None and len(accesses)==2
 diffs=[i for i,(a,b) in enumerate(zip(original,raw)) if a!=b]
 print(json.dumps(dict(case=case,method='offline Python checker with labelled supplied file-read intervention; NOT native FF12',input_sha256=sha(raw),baseline_sha256=sha(original),input_bytes=len(raw),differences=diffs,patch=None if not diffs else dict(offset=0x28,before=original[0x28],after=raw[0x28]),bodies=bodies,checker_sha256=sha(checker),page_sha256=sha(page),checker_exit_code=code,stdout=stdout.getvalue(),file_reads=accesses,pid=os.getpid(),interpreter=sys.executable,cleanup='open restored; disposable input only; process exits normally')))
if '--child' in sys.argv:
 child(sys.argv[-1]);sys.exit(0)
assert not (W/'raw.json').exists(),'No duplicate settled capture'
assert sha(REF.read_bytes())==BASE
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();ret=W/'retained';ret.mkdir(exist_ok=False);deps=[]
for p,name in [(P,'alias_check.py'),(PAGE,'primitives.md'),(P.with_name('README.md'),'consumer-README.md')]:
 b=subprocess.check_output(['git','show',commit+':'+p.as_posix()]);working=p.read_bytes()
 if p!=PAGE:assert working.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
 (ret/name).write_bytes(b);deps.append(dict(path=p.as_posix(),retained=name,git_commit=commit,git_blob=subprocess.check_output(['git','rev-parse',commit+':'+p.as_posix()],text=True).strip(),sha256=sha(b),working_sha256=sha(working),view='canonical Git bytes; peer working page overlay not consumed'))
driver_sha=sha(Path(__file__).read_bytes());exe_sha=sha(Path(sys.executable).read_bytes())
cases=[]
for case in ['canonical-baseline','wrong-image-identity']:
 r=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',case],capture_output=True,text=True,timeout=30)
 assert r.returncode==0 and not r.stderr,(case,r.returncode,r.stderr)
 c=json.loads(r.stdout);c.update(child_returncode=r.returncode,stderr=r.stderr);cases.append(c)
assert sha(REF.read_bytes())==BASE and sha(Path(__file__).read_bytes())==driver_sha
out=dict(method='A offline checker falsification; no original-code/native/live execution',reference=dict(path=str(REF),sha256=BASE),dependencies=deps,driver_sha256_before=driver_sha,interpreter=sys.executable,interpreter_sha256_before=exe_sha,cases=cases,cleanup=dict(reference_sha256_after=BASE,driver_unchanged=True,children_exited=True,pc_control='OFF',game_save_config_reference_writes=False,peer_source_writes=False))
(W/'raw.json').write_text(json.dumps(out,indent=2)+'\n');print('Captured two disposable checker controls; no peer/reference writes.',flush=True)
