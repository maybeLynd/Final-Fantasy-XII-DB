#!/usr/bin/env python3
"""record_field_scan.py - recover a record's field list by following a pointer chain.

Most records in this image are not reached from a global. They are reached by walking a chain of
pointers out of something that is: `actor -> [+0xB8] context -> [+0xF0] steering record`. A
displacement scan cannot see such a record at all, because `[rax + 0x28]` says nothing about what
`rax` holds, and a global cross-reference scan cannot see it either, because nothing references it.

So this tracks the chain **inside one function body**, register by register:

    mov R1, [Rk + <hop0>]        <- R1 now holds the intermediate
    mov R2, [R1 + <hop1>]        <- R2 now holds the record
    ...  [R2 + disp]             <- every displacement off R2 is a field of the record

and stops trusting a register the moment anything else writes to it. **Same-register,
same-function** - the technique that recovered 41 of 41 actor fields where a linear taint pass
recovered 4.

A control is mandatory
----------------------
`--control <va>=<disp>[,<disp>...]` re-runs the scan for a function whose fields the caller already
knows by hand, and **refuses to report if the control does not reproduce**. A scan that silently
tracks nothing and a record with no fields produce identical output, which is the failure this
project keeps paying for.

What it does not do
-------------------
- **It does not follow the chain across a call.** A record passed to a callee as an argument is
  invisible here, and the count is a floor rather than a total.
- **It does not prove the chain is the only route.** Another function may reach the same record by
  a different path; those fields are missed, not denied.
- **It does not infer field TYPES.** It reports the access width the instruction used, which is a
  lower bound on the field's size and not the same thing - a `byte` access on a `u32` field is
  ordinary.

Usage
-----
    python record_field_scan.py --chain 0xB8,0xF0 --control 0x26AE90=0x29,0x2C,0x7C
    python record_field_scan.py --chain 0xB8,0xF0 --control ... --out fields.tsv
"""
import argparse
import collections
import io
import os
import re
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ext_string_probe as P                                        # noqa: E402
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph_gn", "functions.tsv")

WRITE_MNEM = ("mov", "movzx", "movsx", "movsxd", "and", "or", "xor", "add", "sub", "inc", "dec",
              "movss", "movsd", "movaps", "movups", "lea", "shl", "shr", "sar", "not", "neg",
              "imul", "test", "cmp", "movd", "movq", "call", "pop", "setne", "sete", "cvtsi2ss")


def load(exe, funcs):
    blob = open(exe, "rb").read()
    secs = P.sections(blob)

    def rd(va, n):
        for _name, raw_off, raw_sz, sva in secs:
            if sva <= va < sva + raw_sz:
                o = raw_off + (va - sva)
                return blob[o:o + n]
        return b""

    rows = []
    for ln in io.open(funcs, encoding="utf-8", errors="replace"):
        p = ln.rstrip("\n").split("\t")
        if len(p) >= 9 and re.match(r"^[0-9A-F]{8}$", p[0]):
            tags = p[8]
            if "CompilerGeneratedEH" in tags:
                continue
            rows.append((int(p[0], 16), int(p[2]), p[1], p[3]))
    return rd, rows


def scan_function(md, code, va, hops, root_global=None):
    """-> {disp: [(mnemonic, size, is_write, site_va, text)]} for the record at the end of `hops`.

    `root_global` supports the THIRD class of record, the one neither generator handled until
    2026-09-13: reached through a STATIC POINTER. `ImageBackedStateBlock` is `*(void**)0x020927C0`
    and `Widget` is `*(char **)0x0208EA58 + i * 0x120` - the record is not at a static address, so a
    RIP-relative census finds nothing, and it is not reached by hops off an argument, so a chain
    scan from a base register finds nothing either. What identifies it is one instruction:

        mov RD, qword ptr [rip + X]        where rip + X resolves to the root global

    After that load, RD holds the pointer, and from there this is the ordinary chain scan - with
    `--chain` empty the register IS the record, and with hops given they are followed from it.
    """
    held = {}          # register -> hop index it currently holds (0 = intermediate, 1 = record...)
    out = collections.defaultdict(list)
    for i in md.disasm(code, va):
        ops = i.operands
        # a memory read `mov RD, [RB + disp]` may advance the chain
        advanced = None
        if i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP \
                and root_global is not None:
            if i.address + i.size + ops[1].mem.disp == root_global:
                # the register now holds the record itself when there are no further hops
                advanced = (i.reg_name(ops[0].reg), -1 if not hops else -1)
        elif i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_MEM and ops[1].mem.base != 0 \
                and ops[1].mem.base != X86_REG_RIP and ops[1].mem.index == 0:
            base = i.reg_name(ops[1].mem.base)
            disp = ops[1].mem.disp
            dst = i.reg_name(ops[0].reg)
            if hops and disp == hops[0]:
                advanced = (dst, 0)
            else:
                lvl = held.get(base)
                if lvl is not None and lvl + 1 < len(hops) and disp == hops[lvl + 1]:
                    advanced = (dst, lvl + 1)
        # every memory operand off a register that holds the FINAL hop is a field access
        # -1 marks 'this register holds the record itself', set by a root-global load.
        last = (len(hops) - 1) if hops else -1
        for o in ops:
            if o.type == X86_OP_MEM and o.mem.base != 0 and o.mem.base != X86_REG_RIP:
                if held.get(i.reg_name(o.mem.base)) == last:
                    is_write = (o is ops[0] and i.mnemonic not in ("cmp", "test"))
                    # The full instruction TEXT is carried, not just the mnemonic and the operand
                    # size. Downstream instruments read the text and cannot work without it:
                    # `check_census_widths` takes the width from it, and
                    # `check_float_typed_as_int` decides float-versus-integer from whether the
                    # instruction is `movss`, a float-constant store, a copy or arithmetic. A
                    # census that records `mov` and `4` cannot tell those apart, and a census this
                    # scan produces should be usable by the same tools as every hand-built one.
                    out[o.mem.disp].append((i.mnemonic, o.size, is_write, i.address,
                                            ('%s %s' % (i.mnemonic, i.op_str)).strip()))
        # then invalidate: anything written by this instruction stops being trusted -- with ONE
        # exception, found by a control rather than by reasoning.
        #
        # `0026C120` restores `mov rbx, [rsp+0x30]` in the mode-4 epilogue at `0026C1D2`. This scan
        # is LINEAR, not control-flow aware, so that restore killed tracking for every basic block
        # after it, and the mode-2/3 block at `0026C1E6` -- which is only reachable with the
        # tracked `rbx` still live -- lost `+0x58`, `+0x5C` and `+0x65`. The control declared those
        # three by hand and the scan refused to report. **That is the control doing its job.**
        #
        # An epilogue restore from the stack is therefore treated as NOT invalidating. It is the
        # less wrong approximation for a linear pass over MSVC output, and its cost is stated: a
        # function that genuinely reuses the register for an unrelated pointer after an epilogue
        # restore would have those accesses misattributed. The control set is the guard against
        # that, and it is why controls are mandatory here rather than optional.
        is_stack_reload = (i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG
                           and ops[1].type == X86_OP_MEM
                           and i.reg_name(ops[1].mem.base) in ("rsp", "rbp"))
        if i.mnemonic in WRITE_MNEM and not is_stack_reload:
            _r, w = i.regs_access()
            for r in w:
                held.pop(i.reg_name(r), None)
        if i.mnemonic == "call":
            # volatile registers do not survive a call under the MS x64 ABI
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                held.pop(r, None)
        if advanced:
            held[advanced[0]] = advanced[1]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--chain", required=True,
                    help="comma-separated hops, e.g. 0xB8,0xF0; may be empty with --root-global")
    ap.add_argument("--root-global", default=None,
                    help="VA of a static POINTER to the record, e.g. 0x020927C0")
    ap.add_argument("--control", action="append", required=True,
                    help="<va>=<disp>[,<disp>...] - a function whose fields are known by hand")
    ap.add_argument("--reject", action="append", default=[],
                    help="<va> - a NEGATIVE control: a function this chain must NOT admit. "
                         "The --control flag only asks whether the scan finds what is already "
                         "known, which cannot fail on a scan that admits too much; this one "
                         "can.")
    ap.add_argument("--out", default=None)
    ap.add_argument("--out-accesses", default=None,
                    help="per-access census TSV, the format check_census_widths reads")
    a = ap.parse_args()

    hops = [int(x, 0) for x in a.chain.split(",") if x.strip()]
    root_global = int(a.root_global, 0) if a.root_global else None
    if not hops and root_global is None:
        print("--chain is empty and no --root-global was given: there is nothing to track.")
        return 2
    rd, rows = load(a.exe, a.funcs)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    per_fn = {}
    for va, size, name, owner in rows:
        if size <= 0:
            continue
        code = rd(va, size)
        if not code:
            continue
        found = scan_function(md, code, va, hops, root_global)
        if found:
            per_fn[va] = (name, owner, found)

    # controls first - a scan that reports nothing and a record with no fields look identical
    ok = True
    print("CONTROLS - each must reproduce, or the scan is broken and nothing below is reportable")
    for c in a.control:
        cva, _, want = c.partition("=")
        cva = int(cva, 0)
        want = set(int(x, 0) for x in want.split(",") if x)
        got = set(per_fn.get(cva, (None, None, {}))[2].keys())
        miss = want - got
        print("  %08X  want %s" % (cva, ", ".join("+0x%02X" % d for d in sorted(want))))
        print("            got  %s%s"
              % (", ".join("+0x%02X" % d for d in sorted(got)) or "(nothing)",
                 "" if not miss else "   MISSING " + ", ".join("+0x%02X" % d for d in sorted(miss))))
        if miss:
            ok = False
    if not ok:
        print("\nCONTROL FAILED - refusing to report.")
        return 1
    print("  all controls reproduce\n")

    # --- THE OTHER HALF OF THE CONTROL, added 2026-09-19 (OPUS) -------------------------------
    # EVERY CONTROL IN THIS KIT UNTIL NOW HAS BEEN A SENSITIVITY CONTROL: "does the scan find
    # the fields I already know?" That question cannot fail on a scan that admits too much, and
    # the scan above admits a great deal. Its first hop is
    #     if hops and disp == hops[0]: advanced = (dst, 0)
    # which matches ANY `mov RD, [RB + hop0]` in ANY function, WITH NO CONSTRAINT ON RB. For a
    # two-hop chain that is tolerable, because the second hop filters. For a ONE-HOP chain there
    # is no filter at all.
    #
    # Measured on --chain 0xB8, the chain behind movement-context-accesses.tsv: 410 functions in
    # the image load a qword from [reg+0xB8], this scan admits 181 of them, and only 68 are in
    # Actor- or Movement-owned code. The other 113 include Audio, Presentation and the script-VM
    # bridge. Two of them - 004640A0 and 004017D0, both PRESENTATION - are why MovementContext's
    # declared floats appeared to contain byte-level bitfield inserts.
    #
    # So the owner spread is printed on every run, and --reject takes functions that MUST NOT be
    # admitted. A negative control cannot prove specificity either, but it can fail, which is
    # more than the sensitivity control could do here.
    owners_admitted = collections.Counter((o or "(none)") for _, o, _ in per_fn.values())
    print("ADMISSION SPREAD - which code domains own the functions this chain admitted")
    for k, v in owners_admitted.most_common():
        print("    %-30s %d" % (k, v))
    print("    A chain into one subsystem's record that admits several unrelated domains is")
    print("    reporting other types' fields. With one hop this is the expected failure, not a")
    print("    remote one: nothing constrains the base register the hop is taken from.")
    print()
    if a.reject:
        print("NEGATIVE CONTROL - these functions must NOT be admitted")
        bad = False
        for rtxt in [x for r in a.reject for x in r.split(",") if x.strip()]:
            rva = int(rtxt, 0)
            hit = rva in per_fn
            print("    %08X  %s" % (rva, "ADMITTED - the chain is too loose" if hit else "absent, as required"))
            if hit:
                bad = True
        if bad:
            print("\nNEGATIVE CONTROL FAILED - refusing to report.")
            return 1
        print()

    agg = collections.defaultdict(list)
    for va, (name, owner, found) in per_fn.items():
        for disp, accesses in found.items():
            for mn, sz, w, site, text in accesses:
                agg[disp].append((va, name, owner, mn, sz, w, site, text))

    print("RECORD FIELDS via chain %s" % " -> ".join("+0x%02X" % h for h in hops))
    print("  %d function(s) reach the record by this chain; %d distinct displacement(s)"
          % (len(per_fn), len(agg)))
    print()
    print("  offset   width  W  fns  owners                          first site")
    for disp in sorted(agg):
        acc = agg[disp]
        widths = sorted(set(x[4] for x in acc))
        fns = sorted(set(x[0] for x in acc))
        owners = sorted(set(x[2] or "-" for x in acc))
        nw = sum(1 for x in acc if x[5])
        print("  +0x%03X %6s %3d %4d  %-30s %08X"
              % (disp, "/".join(str(w) for w in widths), nw, len(fns),
                 ", ".join(owners)[:30], min(x[6] for x in acc)))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("offset\taccess_widths\twrites\treaders\tfunctions\towners\tsites\n")
            for disp in sorted(agg):
                acc = agg[disp]
                fh.write("0x%03X\t%s\t%d\t%d\t%s\t%s\t%s\n" % (
                    disp, "/".join(str(w) for w in sorted(set(x[4] for x in acc))),
                    sum(1 for x in acc if x[5]), sum(1 for x in acc if not x[5]),
                    ";".join("%08X" % v for v in sorted(set(x[0] for x in acc))),
                    ";".join(sorted(set(x[2] or "-" for x in acc))),
                    ";".join("%08X" % x[6] for x in sorted(acc, key=lambda y: y[6]))))
        print("\nwrote %s" % a.out)

    if a.out_accesses:
        # The per-ACCESS census, in the same shape every hand-built `*-accesses.tsv` uses, so that
        # `check_census_widths`, `gen_recoverable_gaps` and `check_float_typed_as_int` can read a
        # record this scan discovered without any of them learning a second format.
        #
        # Why this matters more than the summary beside it: on 2026-09-13 the gap instrument was
        # measured and covers 16 of the store's 247 types, because a type with no access census
        # produces no candidates and its gaps are invisible rather than absent. The chains this
        # scanner follows are exactly how the uncensused records are reached, so emitting the
        # census format is what turns it from a one-off analysis into a way of closing that gap.
        with io.open(a.out_accesses, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
            rows = []
            for disp, acc in agg.items():
                for va, name, owner, mn, sz, w, site, text in acc:
                    rows.append((site, va, name, disp, 'w' if w else 'r', text, owner))
            for site, va, name, disp, kind, text, owner in sorted(rows):
                fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\t%s\t%s\n"
                         % (va, name or ("FUN_%08x" % va).lower(), site, disp, kind, text,
                            "chain:" + a.chain, "owner=" + (owner or "-")))
        print("wrote %s (per-access census format)" % a.out_accesses)
    return 0


if __name__ == "__main__":
    sys.exit(main())
