"""Check retained receipts and links; do not repeat native restore/device I/O."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
P = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
W = P / 'run-01'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
source_pin = '033c37bd65cf4e9b5f33c94af14ad867877ac32cf992ad1515d4c230a6597dec'
def need(condition, why):
    if not condition:
        raise RuntimeError(why)
need(sha(P / 'generation.py') == source_pin, 'source identity')
git = read(P / 'source-git-receipt.json')
need(git['exit'] == 0 and git['terminal'] is True and git['sha256'] == source_pin and not (P / 'source-git.stderr').read_bytes() and sha(P / 'source-git.stdout') == source_pin, 'Git extraction prerequisite')
pre = read(W / 'preconditions.json')
need(pre['source_sha256'] == source_pin and pre['driver_sha256'] == sha(P / 'probe.py'), 'pre-execution producer pins')
outer = read(P / 'invoke-01.json')
need(outer['terminal'] is True and outer['exit'] == 1 and outer['exception'] is None and outer['driver_sha256'] == sha(P / 'probe.py') and not (P / 'invoke-01.stderr').read_bytes(), 'probe completed with explicit semantic reject')
result = read(W / 'result.json')
need(result['verdict'] == 'REJECT_DOCUMENTED_DEVICE_CLASS' and result['controls_valid'] is True and len(result['records']) == 5, 'complete scoped result')
need(len(result['checks']) == 10 and [k for k, v in result['checks'].items() if v is not True] == ['superscript_devices_encoded_and_refused'], 'no hidden control failure')
stdout = (P / 'invoke-01.stdout').read_text().strip()
need(json.loads(stdout)['verdict'] == result['verdict'], 'outer result linkage')
receipts = []
for label, expected_exit in [('original', 0), ('percent-distinct', 0), ('case-pair', 1), ('unverified', 1), ('trailing-period', 0), ('nonempty', 1), ('trailing-output', 1)]:
    receipt = read(W / (label + '.receipt.json'))
    need(receipt['terminal'] is True and receipt['exception'] is None and receipt['exit'] == expected_exit, 'upstream CLI result: ' + label)
    out = (W / (label + '.stdout')).read_bytes()
    err = (W / (label + '.stderr')).read_bytes()
    need(out and not err and receipt['stdout'] == out.decode('utf-8', 'replace') and receipt['stderr'] == '', 'CLI raw output link: ' + label)
    need((b'RESTORED' if expected_exit == 0 else b'REFUSED') in out, 'CLI distinguishing output: ' + label)
    receipts.append({'case': label, 'exit': expected_exit, 'stdout_sha256': hashlib.sha256(out).hexdigest(), 'receipt_sha256': sha(W / (label + '.receipt.json'))})
for record in result['records']:
    need(record['run'] == read(W / (record['case'] + '.receipt.json')), 'normalized run linkage')
    if record['run']['exit'] == 0:
        need(record['zip_member_count'] == len(record['comparisons']) == 35 and all(c['equal'] is True for c in record['comparisons']) and record['reader_problems'] == [], 'complete byte comparison')
    else:
        need(record['target_exists'] is False and record['current'] is False, 'prewrite refusal observation')
devices = read(W / 'device-functions.json')
need(devices == result['device_functions'] and devices['no_device_path_opened'] is True and len(devices['documented_superscript_cases']) == 12, 'actual pure function observations')
need(all(c['mapped'] == c['name'] and c['reason'] is None for c in devices['documented_superscript_cases']), 'documented counterexample retained')
cleanup = read(W / 'cleanup.json')
clean_outer = read(P / 'cleanup-invoke-01.json')
need(clean_outer['exit'] == 0 and clean_outer['terminal'] is True and clean_outer['exception'] is None and clean_outer['driver_sha256'] == sha(P / 'cleanup.py') and not (P / 'cleanup-invoke-01.stderr').read_bytes(), 'cleanup invocation prerequisite')
need(cleanup['all_disposables_absent'] and cleanup['all_input_archives_unchanged'] and cleanup['exact_source_unchanged'] and len(cleanup['records']) == 6 and all(r['absent_after'] for r in cleanup['records']), 'cleanup/restoration receipt')
qualified = read(W / 'input-qualification.json')
need(len(qualified['inputs']) == 6 and all(x['external_required'] for x in qualified['inputs']), 'raw input dependencies explicitly external')
print(json.dumps({'status': 'CHECK_RECEIPTS_VALID_SCOPED_REJECT', 'native_cli_receipts': receipts, 'restored_member_counts': [len(r['comparisons']) for r in result['records'] if 'comparisons' in r], 'reserved_device_calls': 12, 'source_sha256': source_pin, 'semantic_verdict': result['verdict'], 'limits': 'Retained receipt consistency and artifact identity; no new native restore, no fresh physical alias measurement, no device I/O or game execution.'}, indent=2))
