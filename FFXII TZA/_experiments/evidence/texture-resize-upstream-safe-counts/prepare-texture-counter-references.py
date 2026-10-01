"""Bounded original reference candidates for the known element-counter getter.

Not a complete writer/caller proof: raw rel32/abs64/RIP-LEA patterns require
function/table validation. Controls are two retained direct calls and a known
RTTI-bound virtual slot. Reuse before considering any process watch.
"""
import hashlib,json,pathlib,struct,sys
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else W/'texture-counter-reference-preparation-01.json'
if not out.resolve().is_relative_to(W.resolve()):raise ValueError('output outside owned work leaf')
if out.exists():raise ValueError('immutable preparation exists')
d=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if hashlib.sha256(d).hexdigest()!=SHA:raise ValueError('wrong shipping image')
p=struct.unpack_from('<I',d,60)[0];ns=struct.unpack_from('<H',d,p+6)[0];opt=struct.unpack_from('<H',d,p+20)[0];secs=[]
for k in range(ns):
    z=p+24+opt+40*k;name=d[z:z+8].split(b'\0')[0].decode();vs,va,rs,ro=struct.unpack_from('<IIII',d,z+8);secs.append((name,va,rs,ro))
def read(a,n):
    for name,va,rs,ro in secs:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('whole source range not backed')
md=Cs(CS_ARCH_X86,CS_MODE_64);targets=tuple(dict.fromkeys([0x623DF0,0x621FF0]+[int(t,16) for t in sys.argv[2:]]));records=[]
for name,va,rs,ro in secs:
    data=d[ro:ro+rs];base=0x120000+va
    for target in targets:
        key=struct.pack('<Q',target);start=0
        while True:
            at=data.find(key,start)
            if at<0:break
            records.append(dict(kind='raw_abs64',target=hex(target),pc=hex(base+at),section=name,aligned8=(base+at)%8==0,nearby_address=hex(base+max(0,at-24)),nearby_bytes=data[max(0,at-24):min(len(data),at+40)].hex()));start=at+1
    if name!='.text':continue
    for opcode in [0xE8,0xE9]:
        start=0
        while True:
            at=data.find(bytes([opcode]),start)
            if at<0:break
            start=at+1
            if at+5>len(data):continue
            target=base+at+5+struct.unpack_from('<i',data,at+1)[0]
            if target not in targets:continue
            i=next(md.disasm(data[at:at+5],base+at))
            records.append(dict(kind='raw_rel32',target=hex(target),pc=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,section=name))
    for prefix in [b'\x48\x8d',b'\x4c\x8d']:
        start=0
        while True:
            at=data.find(prefix,start)
            if at<0:break
            start=at+1
            if at+7>len(data) or data[at+2]&0xc7!=5:continue
            target=base+at+7+struct.unpack_from('<i',data,at+3)[0]
            if target not in targets:continue
            i=next(md.disasm(data[at:at+7],base+at))
            records.append(dict(kind='raw_rip_lea',target=hex(target),pc=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,section=name))
rawpath=W/'title-cleanup-count-selector-source-01.json'
raw=json.loads(rawpath.read_text())
known=[i for q in raw['ranges'] for i in q['instructions'] if i['mnemonic']=='call' and i['args']=='0x623df0']
if len(known)!=2 or any(not any(r['kind']=='raw_rel32' and r['pc']==i['pc'] and r['bytes']==i['bytes'] for r in records) for i in known):raise ValueError('retained direct-call detection control failed')
if not any(r['kind']=='raw_abs64' and r['pc']=='0xd54348' and r['target']=='0x621ff0' for r in records):raise ValueError('known virtual-slot control failed')
result=dict(status='PREPARATION_ONLY_CONTROLS_VALID',method='A retained shipping reference candidates',exe_sha256=SHA,targets=[hex(t) for t in targets],controls=dict(retained_direct_calls=[i['pc'] for i in known],known_virtual_slot='0xd54348',source_pin=dict(path=rawpath.name,sha256=hashlib.sha256(rawpath.read_bytes()).hexdigest())),references=records,driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),limits='Positive raw candidate detection, not complete references, code alignment, function/table identity, negative write closure or natural reachability. Indexed/computed/RVA/opaque external routes are unclosed. No process/native/game/input/save/config/reference writes.')
out.open('x',encoding='utf-8').write(json.dumps(result,indent=2)+'\n')
print(result['status']);print([(r['kind'],r['pc'],r['target']) for r in records])
