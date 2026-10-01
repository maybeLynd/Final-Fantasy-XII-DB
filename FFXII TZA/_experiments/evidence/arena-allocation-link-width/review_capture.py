"""Review saved JSON only: reconcile every non-stack read/write with recorded initialized state."""
import hashlib,json
from pathlib import Path
W=Path('Database/Tools/work/ASTRA')
E=Path('Database/FFXII TZA/_experiments/evidence')
result=json.loads((W/'arena-allocation-result.json').read_text())
mutant=json.loads((W/'arena-allocation-mutant-result.json').read_text())
fixtures=json.loads((E/'resource-arena-backing/initializer-result.json').read_text())
assert result['stubs']==[] and len(result['cases'])==7
assert result['fixture_receipt_sha256']==hashlib.sha256((E/'resource-arena-backing/initializer-result.json').read_bytes()).hexdigest()
receipts=[E/'resource-arena-backing/primary.json',E/'authored-reference-lifetime-review/primary.json',W/'arena-allocation-primary.json']
bodies={b['address']:b for p in receipts for b in json.loads(p.read_text())['bodies']}
starts={i['address'] for a in result['body_sha256'] for i in bodies[a]['instructions']}
for a,h in result['body_sha256'].items():assert bodies[a]['sha256']==h
G,GN,BASE,A=0x22D7000,0x2000,0x1F83530,0x22D7FD0+2*0xA8
reviews=[]
for c in [*result['cases'],mutant['case']]:
    p=int(c['backing'],16);lo=p&0xFFFFFFFF
    f=next(x for x in fixtures['cases'] if x['name']==c['fixture'])
    regions={G:bytearray(GN),BASE:bytearray(8),p:bytearray(b'\xa5'*0x100000)}
    def locate(a,n):
        for begin,data in regions.items():
            if begin<=a and a+n<=begin+len(data):return data,a-begin
        raise ValueError(hex(a))
    def write(a,n,v):
        data,i=locate(a,n);data[i:i+n]=v.to_bytes(n,'little')
    def read(a,n):
        data,i=locate(a,n);return bytes(data[i:i+n])
    for _,a,n,v in f['writes']:write(int(a,16),n,int(v,16))
    for a,h in c['fixture_sha256'].items():
        a=int(a,16);assert hashlib.sha256(regions[a]).hexdigest()==h
    foreign=[];stats=[];alloc=[];mirror_initial=None
    for s in c['steps']:
        if c['alias_intervention'] and s['label']=='allocation2':
            mirror_initial=bytes(regions[p]);regions[lo]=bytearray(mirror_initial)
            assert hashlib.sha256(mirror_initial).hexdigest()==c['alias_initial_sha256']
        assert s['visited'] and s['visited'][0]==s['entry'] and all(a in starts for a in s['visited'])
        assert s['calls'] and [x['target'] for x in s['calls']]==[a for a in s['visited'] if a in result['body_sha256']]
        assert s['calls'][0]['args']==s['args']
        if s['returned']:assert s['stack_ok'] and s['nonvolatile_ok'] and s['error'] is None and s['rip']=='0x70000000' and s['invalid']==[]
        else:assert s['error']=='Invalid memory write (UC_ERR_WRITE_UNMAPPED)' and len(s['invalid'])==1
        ignored=0
        for rip,kind,a,n,v in s['memory']:
            assert rip in s['visited']
            a=int(a,16)
            if any(i['rip']==rip and int(i['address'],16)==a and i['bytes']==n for i in s['invalid']):
                assert kind=='W' and int(v,16)==int(s['invalid'][0]['value'],16)
                try:locate(a,n)
                except ValueError:pass
                else:raise AssertionError('reported unmapped write is mapped')
                ignored+=1
                continue
            if kind=='R':assert read(a,n).hex()==v,(c['name'],s['label'],rip,hex(a))
            else:assert kind=='W';write(a,n,int(v,16))
            if c['alias_intervention'] and lo<=a<lo+0x100000:foreign.append([rip,kind,hex(a),n,v])
        assert ignored==len(s['invalid'])
        assert read(A,0xA8).hex()==s['arena'] and read(p,0x500).hex()==s['prefix'] and read(p+0xFFF00,0x100).hex()==s['tail']
        stats.append(dict(step=s['label'],instructions=len(s['visited']),calls=len(s['calls']),reads=sum(e[1]=='R' for e in s['memory']),writes=sum(e[1]=='W' for e in s['memory']),returned=s['returned'],rax=s['rax'],invalid=s['invalid']))
        if s['label'].startswith('allocation'):alloc.append(s)
    assert read(BASE,8)==b'\0'*8
    assert len(alloc)==c['requested_allocations']
    expected=[p+0x2C0,p+0x340] if c['direction']==0 else [p+0xFFFC0,p+0xFFF40]
    for i,s in enumerate(alloc):
        if s['returned']:assert int(s['rax'],16)==expected[i]
    if c['name'] in ('above4-two-front','above4-two-back'):
        addr,rip=(lo+0x290,'0x36ca8a') if c['direction']==0 else (lo+0xFFF8C,'0x36ca75')
        assert alloc[0]['returned'] and not alloc[1]['returned']
        assert alloc[1]['invalid']==[dict(rip=rip,access=20,address=hex(addr),bytes=4,value='0x0')]
    else:assert all(s['returned'] for s in c['steps']) and c['steps'][-1]['label']=='restore-selection'
    if c['direction']==0 and c['size']==0x40 and alloc[1]['returned']:
        observed=int.from_bytes(read(p+0x30C,4),'little')
        assert observed==(0 if c['name']=='zero-decoder-mutant' else (p+0x280)&0xFFFFFFFF)
    if c['size']==0xFFD40:assert read(A+0x90,16)==b'\0'*16
    assert int.from_bytes(read(A+0x60,2),'little')==sum(s['returned'] for s in alloc)
    if c['alias_intervention']:
        assert foreign==[['0x36ca8a','W','0x10290',4,'0x0'],['0x36ca8d','W','0x102be',2,'0x0'],['0x36b83e','R','0x10290',4,'00000000'],['0x36b853','W','0x10290',4,'0x10300'],['0x36b856','W','0x102be',2,'0x0']]
        assert bytes(regions[lo])==mirror_initial # foreign writes occurred, but this exact mirrored case restores those bytes
    reviews.append(dict(name=c['name'],all_recorded_memory_consistent=True,steps=stats,foreign_events=foreign,alias_final_matches_initial=None if mirror_initial is None else bytes(regions[lo])==mirror_initial))
out=dict(method='saved-data reconciliation only; no original code execution, no executable modifications',input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [W/'arena-allocation-result.json',W/'arena-allocation-mutant-result.json']},reviews=reviews,all_pass=True)
(W/'arena-capture-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
