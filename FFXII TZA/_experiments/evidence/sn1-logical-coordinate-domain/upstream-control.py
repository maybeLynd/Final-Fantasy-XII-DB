import ast,hashlib,json,struct,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;P=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain');q=Path('Database/FFXII TZA/_index/candidates/sn1-q0-source-domain/logical_lines.py');sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (W/'upstream-control.json').exists();src=q.read_bytes();(W/'retained/fable-logical-producer-before.py').write_bytes(src)
tree=ast.parse(src.decode());nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cont' for t in n.targets)];assert len(nodes)==1
g={'BS':bytes([92])};exec(compile(ast.Module(body=nodes,type_ignores=[]),'unchanged FABLE cont assignment','exec'),g)
pg={'struct':struct};exec((P/'retained/selected-sbn-functions.py').read_text(),pg)
controls=[]
for m,indices in [('mapctrl',[976,1186]),('evctrl',None)]:
 s=(P/'retained'/(m+'.sbn')).read_bytes();o,end=pg['sbn_blocks'](s)[0];L,bs,starts,t=pg['sbn_group_read'](s,o)
 if indices is None:indices=[next(j for j,a in enumerate(starts) if s[a:s.index(b'\0',a,end)].decode('cp932').endswith('\\'))]
 for j in indices:
  a=starts[j];data=s[a:s.index(b'\0',a,end)];actual=g['cont'](data);expected=data.decode('cp932').rstrip(' \t\r\n').endswith('\\')
  controls.append(dict(module=m,physical_line=j+1,offset=a,bytes=data.hex(),decoded=data.decode('cp932'),original_producer_result=actual,decoded_terminal_ascii_result=expected,kind='positive-original-ASCII' if expected else 'negative-original-CP932-945C'))
assert sum(c['kind'].startswith('negative') and c['original_producer_result'] and not c['decoded_terminal_ascii_result'] for c in controls)==2 and any(c['kind'].startswith('positive') and c['original_producer_result'] for c in controls)
r=subprocess.run([sys.executable,str(q),str(P/'retained')],capture_output=True,text=True,timeout=30)
(W/'upstream-default.stdout').write_text(r.stdout);(W/'upstream-default.stderr').write_text(r.stderr)
assert r.returncode==0 and 'FAILS 0' in r.stdout
status=subprocess.check_output(['git','status','--short','--',q.as_posix()],text=True);publication=subprocess.check_output(['git','log','-1','--format=%H','--',q.as_posix()],text=True).strip()
out=dict(producer_path=q.as_posix(),producer_sha256=sha(src),producer_unchanged=q.read_bytes()==src,selected_unchanged_cont_assignment_sha256=sha(ast.unparse(ast.Module(body=nodes,type_ignores=[])).encode()),controls=controls,actual_default_invocation=dict(command=[sys.executable,str(q),str(P/'retained')],returncode=r.returncode,stdout_sha256=sha(r.stdout.encode()),stderr_sha256=sha(r.stderr.encode()),limits='Green original producer default is not semantic acceptance; it checks its raw-byte continuation expectations, while original CP932 negative controls fail them.'),git_status=status.strip(),latest_publication_commit=publication or None,limits='Working producer preimage, not assumed canonical publication/independent acceptance. No original compiler/VM/native/game execution. Owner repairs cont() and affected counts/source lookup/prose; do not edit peer source or regress canonical index.63 ev544 original positives unaffected.')
assert out['producer_unchanged'];(W/'upstream-control.json').write_text(json.dumps(out,indent=2)+'\n');print('UPSTREAM64 original positive seen; two actual CP932 negatives falsely classified; green default retained, publication identity explicit',flush=True)
