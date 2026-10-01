#!/usr/bin/env python3
"""Reproduce SECTION-03 without writing original inputs or launching FF12.

Linux x86-64 + Python 3.10+ + GCC. The native fixture runs original instructions
in a private mapped image with synthetic state. No Capstone/Unicorn dependency.
"""
from __future__ import annotations
import argparse,hashlib,json,os,platform,shutil,struct,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
from review_retained import decode,negative_controls
HERE=Path(__file__).resolve().parent
MUTANTS={
 'skip_xp_division':'null_xp_roster_count_2',
 'lp_signed_row_byte':'lp_unsigned_byte_multiplier',
 'xp_widen_double_mask':'xp_unrelated_modifier_bit0',
 'only_three_roster_slots':'null_xp_roster_count_4',
 'xp_ignore_missing_owner':'xp_orphan_has_no_owner',
 'lp_ignore_global_gate':'lp_global_gate_precedes_award'}

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def need(ok:bool,msg:str)->None:
    if not ok:raise RuntimeError(msg)
def save(p:Path,obj:object)->None:p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def verify_inputs(db:Path)->list[dict]:
    manifest=json.loads((HERE/'input_manifest.json').read_text(encoding='utf-8'))
    rows=[]
    for r in manifest['inputs']:
        path=(db/r['path']).resolve();need(path.is_relative_to(db),'input escapes database')
        b=path.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'input changed: '+r['path'])
        rows.append(dict(path=r['path'],sha256=sha(b),bytes=len(b)))
    return rows

def verify_image(raw:bytes)->dict:
    m=json.loads((HERE/'original_body_manifest.json').read_text())
    need(sha(raw)==m['exe_sha256'],'original EXE hash mismatch')
    rows=[]
    for b in m['bodies']:
        v=raw[b['file_offset']:b['file_offset']+b['bytes']]
        need(len(v)==b['bytes'] and sha(v)==b['sha256'],'original body mismatch '+b['entry'])
        rows.append(dict(entry=b['entry'],bytes=len(v),sha256=sha(v),matched=True,role=b['role']))
    for d in m['additional_data']:
        need(sha(raw[d['file_offset']:d['file_offset']+d['bytes']])==d['sha256'],'original table mismatch')
    return {'method':'Verify pinned original file ranges; no new Ghidra import','exe_sha256':sha(raw),'bodies':rows,'additional_data':m['additional_data']}

def run_native(binary:Path,exe:Path,out:Path,label:str,mutant:str|None=None)->tuple[dict,int]:
    env=dict(os.environ);env.pop('FF12_REWARD_MUTANT',None)
    if mutant:env['FF12_REWARD_MUTANT']=mutant
    p=subprocess.run([str(binary),str(exe)],capture_output=True,text=True,env=env,timeout=35)
    need(bool(p.stdout.strip()) and not p.stderr.strip(),f'native fixture failed {label}: {p.returncode}, {p.stderr}')
    data=json.loads(p.stdout);save(out/(label+'.json'),data);return data,p.returncode

def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe',required=True,type=Path)
    ap.add_argument('--database',type=Path,default=HERE.parents[2])
    ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--cc',default='gcc')
    args=ap.parse_args()
    need(platform.system()=='Linux' and platform.machine().lower() in ('x86_64','amd64'),'native fixture needs Linux x86-64')
    need(shutil.which(args.cc) is not None,'compiler missing')
    exe=args.exe.resolve();db=args.database.resolve();out=args.output.resolve()
    need(not out.exists() or not any(out.iterdir()),'refusing to overwrite nonempty output')
    out.mkdir(parents=True,exist_ok=True)
    inputs=verify_inputs(db);bodies=verify_image(exe.read_bytes());save(out/'body_verification.json',bodies)
    old=db/'_experiments/evidence/battleunit-live-bindings'
    records={name:json.loads((old/name).read_text()) for name in ('current-complete-memory.json','current-field-memory.json','cleanup.json','exit-check.json','save-before.json')}
    observation=decode(records);save(out/'independent_retained_review.json',observation)
    corrupt=negative_controls(records);save(out/'retained_negative_controls.json',corrupt)
    # Replay the old supplied checker in a separate process, after source pinning.
    folder=db/'_experiments/evidence/retained-reward-bindings'
    proc=subprocess.run([sys.executable,str(folder/'check.py'),'--mutations'],capture_output=True,text=True,timeout=25,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    need(proc.returncode==0 and not proc.stderr.strip(),'historical checker failed')
    replay=json.loads(proc.stdout);expected=json.loads((folder/'observation.json').read_text())
    need(replay==expected,'historical replay differs from preserved observation')
    save(out/'historical_checker_replay.json',{'matches_preserved_observation':True,'samples':len(replay['samples']),'old_corrupted_record_controls':replay['receipt_mutations'],'scope':'Replay only; not a fresh observation or independent acceptance of the original live session.'})
    with tempfile.TemporaryDirectory(prefix='ff12-reward-section03-') as tmp:
        binpath=Path(tmp)/'native_controls'
        cmd=[args.cc,'-std=c11','-O2','-Wall','-Wextra','-Werror','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binpath)]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
        need(p.returncode==0 and not p.stderr.strip(),'native compile failed/warned: '+p.stderr)
        base,rc=run_native(binpath,exe,out,'native_baseline');need(rc==0 and base['checks']==71 and base['failures']==0,'native baseline failed')
        repeat,rc=run_native(binpath,exe,out,'native_repeat');need(rc==0 and repeat==base,'native repeat differs')
        mutations=[]
        for m,expected_name in MUTANTS.items():
            result,rc=run_native(binpath,exe,out,'mutant_'+m,m)
            bad=[c['name'] for c in result['cases'] if not c['pass']]
            need(rc==1 and bad==[expected_name],'mutant failed wrong assertion: '+m+': '+repr(bad))
            mutations.append({'mutant':m,'detected':True,'failed_assertion':expected_name})
    save(out/'code_mutations.json',mutations)
    need(verify_inputs(db)==inputs and sha(exe.read_bytes())==bodies['exe_sha256'],'input changed during execution')
    summary={'section':'SECTION-03','status':'PRODUCTION VALIDATED LOCALLY; formal peer acceptance pending','original_bodies_verified':len(bodies['bodies']),'retained_spans_verified':observation['spans_verified'],'retained_samples':observation['sample_count'],'new_corrupted_record_controls':len(corrupt),'historical_checker_matches':True,'historical_corrupted_record_controls':len(replay['receipt_mutations']),'native_controls':base['checks'],'native_failures':0,'repeat_identical':True,'code_mutants_rejected':len(mutations),'inputs_unchanged':True,'no_scripted_application_callees':True,'not_performed':['new live FF12 session','read of actual reward descriptors or row contents','full EXP-090 Unicorn campaign rerun','execution of the entire defeat orchestrator','whole-game/current-GN Ghidra re-import','formal peer or terminal acceptance']}
    save(out/'summary.json',summary)
    save(out/'execution_environment.json',{'python':sys.version,'system':platform.platform(),'compiler':subprocess.check_output([args.cc,'--version'],text=True).splitlines()[0],'fixture_sha256':sha((HERE/'native_controls.c').read_bytes()),'driver_sha256':sha(Path(__file__).read_bytes()),'inputs':inputs})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
