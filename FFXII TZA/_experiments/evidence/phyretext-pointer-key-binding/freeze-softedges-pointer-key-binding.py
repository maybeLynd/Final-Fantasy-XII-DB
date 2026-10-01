"""Freeze the conditional packed-key question; no acceptance or live award."""
import hashlib,json,pathlib,shutil
W=pathlib.Path(__file__).resolve().parent;out=W/'softedges-pointer-key-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda z:hashlib.sha256(z).hexdigest()
r=json.loads((W/'softedges-pointer-key-binding-result-03.json').read_text());c=json.loads((W/'softedges-pointer-key-controls-01/result.json').read_text())
if r.get('producer_complete') is not True or r['checker_sha256']!=sha((W/'reduce-softedges-pointer-key-binding.py').read_bytes()):raise ValueError('unchecked final reduction')
if c['status']!='PASS_PRODUCER_CONTROLS' or c['reducer_sha256']!=r['checker_sha256'] or len(c['checks'])!=2 or any(x['status']!='PASS_REFUSED' for x in c['checks']):raise ValueError('incomplete invocation controls')
names=[x['path'] for x in r['source_pins']]+[
 'capture-index-path.py','capture-softedges-mapping-builders.py','capture-softedges-array-terminal-guard.py',
 'capture-softedges-array-terminal-guard-slot-assumption-01.py','softedges-array-terminal-guard-failure-01.json',
 'softedges-loader-parent-code-01.json','reduce-softedges-pointer-key-binding.py','reduce-softedges-pointer-key-binding-first-pass-01.py',
 'reduce-softedges-pointer-key-binding-source-option-02.py','reduce-softedges-pointer-key-binding-register-assumption-01.py',
 'softedges-pointer-key-binding-failure-01.json','softedges-pointer-key-binding-result-01.json','softedges-pointer-key-binding-result-02.json',
 'softedges-pointer-key-binding-result-03.json','control-softedges-pointer-key-binding.py','freeze-softedges-pointer-key-binding.py',
 'softedges-resource-source-01/phyretext.fx.phyre']
for x in r['source_pins']:
 if sha((W/x['path']).read_bytes())!=x['sha256']:raise ValueError('source moved')
out.mkdir()
for n in names:
 p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
shutil.copytree(W/'softedges-pointer-key-controls-01',out/'softedges-pointer-key-controls-01')
(out/'.gitattributes').write_text('* -text\n** -text\n')
(out/'README.md').write_text('''# PhyreText pointer keys: conditional elements-member resolution

Method A original bytes + retained data. Producer checked, independent pending.
No game session, original-code execution, archive recapture or class census.

Player version: the file divides its shader definitions into eleven adjustable
settings and one World transform. Original loader source tells us which array
member those two references request, under matching unchanged metadata. It
does not establish that loading succeeded or that the resulting memory stays alive.

QUESTION/HYPOTHESES: do packed keys22/27 recurse into m_els or stop at another
member? Does optional query result1 allow or prevent kind2 recursion? These are
native lookup/guard questions distinguishable from retained original source.
Actual loaded-resource binding, pointer identity and lifetime are separate.

REFERENCE: EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. Retained shaderf67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf.
Source captures execute the reviewed access-role adapter with actual store/LEA/RMW
controls. No raw Capstone access flags bypass that policy.

DEPENDENCIES: field-extent5bbbe5528, immutable manifest edc46fa5f7f4488bf7f65a91f527af97feed376104c822cef1bf5190a6938f76,
supplies the decoded retained pointer table. Reducer verifies that whole manifest
identity and the table receipt's member hash, rather than trusting a moving report.
Its independent review remains separate. Prior member-boundaries7a524fda9 proves
conditional callback ABI/status/normal stores; its acceptance remains separate
too. Reproduce this reduction with both canonical packets present in the repository.
These dependency claims are not credited as new tests or independent acceptance.

ORIGINAL BRIDGE:

- File class13 PEffectVariant has packed arrays18/23, width5, type_ref30. File
class17 PArray<PShaderParameterDefinition> has m_els at4,width1,type_ref56.
With13 primitive types, those references select class17 and class43 respectively.
59B430 constructs the actual mapped-member child link at59B93C from that class
reference calculation. The link is not simply assumed null.
- Both native array-member slot8 getters are16D680, original488BC1C3: return self.
632A10 stores its argument7 at member+5C. Outer registered arrays pass3 at5E48C6/
5E4951 and offsets40/50; inner m_els passes2 at5EED9A. Correct native mappings and
unchanged normally constructed metadata are explicit premises, not observed state.
- Original59EC40 permits outer kind3 recursion with these file flags. Residual
22-18 or27-23 becomes4; the supplied native object becomes the array address
object+zext32(nativeOffset+arrayF4-effectVariantF4), modulo64. F4 stays symbolic.
The inner kind2 member has bit6 clear, so59EC40 returnsNULL.59BED0 then returns
the current m_els record at59C0DB. It does not descend into definition fields.
- Retained pointer tuples(80000016,0,0,12,0,11,-1) and
(8000001B,0,11,12,0,1,-1) supply count11 and1 to the59CD25 assignment call.
This requests first11 definition objects and object11, the World singleton.
Prior published setter proof establishes only normal source/count association,
not element copying/lifetime.59CD14 can write a destination slot before the
callback: this reduction is not a complete effect inventory or unchanged-array claim.

CORRECTION: the existing loader prose says optional-query result==1 fails.
Exact59ECD7..59ED0D shows it permits kind2 recursion when the query is invoked;
other results stop. Bit1 always stops, bit6 clear stops kind2 without that query.
The tested shader's relevant bits1/6 are clear, so no opaque query effect is needed
for this conditional route. The general polarity is an original branch proof,
not a claim of natural values or execution frequency.

PRECONDITIONS/LIMITS: native class/member/type matches including59BFAF equality;
registrations return normally; metadata/getters/kinds unchanged; correct bound
list12 objects; assignment site reached and normal continuation after any opaque
old-storage cleanup. This is not successful unmodified initialization, live
membership, pointer stability, destination alias exclusion, whole constructor
AE0 survival, normal command/action reachability or wholeOV42 closure.

CONTROLS/FAILURES: initial getter capture expected an outer null getter and exited1
before creating any capture; its exact driver/no-result/actual slot diagnostic
are retained. Both getters were then verified as self. Initial reducer expected
R14 for the count; exact59CD07 readsR12+14, so it refused before result creation.
Original driver/receipt are retained; repaired path checks the actual instruction.
Two concrete subprocess regressions refuse a missing guard source and the same
wrong-register normalization, even while the underlying bytes are unchanged.
Producer checks are not native runs, external audit executions or acceptance.
Historical01/02 results/drivers are preserved; final03 pins the published table
generation. No failed result was promoted and no source/result was overwritten.

Reproduce from repository root, with fresh output:

    python <packet>/reduce-softedges-pointer-key-binding.py <fresh-result.json>

The canonical packet is at the same root depth as the work carrier; published
dependencies are read by pinned identity. Optional second argument selects a
disposable source directory for concrete refusal controls; reference inputs remain
unchanged. Use result03 for review, not preparation checkpoints or failed attempts.

CONSUMERS: independent SPEC review of this new conditional bridge/polarity, then
FABLE's OV42/reflection/asset-loader owning pages. Retain previous field/member
acceptance dependencies and route OPUS-owned contract changes. No peer page edited.
All own producer/reducer/test processes terminated; no @runtime/PC/game/save/
config/reference writes. Menu stays parked, EXP127 invalid, full goal ACTIVE/NOT_MET.
''',encoding='utf8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A',members=members),indent=2)+'\n')
print('Frozen conditional bridge; payload',len(members),'manifest',sha((out/'manifest.json').read_bytes()))
