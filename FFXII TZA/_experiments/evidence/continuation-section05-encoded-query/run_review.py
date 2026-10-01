#!/usr/bin/env python3
"""Reproduce Section05 on Linux x86-64 with GCC and the authorized original EXE.
No network, game installation changes, or application-callee substitutions.
"""
from __future__ import annotations
import argparse, hashlib, json, platform, shutil, subprocess, tempfile
from pathlib import Path
from review_retained import audit, negative_controls, require
HERE=Path(__file__).resolve().parent
MUTANTS={
'equipment_flag':'equipment_bit54_sets_low_bit',
'tail_six':'class10_strided_full98_layout',
'rebase_64bit':'rebase_pointer_uses_low32_base',
'failure_short_clear':'id_failure_zeroes_full_record',
'derived_mask':'rebase_masks_128_bytes',
'class19_upper':'class19_effF_rejected',
'clear_wrong_output':'direct_rejection_only_clears_name'}

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def save(out:Path,name:str,data:object)->None:(out/name).write_text(json.dumps(data,indent=2)+'\n')
def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--exe',type=Path,required=True);p.add_argument('--database',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    require(platform.system()=='Linux' and platform.machine() in ('x86_64','amd64'),'requires Linux x86-64')
    require(shutil.which('gcc') is not None,'GCC unavailable')
    require(not a.output.exists(),'output directory must not exist');a.output.mkdir(parents=True)
    m=json.loads((HERE/'original_body_manifest.json').read_text());image=a.exe.read_bytes()
    require(hashlib.sha256(image).hexdigest()==m['exe_sha256'],'wrong original image')
    receipts=[]
    for x in m['bodies']+m['data']:
        b=image[x['file_offset']:x['file_offset']+x['length']]
        require(len(b)==x['length'] and hashlib.sha256(b).hexdigest()==x['sha256'],f'range mismatch {x["address"]}')
        receipts.append({'address':x['address'],'length':x['length'],'matches':True})
    inp=json.loads((HERE/'input_manifest.json').read_text())['unchanged_inputs']
    for x in inp:require(digest(a.database/x['path'])==x['sha256'],f'input changed {x["path"]}')
    data=json.loads((a.database/'_experiments/evidence/s04-validator-arms/result.json').read_text())
    retained=audit(data,image);bad=negative_controls(data,image)
    save(a.output,'body_verification.json',{'bodies':len(m['bodies']),'data_spans':len(m['data']),'ranges':receipts})
    save(a.output,'independent_retained_review.json',retained);save(a.output,'retained_negative_controls.json',bad)
    with tempfile.TemporaryDirectory(prefix='ff12-s05-') as tmp:
        binary=Path(tmp)/'native_controls'
        flags=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-fno-strict-aliasing','-fPIE','-pie',str(HERE/'native_controls.c'),'-o',str(binary)]
        build=subprocess.run(flags,capture_output=True,text=True,timeout=30)
        require(build.returncode==0 and not build.stderr,'compiler failed/warned: '+build.stderr)
        def execute(variant=None):
            cmd=[str(binary),str(a.exe.resolve())]+([variant] if variant else [])
            run=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
            require(not run.stderr,'unexpected native diagnostic: '+run.stderr)
            result=json.loads(run.stdout);return run.returncode,result
        rc,base=execute();require(rc==0 and base['checks']==200 and base['failures']==0,'native baseline')
        require(len(base['cases'])==200 and all(x['pass'] for x in base['cases']),'baseline case integrity')
        require(len({x['name'] for x in base['cases']})==200,'duplicate assertion identity')
        rc,repeat=execute();require(rc==0 and base==repeat,'repeat changed')
        mutations=[]
        for name,assertion in MUTANTS.items():
            rc,result=execute(name);fails=[x['name'] for x in result['cases'] if not x['pass']]
            require(rc==1 and fails==[assertion],f'{name} did not fail intended check: {fails}')
            mutations.append({'variant':name,'intended_assertion':assertion,'returncode':rc,'failure':fails,'rejected':True})
        save(a.output,'native_baseline.json',base);save(a.output,'native_repeat.json',repeat);save(a.output,'code_mutations.json',mutations)
        save(a.output,'build_receipt.json',{'compiler':subprocess.run(['gcc','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],'flags':flags[:9], 'source_sha256':digest(HERE/'native_controls.c'),'binary_sha256':digest(binary),'system':platform.system(),'machine':platform.machine()})
    require(digest(a.exe)==m['exe_sha256'],'original image altered')
    for x in inp:require(digest(a.database/x['path'])==x['sha256'],'historical input altered')
    save(a.output,'summary.json',{'status':'PASS_LOCAL_PRODUCTION_CHECKS','native_assertions':200,'repeat_identical':True,'code_mutants_rejected':len(MUTANTS),'retained_traced_records':retained['traced_probe_records'],'retained_summary_only_returns':4,'retained_corruptions_rejected':len(bad),'verified_bodies':len(m['bodies']),'verified_data_spans':len(m['data']),'original_and_historical_inputs_unchanged':True,'original_application_callee_substitutions':0,'import_bridges':1,'live_game_session':False,'full_historical_campaign_rerun':False,'formal_peer_acceptance':'PENDING'})
    print('PASS: 200 native assertions, identical repeat, 7 intended code-mutant refusals, 246 retained traces, 8 retained negative controls.')

if __name__=='__main__':
    main()
