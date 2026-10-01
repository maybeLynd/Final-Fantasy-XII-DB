import argparse,hashlib,json,zipfile
from pathlib import Path
W=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=W/'run-01/raw.json');ap.add_argument('--out',type=Path);a=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads(a.raw.read_text());assert r['finished'] is True and r['source_restored'] is True
assert sha(W/'capture.py')==r['driver_sha256'];src=W/'run-01/generation.py';b=src.read_bytes();assert sha(src)==r['source_sha256']
assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['source_blob']
assert sha(W/'run-01/retained-manifest.json')==r['retained_manifest_sha256']
idx={x['path']:x for x in json.loads((W/'run-01/retained-manifest.json').read_text())['members']}
want={'positive','duplicate-zip-member','unknown-format-zip','malformed-manifest-zip','array-manifest','wrong-output-shape','typed-input-state','unknown-input-state','malformed-folder'}
cs={c['name']:c for c in r['cases']};assert len(cs)==len(r['cases'])==9 and set(cs)==want
assert len(r['owned_cli_processes'])==9
for c in r['cases']:
 q=c['cli'];assert q in r['owned_cli_processes'] and q['terminal'] is True and not q['stderr'] and c['exception'] is None
 if c['name']=='malformed-folder':
  assert c['object'] is None and any('not JSON' in p for p in c['problems']) and q['returncode']==1 and q['stdout'].startswith('INVALID ')
  continue
 p=W/'run-01'/c['archive'];assert sha(p)==c['sha256']
 with zipfile.ZipFile(p) as z:assert [{'name':i.filename,'sha256':hashlib.sha256(z.read(i)).hexdigest()} for i in z.infolist()]==c['entries']
 expected='VERIFIED' if c['name'] in ('positive','unknown-input-state') else 'UNVERIFIED'
 assert c['label']==expected and q['stdout'].startswith(expected+' ') and q['returncode']==(0 if expected=='VERIFIED' else 1)
 if c['name'] in ('positive','duplicate-zip-member','unknown-format-zip','malformed-manifest-zip'):assert c['sha256']==idx['run-01/export/'+c['archive']]['sha256']
assert 'duplicate member names' in cs['duplicate-zip-member']['info']['reason'] and cs['duplicate-zip-member']['info']['entries']==4
assert cs['unknown-format-zip']['info']['reason'].startswith('UNSUPPORTED')
assert 'not JSON' in cs['malformed-manifest-zip']['info']['reason']
assert 'not an object' in cs['array-manifest']['info']['reason'] and 'outputs is not an object' in cs['wrong-output-shape']['info']['reason']
assert 'carries no state' in cs['typed-input-state']['info']['reason']
with zipfile.ZipFile(W/'run-01/positive.zip') as z:base=json.loads(z.read('MANIFEST.json'));base_names=set(z.namelist())
with zipfile.ZipFile(W/'run-01/unknown-input-state.zip') as z:bad=json.loads(z.read('MANIFEST.json'));bad_names=set(z.namelist())
assert bad['format']==base['format'] and bad['outputs']==base['outputs'] and bad['generation']==base['generation']
keys=[k for k in base['inputs'] if base['inputs'][k]!=bad['inputs'][k]];assert len(keys)==1
k=keys[0];old=base['inputs'][k];new=bad['inputs'][k];assert old['state']=='present' and not old.get('external')
assert new['state']=='ASTRA_LABELLED_UNKNOWN_STATE' and {x:v for x,v in new.items() if x!='state'}=={x:v for x,v in old.items() if x!='state'}
assert base_names-bad_names=={'inputs/'+k} and not bad_names-base_names
assert 'Each declared input is `present`' in b.decode() and '`missing` or `unsupported`' in b.decode()
assert cs['unknown-input-state']['info']['members']==cs['positive']['info']['members']-1
result={'verdict':'REJECT','scope':'Exact repaired archive/folder admission f145d442f; original defects fixed, remaining unknown input-state semantic omission',
 'source_commit':r['commit'],'source_sha256':r['source_sha256'],'raw_sha256':sha(a.raw),
 'fixed':'Original retained duplicate4entries, unknownformat and malformedJSON now UNVERIFIED/library+CLIexit1/no traceback; malformedarray/outputshape/nonstringstate refused; copied folder malformedJSON reported None/problems and CLIINVALID/exit1.',
 'defect':'Known-format manifest with one present nonexternal input changed to ASTRA_LABELLED_UNKNOWN_STATE and that snapshot removed is VERIFIED/library+CLIexit0 with one fewer member; all other state metadata/output bytes preserved.',
 'cause':'parse_manifest validates state string type but not the documented present/empty/missing/unsupported vocabulary; both reader membership branches only include present/empty snapshots, so an unknown string silently loses its snapshot obligation.',
 'control':'Unmodified retained valid ZIP VERIFIED; typed nonstring state refused; exact old fixtures bound to original97c4c1b65 manifest. All9 actual CLI invocations terminal/no stderr, library no exception.',
 'limits':'Labelled manually modified private manifest/archive, not normal Store output, authentication of builder origin, deployed reporter integration, FF12 instructions/live or completeM1/M0-M5/fullL1L2. Prior settled export/interruption/input campaigns not repeated. Scoped fixes preserved; unsupported known optional state is not automatically a defect. Earlier transition descendant cleanup not established.',
 'cleanup':'Private copies only; no controller/productionstore/board/game/save/config/reference writes in capture. Actual main args exclude self-test child branch; original inspected verify-zip/status path starts no children and subprocess handles terminal. No timeout accepted.',
 'next':'OPUS enforce supported state vocabulary on shared parser and affected current certification consumers; preserve fixedformat/duplicate/JSON and validknown states. Re-review changed discriminator at exact finalsource; own evidence review separate.'}
if a.out:
 if a.out.exists():assert json.loads(a.out.read_text())==result,'Immutable result'
 else:a.out.write_text(json.dumps(result,indent=2)+'\n')
print('REJECT_UNRECOGNIZED_INPUT_STATE_SCOPED_REPAIRS_PRESERVED',flush=True)
