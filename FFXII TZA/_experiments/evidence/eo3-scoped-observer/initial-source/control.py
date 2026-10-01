"""Synthetic instrument controls; cannot qualify Windows delivery/game health."""
import copy
import json
from pathlib import Path
import struct
from match import Match,POOL,PRODUCER,BUILDER,ISSUER,PRIMARY_RETURN,BUILDER_RETURN,sext

W=Path(__file__).resolve().parent


def fixture(pointer=0x6abcd000):
    tid=77;stack=0x120005000;index=3;ident=(19<<6)|index;dest=0x6a000000
    p=dict(tid=tid,rip=PRODUCER,rsp=stack,rcx=0xff,rdx=pointer&0xffffffff,rdi=pointer,r8=dest,r9=0xffffffff)
    b=dict(tid=tid,rip=BUILDER,rsp=stack-0x40,r10=POOL+index*0x80,rax=ident)
    i=dict(tid=88,rip=ISSUER,rsp=0x120007000,rbx=POOL+index*0x80,rcx=sext(pointer&0xffffffff))
    raw=bytearray(0x80);raw[0x20]=1;raw[0x21]=0xff
    for off,val in [(0x24,p['rdx']),(0x28,0xffffffff),(0x58,index),(0x64,ident)]:struct.pack_into('<I',raw,off,val)
    for off in (0x38,0x70):struct.pack_into('<Q',raw,off,dest)
    return [p,PRIMARY_RETURN,b'PS2Data\\efb\\fixture_primary.efb\0',b,BUILDER_RETURN,raw,i,bytearray(raw)]


def run(f):
    p,pr,path,b,br,raw,i,issued=f;m=Match();m.producer(p,pr,path);m.builder(b,br,raw);m.issuer(i,issued);return m.finish()


def main():
    outcomes=[run(fixture(p))[0] for p in (0x6abcd000,0x100001000,0x18bc13000)]
    assert [r['pointer_preserved'] for r in outcomes]==[True,False,False]
    assert outcomes[1]['Q']==0x1000 and outcomes[2]['Q']==0xffffffff8bc13000
    # Reentry while the outer builder pumps: same thread, two different frames.
    outer=fixture();inner=fixture(0x6bbbd000)
    inner[0]['rsp']-=0x1000;inner[3]['rsp']-=0x1000
    inner[3]['r10']+=0x80;inner[6]['rbx']+=0x80;inner[3]['rax']+=1
    for raw in (inner[5],inner[7]):
        struct.pack_into('<I',raw,0x58,4);struct.pack_into('<I',raw,0x64,inner[3]['rax'])
    nested=Match();nested.producer(*outer[:3]);nested.producer(*inner[:3])
    nested.builder(*inner[3:6]);nested.issuer(*inner[6:])
    nested.builder(*outer[3:6]);nested.issuer(*outer[6:])
    reentry=nested.finish();assert [r['P'] for r in reentry]==[0x6bbbd000,0x6abcd000]
    rejected=[]
    def reject(label,f):
        try:run(f)
        except (AssertionError,KeyError):rejected.append(label)
        else:raise AssertionError('non-discriminating rejection control: '+label)
    f=fixture();f[0]['rdx']=0;reject('pre-assignment/old EDX',f)
    f=fixture();del f[0]['rdi'];reject('old hit record missing RDI',f)
    f=fixture();f[1]=0x377ff8;reject('wrong map-mode caller',f)
    f=fixture();f[3]['rsp']-=0x10;reject('next hit on same thread but different frame',f)
    f=fixture();f[4]=0x32e700;reject('wrong builder return address',f)
    f=fixture();f[3]['r10']+=1;reject('misaligned pool pointer',f)
    f=fixture();struct.pack_into('<I',f[5],0x58,4);reject('wrong slot ordinal',f)
    f=fixture();struct.pack_into('<I',f[7],0x64,(20<<6)|3);reject('slot reused with a new request id',f)
    f=fixture();struct.pack_into('<I',f[7],0x28,0);reject('zero-count path cannot be at this issuer',f)
    f=fixture(0x18bc13000);f[6]['rcx']=f[0]['rdi'];reject('assumed preserved pointer instead of actual issued argument',f)
    try:Match().finish()
    except AssertionError:rejected.append('empty observation')
    else:raise AssertionError('empty passed')
    f=fixture();m=Match();m.producer(*f[:3])
    try:m.finish()
    except AssertionError:rejected.append('producer without completed builder/issuer')
    else:raise AssertionError('incomplete passed')
    result=dict(status='SYNTHETIC_INSTRUMENT_CONTROLS_ONLY',live_game=False,original_code_executed=False,
                positive_results=outcomes,reentry_results=reentry,rejected=rejected,
                limits=['No Windows capture/native-state/health qualification.',
                        'Synthetic fixture path is not a real map identity.',
                        'No claim about actual producer allocation, startup, issue or historical crash.'])
    with (W/'control.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    print('Correlation control: exact frame+return+slot+request-ID;12 misleading/incomplete records rejected. Not a live observation.')


if __name__=='__main__':main()
