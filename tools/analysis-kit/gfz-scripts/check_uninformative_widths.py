#!/usr/bin/env python3
"""Does the value a candidate store writes carry ANY width information?

WHY A ROW CAN AGREE WITH ITS CENSUS AND STILL BE WRONG. check_census_widths.py fires when an
access is WIDER than the declared field. The same artifact acts in the other direction and
leaves nothing to disagree with: a field declared 4 or 8 because ONE wide store was seen, where
that store wrote a byte-repeating value. It was not hypothetical - RenderResourceEntryBank and
RenderStrideC0Bank both declared `dword020 uint32` on the strength of `mov dword ptr
[rcx+0x20], edi` with edi zero, and those four bytes are really two uint16s, `bankCursor` and
`banksLive`.

THE TEST IS THE VALUE, NOT THE INSTRUCTION, AND THE PROPERTY IS PERIODICITY. A store cannot
distinguish one width-byte field from k narrower ones when its value is the same in every one of
those k lanes. 0x00000000 and 0xFFFFFFFF are the obvious cases; 0x00800080 is the one that
caught the first version out, because its bytes are not all identical but its two 16-bit halves
are - Widget's constructor writes it at `+0x9C`, where Widget declares a PAIR of int16s. So one
instruction sets both, and the dword says nothing about the split. 0x3F800000 is not periodic
and can only be one field.

A zeroed register and an immediate 0 are the same case, and so is a register loaded with a
periodic immediate, which is why the classifier resolves a register back to its defining
instruction instead of stopping at "it is a register".

THE DEFINING INSTRUCTION IS FOUND BY DECODING FORWARD from the function entry the census
records, never backwards from the store. Backwards disassembly on x86 guesses at instruction
boundaries; forward from a known entry is aligned by construction.

WHAT A HIT MEANS, and the bound is the point: the declared width rests on NO information. That
is not the same as being wrong, and this tool never says it is. Of the first fourteen found, two
were proved wrong by another instance of the same shape, two were proved RIGHT by that same
instance, and the rest were simply unevidenced.

CONTROLS, both required or the output is refused:
  * POSITIVE - RenderResourceEntryBank +0x018 stores 0xFFFFFFFFFFFFFFFF and must read `all-ones`. (Re-pointed
    2026-09-27, OPUS: the same descriptor field used to be declared on RenderStrideC0Bank, whose copy of the shared bank
    descriptor was folded into RenderResourceEntryBank in ef399fee2 - see _index/candidates/bank-descriptor-merge/.)
  * NEGATIVE - CharacterRenderRecord +0x0618 (liveSpeedScale) stores 0x3F800000, whose byte lanes
    differ, and must read `informative`. (Re-pointed 2026-09-27, OPUS: the original target,
    BattleMenuPanelWidget3010 +0x0078, was folded into that type's 192-byte widgetBase0000, so the
    row no longer exists, the control could not land, and the checker refused all output.)
"""
import collections
import csv
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import disasm_fn as DF  # noqa: E402
import census_artifacts as CA  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

D = os.path.join(KP.DB, "_types") + os.sep
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
STORE = re.compile(r"^mov\s+(byte|word|dword|qword)\s+ptr\s+\[[^\]]+\],\s*([a-z0-9]+)$")
ANY = re.compile(r"\b(byte|word|dword|qword)\s+ptr\b")
CONTROL_POS = ("RenderResourceEntryBank", 0x18, "all-ones")
CONTROL_NEG = ("CharacterRenderRecord", 0x618, "informative")

R64 = ["rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi"] + ["r%d" % i for i in range(8, 16)]
ALIAS = {}
for _i, _r in enumerate(R64):
    ALIAS[_r] = _r
    if _i < 8:
        ALIAS["e" + _r[1:]] = _r
        ALIAS[_r[1:]] = _r
        ALIAS[(_r[1] + "l") if _r[1] in "abcd" else (_r[1:] + "l")] = _r
    else:
        for _s in ("d", "w", "b"):
            ALIAS[_r + _s] = _r


def root(reg):
    return ALIAS.get(reg.strip(), reg.strip())


def periodicity(v, width):
    """A label if the width-byte encoding of v REPEATS, otherwise None.

    THE RULE IS PERIODICITY, NOT `IS IT ZERO`, and the first version of this file got that
    wrong. A store cannot distinguish one width-byte field from k narrower ones when its value
    is the same in every one of those k lanes - and that is true of far more than zero.

    `mov dword ptr [rdi + 0x9c], 0x800080` is the case that exposed it: Widget's constructor
    writing 0x00800080, whose two 16-bit halves are BOTH 0x0080. Widget declares +0x9C and +0x9E
    as two separate int16s, so that one instruction is setting a pair - and the old test called
    it `informative` because its bytes are not all identical.

    Periods are reported smallest first, because a smaller period is the stronger statement: an
    all-zero dword is uninformative about splitting into halves AND into bytes.
    """
    try:
        b = (v & ((1 << (width * 8)) - 1)).to_bytes(width, "little")
    except (OverflowError, ValueError):
        return None
    for p in (1, 2, 4):
        if p < width and b == b[:p] * (width // p):
            if p == 1 and b[0] == 0:
                return "zero"
            if p == 1 and b[0] == 0xFF:
                return "all-ones"
            return "repeats/%d" % p
    return None


def uninformative_immediate(tok, width=4):
    """None if not an immediate; a label if its lanes repeat; False if they differ."""
    try:
        v = int(tok, 0)
    except ValueError:
        return None
    return periodicity(v, width) or False


def load():
    size = {}
    for r in csv.DictReader(io.open(D + "fields.tsv", encoding="utf-8"), delimiter="\t"):
        try:
            size[(r["type"], int(r["offset"], 16))] = (int(r["size"]), r["name"])
        except ValueError:
            pass

    by_type, unresolved = CA.load()
    acc = collections.defaultdict(list)
    for t, rows in by_type.items():
        for r in rows:
            try:
                acc[(t, int(r["disp"], 16))].append(r)
            except (ValueError, TypeError, KeyError):
                continue
    return size, acc, (by_type, unresolved)


def candidates(size, acc):
    """Fields declared 4 or 8 whose ONLY evidence is a store of exactly that width."""
    out = []
    for key, rows in acc.items():
        got = size.get(key)
        if not got or got[0] not in (4, 8):
            continue
        decl, name = got
        widths, stores, other = set(), [], 0
        for r in rows:
            instr = (r.get("instruction") or "").strip()
            m = ANY.search(instr)
            if not m:
                continue
            widths.add(W[m.group(1)])
            s = STORE.match(instr)
            if s and W[s.group(1)] == decl:
                stores.append((r.get("site", "").strip(), s.group(2), instr,
                               (r.get("function") or "").strip()))
            else:
                other += 1
        if stores and other == 0 and widths == {decl}:
            out.append((key[0], key[1], decl, name, stores))
    return sorted(out)


def classify(cand):
    """verdict -> [(type, offset, declared, name, per-site verdicts)].

    Exposed rather than computed inside main() so other sweeps can consume the classification.
    The composition that matters: a row whose width rests on nothing can sometimes be SETTLED by
    another instance of the same shape, which is how RenderResourceEntryBank +0x020 was resolved,
    and a caller can only try that if it can see which rows are uninformative.
    """
    img = DF.Image(DF.DEFAULT_EXE)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    cache = {}

    def define_of(fn_hex, site_hex, reg):
        try:
            fn, site = int(fn_hex, 16), int(site_hex, 16)
        except ValueError:
            return None
        if not fn or site < fn or site - fn > 0x4000:
            return None
        if (fn, site) not in cache:
            data = img.read(fn, site - fn + 16)
            cache[(fn, site)] = list(md.disasm(data, fn)) if data else []
        last, want = None, root(reg)
        for ins in cache[(fn, site)]:
            if ins.address >= site:
                break
            dst = (ins.op_str.split(",") + [""])[0]
            if "[" not in dst and root(dst) == want:
                last = ins
        return last

    buckets = collections.defaultdict(list)
    for t, d, decl, name, stores in cand:
        verdicts = []
        for site, src, _instr, fn in stores:
            imm = uninformative_immediate(src, decl)
            if imm:
                verdicts.append((imm, site, "immediate " + src))
                continue
            if imm is False:
                verdicts.append(("informative", site, "immediate " + src))
                continue
            ins = define_of(fn, site, src)
            if ins is None:
                verdicts.append(("undetermined", site, "no decode from %s" % fn))
                continue
            txt = "%s %s" % (ins.mnemonic, ins.op_str)
            a, b = (ins.op_str.split(",") + [""])[:2]
            if ins.mnemonic == "xor" and root(a) == root(b):
                verdicts.append(("zero", site, txt))
            elif ins.mnemonic == "or" and b.strip() in ("-1", "0xffffffff",
                                                        "0xffffffffffffffff"):
                verdicts.append(("all-ones", site, txt))
            else:
                # a register LOADED WITH a repeating immediate is the same case as storing one
                lab = (uninformative_immediate(b.strip(), decl)
                       if ins.mnemonic == "mov" else None)
                verdicts.append(((lab or "informative"), site, txt))
        worst = ("informative" if any(v[0] == "informative" for v in verdicts)
                 else "undetermined" if any(v[0] == "undetermined" for v in verdicts)
                 else sorted(v[0] for v in verdicts)[0])
        buckets[worst].append((t, d, decl, name, verdicts))
    return buckets


def main():
    size, acc, cov = load()
    cand = candidates(size, acc)
    buckets = classify(cand)

    def landed(ctrl):
        t, d, want = ctrl
        return any(r[0] == t and r[1] == d for r in buckets.get(want, []))

    ok_pos, ok_neg = landed(CONTROL_POS), landed(CONTROL_NEG)
    print("CONTROL positive  %s +0x%03X -> %s   %s"
          % (CONTROL_POS[0], CONTROL_POS[1], CONTROL_POS[2], "PASS" if ok_pos else "FAIL"))
    print("CONTROL negative  %s +0x%03X -> %s   %s"
          % (CONTROL_NEG[0], CONTROL_NEG[1], CONTROL_NEG[2], "PASS" if ok_neg else "FAIL"))
    if not (ok_pos and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  both controls pass - the absences below are meaningful\n")

    print("CANDIDATES - declared 4 or 8, only evidence a same-width store: %d\n" % len(cand))
    order = ["zero", "all-ones"] + sorted(k for k in buckets
                                          if k.startswith("repeats/")) +             ["undetermined", "informative"]
    for b in order:
        rows = buckets.get(b, [])
        print("== %s: %d" % (b.upper(), len(rows)))
        for t, d, decl, name, verdicts in rows:
            print("   %-34s +0x%04X %d %-22s" % (t, d, decl, name))
            for v, site, txt in verdicts:
                print("        %-12s %s  <- %s" % (v, site, txt))
        print("")
    n = sum(len(v) for k, v in buckets.items()
            if k in ("zero", "all-ones") or k.startswith("repeats/"))
    print("WIDTHS RESTING ON NO INFORMATION: %d. That is not a claim that any of them is wrong -"
          % n)
    print("only that nothing in the census supports the declared width.")


if __name__ == "__main__":
    sys.exit(main() or 0)
