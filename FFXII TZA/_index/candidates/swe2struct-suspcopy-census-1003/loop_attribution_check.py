"""fix_census.py - OPUS-REQ-STRUCT-SUSPEND-COPY-CENSUS-ROWS-1001 (SWE2-STRUCT, 2026-10-03).

The restore 0030EDA0 and the snapshot 0030EFF0 copy [unit+0x6B0, unit+0xBA0) with a 9-pass loop of eight
16-byte moves (stride 0x80, `mov edx, 9` / `sub rdx,1; jne`), then a 7-move tail. The census follows only the
first pass, so the loop body is filed at +0x6B0..+0x720 (true for pass 0 only) and the tail, which runs with the
pointer at +0x6B0 + 9*0x80 = +0xB30, is filed at +0x730..+0x790 (the first `lea`'s value) instead of
+0xB30..+0xB90.

This script, every change decoded from the shipping image before it is written:
  * re-attributes the 14 tail rows (0030EE13..0030EE44 writes, 0030F0A9..0030F0DD reads) by +0x400;
  * annotates the loop-body rows and the two loop-carried `lea` rows as pass 0 of 9, loop unfollowed;
  * drops the 4 rows the BattleTargetBuffer projection (embed BattleUnit+0x778) inherited from tail sites -
    their true unit offsets +0xB80/+0xB90 lie past the buffer's end (+0x778 + 0x208 = +0x980).
Refuses (FAILS n) if any instruction no longer decodes as recorded. --apply writes; default is a dry run.
As the REGRESSION (run with --check): every row already carries the fix, so any row it would still change or drop
is a FAIL - a regenerated census that brings back the +0x730 tail attribution is rejected.
"""
import os
import sys

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

DB = os.path.join(ROOT, "Database", "FFXII TZA")
BU = os.path.join(DB, "04-Actor-Entity", "Battle-Unit", "battle-unit-accesses.tsv")
TB = os.path.join(DB, "04-Actor-Entity", "Battle-Unit", "battle-target-buffer-accesses.tsv")
TAG = "OPUS-REQ-STRUCT-SUSPEND-COPY-CENSUS-ROWS-1001"

# (function, loop lea, counter mov, loop jne, tail sites)
LOOPS = {
    0x0030EDA0: dict(base=0x0030EDA7, count=0x0030EDB1, jne=0x0030EE07, lead=0x0030EDB6,
                     body=range(0x0030EDC7, 0x0030EE03), tail=[0x0030EE13, 0x0030EE1A, 0x0030EE22, 0x0030EE2A,
                                                            0x0030EE32, 0x0030EE3A, 0x0030EE44]),
    0x0030EFF0: dict(base=0x0030F04A, count=0x0030F051, jne=0x0030F0A7, lead=0x0030F060,
                     body=range(0x0030F05D, 0x0030F0A3), tail=[0x0030F0A9, 0x0030F0B5, 0x0030F0BD, 0x0030F0C5,
                                                            0x0030F0CD, 0x0030F0D5, 0x0030F0DD]),
}

md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = []
IMG, OFF = fp.load_image()


def ins(va):
    return next(md.disasm(IMG[OFF(va):OFF(va) + 16], va), None)


def check(va, mnem, op):
    i = ins(va)
    got = (i.mnemonic, i.op_str) if i else None
    ok = i is not None and i.mnemonic == mnem and (op is None or i.op_str == op)
    print("%s %08X %-7s %s" % ("ok  " if ok else "FAIL", va, got[0] if got else "?", got[1] if got else ""))
    if not ok:
        fails.append(va)


# the loop shape, both functions
check(0x0030EDA7, "add", "rcx, 0x6b0")
check(0x0030EDB1, "mov", "edx, 9")
check(0x0030EDB6, "lea", "rcx, [rcx + 0x80]")
check(0x0030EDC0, "lea", "rax, [rax + 0x80]")
check(0x0030EE03, "sub", "rdx, 1")
check(0x0030EE07, "jne", "0x30edb6")
check(0x0030F04A, "lea", "rax, [rbx + 0x6b0]")
check(0x0030F051, "mov", "edx, 9")
check(0x0030F056, "lea", "rcx, [rcx + 0x80]")
check(0x0030F060, "lea", "rax, [rax + 0x80]")
check(0x0030F0A3, "sub", "rdx, 1")
check(0x0030F0A7, "jne", "0x30f056")
# every tail site addresses the post-loop pointer (+0xB30) at [reg + k*0x10]
for fn, L in LOOPS.items():
    reg = "rcx" if fn == 0x0030EDA0 else "rax"
    for k, va in enumerate(L["tail"]):
        i = ins(va)
        mem = "xmmword ptr [%s]" % reg if k == 0 else "xmmword ptr [%s + 0x%x]" % (reg, k * 0x10)
        ok = i is not None and i.mnemonic == "movups" and mem in i.op_str
        print("%s %08X tail k=%d  %s %s" % ("ok  " if ok else "FAIL", va, k, i.mnemonic if i else "?",
                                           i.op_str if i else ""))
        if not ok:
            fails.append(va)

TAIL = {va: (fn, k) for fn, L in LOOPS.items() for k, va in enumerate(L["tail"])}
NOTE_TAIL = ("loop-tail re-attributed 2026-10-03 (SWE2-STRUCT, %s): this move runs after the 9-pass x 0x80 "
             "copy loop, with the pointer at +0x6B0+9*0x80 = +0xB30; the census had filed it at the first lea's "
             "+0x730 (+0x%X before)")
NOTE_BODY = ("loop pass 0 of 9 (SWE2-STRUCT 2026-10-03, %s): the copy loop advances the pointer 0x80 per pass "
             "(lea at %08X, edx=9), so this site also reaches +0x%X..+0x%X in passes 1-8; the census follows "
             "pass 0 only (loop unfollowed)")


def rewrite(path, fn_rows):
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").splitlines()
    out, changed, dropped = [], 0, 0
    for ln in lines:
        c = ln.split("\t")
        if len(c) >= 8 and c[0] != "function":
            r = fn_rows(c)
            if r is None:
                dropped += 1
                print("  drop  " + ln[:150])
                continue
            if r != c:
                changed += 1
                print("  -     " + "\t".join(c)[:170])
                print("  +     " + "\t".join(r)[:300])
            c = r
        out.append("\t".join(c))
    return out, changed, dropped, crlf


def bu_row(c):
    site = int(c[2], 16)
    fn = int(c[0], 16)
    if site in TAIL:
        if "loop-tail re-attributed" in c[7]:
            return c
        old = int(c[3], 16)
        k = TAIL[site][1]
        if old != 0x730 + k * 0x10:
            fails.append(site)
            print("FAIL unexpected disp %s at %08X" % (c[3], site))
            return c
        c = list(c)
        c[3] = "0x%X" % (old + 0x400)
        c[7] = ((c[7] + " || ") if c[7] else "") + NOTE_TAIL % (TAG, old)
        return c
    if fn in LOOPS:
        L = LOOPS[fn]
        if site in L["body"] or site == L["lead"]:
            if "loop pass 0 of 9" in c[7]:
                return c
            d = int(c[3], 16)
            c = list(c)
            c[7] = ((c[7] + " || ") if c[7] else "") + NOTE_BODY % (TAG, L["lead"], d + 0x80, d + 8 * 0x80)
            return c
    return c


def tb_row(c):
    site = int(c[2], 16)
    if site in TAIL and "BattleUnit+0x778" in c[6]:
        return None
    return c


apply = "--apply" in sys.argv
for path, f in ((BU, bu_row), (TB, tb_row)):
    print("==", os.path.relpath(path, DB))
    out, ch, dr, crlf = rewrite(path, f)
    print("   changed %d, dropped %d" % (ch, dr))
    if "--check" in sys.argv and (ch or dr):
        fails.append(path)
    if apply and not fails and (ch or dr):
        nl = "\r\n" if crlf else "\n"
        open(path, "wb").write((nl.join(out) + nl).encode("utf-8"))
        print("   written")
print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
