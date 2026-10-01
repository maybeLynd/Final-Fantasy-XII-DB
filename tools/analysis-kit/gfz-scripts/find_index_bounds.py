#!/usr/bin/env python3
"""For every INDEXED access the census records, what bounds the index?

WHY. An `ARRAY BASE, extent NOT established` row is the store's commonest open byte range, and
three of them were closed by hand on 2026-09-20 by exactly the same procedure: take the indexed
access, disassemble the function it sits in, and read the `cmp` that guards it. That procedure
does not need a person.

  * BootSingleton01F7F598 +0x0BE0 - `cmp edx, 0xa` / `jae` at 001867E0, so ten qwords.
  * ActorStorageRecord    +0x0C8  - `cmp r8d, 0x11` / `ja` at 002652D9, so eighteen words.
  * ManagerSub0209BE80_5380 +0x342 - a counter loop, `cmp eax, 6` / `jb`, so six slots.

WHAT IT REPORTS AND WHAT IT DOES NOT. A bound is the largest index the code will FORM, which is
an upper bound on the elements the code can reach. It is NOT the array's length: a table can be
shorter and the guard generous, or the guard can protect one caller's use of a longer table.
So the output is `the accessor admits N` and never `the array has N`. Closing the distance
needs a second reading - the out-of-range path, a count field, or a constructor - which is what
the BootSingleton case had when its fallback returned element 9.

HOW THE GUARD IS FOUND. Decode FORWARD from the function entry the census records, never
backwards from the site: x86 resynchronises, so a late start yields a fluent and fictional
instruction stream. Track the last `cmp <reg>, imm` seen before the access whose register is the
one the access indexes with, and require a conditional branch on it within a few instructions -
a `cmp` whose result is never branched on is not a guard.

CONTROLS, both required or the output is refused:
  * POSITIVE - ActorStorageRecord +0x0C8 must report a bound of 0x11 from 002652D9, admitting
    EIGHTEEN indices - the count, not just the immediate, because `ja` and `jae` on the same
    immediate mean different lengths.
  * NEGATIVE - a site with no `cmp` on its index register must report nothing rather than the
    nearest unrelated `cmp`; BootSingleton01F7F598 +0x0B90's sibling read at 00186810 is a bare
    `mov rax, [rcx + 0xbd8]` with no index at all and must not appear.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import census_artifacts as CA  # noqa: E402
import disasm_fn as DF  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

# `[base + idx*scale + disp]` or `[base + idx + disp]` - the index is the second register.
IDX = re.compile(r"\[\s*([a-z0-9]+)\s*\+\s*([a-z0-9]+)\s*(?:\*\s*([1248]))?\s*(?:\+|\])")
CMP = re.compile(r"^([a-z0-9]+),\s*(0x[0-9a-f]+|\d+)$")
# A BOUND IS A RANGE CHECK, so only ordering branches count. `cmp edi, 0xe` / `jne` at 002652EE
# is an equality test - it selects a case, it does not limit an index - and taking the nearest
# `cmp` regardless of its branch made this tool report 0xE where its control expected 0x11.
JCC = ("ja", "jae", "jb", "jbe", "jl", "jle", "jg", "jge")
CONTROL_POS = ("ActorStorageRecord", 0xC8, 0x11, 18)
CONTROL_NEG = ("BootSingleton01F7F598", 0xBD8)

R64 = ["rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi"] + ["r%d" % i for i in range(8, 16)]
ALIAS = {}
for _i, _r in enumerate(R64):
    ALIAS[_r] = _r
    if _i < 8:
        ALIAS["e" + _r[1:]] = _r
        ALIAS[_r[1:]] = _r
    else:
        for _s in ("d", "w", "b"):
            ALIAS[_r + _s] = _r


def root(r):
    return ALIAS.get(r.strip(), r.strip())


MOVREG = re.compile(r"^([a-z0-9]+),\s*([a-z0-9]+)$")
# `lea D, [A + A*k]` - the index-multiplying idiom x86 uses for a non-power-of-two stride.
LEAMUL = re.compile(r"^([a-z0-9]+),\s*\[\s*([a-z0-9]+)\s*\+\s*([a-z0-9]+)\s*\*\s*([248])\s*\]$")


def guard_for(img, md, fn_hex, site_hex, idx_reg, cache):
    """The last `cmp <r>, imm` before `site`, branched on, where `r` FEEDS the index.

    THE GUARD IS RARELY ON THE INDEX REGISTER ITSELF, which the first version of this assumed
    and which its own positive control refused. ActorStorageRecord +0x0C8 indexes with `rsi`
    and is guarded by `cmp r8d, 0x11`, because 002652D6 does `mov edi, r8d` and 00265308
    `movsxd rsi, edi`. So a simple copy chain is tracked forward - reg-to-reg `mov`, `movsxd`,
    `movzx` - and a `cmp` counts when its register is anywhere in the chain feeding the index at
    the site. Any other write to a register breaks its chain.
    """
    try:
        fn, site = int(fn_hex, 16), int(site_hex, 16)
    except (ValueError, TypeError):
        return None
    if not fn or site <= fn or site - fn > 0x4000:
        return None
    if (fn, site) not in cache:
        data = img.read(fn, site - fn + 16)
        cache[(fn, site)] = list(md.disasm(data, fn)) if data else []
    ins = cache[(fn, site)]

    src = {}          # reg root -> the reg root it was last copied from
    cmoved = set()    # regs a conditional move rewrote on the way to the site
    mul = {}          # reg -> the factor a `lea r,[a+a*k]` applied to it
    cmps = []         # (address, imm, reg root)
    for n, x in enumerate(ins):
        if x.address >= site:
            break
        if x.mnemonic == "cmp":
            m = CMP.match(x.op_str)
            if m:
                br = next((y for y in ins[n + 1:n + 4] if y.mnemonic in JCC), None)
                if br is not None:
                    cmps.append((x.address, int(m.group(2), 0), root(m.group(1)),
                                 br.mnemonic, br.op_str))
            continue
        if x.mnemonic == "lea":
            # A STRIDE THAT IS NOT A POWER OF TWO IS BUILT, NOT ENCODED. x86 has no scale of 3,
            # so `lea rdx, [rax + rax*2]` triples the index and the operand's scale 8 then means
            # an effective stride of 0x18. This binary does it constantly - ActorManagerSlotEntry
            # (i*3 then *8 = 0x18), ManagerSub0209BE80_57E0's widgets, VmResultEntry (i*5 then
            # *8 = 0x28) - so reporting the SIB scale alone mis-spans every one of them.
            lm = LEAMUL.match(x.op_str)
            if lm and root(lm.group(2)) == root(lm.group(3)):
                mul[root(lm.group(1))] = int(lm.group(4)) + 1
                src[root(lm.group(1))] = root(lm.group(2))
            else:
                d0 = x.op_str.split(",")[0].strip()
                if root(d0) in ALIAS.values():
                    src.pop(root(d0), None)
                    mul.pop(root(d0), None)
            continue
        # `lea` IS NOT THE ONLY WAY TO SCALE AN INDEX. `add rax, rax` doubles it and `shl` shifts
        # it, and both appear immediately before a scaled operand in this binary:
        # 00319309 `add rax, rax` then 0031930C `cmp qword ptr [rbx + rax*8 + 0x988], 0` is a
        # stride of 0x10, which is exactly the declared BattleTargetResultEntry[32]. Missing the
        # doubling reported half the array.
        if x.mnemonic in ("add", "shl"):
            pp = [q.strip() for q in x.op_str.split(",")]
            if len(pp) == 2 and root(pp[0]) in ALIAS.values():
                d0 = root(pp[0])
                if x.mnemonic == "add" and root(pp[1]) == d0:
                    mul[d0] = mul.get(d0, 1) * 2
                    continue
                if x.mnemonic == "shl":
                    try:
                        mul[d0] = mul.get(d0, 1) * (1 << int(pp[1], 0))
                        continue
                    except ValueError:
                        pass
                src.pop(d0, None)
                mul.pop(d0, None)
            continue
        parts = x.op_str.split(",")
        if len(parts) != 2 or "[" in x.op_str:
            # a memory operand or an odd shape: if it writes a register, break its chain
            d = parts[0].strip() if parts else ""
            if d and root(d) in ALIAS.values() and "[" not in d:
                src.pop(root(d), None)
                mul.pop(root(d), None)
            continue
        d, s = root(parts[0]), root(parts[1])
        if d not in ALIAS.values():
            continue
        if x.mnemonic.startswith("cmov"):
            # A CONDITIONAL MOVE DOES NOT BREAK THE CHAIN, and treating it as a plain write did.
            # ActorStorageRecord +0x0C8's index passes through `cmovb edi, eax` at 00265305,
            # which leaves edi as EITHER the guarded value or a substituted one - so the guard
            # still describes one of the two, and dropping the provenance loses it entirely.
            # The substitution is real though, so the row is marked `via cmov` rather than
            # reported as if the bound were unconditional.
            cmoved.add(d)
            continue
        if x.mnemonic in ("mov", "movsxd", "movzx", "movsx") and s in ALIAS.values():
            # A PLAIN COPY CARRIES THE CHAIN BUT NOT A STALE FACTOR. `mul` was keyed by register
            # and never invalidated, so an unrelated `lea X,[Y+Y*2]` earlier in a function stayed
            # attached and widened BattleStatsRecord +0x050 from 0xC to 0x24 - a fabricated span
            # on a row already routed to FABLE at the correct one.
            src[d] = s
            mul[d] = mul.get(s, 1)
        else:
            src.pop(d, None)
            mul.pop(d, None)

    chain, cur = set(), root(idx_reg)
    for _ in range(5):
        chain.add(cur)
        cur = src.get(cur)
        if not cur or cur in chain:
            break
    for addr, imm, reg, br, brop in reversed(cmps):
        if reg in chain:
            m = 1
            for c in chain:
                m = max(m, mul.get(c, 1))
            return (addr, imm, bool(chain & cmoved), br, brop, m)
    return None


def admits(bound, br, br_target, site):
    """How many indices the guard actually lets through.

    THE STRICTNESS OF THE BRANCH DECIDES IT, and computing `bound + 1` unconditionally was
    wrong - it is right for `ja` and wrong for `jae`. Which way round depends on whether the
    branch SKIPS the access or CONTINUES a loop containing it:

      * a FORWARD branch past the site is the exit, so the access runs on its negation -
        `ja` (>) leaves `<= bound`, which is bound + 1 values; `jae` (>=) leaves `< bound`,
        which is bound.
      * a BACKWARD branch is a loop edge, so the access runs while it is TAKEN -
        `jb` (<) gives bound values, `jbe` (<=) gives bound + 1.

    All three hand results reproduce under this rule: BootSingleton `jae` 0xa -> 10,
    ActorStorageRecord `ja` 0x11 -> 18, ManagerSub0209BE80_5380 `jb` 6 -> 6.
    """
    try:
        tgt = int(br_target, 16)
    except (ValueError, TypeError):
        return bound + 1, "?"
    forward = tgt > site
    strict_hi = br in ("ja", "jg")        # exit on strictly greater
    strict_lo = br in ("jb", "jl")        # loop while strictly less
    if forward:
        return (bound + 1 if strict_hi else bound), "exit"
    return (bound if strict_lo else bound + 1), "loop"


def main():
    by_type, unresolved = CA.load()
    img = DF.Image(DF.DEFAULT_EXE)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    cache = {}

    found = collections.defaultdict(dict)   # type -> disp -> (site, reg, scale, bound, at)
    indexed = 0
    for t, rows in by_type.items():
        for r in rows:
            instr = (r.get("instruction") or "").strip()
            m = IDX.search(instr)
            if not m:
                continue
            base, idx, scale = m.group(1), m.group(2), m.group(3)
            if root(idx) in ("rsp", "rbp") or root(idx) == root(base):
                continue
            # A DISPLACEMENTLESS `lea` CARRIES NO OFFSET, and attributing its bound to +0x0000
            # is a fabricated finding. 00252EB5 `lea rdi, [rax + rcx*4]` was reported as
            # ImageBackedStateBlock +0x0000 admitting twelve dwords, contradicting a head
            # declared as a dword, a word and two 16-byte vectors - but the read it feeds is
            # `mov edx, dword ptr [rdi + 0x47b8]` at 00252EC9, so the bound belongs to +0x47B8,
            # where the store already declares `slotDwordByIndex uint32[12]` and where this
            # tool reports it correctly from another site. The lea says the STRIDE and the
            # BOUND; it does not say the base.
            if instr.startswith("lea") and "+ 0x" not in instr[instr.find("["):]:
                continue
            indexed += 1
            try:
                d = int(r["disp"], 16)
            except (ValueError, TypeError, KeyError):
                continue
            g = guard_for(img, md, (r.get("function") or "").strip(),
                          (r.get("site") or "").strip(), idx, cache)
            if g and d not in found[t]:
                site_i = int((r.get("site") or "0").strip() or "0", 16)
                n, kind = admits(g[1], g[3], g[4], site_i)
                eff = int(scale or 1) * g[5]
                found[t][d] = (r.get("site", ""), idx, eff, g[1], g[0], g[2],
                               n, kind, g[3], g[5])

    pos = found.get(CONTROL_POS[0], {}).get(CONTROL_POS[1])
    ok_pos = bool(pos) and pos[3] == CONTROL_POS[2] and pos[6] == CONTROL_POS[3]
    ok_neg = CONTROL_NEG[1] not in found.get(CONTROL_NEG[0], {})
    print("CONTROL positive  %s +0x%03X -> bound %s (expect 0x%X / 18)   %s"
          % (CONTROL_POS[0], CONTROL_POS[1],
             ("0x%X admitting %d" % (pos[3], pos[6])) if pos else "none",
             CONTROL_POS[2], "PASS" if ok_pos else "FAIL"))
    print("CONTROL negative  %s +0x%03X -> %s   %s"
          % (CONTROL_NEG[0], CONTROL_NEG[1], "absent" if ok_neg else "REPORTED",
             "PASS" if ok_neg else "FAIL"))
    if not (ok_pos and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  both controls pass - the absences below are meaningful")
    print("  " + CA.coverage_line(by_type, unresolved))
    print("  indexed accesses examined: %d\n" % indexed)

    total = sum(len(v) for v in found.values())
    print("INDEXED ACCESSES WITH A GUARDING BOUND: %d across %d type(s)"
          % (total, len(found)))
    for t in sorted(found):
        print("\n  %s" % t)
        for d in sorted(found[t]):
            site, reg, scale, bound, at, viacmov, n, kind, br, mfac = found[t][d]
            print("      +0x%04X  site %s  index %-4s stride %-4d ->  cmp 0x%X / %s (%s) at %08X%s"
                  % (d, site, reg, scale, bound, br, kind, at,
                     ("   [index x%d, built with lea/add/shl]" % mfac if mfac > 1 else "")
                     + ("   [via cmov]" if viacmov else "")))
            print("               the accessor admits %d element(s); at scale %d that is "
                  "0x%X bytes from +0x%04X" % (n, scale, n * scale, d))
    print("\nA BOUND IS NOT A LENGTH. This is the largest index the code will form - an upper")
    print("bound on what it can reach, not the array's size. Closing the distance needs a")
    print("second reading: the out-of-range path, a count field, or a constructor.")


if __name__ == "__main__":
    sys.exit(main() or 0)
