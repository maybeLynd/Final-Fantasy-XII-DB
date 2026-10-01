"""Synthetic caller/read fixtures for the EO3-only recorder. No native calls."""
import argparse
import copy
import json
from pathlib import Path
import struct
from control import fixture
from observe import Recorder
from project import OFFSETS,REQUIRED

W=Path(__file__).resolve().parent


def context(ctx):
    raw=bytearray(1232)
    struct.pack_into('<I',raw,0x30,REQUIRED)
    for name,offset in OFFSETS.items():struct.pack_into('<Q',raw,offset,ctx.get(name,0))
    return dict(operation='full_context',api='GetThreadContext',result=1,
                requested_flags=REQUIRED,size=1232,context_hex=raw.hex(),
                source='SYNTHETIC Python fixture; not an API receipt')


def memory(f):
    p,pr,path,b,br,raw,i,issued=f
    blobs=[(p['rsp']+0x38,struct.pack('<Q',pr)),(p['rdi'],path),
           (b['rsp']+0x38,struct.pack('<Q',br)),(b['r10'],bytes(raw))]
    def read(address,size):
        for start,value in blobs:
            if start<=address and address+size<=start+len(value):
                return value[address-start:address-start+size]
        raise OSError('fixture read outside supplied memory')
    return blobs,read


def run(f=None,mutate=None):
    f=f or fixture();blobs,reader=memory(f);r=Recorder(100)
    if mutate:mutate(r,f,blobs)
    decisions=[]
    for tick,ctx in enumerate((f[0],f[3],f[6])):
        if r.decision!='CONTINUE':break
        if tick==2:blobs[-1]=(f[6]['rbx'],bytes(f[7]))
        decisions.append(r.event(context(ctx),ctx['tid'],100+tick*.1,reader))
    return r,decisions


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    r,decisions=run();positive=r.finish()
    assert decisions==['CONTINUE','CONTINUE','STOP_MATCHED_PENDING_HEALTH']
    assert positive['results'][0]['pointer_preserved']
    assert positive['semantic_payload_bytes']<32768
    assert all('error' not in x and x['hex'] is not None for x in positive['reads'])
    rejected=[];stops=[]
    def stopped(label,rec):
        try:rec.finish()
        except (ValueError,AssertionError):pass
        else:raise AssertionError(label+' incorrectly accepted')
        rejected.append(label)
        stops.append(dict(label=label,decision=rec.decision,reason=rec.reason,
                          events=rec.events,reads=rec.reads))
    for pointer in (0x100001000,0x18bc13000):
        rec,d=run(fixture(pointer));assert d==['HOLD_FOR_OWNED_ABORT']
        assert not rec.match.results and rec.match.producers
        stopped('changed pointer stays before enqueue '+hex(pointer),rec)
    rec,d=run(mutate=lambda r,f,b:b.__setitem__(1,(f[0]['rdi'],b'PS2Data')))
    assert rec.reads[-1]['error'] and d==['HOLD_FOR_OWNED_ABORT'];stopped('short path/read failure',rec)
    rec,d=run(mutate=lambda r,f,b:b.__setitem__(1,(f[0]['rdi'],b'A'*128)))
    assert len([x for x in rec.reads if x['purpose']=='selected path byte'])==128
    stopped('unterminated bounded path',rec)
    f=fixture();f[1]=0x377ff8;rec,d=run(f)
    assert not rec.match.results and all(x['selection'].startswith(('different','unselected')) for x in rec.events)
    stopped('auxiliary caller produces no primary sample',rec)
    f=fixture();struct.pack_into('<I',f[7],0x64,(20<<6)|3);rec,d=run(f)
    assert d[-1]=='HOLD_FOR_OWNED_ABORT';stopped('slot reused before issuer',rec)
    f=fixture();blobs,reader=memory(f);rec=Recorder(100)
    assert rec.event(context(f[0]),77,110,reader)=='HOLD_FOR_OWNED_ABORT'
    assert not rec.events and not rec.reads;stopped('deadline before further read',rec)
    rec=Recorder(100);rec.bytes=32768-1231
    assert rec.event(context(f[0]),77,100,reader)=='HOLD_FOR_OWNED_ABORT'
    assert not rec.events and not rec.reads;stopped('context exceeds payload budget',rec)
    rec=Recorder(100);rec.bytes=32768-1232-7
    assert rec.event(context(f[0]),77,100,reader)=='HOLD_FOR_OWNED_ABORT'
    assert not rec.reads;stopped('stack read exceeds payload budget',rec)
    # Eight unrelated producer events consume the same bounded allowance.
    f=fixture();f[1]=0x377ff8;blobs,reader=memory(f);rec=Recorder(100)
    for i in range(8):decision=rec.event(context(f[0]),77,100+i*.01,reader)
    assert decision=='HOLD_FOR_OWNED_ABORT' and rec.producers_seen==8
    stopped('eighth producer stops allowance',rec)
    try:rec.event(context(f[0]),77,100.9,reader)
    except ValueError:rejected.append('stopped recorder cannot auto-resume')
    else:raise AssertionError('stopped recorder resumed')
    rec=Recorder(100);bad=context(f[0]);bad['result']=0
    assert rec.event(bad,77,100,reader)=='HOLD_FOR_OWNED_ABORT' and not rec.reads
    stopped('failed context read cannot supply registers',rec)
    rec=Recorder(100);bad=context(f[0]);bad['api']='SetThreadContext'
    assert rec.event(bad,77,100,reader)=='HOLD_FOR_OWNED_ABORT' and not rec.reads
    stopped('context-write proposal cannot supply observation',rec)
    rec=Recorder(100);stopped('empty recorder',rec)
    # The raw context receipt must not alias the caller's mutable dictionary.
    f=fixture();blobs,reader=memory(f);rec=Recorder(100);row=context(f[0]);before=copy.deepcopy(row)
    rec.event(row,77,100,reader);row['context_hex']=''
    assert rec.events[0]['context_read']==before
    result=dict(status='SYNTHETIC_SCOPED_RECORDER_CONTROLS_ONLY',native_calls=0,live_game=False,
                original_code_executed=False,positive=positive,stops=stops,rejected=rejected,
                caller_mutation_does_not_rewrite_receipt=True,
                limitations=['No process/thread binding or owned-debug-event delivery qualification.',
                             'No native pending-event abort, API cleanup or game health qualification.',
                             'No implication that synthetic path or queue fixture exists in FF12.'])
    if args.write:
        with (W/'recorder-control.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    else:
        assert json.loads((W/'recorder-control.json').read_text())==result,'recorded recorder controls differ'
    print('Scoped recorder: complete synthetic chain,',len(rejected),'invalid/stop controls; no native or live execution.')


if __name__=='__main__':main()
