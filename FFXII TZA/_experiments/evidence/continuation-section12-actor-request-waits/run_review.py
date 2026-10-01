#!/usr/bin/env python3
"""Run the bounded Section12 original-instruction fixture, not a live Windows game.
Requires the user's original EXE, Linux x86-64 and GCC. No network or game-file writes.
"""
from __future__ import annotations
import argparse,hashlib,json,platform,shutil,struct,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def virtual(raw:bytes,va:int,n:int)->bytes:
    pe=struct.unpack_from('<I',raw,0x3c)[0]
    if raw[pe:pe+4]!=b'PE\0\0':raise ValueError('Not PE')
    opt=pe+24
    if struct.unpack_from('<H',raw,opt)[0]!=0x20b:raise ValueError('Not PE32+')
    base=struct.unpack_from('<Q',raw,opt+24)[0];rva=va-base
    sec=opt+struct.unpack_from('<H',raw,pe+20)[0]
    for i in range(struct.unpack_from('<H',raw,pe+6)[0]):
        _,start,size,off=struct.unpack_from('<IIII',raw,sec+40*i+8)
        if start<=rva and rva+n<=start+size:
            result=raw[off+rva-start:off+rva-start+n]
            if len(result)!=n:raise ValueError('Truncated')
            return result
    raise ValueError(f'Unbacked address {va:x}')

def main()->None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exe',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if platform.system()!='Linux' or platform.machine().lower() not in ('x86_64','amd64'):raise SystemExit('Requires Linux x86-64; this is not Windows deployment')
    if not shutil.which('gcc'):raise SystemExit('GCC required')
    if a.output.exists():raise SystemExit('Output must not exist')
    exe=a.exe.resolve(strict=True);raw=exe.read_bytes();manifest=json.loads((HERE/'original_body_manifest.json').read_text());digest=hashlib.sha256(raw).hexdigest()
    if digest!=manifest['exe_sha256']:raise SystemExit('Original EXE identity differs')
    checks=[]
    for r in manifest['bodies']+manifest['data_spans']:
        va=int(r.get('entry',r.get('address')),16);actual=hashlib.sha256(virtual(raw,va,r['length'])).hexdigest()
        if actual!=r['sha256']:raise SystemExit('Original range mismatch')
        checks.append({'address':f'{va:08X}','length':r['length'],'sha256':actual,'match':True})
    a.output.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix='ff12-section12-') as d:
        binary=Path(d)/'original_controls'
        cmd=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-fno-strict-aliasing','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=40)
        if r.returncode or r.stderr:raise RuntimeError('Build diagnostics: '+r.stderr)
        baseline=[]
        for name in ('native_baseline','native_repeat'):
            r=subprocess.run([str(binary),str(exe)],capture_output=True,text=True,timeout=15)
            if r.returncode or r.stderr:raise RuntimeError(f'{name}: exit{r.returncode} {r.stderr}')
            value=json.loads(r.stdout)
            if value['checks']!=139 or value['failures'] or not all(c['pass'] for c in value['cases']) or len({c['name'] for c in value['cases']})!=139:raise AssertionError(name)
            (a.output/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n');baseline.append(value)
        if baseline[0]!=baseline[1]:raise AssertionError('Repeat changed')
        muts=[]
        for v in json.loads((HERE/'variant_plan.json').read_text()):
            if virtual(raw,int(v['address'],16),len(bytes.fromhex(v['before']))).hex()!=v['before']:raise AssertionError('Variant preimage')
            r=subprocess.run([str(binary),str(exe),v['name']],capture_output=True,text=True,timeout=15)
            value=json.loads(r.stdout);bad=[c['name'] for c in value['cases'] if not c['pass']]
            if r.returncode!=1 or r.stderr or bad!=[v['expected_first_failure']]:raise AssertionError(f'Wrong variant failure {v["name"]}: {bad} {r.stderr}')
            muts.append(dict(v,rejected=True,exit_code=r.returncode,first_failure=bad[0]))
    if sha(exe)!=digest:raise AssertionError('EXE changed')
    (a.output/'body_verification.json').write_text(json.dumps(checks,indent=2)+'\n');(a.output/'code_mutations.json').write_text(json.dumps(muts,indent=2)+'\n')
    out={'status':'PASS','assertions':139,'identical_repeat':True,'mutants_rejected':len(muts),'original_bodies_verified':len(manifest['bodies']),'original_data_spans_verified':len(manifest['data_spans']),'application_substitutions':0,'import_bridges':0,'planted_callbacks':0,'live_game':False,'fresh_ghidra':False,'full_historical_campaign_rerun':False,'source_sha256':sha(HERE/'native_controls.c'),'exe_sha256':digest,'environment':{'platform':platform.platform(),'python':platform.python_version(),'compiler':subprocess.check_output(['gcc','--version'],text=True).splitlines()[0]},'build_command':cmd[:-1]+['<temporary binary>']}
    (a.output/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
