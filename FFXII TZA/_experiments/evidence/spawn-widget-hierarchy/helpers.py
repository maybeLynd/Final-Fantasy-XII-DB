"""Offline spawn lifecycle; reuse exact-body PE and disassembly collector."""
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0, 'Database/Tools/work/ASTRA/python-libs')
import capstone

raw = Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe').read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe = struct.unpack_from('<I', raw, 60)[0]
opt = pe + 24
ib = struct.unpack_from('<Q', raw, opt + 24)[0]
assert ib == 0x120000
st = opt + struct.unpack_from('<H', raw, pe + 20)[0]
sections = []
for i in range(struct.unpack_from('<H', raw, pe + 6)[0]):
    o = st + 40*i
    vs, va, rs, pr = struct.unpack_from('<IIII', raw, o+8)
    sections.append(dict(name=raw[o:o+8].rstrip(b'\0').decode(), va=ib+va, virtual_bytes=vs, raw_bytes=rs, disk_offset=pr))
def off(rva):
    for s in sections:
        d = ib+rva-s['va']
        if 0 <= d < s['raw_bytes']:
            return s['disk_offset'] + d
    raise ValueError(hex(rva))
def zstr(rva):
    start = off(rva)
    end = raw.index(b'\0', start)
    return raw[start:end].decode()
slots = {}
imp_rva, imp_bytes = struct.unpack_from('<II', raw, opt+112+8)
o = off(imp_rva)
while True:
    oft, _, _, name, ft = struct.unpack_from('<IIIII', raw, o)
    if not name: break
    dll = zstr(name)
    t = off(oft or ft)
    k = 0
    while True:
        v = struct.unpack_from('<Q', raw, t+8*k)[0]
        if not v: break
        sym = 'ordinal'+str(v&65535) if v>>63 else zstr(v+2)
        slots[ib+ft+8*k] = dll+'!'+sym
        k += 1
    o += 20
f = {}
for line in Path('Database/Tools/work/graph/functions.tsv').read_text(encoding='utf-8').splitlines()[1:]:
    p=line.split('\t')
    f[int(p[0],16)] = (p[1], int(p[2]))
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
out = dict(exe_sha256=sha, image_base=hex(ib), dll_characteristics=hex(struct.unpack_from('<H', raw, opt+70)[0]), sections=sections, import_count=len(slots), dll_count=len(set(v.split('!')[0] for v in slots.values())), delay_import_directory=struct.unpack_from('<II', raw, opt+112+13*8), selected_imports={hex(k):slots[k] for k in (0x8C2F70,0x8C2B40)}, capstone_version=capstone.__version__, bodies=[])
out['upstream_sources'] = {p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ('Database/Tools/work/graph/functions.tsv',)}
out['direct_VirtualAlloc_imports'] = [v for v in slots.values() if v.split('!')[-1].startswith('VirtualAlloc')]
for a in (0x247950,0x247930,0x244970,0x246C20,0x583930,0x244F50):
    name,n=f[a]
    catalog_n=n
    extent_proof=None
    if a==0x26C8C0:
        # The catalog counts two noncontiguous ranges, excluding two INT3s.
        # Its count is not the end-start extent. Use this exact shipping .pdata row.
        pd=next(s for s in sections if s['name']=='.pdata')
        rows=[]
        for k in range(0,pd['raw_bytes']-11,12):
            start,end,unwind=struct.unpack_from('<III',raw,pd['disk_offset']+k)
            if ib+start==a:
                rows.append((ib+end,ib+unwind,raw[pd['disk_offset']+k:pd['disk_offset']+k+12].hex()))
        assert len(rows)==1 and rows[0][0]==0x26CDF4 and catalog_n==1330
        end,unwind,pdata_hex=rows[0];n=end-a
        extent_proof=dict(source='shipping .pdata',start=hex(a),end_exclusive=hex(end),unwind=hex(unwind),raw_hex=pdata_hex,
            note='1332-byte extent includes INT3 at0026CDED/0026CDF3; catalog instruction-body count is1330, not a contiguous length.')
    b=raw[off(a-ib):off(a-ib)+n]
    dis=list(md.disasm(b,a))
    assert sum(i.size for i in dis)==n, hex(a)
    ins=[]
    for i in dis:
        item=dict(address=hex(i.address), bytes=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str)
        targets=[]
        for op in i.operands:
            if op.type==capstone.x86.X86_OP_MEM and op.mem.base==capstone.x86.X86_REG_RIP:
                t=i.address+i.size+op.mem.disp
                targets.append(dict(address=hex(t), import_name=slots.get(t)))
        if targets:item['rip_targets']=targets
        ins.append(item)
    out['bodies'].append(dict(address=hex(a),name=name,bytes=n,catalog_body_bytes=catalog_n,extent_proof=extent_proof,sha256=hashlib.sha256(b).hexdigest(),instructions=ins))
output=Path(sys.argv[1]) if len(sys.argv)>1 else Path('Database/Tools/work/ASTRA/spawn-widget-hierarchy-helpers.json')
output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='bodies'},indent=2))
for b in out['bodies']:
    print(b['address'],b['name'],b['bytes'],b['sha256'])
    for i in b['instructions']:
        print(i['address'],i['mnemonic'],i['operands'],i.get('rip_targets',''))
