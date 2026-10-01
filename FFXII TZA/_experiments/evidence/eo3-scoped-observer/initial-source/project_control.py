"""Method A: reuse retained native contexts; no new native or live execution."""
import copy
import hashlib
import json
from pathlib import Path
from project import project,REQUIRED

W=Path(__file__).resolve().parent;ROOT=W.parents[4]
E=ROOT/'Database/FFXII TZA/_experiments/evidence/native-fp-context-control'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((E/'manifest.json').read_text())
def load(relative):
    p=E/relative
    # Original package's manifest is authoritative for these retained bytes.
    expected=manifest[relative] if isinstance(manifest,dict) and relative in manifest else None
    if isinstance(expected,dict):expected=expected.get('sha256')
    assert expected==sha(p),(relative,'unmatched retained source')
    return json.loads(p.read_text())

ready=load('full-observer/target-ready.json');api=load('full-observer/api.json')
matched=[];eligible=[]
for row in api:
    if row.get('api')=='GetThreadContext' and row.get('result')==1 and row.get('requested_flags',0)&REQUIRED==REQUIRED:
        values=project(row);eligible.append(row)
        if values['rip']==ready['gate_address']:
            assert values['rcx']==values['rbx']==ready['buffer_address']>0xffffffff
            matched.append(dict(unix=row['unix'],**values))
assert matched and eligible,'zero captured positives'
# Seed fixture mov rbx,rcx precedes the gate and no intervening instruction writes
# either. This checks two known native 64-bit values, not guessed random registers.
rejected=[]
def reject(label,row):
    try:project(row)
    except (AssertionError,KeyError,ValueError):rejected.append(label)
    else:raise AssertionError('bad context accepted: '+label)
r=copy.deepcopy(eligible[0]);r['api']='SetThreadContext';reject('proposed write is not an observed read',r)
r=copy.deepcopy(eligible[0]);r['result']=0;reject('failed native read',r)
r=copy.deepcopy(eligible[0]);r['requested_flags']=0x100011;reject('CONTROL/DEBUG without INTEGER',r)
r=copy.deepcopy(eligible[0]);r['context_hex']=r['context_hex'][:-2];reject('short context',r)
negative=load('no-fp-request/api.json')
negative_reads=[r for r in negative if r.get('api')=='GetThreadContext' and r.get('result')==1]
assert negative_reads
for r in negative_reads:
    try:project(r)
    except AssertionError:pass
    else:raise AssertionError('captured no-INTEGER context accepted')
assert (matched[0]['rbx']&0xffffffff)!=ready['buffer_address'],'32-bit truncation control was vacuous'
out=dict(status='CAPTURED_NATIVE_GPR_PROJECTION_CONTROL_ONLY',method='A - existing native artifacts',
         fresh_native_execution=False,live_game=False,source_package='749d391c76bb02385ea826060060f3077d3733f0',
         source_hashes={n:sha(E/n) for n in ['full-observer/target-ready.json','full-observer/api.json','no-fp-request/api.json']},
         known_gate=ready['gate_address'],known_buffer=ready['buffer_address'],matched_contexts=matched,
         rejected_captured_no_integer_reads=len(negative_reads),rejections=rejected,
         limits=['No new breakpoint delivery qualification or FF12 process observation.',
                 'RDI/R10 offsets follow the retained AMD64 context layout; their semantic values were not independently seeded here.',
                 'FP/XSTATE transparency is not asserted; the existing FIP counterexample remains unchanged.'])
with (W/'projection-control.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print('Retained native contexts:',len(matched),'known RCX/RBX positives; all',len(negative_reads),'no-INTEGER reads rejected. No new execution.')
