"""sd_slot_header_reads.py - part 2: who reads the save controller's per-slot header copies (OPUS, 2026-09-30).

00580CD0 copies the active image's 0xA0-byte header (image +0x00 .. +0x9F) into the controller's slot-header table:
[ctrl + 0x1C0] + slot * 0xA0 (ctrl = [02CA99B8]; 00580DB0..00580E17). That table is where the save list's header copies
live, so SD-40 (dwords 0x12 / 0x13 = +0x48 / +0x4C) and SD-42 (the stamp copies +0x58 / +0x60) turn on its readers.

Engine: the OV-5/8 (d) census (../ov58d-pointer-flow-0930/ov58d_flow.py) with two extra tokens:
  CTRL  the controller object (a load of [02CA99B8]),
  HDR   the slot-header table (a load of [CTRL + 0x1C0]); HDR + slot * 0xA0 keeps HDR with an unknown offset.
A memory operand whose base register holds HDR is a header field access: field = (offset + disp) mod 0xA0 (disp mod
0xA0 when the slot is unknown). Every such access is written to sd_slot_header_reads.tsv; the four SD fields are printed.
Also printed: every store of an HDR pointer into memory (an escape, e.g. the panel's +0x100 in 0057EFE0) and every
indirect call receiving CTRL or HDR - the flows this census does not follow, stated as its limit.

Control S1: 00580CD0 writes the slot table (the copy at 00580DBE .. 00580E17 stores through HDR).
Control S2: 0057EFE0 (the slot panel filler) reads field +0x08 through HDR (0057F05F `cmp [rsi+8]`), reached with the
header pointer as its second argument from 00580E2F.
"""
import collections, io, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ov58d-pointer-flow-0930"))
import ov58d_flow as F  # noqa: E402
K, X = F.K, F.X

CTRL_G, TABLE_OFF, HDR_SIZE = 0x02CA99B8, 0x1C0, 0xA0
# The table's owner is the save menu widget: 00583040 creates it through the widget factory 00244F50 (size 0x1C8,
# message handler 0057FE80, lea at 005831C5) and stores it at [ctrl + 0xD8] (0058320A). The handler takes the widget in
# rcx (0057FE8F mov rbx, rcx) and allocates the table into [widget + 0x1C0] (0057FF20). So the widget (MENU) is the
# handler's rcx or a load of [CTRL + 0xD8], and the table (HDR) is a load of [MENU + 0x1C0].
MENU_FIELD, HANDLER = 0xD8, 0x0057FE80
# The menu hands a header pointer to its child panels: 0057E6D0 stores it at [panel + 0xD0] (0057E6E3) and 0057EFE0 at
# [panel + 0x100] (0057EFF3). Those panels' own methods read it back through that field, which the flow does not
# follow. Part 3 covers them: in every function of the save UI module (UI_LO .. UI_HI, the functions around the menu,
# its panels and the controller), an 8-byte load of [reg + 0xD0] or [reg + 0x100] is taken as HDRP, a header held by a
# panel (an over-approximation inside the module: it can only add candidates).
UI_LO, UI_HI, PANEL_FIELDS = 0x0057C000, 0x00586000, (0xD0, 0x100)
FIELDS = {0x48: "dword 0x12 (+0x48)", 0x4C: "dword 0x13 (+0x4C)", 0x58: "stamp copy +0x58", 0x60: "stamp copy +0x60"}
acc = collections.defaultdict(set)     # field -> {(fn, addr, kind, text)}
CUR = []

_state = F.is_state
K.has_actor = lambda v: v is not K.UNK and any(_state(b) or b in ("CTRL", "MENU", "HDR", "HDRP") for b, _ in v)

_load = K.load_value


def load_value(st, addr):
    if addr is not K.UNK and addr and all(b == "CTRL" and o == MENU_FIELD for b, o in addr):
        return K.vs(("MENU", 0))
    if addr is not K.UNK and addr and all(b == "MENU" and o == TABLE_OFF for b, o in addr):
        return K.vs(("HDR", 0))
    return _load(st, addr)


K.load_value = load_value
F.K.load_value = load_value

_memaddr = K.memaddr


def memaddr(st, m, ins):
    a = _memaddr(st, m, ins)
    if CUR and m.base not in (0, X.X86_REG_RIP):
        bv = st.r.get(K.fullname(m.base)[0], K.UNK)
        if bv is not K.UNK and any(b in ("HDR", "HDRP") for b, _ in bv):
            ops = ins.operands

            def same(q):
                return (q.base, q.index, q.scale, q.disp) == (m.base, m.index, m.scale, m.disp)
            is_dst = bool(ops) and ops[0].type == X.X86_OP_MEM and same(ops[0].mem)
            size = ops[0].size if is_dst else (ops[1].size if len(ops) > 1 and ops[1].type == X.X86_OP_MEM else 4)
            kind = "LEA" if ins.mnemonic == "lea" else ("W" if is_dst and ins.mnemonic not in ("cmp", "test") else "R")
            for b, o in bv:
                if b not in ("HDR", "HDRP"):
                    continue
                field = ((o or 0) + m.disp) % HDR_SIZE
                acc[(field, size)].add((CUR[-1], ins.address, kind, "%s %s%s" % (ins.mnemonic, ins.op_str, " [panel-held]" if b == "HDRP" else "")))
    return a


K.memaddr = memaddr
F.K.memaddr = memaddr


SEED_DISP = 0x1C0


def _touch_all_mem(st, i):
    """The engine resolves a memory operand only for a load into a register or a store; a read-only use (cmp, test,
    a flag-setting and/or/add into a register from memory is covered, a compare against memory is not) never reaches
    memaddr. Resolve every memory operand once before the step, so the recording hook sees every access."""
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base not in (0, X.X86_REG_RIP):
            memaddr(st, op.mem, i)


class SlotCensus(F.Census):
    def step(self, f, st, i, depth, stack, caller_writes):
        if CUR:
            _touch_all_mem(st, i)
        res = super().step(f, st, i, depth, stack, caller_writes)
        ops = i.operands
        if (UI_LO <= f < UI_HI and i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X.X86_OP_REG
                and ops[0].size == 8 and ops[1].type == X.X86_OP_MEM and ops[1].mem.disp in PANEL_FIELDS
                and ops[1].mem.index == 0 and ops[1].mem.base not in (0, X.X86_REG_RIP)):
            res[1].r[K.fullname(ops[0].reg)[0]] = K.vs(("HDRP", 0))
        return res

    def run(self, f, ctx, depth, stack):
        CUR.append(f)
        try:
            return super().run(f, ctx, depth, stack)
        finally:
            CUR.pop()


def hits(want):
    out = set()
    for (field, size), xs in acc.items():
        if field < want + 4 and field + max(size, 1) > want:
            out |= xs
    return out


def seeded_functions():
    """Every catalogued function holding an 8-byte `mov reg, [reg + 0x1C0]` (the seed)."""
    import uc1_band
    sizes, _ = uc1_band.apply_extents(dict(F.R.ext))
    for st_, sz in uc1_band.load()["frontier"].items():
        sizes.setdefault(st_, sz)
    out = set()
    for f, n in sizes.items():
        d = F.R.at(f, n) if n else None
        if not d:
            continue
        for i in F.R.md.disasm(d, f):
            ops = i.operands
            if (i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X.X86_OP_REG and ops[0].size == 8
                    and ops[1].type == X.X86_OP_MEM and ops[1].mem.disp == SEED_DISP and ops[1].mem.index == 0
                    and ops[1].mem.base not in (0, X.X86_REG_RIP)):
                out.add(f)
                break
    print("seeded functions (an 8-byte load of [reg + 0x1C0]): %d" % len(out))
    return out


def main():
    t0 = time.time()
    refs, calls = F.scan()
    F.globals_root.clear()
    F.globals_root[CTRL_G] = frozenset([("CTRL", 0)])
    an = SlotCensus()
    roots = set(f for f, _, _ in refs.get(CTRL_G, ()))
    an.summary(HANDLER, (("rcx", K.vs(("MENU", 0))),), 0, ())
    ui = sorted(f for f in F.R.ext if UI_LO <= f < UI_HI)
    roots |= set(ui)
    print("save UI module functions rooted for panel-held headers: %d" % len(ui))
    for f in sorted(roots):
        try:
            an.summary(f, (), 0, ())
        except Exception as e:  # noqa: BLE001
            print("  error in %08X: %s %r (a blind spot)" % (f, type(e).__name__, e))
    print("roots (referencing [02CA99B8], plus the widget handler 0057FE80 with rcx = MENU) %d, bodies reached %d (%.0f s)" % (len(roots), len(an.fns), time.time() - t0))
    s1 = any(x[0] == 0x00580CD0 and x[2] == "W" for xs in acc.values() for x in xs)
    s2 = any(x[1] == 0x0057F05F for x in hits(0x08))
    print("%s  S1 00580CD0 stores into the slot-header table" % ("PASS" if s1 else "FAIL"))
    print("%s  S2 0057EFE0 reads field +0x08 at 0057F05F" % ("PASS" if s2 else "FAIL"))
    with io.open(os.path.join(HERE, "sd_slot_header_reads.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("field\tsize\tfunction\taddress\tkind\tinstruction\n")
        for (field, size), xs in sorted(acc.items()):
            for fn, a, kind, text in sorted(xs):
                o.write("+0x%02X\t%d\t%08X\t%08X\t%s\t%s\n" % (field, size, fn, a, kind, text))
    fields_read = sorted(set(f for (f, _), xs in acc.items() if any(x[2] == "R" for x in xs)))
    print("header fields read through HDR: %s" % " ".join("+0x%02X" % f for f in fields_read))
    for want, name in FIELDS.items():
        xs = hits(want)
        rd = sorted(set("%08X@%08X" % (x[0], x[1]) for x in xs if x[2] == "R"))
        wr = sorted(set("%08X" % x[0] for x in xs if x[2] == "W"))
        print("%-20s reads %d: %s | writes: %s" % (name, len(rd), " ".join(rd) or "-", " ".join(wr) or "-"))
    esc = sorted(set(e for e in an.escapes if "HDR" in str(e) or True))
    hdr_esc = [e for e in esc if e[0] in an.fns]
    print("escapes of CTRL/HDR-derived pointers (flows not followed further): %d" % len(hdr_esc))
    for e in hdr_esc:
        print("  ESCAPE   %08X %08X %-46s to %s" % e)
    ind = sorted(set(an.indirect))
    print("indirect calls receiving CTRL/HDR (not followed): %d" % len(ind))
    for e in ind:
        print("  INDIRECT %08X %08X %-46s args %s" % e)
    print("elapsed %.0f s" % (time.time() - t0))
    return 0 if (s1 and s2) else 1


if __name__ == "__main__":
    sys.exit(main())
