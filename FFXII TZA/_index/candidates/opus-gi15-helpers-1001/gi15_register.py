"""gi15_register.py [--apply] - register row GI-15 ANSWERED (OPUS, 2026-10-01). Replaces the last cell
`**OPEN** — static.`; byte-preserving, refuses a pipe, idempotent. Dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.normpath(os.path.join(HERE, "..", "..", "OPEN-QUESTIONS.md"))
OLD = "| **OPEN** — static. |"
TAG = "**ANSWERED 2026-10-01 (OPUS, static)** — every per-site helper read"
CELL = ("| " + TAG + ": the `0x34` arms are five linear ramps plus two nibble setters and the `0x80` switch, on a "
        "`0x70`-byte pool slot (`003AFC10`) that no static reader consumes. Key 29 is a bone key: `00372800` takes the "
        "first `@FTR` record with that key and flags bit 8 set. `0x3F` and `0x48` fill a bone and a preset, and the page's "
        "`0x3F` field sources are corrected. `00423790` compares priorities in the byte map `01F00410`. `004219C0` and the "
        "key are bone binds. `+0x2F2` is the whole-skeleton-bind flag. `0x2A` drives the camera-shake pool, gated by "
        "verb `0x4A0`. `0x16` binds `@FCT` palettes through FCP section 5. The `0x09` tail is read (the row's `0x2F` "
        "tail is the `0x09` / `0041BEE0` one). `00325260` maps each id-4 subtype to an arm, and `00325090` ignores "
        "the command. What remains is content or live: on-screen meaning, per-model bones and palettes. See the "
        "page's GI-15 section. |")


def main():
    apply = "--apply" in sys.argv
    if "|" in CELL[1:-1]:
        print("REFUSING: pipe inside the cell"); print("FAILS 1"); return 1
    lines = open(REG, "rb").read().split(b"\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(b"| GI-15 |")]
    if len(idx) != 1:
        print("REFUSING: %d GI-15 rows" % len(idx)); print("FAILS 1"); return 1
    row = lines[idx[0]]
    cr = row.endswith(b"\r")
    body = row[:-1] if cr else row
    if TAG.encode("utf-8") in body:
        print("ALREADY GI-15"); print("FAILS 0"); return 0
    if not body.endswith(OLD.encode("utf-8")):
        print("REFUSING: last cell is not the OPEN cell"); print("FAILS 1"); return 1
    lines[idx[0]] = body[:-len(OLD.encode("utf-8"))] + CELL.encode("utf-8") + (b"\r" if cr else b"")
    print(("PATCHED " if apply else "WOULD PATCH ") + "GI-15")
    if apply:
        open(REG, "wb").write(b"\n".join(lines))
    print("FAILS 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
