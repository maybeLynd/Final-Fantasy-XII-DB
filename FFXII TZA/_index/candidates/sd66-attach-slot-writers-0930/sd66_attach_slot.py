"""sd66_attach_slot.py - which registrations reach a class descriptor's attach slot (+0x40) outside the five member
routes? (OPUS, 2026-09-30; register SD-66). Scans every catalogued function (Database/Tools/analysis-kit/gfz-scripts/retool.py)
for `mov reg, [static]; ... call [reg + 0x40]` where the static's constructor installs a vtable whose RTTI names a
PClassDescriptor, and asserts the result.
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c, SZ = T.R, T.scan(), T.sizes()
fails = 0
ROUTES = {0x00632960, 0x00632A10, 0x00632A70, 0x00632BE0, 0x00632B30}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def static_vt(g):
    """The vtable a static constructor stores into [g]: `lea reg, [rip -> vt]` then `mov [rip -> g], reg`."""
    for f, a, k in c["refs"].get(g, ()):
        if k != "W":
            continue
        body = list(R.md.disasm(R.at(f, SZ.get(f, 0x200)), f))
        idx = next((n for n, x in enumerate(body) if x.address == a), None)
        if idx is None:
            continue
        src = body[idx].op_str.split(", ")[-1]
        for j in range(idx - 1, max(0, idx - 4), -1):
            if body[j].mnemonic == "lea" and body[j].op_str.startswith(src + ", [rip"):
                return body[j].address + body[j].size + body[j].operands[1].mem.disp
    return None


hits, cache = collections.defaultdict(list), {}
for f, n in SZ.items():
    d = R.at(f, n)
    if not d:
        continue
    b = list(R.md.disasm(d, f))
    for k, i in enumerate(b):
        m = re.match(r"qword ptr \[(r\w+) \+ 0x40\]$", i.op_str) if i.mnemonic == "call" else None
        if not m:
            continue
        for j in range(k - 1, max(0, k - 6), -1):
            p = b[j]
            if p.mnemonic == "mov" and p.op_str.startswith(m.group(1) + ", qword ptr [rip"):
                g = p.address + p.size + p.operands[1].mem.disp
                if g not in cache:
                    vt = static_vt(g)
                    cache[g] = T.rtti_class(vt) if vt else None
                if cache[g] and "PClassDescriptor" in cache[g]:
                    hits[f].append((i.address, g, cache[g]))
                break
for f, v in sorted(hits.items()):
    print("      %08X  %2d calls through [%08X]  %s" % (f, len(v), v[0][1], v[0][2]))
exp = {0x00634540: 3, 0x006349B0: 11, 0x006352A0: 2, 0x006357E0: 1, 0x00635DC0: 2}
check("F1", {f: len(v) for f, v in hits.items()} == exp and not (set(hits) & ROUTES),
      "%d functions, %d calls, none of them the five member routes" % (len(hits), sum(len(v) for v in hits.values())))
cls = {f: v[0][2] for f, v in hits.items()}
check("F2", all("PClassDescriptor" in x for x in cls.values())
      and any("PClassDataMemberDynamic" in x for x in cls.values()) and any("PClassDescriptorDynamic" in x for x in cls.values())
      and any("PClassMember@" in x for x in cls.values()) and any("PClusterDependencyList" in x for x in cls.values())
      and any("PSharray@VPString" in x for x in cls.values()),
      "the descriptors attached to are the reflection system's own classes")
# F3 - the descriptor's +0x40 is a real slot of its vtable (02CF8580 -> vtable 00D56ED0, slot +0x40 = 0062EFD0), and
#      006349B0 passes a member object it filled in itself (02CF9080: +0x48 = 0x38 at 00634A7E, +0x50 = rdi)
s40 = struct.unpack("<Q", R.at(0x00D56ED0 + 0x40, 8))[0]
check("F3", s40 == 0x0062EFD0 and static_vt(0x02CF8580) == 0x00D56ED0
      and "02CF90C8" in T.fmt(next(R.md.disasm(R.at(0x00634A7E, 16), 0x00634A7E, 1)))
      and "02CF9080" in T.fmt(next(R.md.disasm(R.at(0x00634A92, 16), 0x00634A92, 1))),
      "02CF8580's vtable 00D56ED0 has slot +0x40 = 0062EFD0; 006349B0 attaches the member 02CF9080 it built inline")
print("FAILS %d" % fails)
