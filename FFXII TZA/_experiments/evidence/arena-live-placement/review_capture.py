"""Review saved EXP079 bytes only. Does not import a runtime or execute game code."""
from pathlib import Path
import hashlib, json, struct

root = Path(__file__).resolve().parent
repo = root.parents[4]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda name: json.loads((root / name).read_text())
owner = read('process.json')
captures = [read(label + '-memory.json') for label in ('title', 'loaded')]
assert len(captures) == 2
result = dict(method='Saved-data reconciliation only; no live reads or game-code execution.',
              observations=[], limits=['Reads are sequential, not atomic.',
              'Decoded link targets were not generally read.',
              'Enabled mask does not prove a usable allocator; arena7 is an explicit exception.',
              'Module names and EXE text identity do not prove all process memory is unmodified.'])
total_spans = 0
for cap in captures:
    assert cap['pid'] == owner['pid'] and cap['status'] == 'OBSERVED'
    assert cap['exe_sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    assert cap['image_base'] == 0x120000
    assert cap['known_read_control'] == '19930d0a1a0a'
    assert cap['null_read_rejected'] is True and cap['read_handle_closed'] is True
    assert cap['modules'] == captures[0]['modules'] and len(cap['modules']) == 101
    assert cap['modules'][0] == owner['path'].lower()
    assert cap['watched_modules'] == []
    assert any(p.endswith('\\gameoverlayrenderer64.dll') for p in cap['modules'])
    for path, digest in cap['tool_hashes'].items():
        assert sha(repo / path) == digest, path
    assert cap['code_identity'] == [dict(address=0x121000, bytes=7996981,
        disk_sha256='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4',
        live_sha256='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4', matches=True)]
    assert len(cap['samples']) == 2 and cap['start_unix'] < cap['end_unix']
    for index, sample in enumerate(cap['samples']):
        assert cap['start_unix'] <= sample['start_unix'] <= sample['end_unix'] <= cap['end_unix']
        raw = {}
        for name, address, length in [('base', 0x1f83530, 8), ('selector', 0x22d89a8, 32),
                                      ('arenas', 0x22d7fd0, 15 * 0xa8)]:
            assert sample[name]['address'] == address
            raw[name] = bytes.fromhex(sample[name]['bytes'])
            assert len(raw[name]) == length
        base, = struct.unpack('<Q', raw['base'])
        mask, selected = struct.unpack_from('<Ii', raw['selector'], 0x10)
        assert base == sample['decoder_base'] == 0
        assert raw['selector'][:15] == bytes(range(15))
        assert selected == sample['selected_arena'] == 2
        assert mask == sample['enabled_mask'] == (0x2bfc if cap['label'] == 'title' else 0x6bfc)
        assert raw['selector'].hex() == sample['selector_after']
        assert raw['base'].hex() == sample['base_after']
        ids = [i for i in range(15) if mask & (1 << i)]
        assert ids == [r['id'] for r in sample['enabled_records']]
        observed = dict(label=cap['label'], sample=index, mask=hex(mask), map=list(raw['selector'][:15]),
                        base=base, selected=selected, arenas=[])
        seen_bytes = {}
        for record in sample['enabled_records']:
            arena = record['id']
            b = raw['arenas'][arena * 0xa8:(arena + 1) * 0xa8]
            fields = {hex(o): struct.unpack_from('<Q', b, o)[0]
                      for o in (8, 0x20, 0x28, 0x30, 0x38, 0x40, 0x90, 0x98)}
            assert record['fields'] == fields
            assert 0 < fields['0x8'] < 0x80000000
            assert all(0 <= p < 0x80000000 for p in fields.values())
            expected_fields = [hex(o) for o in (8, 0x38, 0x90, 0x98) if fields[hex(o)]]
            assert expected_fields == [p['field'] for p in record['pointed_bytes']]
            a = dict(id=arena, backing=hex(fields['0x8']), inspected=[])
            for p in record['pointed_bytes']:
                assert p['address'] == fields[p['field']] and p['bytes'] is not None
                data = bytes.fromhex(p['bytes'])
                assert len(data) == 64
                total_spans += 1
                for offset, byte in enumerate(data):
                    address = p['address'] + offset
                    assert address not in seen_bytes or seen_bytes[address] == byte
                    seen_bytes[address] = byte
                item = dict(field=p['field'], address=hex(p['address']), prefix=data[:8].hex())
                if p['field'] != '0x8' and data[:2] == b'\x12\xff':
                    assert data[3] == arena
                    refs = {hex(o): struct.unpack_from('<I', data, o)[0] for o in (4, 8, 12, 16)}
                    assert all(x < 0x80000000 for x in refs.values())
                    item['header_links_u32'] = refs
                    item['decode_limit'] = 'Base zero: nonzero references numerically retain their address; target lifetime not tested.'
                elif arena == 7 and p['field'] != '0x8':
                    assert data == bytes(64)
                    item['meaning'] = 'Readable zero bytes; not an FF12 block header.'
                elif p['field'] != '0x8':
                    raise AssertionError(('Unreviewed non-header', arena, p))
                if p['field'] == '0x8':
                    if arena == 7:
                        assert data.startswith(b'EFX0010\0')
                    else:
                        expected = f'TKMALLOC EXECSPACE={arena:02d}/START ADRS={p["address"]:016X}'.encode()
                        assert data.startswith(expected)
                a['inspected'].append(item)
            if arena == 9:
                assert fields['0x90'] == fields['0x98'] == 0
            if arena in (13, 14):
                assert all(fields[hex(o)] == 0 for o in (0x30, 0x38, 0x40))
            observed['arenas'].append(a)
        result['observations'].append(observed)
    assert cap['samples'][0]['arenas'] == cap['samples'][1]['arenas']
assert total_spans == 154
title = {r['id']: r['fields']['0x8'] for r in captures[0]['samples'][0]['enabled_records']}
loaded = {r['id']: r['fields']['0x8'] for r in captures[1]['samples'][0]['enabled_records']}
assert set(loaded) - set(title) == {14} and not set(title) - set(loaded)
assert [i for i in title if title[i] != loaded[i]] == [11]
assert (title[11], loaded[11], loaded[14]) == (0x7c5d3040, 0x7c5d2040, 0x6610ef40)
before, cleanup = read('save-before.json'), read('cleanup.json')
assert len(before['files']) == 26 and before['files'] == cleanup['files']
assert cleanup['status'] == 'RESTORED' and cleanup['processes'] == [] and cleanup['backup_unchanged'] is True
assert cleanup['changed'] == ['76561198045890736\\GameSetting.ini'] and cleanup['changed_keys'] == ['LUIDLow']
assert read('cloud-before.json')['cloudEnabled'] is False and read('cloud-after.json')['cloudEnabled'] is False
assert read('exit-check.json')['exited'] is False  # Preserve the intermediate failed exit check.
assert read('cleanup-first-attempt.json')['status'] == 'STOPPED_BEFORE_WRITE'
result.update(status='PASS_BOUNDED_SAVED_REVIEW', samples=4, pointed_spans=total_spans,
              changed_backing=dict(arena=11, title=hex(title[11]), loaded=hex(loaded[11])),
              newly_enabled=dict(arena=14, backing=hex(loaded[14])),
              input_hashes={p.name: sha(p) for p in sorted(root.glob('*.json')) if p.name not in ('review.json', 'manifest.json')})
(root / 'review.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print('Reviewed 4 nonempty samples and 154 readable spans. Arena7 header exception retained; cleanup receipts agree.')
