"""Offline reduction of retained live evidence; never opens FF12 or writes saves."""
import ast, copy, datetime, hashlib, json, struct, zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EXE='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
TEXT='5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4'
PID=34844
STATES={'current-field':26,'returned-title':18,'old-after-current-complete':18,'old-after-current-field-settled':23}
PULSES={'title-enter':49,'load-modern-enter':49,'dismiss-modern-enter':49,'pause-p':15,
        'title-return-f':5,'confirm-title-enter':49,'reopen-load-enter':49,'load-old-enter':49,
        'dismiss-old-enter':49,'old-menu-r':17,'open-old-inventory-enter':49,
        'close-old-inventory-c':2,'close-old-menu-c':2}
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((ROOT/n).read_text())

def identity(r):
    assert r['exe_sha256']==EXE and r['image_base']==0x120000
    assert r['module_verdict']=='clean' and r['modules']
    if 'watched_modules' in r:assert not r['watched_modules']
    assert len(r['code_identity'])==1
    c=r['code_identity'][0]
    assert c['bytes']==7996981 and c['disk_sha256']==c['live_sha256']==TEXT
    if 'matches' in c:assert c['matches']

def pulse(r,index):
    assert r['status']=='REGISTERED_PULSE_ONLY' and r['pid']==PID and r['hwnd']==1902042
    assert r['read_handle_closed'] and r['null_read_rejected']
    assert r['down_accepted']==r['up_accepted']==2
    identity(r['before']);identity(r['after'])
    counts=dict(baseline=0,held=0,release=0);positive=0;addresses=set()
    for s in r['samples']:
        assert s['status']=='STABLE_CHAIN' and s['chain_before']==s['chain_after']
        assert s['array_address']==s['array_address_after'];addresses.add(s['array_address'])
        raw=bytes.fromhex(s['raw']);assert len(raw)==256
        nz=[i for i,b in enumerate(raw) if b];assert nz==s['nonzero_indices']
        counts[s['phase']]+=1
        if s['phase']=='held':
            assert set(nz)<={index};positive+=bool(nz)
        else:assert not nz
    assert len(addresses)==1 and counts['baseline']==35 and counts['held']>0 and counts['release']==1
    assert positive and r['seen_indices']==[index]
    return dict(counts=counts,positive_held_samples=positive,index=index,held_seconds=r['held_elapsed'])

def unit_identities(raw,capacity):
    return [(bool(raw[k*0xF50]&1),raw[k*0xF50+8:k*0xF50+0x18],
             raw[k*0xF50+0x698:k*0xF50+0x6A8],raw[k*0xF50+0xE60:k*0xF50+0xE70],
             raw[k*0xF50+0xEA9]) for k in range(capacity)]

def sample(s,expected_spans):
    spans={r['name']:r for r in s['reads']}
    assert len(spans)==len(s['reads'])==expected_spans
    data={}
    for name,r in spans.items():
        b=bytes.fromhex(r['bytes']);assert len(b)==r['size'] and sha(b)==r['sha256'];data[name]=b
    for a,b in [('registry_before','registry_after'),('pool_keep_capacity_before','pool_keep_capacity_after'),('image_address_base_before','image_address_base_after')]:
        assert data[a]==data[b],a+' changed during sample'
    assert s['registry_stable'] and s['pool_keep_stable'] and s['base_stable']
    assert spans['registry_before']['address']==spans['registry_after']['address']==0x2EBF120
    assert spans['pool_keep_capacity_before']['address']==0x208E688
    assert spans['image_address_base_before']['address']==0x1F83530
    B=struct.unpack_from('<Q',data['registry_before'],0x70)[0]
    assert B==s['battle_binding']==0x21B290C
    pool,k1,k2,cap=struct.unpack_from('<QQQi',data['pool_keep_capacity_before'])
    assert [k1,k2]==s['keep_bindings'] and pool==s['pool'] and cap==s['capacity'] and 0<cap<=32
    assert spans['battle_unit_pool']['address']==spans['battle_unit_pool_after']['address']==pool
    assert len(data['battle_unit_pool'])==len(data['battle_unit_pool_after'])==cap*0xF50
    assert unit_identities(data['battle_unit_pool'],cap)==unit_identities(data['battle_unit_pool_after'],cap)
    assert s['unit_bindings_stable']
    for k,p in ((1,k1),(2,k2)):
        assert spans['keep_bank_'+str(k)]['address']==p and len(data['keep_bank_'+str(k)])==0x9400
    im=data['active_save_image'];b=data['bound_battle_block']
    assert spans['active_save_image']['address']==0x2164280 and len(im)==0x56690
    assert spans['bound_battle_block']['address']==B and len(b)==0x7410
    assert b==im[0x4E68C:0x4E68C+0x7410]
    return data

def memory(r,expected_spans):
    identity(r)
    assert r['watched_modules']==[]
    assert r['status']=='OBSERVED' and r['pid']==PID and r['read_handle_closed']
    assert r['known_read_control']=='19930d0a1a0a' and r['null_read_rejected']
    assert len(r['samples'])==2
    return [sample(s,expected_spans) for s in r['samples']]

def reject(name,call):
    try:call()
    except AssertionError:return name
    raise AssertionError(name+' falsely passed')

def main():
    pulses={n:pulse(load(n+'.json'),i) for n,i in PULSES.items()}
    bad=copy.deepcopy(load('pause-p.json'));bad['samples']=[]
    negatives=[reject('empty-input',lambda:pulse(bad,15))]
    bad=copy.deepcopy(load('pause-p.json'))
    for s in bad['samples']:s['raw']='00'*256;s['nonzero_indices']=[]
    negatives.append(reject('no-held-detection',lambda:pulse(bad,15)))
    states={label:memory(load(label+'-memory.json'),count) for label,count in STATES.items()}
    failed=load('old-after-current-field-memory.json')
    assert failed['status']=='INVALID' and failed['read_handle_closed'] and len(failed['samples'])==1
    assert failed['error']=="AssertionError('Binding changed during sequential capture')"
    bad=copy.deepcopy(failed['samples'][0]);bad['registry_stable']=True
    negatives.append(reject('actual-registry-change-even-with-forged-flag',lambda:sample(bad,23)))
    bad=copy.deepcopy(load('current-field-memory.json'));bad['samples']=[]
    negatives.append(reject('empty-memory-run',lambda:memory(bad,26)))

    # Reuse only the four existing decoding functions, without running its broad
    # roundtrip campaign or writing any peer artifact. This is a documented decoder,
    # not original-code execution. The retained real-file roundtrip pins the plaintext.
    decoder=ROOT.parent/'save-container-roundtrip/save_container_roundtrip.py'
    tree=ast.parse(decoder.read_text());names={'rotl','rc4','key_for','unwrap'}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    ns=dict(hashlib=hashlib,struct=struct,zlib=zlib,TITLE=b'FINAL FANTASY XII THE ZODIAC AGE')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(decoder),'exec'),ns)
    before=load('save-before.json');backup=Path(before['backup'])
    raw=(ROOT/'inputs/old-FFXII_004.bin').read_bytes()
    assert sha(raw)=='8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc'
    decoded=ns['unwrap'](raw);plain=decoded['plain']
    assert decoded['declared']==0x4E690 and decoded['n']==26
    receipt=load('../save-container-roundtrip/save-container-roundtrip.json')
    prior=[r for r in receipt['results'] if r['file'].endswith('FFXII_004')]
    assert prior and all(r['status']=='OK' and r['ciphertext_match'] and r['plaintext_sha256']==sha(plain) for r in prior)
    assert sha(plain)=='9d7314c38ed17619f7abb84ce0e084bbe2cbbca2a9e2dfb040012ff3b06eba38'
    legacy=plain[0x2200:0x8200]
    rows=[]
    for label,values in states.items():
        for index,d in enumerate(values):
            b=d['bound_battle_block'];im=d['active_save_image']
            def matches(ref):return [b[0x5B10+i*0x9C:0x5B44+i*0x9C]==ref[0x90+i*0x1C8:0xC4+i*0x1C8] for i in range(40)]
            rows.append(dict(label=label,sample=index,spans=len(d),block_sha256=sha(b),stamp=hex(struct.unpack_from('<I',b)[0]),
                levels=[b[8+i*0x1C8+0x1C2] for i in range(6)],selectors=list(struct.unpack_from('<40i',b,0x7370)),
                prefix_matches_saved_old=b[:0x5B10]==legacy[:0x5B10],bank0_matches_saved_old=sum(matches(legacy)),
                prefix_matches_current_compatibility=b[:0x5B10]==im[0x2200:0x2200+0x5B10],
                bank0_matches_current_compatibility=sum(matches(im[0x2200:0x8200])),
                current_compatibility_equals_saved_old=im[0x2200:0x8200]==legacy,
                keep=[dict(bank=k,address=hex(struct.unpack_from('<Q',d['pool_keep_capacity_before'],k*8)[0]),nonzero=sum(v!=0 for v in d['keep_bank_'+str(k)]),sha256=sha(d['keep_bank_'+str(k)])) for k in (1,2)],
                registry_unit_pool=hex(struct.unpack_from('<Q',d['registry_before'],0x68)[0]),
                field_id=hex(struct.unpack_from('<H',im,0x1244)[0]),
                history_before=list(struct.unpack('<IHHI',d['field_history_stamp_before'])),
                history_after=list(struct.unpack('<IHHI',d['field_history_stamp_after'])),
                clock_before=d['clock_parity_before'].hex(),clock_after=d['clock_parity_after'].hex()))
    transitions=[]
    labels=list(STATES)
    for a,b in zip(labels,labels[1:]):
        da,db=states[a][-1],states[b][0];ba,bb=da['bound_battle_block'],db['bound_battle_block']
        delta=[i for i in range(len(ba)) if ba[i]!=bb[i]]
        transitions.append(dict(before=a,after=b,battle_changed_bytes=len(delta),first=hex(delta[0]) if delta else None,last=hex(delta[-1]) if delta else None,
            keep_changes=[dict(bank=k,changed_bytes=sum(x!=y for x,y in zip(da['keep_bank_'+str(k)],db['keep_bank_'+str(k)]))) for k in (1,2)],
            old_keep1_equals_new_keep2=da['keep_bank_1']==db['keep_bank_2']))
    for row in rows:
        assert row['stamp']=='0x5071901' and row['selectors']==[0]*40
        if row['label'].startswith('old-after'):
            assert row['levels']==[21]*6 and row['prefix_matches_saved_old'] and row['bank0_matches_saved_old']==40
        else:assert row['levels']==[1,1,1,1,2,1] and not row['prefix_matches_saved_old']
    assert transitions[1]['battle_changed_bytes']>0
    cleanup=load('cleanup.json')
    assert cleanup['status']=='RESTORED' and cleanup['files']==before['files'] and len(before['files'])==26
    assert cleanup['backup_unchanged'] and cleanup['processes']==[] and load('process-after.json')['processes']==[]
    assert set(cleanup['changed'])=={'76561198045890736\\GameSetting.ini','76561198045890736\\keymap.ini'}
    assert load('reference-after.json')['sha256']==EXE and load('reference-after.json')['pc_control_reset']
    health=load('health.json');assert health['fatal_dialog_observed'] is False and health['responsive_menu_and_return'] is True
    for label in health['evidence']:
        ui=load(label+'-ui.json');assert ui['screenshots'] and all((ROOT/n).is_file() for n in ui['screenshots'])
    duration=(datetime.datetime.fromisoformat(load('exit-action.json')['at'])-datetime.datetime.fromisoformat(load('launch.json')['at'])).total_seconds()
    assert 0<duration<1200
    output=dict(status='ACCEPTED_BOUNDED_LIVE_OBSERVATIONS_PENDING_INDEPENDENT_REVIEW',pid=PID,
        intervention=load('deployment.json')['intervention'],session_seconds=duration,
        pulses=pulses,samples=rows,transitions=transitions,accepted_samples=8,rejected_samples=1,
        accepted_spans=sum(x['spans'] for x in rows),negative_controls_rejected=negatives,
        decoded_old=dict(input_sha256=sha(raw),plaintext_sha256=sha(plain),bytes=len(plain),rotation=decoded['n'],decoder_source_sha256=sha(decoder.read_bytes()),method='Reuse documented file decoder; existing real-file roundtrip plaintext pin; not original-code execution'),
        rejected_attempt='Initial field sample registry+68 changed0->0x6F6343C0; excluded, not repaired in place',
        cleanup_verified=True,limits=['One exact save pair/build/session with labelled temporary input binding.',
            'Sequential snapshots are not atomic and do not reveal every intermediate writer or callback.',
            'Screenshots establish visible presentation; raw memory separately establishes sampled internal state.',
            'Keep endpoint differences do not prove clearing/copying/swap writers or uninterrupted ownership.',
            'Selector zero before/after cannot prove a reset write.',
            'Watched-module clean verdict is not a proof of every module effect.',
            'Independent review and FABLE/OPUS canonical incorporation remain pending.'])
    (ROOT/'observation.json').write_text(json.dumps(output,indent=2)+'\n')
    print(output['status'],len(pulses),'registered pulses;',output['accepted_spans'],'accepted spans;',duration,'seconds')
    for row in rows:print(row['label'],row['sample'],'levels',row['levels'],'old prefix',row['prefix_matches_saved_old'],'bank0',row['bank0_matches_saved_old'],'keep nonzero',[k['nonzero'] for k in row['keep']])
    print(json.dumps(transitions,indent=2))
    print('Rejected controls:',', '.join(negatives))

if __name__=='__main__':main()
