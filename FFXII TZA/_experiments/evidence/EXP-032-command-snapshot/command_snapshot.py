"""Raw command snapshot for an already selected, qualified BattleUnit.

No process discovery, OS calls, input, debugger or writes. Reader supplies read()
and caller supplies the unit/slot/actor from a fresh field census. Frame brackets
and stable identity guards do not make these sequential reads atomic.
"""
import struct

FRAME=0x0208D45C


def exact(reader,address,size):
    raw=reader.read(address,size)
    if not isinstance(raw,bytes) or len(raw)!=size:
        raise ValueError('invalid read %#x/%d'%(address,size))
    return raw


def command_block(raw):
    if len(raw)!=24:raise ValueError('command block must be24 bytes')
    context=struct.unpack_from('<Q',raw,8)[0]
    return dict(raw=raw.hex(),flags=struct.unpack_from('<I',raw,0)[0],
                action_context=context,context_is_sentinel=context in (0,0xFFFFFFFFFFFFFFFF),
                target_focus_handle=struct.unpack_from('<I',raw,16)[0],
                action_id=struct.unpack_from('<H',raw,20)[0])


def snapshot(reader,unit,slot,actor):
    if unit<=0 or actor<=0 or not 0<=slot<32:raise ValueError('invalid selected identity')
    frame_before=struct.unpack('<I',exact(reader,FRAME,4))[0]
    before=exact(reader,unit,24)
    index_before=exact(reader,unit+0xEA9,1)[0]
    if not before[0]&1 or index_before!=slot or struct.unpack_from('<Q',before,16)[0]!=actor:
        raise ValueError('selected unit identity mismatch')
    phases=exact(reader,unit+0x6B4,3)
    blocks=exact(reader,unit+0x700,48)
    after=exact(reader,unit,24)
    index_after=exact(reader,unit+0xEA9,1)[0]
    frame_after=struct.unpack('<I',exact(reader,FRAME,4))[0]
    if before!=after or index_before!=index_after:
        raise ValueError('unit header changed across command reads')
    return dict(unit=unit,slot=slot,actor=actor,identity_raw=before.hex(),
                frame_before=frame_before,frame_after=frame_after,
                crossed_frame=frame_before!=frame_after,phase_raw=phases.hex(),
                action_phase=phases[0],unnamed_6b6=phases[2],
                live=command_block(blocks[:24]),shadow=command_block(blocks[24:]))
