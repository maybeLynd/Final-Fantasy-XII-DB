#!/usr/bin/env python3
"""census_field_accessors.py - the image's DEDICATED FIELD ACCESSORS, and what they settle.

WHY. `ActorStorageRecord +0x107` sat at `UNKNOWN` carrying its own admission: *"THE SPLIT RESTS ON
THAT SINGLE READ."* One byte load against an initialiser that zeroed both halves as a word is
exactly the shape where the wider reading is safer - a compiler reading a packed field's high byte
looks identical to a byte field's own load. What settled it was not re-reading the field but finding
that `00263B80` is an EIGHT-BYTE FUNCTION whose entire body is that load, with three live callers.

**An accessor is better evidence of a field than an access is.** An access says some instruction
touched those bytes. A whole function that exists to return exactly those bytes, at exactly that
width, says the compiler was given a member and emitted a getter for it. So they are worth having
as a population rather than one at a time.

WHAT COUNTS AS ONE, and the rules are deliberately tight:

  GETTER  the body is one load from `[<arg reg> + disp]` into the return register, then `ret`.
  SETTER  the body is one store of an argument register into `[<arg reg> + disp]`, then `ret`.

Nothing with a branch, a call, a second memory reference, an index register or arithmetic on the
value qualifies. A function that loads and then tests is not an accessor - it is a predicate, and
its width tells you about the test rather than the member.

WHAT THIS DOES NOT ESTABLISH. **An accessor proves a member at that displacement and width; it does
NOT say which TYPE.** The receiver is whatever the callers pass, and this file does not resolve it -
joining an accessor to a field row by offset alone would repeat the mistake of reading a stride as
an extent. The join below is therefore printed as CANDIDATES for a human, never applied, and a
candidate is only interesting when its width matches the row's declared size.

THE POPULATION IS THE LISTED FUNCTION BODIES, and bodies whose listed length ends mid-instruction
are counted and skipped rather than guessed at.
"""
import collections
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP          # noqa: E402
import disasm_fn as DF          # noqa: E402
import resolve_switch_arms as R  # noqa: E402

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_REG, X86_OP_MEM
except ImportError:
    sys.stderr.write("census_field_accessors: needs capstone\n")
    raise SystemExit(2)

ARGS = {"rcx", "rdx", "r8", "r9"}
LOADS = {"mov", "movzx", "movsx", "movsxd", "movss", "movsd", "movups", "movaps", "movdqu"}
MAXBYTES = 24


def classify(ins):
    """GETTER / SETTER / None for a decoded body."""
    if len(ins) != 2 or ins[1].mnemonic != "ret":
        return None
    i = ins[0]
    if i.mnemonic not in LOADS or len(i.operands) != 2:
        return None
    dst, src = i.operands
    if dst.type == X86_OP_REG and src.type == X86_OP_MEM:
        mem, kind = src, "GETTER"
    elif dst.type == X86_OP_MEM and src.type == X86_OP_REG:
        mem, kind = dst, "SETTER"
    else:
        return None
    if not mem.mem.base or mem.mem.index:
        return None
    if R.norm64(i.reg_name(mem.mem.base)) not in ARGS:
        return None
    return kind, mem.mem.disp, mem.size, R.norm64(i.reg_name(mem.mem.base))


def reach(img, found):
    """HOW each accessor is reached - which is ownership information, and needs no receiver.

    Two sweeps, both exact. A rel32 `call`/`jmp` sweep of `.text` counts DIRECT callers. A qword
    sweep of every other section asks whether the accessor's ADDRESS IS STORED IN DATA, which is the
    shape of a vtable or function-table slot. Three classes fall out:

      CALLED       at least one direct rel32 caller.
      DISPATCHED   no direct caller, but its address sits in a data qword - reached indirectly.
                   For a getter this says the member is behind virtual dispatch, which is a fact
                   about the contract rather than about the bytes.
      UNREFERENCED neither. Nothing in the image calls it and nothing stores it.

    TWO LIMITS, STATED BECAUSE THE CLASSES ARE ONLY AS GOOD AS THEM. A qword that happens to equal a
    function address is SHAPED like a table slot; this does not prove it IS a vtable, only that the
    address is stored somewhere a dispatcher could read. And a zero direct-caller count excludes
    calls through a register loaded by any route this does not follow, so UNREFERENCED means
    "unreferenced by these two sweeps", never "dead".
    """
    import struct
    acc = dict((f[0], (f[2], f[3], f[4])) for f in found)
    sec = [s for s in img.secs if s[0] == ".text"][0]
    _n, va, _vs, ra, rs = sec
    base, data = img.base + va, img.d[ra:ra + rs]
    cnt = collections.Counter()
    for i in range(len(data) - 5):
        if data[i] not in (0xE8, 0xE9):
            continue
        t = base + i + 5 + struct.unpack_from("<i", data, i + 1)[0]
        if t in acc:
            cnt[t] += 1
    stored = set()
    for nm, _sva, _vsz, rra, rrs in img.secs:
        if nm == ".text":
            continue
        d = img.d[rra:rra + rrs]
        for i in range(0, max(0, len(d) - 8), 8):
            v = struct.unpack_from("<Q", d, i)[0]
            if v in acc:
                stored.add(v)
    # THE THIRD ROUTE, AND ITS ABSENCE ONCE EMPTIED A WHOLE CLASS. 7589c1822 published
    # "UNREFERENCED 27 - neither sweep finds it" off the two sweeps above, with the caveat that it
    # meant unreferenced BY THOSE TWO and never "dead". Cashing that caveat: a function address also
    # enters a program by having its address TAKEN - `lea r64, [rip + func]` - and every one of
    # those 27 is lea-referenced. The class was an artifact of a missing sweep, not a finding.
    taken = collections.Counter()
    for i in range(len(data) - 7):
        if (data[i] & 0xF8) != 0x48 or data[i + 1] != 0x8D:
            continue
        if (data[i + 2] & 0xC7) != 0x05:
            continue
        t = base + i + 7 + struct.unpack_from("<i", data, i + 3)[0]
        if t in acc:
            taken[t] += 1
    called = [a for a in acc if cnt[a]]
    zero = [a for a in acc if not cnt[a]]
    disp = [a for a in zero if a in stored]
    rest = [a for a in zero if a not in stored]
    addrt = [a for a in rest if a in taken]
    unref = [a for a in rest if a not in taken]
    print("  HOW THEY ARE REACHED - ownership information that needs no receiver:")
    print("      CALLED         %3d   at least one direct rel32 caller" % len(called))
    print("      DISPATCHED     %3d   no direct caller; address stored in a data qword" % len(disp))
    print("      ADDRESS-TAKEN  %3d   no caller and not stored, but `lea r64,[rip+f]` takes it"
          % len(addrt))
    print("      UNREFERENCED   %3d   none of the three finds it" % len(unref))
    print("      (%d have their address stored in data; %d have it taken by a lea.)"
          % (len(stored), len(taken)))
    print("      A stored qword is SHAPED like a table slot and is not proof of a vtable. And")
    print("      UNREFERENCED still means unreferenced BY THESE THREE SWEEPS, never 'dead' - the")
    print("      previous version of this file said that about TWO sweeps and the missing third")
    print("      emptied the class entirely, which is the standing warning against reading it")
    print("      as a finding.")
    print("  MOST-CALLED:")
    for a, n in cnt.most_common(6):
        k, d, w = acc[a]
        print("      %08X  %s +0x%-6X %dB  %d callers" % (a, k[0], d, w, n))
    trio = [(a, n) for a, n in cnt.most_common(3)]
    if len(trio) == 3 and len(set(n for _a, n in trio)) == 1:
        ds = sorted(acc[a][1] for a, _n in trio)
        print("      The top three share a caller count exactly (%d each) at +0x%X/+0x%X/+0x%X -"
              % (trio[0][1], ds[0], ds[1], ds[2]))
        print("      a member trio always written together, not three independent fields.")
    return 0


def main():
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    img = DF.Image(KP.EXE)
    ex = R.extents()
    found = []
    scanned = badextent = 0
    for start, nbytes in ex.items():
        if not nbytes or nbytes > MAXBYTES:
            continue
        scanned += 1
        try:
            ins = R.decode(img, md, start, nbytes)
        except SystemExit:
            badextent += 1
            continue
        c = classify(ins)
        if c:
            found.append((start, nbytes) + c)

    print("DEDICATED FIELD ACCESSORS IN THE SHIPPED IMAGE")
    print("  listed bodies of <= %d bytes scanned        : %d" % (MAXBYTES, scanned))
    print("  skipped, listed length ends mid-instruction : %d" % badextent)
    print("  accessors found                             : %d" % len(found))
    kinds = collections.Counter(f[2] for f in found)
    print("      GETTER %d   SETTER %d" % (kinds["GETTER"], kinds["SETTER"]))
    widths = collections.Counter(f[4] for f in found)
    print("  by access width:", "  ".join("%dB:%d" % (w, widths[w]) for w in sorted(widths)))
    regs = collections.Counter(f[5] for f in found)
    print("  by receiver register:", "  ".join("%s:%d" % (r, regs[r]) for r in sorted(regs)))
    print()
    print("  THE WIDTH IS THE MEMBER'S, THE RECEIVER IS NOT RESOLVED HERE. An accessor proves a")
    print("  member at that displacement and width; which TYPE owns it is whatever the callers")
    print("  pass, and this file does not follow them.")
    print()
    # THE CONTROL IS MANDATORY. 00263B80 was read by hand and published in ad3a64f8a as an
    # eight-byte getter for a one-byte member at +0x107. If this scan cannot find it, the scan is
    # wrong and every absence below is worthless. A checker that can only say `fine` has not been
    # shown to be reading anything.
    by_addr = dict((f[0], f) for f in found)
    ctl = by_addr.get(0x263B80)
    ok = ctl is not None and ctl[2] == "GETTER" and ctl[3] == 0x107 and ctl[4] == 1
    print("  CONTROL  00263B80 recovered as an 8-byte GETTER of 1 byte at +0x107: %s"
          % ("PASS" if ok else "FAIL -> %r" % (ctl,)))
    if not ok:
        return 2
    print()

    # CANDIDATES for the rows that admit they do not know. Joined BY OFFSET AND WIDTH ONLY, which
    # is not proof of ownership - the receiver is whatever the callers pass, and this file does not
    # follow them. Printed for a human; never applied.
    fields = os.path.join(KP.DB, "_types", "fields.tsv")
    raw = io.open(fields, encoding="utf-8", newline="").read().split("\n")
    head = raw[0].split("\t")
    J = {k: head.index(k) for k in head}

    def num(s):
        s = (s or "").strip()
        try:
            return int(s, 16) if s.lower().startswith("0x") else int(s)
        except ValueError:
            return None

    acc = collections.defaultdict(list)
    for a, n, k, d, w, r in found:
        acc[(d, w)].append((a, k))
    cands = []
    for line in raw[1:]:
        if not line.strip():
            continue
        c = line.split("\t")
        if c[J["confidence"]].strip().upper() != "UNKNOWN":
            continue
        if c[J["name"]].startswith("unobserved"):
            continue
        off, size = num(c[J["offset"]]), num(c[J["size"]])
        if off is None or not size:
            continue
        hit = acc.get((off, size))
        if hit:
            cands.append((c[J["type"]], c[J["offset"]], c[J["name"]], size, hit))
    print("  UNKNOWN-CONFIDENCE ROWS WITH AN ACCESSOR AT THE SAME OFFSET AND WIDTH: %d" % len(cands))
    print("  CANDIDATES ONLY - the receiver is not resolved, so an offset match is a lead and not")
    print("  ownership. Joining on offset alone would repeat reading a stride as an extent.")
    print("  CALIBRATED BY RESOLVING TWO, AND BOTH WERE COINCIDENCE. `Widget +0x058` matched")
    print("  0081D520, whose ONE caller 00828050 sits with it in the middleware band, nowhere near")
    print("  the widget functions this corpus reads - 002465F0, 00246AD0, 002482E0, 005C5230.")
    print("  `InventoryCategoryListDescriptor +0x000` matched 00263980 and looked plausible on a")
    print("  first glance at its caller's ADDRESS BAND, which is exactly why a band is not a test:")
    print("  00234200 passes its own rdx argument, with no rip-relative load of the descriptor")
    print("  table anywhere near, and two instructions earlier it calls 00263E30 - IN THIS VERY")
    print("  LIST as a getter at +0x30. The receiver therefore has at least 0x38 bytes and the")
    print("  descriptor is 0x8. Same offset, same width, different type.")
    print("  SO: TWO CHECKED, TWO COINCIDENCES. Read this list as leads to be disproved, not")
    print("  findings, and treat +0x000 as the weakest match there is - a getter at displacement")
    print("  zero fits every type's first field. The instrument disproved its own lead here, which")
    print("  is the use it is actually good for.")
    for t, off, name, size, hit in cands:
        print("      %-30s %-8s %-24s %dB  %s" % (t, off, name, size,
              " ".join("%08X(%s)" % (a, k[0]) for a, k in hit[:4])))
    print()
    reach(img, found)
    print()
    bydisp = collections.defaultdict(list)
    for a, n, k, d, w, r in found:
        bydisp[(d, w)].append((a, k))
    print("  DISPLACEMENTS WITH THE MOST ACCESSORS (a hot member offset, any type):")
    for (d, w), lst in sorted(bydisp.items(), key=lambda kv: -len(kv[1]))[:10]:
        print("      +0x%-6X %dB  %d accessor(s)   %s" % (d, w, len(lst),
              " ".join("%08X(%s)" % (a, k[0]) for a, k in lst[:4])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
