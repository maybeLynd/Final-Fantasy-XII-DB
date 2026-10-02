"""gi_register.py [--apply] - register cells for GI-16 / GI-17 (answered) and GI-19 (narrowed), OPUS 2026-10-01.

Each row must still end with the cell `**OPEN** — static.`; that last cell is replaced. Byte-preserving (each line keeps
its EOL), refuses a pipe in new text, idempotent (ALREADY when the tag is present). Dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.normpath(os.path.join(HERE, "..", "..", "OPEN-QUESTIONS.md"))
OLD = "| **OPEN** — static. |"
OLD_BY_ROW = {"GI-18": "| **OPEN** — static. The note's other two reasons are settled and excluded: the `00566B70`–`0056AD50` per-leaf roles (read 2026-09-15, member table) and `00566C10`'s art (GI-1: a tab-strip pointer, not condition/action art). |", "GI-14": "| **OPEN** — static. `0044A180` (`0x05`) and `0044C850` (`0x0A`) are covered by GI-11's tail reads (A5/B1) and are not in this row. |"}
CELLS = {
    "GI-16": "| **ANSWERED 2026-10-01 (OPUS, static)** — five states, not four: a word store at `00558607` (`0x401` at "
             "`+0x37C`) sets `+0x37D` to 4, and the switch at `00557DF0` has an arm for each of 0-4. 0 asks "
             "`00252D10(0xBB)` and goes to 2 (allowed) or 1 with a `0x10` countdown (denied); 1 counts down, then "
             "`00252D40(0xBB, 1)` and `002CE2F0(self, 0x18)`, to 3; 2 runs `005588C0` / `00558C40` / `00556EC0`, to 3; "
             "3 is settled; 4, entered on message `0x19`, waits for the effect `003B2D80` started (`003B2CE0` returns 0), "
             "marks bit `[+0x358]` of `+0x364`, removes the effect and repaints, to 3, while a three-step `00249C60` "
             "sound sequence plays. On-screen look not claimed. See the page's move-mode paragraph. |",
    "GI-17": "| **ANSWERED 2026-10-01 (OPUS, static)** — the three bodies read: `002D45C0(widget, on)` stores `on & 1` in "
             "bit 16 of `+0xE0` and, when the focused widget (`00244820`) is on the widget's `+0x10` chain and every widget on "
             "that chain up to the root is live and of an eligible kind, calls `003689E0(on)`; `002CFCF0` re-attaches `[0209AC30]+0x278` under the UI root `0208EA28` "
             "when it exists; `0027EE80` sets word `+0x44` of the `[0209AC30]` sub-widgets `+0x2B8` / `+0x2C8` to "
             "`0x6E` and starts their 200 ms moves to `(56, 4)` / `(32, 4)`. On-screen meaning not claimed. See the "
             "shop page's GI-17 section. |",
    "GI-14": "| **OPEN** — static. `0044A180` (`0x05`) and `0044C850` (`0x0A`) are covered by GI-11's tail reads (A5/B1) and are not in this row. *(Narrowed 2026-10-01, OPUS: the six tail helpers and the line emitter `0039D6C0` are "
             "read - see the element-types page's GI-14 section; the blend value sits at the GiPrim command's `+0x30` "
             "and GiPrim `00863D80` passes it to its render context's vtable `+0x40`; only which class implements that "
             "slot, and so how the GS-ALPHA-shaped value becomes the blend state, remains.)* |",
    "GI-18": "| **ANSWERED 2026-10-01 (OPUS, static)** — every arm of both procedures read one level down: the editor `005691E0`'s twelve table arms, its id-12 sub-ids `0x8000`-`0x8004` and the peeled `0x121`, and the pick list `0056B4D0`'s 19 entries (ten share the `005C5230` return-0 default). The arm roles the read refutes are struck on the page: ids 8 / 9 are focus gained / lost, 16 snapshots the set into `+0x128`, 18 writes that snapshot back only when `[0209AC30]+0xDEB` is set, 26 is the per-row slide step `00568FE0`, and `0x8003` empties a row. Not established: the writer of `+0xDEB`. See the gambit page's GI-18 section. |",
    "GI-19": "| **OPEN** — static. *(Narrowed 2026-10-01, OPUS: the chain is two two-step resolves through `0020E600`, "
             "not one four-deep chain - the record's `+0x08` id to an object whose `+0x00` id is the bone array, and "
             "the entry's `+0x08` id to an array of `0x40`-byte sub-entries whose `+0x04` id resolves to an object "
             "holding the u16 bone index; only the three intermediate objects' class names remain.)* |",
}
TAG = {"GI-18": "**ANSWERED 2026-10-01 (OPUS, static)** — every arm of both procedures", "GI-14": "*(Narrowed 2026-10-01, OPUS: the six tail helpers and the line emitter", "GI-16": "**ANSWERED 2026-10-01 (OPUS, static)** — five states", "GI-17": "**ANSWERED 2026-10-01 (OPUS, static)** — the three bodies",
       "GI-19": "*(Narrowed 2026-10-01, OPUS: the chain is two two-step"}


def main():
    apply = "--apply" in sys.argv
    lines = open(REG, "rb").read().split(b"\n")
    fails = 0
    for rid, cell in CELLS.items():
        if "|" in cell[1:-1].replace("\\|", ""):
            print("REFUSING %s: pipe inside the cell" % rid); fails += 1; continue
        idx = [i for i, l in enumerate(lines) if l.startswith(("| %s |" % rid).encode())]
        if len(idx) != 1:
            print("REFUSING %s: %d rows" % (rid, len(idx))); fails += 1; continue
        row = lines[idx[0]]
        cr = row.endswith(b"\r")
        body = row[:-1] if cr else row
        if TAG[rid].encode("utf-8") in body:
            print("ALREADY", rid); continue
        old = OLD_BY_ROW.get(rid, OLD).encode("utf-8")
        if not body.endswith(old):
            print("REFUSING %s: last cell is not %r" % (rid, old[:40])); fails += 1; continue
        lines[idx[0]] = body[:-len(old)] + cell.encode("utf-8") + (b"\r" if cr else b"")
        print(("PATCHED " if apply else "WOULD PATCH ") + rid)
    if apply and not fails:
        open(REG, "wb").write(b"\n".join(lines))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
