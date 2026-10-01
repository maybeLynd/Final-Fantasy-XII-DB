"""wdc_slot10.py WDC_DUMP : for each PClassDescriptorWithoutDefaultConstructor<T> vtable in rtti_vtables.py output, read
slot 10 (vt+0x50). When the body resolves descriptors through 0063BC00, name each descriptor by the class of the vtable its
initialiser stores into it (a `lea reg,[vtable] ; mov [descriptor], reg` pair anywhere in .text, RTTI locator at vt-8)."""
import sys, struct, re, collections
exec(open('disw.py').read().split("fn = int")[0])

TEXT_LO, TEXT_HI = 0x121000, 0x8C2000
t = bytes(d)


def q(va):
    return struct.unpack_from("<Q", t, off(va))[0]


def rtti_name(vt):
    try:
        col = q(vt - 8)
        o = off(col)
        if o is None:
            return None
        td_rva = struct.unpack_from("<I", t, o + 12)[0]
        s = t[off(0x120000 + td_rva) + 16:off(0x120000 + td_rva) + 200].split(b"\0")[0].decode("latin1")
        return s
    except Exception:
        return None


# index every `mov qword ptr [rip+X], reg` whose preceding instruction is `lea reg, [rip+VT]`: descriptor -> vtable
lo, hi = off(TEXT_LO), off(TEXT_HI)
desc_vt = collections.defaultdict(set)
for o in range(lo, hi - 14):
    if t[o] in (0x48, 0x4C) and t[o + 1] == 0x8D and (t[o + 2] & 0xC7) == 0x05:
        if t[o + 7] in (0x48, 0x4C) and t[o + 8] == 0x89 and (t[o + 9] & 0xC7) == 0x05 and (t[o + 2] & 0x38) == (t[o + 9] & 0x38) and (t[o] & 4) == (t[o + 7] & 4):
            va = TEXT_LO + (o - lo)
            vt = va + 7 + struct.unpack_from("<i", t, o + 3)[0]
            dst = va + 14 + struct.unpack_from("<i", t, o + 10)[0]
            desc_vt[dst].add(vt)

for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    m = re.match(r"([0-9A-F]{8}) \.\?AV\?\$PClassDescriptorWithoutDefaultConstructor@V(\w+)@", line)
    if not m:
        continue
    vt = int(m.group(1), 16)
    s10 = q(vt + 0x50)
    descs = []
    if s10 in funcs:
        ins = list(md.disasm(t[off(s10):off(s10) + funcs[s10]], s10))
        for k, x in enumerate(ins):
            if x.mnemonic == "call" and x.op_str == "0x63bc00":
                for y in reversed(ins[max(0, k - 3):k]):
                    if y.mnemonic == "lea" and y.op_str.startswith("rcx, [rip + "):
                        dv = y.address + y.size + int(y.op_str.split("rip + ")[1].rstrip("]"), 16)
                        nm = sorted(filter(None, (rtti_name(v) for v in desc_vt.get(dv, ()))))
                        descs.append("%08X=%s" % (dv, nm[0] if nm else "?"))
                        break
    print("%-40s slot10 %08X %-22s %s" % (m.group(2), s10, names.get(s10, "")[:22], "  ".join(descs)))
