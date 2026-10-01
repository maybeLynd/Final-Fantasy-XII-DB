#!/usr/bin/env python3
"""Reproduce SECTION-02 in a matching merged database. Never writes the EXE or inputs.

Requires Linux x86-64, Python 3.10+, and GCC-compatible cc. No Unicorn/Capstone dependency.
Original instructions run in private mappings with explicit bridge functions. Not live FF12.
"""
from __future__ import annotations
import argparse, ast, copy, hashlib, json, os, platform, shutil, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUTANTS = {
    'omit_free_head_advance': 'take_moves_free_head_not_array_base',
    'remove_generation_increment': 'generation_and_slot_are_distinct',
    'constructor_clobber_unobserved': 'constructor_all_64_links_and_indices',
    'retire_clobber_payload': 'splice_does_not_zero_payload_or_state',
    'offset_round_up': 'offset_truncation_2047',
    'ignore_generation_on_cancel': 'cancel_rejects_stale_generation',
}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def verify_inputs(database: Path, manifest: dict) -> list[dict]:
    rows = []
    for item in manifest['inputs']:
        p = (database / item['path']).resolve()
        require(p.is_relative_to(database.resolve()), 'Unsafe input path')
        data = p.read_bytes()
        require(sha(data) == item['sha256'] and len(data) == item['bytes'], f"Input changed: {item['path']}")
        rows.append({'path': item['path'], 'sha256': sha(data), 'matched': True})
    return rows

def verify_original(raw: bytes, manifest: dict) -> dict:
    require(sha(raw) == manifest['exe_sha256'], 'Original EXE SHA-256 mismatch')
    rows = []
    for body in manifest['bodies']:
        joined = b''
        for region in body['ranges']:
            start = region['file_offset']; size = region['bytes']
            block = raw[start:start+size]
            require(len(block) == size and sha(block) == region['sha256'], f"Original range mismatch: {region['start']}")
            joined += block
        require(sha(joined) == body['sha256'], f"Body mismatch: {body['entry']}")
        rows.append({'entry': body['entry'], 'bytes': len(joined), 'sha256': sha(joined), 'matched': True})
    for extra in manifest['extra_data']:
        block = raw[extra['file_offset']:extra['file_offset']+extra['size']]
        require(sha(block) == extra['sha256'], 'Dispatch-table mismatch')
    return {'method': 'Byte verification using supplied historical body extents; not a fresh Ghidra import', 'exe_sha256': sha(raw), 'bodies': rows, 'extra_data_matched': len(manifest['extra_data'])}

def retained_review(database: Path) -> dict:
    folder = database / '_experiments/evidence/queue-remaining-exec'
    tree = ast.parse((folder/'check.py').read_text(encoding='utf-8'))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'check')
    # Only this previously inspected, pinned function is evaluated. Producer main/emulator is not run.
    scope = {'SLOT0': 0x22C31C0, 'slot': lambda i: 0x22C31C0 + 0x80*i}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(folder/'check.py'), 'exec'), scope)
    check = scope['check']
    results = json.loads((folder/'result.json').read_text())['cases']
    replay = []
    for name, record in results.items():
        ok, failures = check(name, {}, record)
        require(ok, f'Retained assertion fails: {name}: {failures}')
        replay.append({'name': name, 'pass': ok, 'failures': failures})
    mutations = []
    for label, name, corrupt in [
        ('wrong_free_head', 'req-basic', lambda r: r['cells'].__setitem__('free_h', 0x22C31C0)),
        ('wrong_generation_id', 'req-second', lambda r: r.__setitem__('ret', 0x41)),
        ('lost_recycle_id', 'cycle-request-pump-retire', lambda r: r['slot0'].__setitem__('d64', 0)),
        ('missing_stall_flag', 'stall-then-request', lambda r: r.__setitem__('trace', [x for x in r['trace'] if x != 'flag'])),
    ]:
        bad = copy.deepcopy(results[name]); corrupt(bad)
        ok, why = check(name, {}, bad)
        require(not ok, f'Corrupted-record control escaped: {label}')
        mutations.append({'name': label, 'case': name, 'detected': True, 'reasons': why})
    vacuous = []
    for name in ['e040-loader1', 'e040-loader2']:
        changed = copy.deepcopy(results[name]); changed['trace'] = []
        ok, why = check(name, {}, changed)
        require(ok, 'Historical-check limitation changed; inspect rather than treating as a pass')
        vacuous.append({'case': name, 'empty_trace_is_accepted_by_historical_check': True})
    return {'method': 'Replay of the pinned retained assertion function only; no Unicorn producer execution', 'cases': replay, 'negative_controls': mutations, 'known_assertion_gaps': vacuous, 'lifecycle_observation': results['cycle-request-pump-retire']['slot0'], 'scope': '22 historical branches return pass, including two with no positive assertion; the new native controls independently test both loader predicates.'}

def run_native(binary: Path, exe: Path, out: Path, name: str, mutant: str | None = None) -> tuple[dict, int]:
    env = dict(os.environ); env.pop('FF12_QUEUE_MUTANT', None)
    if mutant:
        env['FF12_QUEUE_MUTANT'] = mutant
    result = subprocess.run([str(binary), str(exe)], capture_output=True, text=True, timeout=30, env=env)
    require(bool(result.stdout.strip()), f'Native fixture produced no JSON ({name}): {result.stderr}')
    parsed = json.loads(result.stdout)
    dump(out / (name + '.json'), parsed)
    require(not result.stderr.strip(), f'Native fixture stderr ({name}): {result.stderr}')
    return parsed, result.returncode

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--database', type=Path, default=HERE.parents[2])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cc', default='gcc')
    args = parser.parse_args()
    require(platform.system() == 'Linux' and platform.machine().lower() in ('x86_64', 'amd64'), 'Native fixture requires Linux x86-64; Windows live execution is not substituted.')
    require(shutil.which(args.cc) is not None, 'GCC-compatible compiler missing')
    exe = args.exe.resolve(); database = args.database.resolve(); out = args.output.resolve()
    require(not out.exists() or not any(out.iterdir()), 'Refusing to overwrite a nonempty result directory')
    out.mkdir(parents=True, exist_ok=True)
    inputs = json.loads((HERE/'input_manifest.json').read_text())
    body_manifest = json.loads((HERE/'original_body_manifest.json').read_text())
    pinned = verify_inputs(database, inputs)
    dump(out/'body_verification.json', verify_original(exe.read_bytes(), body_manifest))
    retained = retained_review(database); dump(out/'retained_review.json', retained)
    with tempfile.TemporaryDirectory(prefix='ff12-queue-section02-') as tmp:
        binary = Path(tmp)/'native_controls'
        cmd = [args.cc, '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror', '-fPIE', '-pie', str(HERE/'native_controls.c'), '-o', str(binary)]
        compiled = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        require(compiled.returncode == 0 and not compiled.stderr.strip(), f'Compile failed/warned: {compiled.stderr}')
        baseline, rc = run_native(binary, exe, out, 'baseline')
        require(rc == 0 and baseline['checks'] == 72 and baseline['failures'] == 0, 'Original baseline did not pass all 72 checks')
        repeat, rc = run_native(binary, exe, out, 'repeat')
        require(rc == 0 and baseline == repeat, 'Repeat differed after normalizing the host callback address')
        mutants = []
        for mutant, expected_failure in MUTANTS.items():
            data, rc = run_native(binary, exe, out, 'mutant_' + mutant, mutant)
            failed = [x['name'] for x in data['cases'] if not x['pass']]
            require(rc == 1 and failed == [expected_failure], f'Mutant did not fail the intended assertion: {mutant}: {failed}')
            mutants.append({'mutant': mutant, 'detected': True, 'failed_assertion': expected_failure, 'exit': rc})
    dump(out/'mutation_results.json', mutants)
    require(verify_inputs(database, inputs) == pinned, 'A retained input changed')
    require(sha(exe.read_bytes()) == body_manifest['exe_sha256'], 'Original EXE changed')
    summary = {'section': 'SECTION-02', 'status': 'PASS bounded local production checks; formal peer acceptance pending', 'original_bodies_verified': len(body_manifest['bodies']), 'native_checks': 72, 'native_failures': 0, 'repeat_identical': True, 'host_callback_address_normalization': 'Native code asserts actual callback pointer equality; only last_return display normalizes that host-ASLR address to0.', 'code_mutants_detected': len(mutants), 'retained_assertion_branches': len(retained['cases']), 'historical_branches_without_positive_loader_assertion': 2, 'retained_record_negative_controls': len(retained['negative_controls']), 'inputs_unchanged': pinned, 'not_performed': ['live FF12 run', 'full original Unicorn campaigns', 'fresh current-GN Ghidra import', 'independent T2/terminal acceptance', 'complete underlying I/O service or callback implementation']}
    dump(out/'summary.json', summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('inputs_unchanged',)}, indent=2))

if __name__ == '__main__':
    main()
