#!/usr/bin/env python3
"""Reproduce SECTION-01 controls without Unicorn or a live game.

Requires Python 3.10+, Linux x86-64, and a GCC-compatible C compiler. Run only
against the specified original executable. The child process maps private copies
of its instructions; the executable on disk is never modified. This program
executes the two pinned producer assertion functions against retained JSON, not
those producers' emulator programs. It does not certify T2 or L2 acceptance.
"""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
MUTANTS = {
    'skip_direct_dword_copy': 'copy_without_any_status_mask',
    'suppress_applier_dirty_flag': 'no_effect_status_sink_still_sets_tail_refresh',
    'wrong_tracked_base': 'tracked_real_base_EC1380_not_E81380',
    'omit_mode_failure_bit_clear': 'install_mode2_clears_bit26_not42',
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf8')


def body_receipts(exe: Path) -> list[dict]:
    raw = exe.read_bytes()
    if raw[:2] != b'MZ':
        raise ValueError('Not a PE image')
    pe, = struct.unpack_from('<I', raw, 0x3c)
    if raw[pe:pe+4] != b'PE\0\0':
        raise ValueError('Missing PE signature')
    nsections, = struct.unpack_from('<H', raw, pe+6)
    opt_len, = struct.unpack_from('<H', raw, pe+20)
    opt = pe+24
    magic, = struct.unpack_from('<H', raw, opt)
    base, = struct.unpack_from('<Q', raw, opt+24)
    if magic != 0x20b or base != 0x120000:
        raise ValueError('Unexpected image ABI/base')
    sections = []
    for i in range(nsections):
        h = opt + opt_len + 40*i
        va, size, ptr = struct.unpack_from('<III', raw, h+12)
        sections.append((va, size, ptr))
    receipts = []
    for row in json.loads((HERE/'original_body_manifest.json').read_text()):
        start, end = int(row['start'],16), int(row['end'],16)
        count = end-start+1
        rva = start-base
        segment = next(((va,size,ptr) for va,size,ptr in sections
                        if va <= rva and rva+count <= va+size), None)
        if segment is None:
            raise ValueError(f"Unbacked body: {row['entry']}")
        va, size, ptr = segment
        body = raw[ptr+rva-va:ptr+rva-va+count]
        got = hashlib.sha256(body).hexdigest()
        if len(body) != row['size'] or got != row['sha256']:
            raise ValueError(f"Original bytes differ: {row['entry']}")
        receipts.append({'entry':row['entry'],'bytes':count,'sha256':got,'match':True})
    return receipts


def pinned_assertions(script: Path) -> tuple[dict, object]:
    tree = ast.parse(script.read_text(encoding='utf-8-sig'), filename=str(script))
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CASES' for t in node.targets):
            nodes.append(node)
        elif isinstance(node,ast.FunctionDef) and node.name=='check':
            nodes.append(node)
    if len(nodes) != 2:
        raise ValueError(f'Unexpected pinned assertion structure: {script}')
    scope: dict = {}
    # Deliberately omit imports, world construction and emulator execution.
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(script),'exec'),scope)
    return scope['CASES'], scope['check']


def retained_review(root: Path, manifest: dict) -> dict:
    checked = []
    for row in manifest['retained_inputs']:
        p=root/row['path']
        if not p.is_file() or sha(p)!=row['sha256']:
            raise ValueError(f"Retained input differs/missing: {row['path']}")
        checked.append({'path':row['path'],'sha256':row['sha256'],'match':True})
    groups=[]
    corruptions=[]
    for folder in ('apply-result-callees-exec','apply-result-whole-exec'):
        d=root/'_experiments/evidence'/folder
        cases, check=pinned_assertions(d/'check.py')
        report=json.loads((d/'result.json').read_text())
        if set(cases)!=set(report['results']):
            raise ValueError(f'CASE/result population differs: {folder}')
        rows=[]
        for name,c in cases.items():
            ok, errors=check(name,copy.deepcopy(c),copy.deepcopy(report['results'][name]))
            rows.append({'case':name,'assertions_pass':bool(ok),'failures':errors})
        if not all(r['assertions_pass'] for r in rows):
            raise ValueError(f'Retained assertion failed: {folder}')
        groups.append({'package':folder,'method':'pinned assertions applied to retained records; NO emulator re-execution','cases':len(rows),'results':rows})
        picks=[('fld-p0-m0-set', ('bit',)), ('rc-null', ('faults',))] if folder.startswith('apply-result-callees') else [('ap-copythrough',('tgt','dbc')),('ap-dmg',('tgt','hp'))]
        for name, keys in picks:
            changed=copy.deepcopy(report['results'][name]); cur=changed
            for key in keys[:-1]: cur=cur[key]
            key=keys[-1]
            cur[key]=[] if key=='faults' else cur[key]^1
            ok, errors=check(name,copy.deepcopy(cases[name]),changed)
            if ok:
                raise ValueError(f'Corrupted retained record was accepted: {folder}/{name}')
            corruptions.append({'package':folder,'case':name,'changed_path':'.'.join(keys),'rejected':True,'failures':errors})
    p=root/'_experiments/evidence/battle-unit-construct-exec/result.json'
    d=json.loads(p.read_text())
    # Its check(name,c,world,output) depends on a constructed world. No replay is claimed.
    integrity=(d['cases']==39 and d['pass']==39 and d['fail']==0 and d['ok'] is True
               and len(d['results'])==39 and all(v.get('ok') is True for v in d['results'].values()))
    if not integrity: raise ValueError('EXP-150 retained record integrity differs')
    return {'retained_input_hashes':checked,'assertion_replay_total':sum(g['cases'] for g in groups),
            'groups':groups,'corrupted_record_controls':corruptions,
            'EXP150':{'records':39,'reported_pass':39,'structure_consistent':integrity,
                      'case_names':list(d['results']), 'method':'retained record integrity only; NOT assertion replay or emulator execution',
                      'known_limits':['wrong tracked-table observation address','nondiscriminating bit42 assertion','nested/original boundary limitations remain in review']}}


def execute(binary: Path, exe: Path, mutant: str | None = None) -> tuple[int,dict]:
    env=dict(os.environ)
    env.pop('FF12_CONTROL_MUTANT',None)
    if mutant: env['FF12_CONTROL_MUTANT']=mutant
    proc=subprocess.run([str(binary),str(exe)],capture_output=True,text=True,env=env,timeout=30)
    if proc.returncode not in (0,1):
        raise RuntimeError(f'Native fixture failed with code {proc.returncode}: {proc.stderr}')
    try: data=json.loads(proc.stdout)
    except json.JSONDecodeError as exc: raise RuntimeError(f'Invalid native output: {proc.stderr}') from exc
    if data.get('total')!=42 or len(data.get('cases',[]))!=42:
        raise RuntimeError('Native case population changed')
    actual=sum(not c['pass'] for c in data['cases'])
    if actual!=data['failures'] or (proc.returncode==0)!=(actual==0):
        raise RuntimeError('Inconsistent native exit/result')
    return proc.returncode, data


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe',type=Path,required=True)
    ap.add_argument('--database',type=Path,default=HERE.parents[2])
    ap.add_argument('--output',type=Path,required=True,help='Use a fresh results directory; existing reports are not overwritten.')
    ap.add_argument('--cc',default='cc')
    args=ap.parse_args()
    exe=args.exe.resolve(); root=args.database.resolve(); out=args.output.resolve()
    manifest=json.loads((HERE/'input_manifest.json').read_text())
    if sha(exe)!=manifest['exe_sha256']:
        raise ValueError('Wrong executable SHA256; no execution attempted')
    if platform.system()!='Linux' or platform.machine().lower() not in ('x86_64','amd64'):
        raise RuntimeError('Native fixture requires Linux x86-64; no Windows/live-game run is implied')
    cc=shutil.which(args.cc)
    if cc is None: raise RuntimeError('No GCC-compatible C compiler found')
    out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()): raise ValueError('Output directory must be empty')
    bodies=body_receipts(exe)
    retained=retained_review(root,manifest)
    save(out/'body_verification.json',bodies);save(out/'retained_review.json',retained)
    mutations=[]
    with tempfile.TemporaryDirectory(prefix='ff12_section01_') as td:
        binary=Path(td)/'native_controls'
        cmd=[cc,'-std=c11','-O1','-Wall','-Wextra','-Werror','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        compile_result=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
        if compile_result.returncode: raise RuntimeError(compile_result.stderr)
        code,a=execute(binary,exe)
        if code: raise RuntimeError('Original baseline failed')
        code,b=execute(binary,exe)
        if code or a!=b: raise RuntimeError('Baseline repeat differs or fails')
        save(out/'native_results.json',a);save(out/'native_repeat_results.json',b)
        for mutant, expected_case in MUTANTS.items():
            code,data=execute(binary,exe,mutant)
            failed=[c['name'] for c in data['cases'] if not c['pass']]
            if code!=1 or expected_case not in failed:
                raise RuntimeError(f'Mutant was not rejected by its intended control: {mutant}')
            save(out/f'mutant_{mutant}.json',data)
            mutations.append({'mutant':mutant,'expected_sensitive_case':expected_case,'detected':True,'failed_cases':failed})
    save(out/'mutation_results.json',mutations)
    # Recheck that no input was changed by verification or native execution.
    if sha(exe)!=manifest['exe_sha256']: raise RuntimeError('Executable changed')
    for row in manifest['retained_inputs']:
        if sha(root/row['path'])!=row['sha256']: raise RuntimeError('Retained input changed')
    version=subprocess.run([cc,'--version'],capture_output=True,text=True,timeout=10).stdout.splitlines()[0]
    summary={'section':'SECTION-01','baseline_archive':manifest['baseline_archive'],
             'exe_sha256':manifest['exe_sha256'],'native_source_sha256':sha(HERE/'native_controls.c'),
             'runner_sha256':sha(Path(__file__)),'compiler':version,'platform':platform.platform(),
             'original_bodies_verified':len(bodies),'native_unique_cases':42,'native_failures':0,
             'baseline_repeat_identical':True,'sensitivity_mutants_detected':len(mutations),
             'retained_assertions_replayed':retained['assertion_replay_total'],
             'corrupted_retained_records_rejected':len(retained['corrupted_record_controls']),
             'EXP150_record_integrity_only':39,'original_inputs_unchanged':True,
             'not_claimed':['full EXP-148/149/150 Unicorn rerun','live FF12','complete transitive native runtime','T2 peer acceptance','L2 completion']}
    save(out/'summary.json',summary)
    print(json.dumps(summary,indent=2))
    return 0


if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
        raise SystemExit(f'SECTION-01 verification failed: {exc}')
