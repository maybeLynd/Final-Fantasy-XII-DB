"""queue_contract_splice.py - SWE2-CONTRACT's three resource-queue findings, as an exact splice for the overlay carrier
CONTRACT-resource-request-queue.md (OPUS, 2026-10-01; SWE2CONTRACT-REQ-OPUS-QUEUE-CONTRACT-UNRESOLVED-0930).

The carrier is FRONTIER-applied (overlay-drop-census). OPUS does not write it: this script prints the edits with --dry-run
and applies them with --apply, byte-preserving and idempotent. Anchors re-read by OPUS at the bytes on 2026-10-01:
0032E670 xor r14d,r14d / 0032E6FF mov [rcx+0x50],r14 / 0032E959 mov [r10+0x50],0 / 0032E3B4 mov rax,[rcx+0x50];
0032E153 add [rbx],rax / 0032E229, 0032E725 (r14 = 0), 0032E97C stores of 0; 0032EA9E xor edx,edx then 0032EAA7 and
0032EAE0 store 0 to 022C51E0. The never-read census is SWE2-CONTRACT's (swe2contract-ddres-b6-0930/b6_request_queue.py
Z1-Z3, M1-M2). Prints WOULD PATCH / PATCHED / ALREADY per edit and FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "..", "02-Resource-And-Asset-Pipeline", "CONTRACT-resource-request-queue.md")
SRC = "SWE2-CONTRACT `b6_request_queue.py`"
EDITS = [
    ("| `+0x00`, `+0x08` | Absolute-counter accumulator and latest stamp. State 2 adds the **second** getter result and "
     "stores that same result as the stamp. |",
     "| `+0x00`, `+0x08` | Absolute-counter accumulator and latest stamp. State 2 adds the **second** getter result and "
     "stores that same result as the stamp. **The accumulator is written, never read in this build** (" + SRC + " Z1, "
     "M1-M2, Z3): `0032E153` adds to it and `0032E229` / `0032E725` / `0032E97C` store 0; its purpose is not a static "
     "question. |"),
    ("| `+0x50` | Part callback slot. **The requester clears it; it does not copy descriptor `+0x20`.** |",
     "| `+0x50` | Part callback slot. **The requester clears it; it does not copy descriptor `+0x20`.** **Nonnull part "
     "callbacks: none in the shipped build** (" + SRC + " Z2): the slot is stored only as 0 (`0032E6FF`, `r14` = 0 from "
     "`0032E670`; `0032E959`) and read only at `0032E3B4`, so `0032E3B0` returns 1 and part results 2 / 3 occur only "
     "under seeded controls. |"),
    ("* Authored/reachable producer state for the chunk gate, nonnull part callbacks and invalid input values.",
     "* Authored/reachable producer state for the chunk gate~~, nonnull part callbacks~~ and invalid input values. "
     "*(Nonnull part callbacks answered 2026-10-01: none in the shipped build, `+0x50` row.)*"),
    ("* Meaning of the absolute-counter accumulator and the still-unobserved slot bytes.",
     "* ~~Meaning of the absolute-counter accumulator and the still-unobserved slot bytes.~~ *(Answered 2026-10-01: the "
     "accumulator is written and never read, `+0x00` row; the 16 bytes `022C51E0`..`022C51EF` after the list record are one "
     "qword stored 0 by `0032EAA7` and `0032EAE0` and never read (" + SRC + " Z3).)*"),
]
mode = "--apply" if "--apply" in sys.argv else "--dry-run"
fails = 0
b = open(P, "rb").read()
for old, new in EDITS:
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", old[:50]); continue
    if b.count(o) != 1:
        print("REFUSING (%d): %s" % (b.count(o), old[:60])); fails += 1; continue
    b = b.replace(o, n)
    print(("PATCHED " if mode == "--apply" else "WOULD PATCH ") + old[:50])
if mode == "--apply" and not fails:
    open(P, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
