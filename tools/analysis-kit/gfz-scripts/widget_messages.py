#!/usr/bin/env python3
"""widget_messages.py - recover the widget message protocol from the handlers themselves.

Every menu, window, HUD panel and options row in FFXII is one object with a **handler at `+0x00`**,
called as `handler(self, msg)` where `msg` is a 24-byte record whose first dword is a small id. The
object model is documented (`16-UI/Widget-Object-Model/`), the draw pass names ids 3, 4 and 5, and
the Config screen block named 10, 12, 13 and 14 in two handlers. **Nobody has enumerated the id
space**, and you cannot reimplement a menu without it.

Two passes, and each prints its own denominator.

PASS 1 - who are the handlers?
    One rule, per CONTRACT-widget-object.md §15b: **a widget procedure is an address that reaches
    a widget constructor's `proc` slot.** No list of installation idioms — the instrument computes
    which `lea <reg>, [rip+fn]` definitions reach each constructor transfer site, over the
    caller's own control-flow graph:

        00244F50(size ecx, handler rdx, initmsg r8)       -> handler in RDX
        002465F0(obj rcx, size edx, handler r8, ...)      -> handler in R8
        00245000(obj rcx, size edx, handler r8, ...)      -> handler in R8   (thin wrapper)

    The CFG is what makes the single rule sufficient where three heuristics were not:

      * a handler chosen on a branch that jumps BACKWARD into a shared call site (`0023B330`:
        `lea rdx, 0023B330` at 0023C0CD, branch back to the call at 0023BFFF) reaches the slot
        through the back-edge — the old address-order scan could not see it;
      * a branch choosing between two handlers produces two reaching `lea` defs — both are
        procedures, and both are counted (the old scan attributed the last one);
      * an address `lea`'d into the slot register but consumed by a DIFFERENT call does not reach
        the constructor — this is what removes `0027D700`/`0027D740`/`0027E3E0`/`0027E4E0`/
        `0027E7B0`, whose registers feed `00368A50`/`002969F0`/`00279C48`;
      * `jmp` tail-transfers to a constructor are transfer sites like `call` (17 sites, 14
        procedures the call-only census missed);
      * a `mov rdx, r9` / `mov rdx, r15` def at the site marks the function as a FORWARDER on that
        source register; the same analysis is then run at every call/jmp to the forwarder
        (`00564AC0` on r9, `00406E80` on r15 — the +7). One hop only: a pointer carried through
        more than one register hop is a documented limit, not silent undercount.

    Disassembly starts at each caller's ENTRY, never mid-body: a linear sweep through `.text`
    desynchronises on embedded data and silently skips whole functions.

PASS 2 - which ids does each handler answer?
    MSVC compiles a small dense switch on `msg->id` as a chain of `sub`/`cmp` against a running
    accumulator:

        mov ecx, [rdx]      ; ecx = id
        sub ecx, 1  ; je A  ->  id == 1
        sub ecx, 3  ; je B  ->  id == 4      (1+3)
        sub ecx, 6  ; je C  ->  id == 10     (4+6)
        cmp ecx, 2  ; jne D ->  id == 12+2 = 14

    This decodes that chain. **Handlers that use a jump table, or that never load `[rdx]`, are
    counted as UNPARSED rather than as "no messages"** - the difference between "answers nothing"
    and "this tool cannot read it" is the whole point of printing both numbers.
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
import kit_paths as KP  # noqa: E402
import uc1_band  # noqa: E402

ROOT = KP.ROOT
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

# constructor -> the register that carries the handler at the call
CTORS = {0x00244F50: "rdx", 0x002465F0: "r8", 0x00245000: "r8"}

# Verified terms of the corrected 267 (CONTRACT-widget-object.md §15b) - the control this
# instrument is checked against below. EXPECTED_ADD is the +14 tail-jump procedures plus the
# +7 one-hop forwards; EXPECTED_REM is the five that must NOT appear.
EXPECTED_ADD = {
    0x00285290, 0x00291D90, 0x0029E110, 0x002C13C0, 0x002C3560, 0x002C4460, 0x002CEB40,
    0x002CF740, 0x00393EA0, 0x00394130, 0x003EF830, 0x00406A60, 0x00565E00, 0x002985D0,
    0x005636F0, 0x00563930, 0x00563B10, 0x00563D20, 0x0056E140, 0x00407590, 0x004079A0,
}
EXPECTED_REM = {0x0027D700, 0x0027D740, 0x0027E3E0, 0x0027E4E0, 0x0027E7B0}

_CANON = {}
for _r64, _e32, _w16, _lo, _hi in (
        ("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"),
        ("rcx", "ecx", "cx", "cl", "ch"), ("rdx", "edx", "dx", "dl", "dh"),
        ("rsi", "esi", "si", "sil", None), ("rdi", "edi", "di", "dil", None),
        ("rbp", "ebp", "bp", "bpl", None), ("rsp", "esp", "sp", "spl", None)):
    for _a in (_r64, _e32, _w16, _lo, _hi):
        if _a:
            _CANON[_a] = _r64
for _n in range(8, 16):
    for _a in ("r%d" % _n, "r%dd" % _n, "r%dw" % _n, "r%db" % _n):
        _CANON[_a] = "r%d" % _n


def canon_reg(name):
    """Any general-purpose register name -> the 64-bit register that owns it."""
    return _CANON.get(name, name)


def load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        nm = d[off:off + 8].rstrip(b"\0").decode("latin1")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((nm, va, vs, ra, rs))
        off += 40
    return d, base, secs


def reader(d, base, secs):
    def rd(va, n):
        r = va - base
        for nm, sva, vs, ra, rs in secs:
            if sva <= r < sva + max(vs, rs):
                o = r - sva
                if o >= rs:
                    return None
                return d[ra + o: ra + o + n]
        return None
    return rd


def load_functions(path):
    out = {}
    f = io.open(path, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                out[int(p[0], 16)] = (int(p[2]), p[1], p[8] if len(p) > 8 else "")
            except ValueError:
                pass
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(FUNCS):
        _b = uc1_band.load()
        for e in _b["removed"]:
            out.pop(e, None)
        for e, en in _b["extend"].items():
            if e in out:
                out[e] = (en - e, out[e][1], out[e][2])
        for st, sz in _b["frontier"].items():
            out[st] = (sz, "UC1-FRONTIER-%08X" % st, "")
    return out


def _cfg(ins):
    """Basic blocks and successors for one function's instruction list.

    Returns (blocks, succ, blk_of): blocks is [(start_idx, end_idx)) over `ins`, succ[i] is the
    set of block indices reachable from block i, blk_of maps instruction index -> block index.
    A `call` falls through; a `jmp` to an immediate inside the function edges to its target; a
    `jmp` out (tail transfer, e.g. to a constructor) ends the path; `ret` and indirect `jmp`
    end it too."""
    addr2i = {i.address: n for n, i in enumerate(ins)}
    leaders = {0}
    for n, i in enumerate(ins):
        m, ops = i.mnemonic, i.operands
        if m == "ret":
            continue
        if m.startswith("j"):
            if ops and ops[0].type == X86_OP_IMM and ops[0].value.imm in addr2i:
                leaders.add(addr2i[ops[0].value.imm])
            if n + 1 < len(ins):
                leaders.add(n + 1)
    ls = sorted(leaders)
    blocks = [(ls[k], ls[k + 1] if k + 1 < len(ls) else len(ins)) for k in range(len(ls))]
    blk_of = {}
    for bi, (s, e) in enumerate(blocks):
        for n in range(s, e):
            blk_of[n] = bi
    succ = [set() for _ in blocks]
    for bi, (s, e) in enumerate(blocks):
        last = ins[e - 1]
        m, ops = last.mnemonic, last.operands
        nxt = bi + 1 if bi + 1 < len(blocks) else None
        if m == "ret" or m == "jmp" and (not ops or ops[0].type != X86_OP_IMM):
            continue
        if m == "jmp":
            t = ops[0].value.imm
            if t in addr2i:
                succ[bi].add(blk_of[addr2i[t]])
            continue
        if m.startswith("j") and ops and ops[0].type == X86_OP_IMM:
            t = ops[0].value.imm
            if t in addr2i:
                succ[bi].add(blk_of[addr2i[t]])
        if nxt is not None:
            succ[bi].add(nxt)
    return blocks, succ, blk_of


def _reg_defs(ins, i0, i1, R):
    """Every write to register R in ins[i0:i1], classified.

    ('lea', target, n)   - `lea R, [rip+disp]` at ins[n]: a materialised address
    ('reg', source, n)   - `mov/movzx/movsxd R, <reg>`: forwards whatever the source holds
    ('other', None, n)   - any other write: an immediate, a memory load, arithmetic - the value
                           cannot be named statically

    The instruction index rides along so a `('reg', ...)` def can be chased at its OWN site: the
    source register's reaching defs are wanted at the mov, not at the original query site - the
    source may be rewritten between the two.
    """
    out = []
    for n in range(i0, i1):
        i = ins[n]
        try:
            _, wr = i.regs_access()
        except Exception:
            continue
        if R not in {canon_reg(i.reg_name(x)) for x in wr}:
            continue
        m, ops = i.mnemonic, i.operands
        d = ("other", None, n)
        if m == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and canon_reg(i.reg_name(ops[0].value.reg)) == R \
                and ops[1].type == X86_OP_MEM and ops[1].value.mem.base == X86_REG_RIP:
            d = ("lea", i.address + i.size + ops[1].value.mem.disp, n)
        elif m in ("mov", "movzx", "movsxd") and len(ops) == 2 \
                and ops[0].type == X86_OP_REG \
                and canon_reg(i.reg_name(ops[0].value.reg)) == R \
                and ops[1].type == X86_OP_REG:
            d = ("reg", canon_reg(i.reg_name(ops[1].value.reg)), n)
        out.append(d)
    return out


def _reaching_defs(ins, blocks, succ, blk_of, site_idx, R):
    """The set of R-definitions that can reach ins[site_idx], by forward dataflow."""
    gen = []
    for s, e in blocks:
        ds = _reg_defs(ins, s, e, R)
        gen.append(ds[-1] if ds else None)
    IN = [set() for _ in blocks]
    OUT = [set() for _ in blocks]
    changed = True
    while changed:
        changed = False
        for bi in range(len(blocks)):
            inn = set()
            for p, ss in enumerate(succ):
                if bi in ss:
                    inn |= OUT[p]
            out = {gen[bi]} if gen[bi] is not None else inn
            if inn != IN[bi] or out != OUT[bi]:
                IN[bi], OUT[bi] = inn, out
                changed = True
    bi = blk_of[site_idx]
    prefix = _reg_defs(ins, blocks[bi][0], site_idx, R)
    return {prefix[-1]} if prefix else IN[bi]


def _resolve_sites(ins, site_filter, is_code):
    """Reaching-def resolution at a set of transfer sites inside one function.

    site_filter(site_target) -> the proc register for that transfer, or None to skip.
    Returns (handlers, forward_regs, unresolved_sites, site_count) where handlers is
    {target: (source_kind, site_addr, via)}."""
    blocks, succ, blk_of = _cfg(ins)
    handlers = {}
    forward = set()
    unresolved = []
    sites = 0
    for n, i in enumerate(ins):
        if i.mnemonic not in ("call", "jmp") or not i.operands \
                or i.operands[0].type != X86_OP_IMM:
            continue
        t = i.operands[0].value.imm
        R = site_filter(t)
        if R is None:
            continue
        sites += 1
        defs = _reaching_defs(ins, blocks, succ, blk_of, n, R)
        # Chase every `mov dst, src` def, not only a lone one. 00406E80 is exactly why a lone-reg
        # check undercounts: rdx's reaching set at the ctor call is {stack-`lea`, `mov rdx, r15`}
        # - two defs - while r15's own reaching defs at the mov are the two `lea r15` targets on
        # the loop arms. Chasing each reg def at its own site recovers both.
        leas = set()
        bad_paths = 0
        work = list(defs)
        seen = set()
        while work:
            d = work.pop()
            if d[0] == "reg":
                key = (d[2], d[1])
                if key in seen:
                    continue
                if len(seen) > 16:
                    bad_paths += 1
                    continue
                seen.add(key)
                sub = _reaching_defs(ins, blocks, succ, blk_of, d[2], d[1])
                if not sub:
                    forward.add(d[1])   # src is live-in at the mov: the fn forwards its own arg
                else:
                    work.extend(sub)
            elif d[0] == "lea" and is_code(d[1]):
                leas.add(d[1])
            else:
                bad_paths += 1
        if not defs:
            forward.add(R)          # no def reaches the site: the slot is the fn's live-in arg
        elif leas:
            for h in leas:
                handlers[h] = ("multi" if len(leas) > 1 else (
                    "tail" if i.mnemonic == "jmp" else "direct"), i.address, t)
            if bad_paths:
                unresolved.append(i.address)  # some paths reach the slot by an unreadable def
        else:
            unresolved.append(i.address)
    return handlers, forward, unresolved, sites


def find_handlers(md, rd, funcs, is_code):
    """Pass 1, the proc-slot rule. Returns (hits, sources, unresolved_sites, total_sites).

    hits:    {handler_va: [(caller_entry, site_addr, ctor_or_forwarder)]}
    sources: {handler_va: 'direct'|'tail'|'multi'|'forwarded'}
    """
    ctor_fns, call_map = {}, collections.defaultdict(set)
    for entry in sorted(funcs):
        size = funcs[entry][0]
        if size <= 0 or size > 0x20000:
            continue
        code = rd(entry, size)
        if code is None:
            continue
        ins = list(md.disasm(code, entry))
        has_ctor = False
        for i in ins:
            if i.mnemonic in ("call", "jmp") and i.operands \
                    and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].value.imm
                call_map[entry].add(t)
                if t in CTORS:
                    has_ctor = True
        if has_ctor:
            ctor_fns[entry] = ins

    hits = collections.defaultdict(list)
    sources = {}
    unresolved = []
    sites = 0
    forwarders = collections.defaultdict(set)
    for entry, ins in sorted(ctor_fns.items()):
        hs, fw, un, ns = _resolve_sites(ins, CTORS.get, is_code)
        sites += ns
        for h, (src, site, via) in hs.items():
            hits[h].append((entry, site, via))
            sources[h] = src
        forwarders[entry] |= fw
        unresolved += un

    # one forwarding hop: at each call/jmp to a forwarder, the forwarder's incoming register
    # is the new slot. A second hop is the documented limit, not silent undercount.
    for entry in sorted(funcs):
        targets = call_map.get(entry)
        if not targets or not targets & set(forwarders):
            continue
        size = funcs[entry][0]
        code = rd(entry, size)
        if code is None:
            continue
        ins = list(md.disasm(code, entry))
        for f in sorted(targets & set(forwarders)):
            for G in sorted(forwarders[f]):
                hs, _fw, un, _ns = _resolve_sites(
                    ins, lambda t, _f=f, _G=G: _G if t == _f else None, is_code)
                for h, (src, site, via) in hs.items():
                    hits[h].append((entry, site, f))
                    if h not in sources:
                        sources[h] = "forwarded"
                unresolved += un
    return hits, sources, unresolved, sites


def handled_ids(md, rd, funcs, va, base_lo=0, base_hi=0):
    """Pass 2. Decode the sub/cmp chain on msg->id. Returns (ids, note)."""
    if va not in funcs:
        return None, "not a known function entry"
    size = funcs[va][0]
    code = rd(va, min(size, 0x400))
    if code is None:
        return None, "body not on disk"
    ins = list(md.disasm(code, va))
    # find `mov <r32>, dword ptr [rdx]` - the id load
    acc_reg, start = None, None
    for n, i in enumerate(ins):
        if i.mnemonic == "mov" and len(i.operands) == 2:
            dst, src = i.operands
            if (dst.type == X86_OP_REG and src.type == X86_OP_MEM and src.value.mem.disp == 0
                    and src.value.mem.index == 0 and i.op_str.endswith("[rdx]")):
                acc_reg, start = i.reg_name(dst.value.reg), n + 1
                break
    if acc_reg is None:
        # SHAPE C, the memory-operand compare (OPUS-REQ-UI-UNPARSED-HANDLERS, ruled 2026-09-20):
        # fifteen of the 24 UNPARSED handlers never load the id into a register at all - they
        # compare `dword ptr [rdx]` against an immediate directly and jump to the arm (`je`) or
        # the fallthrough (`jne`, usually the 005C5230 default stub). rdx is still the message
        # pointer, so `cmp [rdx], K` is exactly "if (msg->id == K)" - an equality test, hence
        # exact by the same argument as _equality_ids. 0023E400, 002445D0, 00290FF0, 002BE490
        # and 0056F410 verified byte-wise before this was written.
        ids = _memcmp_ids(ins)
        if ids:
            return ids, None
        return None, "no `mov r32, [rdx]` and no `cmp dword ptr [rdx], imm` in the first %d bytes" % min(size, 0x400)

    # Shape B, the dense jump table:  dec eax / sub eax,N ; cmp eax,K ; ja default ; jmp [table]
    # This is the shape 0023BD40 uses, and an early version of this tool called it "no compare
    # chain" - i.e. reported a handler that answers eighteen messages as unreadable. The dense
    # form is not a fallback for the chain form; it is the form the LARGE handlers use, so
    # omitting it lost exactly the handlers most worth reading.
    # A handler may use BOTH shapes: 0055CD40 tests `cmp eax,0x11D / je` for one outlier id and
    # THEN falls into a 23-arm dense switch. Decoding either alone reports a subset - the first
    # version of this tool listed that handler as answering exactly one message, id 285, when it
    # answers 285 plus most of 1..23. So both run and the results are unioned.
    dense = _dense_range(md, rd, ins, start, acc_reg, base_lo, base_hi)
    eq_ids = _equality_ids(ins, start, acc_reg)
    if dense is not None:
        d_ids, exact = dense
        merged = sorted(set(d_ids) | set(eq_ids))
        return merged, (None if exact else "UPPER BOUND - switch table arms not resolved")

    ids, run = [], 0
    for i in ins[start:start + 40]:
        if i.mnemonic in ("sub", "cmp") and len(i.operands) == 2:
            a, b = i.operands
            if a.type == X86_OP_REG and i.reg_name(a.value.reg) == acc_reg and b.type == X86_OP_IMM:
                if i.mnemonic == "sub":
                    run += b.value.imm
                    ids.append(("sub", run))
                else:
                    ids.append(("cmp", run + b.value.imm))
                continue
        if i.mnemonic in ("je", "jne", "jz", "jnz", "jmp", "ja", "jb"):
            continue
        if i.mnemonic in ("nop", "test", "mov", "movzx", "movsxd", "lea", "xor"):
            continue
        break
    if not ids:
        # The mov match can still be wrong - 0057E610 does `cmp [rdx],1` first, then repoints
        # rdx and a later `mov rax,[rdx]` reads as the id load. Fall back to shape C before
        # reporting failure.
        mc = _memcmp_ids(ins)
        if mc:
            return mc, None
        return None, "id loaded into %s but no compare chain and no dense table followed" % acc_reg
    return sorted(set(v for _, v in ids)), None


def _equality_ids(ins, start, acc_reg):
    """Every unambiguous equality test against the id register, honouring the running accumulator.

    `sub acc,N` shifts the origin; `cmp acc,K` + `je`/`jne` then names id `run+K`. This is exact -
    an equality test can only be one id - so these are safe to union with anything else.
    """
    run, out = 0, []
    for i in ins[start:start + 40]:
        m, ops = i.mnemonic, i.operands
        if m == "dec" and ops and ops[0].type == X86_OP_REG and i.reg_name(ops[0].value.reg) == acc_reg:
            run += 1
        elif len(ops) == 2 and ops[0].type == X86_OP_REG and                 i.reg_name(ops[0].value.reg) == acc_reg and ops[1].type == X86_OP_IMM:
            if m == "sub":
                run += ops[1].value.imm
                out.append(run)
            elif m == "cmp":
                out.append(run + ops[1].value.imm)
        elif m in ("call", "ret"):
            break
    return out


def _memcmp_ids(ins):
    """Every `cmp dword ptr [rdx], imm` in the body names one message id exactly.

    Same discipline as _equality_ids: an equality test can only be one id, so the union of
    immediates is the handler's id set. Requires disp 0, no index - `[rdx+8]` is a different
    field and must not count. Returns sorted distinct ids.
    """
    out = set()
    for i in ins:
        if i.mnemonic != "cmp" or len(i.operands) != 2:
            continue
        a, b = i.operands
        if (a.type == X86_OP_MEM and a.size == 4 and a.value.mem.disp == 0
                and a.value.mem.index == 0
                and i.op_str.split(",")[0].strip().endswith("[rdx]")
                and b.type == X86_OP_IMM):
            out.add(b.value.imm)
    return sorted(out)


def _dense_range(md, rd, ins, start, acc_reg, base_lo, base_hi):
    """`dec`/`sub imm` then `cmp acc,K` then `ja` then an indirect `jmp` through a 4-byte table.

    **All four parts are required.** A first version accepted `cmp` + any `ja` within 120
    instructions and reported `0023B6F0` - a five-arm chain whose ids were read by hand as
    1,4,10,12,13 - as answering ids 2 and 3, because a distant unrelated `ja` bound to a `cmp` from
    the middle of the chain. A relaxed pattern does not degrade to a weaker answer; it produces a
    confident wrong one.

    Arms equal to the `ja` target are the default and are dropped, so a 23-slot table with five
    dead rows reports 18 live ids. If the arm table cannot be read the range is an UPPER BOUND
    (`exact=False`).
    """
    off, bound, ja_target = 0, None, None
    k = start
    # part 1-3: the offset adjustment and the bound check, tightly, right after the id load
    while k < min(start + 14, len(ins)):
        i = ins[k]
        m, ops = i.mnemonic, i.operands
        if m == "dec" and ops and ops[0].type == X86_OP_REG and i.reg_name(ops[0].value.reg) == acc_reg:
            off += 1
        elif m == "sub" and len(ops) == 2 and ops[0].type == X86_OP_REG and                 i.reg_name(ops[0].value.reg) == acc_reg and ops[1].type == X86_OP_IMM:
            off += ops[1].value.imm
        elif m == "cmp" and len(ops) == 2 and ops[0].type == X86_OP_REG and                 i.reg_name(ops[0].value.reg) == acc_reg and ops[1].type == X86_OP_IMM:
            # A `cmp` counts only when the NEXT branch is the unsigned-above escape. Other
            # `cmp`/`je` pairs are equality tests and belong to `_equality_ids`; skipping past
            # them rather than stopping is what lets 0055CD40 be read, where `cmp eax,0x11D / jg`
            # for one outlier id precedes the real 23-arm switch.
            for j in range(k + 1, min(k + 3, len(ins))):
                mj = ins[j].mnemonic
                if mj in ("ja", "jae", "jnbe") and ins[j].operands and                         ins[j].operands[0].type == X86_OP_IMM:
                    bound, ja_target = ops[1].value.imm, ins[j].operands[0].value.imm
                    break
            if bound is not None:
                break
        elif m in ("mov", "movzx", "movsxd", "nop", "lea", "xor", "test", "push", "cdqe"):
            pass
        elif m[0] == "j":
            pass
        else:
            break
        k += 1
    if bound is None or ja_target is None:
        return None
    n = bound + 1
    if not (1 <= n <= 64):
        return None

    # part 4: the indirect jump through a dword table. Required.
    tbl_base = tbl_disp = None
    for i in ins[k:k + 200]:
        m, ops = i.mnemonic, i.operands
        if m == "lea" and len(ops) == 2 and ops[1].type == X86_OP_MEM and                 ops[1].value.mem.base == X86_REG_RIP:
            tbl_base = i.address + i.size + ops[1].value.mem.disp
        elif m == "mov" and len(ops) == 2 and ops[1].type == X86_OP_MEM and                 ops[1].value.mem.index != 0 and ops[1].value.mem.scale == 4 and tbl_base is not None:
            tbl_disp = ops[1].value.mem.disp
        elif m == "jmp" and ops and ops[0].type == X86_OP_REG:
            break
    if tbl_disp is None:
        return None

    ids = list(range(off, off + n))
    raw = rd(tbl_base + tbl_disp, n * 4)
    if raw is not None and len(raw) == n * 4:
        arms = [tbl_base + struct.unpack_from("<I", raw, j * 4)[0] for j in range(n)]
        if all(base_lo <= x < base_hi for x in arms):
            live = [ids[j] for j in range(n) if arms[j] != ja_target]
            if live:
                return live, True
    return ids, False

CORE_LO, CORE_HI = 0x00244000, 0x00249000


def find_senders(md, rd, funcs):
    """Pass 3 - who SENDS each message.

    Two record shapes, and both are required:

        mov  dword ptr [rsp+0x20], 1     ; built on the stack
        lea  rdx, [rsp+0x20]
        call rax                          ; rax = [obj], the handler

        lea  rdx, [rip + ...]             ; a CONSTANT record in .rdata, e.g. 00915070 = {18,0,0}
        call rax

    **A stack-only scan reports zero senders for id 18**, which 65 % of all handlers answer.
    "Nobody sends it" was never a possible answer, so the zero meant the instrument was wrong.
    """
    census = collections.Counter()
    static = collections.Counter()
    sites = collections.defaultdict(list)
    for entry in sorted(funcs):
        size = funcs[entry][0]
        if size <= 0 or size > 0x20000:
            continue
        code = rd(entry, size)
        if code is None:
            continue
        ins = list(md.disasm(code, entry))
        pend = {}
        for n, i in enumerate(ins):
            m, ops = i.mnemonic, i.operands
            if m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM \
                    and ops[1].type == X86_OP_IMM:
                mem = ops[0].value.mem
                if mem.base and mem.index == 0 and 0 <= ops[1].value.imm <= 400 \
                        and i.op_str.startswith("dword"):
                    pend[(mem.base, mem.disp)] = ops[1].value.imm
            elif m == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and i.reg_name(ops[0].value.reg) == "rdx" and ops[1].type == X86_OP_MEM:
                mem = ops[1].value.mem
                mid, is_static = None, False
                if mem.base == X86_REG_RIP:
                    raw = rd(i.address + i.size + mem.disp, 4)
                    if raw is not None and len(raw) == 4:
                        v = struct.unpack("<I", raw)[0]
                        if 0 <= v <= 400:
                            mid, is_static = v, True
                else:
                    mid = pend.get((mem.base, mem.disp))
                if mid is None:
                    continue
                for j in range(n + 1, min(n + 7, len(ins))):
                    if ins[j].mnemonic == "call" and ins[j].operands \
                            and ins[j].operands[0].type != X86_OP_IMM:
                        census[mid] += 1
                        sites[mid].append((entry, ins[j].address))
                        if is_static:
                            static[mid] += 1
                        break
    return census, static, sites


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--out", default=None)
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--senders", action="store_true",
                    help="also run pass 3: who sends each message")
    a = ap.parse_args()

    d, base, secs = load_pe(a.exe)
    rd = reader(d, base, secs)
    text = next((s for s in secs if s[0] == ".text"), None)
    lo, hi = base + text[1], base + text[1] + text[2]

    def is_code(va):
        return lo <= va < hi

    funcs = load_functions(a.funcs)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    hits, sources, unresolved, sites = find_handlers(md, rd, funcs, is_code)
    print("PASS 1 - handler recovery, on the proc-slot rule")
    print("  constructor transfer sites (call + jmp)  : %d" % sites)
    print("  sites resolved to a `lea` def            : %d" % (sites - len(unresolved)))
    print("  sites NOT fully resolved                 : %d" % len(unresolved))
    src_counts = collections.Counter(sources.values())
    print("  WIDGET PROCEDURES (reach a proc slot)    : %d" % len(hits))
    print("    " + "  ".join("%s %d" % (k, src_counts[k]) for k in
          ("direct", "tail", "multi", "forwarded") if src_counts[k]))
    print()

    # CONTROL - the verified terms of the corrected population (CONTRACT-widget-object.md §15b).
    # OPUS derived 267 = 251 - 5 + 14 + 7 by hand on 2026-09-13; this instrument must reproduce
    # every one of those terms from the image alone.
    got = set(hits)
    miss_add = sorted(EXPECTED_ADD - got)
    bad_rem = sorted(EXPECTED_REM & got)
    print("  CONTROL vs the verified §15b terms")
    print("    expected additions found   : %d/%d%s" % (
        len(EXPECTED_ADD) - len(miss_add), len(EXPECTED_ADD),
        "" if not miss_add else "  MISSING: " + " ".join("%08X" % x for x in miss_add)))
    print("    expected removals absent   : %d/%d%s" % (
        len(EXPECTED_REM) - len(bad_rem), len(EXPECTED_REM),
        "" if not bad_rem else "  STILL PRESENT: " + " ".join("%08X" % x for x in bad_rem)))
    print()

    everyone = dict((h, sources.get(h, "direct")) for h in hits)

    exact, bounded, unparsed = {}, {}, []
    for h in sorted(everyone):
        ids, note = handled_ids(md, rd, funcs, h, lo, hi)
        if ids is None:
            unparsed.append((h, note))
        elif note:
            bounded[h] = ids
        else:
            exact[h] = ids

    n = len(everyone)
    # The population is the set of addresses a `lea` def carries into a proc slot - one set now,
    # no confirmed/candidate split. `multi` handlers share a transfer site with a sibling (a
    # branch chose between them); `forwarded` handlers arrive through the one permitted hop.
    print("PASS 2 - message ids answered  (population %d)" % n)
    print("  EXACT   - chain decoded, or table arms resolved : %d" % len(exact))
    print("  BOUNDED - dense switch, arms unresolved         : %d  (upper bounds, NOT counted below)"
          % len(bounded))
    print("  UNPARSED- shape not readable by this tool       : %d" % len(unparsed))
    print()
    census = collections.Counter()
    for ids in exact.values():
        for v in ids:
            census[v] += 1
    print("  id   handlers answering it   (denominator: the %d EXACT handlers)" % len(exact))
    for v, c in sorted(census.items()):
        print("  %4d   %4d  %5.1f %%  %s" % (v, c, 100.0 * c / len(exact), "#" * min(c, 50)))
    print()
    sizes = collections.Counter(len(v) for v in exact.values())
    print("  ids answered per EXACT handler: " + ", ".join("%d ids x%d" % (k, m)
                                                          for k, m in sorted(sizes.items())))
    if a.show:
        print("\n  samples")
        for h in sorted(exact)[:a.show]:
            print("    %08X  exact    %s" % (h, exact[h]))
        for h in sorted(bounded)[:a.show]:
            print("    %08X  <= %s" % (h, bounded[h]))
        for h, note in unparsed[:a.show]:
            print("    %08X  UNPARSED: %s" % (h, note))

    if a.senders:
        census3, static3, sites3 = find_senders(md, rd, funcs)
        print()
        print("PASS 3 - who sends each message")
        print("  send sites found: %d, distinct ids: %d" % (sum(census3.values()), len(census3)))
        print("  (far fewer sites than handlers: most delivery goes through broadcast helpers,")
        print("   so one site can reach every node in a subtree)")
        print()
        print("  id   sites  fns  static  in core  outside  origin")
        for v in sorted(census3):
            fns = set(x for x, _ in sites3[v])
            inn = sum(1 for x in fns if CORE_LO <= x < CORE_HI)
            out = len(fns) - inn
            origin = "FRAMEWORK" if inn and not out else ("application" if not inn else "both")
            print("  %4d  %5d %4d  %6d  %7d  %7d  %s"
                  % (v, census3[v], len(fns), static3[v], inn, out, origin))
        print()
        print("  widget core = %08X-%08X. No id above 25 has a sender inside it."
              % (CORE_LO, CORE_HI))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("handler\tname\tbody_bytes\tsites\tsource\tkind\tids\tnote\n")
            un = dict(unparsed)
            for h in sorted(everyone):
                nm = funcs.get(h, (0, "?", ""))
                if h in exact:
                    kind, ids, note = "exact", exact[h], ""
                elif h in bounded:
                    kind, ids, note = "upper-bound", bounded[h], "switch arms not resolved"
                else:
                    kind, ids, note = "unparsed", [], un.get(h, "")
                f.write("%08X\t%s\t%d\t%d\t%s\t%s\t%s\t%s\n" % (
                    h, nm[1], nm[0], len(hits.get(h, ())), everyone[h], kind,
                    ",".join(str(v) for v in ids), note))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
