"""Read-only validation of raw native receipts. --write seals normalized output once."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct

E=Path(__file__).resolve().parent
DEFAULT_ID='76561198045890736'
PREFIX='C:\\FF12\\'
SENTINEL=0x5A17C0DE
NAMES=['control-stable-direct','control-stable-shim',
       'control-wide-stable-direct','observed-wide-alias-direct',
       'control-wide-stable-shim','observed-wide-alias-shim',
       'control-wide-alias-clobber','control-wide-stable-clobber',
       'boundary-wide-alias-u64max','boundary-wide-stable-u64max']
sha=lambda b:hashlib.sha256(b).hexdigest()


def text(raw):
    assert len(raw)%2==0
    end=next((i for i in range(0,len(raw),2) if raw[i:i+2]==b'\0\0'),None)
    assert end is not None,'unterminated captured text'
    return raw[:end].decode('utf-16le')


def validate(name, proof, raw, cleanup, process):
    assert ((proof['pid']==process['pid'] and proof['parent_pid']==process['orchestrator_pid'])
            or proof['parent_pid']==process['pid']), 'unproven launcher/native child relationship'
    assert process['exit_code']==0 and not process['timed_out'] and process['owned_child_reaped']
    assert cleanup['normal_return'] and cleanup['returned']==SENTINEL
    assert len(cleanup['allocations'])==3 and all(r['freed'] for r in cleanup['allocations'])
    assert not cleanup['debugger_present'] and not proof['debugger_present']
    assert cleanup['source_and_code_unchanged'] and cleanup['crt_sha256_after']==proof['crt_sha256']
    assert len(raw)==0xe00 and sha(raw)==cleanup['raw_sha256']
    assert proof['executable_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    pointer,caller_rsp=struct.unpack_from('<QQ',raw)
    assert caller_rsp%16==0 and caller_rsp-pointer==0x220
    supplied=proof.get('input_id',DEFAULT_ID); prefix=proof.get('prefix',PREFIX)
    assert supplied.isdecimal() and 0<=int(supplied)<2**64
    before=text(raw[0x400:0x600]); assert before==supplied
    clobber=proof.get('clobber',False)
    aliased_value=('X'+supplied[1:]) if clobber else supplied
    consumed=supplied if proof['stable'] else aliased_value
    pre=None
    if proof['shim']:
        args,observed_pointer,crt_rsp,options=struct.unpack_from('<QQQQ',raw,0x18)
        assert args==caller_rsp+0x10 and crt_rsp==caller_rsp-0x58
        assert observed_pointer==(proof['data']+0x200 if proof['stable'] else pointer)
        assert options==proof['printf_options']
        pre=text(raw[0x600:0x800]);assert pre==consumed
    else:assert raw[0x18:0x38]==bytes(0x20) and raw[0x600:0x800]==bytes(512)
    after=text(raw[0x800:0xa00]);assert after==aliased_value
    output=text(raw[0xa00:0xe00]);opt=proof['printf_options']
    assert opt in (0,4)
    expected=prefix+consumed if opt==4 else prefix[0]+consumed[0]
    assert output==expected,('unexpected native output',name,repr(output),repr(expected))
    returned=struct.unpack_from('<i',raw,0x10)[0]; assert returned==len(expected)
    changes=[i for i,(a,b) in enumerate(zip(raw[0x400:0x600],raw[0x800:0xa00])) if a!=b]
    prechanges=[] if not proof['shim'] or proof['stable'] else [i for i,(a,b) in enumerate(zip(raw[0x400:0x600],raw[0x600:0x800])) if a!=b]
    return dict(name=name,kind='explicit clobber control' if clobber else 'native observation',
                stable_control=proof['stable'],entry_observer=proof['shim'],printf_options=opt,
                input_id=supplied,before_returned_buffer=before,pre_crt_input=pre,
                after_returned_buffer=after,formatted_output=output,formatter_return=returned,
                returned_pointer=f'{pointer:016X}',caller_rsp=f'{caller_rsp:016X}',
                changed_returned_window_offsets=changes,pre_crt_changed_returned_window_offsets=prechanges,
                cleanup='three owned allocations freed; child exited zero')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    rows=[];cases={};source_bytes={}
    for p in [E/'run.py',E/'fixture.py',*(E/'observed-source').glob('*.py'),
              *(E/'feasibility-stable-shim').glob('initial-*.py'),
              *(E/'pre-ownership-source').glob('*.py')]:source_bytes[sha(p.read_bytes())]=p
    for name in NAMES:
        d=E/('verified-'+name);proof=json.loads((d/'before.json').read_text());cleanup=json.loads((d/'cleanup.json').read_text())
        process=json.loads((d/'process.json').read_text());raw=(d/'native.bin').read_bytes()
        plan=json.loads((d/'plan.json').read_text());assert all(h in source_bytes for h in plan['sources'].values())
        assert ((proof['pid']==process['pid'] and proof['parent_pid']==process['orchestrator_pid'])
                or proof['parent_pid']==process['pid']), 'unproven launcher/native child relationship'
        assert plan['live_game'] is False and proof['native_executable_sha256']
        cases[name]=(proof,raw,cleanup,process);rows.append(validate(name,*cases[name]))
    assert rows,'empty population is not evidence'
    assert len({r[0]['crt_sha256'] for r in cases.values()})==1
    assert len({r[0]['python_sha256'] for r in cases.values()})==1
    byname={r['name']:r for r in rows}
    for first,second in [('control-stable-direct','control-stable-shim'),
                         ('control-wide-stable-direct','control-wide-stable-shim'),
                         ('observed-wide-alias-direct','observed-wide-alias-shim')]:
        assert byname[first]['formatted_output']==byname[second]['formatted_output']
    bad=E/'feasibility-stable-shim';proc=json.loads((bad/'process.json').read_text());clean=json.loads((bad/'cleanup.json').read_text())
    assert proc['exit_code']==1 and proc['owned_child_reaped'] and not proc['timed_out']
    assert not clean['normal_return'] and all(x['freed'] for x in clean['allocations'])
    assert not (bad/'native.bin').exists() and not (bad/'before.json').exists()
    assert 'assert C.string_at(0x8f38c0,12)' in (bad/'stderr.txt').read_text()
    rejected=[]
    def reject(label,case):
        try:validate('mutated receipt',*case)
        except (AssertionError,UnicodeError):rejected.append(label)
        else:raise AssertionError('mutation survived: '+label)
    base=cases['observed-wide-alias-shim']
    p,r,c,x=copy.deepcopy(base);c['normal_return']=False;reject('failed cleanup',(p,r,c,x))
    p,r,c,x=copy.deepcopy(base);p['parent_pid']=0;reject('wrong native parent PID',(p,r,c,x))
    p,r,c,x=copy.deepcopy(base);r=bytearray(r);r[0x400]=ord('9');c['raw_sha256']=sha(r);reject('altered initial ID',(p,r,c,x))
    p,r,c,x=copy.deepcopy(base);r=bytearray(r);struct.pack_into('<Q',r,0x20,p['data']+0x200);c['raw_sha256']=sha(r);reject('wrong observed alias',(p,r,c,x))
    p,r,c,x=copy.deepcopy(cases['control-stable-direct']);p['printf_options']=4;reject('narrow result promoted to wide',(p,r,c,x))
    p,r,c,x=copy.deepcopy(cases['control-wide-alias-clobber']);p['clobber']=False;reject('clobber erased from provenance',(p,r,c,x))
    out=dict(status='BOUNDED_ORIGINAL_CODE_NATIVE_CRT_OBSERVATION',method='B',live_game=False,
             crt_sha256=base[0]['crt_sha256'],crt_path=base[0]['crt_path'],observations=rows,
             retained_invalid_preparation='Wrong adjacent format literal rejected before execution; all allocations freed.',
             superseded_native_receipts='The10 original folders retain observations but lack a recorded launcher/native-parent relationship; verified-* reruns supersede their acceptance.',
             rejection_controls=rejected,
             established=['Under supplied wide-option4 states the tested17/20-digit IDs survive original return/caller/formatter consumption.',
                          'Intentional alias overwrite changes output; stable retained ID isolates that effect.',
                          'Native option0 controls read C7 in this fixture, not the full wide text.',
                          'Unused returned-buffer bytes do change; full-window preservation is not established.'],
             unresolved=['Actual original Steam/context/logging and CRT option initialization.',
                         'Other installed CRTs, stack states, caller paths, initialization and normal-game reachability.',
                         'Exact intermediate CRT loads/writes; output plus boundary snapshots is not a per-instruction trace.'])
    serialized=json.dumps(out,indent=2)+'\n'
    if args.write:
        with (E/'observation.json').open('x') as f:f.write(serialized)
    else:assert (E/'observation.json').read_text()==serialized
    print('PASS: native receipts, stage-specific identities, wide controls, alias overwrite discriminator, source versions and cleanup.')
    print('Six corrupted receipts rejected; initial pre-execution failure retained as invalid.')


if __name__=='__main__':main()
