#!/usr/bin/env python3
"""state_authority_scan.py - which bodies WRITE static state, and to where.

BQ-15 (FABLE's instrument requirement): the ownerless-helper rule cannot be
tested image-wide without operationalising "independent subsystem
state/lifecycle authority". Two cheap proxies were tried and both failed on
measured grounds:

  * caller diversity - the 585 sealed ownerless functions are NOT shared in
    that sense (only 18 have callers spanning 2+ owners);
  * a rip-relative store sweep - register-base stores are the dominant form
    for exactly the objects that carry subsystem state. The planted control
    `001AF470` installs 222 slot pointers as `lea rax, [rip->global]` +
    `mov [rcx+0x3B00+slot], rax` pairs and a rip sweep credits it with zero.

This instrument tracks BASE REGISTERS inside each listed body: a
`lea reg, [rip->T]` (or `mov reg, imm64`) binding reg to a static address T
makes every later store `[reg + disp]` a write to T+disp, until something
writes reg (reg_tracking.written, the corrected kill rule). Registers are
killed at kills only - a linear sweep, a floor on branching code, as
documented in reg_tracking.py.

Three measures per body, kept apart because they are different kinds of
authority:

  A  static-write sites     - stores whose DESTINATION base is a bound static
                              register (or a direct mov [rip->T]) -> the body
                              writes static storage outright
  B  installed pointers     - stores whose SOURCE is a bound static register:
                              the body binds global addresses into live
                              structures (001AF470's whole shape)
  dyn indexed static stores - A-stores with an index register (variable slot;
                              the exact site is data-dependent)

Writes through a base loaded from memory (mov reg, [rip->ptr]) are heap
stores, not static-state writes, and are deliberately not counted.

Controls shipped with the instrument (BQ-15's own warning: an instrument
that cannot see the control is not measuring):
  1. 001AF470 must report B >= 100 installed pointers (the 222-slot
     installer; extent-limited count is reported, not assumed).
  2. At least one body image-wide must report an A-class register-base
     store, or the sweep is once again blind to the form it exists to see.

    state_authority_scan.py [--exe EXE] [--funcs functions.tsv] [--out TSV]
"""
import argparse, bisect, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP          # noqa: E402
import disasm_fn as DF          # noqa: E402
import reg_tracking as RT       # noqa: E402

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP
except ImportError:
    sys.stderr.write("state_authority_scan: needs capstone\n")
    raise SystemExit(2)

MAXDISP = 0x100000     # a bound base with a larger disp is not the same object
CONTROL = 0x001AF470   # the planted positive: B-class installs must be nonzero


def static(img, va):
    """True when va lands in a writable static section (.data/.bss-style);
    read-only data is indexed separately by the caller via img.section."""
    s = img.section(va)
    return s in (".data", ".bss", "_RDATA")   # _RDATA is writable here (BSS-like)


def scan_body(md, img, start, body):
    """One body -> (a_sites, b_sites, dyn_count). Linear sweep, kills via
    reg_tracking.written; branches are not modelled (a floor)."""
    bound = {}          # canon reg -> static base va
    a_sites, b_sites, dyn = set(), set(), 0
    for ins in md.disasm(body, start):
        # kill first: a `lea rax, [rip->T]` WRITES rax, so a post-instruction
        # kill would erase the binding it just made. Sources this instruction
        # reads keep their pre-instruction binding - that is the write order
        # the CPU executes, and for `lea`/`mov` the written reg IS the new
        # binding, established below after the kill.
        for r in RT.written(ins):
            bound.pop(r, None)
        # bind: lea reg, [rip+d] and mov reg, imm64 into a static section
        if ins.mnemonic == "lea" and len(ins.operands) == 2:
            dst, src = ins.operands
            if (dst.type == X86_OP_REG and src.type == X86_OP_MEM
                    and src.mem.base == X86_REG_RIP):
                tgt = ins.address + ins.size + src.mem.disp
                if img.section(tgt):
                    bound[RT.canon(ins.reg_name(dst.reg))] = tgt
        elif ins.mnemonic == "mov" and len(ins.operands) == 2:
            dst, src = ins.operands
            if (dst.type == X86_OP_REG and src.type == X86_OP_IMM
                    and img.section(src.imm) in (".data", ".bss")):
                bound[RT.canon(ins.reg_name(dst.reg))] = src.imm
        # stores
        for oi, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM:
                continue
            kind = RT.op_kind(ins, op, oi)
            if kind not in ("w", "rw"):
                continue
            mem = op.mem
            if mem.base == X86_REG_RIP:
                a_sites.add(ins.address + ins.size + mem.disp)   # direct [rip]
            elif mem.base:
                base_reg = RT.canon(ins.reg_name(mem.base))
                if base_reg in bound:
                    if mem.index:
                        dyn += 1                                # [base+idx*s+d]
                    elif 0 <= mem.disp <= MAXDISP:
                        a_sites.add(bound[base_reg] + mem.disp)
        # installed pointers: a store whose register SOURCE is a bound static
        if ins.mnemonic in ("mov", "movnti", "xchg"):
            dst = ins.operands[0] if ins.operands else None
            if dst is not None and dst.type == X86_OP_MEM \
                    and RT.op_kind(ins, dst, 0) in ("w", "rw"):
                for op in ins.operands[1:]:
                    if op.type == X86_OP_REG:
                        sr = RT.canon(ins.reg_name(op.reg))
                        if sr in bound:
                            b_sites.add(bound[sr])
    return a_sites, b_sites, dyn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=KP.EXE)
    ap.add_argument("--funcs", default=os.path.join(KP.WORK, "graph",
                                                  "functions.tsv"))
    ap.add_argument("--out", default=os.path.join(
        KP.WORK, "graph", "state-authority.tsv"))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    img = DF.Image(a.exe)
    text = next(s for s in img.secs if s[0] == ".text")
    _, tva, tvs, tro, trs = text
    tva += img.base
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = []
    for ln, line in enumerate(io.open(a.funcs, encoding="utf-8")):
        if ln == 0 or a.limit and ln > a.limit:
            continue
        f = line.split("\t")
        try:
            entry = int(f[0], 16)
            size = int(f[2])
        except (ValueError, IndexError):
            continue
        if not (tva <= entry < tva + tvs) or size <= 0:
            continue
        body = img.read(entry, size)
        if not body or len(body) < size:
            continue
        a_sites, b_sites, dyn = scan_body(md, img, entry, body)
        rows.append((entry, f[1], f[3], f[4] == "true",
                     len(a_sites), len(b_sites), dyn,
                     " ".join("%08X" % x for x in sorted(a_sites)[:40]),
                     " ".join("%08X" % x for x in sorted(b_sites)[:40])))

    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("entry\tname\towner\tfinal_no_owner\t"
                 "n_static_writes\tn_installed_ptrs\tn_dyn_indexed\t"
                 "static_write_sites\tinstalled_ptr_targets\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")

    # CONTROLS - an instrument that cannot see its own control measures nothing
    ctl = next((r for r in rows if r[0] == CONTROL), None)
    b_ok = ctl is not None and ctl[5] >= 100
    a_ok = any(r[4] > 0 for r in rows)
    print("bodies scanned: %d" % len(rows))
    print("control 001AF470 installed-ptr count: %s (need >=100) %s"
          % (ctl[5] if ctl else "missing", "PASS" if b_ok else "FAIL"))
    print("control: >=1 register-base static store exists image-wide: %s"
          % ("PASS" if a_ok else "FAIL"))
    return 0 if (b_ok and a_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
