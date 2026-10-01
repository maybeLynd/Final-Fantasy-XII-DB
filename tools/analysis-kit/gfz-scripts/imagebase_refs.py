# -*- coding: utf-8 -*-
"""Resolve globals reached through an IMAGE-BASE register, which the RIP-relative map cannot see.

MSVC compiles some functions to materialise the image base once --

    lea r15, [rip - 0x75e23]        ; -> 00120000
    ...
    mov [rsi + r15 + 0x1cd1738], xmm0   ; -> 01DF1738

-- and then address every global as `[base + disp]`. **A RIP-relative reference scan sees only the
one `lea`.** Every global the function actually touches is invisible to it, so "this global has no
writer" from that instrument is unsound for these functions.

This was not theoretical. `00195DF0` publishes the input binding profiles entirely through such a
register; the RIP map reported it as naming none of the addresses it in fact writes, which produced a
false contradiction against an already-correct document (`DD-3`).

**Measured population:** 641 of 38,161 functions (1.68 %) take the address of the image base.

The tracker is deliberately conservative:

  * a register is tracked only from a `lea reg, [rip+d]` whose target is exactly the image base;
  * tracking STOPS the moment anything writes to that register, and is not resumed by guesswork;
  * a `call` invalidates every volatile register, per the MS x64 ABI;
  * only `[base + disp]` and `[base + index + disp]` are resolved -- a scaled index is reported with
    its displacement as the base of an array, not as a single address.

So the output is a LOWER BOUND on what these functions touch. It never invents a reference.

    python imagebase_refs.py --fn 00195DF0          # one function, with the instructions
    python imagebase_refs.py --sweep                # every image-base function; totals
    python imagebase_refs.py --addr 01F80130        # who reaches this global through the base
    python imagebase_refs.py --self-test
"""
import argparse
import collections
import csv
import io
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import uc1_band
import importlib.util

_spec = importlib.util.spec_from_file_location("disasm_fn", os.path.join(_HERE, "disasm_fn.py"))
_D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_D)

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP

IMAGE_BASE = 0x00120000
FUNCS_TSV = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "work", "graph", "functions.tsv")

# MS x64: volatile registers are not preserved across a call.
VOLATILE = set("rax rcx rdx r8 r9 r10 r11".split())


def _full(name):
    """Map a 32/16/8-bit register name to its 64-bit container, so `mov r15d, 0` is seen."""
    if not name:
        return None
    n = name.lower()
    m = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi",
         "ebp": "rbp", "esp": "rsp"}
    if n in m:
        return m[n]
    if n.startswith("r") and n.endswith(("d", "w", "b")) and n[1:-1].isdigit():
        return "r" + n[1:-1]
    return n


def load_functions(path=FUNCS_TSV):
    out = {}
    if not os.path.exists(path):
        return out
    with io.open(path, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            a = (row.get("entry") or row.get("address") or "").strip().lower()
            a = a[2:] if a.startswith("0x") else a
            if not a:
                continue
            try:
                va = int(a, 16)
            except ValueError:
                continue
            size = 0
            # `functions.tsv` names this column `body_bytes`. It was omitted from this list once,
            # and the sweep then reported a clean 0 across 38,161 functions -- a dead scan that
            # looked exactly like a real negative. Hence the control in main().
            for k in ("body_bytes", "size", "length", "body", "bytes"):
                if row.get(k, "").strip().isdigit():
                    size = int(row[k])
                    break
            out[va] = (size, row.get("name", ""), row.get("owner", ""))
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(FUNCS_TSV):
        _b = uc1_band.load()
        for e in _b["removed"]:
            out.pop(e, None)
        for e, en in _b["extend"].items():
            if e in out:
                out[e] = (en - e, out[e][1], out[e][2])
        for st, sz in _b["frontier"].items():
            out[st] = (sz, "UC1-FRONTIER-%08X" % st, "")
    return out


class Scanner(object):
    def __init__(self, img):
        self.img = img
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def scan(self, va, size):
        """Yield (insn_va, mnemonic, op_str, target, kind) for every image-base-relative global.

        kind is 'read', 'write' or 'addr'. Returns [] when the function never materialises the
        base -- which is the common case and is not an error."""
        code = self.img.read(va, size)
        if not code:
            return []
        base_regs = {}          # reg -> True while it still holds the image base
        hits = []
        for i in self.md.disasm(code, va):
            # 1. does this instruction MATERIALISE the image base?
            if i.mnemonic == "lea" and len(i.operands) == 2:
                d, s = i.operands
                if (s.type == X86_OP_MEM and s.mem.base == X86_REG_RIP
                        and i.address + i.size + s.mem.disp == IMAGE_BASE
                        and d.type == X86_OP_REG):
                    base_regs[_full(i.reg_name(d.reg))] = True
                    continue

            # 2. does it USE a tracked base register?
            for op in i.operands:
                if op.type != X86_OP_MEM:
                    continue
                b = _full(i.reg_name(op.mem.base)) if op.mem.base else None
                x = _full(i.reg_name(op.mem.index)) if op.mem.index else None
                hit = None
                if b in base_regs:
                    hit = b
                elif x in base_regs and op.mem.scale == 1:
                    hit = x
                if hit is None:
                    continue
                tgt = IMAGE_BASE + op.mem.disp
                if i.mnemonic == "lea":
                    kind = "addr"
                elif i.operands and i.operands[0].type == X86_OP_MEM and op == i.operands[0]:
                    kind = "write"
                else:
                    kind = "read"
                hits.append((i.address, i.mnemonic, i.op_str, tgt, kind))

            # 3. INVALIDATE: any write to a tracked register, and volatiles across a call.
            if i.mnemonic == "call":
                for r in list(base_regs):
                    if r in VOLATILE:
                        del base_regs[r]
            elif i.operands:
                d = i.operands[0]
                if d.type == X86_OP_REG:
                    r = _full(i.reg_name(d.reg))
                    # `lea` into the base register was handled above; anything else clobbers it.
                    if r in base_regs and not (i.mnemonic == "lea" and r in base_regs
                                               and len(i.operands) == 2):
                        del base_regs[r]
        return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", default=_D.DEFAULT_EXE)
    ap.add_argument("--functions", default=FUNCS_TSV)
    ap.add_argument("--fn", help="one function VA (hex)")
    ap.add_argument("--addr", help="which functions reach this global through the base (hex)")
    ap.add_argument("--sweep", action="store_true", help="every function; totals")
    ap.add_argument("--out", help="write TSV rows here")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = _D.Image(a.exe)
    sc = Scanner(img)
    meta = load_functions(a.functions)

    if a.self_test:
        # 00195DF0 is the case that motivated this tool: it publishes the binding profiles
        # entirely through r15, and the RIP map sees none of it.
        hits = sc.scan(0x00195DF0, 526)
        tg = sorted(set(h[3] for h in hits))
        ok = True

        def claim(c, what):
            global_ok = c
            print("   %s  %s" % ("ok  " if c else "FAIL", what))
            return global_ok

        ok &= claim(len(hits) > 0, "00195DF0 yields image-base globals the RIP map cannot see")
        ok &= claim(0x01DF1738 in tg, "01DF1738 (the record it builds) is resolved")
        ok &= claim(0x01F80130 in tg, "01F80130 (the table it publishes to) is resolved")
        ok &= claim(any(h[4] == "write" for h in hits), "at least one WRITE is classified")
        # A function with no image-base lea must yield nothing -- the negative control.
        ok &= claim(sc.scan(0x003A6E60, 345) == [],
                    "control: a function with no image-base lea yields nothing")
        print()
        print("all claims hold" if ok else "FAILED")
        return 0 if ok else 1

    if a.fn:
        va = int(a.fn, 16)
        size = meta.get(va, (0,))[0] or 4096
        hits = sc.scan(va, size)
        print("%08X  %d image-base-relative global reference(s)" % (va, len(hits)))
        for at, mn, ops, tgt, kind in hits:
            print("  %08X  %-7s %-44s -> %08X  %s" % (at, mn, ops, tgt, kind))
        if not hits:
            print("  (this function does not materialise the image base -- the RIP map is complete "
                  "for it)")
        return 0

    # sweep -- with a POSITIVE CONTROL, because a mis-parsed size column silently turns this
    # into a scan that reports 0 for everything and looks like a clean negative.
    CTRL_VA, CTRL_GLOBAL = 0x00195DF0, 0x01F80130
    ctrl_size = meta.get(CTRL_VA, (0,))[0]
    if not ctrl_size:
        print("imagebase_refs: CONTROL FAILED -- %08X has no body size in %s. Every result "
              "below would be a dead scan; refusing to sweep." % (CTRL_VA, a.functions),
              file=sys.stderr)
        return 2
    if CTRL_GLOBAL not in [h[3] for h in sc.scan(CTRL_VA, ctrl_size)]:
        print("imagebase_refs: CONTROL FAILED -- %08X does not resolve %08X. Refusing to sweep."
              % (CTRL_VA, CTRL_GLOBAL), file=sys.stderr)
        return 2

    rows = []
    fns = 0
    for va, (size, name, owner) in sorted(meta.items()):
        if not size:
            continue
        hits = sc.scan(va, size)
        if hits:
            fns += 1
            for at, mn, ops, tgt, kind in hits:
                rows.append((va, at, tgt, kind, name, owner))

    if a.addr:
        want = int(a.addr, 16)
        sel = [r for r in rows if r[2] == want]
        print("global %08X reached through the image base by %d function(s):"
              % (want, len(set(r[0] for r in sel))))
        for va in sorted(set(r[0] for r in sel)):
            kinds = sorted(set(r[3] for r in sel if r[0] == va))
            nm = meta.get(va, (0, "", ""))[1]
            print("   %08X  %-28s %s" % (va, nm[:28], "/".join(kinds)))
        return 0

    kinds = collections.Counter(r[3] for r in rows)
    print("IMAGE-BASE-RELATIVE GLOBAL REFERENCES")
    print("   positive control             : %08X resolves %08X  OK" % (CTRL_VA, CTRL_GLOBAL))
    print("   functions scanned            : %d" % len(meta))
    print("   functions using the base reg : %d  (%.2f %%)" % (fns, 100.0 * fns / max(1, len(meta))))
    print("   references resolved          : %d" % len(rows))
    print("   distinct globals             : %d" % len(set(r[2] for r in rows)))
    for k in ("read", "write", "addr"):
        print("      %-6s %d" % (k, kinds.get(k, 0)))
    print()
    print("   These are references the RIP-relative map does NOT contain. A 'no writer' or")
    print("   'N writers' answer from that instrument is sound only modulo this set.")
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["function", "insn", "global", "kind", "name", "owner"])
            for va, at, tgt, kind, name, owner in rows:
                w.writerow(["%08X" % va, "%08X" % at, "%08X" % tgt, kind, name, owner])
        print()
        print("   wrote %s (%d rows)" % (a.out, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
