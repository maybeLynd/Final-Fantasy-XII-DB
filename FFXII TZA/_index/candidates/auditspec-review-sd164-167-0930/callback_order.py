"""callback_order.py - SWE2-AUDIT-SPEC (2026-09-30): H2 of sd164-167 re-derived from the bytes with arena_ix only.
  O1 0036BFE0: the +0xA0 callback is called before the 0036BC60 attempt, and the retry edge goes back above it.
  O2 each caller of 0036BFE0 (raw E8/E9/jcc): does a direct 0036BC60 attempt + null test precede the call?
  O3 002E6900 (the callback's gate): every `ret` in its body is preceded by `xor eax, eax` (so it always returns 0).
  O4 002E6D60: which paths deliver (0041E490) and free (002E9360) the 0215FD88 tail node.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arena_ix as X  # noqa: E402


def body(a, b):
    return X.dis(a, b)


def show(i):
    return "%08X %s %s" % (i.address, i.mnemonic, i.op_str)


A = body(0x0036BFE0, 0x0036C0E5)
cb = [i for i in A if i.mnemonic == "call" and i.op_str == "rax"]
at = [i for i in A if i.mnemonic == "call" and i.op_str == "0x36bc60"]
back = [i for i in A if i.mnemonic.startswith("j") and i.op_str == "0x36c013"]
print("O1 callback call %s; attempt %s; retry edges to 0036C013 (above the callback): %s" % (
    [show(i) for i in cb], [show(i) for i in at], [show(i) for i in back]))
print("   order callback-before-attempt: %s" % (cb[0].address < at[0].address and all(0x0036C013 < cb[0].address for _ in [0])))

r = X.rel32([0x0036BFE0])[0x0036BFE0]
for s, k in sorted(r):
    f = X.root(s)
    ins = [i for i in X.dis(f, s + 5)]
    pre = [i for i in ins if i.mnemonic == "call" and i.op_str == "0x36bc60" and i.address < s]
    print("O2 caller %08X (%s, root %08X): direct 0036BC60 attempt before it: %s" % (s, k, f, [show(i) for i in pre] or "NONE"))
    for i in ins[-12:]:
        print("      " + show(i))

G = []
for e in X.PD:
    if 0x002E6900 - X.IB <= e[0] < 0x002E6A7A - X.IB:
        G += X.dis(X.IB + e[0], X.IB + e[1])
G = sorted({i.address: i for i in G}.values(), key=lambda i: i.address)
rets = [(G[k - 1], G[k]) for k in range(len(G)) if G[k].mnemonic == "ret"]
print("O3 002E6900 .pdata ranges decoded: %d instructions; rets: %s" % (len(G), [(show(a), show(b)) for a, b in rets]))
print("   rets: %d; the one exit block starts with `%s`" % (len(rets), X.txt(0x002E6A70)))
print("   (the exit block, read linearly:)")
for i in body(0x002E6A70, 0x002E6A7A):
    print("      " + show(i))
jin = [i for i in G if i.mnemonic.startswith("j") and i.op_str in ("0x2e6a70", "0x2e6a72", "0x2e6a76", "0x2e6a78", "0x2e6a79")]
print("   jumps into the exit block past 002E6A70: %s" % [show(i) for i in jin])

D = body(0x002E6D60, 0x002E6E25)
for i in D:
    if i.address in (0x002E6D66, 0x002E6D6D, 0x002E6DAC, 0x002E6DB1, 0x002E6DB3, 0x002E6DB7, 0x002E6DB9, 0x002E6DBD,
                     0x002E6DDD, 0x002E6DE7, 0x002E6DEA, 0x002E6DF6, 0x002E6DF9, 0x002E6DFE, 0x002E6E02, 0x002E6E13,
                     0x002E6E15, 0x002E6E19, 0x002E6E1E):
        print("O4 " + show(i))
