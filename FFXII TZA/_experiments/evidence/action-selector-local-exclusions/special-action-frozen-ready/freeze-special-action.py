"""Freeze already retained action evidence, checking every required producer input.

This verifies receipts and original bytes; it does not rerun the nine-pack census,
award independent acceptance, or infer natural reachability from candidate rows.
"""
import hashlib, json, pathlib, shutil, struct

W = pathlib.Path(__file__).resolve().parent
ROOT = W.parents[4]
F = W / 'special-action-frozen-ready'
if F.exists():
    raise ValueError('immutable destination already exists')

def sha(b): return hashlib.sha256(b).hexdigest()
def load(n): return json.loads((W/n).read_text())
def require(c, msg):
    if not c: raise ValueError(msg)

exe = (ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
esh = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
require(sha(exe) == esh, 'reference identity')
p = struct.unpack_from('<I', exe, 0x3c)[0]
optional = struct.unpack_from('<H', exe, p+20)[0]
sections = [struct.unpack_from('<IIII', exe, p+24+optional+40*i+8)
            for i in range(struct.unpack_from('<H', exe, p+6)[0])]
def read(va, n):
    for vs, sva, rs, ro in sections:
        if 0x120000+sva <= va and va+n <= 0x120000+sva+rs:
            return exe[ro+va-0x120000-sva:ro+va-0x120000-sva+n]
    raise ValueError('unbacked original range')

adapter = ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
ash = sha(adapter.read_bytes())
capture_sha = sha((W/'capture-index-path.py').read_bytes())
for n, driver in [('selector-callers-raw-01.json', 'selector-callers.py'),
                  ('special-loader-raw-01.json', 'capture-special-loader.py'),
                  ('special-admission-raw-01.json', 'capture-special-admission.py')]:
    r = load(n)
    require(r['exe_sha256'] == esh and r['adapter_sha256'] == ash, 'raw dependency identity')
    require(r['driver_sha256'] == capture_sha, 'capture module identity')
    key = 'selector_discovery_driver_sha256' if n.startswith('selector') else 'invocation_driver_sha256'
    require(r[key] == sha((W/driver).read_bytes()), 'actual invocation identity')
    require(len(r['controls']) == 3 and all(c['expected'] == c['observed'] for c in r['controls']),
            'missing/failed access-role prerequisites')
    require(bool(r['ranges']), 'missing ranges is not a valid empty result')
    for span in r['ranges']:
        a, b = int(span['start'],16), int(span['end_exclusive'],16)
        data = read(a,b-a)
        require(sha(data) == span['sha256'], 'range preimage')
        pc = a
        for ins in span['instructions']:
            require(int(ins['pc'],16) == pc, 'instruction continuity')
            chunk = bytes.fromhex(ins['bytes'])
            require(bool(chunk), 'empty instruction')
            pc += len(chunk)
        require(pc == b and b''.join(bytes.fromhex(i['bytes']) for i in span['instructions']) == data,
                'incomplete/or altered original-byte capture')

inventory = load('action-selectors-01/result.json')
require(inventory['driver_sha256'] == sha((W/'check-action-selectors.py').read_bytes()), 'inventory driver')
extractor = ROOT/'agent_flow/tools/vbfextract.py'
require(inventory['extractor_sha256'] == sha(extractor.read_bytes()), 'archive extractor identity')
require(len(inventory['results']) == 9 and len(inventory['controls']) == 4, 'incomplete nine-pack input/control corpus')
require(all(c.get('rejected') or c.get('rejected_invariant') for c in inventory['controls']), 'inventory controls')
for rec in inventory['results']:
    lang = rec['path'].split('/test_battle/')[1].split('/')[0]
    table = W/'action-selectors-01/tables'/('action_data_'+lang+'.st2e')
    require(sha(table.read_bytes()) == rec['table_sha256'], 'table identity')
    require(rec['retained_equals_archive'] and rec['count'] == 543 and rec['stride'] == 60, 'retained inventory prerequisite')
    require(not rec['non_sentinel_negative_rows'] and len(rec['sentinel_rows']) == 68, 'actual bounded invariant')

result = load('special-admission-result-01.json')
require(result['driver_sha256'] == sha((W/'check-special-admission.py').read_bytes()), 'reducer identity')
require(result['raw_sha256'] == sha((W/'special-admission-raw-01.json').read_bytes()), 'reducer raw binding')
require(result['action_receipt_sha256'] == sha((W/'action-selectors-01/result.json').read_bytes()), 'reducer inventory binding')
require(len(result['results']) == 9 and len(result['controls']) == 3, 'reducer corpus/controls')
require(all(not r['non_sentinel_negative'] and r['sentinel_with_bit30_ordinary'] == list(range(511,535))
            for r in result['results']), 'result scope differs')
require(result['controls'][0]['detected'] and result['controls'][1]['removed_all_candidates']
        and result['controls'][2]['rejected'], 'reducer controls failed')

F.mkdir()
(F/'.gitattributes').write_bytes(b'* -text\n')
names = ['SPECIAL-ACTION-RESULT.md','capture-index-path.py','selector-callers.py',
         'selector-callers-raw-01.json','capture-special-loader.py','special-loader-raw-01.json',
         'capture-special-admission.py','special-admission-raw-01.json',
         'check-action-selectors.py','check-special-admission.py','special-admission-result-01.json',
         'freeze-special-action.py']
for n in names: shutil.copyfile(W/n,F/n)
shutil.copytree(W/'action-selectors-01',F/'action-selectors-01')
(F/'dependencies').mkdir()
for source in (adapter, extractor): shutil.copyfile(source,F/'dependencies'/source.name)
(F/'README.md').write_text('''# OV42 special-action narrowing and local admission

Read SPECIAL-ACTION-RESULT.md for the proposition, hypotheses, method, source,
controls, implications, limits and next discriminator. This is original-code
and retained-data analysis, not original-code execution or game observation.

Reproduce the bounded semantic reducer in a fresh output path:

    python check-special-admission.py special-admission-raw-01.json action-selectors-01/result.json action-selectors-01/tables NEW_RESULT.json

The inventory producer records observed fields and counterexamples; that is a
data receipt, not universal semantic PASS. The actual semantic reducer refuses
missing packs/failed roles/changed tables and non-sentinel counterexamples.
The freeze checks its required upstream identities and complete original bytes.
The source captures can be repeated from their repo location with the pinned
EXE and central reviewed adapter; the inventory additionally needs the exact
retained packs/archive paths in its driver. Copies of dependency sources are
identity receipts, not an instruction to replace central repository tooling.

Procedure lessons: the earlier wrong known-positive PC25DAE1 was refused; the
actual call is25DAED. A whole306C3D fragment contained undecoded later bytes;
the accepted capture is only the complete prefix through306C56. Do not use it
as a full-CFG census. A failed prerequisite capture produced no caller result;
dependent reads must run only after its checked terminal success, not in a
shell chain that can hide the producer exit. No missing result is empty proof.

No new scientific sample credit is assigned for this freeze. Previously run
captures/reducer were terminal0; the freeze verifies the retained results now.
Independent SPEC review and FABLE/OPUS canonical consumption remain required.
Rows511..534 are local-predicate candidates only. All whole OV42/OV21 natural
reachability claims remain open. No live process or saves/config were touched.
''', encoding='utf8')
(F/'freeze-receipt.json').write_text(json.dumps(dict(
    mode='receipt and original-byte verification, not a new semantic experiment',
    reference_sha256=esh, original_ranges_checked=True, actual_driver_bindings_checked=True,
    adapter_sha256=ash, extractor_sha256=sha(extractor.read_bytes()),
    required_upstream_results_checked=True, no_process_or_save_config_access=True,
    whole_archive_sha256='not computed; exact selected entry/table identities retained',
    first_packet_unchanged=True, newly_closed_whole_runtime_questions=0),indent=2)+'\n')
members = [dict(path=x.relative_to(F).as_posix(),bytes=x.stat().st_size,sha256=sha(x.read_bytes()))
           for x in sorted(F.rglob('*')) if x.is_file()]
(F/'manifest.json').write_text(json.dumps(dict(
    status='PRODUCER_VALIDATED_PENDING_INDEPENDENT_REVIEW',
    limits='STATIC_ONLY; initialized row/codec premises; natural reachability OPEN',members=members),indent=2)+'\n')
for m in members: require(sha((F/m['path']).read_bytes()) == m['sha256'],'freeze changed')
print('Frozen',len(members),'members; original bytes and required producer bindings checked; whole RT closures0')
