import hashlib,json,struct
from pathlib import Path
W=Path('Database/Tools/work/ASTRA');ns={}
s=(W/'spawn_load_area_primary.py').read_text()
exec(compile(s[:s.index('for a in (0x1831A0')],str(W/'spawn_load_area_primary.py'),'exec'),ns)
cat={int(b['address'],16):b for n in ('primary','callees')
     for b in json.loads((W/('spawn-load-area-'+n+'.json')).read_text())['bodies']}
for a,b in cat.items():
    raw=b'';pos=a
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        d=bytes.fromhex(i['bytes']);pos+=len(d);raw+=d
    assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
    assert b['instructions'][-1]['mnemonic'] in ('ret','jmp')
def calls(a):return [(i['address'],i['operands']) for i in cat[a]['instructions'] if i['mnemonic'] in ('call','jmp')]
assert ('0x267136','0x2342f0') in calls(0x266D10)
assert ('0x26cec6','0x2342f0') in calls(0x26CE60)
assert not any(t=='0x2342f0' for a in (0x1831A0,0x182D40,0x1D8A60,0x1D8A90,0x198790,0x1986E0) for _,t in calls(a))
assert cat[0x290180]['instructions'][0]['operands']=='eax, 2'
reads=[]
for a,n in ((0x16D6A0,3),(0xD1181C,4),(0x9002BC,4),(0x1CEBC08,4),(0x1CEBDA0,16)):
    o=ns['off'](a-ns['ib']);raw=ns['raw'][o:o+n]
    item=dict(address=hex(a),bytes=raw.hex(),sha256=hashlib.sha256(raw).hexdigest())
    if n==4:item['float']=struct.unpack('<f',raw)[0]
    if a==0x16D6A0:
        dis=list(ns['md'].disasm(raw,a));assert sum(i.size for i in dis)==3
        item['instructions']=[dict(address=hex(i.address),mnemonic=i.mnemonic,operands=i.op_str) for i in dis]
        assert dis[-1].mnemonic=='ret' and all(i.mnemonic in ('ret','nop') for i in dis)
    reads.append(item)
out=dict(exe_sha256=ns['sha'],complete_catalog_bodies=len(cat),extra_complete_guard_body=True,
    constants_and_guard=reads,method='A only',limits='Local complete bodies and call-edge controls, not global scheduling or live pointer validity.',checks='pass')
(W/'spawn-load-area-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
