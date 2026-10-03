"""fix_reject_rows_1003.py - apply SWE2-AUDIT-SPEC's two REJECT repairs at cc2da97b8 to OPUS's own rows (OPUS, 2026-10-03):
001FB770 (opus-sab-sound-bank-container-cloudint-1002) and 00568BB0 (opus-contract-widget-object-homing-1002).
Each repair was re-read at the bytes by OPUS before writing (frame 0x48 at 001FB770; 00568C90/CC4, E2B..E41, EC5,
F05..F1B, FA8 at 00568BB0). Idempotent: a row already carrying its replacement is left alone."""
import io
import json
import os

C = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates"

SAB_OLD = "that node, the stack pair (K, 0), the low byte of the fifth (stack) argument"
SAB_NEW = ("the address of a stack slot holding that node, the address of the stack pair (K, 0), and a byte read from this "
           "function's unwritten r8 home slot (an empty-tag argument)")

W_OLD_START = "fills a widget group on the array at qword `[rdx+0x10]`"
W_NEW = (
    "fills a widget group on the array at qword `[rdx+0x10]` from the 32-byte entry at `rcx` + 0x160 + 32 * `r9d`: "
    "for `r9d` 0 it calls `00243580(rdx, 0)` and shows elements `+0x40`, `+0x38` and `+0x48` with the entry's byte "
    "`+0x14` and first qword, coloured with byte `+0x343` as the top byte (element `+0x48`: dword `+0x354` when byte "
    "`+0x353` is 0; otherwise its colour with top byte `+0x343` when word `+0x350` is non-zero, or byte `+0x350` (0) "
    "when it is zero); for other `r9d` it colours elements `+0`, `+8` and `+0x10` with `002DD7E0(entry byte +0x15 + "
    "0x77)` (`0x79` when byte `+0x14` is 0) and fills elements `+0x18`, `+0x20` and `+0x28` from the entry's byte "
    "`+0x14` and qwords `+0` / `+8`; the colour stored at `+0x24` of elements `+0x20` and `+0x28` starts as dword "
    "`+0xC` of the element's first qword, or `002DD7E0(2)` when entry byte `+0x14` is 0 or byte `+0x15` is 2; when the "
    "record at qword `02CA96E0`[dword `+0x35C`] has bit `0x1` of byte `+0x340` clear and the slot index of qword "
    "`+0xD8` equals `r9d`, the colour's top byte becomes `002CC8D0(0x60, 0x20, dword +0x344, 4)` for elements `+0`, "
    "`+8` and `+0x10` when byte `+0x33E` is 0, and `002CC8D0(0x80, 0x20, dword +0x344, 4)` for element `+0x20` when "
    "it is 1 and for element `+0x28` when it is 2; the colour of element `+0x20` is then replaced outright by "
    "`002DD7E0(6)` when entry byte `+0x17` is 1, and that of element `+0x28` when it is 2; returns 1")

JOBS = [
    ("opus-sab-sound-bank-container-cloudint-1002", "001FB770",
     lambda t: t.replace(SAB_OLD, SAB_NEW) if SAB_OLD in t else None,
     "SWE2-AUDIT-SPEC REJECT (auditspec-review-opus-sab-sound-bank-container-cloudint-1002): the byte passed to 001FB470 "
     "is read from the r8 home slot (frame 0x48), not the fifth argument, and the third argument is the address of a "
     "stack slot holding the node; SPEC's replacement applied verbatim; reject_rows_check.py is the regression"),
    ("opus-contract-widget-object-homing-1002", "00568BB0",
     lambda t: W_NEW if t.startswith(W_OLD_START) and t != W_NEW else None,
     "SWE2-AUDIT-SPEC REJECT (auditspec-review-opus-contract-widget-object-homing-1002): element +0x48's top byte "
     "depends on word +0x350; elements +0x20/+0x28 have a base colour rule and a 002DD7E0(6) replacement on entry "
     "byte +0x17; each 002CC8D0 gate pairs with its own +0x33E value; row rewritten per SPEC's repair, re-read at the "
     "bytes; reject_rows_check.py is the regression"),
]

for rec, fn, fix, why in JOBS:
    p = os.path.join(C, rec, "rows.json")
    d = json.load(io.open(p, encoding="utf-8"))
    n = 0
    for r in d["rows"]:
        if r["fn"] == fn:
            new = fix(r["text"])
            if new is not None:
                r["text"] = new
                n += 1
    if n:
        d.setdefault("corrections", []).append({"fn": fn, "why": why})
        json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    print(rec, fn, "replaced" if n else "already")
