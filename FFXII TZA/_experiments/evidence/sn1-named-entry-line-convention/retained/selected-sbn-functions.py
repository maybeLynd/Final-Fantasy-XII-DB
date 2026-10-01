def sbn_blocks(b):
    n = struct.unpack_from('<I', b, 0)[0]
    offs = struct.unpack_from('<%dI' % n, b, 4)
    return list(zip(offs, list(offs[1:]) + [len(b)]))

def sbn_group_read(b, o):
    L, base = struct.unpack_from('<II', b, o)
    p = o + 8
    lines, groups, rem = ([], [base], L)
    while rem > 0:
        k = min(32, rem)
        lines += [base + r for r in struct.unpack_from('<%dH' % k, b, p)]
        p += 2 * k
        rem -= k
        if rem > 0:
            base = struct.unpack_from('<I', b, p)[0]
            p += 4
            groups.append(base)
    return (L, groups, lines, p)
