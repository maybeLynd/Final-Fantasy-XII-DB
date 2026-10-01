"""frame_drain.py [--apply] - ASTRA's lane-drain correction for the per-frame update gate contract
(ASTRA-REQ-OPUS-FRAME-DRAIN-CORRECTION-1001; evidence _experiments/evidence/lane-drain-correction/), staged by OPUS on
2026-10-01 after OPUS re-read 002E6900 and 002E6A80 itself. Apply only after SWE2-AUDIT-SPEC's verdict on
ASTRA-REQ-SPEC-LANE-DRAIN-CORRECTION-1001 (the request asks to consume the independent verdict).

Checks first (in the image): 002E6982 call 0020E600, 002E698C call 0041E490, 002E6994 call 00369800, 002E69E8 call
002E9470, 002E6A70 xor eax,eax (the only return value), 002E6AF0 or eax,[rdi+0x24] after 002E6AED mov eax,[rdi+0x28].
Default is a dry run (WOULD PATCH); --apply writes. Byte-preserving, idempotent; FAILS n."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "00-Engine-Core-Runtime", "CONTRACT-per-frame-update-gate.md")
CHECKS = [(0x002E6982, "call", "0x20e600"), (0x002E698C, "call", "0x41e490"), (0x002E6994, "call", "0x369800"),
          (0x002E69E8, "call", "0x2e9470"), (0x002E6A70, "xor", "eax, eax"), (0x002E6AED, "mov", "eax, dword ptr [rdi + 0x28]"),
          (0x002E6AF0, "or", "eax, dword ptr [rdi + 0x24]")]
REC = "../_index/candidates/opus-frame-drain-1001/frame_drain.py"
NOTE = "*(corrected 2026-10-01, OPUS, on ASTRA's lane-drain correction, re-read at the bytes: %s)*"
EDITS = [
    ("`002E6900` (378 B) is the list append `002E65A0`/`002E6D60` call: walks `0215FD90`'s `+8` links to the tail (or `rbx` when the head is empty), then `0020E600` resolves, `0041E490`/`00369800`/`002E9470` build the node and `002E6A80` links it - the per-frame gate's tail insert.",
     "`002E6900` (378 B) ~~is the list append `002E65A0`/`002E6D60` call: walks `0215FD90`'s `+8` links to the tail (or `rbx` when the head is empty), then `0020E600` resolves, `0041E490`/`00369800`/`002E9470` build the node and `002E6A80` links it - the per-frame gate's tail insert.~~ "
     + NOTE % ("it is the lane DRAIN `002E65A0`/`002E6D60` call. From the tail of `0215FD90`'s list it walks back through `[node]`; for each "
               "of the 32 lanes set in both `+0x14` and `+0x1C` with a non-zero handle at `+0x50 + 4*lane` it resolves the handle "
               "(`0020E600`, `002E6982`), unregisters it (`0041E490`, `002E698C`), frees it (`00369800`, `002E6994`) and clears the lane "
               "and its bits; it unlinks the node and, when `+0x18` and `+0x14` are both 0, retires it through `002E9470` (`002E69E8`); "
               "it repeats while its argument is non-zero, then runs `002E6A80` on nodes whose word `+0x22` is negative. Every normal "
               "return is 0 (`002E6A70`) - not an IO-completion status") + "."),
    ("`002E6D60` enters the cleanup only when `002E6900(0)` returns 0 (`002E6D66`/`002E6D6B`)",
     "`002E6D60` enters the cleanup only when `002E6900(0)` returns 0 (`002E6D66`/`002E6D6B`) - " + NOTE % "which is every normal return, so that test does not gate on IO completion"),
    ("and `002E9470` runs when no flags remain",
     "and `002E9470` runs when ~~no flags remain~~ " + NOTE % "the loaded mask `+0x24` and the mask `+0x28` are both 0 (`002E6AED`/`002E6AF0`); the pending mask `+0x34` is not tested"),
]
fails = 0
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
for a, mn, ops in CHECKS:
    i = next(md.disasm(d[off(a):off(a) + 16], a))
    ok = i.mnemonic == mn and i.op_str == ops
    print("CHECK %08X %s %s -> %s" % (a, i.mnemonic, i.op_str, "ok" if ok else "MISMATCH")); fails += not ok
apply = "--apply" in sys.argv
b = open(P, "rb").read()
for old, new in EDITS:
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", old[:50]); continue
    if b.count(o) != 1:
        print("REFUSING (%d): %s" % (b.count(o), old[:60])); fails += 1; continue
    b = b.replace(o, n); print(("PATCHED " if apply else "WOULD PATCH ") + old[:50])
if apply and not fails:
    open(P, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
