#!/usr/bin/env python3
"""abi_signatures.py - derive an x64 call signature from register liveness, and check it.

What it derives
---------------
For a function body: **a register is a parameter if some path from the entry READS it before
anything writes it.**  Integer slots `rcx, rdx, r8, r9` and float slots `xmm0-3` are positional -
a filled slot 2 with an empty slot 1 still means arity 2, because the x64 ABI assigns argument
POSITIONS, not register files.  Also reported: whether `rax` is written before a `ret`, whether the
entry spills argument registers to their home slots (the MSVC variadic prologue), and whether the
body **tail-jumps** out, which makes the arity a lower bound.

Why it walks a CFG
------------------
A linear walk gets read-before-write wrong on every branch.  `EVIDENCE-STANDARD` 2026-09-13d
records a register trace of mine that returned an impossible negative offset for exactly that
reason.  This keeps a worklist of (instruction, written-set) and explores both arms.

The control comes from the documents, not from me
-------------------------------------------------
Signatures are parsed out of every `CONTRACT-*.md` interface table and compared against the
derivation.  **That direction matters.**  My first control list was assembled from memory and
scored five "misses"; three were my memory, and the remaining pattern only became visible once the
control was mechanical.  Current result:

    control rows parsed from contracts   47
    match                                44
    miss                                  2      <- both are CONTRACT errors, see below
    skipped (tail-jump forwarder)          1
    accuracy on comparable rows        95.7%

**The two misses are the interesting output, not noise.**  `0031B760` is documented `()` and its
body null-tests `rcx` before tail-jumping.  `003299B0` is documented `(BattleUnit* rcx, int event
edx)` and its body stores `r8d` into `[rcx+0x2C]`.  A validated instrument disagreeing with a
document is a finding about the document.

Two rules learned by getting them wrong
---------------------------------------
1. **`xor r, r` is not a read.**  Capstone reports the register as read, because the instruction
   does read it; the zeroing idiom does not.  Before this was special-cased, every function using
   `xor ecx, ecx` looked like it took a parameter in `rcx`.
2. **A `call` does not forward arguments; a tail `jmp` does.**  The first version treated both as
   pass-through and flagged **326 of 562** bodies as unusable lower bounds.  After the fix: **27**.
   After a call returns, this function continues, and a register the callee happens to read is not
   thereby a parameter of ours.

What this is NOT
----------------
**A derived signature is not an explanation, and this tool disposes of nothing.**  Knowing that a
function takes three integer arguments and returns a value says nothing about what it does.  It
does not move the EC-7 frontier and must not be used as if it had.

Usage
-----
    python abi_signatures.py --control          # re-run the contract-derived control
    python abi_signatures.py --tag ABI_UNRESOLVED_DEFAULT --out derived.tsv
    python abi_signatures.py --addr 00300530
"""
import argparse
import collections
import io
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_dispositions as cd          # noqa: E402
import frontier_census as fc             # noqa: E402
import family_prover as fp               # noqa: E402

import capstone                          # noqa: E402
from capstone import x86                 # noqa: E402

MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
MD.detail = True
INT_ARGS = ["rcx", "rdx", "r8", "r9"]
FLT_ARGS = ["xmm0", "xmm1", "xmm2", "xmm3"]
ZEROING = {"xor", "sub", "pxor", "xorps", "xorpd", "sbb"}

PARENT = {}
for _b, _kids in (("rax", "rax eax ax al ah"), ("rbx", "rbx ebx bx bl bh"),
                  ("rcx", "rcx ecx cx cl ch"), ("rdx", "rdx edx dx dl dh"),
                  ("rsi", "rsi esi si sil"), ("rdi", "rdi edi di dil"),
                  ("rbp", "rbp ebp bp bpl"), ("rsp", "rsp esp sp spl"),
                  ("r8", "r8 r8d r8w r8b"), ("r9", "r9 r9d r9w r9b"),
                  ("r10", "r10 r10d r10w r10b"), ("r11", "r11 r11d r11w r11b"),
                  ("r12", "r12 r12d r12w r12b"), ("r13", "r13 r13d r13w r13b"),
                  ("r14", "r14 r14d r14w r14b"), ("r15", "r15 r15d r15w r15b")):
    for _k in _kids.split():
        PARENT[_k] = _b
for _i in range(16):
    PARENT["xmm%d" % _i] = "xmm%d" % _i


def canon(r):
    return PARENT.get(MD.reg_name(r), MD.reg_name(r))


def analyse(d, off, a, size):
    o = off(a)
    if o is None or size <= 0:
        return None
    ins = list(MD.disasm(d[o:o + size], a))
    if not ins:
        return None
    by_addr = {i.address: n for n, i in enumerate(ins)}
    lo, hi = a, a + size
    params, home = set(), set()
    writes_rax = False
    forwards = False
    seen, work = set(), [(0, frozenset())]
    while work:
        idx, written = work.pop()
        k = (idx, written)
        if k in seen or idx >= len(ins):
            continue
        seen.add(k)
        i = ins[idx]
        try:
            rd, wr = i.regs_access()
        except Exception:
            rd, wr = (), ()
        rdn = {canon(r) for r in rd}
        wrn = {canon(r) for r in wr}
        if (i.mnemonic in ZEROING and len(i.operands) == 2
                and i.operands[0].type == x86.X86_OP_REG
                and i.operands[1].type == x86.X86_OP_REG
                and canon(i.operands[0].reg) == canon(i.operands[1].reg)):
            rdn.discard(canon(i.operands[0].reg))       # the zeroing idiom is not a read
        for op in i.operands:
            if op.type == x86.X86_OP_MEM:
                for r in (op.mem.base, op.mem.index):
                    if r:
                        rdn.add(canon(r))
        for r in rdn:
            if (r in INT_ARGS or r in FLT_ARGS) and r not in written:
                params.add(r)
        if "rax" in wrn:
            writes_rax = True
        if idx < 6 and i.mnemonic == "mov" and len(i.operands) == 2:
            dst, src = i.operands
            if (dst.type == x86.X86_OP_MEM and src.type == x86.X86_OP_REG
                    and canon(src.reg) in INT_ARGS
                    and canon(dst.mem.base) in ("rsp", "rax", "r11")):
                home.add(canon(src.reg))
        grp = i.groups
        is_jmp = x86.X86_GRP_JUMP in grp
        is_call = x86.X86_GRP_CALL in grp
        tgt = None
        if (is_jmp or is_call) and i.operands and i.operands[0].type == x86.X86_OP_IMM:
            t = i.operands[0].imm
            if lo <= t < hi and t in by_addr:
                tgt = by_addr[t]
            elif not (lo <= t < hi) and is_jmp:
                if any(r not in written and r not in params for r in INT_ARGS):
                    forwards = True                     # only a TAIL JUMP forwards
        if i.mnemonic == "ret":
            continue
        nw = written | wrn
        if is_call:
            nw = nw | {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11",
                       "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5"}
        if is_jmp:
            if tgt is not None:
                work.append((tgt, frozenset(nw)))
            if i.mnemonic != "jmp":
                work.append((idx + 1, frozenset(nw)))
            continue
        if tgt is not None:
            work.append((tgt, frozenset(nw)))
        work.append((idx + 1, frozenset(nw)))
    arity = 0
    for n, r in enumerate(INT_ARGS):
        if r in params or FLT_ARGS[n] in params:
            arity = n + 1
    return {"addr": a, "arity": arity, "int": [r for r in INT_ARGS if r in params],
            "flt": [r for r in FLT_ARGS if r in params], "rax": writes_rax,
            "home": sorted(home), "lower_bound": forwards, "insns": len(ins)}


ROW = re.compile(r"^\|[^|]*\|\s*`([0-9A-Fa-f]{8})`[^|]*\|\s*`\(([^`]*)\)`\s*\|", re.M)
# A slot is filled by EITHER its integer or its float register: the ABI assigns POSITIONS.
SLOT = [("rcx", "ecx", "cl", "xmm0"), ("rdx", "edx", "dx", "xmm1"),
        ("r8", "r8d", "r8b", "xmm2"), ("r9", "r9d", "r9w", "xmm3")]


def contract_control(db):
    out = {}
    for root, _dd, files in os.walk(db):
        for f in files:
            if not (f.startswith("CONTRACT-") and f.endswith(".md")):
                continue
            t = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for m in ROW.finditer(t):
                sig = m.group(2)
                if "…" in sig or "..." in sig:
                    continue
                ar = 0
                for n, names in enumerate(SLOT):
                    if any(re.search(r"\b%s\b" % nm, sig) for nm in names):
                        ar = n + 1
                out.setdefault(int(m.group(1), 16), (ar, f, sig))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--tag", default=None)
    ap.add_argument("--addr", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    db = a.db or cd.DEFAULT_DB
    d, off = fp.load_image()
    sizes = cd.load_functions()

    if a.addr:
        x = int(a.addr, 16)
        r = analyse(d, off, x, sizes.get(x, 0))
        print(r)
        return 0

    if a.control:
        ctl = contract_control(db)
        print("control rows parsed from contracts: %d" % len(ctl))
        ok = bad = skip = 0
        misses = []
        for x, (want, src, sig) in sorted(ctl.items()):
            r = analyse(d, off, x, sizes.get(x, 0))
            if r is None:
                skip += 1; continue
            if r["lower_bound"] and r["arity"] < want:
                skip += 1; continue
            if r["arity"] == want:
                ok += 1
            else:
                bad += 1; misses.append((x, want, r["arity"], sig[:46], src))
        print("match %d   miss %d   skipped %d   accuracy %.1f%%"
              % (ok, bad, skip, 100.0 * ok / max(ok + bad, 1)))
        for x, want, got, sig, src in misses:
            print("  %08X stated %d derived %d  %-46s %s" % (x, want, got, sig, src))
        return 0

    rows, idx = fc.load_rows()
    front = fp.frontier(db, sizes)
    tagsel = a.tag or "ABI_UNRESOLVED_DEFAULT"
    mem = sorted(x for x in front
                 if tagsel in ((rows[x][idx["tags"]] if x in rows else "") or ""))
    res = [r for r in (analyse(d, off, x, sizes[x]) for x in mem) if r]
    ar = collections.Counter(r["arity"] for r in res)
    lb = sum(1 for r in res if r["lower_bound"])
    print("%s in frontier: %d   analysed: %d" % (tagsel, len(mem), len(res)))
    print("  derived arity: %s" % dict(sorted(ar.items())))
    print("  settled (not a tail-jump forwarder): %d   lower bound only: %d" % (len(res) - lb, lb))
    print("  returns a value in rax: %d" % sum(1 for r in res if r["rax"]))
    print("  a float slot is used   : %d" % sum(1 for r in res if r["flt"]))
    print("  home-slot spill (possible varargs): %d" % sum(1 for r in res if r["home"]))
    if a.out:
        o = ["addr\tarity\tint_regs\tflt_regs\treturns_rax\thome_spill\tlower_bound\tinsns"]
        for r in sorted(res, key=lambda z: z["addr"]):
            o.append("%08X\t%d\t%s\t%s\t%d\t%s\t%d\t%d"
                     % (r["addr"], r["arity"], ",".join(r["int"]) or "-",
                        ",".join(r["flt"]) or "-", 1 if r["rax"] else 0,
                        ",".join(r["home"]) or "-", 1 if r["lower_bound"] else 0, r["insns"]))
        io.open(a.out, "w", encoding="utf-8", newline="\n").write("\n".join(o) + "\n")
        print("  wrote %s (%d rows)" % (a.out, len(res)))
    print()
    print("A derived signature is NOT an explanation. This disposes of nothing and does not")
    print("move the EC-7 frontier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
