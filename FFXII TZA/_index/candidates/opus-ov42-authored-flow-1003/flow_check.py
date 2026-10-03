"""flow_check.py - the bridge facts OPUS re-read before consuming SWE2-DATA's authored getspattackskillinfo ->
spattackread flow (OPUS, 2026-10-03; ASTRA-REQ-OPUS-OV42-AUTHORED-FLOW-CONSUME-1003). Rejecting regression over the
shipping image through retool.py: each check names an instruction at fn + off and the text it must hold. The script
side (the three call sites in spc_z0000.ebp) rests on SWE2-DATA's prove_spattack_flow.py and SWE2-AUDIT-SPEC's
independent decode; it is not repeated here. Last line 'FAILS n'."""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool  # noqa: E402

R = retool.R
fails = 0


def ins(fn, off):
    a = fn + off
    i = next(R.md.disasm(R.at(a, 16), a), None)
    return "" if i is None else "%s %s" % (i.mnemonic, i.op_str)


def check(fn, off, want, what):
    global fails
    got = ins(fn, off)
    ok = all(w in got for w in want)
    print("%s  %08X + 0x%X  %-36s %s" % ("PASS" if ok else "FAIL", fn, off, got, what))
    fails += 0 if ok else 1


# 029A bridge 00348330: one context, first pop -> RDX (action), second pop -> RCX (unit), then the writer
check(0x348330, 0x1A, ["call 0x2640c0"], "the context, read once")
check(0x348330, 0x22, ["mov rbx, rax"], "context kept in RBX")
check(0x348330, 0x33, ["call 0x2650b0"], "first pop decoded")
check(0x348330, 0x3B, ["mov rsi, rax"], "first destination kept in RSI")
check(0x348330, 0x4C, ["call 0x2650b0"], "second pop decoded, same context")
check(0x348330, 0x51, ["mov rdx, rsi"], "RDX = first pop = action destination")
check(0x348330, 0x54, ["mov rcx, rax"], "RCX = second pop = unit destination")
check(0x348330, 0x5A, ["call 0x309c00"], "the writer")
# 029B bridge 00348870: first pop -> EDX (action), second -> ECX (unit)
check(0x348870, 0x10, ["call 0x267e10"], "first pop")
check(0x348870, 0x18, ["mov ebx, eax"], "first value kept")
check(0x348870, 0x1F, ["mov edx, ebx"], "EDX = first pop = action word")
check(0x348870, 0x21, ["mov ecx, eax"], "ECX = second pop = unit")
check(0x348870, 0x23, ["call 0x30eea0"], "the reader")
# reference decoder, class 1 ('file'): [ctx + 0x40] + low 24 bits
check(0x2650FC, 0x00, ["mov rcx, qword ptr [r9 + 0x40]"], "file-class base")
check(0x2650FC, 0x06, ["and eax, 0xffffff"], "24-bit offset")
check(0x2650FC, 0x0B, ["add rax, rcx"], "base + offset")
print("FAILS %d" % fails)
