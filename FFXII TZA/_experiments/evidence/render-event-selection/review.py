"""Independent raw-memory review of original lookup and caller-policy controls."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json

work=Path('Database/Tools/work/ASTRA')
files=[work/'render-event-result.json',work/'render-event-selection-controls.json']
data=[json.loads(p.read_text()) for p in files]

def review(data):
    assert [len(d['cases']) for d in data]==[25,7]
    cases=[c for d in data for c in d['cases']]
    assert len({c['name'] for c in cases})==32
    source_paths={p:sha for d in data for p,sha in d['source_hashes'].items()}
    for p,sha in source_paths.items(): assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha
    catalog={b['address']:b for p in source_paths for b in json.loads(Path(p).read_text())['bodies']}
    instructions={i['address'] for b in catalog.values() for i in b['instructions']}
    reads=writes=0;visited=set()
    for c in cases:
        assert c['visited'] and set(c['visited'])<=instructions
        visited.update(c['visited']);assert c['code_unchanged']
        assert c['before']==dict(c['injected_writes'])
        mem={int(a,16)+i:v for a,h in c['injected_writes'] for i,v in enumerate(bytes.fromhex(h))}
        for pc,kind,a,n,value in c['memory']:
            assert pc in instructions
            addr=int(a,16);assert all(addr+i in mem for i in range(n))
            if kind=='R':
                assert bytes(mem[addr+i] for i in range(n)).hex()==value,(c['name'],pc)
                reads+=1
            else:
                assert kind=='W'
                for i,v in enumerate(int(value,16).to_bytes(n,'little')):mem[addr+i]=v
                writes+=1
        for a,h in c['after'].items():
            assert bytes(mem[int(a,16)+i] for i in range(len(h)//2)).hex()==h,(c['name'],a)
        if c['name']=='null-table-index1-invalid':
            assert not c['returned'] and c['error'] and c['invalid']==[['0x51f2a3',19,'0x30',1]]
            assert not any(e[1]=='W' for e in c['memory'])
            continue
        assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and not c['invalid'] and c['error'] is None
        assert c['rax']==c['expected_return']
        effects=[e for e in c['memory'] if e[1]=='W']
        if c['parameters'].get('refresh'):
            assert effects==[['0x51f2b7','W','0x51001048',8,c['expected_return']]]
        else:assert not effects
        if c['name'].startswith('getter-'):
            assert '0x423743' not in c['visited'] and '0x423760' not in c['visited']
    byname={c['name']:c for c in cases}
    assert byname['selector2-rejects-lower-priority']['rax']=='0x0'
    assert byname['getter-same-events-selects-alternate']['rax']=='0x2001'
    assert '0x423743' in byname['selector2-rejects-lower-priority']['visited']
    for name,value in [('selector0-entry-bit12-clear-rejects','0x0'),('selector0-entry-bit12-set-accepts','0x1')]:
        c=byname[name];assert '0x424230' in c['visited'] and '0x41c760' in c['visited'] and c['rax']==value
    reached=[a for a in data[0]['body_sha256'] if a in visited]
    assert len(reached)==8
    return dict(valid_returns=31,expected_invalid_state=1,reads=reads,writes=writes,
                reached_bodies=reached,all_observed_memory_replayed=True,
                getter_vs_selector2_negative_control=True,selector0_actual_entry_flag_control=True)

receipt=review(data)
mut=deepcopy(data)
c=next(c for c in mut[0]['cases'] if c['name']=='refresh-above2-sign-extension')
c['memory']=[e for e in c['memory'] if e[1]!='W']
assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok']
try:review(mut)
except AssertionError as e:receipt['missing_cache_write_mutation']={'rejected':True,'reason':str(e),'return_and_abi_retained':True}
else:raise AssertionError('Omitted cache write passed')
receipt['sources']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(work/'render-event-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
