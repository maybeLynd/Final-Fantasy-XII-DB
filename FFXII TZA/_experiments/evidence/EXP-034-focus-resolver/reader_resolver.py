"""Read-only counterpart to the inspected resolver chain; non-atomic reads.
Unreadable memory is an error, not the engine's legitimate null result.
Caller must qualify process/code identity and bracket with state/identity checks.
"""
import struct


def resolve(reader,handle):
    if not isinstance(handle,int) or not 0<=handle<=0xFFFFFFFF:raise ValueError('u32 handle required')
    def read(address,fmt):
        size=struct.calcsize(fmt);raw=reader.read(address,size)
        if not isinstance(raw,bytes) or len(raw)!=size:raise ValueError('invalid read %#x/%d'%(address,size))
        return struct.unpack(fmt,raw)[0]
    result=dict(handle=handle,actor=0,unit=0,reason=None)
    def absent(reason):
        result['reason']=reason
        return result
    if not read(0x2089340,'<B')&0x10:return absent('field_gate_off')
    if handle==0:return absent('zero_handle')
    index=handle&0xFFFF;manager=(handle>>16)&15;disc=(handle>>20)&0x7FF
    result.update(index=index,manager=manager,discriminator=disc)
    if manager>=5:return absent('manager_out_of_range')
    slot=0x2098E10+manager*0x288
    vector=read(slot+8,'<Q')
    if not vector:return absent('null_vector')
    if not read(slot,'<Q'):return absent('null_storage')
    if index>=read(slot+0x20,'<i'):return absent('capacity_bound')
    if not read(slot+0x10,'<B')&1:return absent('manager_disabled')
    if index>=read(vector,'<i'):return absent('vector_count_bound')
    actor=read(vector+8+index*8,'<Q')
    if not actor:return absent('null_entry')
    if read(actor+0x16,'<H')!=disc:return absent('discriminator_mismatch')
    result['actor']=actor
    result['unit']=read(actor+0x30,'<Q')
    result['reason']='resolved' if result['unit'] else 'actor_without_unit'
    return result
