import hashlib,json,subprocess,sys
from pathlib import Path
W=Path('Database/Tools/work/ASTRA/poison-q6-independent');sha=lambda b:hashlib.sha256(b).hexdigest();src=json.loads((W/'source.json').read_text());p=W/'private-source'
a=[]
for r in src['records']:
 d=Path(r['path']).read_bytes();same=sha(d)==r['current_preimage_sha256'];a.append(dict(path=r['path'],sha256=sha(d),unchanged_since_preparation=same));assert same,r['path']
 if not r['current_matches']:(p/('current-preimage-'+r['copy'])).write_bytes(d)
old=json.loads((p/'author-poison-result.json').read_text());current=json.loads(Path(src['records'][2]['path']).read_text());print('AUTHOR_RESULT_JSON_EQUAL',old==current)
q=subprocess.run([sys.executable,'-B',str(W/'capture.py'),'--prerequisite-control'],capture_output=True,text=True);assert q.returncode!=0 and 'UPSTREAM_FAILED_OR_MISSING' in q.stderr
rec={'argv':q.args,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True,'shipping_code_executed':False,'input':'retained run-01 prerequisite with ok False','expected':'refuse before downstream'};(W/'prerequisite-control.json').write_text(json.dumps(rec,indent=2)+'\n')
post={'originals':a,'reference_unchanged':sha(Path(src['image']['path']).read_bytes())==src['image']['sha256'],'graph_unchanged':all(sha(Path(g['path']).read_bytes())==g['sha256'] for g in src['graph']),'live_game_or_pc_control_used':False,'private_capture_process_terminal':True,'prior_author_result_json_equal_current':old==current};assert post['reference_unchanged'] and post['graph_unchanged'];(W/'cleanup.json').write_text(json.dumps(post,indent=2)+'\n')
(W/'run-01/tool-receipt.json').write_text(json.dumps({'tool':'exec_command','chunk_id':'7fc1f3','cmd':'.\\Collaboration\\Tools\\analysis\\venv\\Scripts\\python.exe -B Database/Tools/work/ASTRA/poison-q6-independent/capture.py','exit_code':0,'output':'ACCEPT_SCOPED_ORIGINAL_BUILDER_Q6_AND_CRITICAL_SELECTION None','terminal':True,'source':'actual terminal tool result, no recapture'},indent=2)+'\n')
print('PREREQUISITE_REFUSED_AND_ORIGINALS_UNCHANGED',q.returncode,len(a))
