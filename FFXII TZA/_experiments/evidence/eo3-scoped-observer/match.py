"""EO3 only: qualify correlation logic before connecting it to a live observer.

Synthetic records here test the instrument, not FF12 initialization or scheduling.
No process access, input, debugger, original-code execution or callback effects.
"""
import struct

POOL=0x22c31c0
PRODUCER=0x32e84d
BUILDER=0x32e983
ISSUER=0x32e111
PRIMARY_RETURN=0x377f87
BUILDER_RETURN=0x32e852


def sext(value):
    return struct.unpack('<q',struct.pack('<Q',value if value<0x80000000 else value|0xffffffff00000000))[0]&0xffffffffffffffff


def slot(address, raw):
    assert POOL<=address<POOL+64*0x80 and (address-POOL)%0x80==0,'not a queue slot'
    assert len(raw)==0x80,'incomplete slot snapshot'
    u32=lambda offset:struct.unpack_from('<I',raw,offset)[0]
    u64=lambda offset:struct.unpack_from('<Q',raw,offset)[0]
    index=(address-POOL)//0x80
    assert u32(0x58)==index,'slot ordinal does not match address'
    assert u32(0x64)!=0xffffffff and u32(0x64)&63==index,'no identified live request'
    return dict(address=address,id=u32(0x64),kind=raw[0x21],state=raw[0x20],
                low=u32(0x24),count=u32(0x28),offset=u32(0x2c),
                destination=u64(0x38),original_destination=u64(0x70),raw=raw.hex())


class Match:
    def __init__(self):
        self.producers={};self.requests={};self.results=[]

    def producer(self, ctx, parent_return, path):
        assert ctx['rip']==PRODUCER and ctx['rcx']==0xff
        assert ctx['rdx']==(ctx['rdi']&0xffffffff),'not the staged low32 argument'
        assert parent_return==PRIMARY_RETURN,'not the selected primary map caller'
        assert 1<len(path)<=128 and path.endswith(b'\0') and b'\0' not in path[:-1]
        normalized=path[:-1].replace(b'\\',b'/').lower()
        assert normalized.startswith(b'ps2data/efb/') and normalized.endswith(b'.efb')
        key=(ctx['tid'],ctx['rsp']);assert key not in self.producers,'unresolved producer stack reused'
        self.producers[key]=dict(context=dict(ctx),parent_return=parent_return,path_hex=path.hex())

    def builder(self, ctx, return_address, raw):
        assert ctx['rip']==BUILDER and return_address==BUILDER_RETURN
        # Original pushes24 + sub32 + the call's return8 =0x40.
        key=(ctx['tid'],ctx['rsp']+0x40)
        assert key in self.producers,'builder did not return to this producer frame'
        p=self.producers[key];s=slot(ctx['r10'],raw)
        assert s['state']==1 and s['kind']==0xff
        assert s['low']==p['context']['rdx'] and s['id']==ctx['rax']
        assert s['count']==p['context']['r9']&0xffffffff
        assert s['destination']==s['original_destination']==p['context']['r8']
        assert not any(a==s['address'] for a,i in self.requests),'slot reused before matched issuance'
        self.requests[(s['address'],s['id'])]=dict(producer=p,builder_context=dict(ctx),builder=s)
        del self.producers[key]

    def issuer(self, ctx, raw):
        assert ctx['rip']==ISSUER
        s=slot(ctx['rbx'],raw);key=(s['address'],s['id'])
        assert key in self.requests,'unmatched or reused request at issuer'
        r=self.requests[key]
        assert s['kind']==0xff and s['low']==r['builder']['low'] and s['count']!=0
        assert ctx['rcx']==sext(s['low']),'issued argument is not the observed sign extension'
        p=r['producer']['context']['rdi'];q=ctx['rcx']
        self.results.append(dict(**r,issuer_context=dict(ctx),issuer=s,P=p,Q=q,pointer_preserved=p==q))
        del self.requests[key]

    def finish(self):
        assert self.results and not self.producers and not self.requests,'empty or incomplete selected chain'
        return self.results
