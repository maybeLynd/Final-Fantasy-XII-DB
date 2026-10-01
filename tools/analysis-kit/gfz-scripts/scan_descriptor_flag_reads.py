#!/usr/bin/env python3
"""scan_descriptor_flag_reads.py - which bits of a descriptor's +0xFC are ever READ.

Sibling of scan_descriptor_flag_bits.py, which censuses the WRITES. Named `scan_` for the same
reason: run_gates.py collects `check_*` and this takes minutes.

Which bits of a descriptor's +0xFC are ever READ, tied to a descriptor.

The write census (scan_descriptor_flag_bits.py) found bits 1, 27, 28, 29, 30 and 31 set and bit 3
never set. Writes alone do not say whether a bit does anything. Bits 27 and 28 are written by
00639C80, the layout validation, and nothing so far shows anyone consuming them - if nobody does,
that validation is a fourth disarmed arm and the pattern covers the whole validation half.

METHOD. Same descriptor taint. On every tainted path, find
  * a direct examination of the memory: `test/cmp/bt [desc+0xFC], imm`
  * or a LOAD of it into a register, which is then followed until something consumes it:
    `bt r,imm`, `test r,imm`, `and r,imm`, `test r,r` + a sign branch, `cmp`, `shr`.
Every consuming instruction is printed verbatim rather than reduced to a bit number, because the
reduction is where a reader would start guessing.

CONTROLS - five reads this project has already established, across three functions:
    0063A99A  test byte ptr [r8+0xfc], 8        bit 3, PCluster::create's refusal
    0063C93D  test eax,eax (+ js)               bit 31, 0063C910
    0063C941  bt eax, 0x1e                      bit 30, 0063C910
    0063BC19  test eax,eax (+ js)               bit 31, 0063BC00
    00639AB6  test bl, 1  / 00639AF1 test bl,2  bits 0 and 1, 00639A60 after `and ebx,0x7ffffff`
A run that does not find these has not shown it can see a flag read. All five found,
2026-09-19 (OPUS).

THE COMPLETE READ SET, descriptor-tied, 2026-09-19 (OPUS):

    0063946F  test byte [rbx+0xFC], 1          bit 0
    0063954C  test byte [r9+0xFC], 2           bit 1
    00639A94  test ebx,ebx  (after the load)   bit 31
    00639AA1  and ebx, 0x7FFFFFF               keeps bits 0-26 for the tests below
    00639AB6  test bl, 1                       bit 0
    00639AF1  test bl, 2                       bit 1
    00639B27  shr ebx,3 ; not bl ; test bl,1   bit 3
    0063A99A  test byte [r8+0xFC], 8           bit 3, PCluster::create's refusal
    0063BC19  test eax,eax   0063BC1D bt eax,0x1e    bits 31 and 30
    0063C93D  test eax,eax   0063C941 bt eax,0x1e    bits 31 and 30
    0063C9C0  movzx r12d, byte [r13+0xFC] ; not r12b  the low byte

PUT BESIDE THE WRITE CENSUS, ONLY THREE BITS ARE BOTH WRITTEN AND READ:

    bit   written            read              verdict
    0     never              3 sites           READ-ONLY - the arm it gates cannot run
    1     315 ctors          3 sites           live
    3     never              3 sites           READ-ONLY - PCluster::create's refusal is dead
    27    00639EEF           never             WRITE-ONLY - the validation's answer, discarded
    28    0063A0E2           never             WRITE-ONLY - the validation's answer, discarded
    29    0063BC49           never             WRITE-ONLY - "pointer handed out", nobody asks
    30    00639465           2 sites           live
    31    00639C55           3 sites           live

So the validation half of the class-descriptor system is disarmed AT BOTH ENDS: the arms that
would report are unreachable because their bits are never set, and the results that do get
computed land in bits nobody reads.

BOUNDARY, the same as the write census: indirect calls are not followed, nor a descriptor parked
in memory and reloaded with no lea on the path. "Never read on a descriptor-tied path" is the
claim, not "never read".
"""
import collections
import sys

sys.path.insert(0, "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
import check_default_instance_writers as W  # noqa: E402
import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
FLAG = 0xFC
CONSUME = ("test", "bt", "and", "cmp", "shr", "or", "xor", "movzx", "not", "btr", "bts")


def scan(img, entry, seed_regs, seed_values=None):
    t = W.Taint(img)
    starts, blocks, succ = t._blocks(entry)
    if not starts:
        return [], set()
    size = img.sizes.get(entry, 0)
    out, forwards = [], set()
    state = {starts[0]: (frozenset(seed_regs), frozenset())}
    work = collections.deque([starts[0]])
    n = 0
    while work and n < 20000:
        n += 1
        b = work.popleft()
        regs, flagw = (set(x) for x in state[b])
        for i in blocks[b]:
            m = i.mnemonic
            # direct examination of the memory operand
            for o in i.operands:
                if (o.type == X86_OP_MEM and o.value.mem.disp == FLAG
                        and not o.value.mem.index
                        and W.norm(o.value.mem.base) in regs and m in CONSUME):
                    out.append((i.address, "mem", m, i.op_str))
            # a consumer of a register that holds the flag word
            if flagw and m in CONSUME:
                for o in i.operands:
                    if o.type == X86_OP_REG and W.norm(o.reg) in flagw:
                        out.append((i.address, "reg", m, i.op_str))
                        break
            # load of the flag word into a register
            if (m in ("mov", "movzx") and len(i.operands) == 2
                    and i.operands[0].type == X86_OP_REG
                    and i.operands[1].type == X86_OP_MEM
                    and i.operands[1].value.mem.disp == FLAG
                    and not i.operands[1].value.mem.index
                    and W.norm(i.operands[1].value.mem.base) in regs):
                flagw.add(W.norm(i.operands[0].reg))
                continue
            v = W.lea_value(i)
            if v is not None:
                d = W.norm(i.operands[0].reg)
                if seed_values and v in seed_values:
                    regs.add(d)
                else:
                    regs.discard(d)
                flagw.discard(d)
                continue
            if m in ("mov", "and", "shr", "or") and len(i.operands) == 2 \
                    and i.operands[0].type == X86_OP_REG:
                d = W.norm(i.operands[0].reg)
                s = i.operands[1]
                if m == "mov":
                    if s.type == X86_OP_REG and W.norm(s.reg) in regs:
                        regs.add(d)
                        flagw.discard(d)
                        continue
                    if s.type == X86_OP_REG and W.norm(s.reg) in flagw:
                        flagw.add(d)
                        regs.discard(d)
                        continue
                    regs.discard(d)
                    flagw.discard(d)
                    continue
                if d in flagw:          # masking keeps it the flag word
                    continue
            if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                tgt = i.operands[0].imm
                if not (entry <= tgt < entry + size) and tgt in img.sizes:
                    for k, ar in enumerate(W.ARG_REGS):
                        if ar in regs:
                            forwards.add((tgt, k + 1))
                if m == "call":
                    regs -= W.VOLATILE
                    flagw -= W.VOLATILE
                continue
            if m == "call":
                regs -= W.VOLATILE
                flagw -= W.VOLATILE
                continue
            try:
                _r, w = i.regs_access()
            except capstone.CsError:
                w = []
            for r in w:
                regs.discard(W.norm(r))
                flagw.discard(W.norm(r))
        o = (frozenset(regs), frozenset(flagw))
        for s in succ[b]:
            prev = state.get(s)
            if prev is None:
                state[s] = o
                work.append(s)
            else:
                mg = tuple(a | c for a, c in zip(prev, o))
                if mg != prev:
                    state[s] = mg
                    work.append(s)
    return out, forwards


def main():
    img = W.Image()
    descs = W.store_descriptors(W.G.DB) | set(W.enumerate_descriptors(img))
    hosts = [e for e in img.sizes
             if any(W.lea_value(i) in descs for i in img.body(e) if i.mnemonic == "lea")]
    reads, seen, work = [], set(), collections.deque()
    for e in hosts:
        r, f = scan(img, e, set(), seed_values=descs)
        reads += [(e,) + x for x in r]
        for g in f:
            if g not in seen:
                seen.add(g)
                work.append((g[0], g[1], 0))
    while work:
        fn, slot, d = work.popleft()
        r, fw = scan(img, fn, {W.ARG_REGS[slot - 1]})
        reads += [(fn,) + x for x in r]
        if d >= 12:
            continue
        for g in fw:
            if g not in seen:
                seen.add(g)
                work.append((g[0], g[1], d + 1))
    byfn = collections.defaultdict(list)
    for host, addr, kind, m, ops in sorted(set(reads), key=lambda x: x[1]):
        byfn[host].append((addr, kind, m, ops))
    print("descriptor-tied examinations of +0xFC: %d, in %d function(s)"
          % (sum(len(v) for v in byfn.values()), len(byfn)))
    for fn in sorted(byfn):
        print("  %08X %s" % (fn, img.names.get(fn, "")))
        for addr, kind, m, ops in byfn[fn]:
            print("      %08X %-4s %-6s %s" % (addr, kind, m, ops))
    got = {a for v in byfn.values() for a, _k, _m, _o in v}
    print()
    for a, what in ((0x0063A99A, "bit 3, PCluster::create refusal"),
                    (0x0063C93D, "bit 31, 0063C910"),
                    (0x0063C941, "bit 30, 0063C910"),
                    (0x0063BC19, "bit 31, 0063BC00"),
                    (0x00639AB6, "bit 0, 00639A60")):
        print("CONTROL %08X %-34s %s" % (a, what, "FOUND" if a in got else "MISSING"))


if __name__ == "__main__":
    main()
