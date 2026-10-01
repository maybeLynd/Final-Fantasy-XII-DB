"""worldtick_corrections.py - two page lines the interior reading contradicted, corrected (OPUS, 2026-10-01).
Re-read at the bytes before writing:
  001EC690: `inc dword ptr [01F832C4]` then `ret` (7 B) - an increment, not a flag read.
  0051E800: `0051E809 mov dword ptr [rcx+0x128], 0`; its sibling 0051E840: `0051E849 mov dword ptr [rcx+0x128], 1`.
The script checks both instructions in the image, then strikes the old wording with a dated note. Byte-preserving,
idempotent; PATCHED / ALREADY per edit, FAILS n."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "00-Engine-Core-Runtime", "Battle-Frame", "the-world-tick-and-the-field-frame.md")
CHECKS = [(0x001EC690, "inc", "dword ptr [rip + 0x1d96c2e]"), (0x0051E809, "mov", "dword ptr [rcx + 0x128], 0"),
          (0x0051E849, "mov", "dword ptr [rcx + 0x128], 1")]
NOTE = "*(corrected 2026-10-01, OPUS, on reading the bodies: %s)*"
EDITS = [
    ("`001EC690` (7 B `01F832C4` flag read)",
     "`001EC690` (7 B ~~`01F832C4` flag read~~ " + NOTE % "it increments dword `01F832C4` (`inc` at the entry) and returns" + ")"),
    ("| `0051E800`, `0051E840` | set `+0x128` `=1`, then",
     "| `0051E800`, `0051E840` | ~~set `+0x128` `=1`~~ " + NOTE % "`0051E800` stores 0 at `+0x128` (`0051E809`), `0051E840` stores 1 (`0051E849`)" + ", then"),
]
fails = 0
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
for a, mn, ops in CHECKS:
    i = next(md.disasm(d[off(a):off(a) + 16], a))
    ok = i.mnemonic == mn and i.op_str == ops
    print("CHECK %08X %s %s -> %s" % (a, i.mnemonic, i.op_str, "ok" if ok else "MISMATCH")); fails += not ok
b = open(P, "rb").read()
for old, new in EDITS:
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", old[:40]); continue
    if b.count(o) != 1:
        print("REFUSING (%d): %s" % (b.count(o), old[:50])); fails += 1; continue
    b = b.replace(o, n); print("PATCHED", old[:40])
if not fails:
    open(P, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
