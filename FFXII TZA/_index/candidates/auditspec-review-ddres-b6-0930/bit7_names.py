"""bit7_names.py - widened bit-7 writer sweep at +0x38 and the atlas name each writer's 0024A5A0 call was given.

  1. every `and`/`or`/`mov` with an immediate at `dword|byte ptr [reg + 0x38]` (non-rsp) whose immediate changes bit 7
     (and: bit 7 clear in the mask; or: bit 7 set; mov: any immediate), image-wide
  2. for each, the nearest preceding call in the same owner (within 12) and, if it is 0024A5A0, its rcx argument:
     walk back from the call to the last write of rcx/ecx; `lea rcx, [rip+X]` is read as a C string
  3. context of the two writers with no preceding call (0033B5B8, 0033B5D3)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402
import textcache as TC  # noqa: E402

T = TC.load()
pos = {a: k for k, (a, s, m, o, w) in enumerate(T)}
pat = re.compile(r"^(dword|byte) ptr \[(r\w+) \+ 0x38\], (0x[0-9a-f]+|\d+)$")


def cstr(va):
    b = I.rd(va, 64) or b""
    return b.split(b"\0")[0].decode("latin-1")


def rcx_of(kcall):
    w = T[kcall][4]
    for j in range(kcall - 1, max(0, kcall - 40), -1):
        a, s, m, o, ww = T[j]
        if ww != w:
            return None
        if re.match(r"^(rcx|ecx)\b", o) and m not in ("cmp", "test", "push"):
            if m == "lea" and o.startswith("rcx, [rip + "):
                d = int(o.split("+ ")[1].rstrip("]"), 16)
                return "'%s'" % cstr(a + s + d)
            if m == "mov" and o.startswith("rcx, qword ptr [rip + "):
                d = int(o.split("+ ")[1].rstrip("]"), 16)
                cell = a + s + d
                q = I.rd(cell, 8)
                p = int.from_bytes(q, "little") if q else 0
                return "'%s' (via %08X%s)" % (cstr(p) if p else "?", cell, " reloc" if cell in I.relocs() else " NOT-reloc")
            return "%08X %s %s" % (a, m, o)
        if m == "call":
            return "(call before rcx write)"
    return None


rows = []
for k, (a, s, m, o, w) in enumerate(T):
    mm = pat.match(o)
    if not mm or mm.group(2) == "rsp" or m not in ("and", "or", "mov"):
        continue
    width, base, imm = mm.groups()
    v = int(imm, 0)
    if m == "and" and (v & 0x80):
        continue
    if m == "or" and not (v & 0x80):
        continue
    kc = None
    for j in range(k - 1, max(0, k - 12), -1):
        if T[j][4] != w:
            break
        if T[j][2] == "call":
            kc = j
            break
    call = T[kc][3] if kc is not None else None
    rows.append((a, m, o, w, call, rcx_of(kc) if call == "0x24a5a0" else None))
print("widened writers (and-clear / or-set / mov-imm of bit 7 at +0x38, non-rsp):", len(rows))
for r in rows:
    print("  %08X %-3s %-36s owner %-8s prev call %-9s name %s" % r)
print("after 0024A5A0:", sum(1 for r in rows if r[4] == "0x24a5a0"), " other:",
      [("%08X" % r[0], r[2], r[4]) for r in rows if r[4] != "0x24a5a0"])
print()
k = pos[0x0033B5B8]
for (a, s, m, o, w) in T[k - 8:k + 8]:
    print("%08X  %-8s %s" % (a, m, o))
