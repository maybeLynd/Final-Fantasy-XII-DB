#!/usr/bin/env python3
"""Reproduce Section 07 in isolated native child processes (Linux x86-64, GCC).

No game, Windows loader, external download or historical experiment is launched.
The supplied executable is read-only. Native code maps private copies of its bytes.
The output directory must be new; all compiled files live in a temporary directory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
VARIANTS = {
    'skip_payload_copy':'mover_preserves_full_payload',
    'skip_slot_generation':'mover_updates_generation_pair',
    'wrong_movement_inhibit_mask':'member_with_inhibit_bit_is_not_moved',
    'skip_context_repair':'original_refresh_reads_actual_moved_slot',
    'admit_child_eleven':'rejected_index_does_not_refresh',
    'zero_requests_refresh':'zero_child_index_returns_success',
    'retain_old_request_index':'later_request_replaces_not_appends',
    'keep_delivered_pending_bit':'stale_full_ticket_retires_pending_bit',
    'skip_combined_container_base':'combined_first_container_rebased',
    'skip_movement_latch':'mover_marks_compaction_change',
}

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def original_ranges(raw: bytes, manifest: dict) -> list[dict]:
    pe = struct.unpack_from('<I', raw, 0x3C)[0]
    if raw[pe:pe+4] != b'PE\0\0':
        raise ValueError('Invalid PE signature')
    opt = pe + 24
    if struct.unpack_from('<H', raw, pe+4)[0] != 0x8664 or struct.unpack_from('<H', raw, opt)[0] != 0x20B:
        raise ValueError('Requires PE32+ AMD64')
    base = struct.unpack_from('<Q', raw, opt+24)[0]
    tab = opt + struct.unpack_from('<H', raw, pe+20)[0]
    sections = []
    for i in range(struct.unpack_from('<H', raw, pe+6)[0]):
        _, va, size, disk = struct.unpack_from('<4I', raw, tab+i*40+8)
        sections.append((base+va, size, disk))
    checks = []
    for item in manifest['functions']:
        chunks = []
        for r in item['ranges']:
            start, end = int(r['start'],16), int(r['end'],16)
            if end < start or end-start+1 != r['bytes']:
                raise ValueError('Malformed body range')
            for va, size, disk in sections:
                if va <= start and end < va+size:
                    chunks.append(raw[disk+start-va:disk+end-va+1]); break
            else:
                raise ValueError(f'Range outside file-backed section: {r}')
        body = b''.join(chunks)
        if len(body) != item['bytes'] or sha(body) != item['sha256']:
            raise ValueError(f'Original body mismatch: {item["entry"]}')
        checks.append({'entry':item['entry'],'bytes':len(body),'sha256':sha(body),'pass':True,'scope':item['scope']})
    return checks

def validate_cases(rec: dict, expected_count: int | None = None) -> list[str]:
    cases = rec['cases']
    names = [x['name'] for x in cases]
    if not cases or len(names) != len(set(names)) or rec['checks'] != len(cases):
        raise ValueError('Empty, duplicate, or miscounted cases')
    bad = [x['name'] for x in cases if x['pass'] is not True]
    if rec['failures'] != len(bad):
        raise ValueError('Failure counter inconsistent')
    if expected_count is not None and len(cases) != expected_count:
        raise ValueError(f'Expected {expected_count} assertions, got {len(cases)}')
    for x in cases:
        if (x['actual'] == x['expected']) != x['pass']:
            raise ValueError('Assertion label disagrees with retained values')
    return bad

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    if platform.system() != 'Linux' or platform.machine() not in ('x86_64','AMD64'):
        raise ValueError('This is a Linux x86-64 fixture, not a Windows/game test')
    exe = args.exe.resolve(strict=True)
    out = args.output.resolve()
    if out.exists():
        raise ValueError('Output directory must not already exist')
    raw = exe.read_bytes()
    if sha(raw) != EXE_SHA:
        raise ValueError('Original executable identity mismatch')
    manifest = json.loads((HERE/'original_body_manifest.json').read_text())
    if manifest['exe_sha256'] != EXE_SHA:
        raise ValueError('Manifest image identity mismatch')
    body_checks = original_ranges(raw,manifest)
    gcc = shutil.which('gcc')
    if not gcc:
        raise ValueError('GCC is required; nothing will be downloaded')
    out.mkdir(parents=True)
    def save(name: str, value: object):
        (out/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    save('body_verification.json',{'functions':body_checks,'count':len(body_checks),'exe_sha256':EXE_SHA})
    mutations = []
    with tempfile.TemporaryDirectory(prefix='ff12-section07-') as td:
        binary = Path(td)/'native_controls'
        command = [gcc,'-std=c11','-O2','-Wall','-Wextra','-Werror','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        compiled = subprocess.run(command,capture_output=True,text=True,timeout=45)
        if compiled.returncode or compiled.stdout or compiled.stderr:
            raise ValueError('Compiler failed or emitted diagnostics: '+compiled.stderr)
        runs = []
        for filename in ['native_baseline.json','native_repeat.json']:
            run = subprocess.run([str(binary),str(exe)],capture_output=True,text=True,timeout=25)
            if run.returncode or run.stderr:
                raise ValueError(f'Native baseline failed ({run.returncode}): {run.stderr}')
            data = json.loads(run.stdout)
            if validate_cases(data,123):
                raise ValueError('Baseline assertion failed')
            save(filename,data); runs.append(data)
        if runs[0] != runs[1]:
            raise ValueError('Baseline repeat differs')
        for variant, expected in VARIANTS.items():
            run = subprocess.run([str(binary),str(exe),variant],capture_output=True,text=True,timeout=25)
            if run.returncode != 1 or run.stderr:
                raise ValueError(f'Wrong failure mechanism for {variant}: {run.returncode} {run.stderr}')
            data = json.loads(run.stdout)
            bad = validate_cases(data)
            if bad != [expected]:
                raise ValueError(f'Wrong discriminator for {variant}: {bad}')
            mutations.append({'variant':variant,'rejected':True,'exit_code':run.returncode,'required_failure':expected,'record':data})
        boundary_run = subprocess.run([str(binary),str(exe),'overlap-boundary'],capture_output=True,text=True,timeout=25)
        if boundary_run.returncode or boundary_run.stderr:
            raise ValueError('Overlap boundary not cleanly observed: '+boundary_run.stderr)
        boundary = json.loads(boundary_run.stdout)
        d,src,n = boundary['destination'],boundary['source'],boundary['length']
        if not (d < src < d+n and n == 0x400 and boundary['overlap'] is True
                and boundary['slot_published'] == 1 and boundary['old_source_freed'] == 1
                and boundary['evidence'] == 'stopped at original memcpy import before copying'):
            raise ValueError('Unexpected overlap-boundary receipt')
        save('overlap_import_boundary.json',boundary)
    if sha(exe.read_bytes()) != EXE_SHA:
        raise ValueError('Original executable changed')
    save('code_mutations.json',mutations)
    save('summary.json',{
        'section':'SECTION-07','production_status':'locally validated; formal peer acceptance pending',
        'exe_sha256':EXE_SHA,'selected_body_records':len(body_checks),
        'native_assertions':123,'native_passed':123,'repeat_identical':True,
        'code_variants':len(mutations),'variants_rejected':len(mutations),
        'evidence':'isolated original-instruction execution with synthetic data/arenas',
        'application_substitutions':['0017D2E0 diagnostic formatter: empty string, invocation counter, returns zero'],
        'import_bridges':['memset IAT008C2A60','memcpy IAT008C2A68','strncpy IAT008C2F70'],
        'explicit_execution_window':'0024D565..0024D6A9 with equivalent register/stack entry and a return barrier at0024D6AA; NOT whole0024D540',
        'overlap_boundary':'one actual selector/mover invocation stops before overlapping memcpy; no copied-data or post-move success claim',
        'environment':{'platform':platform.platform(),'python':sys.version,'gcc':subprocess.check_output([gcc,'--version'],text=True).splitlines()[0]},
        'source_sha256':sha((HERE/'native_controls.c').read_bytes()),
        'limitations':['No live FF12 process, Windows deployment, real IO/audio/GPU, or full-game concurrency.',
                       'Original mover/free/copy/reissue and allocator pressure run; backing maps are synthetic and arena release is not OS unmapping.',
                       'Specialized repair walkers have default/empty children; arbitrary payload branches are not certified.',
                       'Combined window skips five initial service calls and the post-window render path; it is not a whole-frame execution.',
                       'Synthetic container nodes are detached before destruction; their allocation/construction/destruction is not tested.',
                       'Overlapping copy control stops before the import; host memmove is not substituted for original Windows memcpy.',
                       'Maintenance/script scheduling and movement-latch consumers are inspected statically, not a new live timeline.',
                       'Only ten impacted private-image variants; no full historical or project mutation campaign.'],
        'original_exe_unchanged':True})
    print(json.dumps({'output':str(out),'native_assertions':123,'mutants_rejected':len(mutations),'body_records':len(body_checks),'status':'PASS'},indent=2))
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as exc:
        print('Section 07 reproduction failed: '+str(exc),file=sys.stderr)
        raise SystemExit(2)
