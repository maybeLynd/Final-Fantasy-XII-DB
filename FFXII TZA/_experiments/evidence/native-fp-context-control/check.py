"""Read-only reducer and falsification checks for retained native receipts.

--write creates normalized.json exclusively. It does not execute native code.
Initial invalid evidence stays invalid; diagnostic health is checked separately
from the refuted whole-state-preservation hypothesis.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct

import capstone
from fixture import make, seed, state, verify_sample

E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())


def source_identity(folder):
    plan=read(folder/'plan.json')
    for name,digest in plan['sources'].items():
        variants=[E/name]
        if name in ('run.py','fixture.py'):
            variants += [E/'initial-source'/name,E/'diagnostic-source'/name]
        assert any(p.is_file() and sha(p)==digest for p in variants), ('source identity',name,digest)
    assert read(folder/'result.json')['sources']==plan['sources']


def require_health(result,capture):
    assert result['status']=='NATIVE_CONTROL_OBSERVED'
    assert result['final_exits']==dict(debugger=0,target=0)
    assert not result['forced_termination']
    e=result['target_exit']
    assert e['normal_exit'] and e['code_freed'] and e['data_freed'] and not e['debugger_present']
    assert capture['status']=='PASS' and capture['detach'] and not capture['errors']
    assert capture['hits'], 'zero-case capture'
    c=capture['cleanup']
    assert c['status']=='PASS' and c['clears'] and c['verified']
    assert all(ok for _,ok in c['clears']+c['verified'])
    assert result['baseline']['exit'] is None and not result['baseline']['debugger']
    post=result['post']
    assert len(post)==4 and all(p['exit'] is None and not p['debugger'] for p in post)
    assert all(b['sample_bytes']>a['sample_bytes'] for a,b in zip(post,post[1:]))
    assert result['end_unix']-result['start_unix']<15


def reject(label,fn):
    try: fn()
    except (AssertionError,KeyError,ValueError,IndexError): return label
    raise AssertionError('malformed/adversarial receipt was accepted: '+label)


def reduce():
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    decoded=read(E/'fixture-decode.json')
    for mode in ('preserve','change'):
        code,gate=make(mode)
        assert code==(E/(mode+'.bin')).read_bytes()
        ins=list(md.disasm(code,0))
        assert sum(i.size for i in ins)==len(code)
        assert next(i for i in ins if i.address==gate).mnemonic==('nop' if mode=='preserve' else 'pxor')
        assert decoded['fixtures'][mode]['instructions']==[
            dict(offset=i.address,bytes=i.bytes.hex(),text=i.mnemonic+' '+i.op_str) for i in ins]
    result=dict(method='native disposable instrument control; no FF12 execution',
                capstone=capstone.__version__,initial_invalid={},arms={},negative_checks=[])
    initial=E/'preserve'
    source_identity(initial)
    invalid=read(initial/'result.json');cap=read(initial/'capture.json')
    assert invalid['status']=='INVALID' and cap['status']=='INVALID'
    assert invalid['final_exits']==dict(debugger=0,target=1)
    assert cap['cleanup']['status']=='INVALID' and len(cap['hits'])==1
    samples=[json.loads(l) for l in (initial/'samples.jsonl').read_text().splitlines()]
    assert len(samples)==3
    assert not verify_sample(read(initial/'baseline.json'),'preserve')['fip_truncated']
    result['initial_invalid']=dict(status='INVALID_RETAINED',samples=3,owned_hits=1,
        fip_truncations=sum(verify_sample(s,'preserve',allow_fip_truncation=True)['fip_truncated'] for s in samples),
        reason='target assertion exited while attached; requested cleanup could not complete; no health-qualified conclusion')
    for arm,mode,policy in [('full-observer','preserve','original-full'),
                            ('narrow-preserve','preserve','control-debug-only'),
                            ('narrow-change','change','control-debug-only'),
                            ('no-fp-request','preserve','control-debug-read-write')]:
        folder=E/arm
        source_identity(folder)
        plan,r,c,info=[read(folder/name) for name in ('plan.json','result.json','capture.json','target-ready.json')]
        assert plan['resume_policy']==r['resume_policy']==policy
        assert r['mode']==mode and info['pid']==r['owned_child_pid']==read(folder/'owned-child.json')['pid']
        assert info['sources']==plan['sources']
        assert plan['host']==r['host'] and set(r['host']['modules'])=={'kernel32.dll','kernelbase.dll','ntdll.dll','python314.dll'}
        if (E/'environment-post.json').exists():
            post_identity=read(E/'environment-post.json')['arms'][arm]
            expected=dict(plan['host']['modules'])
            expected['python.exe']=dict(path=plan['host']['python_binary'],sha256=plan['host']['python_sha256'])
            assert post_identity=={name:dict(entry,unchanged=True) for name,entry in expected.items()}
        require_health(r,c)
        code,gate=make(mode)
        assert bytes.fromhex(info['code_hex'])==code
        assert info['gate_address']==info['code_address']+gate and info['code_address']>0xffffffff
        assert info['buffer_address']&15==0
        baseline=verify_sample(read(folder/'baseline.json'),mode)
        assert not baseline['fip_truncated']
        rows=[json.loads(l) for l in (folder/'samples.jsonl').read_text().splitlines()]
        assert rows and len(rows)==r['samples']
        observed=[verify_sample(s,mode,allow_fip_truncation=True) for s in rows]
        truncated=sum(o['fip_truncated'] for o in observed)
        api=read(folder/'api.json')
        context=[a for a in api if a['operation']=='full_context']
        assert context and all(a['result'] for a in context)
        reads=set();writes=set();last_get={};resumes=[];owned_gets=[]
        for a in context:
            raw=bytes.fromhex(a['context_hex'])
            assert len(raw)==a['size']==1232 and a['flt_offset']==256
            assert a['address']&15==0
            assert raw[256:768].hex()==a['flt_hex']
            flags=struct.unpack_from('<I',raw,48)[0]
            assert flags==a['requested_flags']
            rip=struct.unpack_from('<Q',raw,248)[0]
            if a['api']=='GetThreadContext':
                reads.add(flags);last_get[a['handle']]=raw
                if rip==info['gate_address']:
                    owned_gets.append(a)
                    if flags&8:
                        fp=state(raw[256:768])
                        # XMM_SAVE_AREA32 ErrorOffset is u32, not native FXSAVE64 FIP.
                        assert struct.unpack_from('<I',raw,264)[0]==(info['code_address']+210)&0xffffffff
                        for key in ('fcw','fsw','ftw','mxcsr','x87','xmm'):
                            assert fp[key]==baseline['before'][key],key
                        assert struct.unpack_from('<I',raw,52)[0]==baseline['before']['mxcsr']
            else:
                writes.add(flags)
                if rip==info['gate_address'] and flags&1:
                    old=bytearray(last_get[a['handle']])
                    struct.pack_into('<I',old,48,flags)
                    struct.pack_into('<I',old,68,struct.unpack_from('<I',old,68)[0]|0x10000)
                    struct.pack_into('<Q',old,104,0)  # Dr6 only; full before/proposed receipt
                    assert bytes(old)==raw, 'unexplained proposed context byte change'
                    assert flags==(0x10001b if policy=='original-full' else 0x100011)
                    resumes.append(a)
        assert owned_gets and resumes
        assert reads==({0x100010,0x100011} if policy=='control-debug-read-write' else {0x100010,0x10001b})
        assert writes==({0x100010,0x10001b} if policy=='original-full' else {0x100010,0x100011})
        hits=[a for a in api if a['operation']=='exception_chance' and a['exception']==0x80000004]
        assert hits and all(a['address']==info['gate_address'] and a['tid']==info['tid'] and a['first_chance']==1 for a in hits)
        assert len(hits)==len(resumes)==len(c['hits'])==r['owned_hits']==truncated
        assert all(h['rip']==info['gate_address'] and h['tid']==info['tid'] for h in c['hits'])
        assert all(o['before']['fip']==info['code_address']+210 for o in observed)
        # No iteration from the post-detach health window has the address change.
        post=[o for s,o in zip(rows,observed) if s['unix']>r['post'][0]['unix']]
        assert post and not any(o['fip_truncated'] for o in post)
        result['arms'][arm]=dict(session='HEALTH_CONTROL_SATISFIED',whole_state_preserved=False,
            mode=mode,policy=policy,samples=len(rows),owned_hits=len(hits),fip_truncations=truncated,
            xmm0_deliberately_zeroed=mode=='change',other_seeded_numeric_fields_preserved=True,
            caller_state_restored_every_return=True,context_read_flags=sorted(reads),
            context_write_flags=sorted(writes),native_before_fip=hex(info['code_address']+210),
            trapped_after_fip=hex((info['code_address']+210)&0xffffffff),post_detach_samples=len(post),
            full_context_size=1232,full_context_observed_alignment=16,final_exits=r['final_exits'])
        if arm=='full-observer':
            result['negative_checks'].append(reject('empty capture cannot pass',lambda:require_health(r,dict(c,hits=[]))))
            bad=copy.deepcopy(c);bad['cleanup']['status']='INVALID'
            result['negative_checks'].append(reject('failed cleanup cannot pass',lambda:require_health(r,bad)))
            bad=copy.deepcopy(rows[0]);raw=bytearray.fromhex(bad['buffer_hex']);raw[0x400+160+7*16]^=1;bad['buffer_hex']=raw.hex()
            result['negative_checks'].append(reject('changed XMM7 is detected',lambda:verify_sample(bad,mode,allow_fip_truncation=True)))
            bad=copy.deepcopy(rows[0]);bad['returned']=0
            result['negative_checks'].append(reject('missing native sentinel is detected',lambda:verify_sample(bad,mode,allow_fip_truncation=True)))
            changed=next(s for s,o in zip(rows,observed) if o['fip_truncated'])
            result['negative_checks'].append(reject('full preservation claim rejects actual FIP change',lambda:verify_sample(changed,mode)))
        if arm=='narrow-change':
            result['negative_checks'].append(reject('native PXOR is rejected as unchanged numeric state',lambda:verify_sample(rows[0],'preserve',allow_fip_truncation=True)))
    result['conclusion']='Full x87 instruction-address preservation is refuted for these native breakpoint paths. Removing FP/INTEGER from resume writes, and then from reads too, did not prevent the observed FIP truncation. Numeric seed preservation and clean return do not imply all-state preservation. Mechanism and FF12 crash relevance remain unknown.'
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=reduce()
    if args.write:
        with (E/'normalized.json').open('x') as out: json.dump(result,out,indent=2)
    elif (E/'normalized.json').exists(): assert result==read(E/'normalized.json')
    if (E/'manifest.json').exists():
        for name,digest in read(E/'manifest.json').items():assert sha(E/name)==digest,name
    print(json.dumps(result,indent=2))
