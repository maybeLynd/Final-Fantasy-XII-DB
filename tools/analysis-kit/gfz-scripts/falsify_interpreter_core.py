"""falsify_interpreter_core.py - falsification pass 1 on 01-Script-VM-Native-Bridge/CONTRACT-interpreter-core.md
(OPUS, 2026-09-30). Static; reads only the shipping image.

The interpreter facts the contract shares with the script-resume page are re-run from falsify_script_resume.py (R1-R10);
this adds the contract's own clauses:
K1  §2 the interpreter is 14,646 bytes
K2  §2 the evaluation stack's extent is 0x284: the lifecycle writes four 64-entry arrays at +0x04 (byte), +0x44 (byte),
    +0x84 (dword) and +0x184 (dword), so the last byte is +0x283
K3  I5 opcode 00's table entry is the plain advance (length 0: the PC does not move) and opcode 01's is the stop entry
K4  I6 opcodes above 0x63 still reach the opcode-indexed length lookup: the advance reads the saved opcode byte, any value
K5  §3 the actor record's integer registers +0x64..+0x70 and float registers +0x74..+0x80 are addressed by the interpreter
K6  §7 REQSW (0x24) and REQEW (0x27) arm wait kind 4 (byte +0x14 of the wait slot)
"""
import io, os, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext, BASE = R.at, R.md, R.ext, R.b.BASE
INTERP, LIFE = 0x0025E4C0, 0x002621D0
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


# the shared interpreter facts
r = subprocess.run([sys.executable, "-B", os.path.join(HERE, "falsify_script_resume.py")], capture_output=True, text=True)
shared = [l for l in r.stdout.splitlines() if l[:1] == "R" and l[1:3].strip().isdigit()]
for l in shared:
    cid, verdict = l.split()[0], l.split()[1]
    results.append((cid, verdict == "SURVIVES"))
    print(l[:200])

body = list(md.disasm(at(INTERP, ext[INTERP]), INTERP))
T = [BASE + struct.unpack("<I", at(0x00261DF8 + 4 * k, 4))[0] for k in range(100)]

check("K1", ext[INTERP] == 14646, "0025E4C0 extent %d B" % ext[INTERP])

lb = list(md.disasm(at(LIFE, ext[LIFE]), LIFE))
arr = sorted(set((op.mem.disp, op.size) for i in lb for op in i.operands
                 if op.type == X.X86_OP_MEM and "rbx" in (md.reg_name(op.mem.base), md.reg_name(op.mem.index) if op.mem.index else None)
                 and op.mem.index != 0 and op.mem.disp in (4, 0x44, 0x84, 0x184)))
last = max(d + 64 * s for d, s in arr) if arr else 0
check("K2", arr == [(4, 1), (0x44, 1), (0x84, 4), (0x184, 4)] and last == 0x284,
      "002621D0's indexed stack stores (displacement, width) %s -> 64 entries end at +0x%X" % (arr, last))

check("K3", T[0] == 0x0025E613 and T[1] == 0x0025E60A,
      "opcode 00 -> %08X (the advance), opcode 01 -> %08X (the stop entry, then the advance)" % (T[0], T[1]))

adv = [i for i in body if 0x0025E613 <= i.address <= 0x0025E641]
k4 = ["%s %s" % (i.mnemonic, i.op_str) for i in adv]
check("K4", k4[0] == "movzx edx, byte ptr [rsp + 0xb8]" and "movzx eax, dl" in k4 and any("word ptr [rax + rcx*8 + 0x1ddea60]" in x for x in k4),
      "the advance indexes the length rows by the saved opcode byte, unbounded: %s" % " ; ".join(k4[:6]))

regs = sorted(set(op.mem.disp for i in body for op in i.operands
                  if op.type == X.X86_OP_MEM and md.reg_name(op.mem.base) == "r15" and op.mem.disp in range(0x64, 0x84, 4)))
check("K5", regs == list(range(0x64, 0x84, 4)), "r15 (the actor record) is addressed at %s" % [hex(d) for d in regs])

starts = sorted(set(T))


def arm(a):
    end = next((s for s in starts if s > a), INTERP + ext[INTERP])
    return [i for i in body if a <= i.address < end]


def reaches_kind4(a, limit=400):
    """Follow the arm's own control flow inside the interpreter (fall-through and direct branches) until a store of
    kind 4 at +0x14 of a register base, or the budget runs out."""
    seen, work = set(), [a]
    while work and len(seen) < limit:
        x = work.pop()
        if x in seen or not (INTERP <= x < INTERP + ext[INTERP]):
            continue
        seen.add(x)
        i = R.dec(x)
        if i is None:
            continue
        if i.mnemonic == "mov" and i.op_str.startswith("byte ptr [") and i.op_str.endswith("+ 0x14], 4"):
            return "%08X %s %s" % (i.address, i.mnemonic, i.op_str)
        if i.mnemonic in ("ret",) or (i.mnemonic == "jmp" and not (i.operands and i.operands[0].type == X.X86_OP_IMM)):
            continue
        tgt = i.operands[0].imm if i.mnemonic.startswith("j") and i.operands[0].type == X.X86_OP_IMM else None
        if i.mnemonic == "jmp":
            work.append(tgt)
            continue
        work.append(i.address + i.size)
        if tgt is not None:
            work.append(tgt)
    return None


kind4 = {"REQSW 0x24": reaches_kind4(T[0x24]), "REQEW 0x27": reaches_kind4(T[0x27])}
check("K6", all(kind4.values()), "kind-4 stores in the REQSW (0x24) / REQEW (0x27) arms: %s" % kind4)

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
