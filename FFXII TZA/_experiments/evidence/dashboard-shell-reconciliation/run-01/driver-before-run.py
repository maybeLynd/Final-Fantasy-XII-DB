import hashlib,importlib.util,json,os,socket,subprocess,sys,time,traceback,urllib.request,urllib.error
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';assert not R.exists();R.mkdir();H=R/'source';C='69bbf8c81bbfea644a05584e70b7fd73e51fb80e';sha=lambda b:hashlib.sha256(b).hexdigest();raw={'method':'A original repository Python/actual private loopback HTTP; labelled synthetic generations, no FF12/game/PC','source_commit':C,'driver_sha256':sha(Path(__file__).read_bytes()),'sources':{},'cases':[],'http':[],'terminal':False,'exception':None,'cleanup':None};(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes());child=None;log=None
try:
 for rel in ['Database/Tools/dashboard/server.py','Database/Tools/dashboard/requirements.py','Database/Tools/analysis-kit/gfz-scripts/generation.py']:
  q=subprocess.run(['git','show',C+':'+rel],capture_output=True);assert q.returncode==0,q.stderr;b=q.stdout;p=H/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  q=subprocess.run(['git','rev-parse',C+':'+rel],capture_output=True,text=True);assert q.returncode==0;raw['sources'][rel]={'sha256':sha(b),'blob':q.stdout.strip(),'original_preimage_sha256':sha(Path(rel).read_bytes())}
 gp=H/'Database/Tools/analysis-kit/gfz-scripts/generation.py';sp=importlib.util.spec_from_file_location('private_original_generation',gp);G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G);assert Path(G.__file__).resolve()==gp.resolve()
 st=G.Store(str((R/'store').resolve()));inp=R/'controlled-input';inp.write_bytes(b'ASTRA private shell selected-view input\n');inputs={'controlled':{'path':str(inp.resolve())}}
 def commit(overview):
  b=st.begin(inputs,dict(name='ASTRA labelled selected-view HTTP fixture',sha256=raw['driver_sha256']))
  fleet={'view':'fleet','status':'OK','measures':[],'sentinel':'INERT_OUTPUT'};Path(b.output_path('view-fleet.json')).write_text(json.dumps(fleet));names=['view-fleet.json']
  if overview is not None:Path(b.output_path('view-overview.json')).write_bytes(overview);names.append('view-overview.json')
  gid=st.commit(b,names);man,gd,probs=st.open_current();assert not probs and man['generation']==gid
  q=subprocess.run([sys.executable,'-B',str(gp),'verify',st.root],capture_output=True,text=True);assert q.returncode==0 and not q.stderr,(q.returncode,q.stdout,q.stderr)
  return {'generation':gid,'manifest_sha256':sha((Path(gd)/G.MANIFEST).read_bytes()),'cli':{'argv':q.args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True},'output_names':names,'overview_bytes_hex':None if overview is None else overview.hex()}
 def request(path):
  with urllib.request.urlopen(base+path,timeout=3) as z:status=z.status;data=z.read()
  rec={'path':path,'status':status,'bytes_hex':data.hex(),'parsed':json.loads(data)};raw['http'].append(rec);return rec
 payloads=[('valid-selected-view',json.dumps({'view':'overview','status':'OK','measures':[],'sentinel':'POSITIVE_SELECTED_VIEW'}).encode(),'OK'),('hash-declared-nonjson',b'not JSON: this is intentionally hash-declared fixture bytes','MALFORMED'),('missing-selected-view',None,'UNMEASURED'),('failed-selected-view',json.dumps({'view':'overview','status':'FAILED','measures':[],'why':'labelled adapter failure','sentinel':'FAILED_VIEW_STATUS'}).encode(),'FAILED')]
 first=commit(payloads[0][1]);sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close();base='http://127.0.0.1:'+str(port)
 server=H/'Database/Tools/dashboard/server.py';env=os.environ.copy();env['FF12_FLEET_DIR']=str((R/'inert-fleet').resolve());log=(R/'server.log').open('wb');argv=[sys.executable,'-B',str(server),'--root',st.root,'--port',str(port)];child=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,env=env);raw['child']={'pid':child.pid,'argv':argv,'host':'127.0.0.1','port':port}
 deadline=time.monotonic()+8
 while True:
  assert child.poll() is None,'Child stopped before readiness'
  try:ready=request('/api/status');break
  except (urllib.error.URLError,ConnectionError,TimeoutError):
   if time.monotonic()>deadline:raise TimeoutError('Private server startup exceeded8s')
   time.sleep(.1)
 for j,(name,payload,expected) in enumerate(payloads):
  gen=first if j==0 else commit(payload);status=request('/api/status');view=request('/api/view/overview');s=status['parsed'];v=view['parsed'];assert status['status']==view['status']==200 and s['generation']==gen['generation'] and not s['problems'] and not s['reader_stale']
  assert s['views']['overview']==expected and s['views']['fleet']=='OK'
  if expected in ['MALFORMED','UNMEASURED']:assert v['status']==expected and 'view' not in v
  else:assert v['view']['status']==expected and v['meta']['generation']==gen['generation']
  raw['cases'].append({'name':name,'expected_selected_status':expected,'generation':gen,'status_http_index':len(raw['http'])-2,'view_http_index':len(raw['http'])-1,'observed':expected,'pass':True,'other_missing_views':{k:z for k,z in s['views'].items() if k not in ['overview','fleet']}})
 assert child.poll() is None;raw['post_health']=request('/api/status')
 raw['page_presentation']='NOT_EXECUTED: HTTP statuses/data only; no rendered browser/navigation acceptance'
 raw['verdict']='ACCEPT_SCOPED_SELECTED_VIEW_HTTP_ADMISSION'
except BaseException as e:
 raw['exception']={'type':type(e).__name__,'text':str(e),'traceback':traceback.format_exc()};raw['verdict']='INVALID'
finally:
 if child is not None:
  child.terminate()
  try:child.wait(timeout=5)
  except subprocess.TimeoutExpired:child.kill();child.wait(timeout=5)
  if log:log.close()
  net=subprocess.run(['netstat','-ano','-p','tcp'],capture_output=True,text=True);assert net.returncode==0
  listeners=[l for l in net.stdout.splitlines() if 'LISTENING' in l and l.split()[1].endswith(':'+str(raw['child']['port']))]
  raw['cleanup']={'pid':child.pid,'owned_handle_terminal':child.poll() is not None,'returncode':child.returncode,'exact_port_listeners':listeners,'netstat_returncode':net.returncode};assert not listeners
 raw['source_readback']={rel:sha(Path(rel).read_bytes())==z['original_preimage_sha256'] and sha((H/rel).read_bytes())==z['sha256'] for rel,z in raw['sources'].items()}
 raw['terminal']=True;(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n');print(raw.get('verdict'),raw['exception']);sys.exit(1 if raw['exception'] else 0)
