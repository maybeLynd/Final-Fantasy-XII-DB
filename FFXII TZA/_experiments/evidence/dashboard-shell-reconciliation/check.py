import argparse,hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();p=argparse.ArgumentParser();p.add_argument('--raw',type=Path);a=p.parse_args();r=json.loads((a.raw or W/'run-01/raw.json').read_text());R=W/'run-01'
assert r['terminal'] and r['exception'] is None and r['verdict']=='ACCEPT_SCOPED_SELECTED_VIEW_HTTP_ADMISSION','INVALID_CAPTURE'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
q=json.loads((W/'capture-terminal.json').read_text());assert q['terminal'] and q['returncode']==0 and not q['stderr']
assert r['source_readback'] and all(r['source_readback'].values())
for rel,z in r['sources'].items():
 b=(R/'source'/rel).read_bytes();assert sha(b)==z['sha256'];q=subprocess.run(['git','rev-parse',r['source_commit']+':'+rel],capture_output=True,text=True);assert q.returncode==0 and q.stdout.strip()==z['blob'];assert subprocess.run(['git','hash-object','--stdin'],input=b,capture_output=True).stdout.decode().strip()==z['blob']
cs=r['cases'];assert len(cs)==4 and {x['name'] for x in cs}=={'valid-selected-view','hash-declared-nonjson','missing-selected-view','failed-selected-view'},'MISSING_CASE'
assert len({x['generation']['generation'] for x in cs})==4
for x in cs:
 g=x['generation'];q=g['cli'];assert q['terminal'] and q['returncode']==0 and not q['stderr'] and 'verify' in q['argv'],'FAILED_PREREQUISITE'
 assert g['output_names'] and 'view-fleet.json' in g['output_names'] and x['pass']
 sh=r['http'][x['status_http_index']];vh=r['http'][x['view_http_index']];assert sh['path']=='/api/status' and vh['path']=='/api/view/overview' and sh['status']==vh['status']==200
 for h in [sh,vh]:assert json.loads(bytes.fromhex(h['bytes_hex']))==h['parsed']
 s,v=sh['parsed'],vh['parsed'];e=x['expected_selected_status'];assert s['generation']==g['generation'] and not s['problems'] and not s['reader_stale'] and s['views']['overview']==e and s['views']['fleet']=='OK'
 if e in ['MALFORMED','UNMEASURED']:assert v['status']==e and 'view' not in v,'BAD_DATA_SERVED'
 else:assert v['view']['status']==e and v['meta']['generation']==g['generation']
 assert x['other_missing_views'] and all(z=='UNMEASURED' for z in x['other_missing_views'].values())
c=r['cleanup'];assert c['owned_handle_terminal'] and not c['exact_port_listeners'] and c['netstat_returncode']==0
assert r['post_health']['status']==200 and r['page_presentation'].startswith('NOT_EXECUTED')
print('ACCEPT_SCOPED_SELECTED_VIEW_HTTP; RETAIN_RENDERING_AND_DEPLOYMENT_GAPS')
