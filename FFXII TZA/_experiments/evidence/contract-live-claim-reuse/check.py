"""Receipt checks and narrowly relevant invalid/empty detection regressions."""
import copy, hashlib, json, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((HERE/n).read_text())
def transform(r):
    assert r['status']=='COUNTEREXAMPLE_VALID_ISOLATED_ORIGINAL_CODE' and r['live_game'] is False
    assert r['faults']==r['stubs_reached']==[]
    body=r['body'];assert len(bytes.fromhex(body['raw']))==body['bytes']==377
    assert sha(bytes.fromhex(body['raw']))==body['sha256']=='1965049e479872fa5d23d2688a53f733287f98bb0e63c9843e86f2f17be2eb26'
    ins=body['instructions'];assert len(ins)==68
    assert sum(len(bytes.fromhex(i['bytes'])) for i in ins)==377
    assert ''.join(i['bytes'] for i in ins)==body['raw']
    assert [c['label'] for c in r['cases']]==['seed','same-input-repeat','changed-input-control']
    slots=[0x22D91A0,0x22D9300,0x22D9310,0x22D8F90]
    for c in r['cases']:
        assert c['returned'] and c['instruction_trace']==[i['address'] for i in ins]
        covered=set()
        assert len(c['deposit_writes'])==14
        for w in c['deposit_writes']:
            assert w['pc'] in c['instruction_trace']
            assert len(bytes.fromhex(w['before']))==w['bytes']
            covered.update(range(int(w['address'],16),int(w['address'],16)+w['bytes']))
        for s in slots:
            key=hex(s);assert set(range(s,s+16))<=covered
            before=bytes.fromhex(c['before'][key]);after=bytes.fromhex(c['after'][key])
            assert len(before)==len(after)==16
            delta=sum(a!=b for a,b in zip(before,after))
            assert delta==c['changed_bytes'][key]
            assert (delta==0) if c['label']=='same-input-repeat' else (delta>0)
    assert r['cases'][0]['after']==r['cases'][1]['before']==r['cases'][1]['after']
    assert r['cases'][0]['input']==r['cases'][1]['input']!=r['cases'][2]['input']
    assert len({c['matrix'] for c in r['cases']})==len({c['leaf'] for c in r['cases']})==1
def bazaar(r):
    assert r['status']=='BOUNDED_CAPTURE_REUSE_PENDING_CANONICAL_CONSUMPTION'
    assert r['payload_size']=='0x56490' and r['save_image_size']=='0x56690'
    assert all(r['source_checks'].values())
    assert len(r['captured_inputs'])==4 and len(r['samples'])==16
    expected={(s,i,n) for s in ('current-field','returned-title','old-after-current-complete','old-after-current-field-settled') for i in (0,1) for n in ('goods_flags','loot_sold_counters')}
    assert {(v['label'],v['sample'],v['region']) for v in r['samples']}==expected
    for v in r['samples']:
        b=bytes.fromhex(v['bytes']);assert len(b)==v['length'] and sha(b)==v['sha256']
        offset,length=(0x59C8,128) if v['region']=='goods_flags' else (0x57C8,512)
        assert len(b)==length and int(v['battle_offset'],16)==offset
        assert int(v['payload_offset'],16)==0x4E48C+offset
        assert int(v['image_offset'],16)==0x4E68C+offset
        assert int(v['address'],16)==0x21B290C+offset
        assert v['nonzero']==[[i,x] for i,x in enumerate(b) if x]
        old=v['label'].startswith('old-after')
        assert v['matches_saved_old']==old
        assert len(v['nonzero'])==((18 if v['region']=='goods_flags' else 44) if old else 0)
def reject(name,fn):
    try:fn()
    except AssertionError:return name
    raise AssertionError(name+' incorrectly accepted')
t=load('transform-counterexample.json');b=load('bazaar-observation.json')
transform(t);bazaar(b)
negative=[]
v=copy.deepcopy(t);v['cases']=[];negative.append(reject('empty execution',lambda:transform(v)))
v=copy.deepcopy(t);v['cases'][1]['instruction_trace']=[];negative.append(reject('no execution detection',lambda:transform(v)))
v=copy.deepcopy(t);v['cases'][1]['deposit_writes']=[];negative.append(reject('no write detection',lambda:transform(v)))
v=copy.deepcopy(b);v['samples']=[];negative.append(reject('empty capture reduction',lambda:bazaar(v)))
v=copy.deepcopy(b);v['samples'][0]['image_offset']='0x53E54';negative.append(reject('header omitted from image coordinate',lambda:bazaar(v)))
for s in load('source-catalog.json'):
    raw=(HERE/s['retained']).read_bytes();assert len(raw)==s['bytes'] and sha(raw)==s['sha256']
deps=load('dependencies.json');assert len(deps)==11
for d in deps:
    committed=subprocess.check_output(['git','cat-file','blob',d['commit']+':'+d['path']],cwd=HERE.parents[4])
    assert len(committed)==d['committed_bytes'] and sha(committed)==d['committed_sha256']
    raw=(HERE.parents[4]/d['path']).read_bytes()
    if raw!=committed:
        assert len(raw)==d['working_bytes'] and sha(raw)==d['working_sha256']
        assert d['relation']=='CRLF-to-LF-only' and raw.replace(b'\r\n',b'\n')==committed
        if d['path'].endswith('.json'):assert json.loads(raw)==json.loads(committed)
    else:assert d['relation'] in ('byte-identical','CRLF-to-LF-only')
print('PASS: nonempty original-code execution/write/change controls and retained live byte/coordinate checks.')
print('Rejected controls:',', '.join(negative))
