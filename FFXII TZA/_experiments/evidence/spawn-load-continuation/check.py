"""Local source integrity, primary dispatch table and bounded pointer/branch checks."""
import hashlib,json,struct
from pathlib import Path
W=Path('Database/Tools/work/ASTRA')
ns={}
s=(W/'spawn_load_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x5843E0')],str(W/'spawn_load_primary.py'),'exec'),ns)
cat={int(b['address'],16):b for n in ('primary','callees','sequence','metadata-leaves')
     for b in json.loads((W/('spawn-load-'+n+'.json')).read_text())['bodies']}
for a,b in cat.items():
    raw=b'';pos=a
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);pos+=len(d);raw+=d
    assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
    assert b['instructions'][-1]['mnemonic'] in ('ret','jmp')
def at(a):return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
def ops(a):return at(a)['operands']
assert ops(0x584434)=='rcx, [rdi + 0xe440]' and ops(0x584457)=='rcx, [rdi + 0x2e650]'
assert at(0x584440)['mnemonic']=='jmp' and ops(0x584440)=='0x584471'
assert ops(0x236767)=='eax, dword ptr [rax + 4]' and ops(0x23676A)=='eax, 0xc'
assert ops(0x584445)=='0x58444b' and ops(0x584449)=='0x584463'
assert ops(0x269A27)=='edx, 4' and ops(0x25D8E7)=='edx, 4'  # 4*128=512 group copy
assert ops(0x2EF747)=='edx, 0x400' and ops(0x2EF7B6)=='xmmword ptr [rcx], xmm0'
assert ops(0x2EF7C7)=='edx, 4'
active=0x2164280;staging=0x21BA940
assert active+0xE240==0x21724C0 and staging+0xE240==0x21C8B80
assert active+0xE440==0x21726C0 and staging+0xE440==0x21C8D80
tables=[]
for a,n in [(0x582F54,19),(0x582FA0,8)]:
    o=ns['off'](a-ns['ib']);raw=ns['raw'][o:o+4*n]
    vals=struct.unpack('<'+'I'*n,raw)
    tables.append(dict(address=hex(a),bytes=raw.hex(),sha256=hashlib.sha256(raw).hexdigest(),
         targets=[hex(ns['ib']+v) for v in vals]))
    assert all(any(int(i['address'],16)==ns['ib']+v for i in cat[0x582860]['instructions']) for v in vals)
out=dict(exe_sha256=ns['sha'],complete_bodies=len(cat),tables=tables,checks='pass',
    active_base=hex(active),staging_base=hex(staging),group_bytes=4*128,spawn_image_bytes=0x400*128+16,
    limits='Read-only exact instructions/table bytes. No live or isolated execution. Larger controller dependencies not all executed/read.',
    selected_branch_truth=[dict(flag12=a,mode_is3=b,header57_bit0=c,selection=('A' if not a else 'skip' if b and not c else 'B'))
                           for a in (0,1) for b in (0,1) for c in (0,1)])
(W/'spawn-load-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
