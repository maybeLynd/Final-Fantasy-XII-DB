"""apply.py [--apply] - FABLE's answer to OPUS-REQ-FABLE-SYSTEMSTOP-14-1003 on CONTRACT-system-stop-registry.md
(2026-10-03): section 14's "+0x08 still unobserved" is struck and replaced by the builder's stores plus the reader
census (check.py, FAILS 0), and the two places that call 01FD46B0/01FD46C8 the last-computed fade are corrected (the
apply copies them from stack slots it never writes, and nothing reads them). Anchored, all-or-nothing, refuses a dirty
page, keeps line endings. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "00-Engine-Core-Runtime", "System-Stop-Registry", "CONTRACT-system-stop-registry.md")
REC = "[`fable-systemstop-08-1003`](../../_index/candidates/fable-systemstop-08-1003/README.md)"
EDITS = [
    ("01FD46A0..01FD46C8   the combined masks and fade the last apply computed",
     "01FD46A0..01FD46C8   the combined masks the last apply computed (+0x00 of each 0x18 record); +0x08 and +0x10\n"
     "                     are copied from apply stack slots the apply never writes, and nothing reads them\n"
     "                     (FABLE 2026-10-03, section 14)"),
    ("- **The combined fade is different.** Its last-computed value (`01FD46B0` / `01FD46C8`) is set to `-1` by the\n"
     "  initialiser itself (`00226B6D`).",
     "- **The combined fade is different.** ~~Its last-computed value~~ (`01FD46B0` / `01FD46C8`) is set to `-1` by the\n"
     "  initialiser itself (`00226B6D`). *(corrected 2026-10-03, FABLE: these two cells hold no computed fade. Each apply\n"
     "  copies them from its stack slots `[rsp+0x48]` / `[rsp+0x30]` (`002265E5` / `0022661E`), which it never writes,\n"
     "  and no instruction reads them. The frame's fade is the minimum in `ecx`, used in registers; section 14,\n"
     "  " + REC + ".)*"),
    ("The remaining bytes — `+0x08` qword and\n  `+0x15`–`+0x17` — are still unobserved.",
     "The remaining bytes — ~~`+0x08` qword and~~\n  `+0x15`–`+0x17` — are still unobserved.\n"
     "  **`+0x08` (FABLE, 2026-10-03, on OPUS-REQ-FABLE-SYSTEMSTOP-14-1003; record " + REC + ", `check.py` FAILS 0):**\n"
     "  - **Written by the builder.** `00227680` stores the qword in both records of the id it builds: 0 on entry\n"
     "    (`00227698` / `002276A2`) and all-ones in five arms (`002277A1`, `0022793E`, `00227C0E`, `00227C46`,\n"
     "    `00227C82`, each followed by the same store to record B).\n"
     "  - **Read by nothing found.** The census covered every rip-relative reference into `01FD4160`–`01FD46D0`, from\n"
     "    a raw rel32 sweep of every `.text` offset, which reaches seven functions plus the builder. It also covered every\n"
     "    operand through a record pointer in those functions, and the two callers of the record accessor `00226B10`.\n"
     "    It finds the builder's 12 stores at `+0x08` and no reader. The same classifier finds the apply's known\n"
     "    readers of `+0x00` and `+0x10`.\n"
     "  - **The combined records do not carry it.** The apply ANDs only the first qwords. The high half of its\n"
     "    16-byte copies (`00226603` / `00226624`) comes from the stack slots `[rsp+0x40]` / `[rsp+0x28]`, which\n"
     "    the apply never writes. So the per-id `+0x08` never reaches the combined records, and nothing reads\n"
     "    their `+0x08` either.\n"
     "  - **For a port:** writing or omitting the field changes nothing the census can see. It is not\n"
     "    reconstruction-critical unless a reader exists outside the census forms (a computed pointer from\n"
     "    outside these functions)."),
]
if subprocess.run(["git", "diff", "--quiet", "--", P], cwd=HERE).returncode != 0:
    print("REFUSED: the page has uncommitted changes"); print("FAILS 1"); sys.exit(1)
raw = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
t = raw.replace("\r\n", "\n")
fails = 0
for old, new in EDITS:
    if new in t:
        continue
    if t.count(old) != 1:
        print("MISS (%d): %s" % (t.count(old), old[:70])); fails += 1; continue
    t = t.replace(old, new)
if not fails and "--apply" in sys.argv:
    out = t.replace("\n", nl)
    if out != raw:
        io.open(P, "w", encoding="utf-8", newline="").write(out); print("PATCHED")
    else:
        print("ALREADY")
elif not fails:
    print("WOULD PATCH")
print("FAILS %d" % fails)
