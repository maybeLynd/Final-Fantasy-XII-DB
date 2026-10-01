"""Local original-code order and message-byte controls; no execution."""
from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');ns={}
s=(W/'spawn_widget_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x244F00')],str(W/'spawn_widget_primary.py'),'exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={int(b['address'],16):b for name in ('primary','helpers') for b in json.loads((W/('spawn-widget-'+name+'.json')).read_text())['bodies']}
assert len(cat)==9
for a,b in cat.items():
    pos=a;raw=b''
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);raw+=d;pos+=len(d)
    o=ns['off'](a-ns['ib'])
    assert len(raw)==b['bytes'] and sha(raw)==b['sha256'] and raw==ns['raw'][o:o+len(raw)]
    assert b['instructions'][-1]['mnemonic']=='ret'
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
anchors={
    0x244F14:('and','eax, 0x21'),0x244F20:('jmp','0x244dd0'),
    0x244F34:('call','rax'),0x244F39:('call','0x245020'),
    0x245032:('call','0x2448d0'),0x24503F:('call','0x244700'),
    0x245047:('mov','rbx, qword ptr [rdi + 0x18]'),0x24505A:('call','rax'),
    0x245064:('call','0x2473b0'),0x245069:('mov','rbx, qword ptr [rbx + 0x20]'),
    0x245072:('test','byte ptr [rdi + 0x40], 0x20'),0x245085:('jmp','0x2482e0'),
    0x24508C:('call','0x2473f0'),0x245097:('bts','eax, 0xa'),
    0x2473B9:('mov','rbx, qword ptr [rcx + 0x18]'),0x2473C9:('call','rax'),
    0x2473D3:('call','0x2473b0'),0x2473D8:('mov','rbx, qword ptr [rbx + 0x20]'),
    0x244E41:('jne','0x244ef7'),0x244ED7:('and','dword ptr [rbx + 0x7c], 0xfffffff4'),
    0x244EDB:('or','dword ptr [rbx + 0x7c], 4'),0x244EF5:('call','rax'),
    0x2482F7:('mov','rbx, qword ptr [rcx + 0x20]'),0x2482FB:('call','0x2482e0'),
    0x2483B2:('call','rax'),0x2483C2:('call','0x228450'),
    0x2483CA:('mov','rbx, qword ptr [rdi + 8]'),0x2483CE:('mov','qword ptr [rdi], 0'),
    0x2483DE:('call','0x3697f0'),0x2483E9:('mov','byte ptr [rdi + 0xa2], 0'),
    0x248405:('jmp','rax'),0x24741B:('mov','dword ptr [rsp + 0x20], ecx'),
    0x24744E:('call','rax'),0x24746A:('call','0x247490'),
    0x244965:('je','0x248220'),
}
for a,want in anchors.items():
    i=at(a);assert (i['mnemonic'],i['operands'])==want,(hex(a),i)
c=json.loads((W/'spawn-widget-constants.json').read_text());assert c['exe_sha256']==ns['sha']
records=[]
expected={0x915058:15,0x915070:18,0x915040:24,0x1E0C0F8:15}
for r in c['records']:
    a=int(r['address'],16);raw=bytes.fromhex(r['raw_hex']);o=ns['off'](a-ns['ib'])
    assert raw==ns['raw'][o:o+len(raw)]
    if a in expected:assert struct.unpack('<QQQ',raw)==(expected[a],0,0)
    if a==0x1CEBBA8:assert struct.unpack('<f',raw)[0]==1.0
    records.append(dict(r,sha256=sha(raw)))
for a,target in ((0x244F2D,0x915058),(0x245050,0x915070),(0x2473C2,0x915070),
                 (0x244EEB,0x1E0C0F8),(0x2483A8,0x915040)):
    assert int(at(a)['rip_targets'][0]['address'],16)==target
# A whole local body cannot directly perform an omitted call. Do not extend to its callees.
assert not any(i['operands']=='0x245020' for i in cat[0x244DD0]['instructions'] if i['mnemonic'] in ('call','jmp'))
assert any(i['operands']=='0x245020' for i in cat[0x244F00]['instructions'] if i['mnemonic']=='call')
out=dict(exe_sha256=ns['sha'],method='A only',complete_bodies=9,checks='pass',
    anchors=[at(a) for a in anchors],constants=records,
    local_controls='Immediate destroy reaches245020; deferred244DD0 does not directly reach it. Original message15/18/24 constants and callback/cached-child/next-sibling sites checked.',
    limits='No B/live run, callback intervention or initialized hierarchy. Local preorder18 and postorder24/release do not establish actual controller membership, separate-destruction chronology, deferred completion, native callback effects or all message paths.')
(W/'spawn-widget-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:9 complete original bodies and message15/18/24 byte/order controls. No execution.')
