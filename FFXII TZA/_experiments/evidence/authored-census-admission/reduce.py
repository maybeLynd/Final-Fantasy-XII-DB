"""Deterministic acceptance boundary for the actual research-tool fixtures."""
import hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=Path(sys.argv[1])
if out.exists():raise RuntimeError('immutable reduction exists')
ret=json.loads((P/'retention-01.json').read_text())
if ret.get('complete') is not True or ret['exit']!=0 or ret['sha256']!=sha(P/'script_verb_census.py'):raise RuntimeError('unmodified committed collector missing')
rows=[]
for label,exitcode,returned,failed,count in [('all-readable',0,['fixture/a.ebp','fixture/b.ebp'],[],2),('one-extraction-fails',0,['fixture/a.ebp'],['fixture/b.ebp'],1),('all-extractions-fail',1,[],['fixture/a.ebp','fixture/b.ebp'],0)]:
 q=P/'cases'/label;s=json.loads((q/'status.json').read_text());e=json.loads((q/'fixture-effects.json').read_text());cfg=json.loads((q/'case.json').read_text())
 if s.get('terminal') is not True or s.get('exit')!=exitcode or s.get('exception') is not None or s['driver_sha256']!=sha(P/'fixture_entry.py') or e['wrapper_sha256']!=sha(P/'fixture_entry.py'):raise RuntimeError('actual fixture invocation incomplete/changed')
 if e['attempted']!=['fixture/a.ebp','fixture/b.ebp'] or e['returned']!=returned or e['failed']!=failed:raise RuntimeError('extraction detection/positive controls disagree')
 if cfg['collector_sha256']!=ret['sha256'] or sha(q/'Database/Tools/analysis-kit/gfz-scripts/script_verb_census.py')!=ret['sha256'] or e['collector_sha256']!=ret['sha256']:raise RuntimeError('not the unmodified actual collector')
 stdout=(q/'stdout').read_text();stderr=(q/'stderr').read_text();table=q/'calls.tsv'
 if count:
  if stderr or 'CALL-family sites decoded: '+str(count) not in stdout or not table.is_file():raise RuntimeError('positive CLI output/control missing')
  lines=table.read_text().splitlines()
  if len(lines)!=count+1 or not lines[0].startswith('file\tscript\tpc\tverb\t'):raise RuntimeError('actual output table incomplete')
  verbs=[l.split('\t')[3] for l in lines[1:]]
  if verbs!=(['0x29A','0x29B'] if count==2 else ['0x29A']):raise RuntimeError('selected verb detection differs')
 else:
  if table.exists() or 'REFUSE: control failed - no CALL-family site decoded' not in stderr:raise RuntimeError('all-failed zero-case did not refuse')
 rows.append(dict(case=label,exit=exitcode,attempted=e['attempted'],failed=e['failed'],reported_CALL_count=count,
  stderr_empty=not bool(stderr),output_table_rows=count,limits=e['limits']))
z=dict(complete=True,verdict='REJECT_STANDALONE_CORPUS_COMPLETENESS_INFERENCE',driver_sha256=sha(Path(__file__)),collector_sha256=ret['sha256'],fixture_sha256=sha(P/'fixture_entry.py'),observations=rows,
 conclusion='Actual unmodified collector accepts one positive sibling while another read_entry raises: CLI0, stderr empty, selected29B absent, no failure/completeness field. All-failed control CLI1 proves its globalzero guard, not per-input admission.',
 scope='Independent research-tool failure-handling control; synthetic archive/index/extractor/decoder and names/reference arguments. Not original FF12 code execution, actual shipped callsites, bytecode decoder correctness, real VBF read failure or natural gameplay.',
 affected_claim='Nonzero all-CALL count alone cannot establish all selected/corpus inputs decoded, nor support universal absence of29B. Positive real captures are not automatically retracted; completeness consumers need separate coverage/error evidence.',
 repair_owner='OPUS helper/contract; DATA selected authored-flow capture must account read/parse/decode/unresolved states. No peer helper modified and no competing partition repair.',
 acceptance='After owner fix, actual invocation must either refuse/mark INCOMPLETE for failed input when completeness is requested, or explicitly label partial positive-only results and withhold absence inference; retain fully readable positive and all-failed controls.')
with out.open('x') as f:json.dump(z,f,indent=2)
print(z['verdict'],'three actual host fixtures; no FF12/corpus run')
