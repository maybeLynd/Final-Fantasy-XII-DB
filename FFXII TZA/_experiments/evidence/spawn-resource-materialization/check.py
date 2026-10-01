from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
s=(W/'spawn_materialization_primary.py').read_text();ns={};exec(compile(s.split('for a in (')[0],'<verified shipping PE reader>','exec'),ns)
sha=lambda b:hashlib.sha256(b).hexdigest()
cat={};sources=[];reused=[]
for name in ('primary','helpers'):
 p=W/('spawn-materialization-'+name+'.json');j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for b in j['bodies']:a=int(b['address'],16);assert a not in cat;cat[a]=b
 sources.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes())))
assert len(cat)==10
for name,addresses in [
 ('spawn-widget-reclaim/primary.json',[0x249660,0x249670]),
 ('spawn-widget-retention/adapters.json',[0x2495C0,0x249320,0x2493D0]),
 ('spawn-widget-retention/helpers.json',[0x393460,0x3933F0]),
 ('spawn-widget-hierarchy/linkage.json',[0x582790]),
]:
 p=E/name;j=json.loads(p.read_text());assert j['exe_sha256']==ns['sha']
 for a in addresses:assert a not in cat;cat[a]=next(b for b in j['bodies'] if int(b['address'],16)==a)
 reused.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),addresses=[hex(a) for a in addresses]))
assert len(cat)==18
for a,b in cat.items():
 pos=a;data=b''
 for i in b['instructions']:
  assert int(i['address'],16)==pos
  d=bytes.fromhex(i['bytes']);data+=d;pos+=len(d)
 o=ns['off'](a-ns['ib']);assert data==ns['raw'][o:o+len(data)] and len(data)==b['bytes'] and sha(data)==b['sha256']
allins={int(i['address'],16):i for b in cat.values() for i in b['instructions']}
anchors={
 0x2495E8:('call','rax'),0x2495EA:('mov','rdi, qword ptr [rbx]'),0x2495ED:('inc','word ptr [rdi + 0x1a]'),
 0x249612:('mov','dword ptr [rsp + 0x20], 0x10'),0x249632:('call','rax'),
 0x249660:('mov','rcx, qword ptr [rcx + 8]'),0x249664:('jmp','0x2a00f0'),
 0x249670:('mov','rdx, qword ptr [rcx + 8]'),0x249674:('mov','rcx, qword ptr [rcx + 0x18]'),0x249678:('jmp','0x24a1d0'),
 0x2A00F6:('cmp','byte ptr [rcx + 3], 1'),0x2A00FD:('je','0x2a016e'),
 0x2A0102:('add','ecx, esi'),0x2A010E:('call','0x20e620'),0x2A0116:('mov','dword ptr [rsi + 8], eax'),
 0x2A0119:('call','0x2a1a80'),0x2A0121:('add','ecx, esi'),0x2A012A:('mov','dword ptr [rsi + 0x28], eax'),
 0x2A012D:('call','0x20e600'),0x2A0137:('cmp','dword ptr [rsi + 0x24], edi'),0x2A013A:('jbe','0x2a0160'),
 0x2A0141:('lea','rbx, [rax + 8]'),0x2A0147:('add','ecx, ebp'),0x2A014E:('mov','dword ptr [rbx], eax'),
 0x2A0150:('lea','rbx, [rbx + 0xc]'),0x2A0159:('jb','0x2a0145'),0x2A016A:('mov','byte ptr [rsi + 3], 1'),
 0x2A1A93:('mov','ecx, dword ptr [rcx + 0x20]'),0x2A1A96:('add','ecx, esi'),0x2A1A9F:('mov','dword ptr [rsi + 0x20], eax'),
 0x2A1AAC:('cmp','dword ptr [rsi + 0x1c], edi'),0x2A1AAF:('jbe','0x2a1ae6'),0x2A1AC0:('movsxd','rcx, edi'),
 0x2A1AC3:('lea','rdx, [rcx + rcx*4]'),0x2A1AC7:('mov','ecx, dword ptr [r14 + rdx*4 + 0x10]'),
 0x2A1ACC:('lea','rbx, [r14 + rdx*4]'),0x2A1AD0:('add','ecx, ebx'),0x2A1AD9:('mov','dword ptr [rbx + 0x10], eax'),
 0x20E600:('mov','eax, ecx'),0x20E626:('mov','eax, ecx'),
 0x24A4F3:('test','byte ptr [rax + 0x38], 0x20'),0x24A4F9:('add','rax, 0x48'),0x24A51F:('cmp','r8d, 0x40'),
 0x24A536:('cmp','r8d, 0x40'),0x24A53A:('jne','0x24a53f'),0x24A53C:('xor','eax, eax'),
 0x24A53F:('test','rcx, rcx'),0x24A550:('movzx','ecx, byte ptr [r9]'),0x24A55E:('jne','0x24a550'),
 0x24A56C:('and','r10d, 0xf'),0x24A570:('and','ecx, 0x3ff10'),0x24A576:('mov','qword ptr [rax + 0x28], r11'),
 0x24A57D:('mov','qword ptr [rax + 0x40], r11'),0x24A581:('or','ecx, 0xa0'),
 0x24A1E7:('movzx','eax, word ptr [rdx + 0x1c]'),0x24A1EB:('lea','rsi, [rdx + 0x10]'),
 0x24A1EF:('mov','edi, dword ptr [rsi + 8]'),0x24A1F5:('add','rax, rsi'),0x24A1FB:('add','rdi, rax'),
 0x24A202:('shr','rax, 0x14'),0x24A210:('and','eax, 0x3f00'),0x24A21C:('shr','rcx, 0x33'),
 0x24A226:('and','ecx, 0x3c000'),0x24A22C:('mov','qword ptr [rbx + 0x18], rdx'),0x24A238:('mov','qword ptr [rbx + 0x20], rsi'),
 0x24A271:('sub','eax, 0x13'),0x24A274:('je','0x24a3b9'),0x24A27A:('cmp','eax, 1'),0x24A27D:('jne','0x24a427'),
 0x24A287:('movzx','esi, word ptr [rsi + 0xe]'),0x24A298:('mov','esi, ecx'),0x24A29A:('mov','rdi, rax'),0x24A29D:('shr','esi, 0x12'),
 0x24A2AD:('lea','ecx, [rsi + 0xff]'),0x24A2B3:('shr','ecx, 8'),0x24A2B6:('shl','ecx, 0xa'),0x24A2B9:('call','0x36a190'),
 0x24A2CC:('shr','r8, 4'),0x24A2D3:('je','0x24a330'),0x24A2E6:('lea','rdi, [rdi + 0x40]'),
 0x24A2EA:('and','eax, 1'),0x24A2F0:('sar','ecx, 1'),0x24A2F5:('shl','ecx, 5'),0x24A2F8:('lea','edx, [rax*8]'),
 0x24A304:('movups','xmmword ptr [rbp + rax*4], xmm0'),0x24A312:('lea','eax, [rdx + 0x10]'),
 0x24A339:('mov','qword ptr [rbx + 0x10], rbp'),0x24A34E:('call','0x181190'),0x24A380:('call','0x180e70'),0x24A3B2:('call','0x180e70'),
 0x24A3C2:('mov','qword ptr [rbx + 0x10], rdi'),0x24A3D7:('call','0x181250'),0x24A422:('call','0x181000'),
 0x24A427:('or','dword ptr [rbx + 0x38], 0x40'),
 0x181214:('inc','ax'),0x181217:('inc','r9w'),0x181223:('call','0x183ee0'),0x181248:('jmp','0x1b21d0'),
 0x1812D4:('inc','ax'),0x1812D7:('inc','r9w'),0x1812E3:('call','0x184140'),0x181308:('jmp','0x1b21d0'),
 0x180EA9:('sar','eax, 4'),0x180EB4:('jle','0x180fd0'),0x180F75:('jl','0x180f20'),0x180F8E:('call','0x17f3b0'),
 0x180FAC:('call','0x1b20b0'),0x180FB3:('add','rsi, 0x40'),
 0x181039:('sar','eax, 8'),0x181044:('jle','0x181167'),0x181122:('call','0x17f3b0'),0x181140:('call','0x1b20b0'),0x181147:('add','rsi, 0x400'),
 0x39349A:('mov','r8d, dword ptr [rbx - 0x10]'),0x3934AE:('lea','edx, [r9 + 5]'),0x3934B2:('call','0x2493d0'),
 0x3934C4:('mov','dword ptr [rax + 0x40], ecx'),0x393424:('mov','edx, 7'),0x39342C:('call','0x249320'),
 0x2493EF:('call','0x24a4e0'),0x2493FB:('mov','qword ptr [rbx + 0x18], rax'),
}
for a,w in anchors.items():i=allins[a];assert (i['mnemonic'],i['operands'])==w,(hex(a),i)
rips={0x20E602:0x1F83530,0x20E620:0x1F83530,0x24A4E3:0x208F580,0x24A58A:0x2090780,
 0x5827AF:0xD23D80,0x5827CE:0xD23D98,0x249337:0x249660,0x2493F4:0x249670}
for a,t in rips.items():assert int(allins[a]['rip_targets'][0]['address'],16)==t
inputs=json.loads((W/'spawn-materialization-inputs.json').read_text());assert inputs['exe_sha256']==ns['sha'] and len(inputs['records'])==3
for r in inputs['records']:
 a=int(r['address'],16);d=bytes.fromhex(r['raw_hex']);o=ns['off'](a-ns['ib'])
 assert ns['raw'][o:o+len(d)]==d and sha(d)==r['sha256'] and len(d)==r['bytes']
assert struct.unpack('<IIQII',bytes.fromhex(inputs['records'][0]['raw_hex']))==(127,0,0xD23EB8,0,0)
assert struct.unpack('<I',bytes.fromhex(inputs['records'][1]['raw_hex']))==(111,)
assert bytes.fromhex(inputs['records'][2]['raw_hex'])==b'dataface_c\0'
# Branch controls are original opposite paths, not a rewritten implementation.
assert int(allins[0x2A00FD]['operands'],16)>0x2A016A
assert allins[0x24A274]['operands']=='0x24a3b9' and allins[0x24A27D]['operands']=='0x24a427'
assert 0x2495E8<0x2495ED<0x249632
assert allins[0x2A0147]['operands']=='ecx, ebp' and allins[0x2A1AD0]['operands']=='ecx, ebx'
out=dict(exe_sha256=ns['sha'],method='A only; no original instructions executed',checks='pass',collected_complete_bodies=10,reused_complete_bodies=8,
 sources=sources,reused=reused,bodies=[dict(address=hex(a),bytes=b['bytes'],sha256=b['sha256']) for a,b in cat.items()],
 anchors=[allins[a] for a in anchors],rip_anchors=[allins[a] for a in rips],inputs=inputs,
 conclusion='Native member callbacks perform guarded relocation or header-driven record/data preparation before batch count/ready16. Reference bases differ between nested tables. Other format values skip both detailed conversion arms but still set object flag6; no success result is tested by the member adapter.',
 limits='Not asset-file validation, complete format identification, actual allocation/input address proof, renderer/GPU effects, initialized native resource delivery or integrated parity. Downstream183EE0/184140/17F3B0/1B21D0/1B20B0 remain separate native boundaries; no live or B run.')
(W/'spawn-materialization-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS:10 collected/8 reused shipping bodies, opposite relocation/format gates, distinct nested reference bases, raw load descriptors and callback-before-ready order. Method A only.')
