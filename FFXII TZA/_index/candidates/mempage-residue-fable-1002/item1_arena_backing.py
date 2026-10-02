"""item1_arena_backing.py - where each arena's backing memory comes from (FABLE, 2026-10-02). Static, read-only.

Question (memory page, intro and Section 2): the fifteen-record arena (records at 022D7FD0, initializer 00369D30(id, block,
size, slots)) carves memory that someone else obtained. Which function obtains each arena's block, from which call site?

Method
  M1  raw E8/E9/jcc index of the initializer 00369D30 (not the call graph), plus rip-relative operands, absolute qwords
      and RVA dwords that equal it (unwind entries named as such).
  M2  writers of the enable mask 022D89B8 (rip-relative operand census over every listed body): an arena is usable only
      after its bit is set, so a second enabling path would show here.
  M3  at each initializer call: the id (ecx), the block (rdx), the size (r8d) and the slot count (r9d), read by a
      backward linear walk inside the caller; a block loaded from a global is traced to the store into that global and
      the call whose rax it stores.
  M4  the two producers: the malloc shim 0036D240 (body + its thunk + the import it reaches, resolved through the PE
      import directory) and the arena wrapper 0036A190 with the selection push 0036C1D0 before it.
  M5  arena 12's caller 003E9AA0 is reached only through verb 0395's dispatch qword; its arguments in the shipped
      scripts are read from FABLE's decompiled US corpus when that (gitignored) corpus is present.

Controls
  C1  boot 0022A0B0 must give exactly nine initializer calls with ids {2..9, 11} (the page's table and EXP-142).
  C2  the malloc shim's import must resolve to `malloc` in api-ms-win-crt-heap-l1-1-0.dll (the page's census).
  C3  M2 must find the initializer's own `or`-store at 00369DE7 (instrument sees a known writer).
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mp_lib import *

INIT, SHIM, SHIMFREE, AWRAP, PUSH = 0x369D30, 0x36D240, 0x36D250, 0x36A190, 0x36C1D0
MASK = 0x22D89B8
fails = []


def imports():
    """{iat_slot_address: (dll, name)}"""
    dd = _ddir = struct.unpack_from("<II", d, _pe_opt() + 112 + 8)
    rva, size = dd
    res = {}
    o = off(BASE + rva)
    while True:
        oft, _ts, _fc, name_rva, ft = struct.unpack_from("<IIIII", d, o)
        if name_rva == 0:
            break
        dll = d[off(BASE + name_rva):].split(b"\0")[0].decode()
        k = 0
        while True:
            thunk = struct.unpack_from("<Q", d, off(BASE + (oft or ft)) + 8 * k)[0]
            if thunk == 0:
                break
            nm = ("#%d" % (thunk & 0xFFFF)) if thunk >> 63 else d[off(BASE + (thunk & 0x7FFFFFFF)) + 2:].split(b"\0")[0].decode()
            res[BASE + ft + 8 * k] = (dll, nm)
            k += 1
        o += 20
    return res


def _pe_opt():
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    return pe + 24


def regval(ins, k, reg, depth=0):
    """value written to `reg` (a 32/64-bit name family) by the last writer before ins[k], linear walk."""
    fam = {"ecx": ("ecx", "rcx"), "edx": ("edx", "rdx"), "r8d": ("r8d", "r8"), "r9d": ("r9d", "r9"),
           "rcx": ("ecx", "rcx"), "rdx": ("edx", "rdx")}[reg]
    for j in range(k - 1, -1, -1):
        x = ins[j]
        ops = x.op_str.replace(" ", "")
        dst = ops.split(",")[0]
        if x.mnemonic == "call" and fam[0] in ("ecx", "edx", "r8d", "r9d"):
            return ("clobbered-by-call", x.address)
        if dst not in fam:
            continue
        src = ops.split(",", 1)[1] if "," in ops else ""
        if x.mnemonic == "mov" and re.fullmatch(r"-?0x[0-9a-f]+|\d+", src):
            return (int(src, 0), x.address)
        if x.mnemonic == "xor" and src in fam:
            return (0, x.address)
        if x.mnemonic == "lea":
            m = re.fullmatch(r"\[(r\w+)([+-])(0x[0-9a-f]+|\d+)\]", src)
            if m and m.group(1) in ("r9", "r8", "rdx"):
                base = regval(ins, j, {"r9": "r9d", "r8": "r8d", "rdx": "edx"}[m.group(1)], depth + 1)
                if isinstance(base[0], int):
                    v = int(m.group(3), 0)
                    return (base[0] + v if m.group(2) == "+" else base[0] - v, x.address)
            return ("lea " + src, x.address)
        if x.mnemonic == "mov" and "[rip" in src:
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    return (("global", rip_target(x, op)), x.address)
        if x.mnemonic == "mov" and src == "rax":
            return (("rax", None), x.address)
        if x.mnemonic == "cmovns":
            return ("cmovns " + src, x.address)
        return (x.mnemonic + " " + x.op_str, x.address)
    return (None, None)


def main():
    out = []
    p = out.append
    p("# item 1 - arena backing sources (static). run: item1_arena_backing.py at %s" % head_sha())
    imp = imports()
    # M1 raw index
    idx = raw_index([INIT, SHIM, SHIMFREE, AWRAP])
    p("\n## M1 raw E8/E9/jcc sites of the initializer 00369D30")
    sites = []
    for site, form, o, al in sorted(idx[INIT]):
        p("  %-6s %08X in %s%s" % (form, site, "%08X" % o if o else "unlisted", "" if al else "  (byte coincidence, not an instruction)"))
        if al:
            sites.append((site, o))
    p("  aligned sites: %d" % len(sites))
    # pointer forms
    q = struct.pack("<Q", INIT); r32 = struct.pack("<I", INIT - BASE)
    qh = [m.start() for m in re.finditer(re.escape(q), d)]
    rh = [m.start() for m in re.finditer(re.escape(r32), d)]
    p("  absolute-qword copies of 00369D30 in the file: %d" % len(qh))
    for fo in rh:
        nxt = struct.unpack_from("<I", d, fo + 4)[0]
        kind = "RUNTIME_FUNCTION begin (next dword = end RVA %X, i.e. an unwind entry)" % nxt if 0 < nxt - (INIT - BASE) < 0x400 else "other"
        p("  RVA-dword copy at file offset %X: %s" % (fo, kind))
    riphits, maskw = [], []
    for fn in all_functions():
        for x in decode(fn):
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = rip_target(x, op)
                    if t == INIT:
                        riphits.append((x.address, fn))
                    if MASK <= t < MASK + 4 and (op.access & CS_AC_WRITE):
                        maskw.append((x.address, fn, x.mnemonic + " " + x.op_str, op.size))
    p("  rip-relative operands resolving to 00369D30: %d" % len(riphits))
    # M2
    p("\n## M2 writers of the enable mask 022D89B8 (rip operand census, all %d listed bodies)" % len(all_functions()))
    for a, fn, s, w in maskw:
        p("  %08X in %08X  %s   (width %d)" % (a, fn, s, w))
    if not any(a == 0x369DE7 for a, *_ in maskw):
        fails.append("C3 initializer mask store not seen")
    # M3
    p("\n## M3 per call: id, block source, size, slots")
    rows = []
    for site, fn in sites:
        ins = decode(fn)
        k = [i for i, x in enumerate(ins) if x.address == site][0]
        rid = regval(ins, k, "ecx")[0]
        blk = regval(ins, k, "rdx")
        size = regval(ins, k, "r8d")[0]
        slots = regval(ins, k, "r9d")[0]
        src = "?"
        if isinstance(blk[0], tuple) and blk[0][0] == "global":
            g = blk[0][1]
            # store into g in the same function, and the producing call before it
            st = None
            for j, x in enumerate(ins):
                for op in x.operands:
                    if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and rip_target(x, op) == g and (op.access & CS_AC_WRITE) and x.address < site:
                        st = j
            if st is not None:
                call = None
                for j in range(st - 1, -1, -1):
                    if ins[j].mnemonic == "call":
                        call = ins[j]; break
                creq = regval(ins, [i for i, x in enumerate(ins) if x.address == call.address][0], "ecx")[0]
                src = "global %08X <- rax of call %s at %08X (request ecx=%s) stored at %08X" % (
                    g, call.op_str, call.address, hex(creq) if isinstance(creq, int) else creq, ins[st].address)
        elif isinstance(blk[0], tuple) and blk[0][0] == "rax":
            for j in range(k - 1, -1, -1):
                if ins[j].mnemonic == "call" and ins[j].op_str.startswith("0x"):
                    tgt = int(ins[j].op_str, 16)
                    if tgt in (AWRAP, SHIM):
                        creq = regval(ins, j, "ecx")[0]
                        push = None
                        for jj in range(j - 1, -1, -1):
                            if ins[jj].mnemonic == "call" and ins[jj].op_str == hex(PUSH):
                                push = (regval(ins, jj, "ecx")[0], regval(ins, jj, "edx")[0], ins[jj].address); break
                        src = "rax of call %08X at %08X (request ecx=%s)%s" % (tgt, ins[j].address,
                              hex(creq) if isinstance(creq, int) else creq,
                              "; selection push 0036C1D0(arena=%s, category=%s) at %08X" % push if push else "")
                        break
        rows.append((site, fn, rid, src, size, slots))
        p("  %08X in %08X  id=%s  size=%s  slots=%s\n      block: %s" % (site, fn, rid if not isinstance(rid, int) else hex(rid),
          hex(size) if isinstance(size, int) else size, hex(slots) if isinstance(slots, int) else slots, src))
    boot = sorted(r[2] for r in rows if r[1] == 0x22A0B0 and isinstance(r[2], int))
    p("  C1 boot ids: %s" % [hex(i) for i in boot])
    if boot != [2, 3, 4, 5, 6, 7, 8, 9, 11]:
        fails.append("C1 boot ids differ")
    # M4
    p("\n## M4 the producers")
    for fn in (SHIM, SHIMFREE, AWRAP):
        p("  %08X: %s" % (fn, " | ".join(x.mnemonic + " " + x.op_str for x in decode(fn))))
    for thunk in (0x85E730, 0x19C590):
        x = list(md.disasm(d[off(thunk):off(thunk) + 7], thunk))[0]
        slot = rip_target(x, x.operands[0])
        p("  thunk %08X: %s %s -> IAT slot %08X = %s" % (thunk, x.mnemonic, x.op_str, slot, imp.get(slot)))
    xm = list(md.disasm(d[off(0x85E730):off(0x85E730) + 7], 0x85E730))[0]
    if imp.get(rip_target(xm, xm.operands[0])) != ("api-ms-win-crt-heap-l1-1-0.dll", "malloc"):
        fails.append("C2 malloc import")
    p("  raw sites of the shim 0036D240: %s" % ", ".join("%08X in %08X" % (s, o) for s, f, o, al in sorted(idx[SHIM]) if al))
    p("  raw sites of the free shim 0036D250: %s" % ", ".join("%08X in %08X" % (s, o) for s, f, o, al in sorted(idx[SHIMFREE]) if al))
    # M5
    p("\n## M5 arena 12's caller 003E9AA0 and verb 0395")
    r = raw_index([0x3E9AA0, 0x34D080])
    for t in (0x3E9AA0, 0x34D080):
        p("  raw sites of %08X: %s" % (t, ", ".join("%s %08X in %s" % (f, s, "%08X" % o if o else "unlisted") for s, f, o, al in r[t] if al) or "none"))
    qh = [m.start() for m in re.finditer(re.escape(struct.pack("<Q", 0x34D080)), d)]
    for fo in qh:
        p("  absolute qword 0034D080 at file offset %X" % fo)
    corpus = os.path.join(DBROOT, "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
    if os.path.isdir(corpus):
        txt = [f for f in os.listdir(corpus) if f.endswith(".txt")]
        calls = []
        for f in txt:
            for line in open(os.path.join(corpus, f), encoding="utf-8", errors="replace"):
                if "setexpandvoicememory" in line.lower():
                    calls.append((f, line.strip()))
        p("  decompiled US corpus: %d scripts; setexpandvoicememory calls: %d" % (len(txt), len(calls)))
        for f, l in calls:
            p("    %s: %s" % (f, l))
    else:
        p("  decompiled corpus not present on this machine; shipped arguments not re-read")
    p("\nFAILS %d %s" % (len(fails), fails))
    open(os.path.join(HERE, "item1_arena_backing.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


main()
