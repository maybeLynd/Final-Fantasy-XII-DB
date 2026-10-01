#!/usr/bin/env python3
"""check_ctor_clears.py - which UNKNOWN bytes are nonetheless zero-initialised by a constructor.

**UNREAD IS NOT UNTOUCHED, AND THE TWO QUESTIONS HAVE DIFFERENT INSTRUMENTS.** Every closure scan in
this kit answers *what reads or individually writes these bytes*. None answers *what writes them in
bulk*, and a span with no accessor is routinely described as though the first answer settled both.
On 2026-09-19 that gap turned up three times in one day:

* `BattleUnit +0x298` - 1,016 bytes *"unreached on six routes"*, and cleared by
  `memset(unit + 0x80, 0, 0x610)` in `BattleUnit_ResetStateForReuse`.
* `ManagerSingleton0209BE80 +0xB244` - **23,224 bytes**, about a third of every unknown byte in the
  database, reached zero times on five routes, and zeroed wholesale by `memset(this, 0, 0x10FD0)` -
  the **first instruction** of the constructor `types.tsv` already named.
* `SavePayload` - three spans totalling 11,940 bytes with no access at all, all inside
  `memset(02164280, 0, 0x56690)`, the whole save image.

Each was found by hand, after the span had been published as unreached. This makes it a sweep.

WHY IT MATTERS FOR RECONSTRUCTION AND NOT ONLY FOR TIDINESS. A field nobody reads still has a value,
and *zero from construction* is a fact a reimplementation has to reproduce. Allocate the object
without the clear and it differs from the engine in bytes **no test will catch**, precisely because
nothing reads them yet - until something does.

THE TEST. For every type whose `types.tsv` row records a constructor address, disassemble that body
and look for a `memset` whose destination is `this` and whose length is a literal. `this` means `rcx`
still holds the incoming argument: unmodified, or saved to another register and passed back. The
length is compared against the type's declared size, and the type's gap-named rows are then checked
against the cleared extent.

**A CLEAR IS A LIFETIME FACT, NOT A SEMANTIC ONE.** It says the bytes start at zero, never what they
are for, and never that the clear is the only writer - a later bulk copy, a `rep stos`, or a write
through a pointer handed elsewhere are all outside this test.

WHAT IT FOUND, AND WHY THAT IS THE RIGHT RESULT. Of **40** types whose row records a constructor,
**2** clear the whole object, and **both were already established** - `ManagerSingleton0209BE80`
(`00291750`, `0x10FD0`), published the same day this was written, and `CharacterRenderRecord`
(`0041F730`, `0x740`), which the record-array page and the pool-lifecycle contract both already state
as *"`0041F730` opens with `memset(record, 0, 0x740)`"*. **A new instrument whose every hit is a fact
somebody else already checked is behaving correctly**; that is what earns it the right to be believed
on a hit nobody has checked.

What it adds over the prose is the **quantity**: it reports how many of a type's gap-named bytes the
clear covers - **25,682 bytes across 19 spans** for the singleton, **253 across 42** for the record -
which is the figure a reconstruction needs and which no page states.

HOW GOOD ARE THE CANDIDATES? **It depends entirely on the size, and the first framing of this note
was wrong.** Six of the six LARGEST read as genuine, and I nearly wrote that the match was
"high-precision" full stop. It is not. Two discriminators separate the real from the coincidental,
and both are now printed:

* **SITE COUNT.** A size with one or two `memset` sites in the whole image is a type; a size with
  **73** of them is just a common number. `ManagerSub00A0Entry` is `0x100`, `SaveImageHeader` is
  `0x200`, `SteeringRecord` is `0x80` - 73, 33 and 36 sites respectively, and no useful signal in any
  of them.
* **A STACK DESTINATION IS NOT THE OBJECT.** `lea rcx, [rsp + 0x40]` or `[rbp - 0x10]` clears a local
  buffer that merely happens to be the same size. Every one of the small-size candidates resolves
  this way - `MovementContext`, `TextDrawState`, `BattleResultRecord`, `EfxCallerTemplate`,
  `CharacterRenderSystemTail` - and none of them is evidence about the type at all.

With those applied, the candidates worth reading are the ones with **few sites and a non-stack
destination**, and the six largest are exactly that set:

* `SpawnKeepImage` `0x20010` - `SpawnKeep_SerializePersistenceBank`, `rcx` is the incoming argument.
* `BattleSystemState` `0x7410` - `002370C0`, destination `[rip -> a global pointer]`; already
  documented as the block reset.
* `ImageBackedStateBlock` `0x4818` - `SaveRuntime_InitializeHeaderAndImageBackedState`, a second
  `memset` after the `0x58` header clear.
* `PersistentFlagPayload` `0x1538` - `002EF2D0` calls the buffer getter and clears `rax + 0x200`, the
  persistent payload base `U-5` identifies; the cleared extent **ends exactly where
  `unobservedSpan1538` begins**.
* `ManagerSub0209BE80_57E0ArrayRecord` `0x2A0` - `00333030`, `rcx` is the incoming record.
* `ActorManagerSlot` `0x288` - `00266D10`, a `rip`-relative static array cleared slot by slot.

    python check_ctor_clears.py --self-test
    python check_ctor_clears.py
"""
import argparse
import collections
import csv
import io
import os
import re
import sys

import kit_paths as KP
import check_literal_citations as CLC
import member_reach_scan as MRS
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_REG_RCX

MEMSET = 0x00861EC0
TYPES = os.path.join(KP.DB, "_types", "types.tsv")
FIELDS = os.path.join(KP.DB, "_types", "fields.tsv")
GAP = re.compile(r"unobserved|unknown|gap|pad|span", re.I)


def find_this_memset(img, md, sizes, ctor):
    """(site, length) for a memset(this, 0, literal) in `ctor`, else None.

    `this` is rcx at entry. It survives as rcx, or is saved into another register and restored -
    `mov rdi, rcx` then `mov rcx, rdi` is the common shape - so both are accepted. A `lea rcx,
    [reg+disp]` retargets the destination and is NOT this object's own clear, which is what keeps
    `BattleUnit`'s `memset(unit + 0x80, ...)` out of the whole-object column.
    """
    sz = sizes.get(ctor, 0)
    if not sz:
        return None
    _s, b = img.at(ctor, sz)
    if not b:
        return None
    holds = {X86_REG_RCX}          # registers currently holding `this`
    length = None
    for i in md.disasm(b, ctor):
        m, o = i.mnemonic, i.op_str
        if m == "call" and o.startswith("0x") and int(o, 16) == MEMSET:
            if X86_REG_RCX in holds and length is not None:
                return i.address, length
            length = None
            continue
        if m == "mov" and "," in o:
            dst, src = [x.strip() for x in o.split(",", 1)]
            if dst in ("r8d", "r8") and src.startswith("0x"):
                try:
                    length = int(src, 16)
                except ValueError:
                    length = None
                continue
            if src == "rcx" and dst.startswith("r") and " " not in dst:
                holds.add(dst)
                continue
            if dst == "rcx":
                holds = {dst} if src in holds else set()
                continue
        if m == "lea" and o.startswith("rcx"):
            holds.discard(X86_REG_RCX)
    return None



def dest_of(img, md, sizes, fn, site):
    """How the destination register was set at a memset site - the second discriminator.

    A `lea rcx, [rsp+N]` or `[rbp-N]` is a LOCAL BUFFER that happens to match a type's size, and it
    is the single commonest way a size match misleads: every small-size candidate in this corpus
    resolves to one.
    """
    sz = sizes.get(fn, 0)
    if not sz:
        return "?"
    _s, b = img.at(fn, sz)
    if not b:
        return "?"
    last = None
    for i in md.disasm(b, fn):
        if i.address == site:
            break
        if i.mnemonic in ("mov", "lea") and i.op_str.startswith("rcx"):
            last = (i.mnemonic, i.op_str)
    if last is None:
        return "rcx = incoming this"
    m, o = last
    rhs = o.split(",", 1)[1].strip()
    if "rsp" in rhs or "rbp" in rhs:
        return "stack " + rhs
    if "rip" in rhs:
        return ("static " if m == "lea" else "global ptr ") + "[rip]"
    return m + " " + rhs


def runtime_this_memset(img, md, sizes, fn):
    """A `memset(this, 0, <register>)` - a whole-object clear whose LENGTH is computed at runtime.

    THE BLIND SPOT THAT COST A PUBLISHED CLAIM. Restricting to literal lengths made
    `MessageWindowRecord +0x1B0` (520 B) look uninitialised and put it in the "genuinely undefined"
    column. It is not: every widget is allocated by `00244F50` and constructed by `002465F0`, which
    does `movsxd r8, edx` on the size ARGUMENT, `xor edx, edx`, and `call memset` - so the whole
    record is zeroed with a length the caller supplies. A literal-only sweep cannot see that, and the
    idiom is normal for any allocator that takes a size.

    The size is not resolvable here, so this reports a SHAPE and the caller has to supply the number.
    """
    sz = sizes.get(fn, 0)
    if not sz:
        return None
    _s, b = img.at(fn, sz)
    if not b:
        return None
    holds = {"rcx"}
    size_reg = None
    for i in md.disasm(b, fn):
        m, o = i.mnemonic, i.op_str
        if m == "call" and o.startswith("0x") and int(o, 16) == MEMSET:
            if "rcx" in holds and size_reg:
                return i.address, size_reg
            size_reg = None
            continue
        if m in ("mov", "movsxd") and "," in o:
            dst, src = [x.strip() for x in o.split(",", 1)]
            if dst in ("r8", "r8d") and not src.startswith("0x"):
                size_reg = src
            elif src == "rcx" and dst.startswith("r"):
                holds.add(dst)
            elif dst == "rcx":
                holds = {dst} if src in holds else set()
        elif m == "lea" and o.startswith("rcx"):
            holds.discard("rcx")
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=CLC.EXE)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = CLC.Image(a.exe)
    sizes, names = MRS.load_funcs()
    md = Cs(CS_ARCH_X86, CS_MODE_64)

    if a.self_test:
        # The case this was written from: the singleton's ctor clears its whole 0x10FD0.
        got = find_this_memset(img, md, sizes, 0x00291750)
        ok = bool(got) and got[1] == 0x10FD0
        print("  %-52s %s" % ("00291750 clears 0x10FD0 (the whole singleton)",
                              "ok" if ok else "BROKEN got=%r" % (got,)))
        # A control in the other direction: a body with no memset at all must not report one.
        none = find_this_memset(img, md, sizes, 0x00273A20)
        ok2 = none is None
        print("  %-52s %s" % ("00273A20 (a 9-byte null test) reports nothing",
                              "ok" if ok2 else "BROKEN got=%r" % (none,)))
        print("  %s" % ("all controls behave" if ok and ok2 else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if (ok and ok2) else 2

    rows = list(csv.reader(io.open(TYPES, encoding="utf-8", newline=""), delimiter="\t"))
    hdr = rows[0]
    ci, si = hdr.index("ctor"), hdr.index("size")
    gaps = {}
    for f in csv.reader(io.open(FIELDS, encoding="utf-8", newline=""), delimiter="\t"):
        if len(f) < 9 or not GAP.search(f[3]):
            continue
        try:
            gaps.setdefault(f[0], []).append((int(f[1], 0), int(f[2], 0), f[3]))
        except ValueError:
            pass

    found, checked = [], 0
    for r in rows[1:]:
        if len(r) <= ci:
            continue
        m = re.match(r"\s*([0-9A-Fa-f]{8})", r[ci] or "")
        if not m:
            continue
        checked += 1
        hit = find_this_memset(img, md, sizes, int(m.group(1), 16))
        if not hit:
            continue
        site, length = hit
        try:
            declared = int(r[si], 0)
        except ValueError:
            declared = None
        cov = [g for g in gaps.get(r[0], []) if g[0] + g[1] <= length]
        found.append((r[0], declared, length, site, m.group(1), cov))

    print("types with a recorded constructor : %d" % checked)
    print("whose constructor clears `this`   : %d" % len(found))
    print()
    print("%-34s %-10s %-10s %-9s %s" % ("type", "size", "cleared", "ctor", "gap bytes covered"))
    for ty, dec, ln, site, ctor, cov in sorted(found, key=lambda x: -x[2]):
        nb = sum(g[1] for g in cov)
        flag = "" if (dec is None or ln >= dec) else "  <- clears LESS than the type"
        print("%-34s %-10s 0x%-8X %-9s %d in %d span(s)%s"
              % (ty[:34], (hex(dec) if dec else "?"), ln, ctor, nb, len(cov), flag))
    print()
    # SECOND PASS: the clear is usually NOT in the recorded constructor. Requiring it there found 2
    # types; matching a declared size against any literal memset length in the image finds 25. The
    # match is a CANDIDATE and not a finding - a `memset(x, 0, 0x200)` proves nothing about a
    # 0x200-byte type until its destination is read - so these are printed separately and labelled.
    all_sites = collections.defaultdict(list)
    for fn in sorted(sizes):
        fs = sizes[fn]
        if fs <= 0 or fs > 20000:
            continue
        _s, bb = img.at(fn, fs)
        if not bb:
            continue
        ln = None
        for i in md.disasm(bb, fn):
            o = i.op_str
            if i.mnemonic == "mov" and (o.startswith("r8d,") or o.startswith("r8,")) and "0x" in o:
                try:
                    ln = int(o.split(",")[1].strip(), 16)
                except ValueError:
                    ln = None
            elif i.mnemonic == "call" and o.startswith("0x") and int(o, 16) == MEMSET:
                if ln:
                    all_sites[ln].append((fn, i.address))
                ln = None
    confirmed = {f[0] for f in found}
    cand = []
    for r in rows[1:]:
        try:
            s = int(r[si], 0)
        except (ValueError, IndexError):
            continue
        if s >= 0x40 and s in all_sites and r[0] not in confirmed:
            cand.append((r[0], s, all_sites[s]))
    cand.sort(key=lambda x: -x[1])
    print()
    print("=== CANDIDATES: a declared size equals a literal memset length somewhere in the image ===")
    print("    %d type(s). A SIZE MATCH IS NOT A FINDING - the destination must be read before the" % len(cand))
    print("    clear can be attributed to the type. Confirmed examples of what reading them yields:")
    print("    BattleUnit 0xF50 is cleared IN FULL twice - 002342CE in")
    print("    ActorSystem_ReleaseBattleUnitSlotForActor (on release, after a pool bounds check) and")
    print("    002344D2 in BattleUnit_AllocateSlotAndBindActor (on allocation, at the free slot).")
    print()
    print("    %-34s %-9s %-4s %-22s %s" % ("type", "size", "n", "destination", "first site"))
    for ty, s, ss in cand[:22]:
        d = dest_of(img, md, sizes, ss[0][0], ss[0][1])
        note = ""
        if len(ss) >= 8:
            note = "  <- %d sites: a common size, not a type" % len(ss)
        elif d.startswith("stack"):
            note = "  <- STACK buffer, not the object"
        print("    %-34s 0x%-7X %-4d %-22s %08X%s" % (ty[:34], s, len(ss), d[:22], ss[0][1], note))
    print()
    rt = []
    for r in rows[1:]:
        if len(r) <= ci:
            continue
        mm = re.match(r"\s*([0-9A-Fa-f]{8})", r[ci] or "")
        if not mm:
            continue
        hit = runtime_this_memset(img, md, sizes, int(mm.group(1), 16))
        if hit and r[0] not in {f[0] for f in found}:
            rt.append((r[0], r[si], mm.group(1), hit[0], hit[1]))
    print()
    print("=== RUNTIME-SIZE whole-object clears: memset(this, 0, <register>) ===")
    print("    The length is the caller's, so the literal passes above cannot see these. This is the")
    print("    shape that made MessageWindowRecord look uninitialised when its widget constructor")
    print("    002465F0 zeroes the whole record with the size it is handed.")
    print()
    print("    %-34s %-10s %-9s %-9s %s" % ("type", "size", "ctor", "site", "length from"))
    for ty, s, ctor, site, reg in rt[:20]:
        print("    %-34s %-10s %-9s %08X  %s" % (ty[:34], s, ctor, site, reg))
    if not rt:
        print("    none")
    print()
    print("A CLEAR IS A LIFETIME FACT, NOT A SEMANTIC ONE. These bytes start at zero; that is not")
    print("what they are for, and not proof the clear is their only writer. What it does mean is")
    print("that a reimplementation which skips the clear differs from the engine in bytes no test")
    print("will catch, because nothing reads them yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
