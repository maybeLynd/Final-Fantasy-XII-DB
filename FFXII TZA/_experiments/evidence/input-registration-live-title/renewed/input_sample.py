"""Read the existing EXP006/024 keyboard chain; no OS calls, input or writes.

Finite polling can observe a held byte but cannot prove an arbitrarily brief
transition did not occur. A zero without a positive keyboard control is not a
negative registration verdict. Stable pointers do not exclude ABA reuse.
"""
import struct

MANAGER = 0x02EA5368
FRAME = 0x0208D45C


def exact(reader, address, size):
    value = reader.read(address, size)
    if not isinstance(value, bytes) or len(value) != size:
        raise ValueError('Incomplete read at %#x, requested %d' % (address, size))
    return value


def chain(reader):
    result = []
    address = MANAGER
    for offset in (0xDF8, 0x118, 0x30):
        raw = exact(reader, address, 8)
        pointer = struct.unpack('<Q', raw)[0]
        result.append(dict(address=address, raw=raw.hex(), pointer=pointer))
        if pointer == 0:
            raise ValueError('Null keyboard-chain pointer at %#x' % address)
        address = pointer + offset
    return address, result


def snapshot(reader):
    frame_before = struct.unpack('<I', exact(reader, FRAME, 4))[0]
    address, before = chain(reader)
    raw = exact(reader, address, 256)
    end_address, after = chain(reader)
    frame_after = struct.unpack('<I', exact(reader, FRAME, 4))[0]
    return dict(status='STABLE_CHAIN' if before == after else 'CHANGED_CHAIN',
                array_address=address, array_address_after=end_address,
                chain_before=before, chain_after=after, raw=raw.hex(),
                nonzero_indices=[i for i, value in enumerate(raw) if value],
                frame_before=frame_before, frame_after=frame_after,
                crossed_frame=frame_before != frame_after)
