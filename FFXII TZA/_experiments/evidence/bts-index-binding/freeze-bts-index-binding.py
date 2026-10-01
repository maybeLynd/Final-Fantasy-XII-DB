"""Freeze focused test-zone mapping and actual invocation history, never reseal a publication."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'bts-index-binding-frozen-ready-02'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'bts-index-binding-result-03.json').read_text());c=json.loads((W/'bts-index-binding-controls-01/result.json').read_text())
for tag,d,key in [('bts-index-binding-capture-02','capture-bts-index-binding.py','driver_sha256'),('bts-index-binding-positive-03','prove-bts-index-binding.py','checker_sha256'),('bts-index-binding-controls-run-01','control-bts-index-binding.py','driver_sha256')]:
 st=json.loads((W/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get(key)!=sha(W/d) or not (W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale '+tag)
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-bts-index-binding.py') or r.get('helper_sha256')!=sha(W/'prove-title-queue-consumption.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_BTS_BINDING_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c.get('checker_sha256')!=r['checker_sha256'] or c.get('positive_reused',{}).get('sha256')!=sha(W/'bts-index-binding-result-03.json'):raise ValueError('controls incomplete/stale')
if any(x.get('exit')==0 or x.get('expected_error_seen') is not True or x.get('result_absent') is not True for x in c['refusals']):raise ValueError('concrete refusal failed')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('required input moved')
# The shared publisher's source-annotation qualifier accepts instruction JSON,
# not binary data. Derive its narrow input map from the checked full result;
# all primary binaries remain required by the reducer, freezer and manifest.
annotation_map=W/'bts-index-binding-annotation-prerequisite-01.json'
source_pins=[x for x in r['source_pins'] if x['path']=='bts-index-binding-source-02.json']
if len(source_pins)!=1:raise ValueError('missing exact instruction source')
annotation_map.open('x').write(json.dumps(dict(producer_complete=True,source_pins=source_pins,
 result_sha256=sha(W/'bts-index-binding-result-03.json'),data_prerequisites=r['source_pins'][1:],
 limits='Projection for existing source-annotation publisher qualifier only; primary binary identities checked separately by actual reducer/freezer, no binary access-role annotation'),indent=2)+'\n')
paths={x['path'] for x in pins}|{'bts-index-binding-annotation-prerequisite-01.json','bts-index-binding-method-01.json','bts-index-binding-result-02.json','bts-index-binding-result-03.json','prove-bts-index-binding.py','control-bts-index-binding.py','freeze-bts-index-binding.py','capture-bts-index-binding-before-inline-data-fix-01.py','prove-bts-index-binding-before-uk-control-fix-01.py','prove-bts-index-binding-before-primary-pin-fix-02.py','index-domain-result-01.json','index-path-raw-02.json'}
paths|={tag+s for tag in ['bts-index-binding-capture-01','bts-index-binding-positive-01','bts-index-binding-positive-02','bts-index-binding-positive-03','bts-index-binding-controls-run-01'] for s in ['.status.json','.stdout','.stderr']}
paths|={p.relative_to(W).as_posix() for p in (W/'bts-index-binding-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/bts-index-binding/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md'];units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('native explicit path budget exceeded')
if any(not(W/p).is_file() for p in paths):raise ValueError('required file missing')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
 p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Shipped test-zone indices do not select the empty reward ARDs

Method A: original instructions and primary/retained authored data. Producer
valid, independent acceptance and canonical incorporation pending. Exact EXE
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
image base120000. No game, native/emulated execution or repeated script census.

The competing explanations for GR18's31 bts_* zones were populated/empty ARD
selection versus missing resource entries. Both original namespace26 NMB arrays
name the same31 zones at the same numeric area indices. Both primary MRF images
(sha7c63552f, full bytes retained) map those areas to31 distinct field rows.
Original264ED0 reads unsignedWORD row+4, not group+6;3EA6E0 forwards it to3EA820
when changed or forced. NMB naming is metadata, not proof of script execution.

At those area indices both literal namespace21 arrays have NULL at2*area and
2*area+1. They do not select any of the four known empty-table ARDs. At the
corresponding field IDs all ten literal namespace5 alternatives have NULL at
3*field+0,+1,+2. The twelve retained shipping FSTs have-1 in all those slots.
This is bounded exact-data absence with detection controls, not hours of no hits.
The detailed join and original bytes are in source02 and result03; no integer
address or directory-name shortcut stands in for the original lookup identity.

All pointer arrays pass nonnull ttl_a pointer/string controls. Every FST has
positive asp_a ARD size224. Eleven title-script entries are positive; UK's is
-1 and is preserved as such. Missing table entries are different from a bound
reward descriptor with count0. They do not establish a normally running bts
script, a live storage pointer, current initialization or a lifetime guarantee.

Manager0's retained original32FCA0 branch computes namespace5/base3*selector.
It later calls330310 or3306E0 for the primary carrier. Their whole admission,
runtime size overrides, aliases, alternate selectors, copied/embedded bodies,
other writers and pending callbacks remain explicit next discriminators. Do not
claim universal bts unreachability or whole GR18 E1 closure from this join.

Reproduce the reducer with the existing analysis Python and a fresh output:

    python <packet>/prove-bts-index-binding.py <fresh.json>

The actual capture uses the reviewed access-role adapter with store, LEA and
read/modify/write controls; reducer redecodes annotations and pins full EXE,
raw arrays, primary file identity, normal pdata entries and finite switch targets.
Four actual CLI refusals reuse result03: failed upstream capture, coherent
getter word+6 substitution, missing focused index, and altered MRF with a
coherently rewritten local hash. No missing/failed evidence passes as empty.
These are producer controls, distinct from independent semantic acceptance.

Failure history is immutable: capture01exit1/no output because the original
pdata extent includes inline switch data afterRET. Capture02 separates the
2831-byte code from NOP/eleven RVA words. Positive01exit1/no result exposed the
false universal title-size control; corrected02 preserves UK-1 and positive
asp_a controls. Result03 adds independent complete primary identity pins;02
and prior drivers remain history. No conclusion relies on a failed invocation.
Do not decode inline switch bytes as instructions or manufacture a title positive.

FABLE consumes the numeric GR18 residual; OPUS distinguishes missing resource
entries from empty bound reward tables. Independent SPEC review is required;
canonical peer pages are unchanged. One scoped numeric observation question is
answered offline; zero whole GR18/OV rows newly closed. Natural reachability stays
open, and an archive directory alone does not prove game availability.

Player version: the shipped test-area names exist, but their ordinary lookup
slots supply neither the battle file nor the map script. They do not point at
the four empty reward areas. We are checking whether another loading route can
use those scripts before deciding that gameplay evidence is necessary.

Cleanup: finite file reads/private copies only; no PC/game/input/instrument/
save/config/reference or peer-process mutation. Full L1+L2 goalACTIVE/NOT_MET;
parked menu allowance persists and EXP127 remains invalid. Review waits affect
these claims only; original primary-carrier analysis continues independently.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native units',units,'manifest',sha(out/'manifest.json'))
