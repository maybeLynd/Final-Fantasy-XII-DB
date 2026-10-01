# -*- coding: utf-8 -*-
"""Image-wide sweep for every access at a given displacement - the route census's blind spot.

WHY THIS EXISTS. The route-tracked censuses only see accesses through a base they followed from an
establishment site. That is what makes them trustworthy: a displacement is not an identity, and
`[rcx+0x60]` and `[rsi+0x60]` are different structures. But it means a reader that reaches the object
by a route the census does not track is invisible. BattleUnit +0x760 was recorded as a 16-byte region
for exactly that reason, and an image-wide sweep found two functions comparing +0x768 against +0x76C
as current-versus-target. The region became four fields.

WHAT THIS COSTS, STATED UP FRONT. A displacement sweep has the failure the census was built to avoid:
it finds every structure that happens to use the same displacement. Its output is a CANDIDATE LIST,
never a fact. A hit becomes evidence only when something independent ties it to this type - the
register's provenance, a semantic pairing like current-versus-target, or a function already known to
take this type. That judgement is not automatable and this tool does not pretend to make it.

THE CONTROL, and it is the whole point. Sweep a displacement the type does NOT have alongside the one
it does. Both will return hits; the question is whether the hits at the real displacement are
distinguishable - clustered in functions already associated with the type - while the control's are
scattered. If the two look alike, the sweep has found nothing about this type and says so.
"""
import io
import sys
import struct
import collections

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
EXE = ROOT + r"\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = ROOT + r"\Database\Tools\work\graph\functions.tsv"

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(nsec)]


def rd(va, n):
    rva = va - base
    for vsz, sva, rsz, ro in secs:
        if sva <= rva < sva + max(vsz, rsz):
            return d[ro + rva - sva: ro + rva - sva + n]
    return b""


funcs = []
for n, l in enumerate(io.open(FUNCS, encoding="utf-8")):
    if not n:
        continue
    c = l.rstrip("\n").split("\t")
    try:
        funcs.append((int(c[0], 16), c[1], int(c[2])))
    except (ValueError, IndexError):
        pass

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
SZ = {1: "byte", 2: "word", 4: "dword", 8: "qword", 16: "xmmword"}


def sweep(disp):
    out = []
    for entry, name, sz in funcs:
        if sz <= 0 or sz > 0x8000:
            continue
        buf = rd(entry, sz)
        if not buf:
            continue
        for ins in md.disasm(buf, entry):
            for op in ins.operands:
                if (op.type == X86_OP_MEM and op.mem.disp == disp and op.mem.base
                        and op.mem.base not in (X86_REG_RIP, X86_REG_RSP, X86_REG_RBP)
                        and ins.mnemonic != "lea" and not ins.mnemonic.startswith("nop")):
                    out.append((entry, name, ins.address, op.size,
                                "%s %s" % (ins.mnemonic, ins.op_str)))
    return out


def report(label, disp, assoc):
    hits = sweep(disp)
    fns = collections.Counter(h[1] for h in hits)
    near = [f for f in fns if any(a.lower() in f.lower() for a in assoc)]
    print("%s +0x%X: %d access(es) in %d function(s); %d function(s) match the type's vocabulary %s"
          % (label, disp, len(hits), len(fns), len(near), assoc))
    for h in hits[:14]:
        mark = " <-" if any(a.lower() in h[1].lower() for a in assoc) else ""
        print("     %08X %-46s %-8s %s%s"
              % (h[2], h[1][:46], SZ.get(h[3], "?"), h[4][:46], mark))
    if len(hits) > 14:
        print("     ... %d more" % (len(hits) - 14))
    return len(hits), len(near)


if __name__ == "__main__":
    target = int(sys.argv[1], 16)
    control = int(sys.argv[2], 16)
    assoc = sys.argv[3].split(",") if len(sys.argv) > 3 else ["BattleUnit", "BattleLocomotion"]
    t_all, t_near = report("TARGET ", target, assoc)
    print()
    c_all, c_near = report("CONTROL", control, assoc)
    print()
    # A CONTROL THAT FINDS NOTHING HAS NOT CONTROLLED ANYTHING. The first control tried here was
    # +0x1A6, one byte off the target, and it returned 0 accesses in the whole image - not because
    # the target is special but because MISALIGNED DISPLACEMENTS BARELY OCCUR in compiled code. A
    # control like that makes any target look significant. This is the second time that confound has
    # appeared in this work, so the tool refuses on it rather than leaving it to be noticed.
    if c_all == 0:
        print("DEGENERATE CONTROL - the control displacement has no accesses anywhere in the image,")
        print("so it measures nothing. Misaligned displacements barely occur in compiled code; pick")
        print("a control at the same alignment as the target.")
        raise SystemExit(2)
    if t_near == 0:
        print("NOTHING PROVED - no hit at the target is in a function associated with the type.")
    elif c_near >= t_near:
        print("NOTHING PROVED - the control displacement, which this type does not have, attracts as")
        print("many associated functions (%d) as the target (%d). The sweep is matching the"
              % (c_near, t_near))
        print("vocabulary, not the structure.")
    else:
        print("The target's hits concentrate in associated functions (%d) far more than the"
              % t_near)
        print("control's (%d). Candidates worth resolving individually - still not yet facts."
              % c_near)
