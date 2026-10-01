import ctypes,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT/'Database/Tools/analysis-kit/gfz-scripts'))
import ffxii_runtime as rt
pid=json.loads((HERE/'process.json').read_text())['pid'];k=ctypes.windll.kernel32
r={'at':time.time(),'hypothesis':'Missing HANDLE prototypes in existing live_modules may corrupt x64 snapshot API arguments.','pid':pid}
r['untyped_modules']=rt.live_modules(pid,attempts=1,pause=0)
r['untyped_error']=k.GetLastError()
k.CreateToolhelp32Snapshot.argtypes=[ctypes.c_ulong,ctypes.c_ulong];k.CreateToolhelp32Snapshot.restype=ctypes.c_void_p
k.Module32First.argtypes=[ctypes.c_void_p,ctypes.c_void_p];k.Module32First.restype=ctypes.c_int
k.Module32Next.argtypes=[ctypes.c_void_p,ctypes.c_void_p];k.Module32Next.restype=ctypes.c_int
k.CloseHandle.argtypes=[ctypes.c_void_p];k.CloseHandle.restype=ctypes.c_int
r['typed_modules']=rt.live_modules(pid,attempts=1,pause=0)
r['typed_error']=k.GetLastError()
r['self_modules']=rt.live_modules(k.GetCurrentProcessId(),attempts=1,pause=0)
r['positive']=bool(r['typed_modules']) and any(x.endswith('ffxii_tza.exe') for x in r['typed_modules']) and any(x.endswith('ntdll.dll') for x in r['typed_modules']) and bool(r['self_modules'])
out=HERE/('module-control'+('-outside-sandbox' if '--outside-sandbox' in sys.argv else '')+'.json')
assert not out.exists(),'preserve earlier module control'
out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if not k.endswith('modules')},indent=2));print('module counts',*[len(r[k] or []) for k in ['untyped_modules','typed_modules','self_modules']])
assert r['positive'],'module control failed; no pool capture'
