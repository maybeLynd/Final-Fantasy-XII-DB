import ctypes,hashlib,importlib,json,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-logical-coordinate-domain');sha=lambda b:hashlib.sha256(b).hexdigest();assert not P.exists()
before=sha((W/'preparation.json').read_bytes());r=subprocess.run([sys.executable,str(W/'probe.py')],capture_output=True,text=True,timeout=30)
assert r.returncode==0 and 'PASS64' in r.stdout and 'PREP64' not in r.stdout and sha((W/'preparation.json').read_bytes())==before
(W/'default-invocation.stdout').write_text(r.stdout);(W/'default-invocation.stderr').write_text(r.stderr);(W/'default-invocation-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,probe_sha256=sha((W/'probe.py').read_bytes()),check_sha256=sha((W/'check.py').read_bytes()),preparation_before_sha256=before,preparation_after_sha256=sha((W/'preparation.json').read_bytes()),path='Actual probe default with retained old preparation consumes corrected decoded-source checker; original preparation unchanged, no native/compiler/game execution'),indent=2)+'\n')
# Exercise fresh generation branch in an owned disposable subdirectory; retained
# original data is reread, no game capture or peer/current preparation overwritten.
temp=W/'fresh-default-control'
if not temp.exists():
 temp.mkdir();shutil.copyfile(W/'probe.py',temp/'probe.py');r=subprocess.run([sys.executable,str(temp/'probe.py')],capture_output=True,text=True,timeout=30);assert r.returncode==0 and 'PREP64' in r.stdout
else:
 receipt=json.loads((W/'fresh-default-receipt.json').read_text());assert receipt['returncode']==0 and receipt['probe_sha256']==sha((temp/'probe.py').read_bytes())==sha((W/'probe.py').read_bytes()) and receipt['generated_preparation_sha256']==sha((temp/'preparation.json').read_bytes());r=subprocess.CompletedProcess([],0,receipt['stdout'],'') # Preserve validated generation; do not overwrite existing original receipt/output.
new=json.loads((temp/'preparation.json').read_text());assert new['counter_mode']=='DECODED_ASCII_CONTINUATION';mp=next(x for x in new['source_blocks'] if (x['module'],x['block'])==('mapctrl',0));assert mp['logical']==mp['physical']==2768 and mp['decoded_ascii_continuations']==0 and mp['non_ascii_terminal5c']==[976,1186]
(W/'fresh-default-receipt.json').write_text(json.dumps(dict(returncode=r.returncode,probe_sha256=sha((temp/'probe.py').read_bytes()),generated_preparation_sha256=sha((temp/'preparation.json').read_bytes()),mode=new['counter_mode'],map_source=mp,stdout=r.stdout,limits='Owned disposable output, original retained source reread only; not original compiler behavior'),indent=2)+'\n')
receipts=[]
for arg,expected in [('--fault-raw-byte-fold','CP932 trailing5C character'),('--fault-physical-guard','LogicalL+1 within physicalL'),('--fault-old-preparation-mode','Decoded logical domain corrects'),('--fault-ignore-multiphysical-group','Actual source multi-physical group')]:
 c=subprocess.run([sys.executable,str(W/'check.py'),arg],capture_output=True,text=True,timeout=30);name=arg[2:];(W/(name+'.stdout')).write_text(c.stdout);(W/(name+'.stderr')).write_text(c.stderr);assert c.returncode==1 and expected in c.stderr;receipts.append(dict(argument=arg,returncode=c.returncode,expected=expected,stdout_sha256=sha(c.stdout.encode()),stderr_sha256=sha(c.stderr.encode())))
(W/'regression-controls.json').write_text(json.dumps(receipts,indent=2)+'\n');subprocess.run([sys.executable,str(W/'check.py')],check=True)
codec=importlib.import_module('_codecs_jp')
if getattr(codec,'__file__',None):provider=Path(codec.__file__);kind='Extension module file'
else:
 assert codec.__spec__.origin=='built-in';k=ctypes.WinDLL('kernel32',use_last_error=True);f=k.GetModuleFileNameW;f.argtypes=[ctypes.c_void_p,ctypes.c_wchar_p,ctypes.c_uint32];f.restype=ctypes.c_uint32;buf=ctypes.create_unicode_buffer(32768);n=f(ctypes.pythonapi._handle,buf,len(buf));assert 0<n<len(buf);provider=Path(buf.value);kind='Built-in codec in actual loaded Python core module; own host loader path read only'
assert provider.is_file();tool=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),codec_name=codec.__name__,codec_origin=codec.__spec__.origin,codec_provider=str(provider),codec_provider_kind=kind,codec_provider_sha256=sha(provider.read_bytes()),limits='Provider file identities, not all RAM/modules or original FF12 execution');(W/'tool-identity.json').write_text(json.dumps(tool,indent=2)+'\n')
P.mkdir();(P/'.gitattributes').write_bytes(b'* -text\n')
names=['PLAN.md','README.md','probe.py','check.py','repair.py','repair-encoding.py','fix-probe.py','upstream-control.py','upstream-control.json','upstream-default.stdout','upstream-default.stderr','preparation.json','result.json','failure.json','freeze.py','default-invocation.stdout','default-invocation.stderr','default-invocation-receipt.json','fresh-default-receipt.json','regression-controls.json','tool-identity.json']
names.extend([arg[2:]+ext for arg in ['--fault-raw-byte-fold','--fault-physical-guard','--fault-old-preparation-mode','--fault-ignore-multiphysical-group'] for ext in ['.stdout','.stderr']])
for n in names:shutil.copyfile(W/n,P/n)
shutil.copytree(W/'retained',P/'retained');(P/'fresh-default-generated-preparation.json').write_bytes((temp/'preparation.json').read_bytes());rr=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  a=subprocess.check_output(['git','hash-object','--',p.as_posix()],text=True).strip();b=subprocess.check_output(['git','hash-object','--no-filters','--',p.as_posix()],text=True).strip();assert a==b,p;rr.append(dict(path=p.relative_to(P).as_posix(),git_blob=a))
(P/'filtered-byte-check.json').write_text(json.dumps(dict(existing_policy='* -text',receipts=rr),indent=2)+'\n');members=[dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(P.rglob('*')) if p.is_file()]
(P/'manifest.json').write_text(json.dumps(dict(members=members,limits='Actual two CP932 source negatives expose raw5C producer misuse; decoded conditional original domain no additional six-known-missing records with positive/detection controls. No original compiler/native/live/global rule; peer consumer/independent review pending.'),indent=2)+'\n');subprocess.run([sys.executable,str(P/'probe.py')],check=True);print('FROZEN64',len(members),flush=True)
