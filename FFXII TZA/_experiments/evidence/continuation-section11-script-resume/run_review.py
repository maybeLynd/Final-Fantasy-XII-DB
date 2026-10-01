#!/usr/bin/env python3
"""Reproduce Section11 on Linux x86-64. Requires the authorized EXE and baseline DB.
No packages/downloads, Windows services, code on disk modification or persistent binaries.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
from review_retained import run as run_retained

HERE=Path(__file__).resolve().parent

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_virtual(raw: bytes, va: int, size: int) -> bytes:
    pe=struct.unpack_from('<I',raw,0x3c)[0]
    if raw[pe:pe+4]!=b'PE\0\0':raise ValueError('not PE')
    opt=pe+24
    if struct.unpack_from('<H',raw,opt)[0]!=0x20b:raise ValueError('not PE32+')
    base=struct.unpack_from('<Q',raw,opt+24)[0];rva=va-base
    n=struct.unpack_from('<H',raw,pe+6)[0]
    sections=opt+struct.unpack_from('<H',raw,pe+20)[0]
    for i in range(n):
        s=sections+40*i;vs,start,rs,off=struct.unpack_from('<IIII',raw,s+8)
        if start<=rva and rva+size<=start+rs:
            result=raw[off+rva-start:off+rva-start+size]
            if len(result)!=size:raise ValueError('truncated range')
            return result
    raise ValueError(f'unbacked range {va:x}+{size:x}')

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe',type=Path,required=True);p.add_argument('--database',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if platform.system()!='Linux' or platform.machine() not in ('x86_64','amd64'):
        raise SystemExit('requires Linux x86-64, not live Windows/game execution')
    if not shutil.which('gcc'):raise SystemExit('gcc is required')
    if a.output.exists():raise SystemExit('output must not exist')
    exe=a.exe.resolve(strict=True);db=a.database.resolve(strict=True)
    manifest=json.loads((HERE/'original_body_manifest.json').read_text())
    raw=exe.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    if sha!=manifest['exe_sha256']:raise SystemExit('original EXE hash mismatch')
    checked=[]
    for row in manifest['bodies']+manifest['data_spans']:
        va=int(row.get('entry',row.get('address')),16);body=read_virtual(raw,va,row['length'])
        if hashlib.sha256(body).hexdigest()!=row['sha256']:raise SystemExit(f'body mismatch {va:x}')
        checked.append({'address':f'{va:08X}','bytes':len(body),'sha256':row['sha256'],'match':True})
    inputs=json.loads((HERE/'input_manifest.json').read_text())['inputs']
    for row in inputs:
        if digest(db/row['path'])!=row['sha256']:raise SystemExit('historical input mismatch: '+row['path'])
    a.output.mkdir(parents=True)
    versions={'platform':platform.platform(),'python':platform.python_version(),'compiler':subprocess.check_output(['gcc','--version'],text=True).splitlines()[0]}
    with tempfile.TemporaryDirectory(prefix='ff12-section11-') as tmp:
        binary=Path(tmp)/'native_controls'
        command=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-fno-strict-aliasing','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        build=subprocess.run(command,capture_output=True,text=True,timeout=40)
        if build.returncode or build.stderr:raise RuntimeError('compilation failed/diagnostics: '+build.stderr)
        baselines=[]
        for name in ['native_baseline','native_repeat']:
            x=subprocess.run([str(binary),str(exe)],capture_output=True,text=True,timeout=30)
            if x.returncode or x.stderr:raise RuntimeError(f'{name}: {x.returncode} {x.stderr}')
            value=json.loads(x.stdout)
            if value['checks']!=146 or value['failures']!=0 or not all(c['pass'] for c in value['cases']):raise AssertionError(name)
            if len({c['name'] for c in value['cases']})!=146:raise AssertionError('duplicate assertion names')
            (a.output/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n');baselines.append(value)
        if baselines[0]!=baselines[1]:raise AssertionError('baseline repeat mismatch')
        mutations=[]
        for variant in json.loads((HERE/'variant_plan.json').read_text()):
            if read_virtual(raw,int(variant['address'],16),len(bytes.fromhex(variant['before']))).hex()!=variant['before']:raise AssertionError('mutation preimage')
            x=subprocess.run([str(binary),str(exe),variant['name']],capture_output=True,text=True,timeout=30)
            value=json.loads(x.stdout);bad=[c['name'] for c in value['cases'] if not c['pass']]
            valid=x.returncode==1 and not x.stderr and bad==[variant['expected_first_failure']]
            if not valid:raise AssertionError(f'wrong mutant failure: {variant["name"]}: {bad}; {x.stderr}')
            mutations.append(dict(variant,rejected=True,exit_code=x.returncode,first_failure=bad[0]))
        (a.output/'code_mutations.json').write_text(json.dumps(mutations,indent=2)+'\n')
    retained=run_retained(db,a.output)
    if digest(exe)!=sha:raise AssertionError('EXE changed')
    for row in inputs:
        if digest(db/row['path'])!=row['sha256']:raise AssertionError('historical input changed')
    (a.output/'body_verification.json').write_text(json.dumps(checked,indent=2)+'\n')
    summary={'status':'PASS','exe_sha256':sha,'selected_bodies':len(manifest['bodies']),'data_spans':len(manifest['data_spans']),
             'assertions':146,'identical_repeat':True,'mutants_rejected':len(mutations),'retained':retained,
             'application_substitutions':0,'import_bridges':0,'live_game':False,'full_unicorn_campaign_rerun':False,
             'source_sha256':digest(HERE/'native_controls.c'),'environment':versions}
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
