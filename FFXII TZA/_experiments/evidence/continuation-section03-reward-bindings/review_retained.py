"""Independent reduction of the retained EXP-081 capture bytes.

No original observer/reducer code is imported. Hash/size identity is checked by
run_review.py before this module receives records. In-memory corrupted-record
controls recompute span hashes where appropriate, so they test structural checks
rather than only a checksum. This does not create a live observation.
"""
from __future__ import annotations
import copy
import hashlib
import struct

EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TEXT_SHA = '5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
SOURCES = ('current-complete-memory.json', 'current-field-memory.json')

def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def num(buf: bytes, offset: int = 0, width: int = 8) -> int:
    need(offset >= 0 and offset+width <= len(buf), 'out-of-range scalar')
    return int.from_bytes(buf[offset:offset+width], 'little')

def decode(records: dict) -> dict:
    rows = []
    span_count = 0
    sample_keys = set()
    for source in SOURCES:
        doc = records[source]
        need(doc['status'] == 'OBSERVED' and doc['pid'] == 30640, 'original session identity')
        need(doc['exe_sha256'] == EXE_SHA and doc['image_base'] == 0x120000, 'original image identity')
        need(doc['known_read_control'] == '19930d0a1a0a' and doc['null_read_rejected'] and doc['read_handle_closed'], 'read/control/cleanup receipt')
        code = doc['code_identity']
        need(len(code) == 1 and code[0]['matches'] and code[0]['bytes'] == 7996981 and code[0]['disk_sha256'] == code[0]['live_sha256'] == TEXT_SHA, 'live text receipt')
        need(len(doc['samples']) == 2, 'expected two retained samples per stage')
        for sample in doc['samples']:
            key = (source, sample['index'])
            need(key not in sample_keys and sample['index'] in (0, 1), 'sample identity duplicated or changed')
            sample_keys.add(key)
            need(doc['start_unix'] <= sample['start_unix'] <= sample['end_unix'] <= doc['end_unix'], 'time brackets')
            reads = {}
            for read in sample['reads']:
                name = read['name']
                need(name not in reads, 'duplicate read name')
                buf = bytes.fromhex(read['bytes'])
                need(read['size'] == len(buf) and hashlib.sha256(buf).hexdigest() == read['sha256'], 'span hash/size')
                need(isinstance(read['address'], int) and read['address'] >= 0, 'bad address')
                reads[name] = (read['address'], buf)
                span_count += 1
            def get(name: str, address: int | None = None, size: int | None = None) -> bytes:
                need(name in reads, 'missing span '+name)
                addr, buf = reads[name]
                need(address is None or addr == address, 'wrong span address '+name)
                need(size is None or len(buf) == size, 'wrong span size '+name)
                return buf
            for before, after, addr, size in (
                    ('registry_before', 'registry_after', 0x2ebf120, 0x78),
                    ('pool_keep_capacity_before', 'pool_keep_capacity_after', 0x208e688, 32),
                    ('image_address_base_before', 'image_address_base_after', 0x1f83530, 8)):
                need(get(before, addr, size) == get(after, addr, size), 'bracket changed '+before)
            need(all(sample[k] for k in ('registry_stable', 'pool_keep_stable', 'base_stable', 'unit_bindings_stable')), 'original stability flag false')
            registry = get('registry_before')
            allocation = get('pool_keep_capacity_before')
            pool, keep1, keep2, capacity = [num(allocation, i, 8 if i < 24 else 4) for i in (0, 8, 16, 24)]
            need(pool == sample['pool'] and capacity == sample['capacity'] == 32, 'pool/capacity identity')
            block_address = num(registry, 0x70)
            block = get('bound_battle_block', block_address, 0x7410)
            bank1 = get('keep_bank_1', keep1, 64*0x250)
            bank2 = get('keep_bank_2', keep2, 64*0x250)
            before = get('battle_unit_pool', pool, capacity*0xf50)
            after = get('battle_unit_pool_after', pool, capacity*0xf50)
            address_base = num(get('image_address_base_before'))
            reward_descriptors = {'base': num(registry, 0x28), 'per_level': num(registry, 0x20)}
            def intersections(address: int, size: int) -> list[dict]:
                if address == 0:
                    return []
                return [{'read': name, 'start': hex(max(address, addr)), 'bytes': min(address+size, addr+len(buf))-max(address, addr)}
                        for name, (addr, buf) in reads.items() if max(address, addr) < min(address+size, addr+len(buf))]
            def region(buf: bytes, i: int) -> bytes:
                return buf[i*0xf50:(i+1)*0xf50]
            units = []
            for i in range(capacity):
                unit, post = region(before, i), region(after, i)
                # Compare all reward bytes explicitly, not just the old observer flag.
                for lo, hi in ((0, 1), (8, 0x18), (0x698, 0x6a8), (0xe60, 0xe80), (0xea9, 0xeaa)):
                    need(unit[lo:hi] == post[lo:hi], 'unit binding changed across reward bracket')
                if not(unit[0]&1 and num(unit, 0x10) and num(unit, 0x698)):
                    continue
                need(unit[0xea9] == i, 'unit slot byte')
                stats_addr = num(unit, 0x698)
                stats = get(f'unit_{i}_stats', stats_addr, 0x1c8)
                kind = stats[5]
                u = {'slot': i, 'unit': hex(pool+i*0xf50), 'actor': hex(num(unit, 0x10)),
                     'definition_id': hex(num(stats, 4, 2)), 'kind': kind, 'stats': hex(stats_addr),
                     'spawn_keep': hex(num(unit, 0x6a0)), 'authored_definition': hex(num(unit, 0xe60)),
                     'authored_class': hex(num(unit, 0xe68)), 'reward_base': hex(num(unit, 0xe70)),
                     'reward_per_level': hex(num(unit, 0xe78)), 'reward_bytes_equal_in_pool_bracket': True,
                     'reward_operand_capture': {}}
                if kind == 0:
                    off = stats_addr-block_address
                    need(off >= 8 and (off-8)%0x1c8 == 0 and off+0x1c8 <= len(block), 'party stats extent')
                    need(stats == block[off:off+0x1c8], 'party record differs from retained block')
                    need(num(unit,0x6a0) == num(unit,0xe68) == num(unit,0xe70) == num(unit,0xe78) == 0, 'observed party binding differs')
                    u['stats_storage'] = 'battle-state block'
                elif kind == 1:
                    spawn = num(unit, 0x6a0)
                    off = spawn-keep1
                    need(off >= 0 and off%0x250 == 0 and off+0x250 <= len(bank1), 'primary keep range')
                    need(stats_addr == spawn+0x80 and stats == bank1[off+0x80:off+0x80+0x1c8], 'spawn stats do not match keep slice')
                    header = get('enemy_table_header', num(registry), 32)
                    count, stride, encoded = num(header,4,4),num(header,8,2),num(header,12,4)
                    base = (encoded+address_base)&((1<<64)-1)
                    table = get('enemy_table_rows', base, count*stride)
                    offset = num(unit,0xe60)-base
                    need(stride >= 0x26 and 0 <= offset < len(table) and offset%stride == 0, 'definition pointer extent')
                    need(offset//stride == stats[4], 'definition row index disagrees')
                    need(not(keep1 <= num(unit,0xe68) < keep1+len(bank1)) and not(keep2 <= num(unit,0xe68) < keep2+len(bank2)), 'class points into keep storage')
                    u.update(stats_storage='primary keep entry +0x80', enemy_row=offset//stride,
                             reward_base_selector=num(table,offset+0x22,2), reward_per_level_selector=num(table,offset+0x24,2))
                    need(num(unit,0xe70) != 0 and num(unit,0xe78) != 0, 'observed kind1 reward pointers changed')
                else:
                    raise ValueError('unexpected retained active kind')
                for which, ptr in (('base',num(unit,0xe70)), ('per_level',num(unit,0xe78))):
                    u['reward_operand_capture'][which] = {
                        'required_prefix_0x38_overlap': intersections(ptr,0x38),
                        'lp_byte_overlap': intersections(ptr+0x2f,1) if ptr else [],
                        'xp_dword_overlap': intersections(ptr+0x34,4) if ptr else []}
                units.append(u)
            header_overlap = {which: intersections(addr,0x20) for which,addr in reward_descriptors.items()}
            need(not any(header_overlap.values()), 'reward header capture unexpectedly present')
            need(all(not result['required_prefix_0x38_overlap'] for u in units for result in u['reward_operand_capture'].values()), 'reward row capture unexpectedly present')
            if source.startswith('current-complete'):
                need(not units and reward_descriptors == {'base':0,'per_level':0}, 'load-popup population changed')
            else:
                need([u['slot'] for u in units] == [0,4,5,7] and all(reward_descriptors.values()), 'field active population changed')
            candidates = {}
            for which in ('base','per_level'):
                enemies = [u for u in units if u['kind'] == 1]
                if enemies:
                    zero = next(u for u in enemies if u[f'reward_{which}_selector'] == 0)
                    row0 = int(zero[f'reward_{which}'],16)
                    differences=[]
                    for u in enemies:
                        index=u[f'reward_{which}_selector']
                        if index:
                            delta=int(u[f'reward_{which}'],16)-row0
                            differences.append({'selector':index,'row_address_delta':delta,'divisible':delta%index==0,'quotient':delta//index})
                    candidates[which]={'zero_selector_pointer':hex(row0),'offset_from_descriptor':row0-reward_descriptors[which],
                                      'differences':differences,'interpretation':'0x38 affine spacing fits sampled pairs; header stride/count/encoded base were not read. Not independent validation of row contents or lifetime.'}
            rows.append({'source':source,'sample':sample['index'],'original_start':sample['start_unix'],'original_end':sample['end_unix'],
                         'reads':len(reads),'address_base':hex(address_base),'reward_descriptors':{k:hex(v) for k,v in reward_descriptors.items()},
                         'reward_header_overlap':header_overlap,'active_units':units,'conditional_affine_fit':candidates})
    need(len(rows)==4 and span_count==88, 'original raw population changed')
    cleanup,exited=records['cleanup.json'],records['exit-check.json']
    need(cleanup['status']=='RESTORED' and not cleanup['processes'] and cleanup['backup_unchanged'], 'original cleanup not accepted')
    need(cleanup['files']==records['save-before.json']['files'] and len(cleanup['files'])==26 and not exited['processes'] and exited['owned_pid']==30640, 'original restore/exit receipt mismatch')
    return {'status':'PASS bounded independent retained-byte review; peer acceptance pending',
            'method':'Independent Python parsing, byte/range comparison and hashing of retained EXP-081 inputs; no new live observation.',
            'spans_verified':span_count,'sample_count':len(rows),'observations':rows,
            'limitations':['One historical process and four sequential non-atomic samples.',
                           'Registry slots and unit reward-pointer words were read; actual reward descriptors and row bytes were not.',
                           'Null popup slots do not prove null rows on a reached installer or defeat path.',
                           'Stable brackets do not prove uninterrupted lifetime, no intermediate rebind, or causality.',
                           'No reward amount, death action, installer execution or rendered payout was observed here.']}

def negative_controls(records: dict) -> list[dict]:
    names=('changed_reward_after_bracket','wrong_registry_address','wrong_stats_address','changed_stats_content',
           'misaligned_definition_pointer','empty_field_samples','duplicate_sample_id','false_observer_flag',
           'added_uncaptured_reward_bytes','restoration_mismatch')
    results=[]
    for name in names:
        bad=copy.deepcopy(records)
        d=bad['current-field-memory.json'];s=d['samples'][0];reads={r['name']:r for r in s['reads']}
        def modify(readname,offset,payload):
            r=reads[readname];b=bytearray.fromhex(r['bytes']);b[offset:offset+len(payload)]=payload;r['bytes']=b.hex();r['sha256']=hashlib.sha256(b).hexdigest()
        if name=='changed_reward_after_bracket':modify('battle_unit_pool_after',4*0xf50+0xe70,b'\x00')
        elif name=='wrong_registry_address':reads['registry_before']['address']+=8
        elif name=='wrong_stats_address':reads['unit_4_stats']['address']+=8
        elif name=='changed_stats_content':modify('unit_4_stats',0x10,b'\xA5')
        elif name=='misaligned_definition_pointer':
            for r in ('battle_unit_pool','battle_unit_pool_after'):
                b=bytes.fromhex(reads[r]['bytes']);value=num(b,4*0xf50+0xe60)+1;modify(r,4*0xf50+0xe60,value.to_bytes(8,'little'))
        elif name=='empty_field_samples':d['samples']=[]
        elif name=='duplicate_sample_id':d['samples'][1]['index']=0
        elif name=='false_observer_flag':s['registry_stable']=False
        elif name=='added_uncaptured_reward_bytes':
            b=bytes.fromhex(reads['battle_unit_pool']['bytes']);addr=num(b,4*0xf50+0xe70)+0x34;payload=b'\x00'*4
            s['reads'].append({'name':'fabricated_reward_operand','address':addr,'size':4,'bytes':payload.hex(),'sha256':hashlib.sha256(payload).hexdigest()})
        elif name=='restoration_mismatch':bad['cleanup.json']['files']={}
        try:
            decode(bad)
        except (ValueError,KeyError,TypeError) as exc:
            results.append({'control':name,'rejected':True,'reason':str(exc)})
        else:
            raise RuntimeError('corrupted retained observation accepted: '+name)
    return results
