"""Check shipping instruction and table evidence; this is not execution."""
from pathlib import Path
import hashlib, json, struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
ns={};source=(W/'spawn_widget_hierarchy_primary.py').read_text()
exec(compile(source[:source.index('for a in (0x583260')],'<existing PE reader>','exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={int(b['address'],16):b for name in ('primary','helpers','linkage','roots')
     for b in json.loads((W/('spawn-widget-hierarchy-'+name+'.json')).read_text())['bodies']}
assert len(cat)==18
reused=[]
for path,addresses in [('spawn-load-continuation/sequence.json',[0x582860]),
                       ('spawn-restore-request/callers.json',[0x280140]),
                       ('spawn-widget-teardown/helpers.json',[0x244960])]:
    p=E/path;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
    for a in addresses:cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
    reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addresses]))
assert len(cat)==21
for a,b in cat.items():
    pos=a;data=b''
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);data+=d;pos+=len(d)
    o=ns['off'](a-ns['ib'])
    assert data==ns['raw'][o:o+len(data)] and len(data)==b['bytes'] and sha(data)==b['sha256']
    assert b['instructions'][-1]['mnemonic'] in ('ret','jmp','je'),hex(a)
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
anchors={
  0x247CF2:('mov','ebp, 3'),0x247D1D:('xor','r14d, r14d'),0x247D2C:('mov','esi, r14d'),
  0x247D40:('mov','qword ptr [rsp + 0x58], rsi'),0x247D9A:('call','0x2465f0'),
  0x247D9F:('mov','qword ptr [rdi], rbx'),0x247DA2:('inc','rsi'),
  0x247DAC:('add','rdi, 8'),0x247DB0:('sub','rbp, 1'),0x247DB4:('jne','0x247d40'),
  0x250630:('mov','rcx, qword ptr [rdi]'),0x250633:('cmp','qword ptr [rcx + 0x18], 0'),
  0x25063F:('add','rdi, 8'),0x250643:('sub','rbp, 1'),0x250647:('jne','0x250630'),
  0x250675:('mov','rcx, qword ptr [rbx]'),0x25067F:('call','0x244970'),
  0x250684:('add','rbx, 8'),0x250688:('sub','rsi, 1'),0x25068C:('jne','0x250675'),
  0x24795C:('cmp','qword ptr [rcx + 0x10], 0'),0x247963:('and','dword ptr [rcx + 0x40], 0xfffffffd'),
  0x247967:('and','edx, 1'),0x247975:('jmp','0x248220'),0x24797A:('jmp','0x247870'),
  0x24825C:('mov','qword ptr [rcx + 0x20], rsi'),0x248260:('mov','qword ptr [rdx + 0x28], rcx'),
  0x248264:('inc','dword ptr [rbx + 0x30]'),0x248267:('mov','qword ptr [rdx + 0x10], rbx'),
  0x2482CC:('or','dword ptr [rbx + 0x40], 0x2000'),0x244965:('je','0x248220'),
  0x246626:('call','0x861ec0'),0x246748:('call','rax'),
  0x583950:('mov','ecx, 0x5a0'),0x583974:('call','0x244f50'),
  0x583283:('mov','ecx, 0x178'),0x583295:('call','0x244f50'),
  0x582A14:('call','0x244960'),0x582A1E:('call','0x247870'),
  0x2804CA:('call','0x247950'),0x280033:('call','0x247950'),
  0x280335:('call','0x245020'),0x28033A:('mov','rax, qword ptr [rbx + 0xc0]'),
  0x244996:('call','0x2479b0'),0x2449A9:('call','0x246c20'),
  0x2449B8:('cmp','al, 1'),0x2449BF:('test','al, 0x40'),0x2449CB:('jmp','0x245020'),
  0x246FC1:('test','edx, edx'),0x247002:('jg','0x24707f'),
  0x24701E:('mov','dword ptr [rsp + 0x28], 0x13'),0x247029:('mov','dword ptr [rbx + 0x7c], ecx'),
  0x247050:('mov','dword ptr [rsp + 0x28], 0x14'),0x24705B:('mov','dword ptr [rbx + 0x7c], ecx'),
  0x24706B:('call','rax'),0x247079:('and','dword ptr [rbx + 0x7c], 0xffffffcf'),
  0x247A11:('movsx','ecx, word ptr [rdx + 0x44]'),0x247A4C:('call','0x249ce0'),
  0x247A58:('mov','qword ptr [rdi + 0x18], rax'),
  0x244610:('mov','eax, dword ptr [rdx]'),0x244612:('sub','eax, dword ptr [rcx]'),
  0x24874E:('call','0x245020'),0x27FD62:('call','0x245020'),
}
for a,want in anchors.items():
    i=at(a);assert (i['mnemonic'],i['operands'])==want,(hex(a),i)
rips={0x247D20:0x208EA20,0x247D93:0x2445D0,0x25061C:0x208EA20,
      0x247950:0x208EA28,0x58395A:0x582860,0x583288:0x57E4D0,0x582A0A:0x208EA28,
      0x28030E:0x208EA30,0x280320:0x208EA20,0x246C4A:0x915120}
for a,target in rips.items():assert int(at(a)['rip_targets'][0]['address'],16)==target
# Positive root-array reader and unrelated direct root store expose why the old
# exact-address/RIP-only null claim cannot cover the register-walk writer.
assert int(at(0x247E11)['rip_targets'][0]['address'],16)==0x208EA38
assert not any(i['operands']=='0x245020' for i in cat[0x247950]['instructions'])
assert any(i['operands']=='0x245020' for i in cat[0x244980]['instructions'])
tpath=E/'spawn-load-continuation/check.json';t=json.loads(tpath.read_text())['tables'][0]
a=int(t['address'],16);data=bytes.fromhex(t['bytes']);o=ns['off'](a-ns['ib'])
assert data==ns['raw'][o:o+len(data)] and sha(data)==t['sha256']
assert t['targets'][0]=='0x5828ac' and t['targets'][15]=='0x5829c0' and t['targets'][17]=='0x582e81'
reused.append(dict(path=tpath.as_posix(),sha256=sha(tpath.read_bytes()),table=t))
# Existing EXP069 has the complete generic caller, but its factory was a stub.
p=E/'EXP-069-ui-native-feedback/disassembly.txt'
assert p.exists();reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),limit='Earlier B caller evidence only; factory stub does not establish native topology.'))
o=ns['off'](0x915120-ns['ib']);msg=ns['raw'][o:o+24]
assert struct.unpack('<QQQ',msg)==(25,0,0)
out=dict(exe_sha256=ns['sha'],method='A only; no instructions executed',checks='pass',
    new_complete_bodies=18,reused_complete_bodies=3,
    bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],
    anchors=[at(a) for a in anchors],rip_anchors=[at(a) for a in rips],
    message25=dict(address='0x915120',raw_hex=msg.hex(),sha256=sha(msg)),reused=reused,
    distinguishing_evidence='Three-iteration RDI pointer walk writes 208EA20,208EA28,208EA30; 248220 dereferences RCX. The permanent-null/ignored-manager claim is false at original-code level.',
    limits='No live initialized root values, ordinary load delivery order, native resource completion or callback effects. Local attach, sort preparation and completion are separate from execution frequency, actual topology and parity.')
(W/'spawn-widget-hierarchy-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:18 new and3 reused shipping bodies, indexed root writer/read controls, attach and completion branches; no B/live execution.')
