"""The first HTTP timeout probes are NOT termination proof; verify owned PIDs/ports."""
import ctypes,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
r=json.loads((W/'run-01/raw.json').read_text())
n=subprocess.run(['netstat','-ano','-p','tcp'],capture_output=True,text=True)
assert n.returncode==0,(n.returncode,n.stderr)
k=ctypes.WinDLL('kernel32',use_last_error=True)
k.OpenProcess.argtypes=[ctypes.c_uint32,ctypes.c_int,ctypes.c_uint32];k.OpenProcess.restype=ctypes.c_void_p
k.CloseHandle.argtypes=[ctypes.c_void_p]
out=[]
for c in r['cleanup']:
    port=c['base'].rsplit(':',1)[1]
    rows=[x for x in n.stdout.splitlines() if re.search(r'127\.0\.0\.1:'+port+r'\s',x)]
    ctypes.set_last_error(0);h=k.OpenProcess(0x1000,0,c['pid']);err=ctypes.get_last_error()
    if h:k.CloseHandle(h)
    state='ABSENT' if not h and err==87 else ('PRESENT' if h else 'UNKNOWN')
    out.append(dict(pid=c['pid'],base=c['base'],parent_wait_returncode=c['returncode'],process_state=state,open_error=err,
                    rows=rows,listener_present=any('LISTENING' in x for x in rows)))
receipt=dict(netstat_exit=n.returncode,correction='Earlier URL timeout/nonresponse does not establish closed port/process. Original cleanup-verification.json preserved; this additive native query is the acceptance control.',servers=out)
receipt['verified']=all(x['process_state']=='ABSENT' and not x['listener_present'] for x in out)
(W/'cleanup-native-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('CLEANUP_NATIVE',receipt['verified'],len(out));sys.exit(0 if receipt['verified'] else 1)
