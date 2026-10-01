"""Reconcile retained original-process reads; never opens the game or replays code."""
import csv
import hashlib
import json
from pathlib import Path
import struct

E = Path(__file__).resolve().parent
R = E.parents[4]
load = lambda n: json.loads((E/n).read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
rows = lambda n: list(csv.DictReader((l for l in (E/n).read_text().splitlines()
                                    if not l.startswith('#')), delimiter='\t'))
expected = {r['class_leaf']: r for r in rows('phyre-default-instances.tsv')}
capture = load('title-defaults.json')
assert len(expected) == 173
assert capture['status'] == 'OBSERVED' and capture['defaults_only'] is True
assert capture['requested_descriptors'] == capture['requested_default_spans'] == 173
ds = capture['descriptors']
assert len(ds) == 173 and {d['name'] for d in ds} == set(expected)
assert len({d['target']['address'] for d in ds}) == 173
for name in ('title-pilot-readable.json', 'title-defaults.json'):
    c = load(name)
    assert c['status'] == 'OBSERVED' and c['read_handle_closed'] is True
    assert c['null_read_rejected'] is True and c['debugger_present'] is False
    assert c['pid'] == load('process.json')['pid']
    assert c['image_base'] == 0x120000
    assert c['exe_sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    assert c['module_verdict'] == c['module_verdict_after'] == 'clean'
    assert c['modules_before'] == c['modules_after'] and c['modules_before']
    for side in ('before','after'):
        t = c['text_'+side]
        assert t['matches'] and t['bytes'] == 7996981
        assert t['disk_sha256'] == t['live_sha256'] == '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
    for read in c['reads']:
        assert read['hex'] is not None and len(bytes.fromhex(read['hex'])) == read['size']
        assert c['start_unix'] <= read['start_unix'] <= read['end_unix'] <= c['end_unix']
    controls = [r for r in c['reads'] if r['purpose'] in ('nonzero positive','positive-after')]
    assert len(controls) == 2 and all(r['address']==0x1CCD300 and r['hex']=='19930d0a1a0a' for r in controls)
    for path,digest in c['tool_hashes'].items():
        file=R/path
        if file.name=='observe.py' and name=='title-pilot-readable.json':
            file=E/'observe-before-default-scope.py'
        assert sha(file.read_bytes()) == digest, path

def reads(address, purpose):
    return [r for r in capture['reads'] if r['address']==address and r['purpose']==purpose]

name_bytes={}
for r in capture['reads']:
    if r['purpose']=='class-name-byte':
        value=bytes.fromhex(r['hex'])
        assert r['address'] not in name_bytes or name_bytes[r['address']]==value
        name_bytes[r['address']]=value
def raw_name(pointer):
    result=bytearray()
    for offset in range(256):
        value=name_bytes[pointer+offset]
        if value==b'\0':
            return result.decode('ascii')
        result+=value
    raise AssertionError('unterminated captured name')

names = {d['target']['address']: d['name'] for d in ds}
names.update({p['address']: p['name'] for p in capture['extra_parents']})
graph = {d['target']['address']: d['fields']['parent'] for d in ds}
graph.update({p['address']: p['fields']['parent'] for p in capture['extra_parents']})
for p in capture['extra_parents']:
    saved=reads(p['address'],'ancestor-descriptor')
    assert len(saved)==1
    raw=bytes.fromhex(saved[0]['hex'])
    assert struct.unpack_from('<Q',raw,0x78)[0]==p['fields']['parent']
    assert struct.unpack_from('<I',raw,0x38)[0]==p['fields']['size']
    assert raw_name(struct.unpack_from('<Q',raw,0x30)[0])==p['name']
for address in graph:
    seen=set()
    while address:
        assert address not in seen, 'cycle in observed parent graph'
        seen.add(address)
        assert address in graph, 'unobserved ancestor'
        address=graph[address]

blob=bytearray()
normalized=[]
for d in ds:
    row=expected[d['name']]
    address=int(row['descriptor'],16)
    bfr,afr=reads(address,'descriptor-before'),reads(address,'descriptor-after')
    assert len(bfr)==len(afr)==1
    raw=bytes.fromhex(bfr[0]['hex'])
    assert raw==bytes.fromhex(afr[0]['hex']) and d['header_bracket_matches'] is True
    q=lambda off:struct.unpack_from('<Q',raw,off)[0]
    assert raw_name(q(0x30))==d['name']
    size=struct.unpack_from('<I',raw,0x38)[0]
    flags=struct.unpack_from('<I',raw,0xFC)[0]
    assert d['target']['address']==address and size==int(row['instance_size'],0)==d['fields']['size']
    assert q(0xC0)==int(row['default_instance'],16)==d['fields']['default_pointer']
    assert q(0x78)==d['fields']['parent'] and flags==d['fields']['flags']
    data=reads(q(0xC0),'default-buffer')
    assert len(data)==1 and data[0]['hex']==d['default_hex']
    value=bytes.fromhex(data[0]['hex'])
    assert len(value)==size and d['prepared_bit31']==bool(flags&0x80000000)
    assert d['nonzero_bytes']==sum(b!=0 for b in value)
    normalized.append(dict(name=d['name'],descriptor=f'{address:08X}',size=size,
          default_pointer=f'{q(0xC0):08X}',flags=f'{flags:08X}',prepared_bit31=int(bool(flags&0x80000000)),
          parent=f'{q(0x78):08X}',parent_name=names.get(q(0x78),''),
          static_parent=d['target']['expected_parent'],nonzero_bytes=d['nonzero_bytes'],
          all_a5=int(set(value)=={0xA5}),blob_offset=len(blob),sha256=sha(value)))
    blob+=value
assert len(blob)==34392
# Invalid attempts remain invalid, and do not contribute to the promoted census.
assert load('title-pilot.json')['status']=='INVALID' and load('title-pilot.json')['module_verdict']=='unreadable'
failed=load('title-full.json')
assert failed['status']=='INVALID' and failed['read_handle_closed'] is True
assert failed['requested_descriptors']==177 and not failed['descriptors']
bad=next(r for r in failed['reads'] if r['purpose']=='descriptor-before')
assert bad['address']==0x02CF6678
assert struct.unpack_from('<Q',bytes.fromhex(bad['hex']),0x30)[0]==0x10
assert failed['reads'][-1]['address']==0x10 and failed['reads'][-1]['hex'] is None
cleanup=load('cleanup.json');before=load('save-before.json')
assert cleanup['status']=='RESTORED' and cleanup['processes']==[]
assert cleanup['files']==before['files'] and len(before['files'])==26 and cleanup['backup_unchanged']
assert cleanup['changed_keys']==['LUIDLow'] and load('cloud-before.json')['cloudEnabled'] is False
(E/'defaults.bin').write_bytes(blob)
with (E/'defaults.tsv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(normalized[0]),delimiter='\t',lineterminator='\n')
    writer.writeheader();writer.writerows(normalized)
result=dict(status='PASS_BOUNDED_RETAINED_REVIEW',method='A: review of retained C observations; no new execution',
            captured_defaults=173,bytes=len(blob),prepared=sum(r['prepared_bit31'] for r in normalized),
            unprepared=[r['name'] for r in normalized if not r['prepared_bit31']],
            nonzero_buffers=sum(r['nonzero_bytes']>0 for r in normalized),
            prepared_zero_buffers=sum(r['prepared_bit31'] and not r['nonzero_bytes'] for r in normalized),
            all_a5=[r['name'] for r in normalized if r['all_a5']],
            explicit_static_parent_matches=sum(bool(r['static_parent']) and int(r['static_parent'],16)==int(r['parent'],16) for r in normalized),
            blank_static_parent_to_PBase=sum(not r['static_parent'] and r['parent_name']=='PBase' for r in normalized),
            extra_ancestors=len(capture['extra_parents']),observed_graph_acyclic=True,
            limitation='One title-state census, sequential reads; seven unprepared buffers unresolved. Four non-default sized rows not qualified; first failed supplied descriptor mapping. No constructor/copy execution or general lifetime claim.',
            raw_capture_sha256=sha((E/'title-defaults.json').read_bytes()),defaults_blob_sha256=sha(blob))
# Derive the actual four omitted names from the two pinned populations.
sized={r['class_leaf'] for r in rows('phyre-class-instance-sizes.tsv')}
result['unresolved_sized_classes']=sorted(sized-set(expected))
(E/'review.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
