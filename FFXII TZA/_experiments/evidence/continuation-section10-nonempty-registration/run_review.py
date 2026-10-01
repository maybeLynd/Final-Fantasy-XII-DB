#!/usr/bin/env python3
"""Reproduce Section 10 in isolated native child processes (Linux x86-64, GCC).

No game, Windows loader, real IO, external download or historical experiment is launched.
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
VARIANTS = {r['variant']:r['required_failure'] for r in json.loads((HERE/'variant_plan.json').read_text())}

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
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if platform.system()!='Linux' or platform.machine() not in ('x86_64','AMD64'):
        raise ValueError('Requires Linux x86-64; this is not a Windows/game test')
    exe=args.exe.resolve(strict=True);out=args.output.resolve()
    if out.exists():raise ValueError('Output must be a new directory')
    raw=exe.read_bytes()
    if sha(raw)!=EXE_SHA:raise ValueError('Original image identity mismatch')
    manifest=json.loads((HERE/'original_body_manifest.json').read_text())
    if manifest['exe_sha256']!=EXE_SHA:raise ValueError('Manifest image mismatch')
    body_checks=original_ranges(raw,manifest)
    data_items=[dict(entry=x['start'],scope=x['meaning'],bytes=x['bytes'],sha256=x['sha256'],ranges=[dict(start=x['start'],end=f"{int(x['start'],16)+x['bytes']-1:08X}",bytes=x['bytes'])]) for x in manifest['data_spans']]
    data_checks=original_ranges(raw,{'functions':data_items})
    gcc=shutil.which('gcc')
    if not gcc:raise ValueError('GCC is required; nothing is downloaded')
    out.mkdir(parents=True)
    def save(n,v):(out/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    save('body_verification.json',dict(functions=body_checks,count=len(body_checks),data_spans=data_checks,data_count=len(data_checks),exe_sha256=EXE_SHA))
    controls=[]
    with tempfile.TemporaryDirectory(prefix='ff12-section10-') as td:
        binary=Path(td)/'native_controls'
        cmd=[gcc,'-std=c11','-O2','-Wall','-Wextra','-Werror','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        c=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
        if c.returncode or c.stdout or c.stderr:raise ValueError('Compiler failed or emitted diagnostics: '+c.stderr)
        records=[]
        for name in ('native_baseline.json','native_repeat.json'):
            x=subprocess.run([str(binary),str(exe)],capture_output=True,text=True,timeout=25)
            if x.returncode or x.stderr:raise ValueError(f'Baseline failed {x.returncode}: {x.stderr}')
            rec=json.loads(x.stdout)
            if validate_cases(rec,159):raise ValueError('Baseline assertion failed')
            save(name,rec);records.append(rec)
        if records[0]!=records[1]:raise ValueError('Repeated baseline differs')
        for name,expected in VARIANTS.items():
            x=subprocess.run([str(binary),str(exe),name],capture_output=True,text=True,timeout=25)
            if x.returncode!=1 or x.stderr:raise ValueError(f'Wrong mutation failure for {name}: {x.returncode} {x.stderr}')
            rec=json.loads(x.stdout);bad=validate_cases(rec)
            if bad!=[expected]:raise ValueError(f'Wrong discriminator for {name}: {bad}')
            controls.append(dict(variant=name,rejected=True,required_failure=expected,record=rec))
    if sha(exe.read_bytes())!=EXE_SHA:raise ValueError('Original EXE changed')
    save('code_mutations.json',controls)
    save('summary.json',dict(section='SECTION-10',status='locally validated; formal independent acceptance pending',
        native_assertions=159,native_passed=159,repeat_identical=True,mutants_rejected=len(controls),selected_body_records=len(body_checks),data_spans_verified=len(data_checks),
        exe_sha256=EXE_SHA,original_exe_unchanged=True,source_sha256=sha((HERE/'native_controls.c').read_bytes()),
        application_substitutions=['0017D2E0 diagnostic formatter: empty output and counter'],
        import_bridges=['008C2A60 memset','008C2A68 memcpy: nonoverlapping only','008C2F70 bounded strncpy'],
        scope='Original PRF0/1 normalization and lookup, full nonempty registration, A00 subtype0 nonzero embedded-pointer relocation, original compactor/refresh and teardown with synthetic data.',
        limitations=['No live FF12, OS IO, fresh Ghidra, Windows overlap-copy result or graphics output.',
        'Only A00 subtype0 payload fixups are newly exercised; no promise for every PRF asset/subtype or real authored-data reachability.',
        'Synthetic metadata/config selects a no-config-string branch. Optional .cm lookup, strstr/scanf, and priority override are not executed.',
        'Known selected original function hashes are not whole-function or branch coverage counts.',
        'Bad signatures, missing names, no free ticket, repeated mutated source and wrap cases establish scoped preconditions, not observed game failures.',
        'No TEAM/L2/global score/history or reconstruction changes. New semantic production needs independent review.'],
        environment=dict(python=sys.version,platform=platform.platform(),gcc=subprocess.check_output([gcc,'--version'],text=True).splitlines()[0])))
    print(json.dumps(dict(status='PASS',assertions=159,mutants=len(controls),body_records=len(body_checks),output=str(out)),indent=2))
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as exc:
        print('Section 10 reproduction failed: '+str(exc),file=sys.stderr);raise SystemExit(2)
