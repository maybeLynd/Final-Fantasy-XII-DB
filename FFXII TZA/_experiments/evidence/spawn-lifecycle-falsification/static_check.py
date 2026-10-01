"""Check retained complete bodies and local control-flow discriminators, not global reachability."""
import hashlib,json
from pathlib import Path
W=Path('Database/Tools/work/ASTRA')
sources=[W/('spawn-lifecycle-'+n+'.json') for n in ('primary','callees')]
cat={int(b['address'],16):b for p in sources for b in json.loads(p.read_text())['bodies']}
for a,b in cat.items():
    pos=a;raw=b''
    for i in b['instructions']:
        assert int(i['address'],16)==pos
        part=bytes.fromhex(i['bytes']);pos+=len(part);raw+=part
    assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
    assert b['instructions'][-1]['mnemonic'] in ('ret','jmp')
area=cat[0x234AF0]
ins={int(i['address'],16):i for i in area['instructions']}
def reachable(start):
    pending=[start];seen=set()
    while pending:
        a=pending.pop()
        if a in seen:continue
        assert a in ins,hex(a)
        seen.add(a);i=ins[a];mn=i['mnemonic'];nxt=a+len(bytes.fromhex(i['bytes']))
        if mn=='ret':continue
        if mn.startswith('j'):
            pending.append(int(i['operands'],16))
            if mn!='jmp':pending.append(nxt)
        else:pending.append(nxt)
    return seen
ra=reachable(0x234C43);rp=reachable(0x234BC8)
assert 0x234C37 not in ra and 0x234C37 in rp
assert {a for a in ra if ins[a]['mnemonic']=='call' and ins[a]['operands']=='0x328370'}=={0x234C43,0x234C6C}
def at(a):
    return next(i for b in cat.values() for i in b['instructions'] if int(i['address'],16)==a)
assert at(0x234B55)['operands']=='0x3209c0' and at(0x234B5C)['mnemonic']=='js'
assert at(0x3209C7)['operands']=='edx, ecx' and at(0x3209C9)['operands']=='ecx, ecx'
assert at(0x234C57)['operands']=='ecx' and at(0x234C76)['operands']=='r15d'
assert at(0x233803)['mnemonic']=='ja' and at(0x2337F0)['operands'].startswith('ecx, dword ptr')
assert at(0x2351B9)['mnemonic']=='jbe' and at(0x235280)['mnemonic']=='ja'
assert at(0x2358EB)['operands']=='qword ptr [rsi], r10' and at(0x23581D)['operands']=='r10, 0x2200000000000'
# Positive control: serializer has both pointer globals; restorer only bank 2.
def refs(a):return {int(t['address'],16) for i in cat[a]['instructions'] for t in i.get('rip_targets',[])}
assert {0x208E690,0x208E698}<=refs(0x233440)
assert 0x208E698 in refs(0x233550) and 0x208E690 not in refs(0x233550)
assert {0x2089370,0x2089372}<=refs(0x233440)&refs(0x233550)
assert not ({0x2089374,0x208936C}&(refs(0x233440)|refs(0x233550)))
out=dict(complete_bodies=len(cat),body_integrity=True,area_cfg_nodes=len(ra),point_cfg_nodes=len(rp),
    point_validator_positive_control=True,area_validator_absent=True,serializer_two_bank_positive_control=True,
    restorer_only_bank2_local_refs=True,limits='Complete local CFG and direct references, not global alias or caller proof.',
    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})
(W/'spawn-lifecycle-static-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
