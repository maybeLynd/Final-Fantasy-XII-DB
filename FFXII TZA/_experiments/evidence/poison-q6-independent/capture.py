import contextlib,hashlib,io,json,sys,traceback
from pathlib import Path
W=Path(__file__).resolve().parent;P=W/'private-source';sha=lambda b:hashlib.sha256(b).hexdigest()
def require_prerequisite(r):
 assert isinstance(r,dict) and r.get('total')==6 and r.get('pass')==6 and r.get('ok') is True,'UPSTREAM_FAILED_OR_MISSING'
 assert len(r.get('results',{}))==6 and all(x.get('pass_') is True for x in r['results'].values()),'UPSTREAM_CASE_FAILED_OR_MISSING'
if '--prerequisite-control' in sys.argv:
 r=json.loads((W/'run-01/raw.json').read_text())['prerequisite']
 r['ok']=False
 require_prerequisite(r)
 raise AssertionError('Required refusal was suppressed')
R=W/'run-01';R.mkdir(exist_ok=False);(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes());out={'evidence_class':'B isolated verified shipping instructions; planted stats/tables; memset import bridge; no live game','reference':json.loads((W/'source.json').read_text()),'driver_sha256':sha(Path(__file__).read_bytes()),'terminal':False,'exception':None,'downstream_started':False}
text=io.StringIO()
try:
 for r in out['reference']['records']:
  assert sha((P/r['copy']).read_bytes())==r['sha256'],'PRIVATE_SOURCE_MOVED'
 for r in out['reference']['graph']:assert sha(Path(r['path']).read_bytes())==r['sha256'],'GRAPH_MOVED'
 sys.path.insert(0,str(P))
 with contextlib.redirect_stdout(text):
  import check as C
  out['module_paths']={'check':C.__file__}
  out['prerequisite']=json.loads((P/'result.json').read_text());require_prerequisite(out['prerequisite']);assert C.allok is True
  out['downstream_started']=True
  import poison as Q
  out['module_paths']['poison']=Q.__file__
  original=json.loads((P/'poison_result.json').read_text());out['original_case_results']=original
  assert original['fails']==0 and len(original['cases'])==14
  for name,r in original['cases'].items():
   got=r['observed'];assert got['ran'] is True and not got['faults'] and not got['outside'] and r['verdict']=='PASS',name
  expected_deltas={'1_poison_maxhp_1000':-62,'2_poison_under_bubble':-125,'3_poison_under_disease_hp40':-2,'4_poison_maxhp_15_zero_share':-1,'5a_sap_hp_1':0,'5b_sap_hp_2':-1,'7_stop_skips_poison':0,'10_no_status_hp_below_line':0,'12_crit_only_hp_above_line':0}
  for name,delta in expected_deltas.items():assert original['cases'][name]['observed']['hp_delta']==delta,name
  assert int(original['cases']['6a_word1_duration_expires']['observed']['remove'],16)&(1<<20)
  assert not(int(original['cases']['6b_word1_duration_not_yet']['observed']['remove'],16)&(1<<20))
  for name in ['10_no_status_hp_below_line','5a_sap_hp_1']:
   obs=original['cases'][name]['observed'];assert not(int(obs['flagA'],16)&0x100) and int(obs['apply'],16)&(1<<29)
  obs=original['cases']['12_crit_only_hp_above_line']['observed'];assert not(int(obs['flagA'],16)&0x100) and int(obs['remove'],16)&(1<<29)
  # Focused independent entry/boundary controls, not a full-arm census.
  from unicorn import UC_HOOK_CODE
  from unicorn.x86_const import UC_X86_REG_R8,UC_X86_REG_RCX,UC_X86_REG_RDX
  selected={0x386F81,0x386F85,0x386F95,0x386FD2,0x386FD5,0x386FDE,0x386FE7,0x386FF3};trace=[]
  def observe(u,a,n,_):
   if a in selected:
    assert len(trace)<100,'TRACE_BUDGET_EXCEEDED'
    trace.append({'pc':hex(a),'r8d':u.reg_read(UC_X86_REG_R8)&0xffffffff,'ecx':u.reg_read(UC_X86_REG_RCX)&0xffffffff,'edx':u.reg_read(UC_X86_REG_RDX)&0xffffffff})
  hook=C.uc.hook_add(UC_HOOK_CODE,observe);C.uc.ctl_remove_cache(0x386C70,0x387017)
  cases=[('below_critical_line',dict(hp=199),dict(apply_has=1<<29,flagA_lacks=0x100,hp_delta=0)),('equal_critical_line',dict(hp=200,w3c=1<<29),dict(remove_has=1<<29,apply_lacks=1<<29,flagA_lacks=0x100,hp_delta=0)),('nonpositive_removes_critical',dict(hp=0,w3c=1<<29),dict(remove_has=1<<29,apply_lacks=1<<29,flagA_lacks=0x100,hp_delta=0)),('stop_poison_low_hp',dict(hp=100,w3c=(1<<3)|(1<<8),beat={8:10}),dict(apply_has=1<<29,flagA_lacks=0x100,hp_delta=0)),('bubble_equal_line',dict(hp=400,w3c=(1<<28)|(1<<29)),dict(remove_has=1<<29,apply_lacks=1<<29,flagA_lacks=0x100,hp_delta=0))]
  out['independent_boundaries']={}
  for name,kw,want in cases:
   trace.clear();got=Q.case(**kw);bad=Q.judge(got,want);assert not bad,(name,bad)
   stats_before_criterion=all(not(0x72000000<=a<0x72000800) for _,a,n in C.state['writes'])
   guard=bytes(C.uc.mem_read(C.RESULT+C.RSIZE,C.GUARD));assert guard==bytes([0xcc])*C.GUARD
   assert stats_before_criterion and C.state['order']==[1,2,3,4,5] and not C.state['faults'] and not C.state['bad']
   assert any(x['pc']=='0x386f95' for x in trace),name
   out['independent_boundaries'][name]={'fixture':kw,'expected':want,'observed':got,'trace':list(trace),'stage_order':list(C.state['order']),'stats_write_observed':not stats_before_criterion,'guard_unchanged':True,'verdict':'PASS'}
  C.uc.hook_del(hook)
  sample=out['independent_boundaries']['below_critical_line']['observed'];out['judge_controls']={'valid':Q.judge(sample,cases[0][2]),'wrong_hp_delta':Q.judge(sample,dict(hp_delta=-1))};assert out['judge_controls']['valid']==[] and out['judge_controls']['wrong_hp_delta']
 for r in out['reference']['records']:
  assert sha((P/r['copy']).read_bytes())==r['sha256']
 for r in out['reference']['graph']:assert sha(Path(r['path']).read_bytes())==r['sha256']
 out['verdict']='ACCEPT_SCOPED_ORIGINAL_BUILDER_Q6_AND_CRITICAL_SELECTION'
except BaseException as e:
 out['exception']={'type':type(e).__name__,'text':str(e),'traceback':traceback.format_exc()};out['verdict']='INVALID'
finally:
 out['stdout']=text.getvalue();out['terminal']=True;(R/'raw.json').write_text(json.dumps(out,indent=2)+'\n')
 print(out['verdict'],out['exception']);sys.exit(1 if out['exception'] else 0)
