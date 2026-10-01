from pathlib import Path
import json
W=Path(__file__).resolve().parent;R=W/'run-02';raw=json.loads((R/'raw.json').read_text());assert raw['verdict']=='INVALID';(R/'outer-driver-before-run.py').write_bytes((W/'run.py').read_bytes())
s=(W/'capture.py').read_text();assert s==(R/'driver-before-run.py').read_text();s=s.replace("R=W/'run-02'","R=W/'run-03'")
needle="C=json.loads((W/'run-01/raw.json').read_text())['source_commit'];raw="
helper="""def validate_verifier(q,gid,man):
 expected='CURRENT %s committed %s; %d outputs; sources unchanged\\n'%(gid,man['committed_at'],len(man['outputs']))
 assert q.returncode==0 and not q.stderr and q.stdout==expected,('VERIFIER_PREREQUISITE',q.returncode,q.stdout,q.stderr,expected)
 return dict(argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True)
"""
assert needle in s;s=s.replace(needle,helper+needle)
old="assert q.returncode==0 and q.stdout.startswith('CURRENT '+gid+' committed ') and q.stdout.strip().endswith('no input drift') and not q.stderr,(q.returncode,q.stdout,q.stderr)"
assert old in s;s=s.replace(old,"raw.setdefault('prerequisite_verifications',[]).append(dict(argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True));validate_verifier(q,gid,man)")
old="assert q.returncode==0 and not q.stderr and q.stdout.startswith('CURRENT '+gid+' committed ') and q.stdout.strip().endswith('no input drift');made.append"
assert old in s;s=s.replace(old,"raw.setdefault('prerequisite_verifications',[]).append(dict(argv=q.args,returncode=q.returncode,stdout=q.stdout,stderr=q.stderr,terminal=True));validate_verifier(q,gid,man);made.append")
s=s.replace(" raw['preparation_failure']=", " raw['second_preparation_failure']={'raw_sha256':sha((W/'run-02/raw.json').read_bytes()),'terminal_sha256':sha((W/'capture-terminal-02.json').read_bytes()),'limit':'INVALID guessed unchanged-source wording; now exact original CLI format read and receipt recorded before assertion'}\n raw['preparation_failure']=")
assert 'no input drift' not in s;(W/'capture.py').write_text(s)
q=(W/'run.py').read_text().replace("f=W/'capture-terminal-02.json'", "f=W/'capture-terminal-03.json'");(W/'run.py').write_text(q)
print('EXACT_SOURCE_BOUND_VERIFIER_PRECONDITION; TWO_INVALID_ATTEMPTS_RETAINED')
