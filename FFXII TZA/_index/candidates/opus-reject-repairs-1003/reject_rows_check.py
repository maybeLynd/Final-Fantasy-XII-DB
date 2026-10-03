"""reject_rows_check.py - regression for OPUS's repairs of SWE2-AUDIT-SPEC's two REJECTs at cc2da97b8 (OPUS, 2026-10-03).

For each repaired row it decodes the function from the certified image and checks every fact the repair rests on, then
checks the published row text: the repaired clause must be present and the rejected clause must be absent.
Run against the rejected texts (--rejected), it must fail both rows: that is the rejecting control."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))            # FFXII TZA/
KIT = os.path.normpath(os.path.join(DBR, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import retool  # noqa: E402

R = retool.R
CAND = os.path.join(DBR, "_index", "candidates")


def dis(start, size):
    return {i.address: (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(start, size), start)}


def row(rec, fn):
    d = json.load(io.open(os.path.join(CAND, rec, "rows.json"), encoding="utf-8"))
    return next(r["text"] for r in d["rows"] if r["fn"] == fn)


def sab(text):
    fails = []
    m = dis(0x001FB770, 0x90)
    want = {0x001FB770: ("push", "rbx"), 0x001FB772: ("sub", "rsp, 0x40"),
            0x001FB7B3: ("mov", "qword ptr [rsp + 0x50], rax"), 0x001FB7BD: ("movzx", "eax, byte ptr [rsp + 0x60]"),
            0x001FB7C2: ("lea", "r8, [rsp + 0x50]"), 0x001FB7CC: ("mov", "byte ptr [rsp + 0x20], al"),
            0x001FB7E1: ("call", "0x1fb470")}
    for a, w in want.items():
        if m.get(a) != w:
            fails.append("001FB770 image: %08X is %s, expected %s" % (a, m.get(a), w))
    # frame: push (8) + 0x40 -> body rsp+0x60 = entry rsp+0x18 = the r8 home slot; nothing in the body writes it
    writes = [a for a, (mn, op) in m.items() if op.startswith("byte ptr [rsp + 0x60]") or
              op.startswith("qword ptr [rsp + 0x60]") or op.startswith("dword ptr [rsp + 0x60]")]
    if writes:
        fails.append("001FB770 image: the r8 home slot is written at %s" % ", ".join("%08X" % a for a in writes))
    if "a byte read from this function's unwritten r8 home slot" not in text or \
            "the address of a stack slot holding that node" not in text:
        fails.append("001FB770 row: the repaired clause is missing")
    if "the low byte of the fifth (stack) argument" in text:
        fails.append("001FB770 row: still carries the rejected fifth-argument clause")
    return fails


def widget(text):
    fails = []
    m = dis(0x00568BB0, 0x423)
    want = {0x00568C87: ("cmp", "byte ptr [rdi + 0x353], 0"), 0x00568C90: ("cmp", "word ptr [rdi + 0x350], 0"),
            0x00568CA2: ("je", "0x568cc4"), 0x00568CA4: ("movzx", "eax, byte ptr [rdi + 0x343]"),
            0x00568CC4: ("movzx", "eax, byte ptr [rdi + 0x350]"), 0x00568CE4: ("mov", "eax, dword ptr [rdi + 0x354]"),
            0x00568D3F: ("cmp", "byte ptr [rdx + 0x33e], 0"), 0x00568D96: ("lea", "ecx, [rdx + 0x40]"),
            0x00568E2B: ("cmp", "byte ptr [rsi + 0x14], 0"), 0x00568E31: ("cmp", "byte ptr [rsi + 0x15], 2"),
            0x00568E37: ("mov", "eax, dword ptr [rcx + 0xc]"), 0x00568E3C: ("mov", "ecx, 2"),
            0x00568E5E: ("cmp", "byte ptr [rdx + 0x33e], 1"), 0x00568EB5: ("lea", "ecx, [rdx + 0x60]"),
            0x00568EC5: ("cmp", "byte ptr [rsi + 0x17], 1"), 0x00568ECB: ("mov", "ecx, 6"),
            0x00568ED0: ("call", "0x2dd7e0"), 0x00568ED5: ("mov", "dword ptr [rbx + 0x24], eax"),
            0x00568F05: ("cmp", "byte ptr [rsi + 0x14], 0"), 0x00568F3D: ("cmp", "byte ptr [rdx + 0x33e], 2"),
            0x00568F98: ("lea", "ecx, [rdx + 0x60]"), 0x00568FA8: ("cmp", "byte ptr [rsi + 0x17], 2"),
            0x00568FAE: ("mov", "ecx, 6"), 0x00568FB3: ("call", "0x2dd7e0"),
            0x00568FB8: ("mov", "dword ptr [rbx + 0x24], eax")}
    for a, w in want.items():
        if m.get(a) != w:
            fails.append("00568BB0 image: %08X is %s, expected %s" % (a, m.get(a), w))
    for need in ("when word `+0x350` is non-zero, or byte `+0x350` (0) when it is zero",
                 "or `002DD7E0(2)` when entry byte `+0x14` is 0 or byte `+0x15` is 2",
                 "replaced outright by `002DD7E0(6)` when entry byte `+0x17` is 1",
                 "`002CC8D0(0x60, 0x20, dword +0x344, 4)` for elements `+0`, `+8` and `+0x10` when byte `+0x33E` is 0",
                 "for element `+0x20` when it is 1 and for element `+0x28` when it is 2"):
        if need not in text:
            fails.append("00568BB0 row: missing %r" % need)
    if "equal to 0, 1 or 2" in text:
        fails.append("00568BB0 row: still carries the rejected unpaired +0x33E gate")
    return fails


REJECTED = {
    "001FB770": "... calls it `001FB470(rcx + 8, a stack result slot, that node, the stack pair (K, 0), the low byte of "
                "the fifth (stack) argument)` ...",
    "00568BB0": "... in each of these colourings, when ... byte `+0x33E` equal to 0, 1 or 2 and the slot index ...",
}


def main():
    rejected = "--rejected" in sys.argv
    checks = [("opus-sab-sound-bank-container-cloudint-1002", "001FB770", sab),
              ("opus-contract-widget-object-homing-1002", "00568BB0", widget)]
    fails = []
    for rec, fn, f in checks:
        text = REJECTED[fn] if rejected else row(rec, fn)
        out = f(text)
        print("%s %s: %s" % (fn, rec, "ok" if not out else "FAIL"))
        for x in out:
            print("   " + x)
        fails += out
    print("rows 2  FAILS %d%s" % (len(fails), "  (rejected texts: both rows must fail)" if rejected else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
