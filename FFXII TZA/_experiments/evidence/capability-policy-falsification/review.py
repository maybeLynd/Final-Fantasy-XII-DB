"""Review captured original-code effects independently; never runs the emulator."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

work=Path('Database/Tools/work/ASTRA')
source=work/'cap-policy-result.json'
data=json.loads(source.read_text())

def review(data):
    cases=data['cases']
    assert len(cases)==146 and len({c['name'] for c in cases})==146
    catalog={int(b['address'],16):b for p in data['source_hashes']
             for b in json.loads(Path(p).read_text())['bodies']}
    for p,sha in data['source_hashes'].items():
        assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha
    instructions={i['address'] for b in catalog.values() for i in b['instructions']}
    visited=set(); reads=0; writes=0
    for c in cases:
        assert c['visited'] and set(c['visited'])<=instructions
        visited.update(c['visited'])
        assert c['code_unchanged']
        assert c['before']==dict(c['injected_writes'])
        memory={int(a,16)+i:v for a,h in c['injected_writes']
                for i,v in enumerate(bytes.fromhex(h))}
        for pc,access,a,n,value in c['memory']:
            assert pc in instructions
            address=int(a,16)
            assert all(address+i in memory for i in range(n)),(c['name'],a)
            if access=='R':
                assert bytes(memory[address+i] for i in range(n)).hex()==value,(c['name'],pc)
                reads+=1
            else:
                assert access=='W'
                for i,v in enumerate(int(value,16).to_bytes(n,'little')):
                    memory[address+i]=v
                writes+=1
        for a,h in c['after'].items():
            assert bytes(memory[int(a,16)+i] for i in range(len(h)//2)).hex()==h,(c['name'],a)
        if c['name']=='null-bkbi-negative':
            assert not c['returned'] and not c['stack_ok'] and c['error']
            assert c['invalid']==[['0x23b15e',19,'0x64',4]]
            assert not any(e[1]=='W' for e in c['memory'])
            continue
        assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and not c['invalid'] and c['error'] is None
        if 'expected_mask' in c:
            mask=c['expected_mask']
            old=bytes.fromhex(c['before']['0x22c8000'])
            movement=(int.from_bytes(old[:4],'little')&0xFFFFFFFD)|(2 if mask&1 else 0)
            mask1=(old[5]&0xFD)|(2 if mask&4 else 0)
            permit=0 if mask&2 else 1
            effects=[('0x22c8005',1,mask1),('0x22c8000',4,movement)]
            if movement:
                effects += [('0x500b0024',4,0),('0x5006000c',1,0x10),
                            ('0x500800d0',4,0),('0x500900c8',4,0),('0x50090110',4,0x8C)]
            effects += [('0x209a2c5',1,permit)]
            assert [(e[2],e[3],int(e[4],16)) for e in c['memory'] if e[1]=='W']==effects,c['name']
            if c['name'] in ('incapacity-mode2-skip','incapacity-field-skip'):
                assert '0x3272a0' not in c['visited']
            if c['name']=='incapacity-no-leader':
                assert '0x3272a0' in c['visited'] and '0x23b0ca' not in c['visited']
        elif c['name'].startswith('predicate-'):
            value=int(c['args'][0],16)&0xFFFFFFFF
            expected=int(value in {0x2006,0x2037,0x2039,0x203A,0x203B,0x203C}) if c['entry']=='0x322600' else int(value not in {0x2001,0x2009,0x2031})
            assert int(c['rax'],16)==expected and not c['memory']
        else:
            assert c['name'].startswith('permit-setter-')
            value=int(bool(int(c['args'][0],16)&0xFFFFFFFF))
            assert c['memory']==[['0x26bd42','W','0x209a2c5',1,hex(value)]]
    assert sum('expected_mask' in c for c in cases)==24
    assert sum(c['name'].startswith('predicate-') for c in cases)==116
    reached=[hex(a) for a in catalog if hex(a) in visited]
    assert len(reached)==29 and '0x4235c0' not in reached
    return dict(valid_return_cases=145,expected_invalid_state_cases=1,
                full_entry_valid_cases=24,predicate_cases=116,setter_cases=5,
                reached_bodies=reached,unreached_bodies=['0x4235c0'],
                reads=reads,writes=writes,all_observed_bytes_replayed=True,
                exact_output_and_movement_write_order=True)

receipt=review(data)
mutant=deepcopy(data)
case=next(c for c in mutant['cases'] if c['name']=='immobilize-positive')
case['memory']=[e for e in case['memory'] if not (e[1]=='W' and e[2]=='0x500800d0')]
assert case['returned'] and case['nonvolatile_ok']
try: review(mutant)
except AssertionError as error:
    receipt['negative_control']=dict(intervention='Private receipt omits the original requested-speed write while retaining return and ABI flags.',rejected=True,reason=str(error))
else: raise AssertionError('Missing native write escaped review')
receipt['result_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
(work/'cap-policy-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
