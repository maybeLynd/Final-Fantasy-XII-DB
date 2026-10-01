"""Independent outcome table and byte-effect replay for the retained original-code run."""
import copy, hashlib, json, struct
from pathlib import Path
W=Path('Database/Tools/work/ASTRA')
p=W/'spawn-lifecycle-execution.json'
j=json.loads(p.read_text())
C={c['name']:c for c in j['cases']}
assert len(C)==40
def u32(h,o=0):return struct.unpack_from('<I',bytes.fromhex(h),o)[0]
expect_zero=['empty-control','early-publish-later-reject','reject-before-focus','no-focus','status-skip','no-stats','min-reject','infinite-distance']
for n,c in C.items():
    assert c['returned'] and c['stack_ok'] and c['nonvolatile_ok'] and c['code_unchanged'] and not c['invalid'] and c['error'] is None,n
    if n.startswith('validator-'):
        assert int(c['rax'],16)==(0 if n[len('validator-'):] in expect_zero else 1),n
def out(n):return u32(C[n]['after']['0x50040000'],0x28)
assert out('validator-early-publish-later-reject')==0x41C80000
assert out('validator-reject-before-focus')==0xC47A0000
assert out('validator-nan-distance')==0x7FC12345
for n,v in [(-1,1),(0,1),(1,1),(127,127),(128,128),(255,255),(256,0),(257,1)]:
    assert bytes.fromhex(C['setter-'+str(n)]['after']['0x208d457'])[0]==v
for n,ret,calls in [(0,0xffffffff,0),(1,0xffffffff,1),(127,0xffffffff,127),(128,1,0),(255,1,0)]:
    c=C['automatic-attempt-'+str(n)]
    assert int(c['rax'],16)==ret and sum(x['target']=='0x234af0' for x in c['calls'])==calls
    if n in (128,255):
        expected=struct.pack('<4f',10,20,30,40)
        b=bytes.fromhex(c['after']['0x50050000'])
        assert b[0x2A0:0x2B0]==expected and b[0x2B0:0x2C0]==expected
        assert u32(c['after']['0x50010000'])==0x4000000
for n,ret in [('success-control',1),('nan-observed',1),('infinite-observed',0xffffffff),
              ('no-output-finite-stack',1),('no-output-infinite-stack',0xffffffff),
              ('cap-boundary',0xffffffff),('cap-signed128',0xffffffff)]:
    assert int(C['automatic-'+n]['rax'],16)==ret,n
for bit in (45,49,44,48):
    calls=[x for x in C['automatic-min-flag-'+str(bit)]['calls'] if x['target']=='0x234af0']
    assert len(calls)==1 and int(calls[0]['xmm2'],16)==(0x421C0000 if bit in (45,49) else 0)
def replay(c):
    mem={}
    for a,h in c['injected_writes']:
        mem.update({int(a,16)+i:b for i,b in enumerate(bytes.fromhex(h))})
    reads=writes=0
    for ip,kind,a,n,h in c['memory']:
        a=int(a,16);b=bytes.fromhex(h)
        assert len(b)==n,(c['name'],ip,'width')
        if kind in ('W','STUB-W'):
            mem.update({a+i:v for i,v in enumerate(b)});writes+=1
        else:
            assert bytes(mem.get(a+i,0) for i in range(n))==b,(c['name'],ip,'read replay',hex(a))
            reads+=1
    for a,h in c['after'].items():
        b=bytes.fromhex(h);a=int(a,16)
        assert bytes(mem.get(a+i,0) for i in range(len(b)))==b,(c['name'],'final replay',hex(a))
    return reads,writes
totals=[replay(c) for c in C.values()]
mutant=copy.deepcopy(C['validator-early-publish-later-reject'])
mutant['memory']=[x for x in mutant['memory'] if not (x[0]=='0x234e7d' and x[1]=='W')]
try:replay(mutant)
except AssertionError:missing_write_rejected=True
else:raise AssertionError('Missing-publication mutation escaped')
result=dict(input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),cases=40,
    replay_reads=sum(a for a,b in totals),replay_writes=sum(b for a,b in totals),
    missing_publication_mutation_rejected=missing_write_rejected,pass_all=True)
(W/'spawn-lifecycle-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,indent=2))
