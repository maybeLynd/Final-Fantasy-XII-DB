"""Validate a failed setup checkpoint without accepting its semantic result."""
import copy,hashlib,json
from pathlib import Path
import reduce as reducer
HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def check(result,raw,cleanup):
    require(result['status']=='INVALID_FIELD_SETUP' and result['semantic_closure']==[],'failed setup must not close claims')
    require(result['field_observation'] is None,'field evidence missing')
    observed=reducer.reduce(raw)
    require(len(observed['samples'])==2,'exact nonzero samples')
    require(all(s['status']=='INITIALIZED' and s['used_count']==0 and len(s['free_indices'])==128 for s in observed['samples']),'provisional raw title structure')
    require(cleanup['status']=='RESTORED_UNCHANGED' and cleanup['processes']==[] and cleanup['changed_files']==[],'cleanup missing')
    require(cleanup['fresh_backup_and_original_census_match'] and cleanup['save_config_files']==26 and cleanup['pc_control'].startswith('OFF'),'restoration/control release')
    return observed
def main():
    manifest=json.loads((HERE/'manifest.json').read_text());require(len(manifest)>0,'empty manifest')
    for name,v in manifest.items():
        b=(HERE/name).read_bytes();require(len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],'manifest mismatch '+name)
    result=json.loads((HERE/'result.json').read_text());raw=json.loads((HERE/'title-access-qualified-raw.json').read_text());cleanup=json.loads((HERE/'cleanup.json').read_text())
    check(result,raw,cleanup)
    initial=json.loads((HERE/'title-raw.json').read_text());require(initial['status']=='INVALID' and not initial['samples'] and initial['module_verdict']=='unreadable','retain rejected initial observer')
    access=json.loads((HERE/'module-control.json').read_text());qualified=json.loads((HERE/'module-control-outside-sandbox.json').read_text())
    require(access['untyped_modules'] is None and access['typed_modules'] is None and access['self_modules'],'access failure detection control')
    require(qualified['positive'] and len(qualified['typed_modules'])==93 and qualified['typed_modules']==qualified['untyped_modules'],'access hypothesis discriminator')
    budget=json.loads((HERE/'setup-budget.json').read_text());require(budget['attempts']==budget['limit_attempts']==2 and budget['status']=='STOP_LOSS_REACHED_INPUT','no renewed setup allowance')
    mutations=[]
    for name,fn in [('semantic-promotion',lambda r,w,c:r.update(status='VALIDATED')),('invent-field',lambda r,w,c:r.update(field_observation={'used':9})),('corrupt-pool',lambda r,w,c:w['samples'][0]['reads'][2].update(hex='00')),('omit-restoration',lambda r,w,c:c.update(fresh_backup_and_original_census_match=False))]:
        r,w,c=copy.deepcopy(result),copy.deepcopy(raw),copy.deepcopy(cleanup);fn(r,w,c)
        try:check(r,w,c)
        except ValueError:mutations.append(name)
        else:raise ValueError('mutation survived '+name)
    return {'checkpoint_integrity':'PASS','live_semantic_result':'INVALID_FIELD_SETUP','semantic_closure':[],'reducer_controls':reducer.controls(),'rejected_checkpoint_mutations':mutations}
if __name__=='__main__':
    result=main();(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
