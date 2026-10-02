"""apply_router.py [--apply] - the request-router page: SWE2-CONTRACT's atlas-slot correction
(SWE2CONTRACT-REQ-FABLE-ROUTER-ATLAS-BIT7-0930, verified by OPUS at the bytes) and the owner re-status to DOCUMENTED
that documented_rule.py allows (READY: no live register id, no open box). OPUS, 2026-10-01, FABLE inactive.

Checks first: 0027FA38..0027FA98 are five 0024A5A0 lookups each followed by `and [rax+0x38], 0xffffff7f`;
0024A5A3 loads the 64-slot registry 0208F580; 0024A710 builds the mask 0xE0 | (1 << k) and tests it against slot
+0x38 (r14 = 0208F5B8). Tag-guarded, idempotent; dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

PAGE = os.path.join(DB, "16-UI", "Request-Router", "ui-request-router.md")
CHECKS = [(0x0027FA38, "call", "0x24a5a0"), (0x0027FA42, "and", "+ 0x38], 0xffffff7f"),
          (0x0027FA5A, "and", "+ 0x38], 0xffffff7f"), (0x0027FA72, "and", "+ 0x38], 0xffffff7f"),
          (0x0027FA8A, "and", "+ 0x38], 0xffffff7f"), (0x0027FA98, "call", "0x24a5a0"),
          (0x0024A5A3, "lea", "r9, [rip"), (0x0024A733, "mov", "ebx, 0xe0"), (0x0024A73B, "bts", "ebx, ecx"),
          (0x0024A762, "lea", "r14, [rip"), (0x0024A793, "and", "rcx, rax"), (0x0024A796, "cmp", "rcx, rax")]
TARGETS = {0x0024A5A3: 0x0208F580, 0x0024A762: 0x0208F5B8}
LINK = "../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md"
EDITS = [
    ("which only clears bit 7 of five widget records' `+0x38`.",
     "which only clears bit 7 of five ~~widget records'~~ named UI atlas slots' `+0x38` *(corrected 2026-10-01, OPUS, "
     "on SWE2-CONTRACT's request, at the bytes: `0024A5A0` finds each slot by name in the 64-slot registry `0208F580`, "
     "and bit 7 admits an atlas to the texture-memory layout pass `0024A710`, which takes a slot only when its `+0x38` "
     "holds `0xE0 | (1 << k)` - see [a typed list measured once](" + LINK + ") §5d)*.",
     "named UI atlas slots' `+0x38` *(corrected 2026-10-01, OPUS"),
    ("(marks a widget record)",
     "(~~marks a widget record~~ re-admits that atlas to the layout pass - *corrected 2026-10-01, OPUS*)",
     "re-admits that atlas to the layout pass - *corrected 2026-10-01, OPUS*"),
    # the re-status makes interior cites A: cite the thunk entry, not its last instruction, so the three-member
    # NativeAdapter.GlobalOffsetTailCall family is not refused (adrift_report, 2026-10-01)
    ("(`0028E860`–`0028E86E` → `0028CA30` → `memset`)", "(`0028E860` → `0028CA30` → `memset`)",
     "(`0028E860` → `0028CA30` → `memset`)"),
    ("status: PARTIAL — UQ-162 answered 2026-09-25",
     "status: DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): "
     "UQ-162 answered 2026-09-25", "status: DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS"),
]


def main():
    apply = "--apply" in sys.argv
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, frag in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and frag in ins.op_str
        if ok and va in TARGETS:
            ok = va + ins.size + int(ins.op_str.split("rip + ")[1].split("]")[0], 16) == TARGETS[va]
        fails += 0 if ok else 1
        print("%s %08X %s" % ("ok  " if ok else "FAIL", va, "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<none>"))
    if fails:
        print("REFUSING: image check failed")
        print("FAILS", fails)
        return 1
    raw = open(PAGE, "rb").read().decode("utf-8")
    for old, new, tag in EDITS:
        if tag in raw:
            print("ALREADY", old[:50]); continue
        if raw.count(old) != 1:
            print("REFUSING: %d occurrences of %s" % (raw.count(old), old[:50])); fails += 1; continue
        raw = raw.replace(old, new)
        print(("PATCHED " if apply else "WOULD PATCH ") + old[:50])
    if apply and not fails:
        open(PAGE, "wb").write(raw.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
