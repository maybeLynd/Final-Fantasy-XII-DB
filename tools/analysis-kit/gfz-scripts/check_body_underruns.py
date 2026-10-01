"""check_body_underruns.py - listed bodies whose own control flow reaches past functions.tsv's body_bytes (OPUS, 2026-09-29).

The underrun sibling of check_extent_overruns.py, and the re-derivation of
`99-Unresolved-Residual/Unlisted-Code/listed-bodies-with-code-past-body-bytes.tsv` (177 bodies, 2,564 bytes; 2026-09-21).

WHY IT EXISTS. Re-reading that page for its status (FABLE's status-currency rule, 2026-09-29) found its walk reaching code
the function cannot reach: `00148F10` was listed 539 bytes past its end, although the instruction at its recorded end is
`repz ret`, and `00862022` (a 6-byte `jmp qword ptr [rip+x]`) was said to reach the next thunk. A walk that tests the
mnemonic for exactly "ret", or lets an indirect jump fall through, reads a terminated body as continuing.

THE WALK, from each listed entry over [entry, next listed entry):
  terminators    every ret form (ret, repz ret, rep ret, retf), int3, ud2, hlt; a call to a function flagged noreturn
  jmp direct     follow the target only (no fall-through); a target outside the window is not followed
  jmp indirect   follow the arms ONLY when it is the image-base-relative table this image uses -
                   cmp idx, N ; ja ... ; mov r32, dword [rBase + idx*4 + disp] ; add rX, rBase ; jmp rX
                 with rBase loaded as the image base; N+1 arms at BASE + disp. Otherwise the path ends.
  jcc / call     both successors (call falls through unless the callee is noreturn)
Truncation = end of the last reachable NON-PADDING instruction beyond entry + body_bytes (body_bytes excludes the int3
tail by convention).

CONTROL: 0037C3F0 (FABLE's case: 11 arms, 9 past the recorded end, code to 0037C6C3) must be found truncated; 00148F10
and 00862022 must NOT be (their recorded ends are terminators).

    python check_body_underruns.py [--compare <old tsv>] [--out <tsv>]
"""
import argparse, bisect, io, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
TERM = {"ret", "retf", "int3", "ud2", "hlt"}


def load():
    blob = io.open(EXE, "rb").read()
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    secs = [(base + s.VirtualAddress, s.SizeOfRawData, s.PointerToRawData) for s in pe.sections]
    rows = {}
    with io.open(FUNCS, encoding="utf-8", errors="replace") as f:
        h = f.readline().rstrip("\n").split("\t")
        ie, inm, isz, inr = h.index("entry"), h.index("name"), h.index("body_bytes"), h.index("noreturn")
        for l in f:
            c = l.rstrip("\n").split("\t")
            try:
                rows[int(c[ie], 16)] = (c[inm], int(c[isz]), c[inr] == "true")
            except (ValueError, IndexError):
                pass
    return blob, base, secs, rows


def walk(blob, base, secs, rows, entries, e, md):
    """(code_end, jump_table_arms) for the listed entry e, or None when it cannot be decoded."""
    k = bisect.bisect_right(entries, e)
    hi = entries[k] if k < len(entries) else e + 0x10000
    off = next((raw + (e - st) for st, sz, raw in secs if st <= e < st + sz), None)
    if off is None:
        return None
    code = blob[off:off + (hi - e)]
    ins = {x.address: x for x in md.disasm(code, e)}
    order = sorted(ins)
    nxt = {a: order[i + 1] if i + 1 < len(order) else None for i, a in enumerate(order)}
    noret = {a for a, r in rows.items() if r[2]}
    seen, stack, arms = set(), [e], 0
    while stack:
        a = stack.pop()
        if a in seen or a not in ins or not (e <= a < hi):
            continue
        seen.add(a)
        x = ins[a]
        m = x.mnemonic
        if m in TERM or m.endswith(" ret") or m.startswith("ret"):
            continue
        if m == "jmp":
            op = x.operands[0]
            if op.type == X86_OP_IMM:
                stack.append(op.imm)
            elif op.type == X86_OP_REG:
                t = table(ins, order, a, base, blob, secs, x)
                if t:
                    arms += len(t)
                    stack.extend(t)
            continue                                    # an indirect jmp through memory ends the path
        if m.startswith("j"):                            # jcc
            if x.operands and x.operands[0].type == X86_OP_IMM:
                stack.append(x.operands[0].imm)
            stack.append(nxt[a])
            continue
        if m == "call" and x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm in noret:
            continue
        stack.append(nxt[a])
    real = [a for a in seen if ins[a].mnemonic not in ("int3", "nop")]
    if not real:
        return None
    last = max(real)
    return last + ins[last].size, arms


def table(ins, order, a, base, blob, secs, jx):
    """Arms of `mov r32,[rB+idx*4+disp]; add rX,rB; jmp rX` with a `cmp idx,N; ja` bound and rB = image base, else None."""
    i = order.index(a)
    win = [ins[order[j]] for j in range(max(0, i - 10), i)]
    reg = jx.op_str
    mov = next((x for x in reversed(win) if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_MEM
                and x.operands[1].mem.scale == 4 and x.operands[1].mem.disp > 0), None)
    add = next((x for x in reversed(win) if x.mnemonic == "add" and x.op_str.startswith(reg + ",")), None)
    cmp_ = next((x for x in reversed(win) if x.mnemonic == "cmp" and len(x.operands) == 2 and x.operands[1].type == X86_OP_IMM), None)
    if not (mov and add and cmp_):
        return None
    disp, n = mov.operands[1].mem.disp, cmp_.operands[1].imm + 1
    if not (0 < n <= 4096):
        return None
    tva = base + disp
    off = next((raw + (tva - st) for st, sz, raw in secs if st <= tva < st + sz), None)
    if off is None:
        return None
    return [base + struct.unpack_from("<I", blob, off + 4 * j)[0] for j in range(n)]


def run(compare=None, out=None):
    blob, base, secs, rows = load()
    entries = sorted(a for a, r in rows.items() if not r[0].startswith(("Unwind@", "Catch_All@")) and r[1] > 0)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    found = {}
    for e in entries:
        r = walk(blob, base, secs, rows, entries, e, md)
        if r and r[0] > e + rows[e][1]:
            found[e] = (r[0], r[0] - (e + rows[e][1]), r[1])
    ctrl = {"0037C3F0 truncated (FABLE's case)": 0x0037C3F0 in found and found[0x0037C3F0][0] >= 0x0037C6C3,
            "00148F10 not truncated (repz ret at its end)": 0x00148F10 not in found,
            "00862022 not truncated (jmp [mem] thunk)": 0x00862022 not in found}
    for k, v in ctrl.items():
        print("%s  control: %s" % ("PASS" if v else "FAIL", k))
    print("truncated bodies: %d, bytes beyond: %d, with a jump table: %d" % (
        len(found), sum(v[1] for v in found.values()), sum(1 for v in found.values() if v[2])))
    if compare:
        old = {}
        for l in io.open(compare, encoding="utf-8"):
            if l.startswith(("#", "entry")) or not l.strip():
                continue
            c = l.rstrip("\n").split("\t")
            old[int(c[0], 16)] = int(c[4])
        both = set(old) & set(found)
        print("recorded list %d: confirmed %d, not reproduced %d (recorded bytes %d), new %d" % (
            len(old), len(both), len(set(old) - set(found)), sum(old[e] for e in set(old) - set(found)), len(set(found) - set(old))))
        for e in sorted(set(old) - set(found))[:12]:
            print("   not reproduced %08X (recorded %d beyond)" % (e, old[e]))
    if out:
        with io.open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Listed bodies whose own control flow reaches past functions.tsv's body_bytes - check_body_underruns.py (OPUS, 2026-09-29).\n")
            f.write("# Terminators include every ret form and indirect jmp; tables followed only when image-base-relative and bounded.\n")
            f.write("entry\tname\tbody_bytes\tcode_ends\tbytes_beyond\tjump_table_arms\n")
            for e in sorted(found):
                f.write("%08X\t%s\t%d\t%08X\t%d\t%d\n" % (e, rows[e][0], rows[e][1], found[e][0], found[e][1], found[e][2]))
    return 0 if all(ctrl.values()) else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--compare"); ap.add_argument("--out")
    a = ap.parse_args()
    sys.exit(run(a.compare, a.out))
