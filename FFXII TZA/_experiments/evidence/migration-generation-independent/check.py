import argparse, hashlib, json, zipfile
from pathlib import Path
W=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=W/'run-01/raw.json');ap.add_argument('--out',type=Path,default=W/'result.json');a=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads(a.raw.read_text());assert r['finished'] is True and r['source_restored'] is True
assert r['driver_sha256']==sha(W/'capture.py') and r['worker_sha256']==sha(W/'interrupt-worker.py')
src=W/'run-01/generation.py';data=src.read_bytes();assert sha(src)==r['source_sha256']
assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['source_blob']
prior=json.loads((W/'run-01/retained-raw.json').read_text());assert sha(W/'run-01/retained-raw.json')==r['retained']['raw_sha256']
assert r['retained']['source_sha256']==r['source_sha256']
reuse={'missing-output-failed-build-preserves-current','strict-input-mid-build-rejected','volatile-change-coherent-commit','warm-output-tamper-rejected','snapshot-tamper-no-fallback'}
assert {c['name'] for c in r['retained']['cases']}==reuse
assert r['retained']['cases']==[c for c in prior['cases'] if c['name'] in reuse] and all(c['passed'] for c in r['retained']['cases'])
names={'required-missing','default-empty','schema-allowed-empty','schema-malformed-nonempty','interrupt-before-rename','interrupt-after-rename','cli-positive-export','refresh-during-export','mixed-zip','duplicate-zip-member','unknown-format-zip','malformed-manifest-zip','added-output-membership'}
cs={c['name']:c['observed'] for c in r['cases']};assert len(cs)==len(r['cases'])==13 and set(cs)==names
def cli(c,rc,word=None):
 assert c['terminal'] is True and c['returncode']==rc
 if word:assert c['stdout'].startswith(word) and not c['stderr']
for name in ('required-missing','default-empty','schema-malformed-nonempty'):
 c=cs[name];assert c['error']['type']=='GenerationError' and c['new'] is None and c['pointer_unchanged'] and c['history_unchanged']
 assert c['failure']['current_unchanged']==c['old'];cli(c['cli'],0,'STALE')
assert cs['required-missing']['state']['state']=='missing'
assert cs['default-empty']['state']['state']=='empty' and cs['default-empty']['state']['size']==0
assert cs['schema-malformed-nonempty']['state']['state']=='present' and cs['schema-malformed-nonempty']['schema_error'].startswith('JSONDecodeError')
c=cs['schema-allowed-empty'];assert c['error'] is None and c['new']!=c['old'] and c['state']['state']=='empty' and c['state']['size']==0
assert not c['pointer_unchanged'] and not c['history_unchanged'];cli(c['cli'],0,'CURRENT')
assert len(r['owned_process_cleanup'])==2
for c in r['owned_process_cleanup']:assert c['terminal'] is True and c['returncode']!=0 and c['pid']==c['gate']['pid'] and c['no_child_launch']
for stage in ('before-rename','after-rename'):
 c=cs['interrupt-'+stage];assert c['gate']['stage']==stage and c['owned_pid']==c['gate']['pid']
 assert c['partial_at_gate']==(stage=='before-rename') and c['final_at_gate']==(stage=='after-rename')
 assert c['pointer_unchanged'] and c['history_unchanged'];cli(c['cli'],0,'CURRENT');assert c['old'] in c['cli']['stdout']
c=cs['cli-positive-export'];[cli(v,0,{'status':'CURRENT','verify':'CURRENT','export':'EXPORTED','zip':'VERIFIED'}[k]) for k,v in c['cli'].items()]
c=cs['refresh-during-export'];assert c['returncode']==0 and not c['stderr'] and c['stdout'].startswith('EXPORTED') and len(c['event'])==1
assert c['event'][0]['after_member']=='MANIFEST.json' and c['current']==c['event'][0]['new_current']!=c['old']
assert c['export_generation']==c['old'] and c['view']=={'sentinel':'OLD'};cli(c['cli'],0,'VERIFIED')
with zipfile.ZipFile(W/'run-01/export/refresh.zip') as z:assert json.loads(z.read('MANIFEST.json'))['generation']==c['old'] and json.loads(z.read('outputs/view.json'))==c['view']
for name in ('mixed-zip','duplicate-zip-member','unknown-format-zip','malformed-manifest-zip'):
 c=cs[name];p=W/'run-01/export'/c['archive'];assert sha(p)==c['sha256']
 with zipfile.ZipFile(p) as z:
  assert z.namelist()==c['member_names']
  entries=[{'name':i.filename,'sha256':hashlib.sha256(z.read(i)).hexdigest()} for i in z.infolist()]
  assert entries==c['entries']
c=cs['mixed-zip'];assert c['label']=='UNVERIFIED' and c['info']['hash_mismatch']==['outputs/view.json'] and c['exception'] is None;cli(c['cli'],1,'UNVERIFIED')
c=cs['duplicate-zip-member'];assert c['member_names'].count('outputs/view.json')==2
hashes=[e['sha256'] for e in c['entries'] if e['name']=='outputs/view.json'];assert len(set(hashes))==2
assert c['label']=='VERIFIED' and c['info']['members']==3 and len(c['entries'])==4;cli(c['cli'],0,'VERIFIED')
c=cs['unknown-format-zip'];assert c['label']=='VERIFIED';cli(c['cli'],0,'VERIFIED')
with zipfile.ZipFile(W/'run-01/export'/c['archive']) as z:assert json.loads(z.read('MANIFEST.json'))['format']=='ff12-generation-unknown'
c=cs['malformed-manifest-zip'];assert c['label'] is None and c['exception']['type']=='JSONDecodeError';cli(c['cli'],1);assert not c['cli']['stdout'] and 'JSONDecodeError' in c['cli']['stderr']
c=cs['added-output-membership'];assert any('uncited.json' in x for x in c['problems']);cli(c['cli'],1,'INVALID')
result={'verdict':'REJECT','scope':'generation.py library/CLI archive certification; positive publication/input/export boundaries retained separately',
 'source_tree_commit':r['source_tree_commit'],'source_last_commit':r['source_last_commit'],'source_sha256':r['source_sha256'],
 'raw_sha256':sha(a.raw),'new_cases':13,'retained_cases':sorted(reuse),'retained_credit':'Five previously executed observations at51660c616, exact identical source; not fresh tests or whole historical package acceptance',
 'defects':['Duplicate different-content ZIP entries for outputs/view.json collapse to one name and certify VERIFIED/members3 despite4 physical entries','Unknown manifest format is VERIFIED by ZIP path although folder reader limits readable formats','Malformed manifest raises JSONDecodeError/CLIexit1 without promised UNVERIFIED label; refusal works, certification does not'],
 'cause':'verify_zip uses a set of names plus name-based last-entry reads, never validates readable format, and catches unreadable archive errors but not malformed manifest parse/shape',
 'established':'Missing/defaultzero/schema-rejected input cannot replace old CURRENT; explicit allow_empty succeeds. Interrupted original pre-CURRENT boundaries before/after directory rename preserve old pointer/history and CLI-valid old generation. Labelled export refresh commits NEW while actual original main export produces coherent OLD ZIP. Mixed bytes and extra output membership refused.',
 'cleanup':'Both owned single-process base-Python interruption workers terminated/reaped through retained handles; no descendants launched on inspected path. No production/game changes. Earlier unrelated transition descendant cleanup remains unverified.',
 'limits':'MethodA Python tool fixtures, not original FF12 instructions/live/parity. Pause/writes are labelled interventions, not natural crash or arbitrary timing proof. Nonempty JSON schema checked by local parser and passed via validated; library does not independently infer schema. No real reporter/export adoption, host cancellation, completeM1/M0-M5/fullL1L2 award. Cryptographic hashes bind bytes, not unsupported manifest meaning.',
 'next':'OPUS cause repair ZIP membership/format/structuredrefusal; preserve valid inputs/export/interruption behavior. Re-request review at finalsource, only changed discriminators repeat. DATA owns actual reporter integration. Existing request lacks reviews metadata: route one explicit repair after verified publication, no inferred automatic repair.'}
if a.out.exists():assert json.loads(a.out.read_text())==result,'Preserve existing result'
else:a.out.write_text(json.dumps(result,indent=2)+'\n')
print('REJECT_GENERATION_ARCHIVE_CERTIFICATION',flush=True)
