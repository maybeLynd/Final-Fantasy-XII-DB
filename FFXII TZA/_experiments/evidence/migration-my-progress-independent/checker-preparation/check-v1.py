"""Focused retained-evidence checker; default is read-only, never re-runs captures."""
import argparse,hashlib,json,re
from pathlib import Path
W=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['core','admission','collection','author','http','ui']);ap.add_argument('--raw',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def raw(name,phase):return read(a.raw if a.phase==phase and a.raw else W/name/'raw.json')
def source_check(r,base):
 for rel,s in r['sources'].items():
  p=base/rel;data=p.read_bytes();assert sha(p)==s['sha256'],rel
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==s['blob'],rel
def names(r,want):
 assert len(r['cases'])==len(want) and {c['name'] for c in r['cases']}==set(want),'Missing/duplicate case'
 return {c['name']:c for c in r['cases']}
c=raw('core-01','core');assert c['phase_finished'] is True and sha(W/'core-controls.py')==c['driver_sha256']
assert sha(W/'core-01/requirements.py')==c['source_sha256']
cs=names(c,('all-accepted-final30','open-Q-with-all-L2-MET','missing-bucket-family','invalid-terminal-required0'))
for n,v in cs.items():
 assert sha(W/'core-01'/(n+'-input.json'))==v['input_sha256']
 assert sha(W/'core-01'/(n+'-output.json'))==v['output_sha256']
 o=read(W/'core-01'/(n+'-output.json'));assert o['ready']==v['ready'] and o['terminal']==v['terminal'] and o['scopes']['union']==v['union']
assert cs['all-accepted-final30']['ready'] and cs['all-accepted-final30']['terminal']=={'accepted':30,'required':30}
assert not cs['open-Q-with-all-L2-MET']['ready'] and not cs['missing-bucket-family']['measured'] and not cs['missing-bucket-family']['ready']
assert cs['invalid-terminal-required0']['ready'] and cs['invalid-terminal-required0']['terminal']=={'accepted':0,'required':0}
r=raw('admission-01','admission');assert r['finished'] is True and r['sources_unchanged'] is True
assert sha(W/'admission-controls.py')==r['driver_sha256'];source_check(r,W/'admission-01/source')
assert r['sources']['Database/Tools/dashboard/requirements.py']['sha256']==c['source_sha256']
ac=names(r,('valid-final30','invalid-terminal0','partial29-not-met','inconsistent-headline','ready-with-open-Q'))
for n,v in ac.items():
 d=W/'admission-01'/n;assert sha(d/'view-input.json')==v['view_sha256'] and sha(d/'producer-original.json')==v['original_producer_sha256']
 assert read(d/'receipt.json')==v
 assert not v['status']['reader_stale'] and not v['status']['problems']
 view=read(d/'view-input.json');assert v['status']['generation']==v['generation']
 if n in ('valid-final30','invalid-terminal0','partial29-not-met'):
  assert v['check_view_reason'] is None and v['admitted'] is True and v['status']['views']['progress']=='OK'
  assert v['served']['view']==view and v['original_producer_sha256']==v['view_sha256']
 else:assert v['check_view_reason'] and v['admitted'] is False and v['status']['views']['progress']=='MALFORMED' and 'view' not in v['served']
 assert view['progress']['reconstruction']['state'].startswith('DATABASE READY')==(n in ('valid-final30','invalid-terminal0','ready-with-open-Q'))
assert ac['invalid-terminal0']['served']['view']['progress']['terminal']=={'accepted':0,'required':0}
assert ac['partial29-not-met']['served']['view']['progress']['terminal']=={'accepted':29,'required':30}
rep=(W/'admission-01/source/Database/FFXII TZA/_index/progress/progress_report.py').read_text()
assert re.search(r'[\"\']required_consecutive[\"\']\s*:\s*30',rep),'Retain normal-emitter limit'
r=raw('collection-02','collection');assert r['finished'] is True and r['sources_unchanged'] is True
assert sha(W/'collection-controls.py')==r['driver_sha256'];source_check(r,W/'collection-02/source')
cc=names(r,('collect-carrier-READY','collect-carrier-DONE','conflicting-duplicate-key','reopen-required-row','DD-split-current'))
for state in ('READY','DONE'):
 v=cc['collect-carrier-'+state];assert v['carrier']['ok']==(state=='DONE') and len(v['page_residue'])==2
 assert {'F','R','X','K'}<=set(v['failed_families'])
 assert v['documents']['DD:04-Actor-Entity/answered.md']['st']=='documented, all answered'
 assert v['documents']['DD:04-Actor-Entity/dispositioned.md']['st']=='documented with a dispositioned residue'
 assert not v['documents']['DD:04-Actor-Entity/partial.md']['ok']
 f=read(W/'collection-02'/('facts-'+state+'.json'));assert next(x for x in f['facts'] if x['k']=='Q:W-901')==v['carrier']
 assert [x for x in f['facts'] if x['f']=='P']==v['page_residue']
v=cc['conflicting-duplicate-key'];assert v['duplicates_merged']==1 and v['scopes']['union']['total']==45 and not v['ready']
assert not cc['reopen-required-row']['ready']
v=cc['DD-split-current'];assert not v['measured'] and v['q_split']['dd_answered']==v['q_split']['dd_dispositioned']==1
fail=read(W/'collection-preparation-v1/failure.json');assert fail['collection_finished'] is False and 'parenthetical' in fail['cause']
assert 'sys.excepthook=retain_failure' in (W/'collection-controls.py').read_text(),'Actual corrected driver must retain failure'
r=raw('author-622-01','author');assert r['terminal'] is True and r['returncode']==0 and not r['stderr'] and r['complete_case_set'] is True and r['all_sources_unchanged'] is True
assert sha(W/'author-suite.py')==r['driver_sha256'];source_check(r,W/'author-622-01/source')
assert r['commit']=='622c0866ddf7b7f1484b92b34adfaa46190ee821'
assert r['tags']=={'MP'+str(i):'PASS' for i in range(1,13)} and r['stdout'].rstrip().endswith('FAILS 0')
r=raw('deployed-01','http');assert r['finished'] is True and sha(W/'deployed-http.py')==r['driver_sha256'] and len(r['requests'])==4
for x in r['requests']:
 p=W/'deployed-01'/(x['name']+('.html' if x['name']=='page' else '.json'));assert sha(p)==x['sha256'] and p.stat().st_size==x['bytes'] and x['status']==200
assert r['reported_reader_stale']==[True,True] and r['view_status']=='PARTIAL' and r['progress_measured'] is False and r['gaps']
v=read(W/'deployed-01/progress.json')['view'];m={x['id']:x for x in v['measures']}
for k,s in v['progress']['scopes'].items():
 key='union-exf' if k=='union_exF' else k;assert (s['accepted'],s['total'])==(m[key]['numerator'],m[key]['denominator'])
for s in v['progress']['categories']:assert (s['accepted'],s['total'])==(m['cat-'+s['code']]['numerator'],m['cat-'+s['code']]['denominator'])
r=raw('deployed-ui-02','ui');assert r['finished'] is False and r['fatal']=={'type':'KeyError','reason':"'key'"}
assert sha(W/'browser-receipt.py')==r['driver_sha256'] and len(r['requests'])==3
for x in r['requests']:assert sha(W/'deployed-ui-02'/(x['name']+'.json'))==x['sha256'] and x['status']==200
for n,s in r['files'].items():assert sha(W/'deployed-01'/n)==s['sha256']
u=read(W/'deployed-ui-02/normalized.json');assert u['finished'] is True and u['raw_sha256']==sha(W/'deployed-ui-02/raw.json') and u['normalizer_sha256']==sha(W/'browser-normalize.py')
assert u['generation']==r['browser_generation']=='g20260929T074817Z-5dfce1' and u['reader_stale']==[False,False] and len(u['ids'])==len(set(u['ids']))==16
assert set(u['ids'])=={x['k'] for x in u['category']['items']} and 'close returned' in u['closed']
assert (W/'deployed-01/browser-expanded.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
result={'verdict':'REJECT','scope':'My Progress terminal prerequisite admission; bounded independent collect/measure/producer/reader controls and deployed presentation separately retained',
 'requirements_source_last_commit':c['source_last_commit'],'requirements_sha256':c['source_sha256'],
 'producer_reader_source_tree':'f21fe80440fc9d24df09fc19172753394fe61773',
 'defect':'Explicit pre-resolved required_consecutive=0 with synthetic MET/acceptanceOK gate yields DATABASE READY, terminal0of0 through original measure/v_progress/Store/State/check_view. Fixed30 is not validated on those composed boundaries.',
 'cause':'terminal_facts trusts reporter required_consecutive; measure and server check readiness against that supplied denominator rather than the governing fixed30 prerequisite.',
 'reachability_limit':'Normal captured reporter source hardcodes30. Invalid0 is injected input, not demonstrated normal producer output or a false Ready in actual deployed database. Full _build_once, other adapters/CLI-main and real terminal audits omitted.',
 'positive_controls':'Complete30 admitted; openQ with allL2MET and missingbucket rejectReady; inconsistent headline and Ready-with-openQ refused by reader; pending transfer remains unaccepted until DONE; duplicate conflicts retain false/global-once; reopening removes acceptance. Current DD answered/dispositioned split observed with page residue retained.',
 'author_suite':'Exact requested622c0866d producer-authored MP1-MP12 allPASS/FAILS0/exit0, separate from independent design; no current DD/delta suite acceptance.',
 'semantic_question':'MP2 section2 permits receipted partial terminal counter; section6 says partial streaks not shown accepted. Original partial29-not-met shows accepted29/30 and NotReady. Meaning/adoption requires FABLE ruling; not falsefullcompletion.',
 'deployment':'EarlierHTTP generation g20260929T074315Z-b38fd2 reader_staleTrue; newer rendered and bracketedHTTP g20260929T074817Z-5dfce1 reader_staleFalse. Both PARTIAL/UNMEASURED/NOT_READY, bucket gap visible. UI16 exact Worldmaps DA/DD IDs agree with same-generation HTTP. This is not PID/loaded-module/final deployment acceptance.',
 'corrections':'Collection01 invalid parenthetical status fixture retained; corrected supported delimiter plus actual exception receipt hook. UI binding key/K confusion retained as failed raw; same captured bytes normalized using actual k, no recapture or additional run credit.',
 'cleanup':'Agent-created dashboard tab closed; captures read-only. Requested authored process terminal; private source fixtures only. No game/controller/production board/store/save/config/reference changes. Earlier unrelated transition descendant cleanup remains UNVERIFIED.',
 'limits':'MethodA Python tools/synthetic or captured dashboard, not FF12 instructions/live/parity. DD literalstatus fixture is not five-condition legal DOCUMENTED certification; failed F/R/X/K corpus families remainUNMEASURED. No allM0-M5/A17/A19/fullL1L2 acceptance. Ownchecker/producer suites not independent acceptance.',
 'next':'OPUS cause/affectedconsumer repair for fixed30 prerequisite admission and exact finalsource scoped review. FABLE settles partial29 displayedacceptance meaning. FRONTIER current deployment lineage acceptance separately open; do not resend resolved stale-reader request or edit peer consumers. Continue returned generation/transition repairs after publication.'}
if a.out:
 if a.out.exists():assert read(a.out)==result,'Preserve existing result'
 else:a.out.write_text(json.dumps(result,indent=2)+'\n')
print('REJECT_PROGRESS_TERMINAL_ADMISSION_BOUNDED_CONTROLS_COMPLETE',flush=True)
