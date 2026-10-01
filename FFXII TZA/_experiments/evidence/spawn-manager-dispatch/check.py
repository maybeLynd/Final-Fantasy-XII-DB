"""Check primary bytes, isolated callback ordering, and independently replay effects."""
import copy,hashlib,json,struct
from pathlib import Path
W=Path('Database/Tools/work/ASTRA')
ns={};s=(W/'spawn_manager_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x25BFB0')],str(W/'spawn_manager_primary.py'),'exec'),ns)
cat={int(b['address'],16):b for n in ('primary','callees') for b in json.loads((W/('spawn-manager-'+n+'.json')).read_text())['bodies']}
reused=Path('Database/FFXII TZA/_experiments/evidence/arena-selector-static/primary.json')
cat[0x2628B0]=next(b for b in json.loads(reused.read_text())['bodies'] if b['address']=='0x2628b0')
for a,b in cat.items():
    raw=b'';pos=a
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);pos+=len(d);raw+=d
    assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
    o=ns['off'](a-ns['ib']);assert raw==ns['raw'][o:o+len(raw)]
    if a==0x32F850:
        assert b['instructions'][-1]['mnemonic']=='call' and b['instructions'][-1]['operands']=='0x809728'
    else:assert b['instructions'][-1]['mnemonic'] in ('ret','jmp')
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
assert at(0x25BFD6)['operands']=='bl, al' and at(0x25BFD8)['operands']=='0x25c027'
assert at(0x25BFF6)['operands']=='0x26ce60' and at(0x25C036)['operands']=='0x2628b0'
assert at(0x314078)['operands']=='0x25bfb0'
assert at(0x32F1BB)['operands']=='0x32f225' and at(0x32F227)['operands']=='0x26ce60'
assert at(0x330171)['operands']=='0x33017a' and at(0x330175)['operands']=='0x32f1b0'
p=W/'spawn-manager-execution.json';j=json.loads(p.read_text());C={c['name']:c for c in j['cases']}
assert len(C)==12 and j['exe_sha256']==ns['sha'] and j['body_sha256']==cat[0x25BFB0]['sha256']
assert j['probe_sha256']==hashlib.sha256((W/'spawn_manager_probe.py').read_bytes()).hexdigest()
f=json.loads((W/'spawn-manager-feasibility.json').read_text())
assert len(f['cases'])==2 and f['probe_sha256']==j['probe_sha256']
expected={
 'empty-control':([],[],0,False), 'bit0-control':([0],[0],0,True),
 'mask-0x2':([],[1],0,False),'mask-0x10':([],[4],0,False),
 'mask-0x1f':([4,3,2,1,0],[4,3,2,1,0],0,True),
 'mask-0x20':([],[],32,False),
 'mask-0x8000001f':([4,3,2,1,0],[4,3,2,1,0],0x80000000,True),
 'init4-clears-bit0':([4],[4],0,True),
 'init4-adds-bit2':([4,2,0],[4,2,0],0,True),
 'unload4-adds-bit2':([],[4,2],0,False),
 'unload0-adds-bit4':([0],[0],16,True),
 'unload2-requeues-self':([],[2],0,False)}
assert set(expected)==set(C)
def outcome(c):
    init,unload,final,clear=expected[c['name']]
    trace=[('0x26ce60',i) for i in init]+[('0x2628b0',i) for i in unload]
    assert [(t['target'],t['index']) for t in c['trace']]==trace,c['name']
    assert struct.unpack('<I',bytes.fromhex(c['after']['0x2099abc']))[0]==final,c['name']
    roster=(bytes(32) if clear else bytes(range(1,33))).hex()
    assert c['after']['0x209a1f0']==roster,c['name']
def replay(c):
    assert all(c[k] for k in ('returned','stack_ok','nonvolatile_ok','code_unchanged')) and not c['invalid'] and c['error'] is None
    mem={int(a,16)+i:b for a,h in c['before'].items() for i,b in enumerate(bytes.fromhex(h))}
    r=w=0
    for index in range(len(c['memory'])+1):
        for t in (t for t in c['trace'] if t['event_index']==index):
            for a,n,h in ((0x2099ABC,4,t['mask']),(0x209A1F0,32,t['roster'])):
                assert bytes(mem[a+i] for i in range(n)).hex()==h,(c['name'],'callback state',index)
        if index==len(c['memory']):break
        ip,kind,a,n,h=c['memory'][index];a=int(a,16);b=bytes.fromhex(h)
        assert len(b)==n and all(a+i in mem for i in range(n)),(c['name'],ip,'untracked address')
        if kind in ('W','STUB-W'):mem.update({a+i:v for i,v in enumerate(b)});w+=1
        else:
            assert kind=='R' and bytes(mem[a+i] for i in range(n))==b,(c['name'],ip,'read replay')
            r+=1
    for a,h in c['after'].items():
        b=bytes.fromhex(h);a=int(a,16)
        assert bytes(mem[a+i] for i in range(len(b)))==b,(c['name'],'final replay')
    return r,w
totals=[]
for c in [*C.values(),*f['cases']]:outcome(c);totals.append(replay(c))
mutants={}
m=copy.deepcopy(C['bit0-control'])
target=next(e for e in m['memory'] if e[0]=='0x25c017' and e[1]=='W')
target[4]=bytes([1])*target[3];target[4]=target[4].hex()
try:replay(m)
except AssertionError:mutants['wrong_roster_publication_rejected']=True
else:raise AssertionError('Roster publication mutation escaped')
m=copy.deepcopy(C['mask-0x1f']);m['trace'][0]['index']=0;m['trace'][4]['index']=4
try:outcome(m)
except AssertionError:mutants['reversed_initialization_order_rejected']=True
else:raise AssertionError('Callback order mutation escaped')
out=dict(exe_sha256=ns['sha'],new_catalog_bodies=10,reused_body=dict(path=str(reused).replace('\\','/'),sha256=hashlib.sha256(reused.read_bytes()).hexdigest(),address='0x2628b0',body_sha256=cat[0x2628B0]['sha256']),
    execution_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),cases=12,feasibility_cases=2,
    replay_reads=sum(a for a,b in totals),replay_writes=sum(b for a,b in totals),mutation_controls=mutants,
    limits='Complete original-byte source checks and isolated queue wrapper only. Provider interventions do not establish native effects or normal load scheduling.',pass_all=True)
(W/'spawn-manager-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
