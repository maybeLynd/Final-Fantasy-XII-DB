"""Bind current checkout files to their actual Git blobs without editing them."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
paths=[Path('Database/Tools/dashboard/server.py'),
       Path('Database/Tools/dashboard/build_views.py'),
       Path('Database/Tools/dashboard/requirements.py'),
       Path('Database/Tools/analysis-kit/gfz-scripts/generation.py')]
def git(*args):
    p=subprocess.run(['git',*args],capture_output=True,text=True)
    assert p.returncode==0,(args,p.returncode,p.stderr)
    return {'stdout':p.stdout.strip(),'stderr':p.stderr,'returncode':p.returncode}
out=[]
for path in paths:
    name=path.as_posix();data=path.read_bytes()
    blob=git('hash-object','--',name)
    head=git('rev-parse','HEAD:'+name)
    commit=git('log','-1','--format=%H','--',name)
    assert blob['stdout']==head['stdout'],'Current source differs from HEAD; do not label it as a committed version'
    out.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),
                'git_blob':blob['stdout'],'head_blob':head['stdout'],
                'last_path_commit':commit['stdout'],
                'git_warnings':[x['stderr'] for x in (blob,head,commit) if x['stderr']]})
result={'status':'CURRENT_CHECKOUT_FILES_MATCH_HEAD','files':out,
        'limits':'This pins the current checkout files; it is not a loaded process PID/path/module proof.'}
(W/'source-identity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'files':[(x['path'],x['last_path_commit'][:10]) for x in out]}))
