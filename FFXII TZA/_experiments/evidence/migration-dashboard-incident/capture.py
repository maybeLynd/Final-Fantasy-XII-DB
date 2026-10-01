"""Independent incident controls. No producer test imports, live-store writes or game access."""
import hashlib, importlib.util, json, os, shutil, socket, subprocess, sys, time
import urllib.error, urllib.request
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
RUN = W/'run-01'
assert not RUN.exists(), 'Immutable run exists; inspect instead of overwriting/replaying'
RUN.mkdir()
raw = {'method':'A actual deployed HTTP plus labelled synthetic tooling stores/child servers',
       'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'python':sys.version, 'executable':sys.executable, 'cases':[], 'http':[], 'commands':[], 'sources':{}, 'cleanup':[]}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(name, observed, ok, limit=''):
    raw['cases'].append(dict(name=name, passed=bool(ok), observed=observed, limits=limit))
def dump():
    (RUN/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
def cmd(args, timeout=15):
    try:
        r=subprocess.run([str(x) for x in args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
        d=dict(args=[str(x) for x in args],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr)
    except subprocess.TimeoutExpired as e:
        d=dict(args=[str(x) for x in args],returncode=None,timeout=timeout,stdout=str(e.stdout),stderr=str(e.stderr))
    raw['commands'].append(d); return d
def http(base,path,method='GET'):
    req=urllib.request.Request(base+path,method=method)
    try:
        with urllib.request.urlopen(req,timeout=5) as r: code=r.status; body=r.read()
    except urllib.error.HTTPError as e: code=e.code; body=e.read()
    d=json.loads(body) if path!='/ ' and body[:1] in [b'{',b'['] else body.decode(errors='replace')
    raw['http'].append(dict(url=base+path,method=method,code=code,body=d));return code,d

# Copy exact current production modules and vocabulary, not their tests.
paths=['Database/Tools/dashboard/server.py','Database/Tools/dashboard/build_views.py',
       'Database/Tools/analysis-kit/gfz-scripts/generation.py',
       'Database/FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md',
       'Database/FFXII TZA/_index/completion-packages/README.md']
for rel in paths:
    p=ROOT/rel; target=RUN/'source'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    raw['sources'][rel]=dict(sha256=sha(p),bytes=p.stat().st_size,retained=str(target.relative_to(RUN)),
        last_commit=subprocess.check_output(['git','log','-1','--format=%H','--',rel],text=True).strip())
gpath=RUN/'source/Database/Tools/analysis-kit/gfz-scripts/generation.py'
spec=importlib.util.spec_from_file_location('independent_generation',gpath);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
server_path=RUN/'source/Database/Tools/dashboard/server.py'
names=['overview','systems','vbf','executable','types','evidence','fleet']
def fixture(name,external=False):
    d=RUN/name;d.mkdir(); inp=d/'source-input';inp.write_bytes(b'ordinary controlled input\n')
    store=G.Store(str(d/'store'));inputs={'controlled':dict(path=str(inp),**({'snapshot':False} if external else {}))}
    return d,inp,store,inputs
def build(st,inputs,marker,missing=None):
    b=st.begin(inputs,dict(name='ASTRA labelled synthetic seven-view fixture',sha256=raw['driver_sha256']))
    for n in names:
        if n==missing:continue
        Path(b.output_path('view-'+n+'.json')).write_text(json.dumps(dict(view=n,status='OK',title=n,measures=[],sentinel=marker)))
    return st.commit(b,['view-'+n+'.json' for n in names])
def current(st): return json.loads((Path(st.root)/G.CURRENT).read_text())['generation']
def cli(st,mode='verify'):return cmd([sys.executable,'-B',gpath,mode,st.root])
def server(st):
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    log=open(Path(st.root).parent/'server.log','wb')
    p=subprocess.Popen([sys.executable,'-B',str(server_path),'--root',st.root,'--port',str(port)],stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
    base='http://127.0.0.1:'+str(port)
    deadline=time.monotonic()+12
    try:
        while time.monotonic()<deadline:
            if p.poll() is not None:raise RuntimeError('Private server exited '+str(p.returncode))
            try:http(base,'/api/status');return p,log,base
            except (urllib.error.URLError,ConnectionError,TimeoutError):time.sleep(.1)
        raise TimeoutError('Private server startup exceeded12s')
    except BaseException:
        p.terminate();p.wait(timeout=5);log.close();raise
def stop(s):
    p,log,base=s;p.terminate()
    try:p.wait(timeout=5)
    except subprocess.TimeoutExpired:p.kill();p.wait(timeout=5)
    log.close();raw['cleanup'].append(dict(pid=p.pid,base=base,terminated=True,returncode=p.returncode))
def no_marker(d,bad):return bad not in json.dumps(d)

try:
    # Deployed observations: read-only, no production start/stop/refresh/cutover.
    base='http://127.0.0.1:8765';c,initial=http(base,'/api/status')
    live=[]
    for n in names:
        code,v=http(base,'/api/view/'+n);live.append((n,code,v))
    c,last=http(base,'/api/status')
    generations=[initial.get('generation'),last.get('generation')]+[v.get('meta',v).get('generation') for _,_,v in live]
    record('deployed-seven-view-coherence',dict(generations=generations,views=initial.get('views'),reader_stale=initial.get('reader_stale')),len(set(generations))==1 and None not in generations and all(c==200 and 'view' in v for _,c,v in live), 'One bracketed HTTP sample; actual loaded module hash/process identity not independently measured.')
    # Baseline covers the incident external-input distinction on a real disk store.
    d,inp,st,inputs=fixture('external-baseline',True);gid=build(st,inputs,'VALID_EXTERNAL');cr=cli(st)
    s=server(st)
    try:
        _,v=http(s[2],'/api/view/overview');record('external-input-baseline',dict(cli=cr['returncode'],http=v),cr['returncode']==0 and v.get('view',{}).get('sentinel')=='VALID_EXTERNAL')
        code,v=http(s[2],'/api/status',method='POST');record('actual-http-read-only',v,code==405)
    finally:stop(s)
    # Ordinary snapshot tampering after the reader has verified/cache-warmed it.
    d,inp,st,inputs=fixture('warm-tamper');old=build(st,inputs,'PRIOR_VALID');gid=build(st,inputs,'NEW_VALID');s=server(st)
    try:
        _,v=http(s[2],'/api/view/overview');assert v['view']['sentinel']=='NEW_VALID'
        out=Path(st.root)/gid/'outputs/view-overview.json';out.write_text(out.read_text().replace('NEW_VALID','CORRUPTED'))
        _,v=http(s[2],'/api/view/overview');_,status=http(s[2],'/api/status');cr=cli(st)
        record('warm-output-tamper-rejected',dict(view=v,status=status,cli=cr['returncode']),cr['returncode']!=0 and status['historical'] and status['generation']==old and v['meta']['historical'] and v['view']['sentinel']=='PRIOR_VALID' and no_marker(v,'CORRUPTED'))
    finally:stop(s)
    d,inp,st,inputs=fixture('input-tamper');gid=build(st,inputs,'NO_INVALID_DATA');(Path(st.root)/gid/'inputs/controlled').write_bytes(b'mismatched snapshot\n');cr=cli(st);s=server(st)
    try:
        _,v=http(s[2],'/api/view/overview');record('snapshot-tamper-no-fallback',dict(http=v,cli=cr['returncode']),cr['returncode']!=0 and v.get('status')=='INVALID' and 'view' not in v)
    finally:stop(s)
    # Same-size edit and mtime restoration deliberately tests the stated stat-cache boundary.
    d,inp,st,inputs=fixture('stat-preserved-tamper');gid=build(st,inputs,'ORIGINAL');s=server(st)
    try:
        _,v=http(s[2],'/api/view/overview');assert v['view']['sentinel']=='ORIGINAL'
        out=Path(st.root)/gid/'outputs/view-overview.json';before=out.stat();oldbytes=out.read_bytes();new=oldbytes.replace(b'ORIGINAL',b'TAMPERED');assert len(oldbytes)==len(new)
        out.write_bytes(new);os.utime(out,ns=(before.st_atime_ns,before.st_mtime_ns));after=out.stat();cr=cli(st)
        _,v=http(s[2],'/api/view/overview');_,status=http(s[2],'/api/status')
        record('stat-preserved-mismatch-detected',dict(size_before=before.st_size,size_after=after.st_size,mtime_before=before.st_mtime_ns,mtime_after=after.st_mtime_ns,cli=cr,http=v,status=status),cr['returncode']!=0 and (status['historical'] or status['no_verified_generation']), 'Cached original data may remain safe while validation/status incorrectly remains CURRENT; distinguish that from serving tampered bytes.')
        record('stat-preserved-tampered-bytes-not-served',v,no_marker(v,'TAMPERED'),'This narrower safety property does not repair an undetected on-disk mismatch.')
    finally:stop(s)
    # Failed candidate must preserve prior pointer/history and separately record failure.
    d,inp,st,inputs=fixture('failed-build');gid=build(st,inputs,'PREVIOUS');pointer=(Path(st.root)/G.CURRENT).read_bytes();hist=(Path(st.root)/G.HISTORY).read_bytes()
    error=None
    try:build(st,inputs,'HALF_BUILD',missing='fleet')
    except G.GenerationError as e:error=str(e)
    failure=json.loads((Path(st.root)/G.FAILURE).read_text());cr=cli(st)
    record('missing-output-failed-build-preserves-current',dict(error=error,failure=failure,cli=cr['returncode']),bool(error) and failure['current_unchanged']==gid and pointer==(Path(st.root)/G.CURRENT).read_bytes() and hist==(Path(st.root)/G.HISTORY).read_bytes() and cr['returncode']==0)
    b=st.begin(inputs);inp.write_bytes(b'changed strict input\n');Path(b.output_path('partial')).write_text('partial');error=None
    try:st.commit(b,['partial'])
    except G.GenerationError as e:error=str(e)
    record('strict-input-mid-build-rejected',dict(error=error,current=current(st)),bool(error) and current(st)==gid and pointer==(Path(st.root)/G.CURRENT).read_bytes())
    d,inp,st,inputs=fixture('volatile-mid-build');inputs['controlled']['volatile']=True;b=st.begin(inputs);snap=Path(b.dir)/'inputs/controlled';snapsha=sha(snap);inp.write_bytes(b'new volatile board state\n')
    for n in names:Path(b.output_path('view-'+n+'.json')).write_text(json.dumps(dict(view=n,status='OK',sentinel='VOLATILE_SNAPSHOT')))
    gid=st.commit(b,['view-'+n+'.json' for n in names]);man,_,probs=st.open_current()
    record('volatile-change-coherent-commit',dict(generation=gid,problems=probs,drift=st.drift(man),snapshot_sha=snapsha),not probs and man['inputs']['controlled']['sha256']==snapsha and 'controlled' in st.drift(man),'Synthetic board bytes, not a real TEAM mutation.')
    # Unknown format must not be silently interpreted, even with a matching pointer hash.
    d,inp,st,inputs=fixture('unknown-format');gid=build(st,inputs,'UNKNOWN_NOT_DATA');mp=Path(st.root)/gid/G.MANIFEST;man=json.loads(mp.read_text());man['format']='ff12-generation-UNKNOWN';mp.write_text(json.dumps(man));ptr=Path(st.root)/G.CURRENT;pjson=json.loads(ptr.read_text());pjson['manifest_sha256']=sha(mp);ptr.write_text(json.dumps(pjson));cr=cli(st);s=server(st)
    try:
        _,status=http(s[2],'/api/status');_,v=http(s[2],'/api/view/overview')
        record('unknown-format-unsupported',dict(cli=cr,status=status,view=v),cr['returncode']!=0 and 'UNSUPPORTED' in cr['stdout'] and v.get('status')=='UNSUPPORTED' and 'view' not in v)
    finally:stop(s)
    # Stale process code: edit ONLY the retained private server after it loaded.
    d,inp,st,inputs=fixture('stale-reader');gid=build(st,inputs,'STALE_CODE_CONTROL');s=server(st);saved=server_path.read_bytes()
    try:
        _,before=http(s[2],'/api/status');server_path.write_bytes(saved+b'\n# PRIVATE SOURCE CHANGE AFTER LOAD\n');_,after=http(s[2],'/api/status')
        record('stale-reader-reports-change',dict(before=before['reader_stale'],after=after['reader_stale']),before['reader_stale'] is False and after['reader_stale'] is True)
    finally:stop(s);server_path.write_bytes(saved)
    # Real current producer CLI to private root; no production-generation cutover.
    bp=ROOT/'Database/FFXII TZA/_index/_inbox/TEAM.json';before=json.loads(bp.read_text());args=[sys.executable,'-B',ROOT/'Database/Tools/dashboard/build_views.py','--root',RUN/'real-build']
    cr=cmd(args,timeout=120);after=json.loads(bp.read_text());rs=G.Store(str(RUN/'real-build'));man,_,probs=rs.open_current()
    record('actual-build-cli-while-board-advances',dict(command=cr,revision_before=before['revision'],revision_after=after['revision'],epoch_before=before['recovery_epoch'],epoch_after=after['recovery_epoch'],generation=(man or {}).get('generation'),problems=probs),cr['returncode']==0 and not probs and before['recovery_epoch']==after['recovery_epoch'] and after['revision']>before['revision'],'Actual scratch build and observed concurrent board operations, not production cutover/controller acceptance.')
    if not probs:
        s=server(rs)
        try:
            _,status=http(s[2],'/api/status');vals=[http(s[2],'/api/view/'+n)[1] for n in names]
            record('real-scratch-build-seven-views',dict(status=status,view_generations=[v.get('meta',v).get('generation') for v in vals]),all(v.get('meta',v).get('generation')==man['generation'] and 'view' in v for v in vals),'Meaning and whole M3 coverage not awarded here.')
        finally:stop(s)
    raw['finished']=True
except BaseException as e:
    raw['fatal']=dict(type=type(e).__name__,error=str(e));raise
finally:
    raw['sources_restored']={rel:sha(RUN/'source'/rel)==info['sha256'] for rel,info in raw['sources'].items()}
    dump()
print('CAPTURED',len(raw['cases']),'FAILED',[c['name'] for c in raw['cases'] if not c['passed']],flush=True)
