"""Method-A source and bridge checks. No simulated behavior or game execution."""
from pathlib import Path
import hashlib, json, struct
W=Path('Database/Tools/work/ASTRA');ns={}
s=(W/'spawn_restore_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x314530')],str(W/'spawn_restore_primary.py'),'exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={}
for n in ('primary','callers','support'):
    r=json.loads((W/('spawn-restore-'+n+'.json')).read_text())
    assert r['exe_sha256']==ns['sha']
    for b in r['bodies']:
        a=int(b['address'],16);assert a not in cat;cat[a]=b
assert len(cat)==13
def verify(b):
    a=int(b['address'],16);pos=a;raw=b''
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);raw+=d;pos+=len(d)
    o=ns['off'](a-ns['ib'])
    assert len(raw)==b['bytes'] and sha(raw)==b['sha256'] and raw==ns['raw'][o:o+len(raw)]
    assert b['instructions'][-1]['mnemonic'] in ('ret','jmp')
for b in cat.values():verify(b)
def at(a,cs=cat):return next(i for b in cs.values() for i in b['instructions'] if int(i['address'],16)==a)
anchors={
    0x267C90:('jmp','0x314530'),0x314563:('or','byte ptr [rax + 0x1062], 0x20'),
    0x314575:('mov','dword ptr [rip + 0x1bd8ae9], edx'),
    0x314586:('mov','dword ptr [rax + 0x105c], edx'),
    0x314478:('jge','0x314512'),0x31448C:('call','0x3145e0'),
    0x31449A:('call','0x3145e0'),0x3144A1:('call','0x26a5f0'),
    0x2801FF:('call','0x268320'),0x280213:('mov','byte ptr [rax + 0x1061], dil'),
    0x28021F:('call','0x267c90'),0x28027C:('call','0x314440'),
    0x280446:('add','rax, 0x3f8'),0x28044C:('mov','qword ptr [rbx + 0xc0], rax'),
    0x285E6B:('or','dword ptr [rax + 0x400], 0x200'),
    0x285E7C:('or','dword ptr [rax + 0x400], 0x400'),
    0x36FD17:('call','0x268320'),0x36FD28:('call','0x267c90'),
    0x394257:('call','0x268320'),0x39425C:('call','0x267c90'),
    0x355949:('call','0x286000'),0x355958:('jmp','0x26b4e0'),
    0x355E80:('xor','ecx, ecx'),0x355E82:('jmp','0x287d00'),
}
for a,want in anchors.items():
    i=at(a);assert (i['mnemonic'],i['operands'])==want,(hex(a),i)
assert 0x3F8+8==0x400
assert at(0x285E64)['rip_targets'][0]['address']=='0x209ac30'
assert at(0x28043F)['rip_targets'][0]['address']=='0x209ac30'
assert at(0x287D00)['rip_targets'][0]['address']=='0x209ac10'
assert at(0x286000)['rip_targets'][0]['address']=='0x209ac10'

# Two script dispatch pointers read directly using the existing verifier's table layout.
dispatch=[]
for cid,target in ((0x5BE,0x355940),(0x5BF,0x355E80)):
    va=0x1EED720+cid*0x20;o=ns['off'](va-ns['ib']);raw=ns['raw'][o:o+0x20]
    assert struct.unpack_from('<Q',raw)[0]==target and target in ns['f']
    dispatch.append(dict(call_id=hex(cid),record_address=hex(va),raw_hex=raw.hex(),sha256=sha(raw),handler=hex(target)))

# Reuse complete save-controller evidence, including message12/subtype16 admission.
P=Path('Database/FFXII TZA/_experiments/evidence/spawn-load-continuation')
p=P/'sequence.json';r=json.loads(p.read_text());b=next(b for b in r['bodies'] if b['address']=='0x582860');verify(b)
selected=[]
for a,want in {
    0x582B2C:('mov','rax, qword ptr [rdx + 8]'),
    0x582B40:('sub','rax, 0xf'),0x582B4A:('sub','rax, 1'),0x582B4E:('je','0x582cb3'),
    0x582CB3:('or','dword ptr [rbx + 0xc4], 0x10'),
    0x582CD0:('call','0x285e60'),0x582CE6:('call','0x285e60'),
    0x582E98:('mov','dword ptr [rip + 0x1b17d6e], 1'),0x582EA2:('call','0x5843e0'),
    0x582EBA:('call','0x584210'),0x582EC2:('call','0x582fc0'),
}.items():
    i=at(a,{0x582860:b});assert (i['mnemonic'],i['operands'])==want;selected.append(i)
control=json.loads((P/'check.json').read_text())['tables'][0]
raw=bytes.fromhex(control['bytes']);o=ns['off'](int(control['address'],16)-ns['ib'])
assert raw==ns['raw'][o:o+len(raw)] and sha(raw)==control['sha256']
assert control['targets'][11]=='0x582b2c' and control['targets'][17]=='0x582e81'

# Cached scan only supplies positive leads; whole-body reads above validate these sites.
pidx=Path('Database/Tools/work/FABLE/pub140-scratch/tools/rawcalls.json')
idx=json.loads(pidx.read_text())
assert idx['314530']==['267C90']
for a in (0x28021F,0x36FD28,0x39425C):assert f'{a:X}' in idx['267C90']
refs=Path('Database/Tools/work/h78/rip_data_refs.tsv')
rows=[l for l in refs.read_text().splitlines() if any('\t'+v+'\t' in l for v in ('0209AC10','01E0C3EC','01EED064'))]
assert any(l.startswith('00582860\t0209AC10\twrite\t00582E98') for l in rows)
assert any(l.startswith('00287D00\t0209AC10\twrite\t00287D00') for l in rows)
out=dict(exe_sha256=ns['sha'],method='A only',complete_bodies=13,checks='pass',
    anchors=[at(a) for a in anchors],dispatch_records=dispatch,
    reused_controller=dict(path=p.as_posix(),sha256=sha(p.read_bytes()),body_sha256=b['sha256'],
        instructions=selected,dispatch_table=control),
    positive_leads=dict(rawcalls_path=pidx.as_posix(),rawcalls_sha256=sha(pidx.read_bytes()),
        selected_targets={k:idx[k] for k in ('314530','267C90','287D00')},
        rip_refs_path=refs.as_posix(),rip_refs_sha256=sha(refs.read_bytes()),selected_rip_rows=rows,
        limits='Cached scans are leads, not exhaustive writer/caller proof. The requeue thunk and cited calls are confirmed in exact original bodies.'),
    limits='No B/live run. Handler message/flag structure and local stores/order do not prove message scheduling, pointer lifetime or integrated save-load behavior. Script labels remain catalog labels; authored trial-script decompilation is a follow-up lead.')
(W/'spawn-restore-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:13 complete original bodies, controller bridge, two shipping dispatch records, and positive lead controls. No B/live run.')
