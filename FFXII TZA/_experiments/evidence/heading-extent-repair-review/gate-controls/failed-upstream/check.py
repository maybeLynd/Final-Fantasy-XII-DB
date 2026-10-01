"""Retained original H8 repair review; producer reports and process status separate."""
import hashlib,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(root):
 t=json.loads((root/'capture-terminal.json').read_bytes())
 if '--fault-upstream-failed' in sys.argv:t['returncode']=1
 assert t['terminal'] is True and t['returncode']==0 and not t['stderr'] and t['stdout'].strip()=='ORIGINAL_H8_AND_FIRST_FRAGMENT_INPUT_STATUS_CAPTURED','Required capture incomplete/failed'
 assert t['driver_sha256']==sha(root/'capture.py')
 ident=json.loads((root/'identity.json').read_bytes());assert ident==json.loads((root/'identity-before.json').read_bytes())
 assert ident['driver_sha256']==t['driver_sha256'] and ident['wrapper_sha256']==sha(root/'h8-input-intervention.py')
 assert ident['exe']['sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 for x in ident['sources']:assert sha(root/'retained'/x['copy'])==x['sha256']
 assert sha(root/'retained/producer-879652c93.py')==ident['producer_commit']['sha256']
 assert (root/'retained/producer-source.py').read_bytes().replace(b'\r\n',b'\n')==(root/'retained/producer-879652c93.py').read_bytes().replace(b'\r\n',b'\n')
 receipts=json.loads((root/'producer-terminal.json').read_bytes());assert [x['case'] for x in receipts]==['original','first-fragment-catalogue']
 assert all(x['terminal'] is True and x['producer_sha256']==sha(root/'retained/producer-source.py') and not x['stderr'] for x in receipts)
 original,negative=receipts
 assert original['returncode']==0 and re.search(r'^SURVIVES  H8  ',original['stdout'],re.M) and original['stdout'].endswith('FAILS 0\n')
 assert negative['returncode']==0 and re.search(r'^BROKEN    H8  ',negative['stdout'],re.M) and negative['stdout'].endswith('FAILS 1\n'),'First-fragment must be reported BROKEN, actual CLI status retained'
 assert negative['wrapper_sha256']==ident['wrapper_sha256']
 raw=json.loads((root/'raw.json').read_bytes());assert raw['original_sources_unchanged'] is True and raw['exe_unchanged'] is True
 assert raw['sizes']==[40,27,397,45,93,144,47,170] and sum(raw['sizes'])==963 and raw['roots']==['0x2e45e0']*8
 assert raw['return_pcs']==['0x2e49a2'] and raw['first_fragment_return_pcs']==[] and len(raw['call_pcs'])==21
 body=(root/'retained/intervening-body963.bin').read_bytes();rows=raw['instructions']
 assert len(body)==963 and b''.join(bytes.fromhex(x['bytes']) for x in rows)==body
 assert rows==json.loads((root/'retained/prior-intervening-body.json').read_bytes())['instructions']
 m=json.loads((root/'catalogue-intervention.json').read_bytes());p=m['original_line'].split('\t');q=m['replacement_line'].split('\t')
 assert p[:3]==['002E45E0','Movement_UpdateSteeringTowardTarget','963'] and q[:3]==['002E45E0','Movement_UpdateSteeringTowardTarget','40'] and p[:2]+p[3:]==q[:2]+q[3:]
 text=(root/'retained/functions.tsv').read_text('utf-8');changed=text.replace(m['original_line'],m['replacement_line']);assert text.count(m['original_line'])==1
 assert hashlib.sha256(text.encode()).hexdigest()==m['full_decoded_original_sha256'] and hashlib.sha256(changed.encode()).hexdigest()==m['full_decoded_mutant_sha256']
 page=(root/'retained/contract.md').read_text('utf-8');active=re.sub(r'~~.*?~~','',page,flags=re.S);section=active.split('## 14. Unresolved')[1].split('## 15. Evidence')[0]
 assert '- [ ] Whether any caller depends' in section and 'REOPENED, narrowed' in section and '963 B, eight chained unwind fragments' in section and 'neither is "the refusal never executes"' in section
 assert 'so the class cannot change in between' not in active and '**The refusal never executes in shipped code' not in active
 if '--fault-cli-refused' in sys.argv:assert negative['returncode']!=0,'BROKEN H8/FAILS1 still exits0; exit-only consumers cannot use this as a fail-closed guard'
 if '--fault-first-fragment-accepted' in sys.argv:assert 'SURVIVES  H8' in negative['stdout'],'H8 text refuses truncated catalogue40B'
 if '--fault-refusal-closed' in sys.argv:assert '- [x] Whether any caller depends' in section,'Canonical item is OPEN; class effects/refusal reachability not proved'
 return {'verdict':'ACCEPT scoped semantic repair / H8 textual truncation refusal; CLI failure-status gap retained','reference':'879652c93; exact raw source/current consumer and certified EXE plus retained2ada8a5a0 code/unwind evidence','extent':{'fragments':raw['sizes'],'bytes':963,'call_sites':21,'ret':'002E49A2'},'control':{'original':'SURVIVES H8 / FAILS0 / exit0','first_fragment_catalogue':'BROKEN H8 / FAILS1 / exit0','intervention':'single catalogue size963->40 through io.open; producer code/reference unchanged'},'semantic':'Current section14/15 correctly reopen class stability/refusal; source extent and same-actor caller bounds agree. H8 predicate detects40B catalogue reading. No gameplay/native execution or new sole-edge census.','producer_limit':'Negative process exits0 despite BROKEN/FAILS1. Checked result is required; no actual downstream false PASS demonstrated or existing stdout-aware prerequisite disproved. OPUS owns status/procedure decision.','limits':'No H0-H7 re-adjudication, whole call effects, actual class mutation/stability, live refusal reachability or all malformed-chain validation. Two producer Python runs; retained bytes reused, not two game experiments. Non-author ASTRA checker/gate review remains separate.'}
if __name__=='__main__':print(json.dumps(check(W),indent=2))
