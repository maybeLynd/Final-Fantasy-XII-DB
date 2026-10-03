"""Raw reference index: E8/E9 rel32, 0F 8x rel32, EB/7x rel8, rip-relative disp32 (decoded), image-base-relative
disp32 == RVA (decoded), and absolute qwords == VA in every section."""
import struct


def raw_refs(img, target):
    base = img.base
    out = []
    rva_t = target - base
    for name, sva, vs, ra, rs in img.secs:
        d = img.d[ra:ra + rs]
        sbase = base + sva
        is_text = name == ".text"
        # absolute qwords
        tq = struct.pack("<Q", target)
        p = d.find(tq)
        while p >= 0:
            out.append(("abs64", sbase + p, name))
            p = d.find(tq, p + 1)
        if not is_text:
            continue
        n = len(d)
        for p in range(n - 4):
            b = d[p]
            rel = struct.unpack_from("<i", d, p + 1)[0] if p + 5 <= n else None
            if b in (0xE8, 0xE9) and rel is not None and sbase + p + 5 + rel == target:
                out.append(("call" if b == 0xE8 else "jmp", sbase + p, name))
            if b == 0x0F and p + 6 <= n and 0x80 <= d[p + 1] <= 0x8F:
                r2 = struct.unpack_from("<i", d, p + 2)[0]
                if sbase + p + 6 + r2 == target:
                    out.append(("jcc32", sbase + p, name))
            if (b == 0xEB or 0x70 <= b <= 0x7F) and p + 2 <= n:
                r1 = struct.unpack_from("<b", d, p + 1)[0]
                if sbase + p + 2 + r1 == target:
                    out.append(("rel8", sbase + p, name))
        # rip-relative and image-base-relative: scan disp32 and confirm by decoding back
        for p in range(n - 4):
            disp = struct.unpack_from("<i", d, p)[0]
            cand = None
            if disp == rva_t:
                cand = "ibr"
            else:
                for k in (0, 1, 2, 4):
                    if sbase + p + 4 + k + disp == target:
                        cand = "rip"
                        break
            if not cand:
                continue
            va = sbase + p
            for back in range(1, 12):
                st = va - back
                try:
                    ins = list(img.cs.disasm(img.read(st, 16), st, 1))
                except Exception:
                    continue
                if not ins:
                    continue
                i = ins[0]
                if i.address + i.size < va + 4:
                    continue
                ok = False
                for op in i.operands:
                    if op.type == 3:
                        m = op.mem
                        if m.base and i.reg_name(m.base) == "rip" and i.address + i.size + m.disp == target:
                            ok = True
                        elif cand == "ibr" and m.disp == rva_t:
                            ok = True
                if ok:
                    out.append((cand, i.address, "%s %s" % (i.mnemonic, i.op_str)))
                    break
    return sorted(set(out), key=lambda x: x[1])
