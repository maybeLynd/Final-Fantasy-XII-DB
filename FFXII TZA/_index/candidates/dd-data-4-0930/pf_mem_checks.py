"""Checks for the memory page (SWE2-DATA 2026-09-30, DD owner read batch 4). Static: the shipping image through
../rc22-34-resource-readers-0930/pe.py.

  M1 MSVCP140 `?_Xbad_alloc@std@@YAXXZ`: the import directory gives its IAT slot; every rip-relative call/jmp through
     the slot (pe.raw_rip_refs, independent of the function list) is counted, with its owning listed function
  M1c control: the same sweep finds references through the ucrtbase `malloc` slot
  M1d `_set_new_mode` IS called: its one slot reference is the import thunk 00862046, which only 00808D5C reaches
     (rel32 tail jump 00808D70); 00808D5C passes 005C5230() (xor eax, eax / ret: 0), and its pointer is the first
     entry of the C++ initializer table at .rdata 008C31D8 - so the startup sets new-mode 0 explicitly
  M2 00244200 loads the block cells 022D8EAC (+0x9C), 022D8EA8 (+0x98) and 022D8EB4 (+0xA4) (00244224, 0024422E,
     00244236), shifts the +0x9C width right by 6 (00244241), forms +0x98 * +0xA4 * +0x9C >> 6 (00244236..0024425A),
     packs the shifted width twice beside 0x333C (00244260..00244278) and calls 0039D0C0 (0024427B)
  M3 00244200 has exactly one rel32 caller in .text (E8/E9 scan)
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis, raw_rip_refs, owner, text_range, BASE  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def imports():
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    opt = pe + 24
    imp_rva = struct.unpack_from("<I", d, opt + 112 + 8)[0]  # PE32+ data directory 1
    out = {}
    o = off(BASE + imp_rva)
    while True:
        oft, _, _, name, ft = struct.unpack_from("<IIIII", d, o)
        if name == 0:
            break
        dll = d[off(BASE + name):d.index(b"\0", off(BASE + name))].decode().lower()
        i = 0
        while True:
            thunk = struct.unpack_from("<Q", d, off(BASE + (oft or ft)) + 8 * i)[0]
            if thunk == 0:
                break
            if not thunk >> 63:
                hn = off(BASE + (thunk & 0x7FFFFFFF)) + 2
                out[(dll, d[hn:d.index(b"\0", hn)].decode())] = BASE + ft + 8 * i
            i += 1
        o += 20
    return out


imp = imports()
slot = {k[1]: v for k, v in imp.items() if k[1] in ("?_Xbad_alloc@std@@YAXXZ", "malloc", "_set_new_mode")}
print("   IAT slots: %s" % {k: "%08X" % v for k, v in slot.items()})
xb = [r for r in raw_rip_refs(slot["?_Xbad_alloc@std@@YAXXZ"], slot["?_Xbad_alloc@std@@YAXXZ"] + 8)
      if r[1] in ("call", "jmp")]
own = sorted(set(owner(r[0]) for r in xb))
print("   _Xbad_alloc: %d call/jmp sites in %d listed functions (%d sites outside a listed function)"
      % (len(xb), len([o for o in own if o is not None]), sum(1 for r in xb if owner(r[0]) is None)))
check("M1 _Xbad_alloc sites counted", len(xb) > 0, "%d sites, %d functions" % (len(xb), len(own)))
ml = raw_rip_refs(slot["malloc"], slot["malloc"] + 8)
sn = raw_rip_refs(slot["_set_new_mode"], slot["_set_new_mode"] + 8)
check("M1c control: malloc's slot is referenced", len(ml) > 0, "malloc %d" % len(ml))
t0_, t1_, ro_ = text_range()
tb = d[ro_:ro_ + (t1_ - t0_)]
thunk_callers = [t0_ + p for p in range(len(tb) - 5) if tb[p] in (0xE8, 0xE9)
                 and t0_ + p + 5 + struct.unpack_from("<i", tb, p + 1)[0] == 0x00862046]
st = {x.address: x for x in dis(0x00808D5C)}
z = dis(0x005C5230)
check("M1d _set_new_mode(0) is called once at startup: thunk 00862046 <- 00808D5C, first C++ initializer",
      [(r[0], r[1]) for r in sn] == [(0x00862046, "jmp")] and thunk_callers == [0x00808D70]
      and st[0x00808D65].op_str == "0x5c5230" and st[0x00808D6A].op_str == "ecx, eax"
      and [(x.mnemonic, x.op_str) for x in z] == [("xor", "eax, eax"), ("ret", "")]
      and struct.unpack_from("<Q", d, off(0x008C31D8))[0] == 0x00808D5C)


def rip_t(x):
    import re
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


a = {x.address: x for x in dis(0x00244200)}
check("M2 00244200: width +0x9C >> 6, +0x98 * +0xA4 * +0x9C >> 6, packed beside 0x333C, call 0039D0C0",
      rip_t(a[0x00244224]) == 0x022D8EAC and rip_t(a[0x0024422E]) == 0x022D8EA8 and rip_t(a[0x00244236]) == 0x022D8EB4
      and a[0x00244241].op_str == "edx, 6" and a[0x0024425A].op_str == "eax, 6"
      and a[0x00244269].op_str == "edx, 0x333c" and a[0x0024426E].op_str == "rax, 0x333c0000"
      and a[0x0024427B].op_str == "0x39d0c0")
t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]
callers = []
for p in range(len(blob) - 5):
    if blob[p] in (0xE8, 0xE9) and t0 + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == 0x00244200:
        callers.append(t0 + p)
print("   rel32 callers of 00244200: %s" % ["%08X" % c for c in callers])
check("M3 00244200 has exactly one rel32 caller", len(callers) == 1)
print("RESULT _Xbad_alloc: the sites and functions counted above; _set_new_mode(0) runs once at startup; 00244200 width arithmetic measured")
print("FAILS %d" % FAILS)
