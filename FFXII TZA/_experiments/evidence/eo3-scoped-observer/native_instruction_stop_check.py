"""The refined control stops on the observable INC itself, not its prior NOP."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
from native_stop_check import validate,fixture,ROOT

W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check(data,desc,code):
    original,oldgate=fixture.make('preserve')
    before=bytes.fromhex(desc['changes']['inserted_before_hex']);after=bytes.fromhex(desc['changes']['inserted_after_hex'])
    assert desc['changes']['original_sha256']==hashlib.sha256(original).hexdigest()
    assert before.hex()=='48ff83000a00004889bb100a0000488dbb000b00004c8d93000a000048b88877665544332211'
    assert after.hex()=='48ff83080a0000488bbb100a0000'
    assert code==original[:oldgate]+before+b'\x90'+after+original[oldgate+1:]
    assert desc['gate']==oldgate+len(before)+1
    active=next(i for i in desc['instructions'] if i['offset']==desc['gate'])
    assert active['bytes']=='48ff83080a0000' and active['instruction']=='inc qword ptr [rbx + 0xa08]'
    assert code[desc['gate']:desc['gate']+7]==bytes.fromhex(active['bytes'])
    assert b''.join(bytes.fromhex(i['bytes']) for i in desc['instructions'])==code
    assert data['target-ready']['code_hex']==code.hex()
    assert data['target-ready']['gate_address']==data['target-ready']['code_address']+desc['gate']
    return validate(data)


def main():
    outcomes=[];rejected=[];hashes={}
    for arm in ('normal','abort','read-failure'):
        folder=W/('native-instruction-'+arm+'-1')
        data={n:json.loads((folder/(n+'.json')).read_text()) for n in ['plan','target-ready','owned-child','result','capture','stopped-observation','api','baseline']}
        data['target-exit']=json.loads((folder/'target-exit.json').read_text()) if (folder/'target-exit.json').exists() else None
        data['shared-final']=(folder/'shared-final.bin').read_bytes()
        data['samples']=[json.loads(s) for s in (folder/'samples.jsonl').read_text().splitlines()]
        desc=json.loads((folder/'fixture.json').read_text());code=(folder/'fixture.bin').read_bytes()
        for name,digest in data['plan']['sources'].items():
            prefix='Database/Tools/work/ASTRA/eo3-observer/'
            source=W/name[len(prefix):] if name.startswith(prefix) else ROOT/name
            assert sha(source)==digest,name
        outcomes.append(check(data,desc,code))
        hashes[folder.name]={p.name:sha(p) for p in folder.iterdir() if p.is_file()}
        def reject(label,bad,description=None):
            try:check(bad,description or desc,code)
            except (AssertionError,KeyError,StopIteration):rejected.append(arm+': '+label)
            else:raise AssertionError('nondiscriminating control: '+label)
        bad_desc=copy.deepcopy(desc);bad_desc['gate']-=1
        reject('prior NOP substituted for the stopped effect instruction',data,bad_desc)
        if arm!='normal':
            bad=copy.deepcopy(data);raw=bytearray(bad['shared-final']);struct.pack_into('<Q',raw,0xa08,bad['stopped-observation']['before'])
            bad['shared-final']=bytes(raw);bad['result']['final_counters'][1]+=1
            reject('stopped INC committed its effect before termination',bad)
            bad=copy.deepcopy(data);j=next(i for i,r in enumerate(bad['api']) if r['operation']=='TerminateProcess')
            bad['api'].insert(j,dict(operation='SetThreadContext',result=1))
            reject('resume write inserted after hold decision',bad)
    out=dict(status='NATIVE_CURRENT_INSTRUCTION_CONTROL_REVIEWABLE',method='Native synthetic controlled process; not shipping FF12 instructions or live game',
             outcomes=outcomes,rejected=rejected,raw_sha256=hashes,
             established='The selected hardware stop is on INC itself. Normal resume commits its shared counter effect; requested/read-failure aborts leave that effect uncommitted through verified process exit.',
             limits=['One bounded observation per arm on this host and fixture; no universal instruction/process guarantee.',
                     'No claim about unobservable micro-operations; the measured boundary is the architectural memory effect.',
                     'Prior NOP controls remain successor-effect observations, not proof of NOP execution/nonexecution.',
                     'Intentional abort is CONTROL_ABORTED and has no target-finally/free receipt, never healthy semantic acceptance.',
                     'No FF12 call/queue/allocation/crash behavior or whole-state/scheduling transparency established.'])
    if '--write' in sys.argv:
        with (W/'native-instruction-stop-observation.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads((W/'native-instruction-stop-observation.json').read_text())==out
    print('Stopped INC effect directly distinguished: normal commits, both owned aborts leave it uncommitted;',len(rejected),'boundary/continuation corruptions reject.')


if __name__=='__main__':main()
