"""build_moves.py - writes moves.json from the source homing records (OPUS, 2026-10-03).

Each row's text, entered_from and anchors are copied from the FABLE record that homed it, never retyped. Two
texts get one edit each, so that bits are written as values (house rule): `00273800` "bit 3 (`0x8`)" -> "bit `0x8`",
and `00198730` "bit 0 of byte" -> "bit `0x1` of byte". The host choice for each row is the one its SWE2-AUDIT-SPEC
review names, re-verified by OPUS; `evidence` quotes the target page's own line that cites the caller, and
move_rows.py checks that quote is still on the page.

    python -B build_moves.py      (rewrites moves.json beside it)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
C = os.path.join(DB, "_index", "candidates")
DATE = "2026-10-03"

SPEC = "auditspec-review-fable-home-%s-1002"
MOVES = [
    # fn, source record slug, review slug, target page, evidence quotes on the target (its own text)
    ("001DE180", "arm-catalogue-slice-a-ids-12-43", "arm-catalogue-slice-a-ids-12-43",
     "19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md",
     ["| interface populate | `001DE5D0` (1,919 B", "The `001DE5D0` question is **answered 2026-09-17 (SWE2-FRONTIER):**"]),
    ("00183260", "arm-catalogue-slice-h-ids-236-267", "arm-catalogue-slice-h-ids-236-267",
     "00-Engine-Core-Runtime/Application-Root/game-application.md",
     ["## SWE2-EC7-122 update (2026-09-21) - the `0079C140` display-mode family measured",
      "| 10 | `0017D120` | `00189120` lookup then `byte [rax] = 1`"]),
    ("00273800", "contract-the-five-parallel-slot-maps", "contract-the-five-parallel-slot-maps",
     "16-UI/the-selection-the-menu-publishes.md",
     ["`002732E0` is the four-slot find. It returns the record among `0035BB20(0..3)` whose `+4` equals the handle",
      "Which records `0035BB20` returns for slots 0 to 3"]),
    ("003EBD70", "contract-ui-request-router", "contract-ui-request-router",
     "00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md",
     ["### The `002628B0` exclusive subtree", "it calls the unload `002628B0` for each set bit"]),
    ("002DEF20", "contract-world-simulation-tick", "contract-world-simulation-tick",
     "18-Audio/the-spatial-audio-object-model.md",
     ["<- 00332C40 / 003B99D0 / 0046C8F0 / 0046CC70      (four callers, the first bodies that"]),
    ("002DF1A0", "contract-world-simulation-tick", "contract-world-simulation-tick",
     "18-Audio/the-spatial-audio-object-model.md",
     ["<- 00332C40 / 003B99D0 / 0046C8F0 / 0046CC70      (four callers, the first bodies that"]),
    ("003A7950", "gambit-evaluation-and-enmity", "gambit-evaluation-and-enmity",
     "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md",
     ["`003ED8A0` (552 B) is the effect-file data parse", "is the sibling emit `003ED8A0` runs for the chain-tracked kind"]),
    ("003A7A50", "gambit-evaluation-and-enmity", "gambit-evaluation-and-enmity",
     "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md",
     ["`003ED8A0` (552 B) is the effect-file data parse", "is the copy-in element emit `003ED8A0` runs for table-driven payloads"]),
    ("003A7AA0", "gambit-evaluation-and-enmity", "gambit-evaluation-and-enmity",
     "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md",
     ["`003ED8A0` (552 B) is the effect-file data parse", "is the sibling emit `003ED8A0` runs for the chain-tracked kind"]),
    ("003A92B0", "gambit-evaluation-and-enmity", "gambit-evaluation-and-enmity",
     "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md",
     ["`003ED8A0` (552 B) is the effect-file data parse"]),
    ("00198730", "the-actor-storage-record-field-map", "the-actor-storage-record-field-map",
     "00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md",
     ["with per-id side calls for a few ids (`00182D60`, `00182D40`, and"]),
    ("00322950", "the-status-write-and-its-side-effects", "the-status-write-and-its-side-effects",
     "04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md",
     ["| `002C7660` | 1190 | ~~display-record channel evaluation~~ the per-unit overhead-display evaluation"]),
    ("002FB250", "when-a-group-is-wiped-and-when-it-comes", "when-a-group-is-wiped-and-when-it-comes",
     "13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md",
     ["| `00319B10` | `Loot_InitializeWorldPickupPool` | 387 B |", "## SWE2-EC7-40 update (2026-09-19) - `00319B10`"]),
    ("00363B00", "when-a-group-is-wiped-and-when-it-comes", "when-a-group-is-wiped-and-when-it-comes",
     "00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md",
     ["| 17 | verbs **`ucon`** / `ucon_4a5` (`0026C5D0`)", "## The `0026C3E0`/`0026C5D0` exclusive-subtree pair"]),
]
TEXT_EDITS = {
    "00273800": ("bit 3 (`0x8`)", "bit `0x8`"),
    "00198730": ("bit 0 of byte", "bit `0x1` of byte"),
}


def line_of(page, quote):
    for i, l in enumerate(open(os.path.join(DB, page), encoding="utf-8", errors="replace").read().splitlines(), 1):
        if quote in l:
            return i
    return None


out = []
for fn, rec_slug, rev_slug, target, quotes in MOVES:
    rec = "fable-home-%s-1002" % rec_slug
    cfg = json.load(open(os.path.join(C, rec, "rows.json"), encoding="utf-8"))
    row = next(r for r in cfg["rows"] if r["fn"] == fn)
    text = row["text"]
    if fn in TEXT_EDITS:
        old, new = TEXT_EDITS[fn]
        assert old in text, (fn, old)
        text = text.replace(old, new)
    out.append({
        "fn": fn,
        "source_page": cfg["page"],
        "source_record": "_index/candidates/" + rec,
        "source_section_date": cfg["date"],
        "review": "_index/candidates/" + SPEC % rev_slug + "/REVIEW.md",
        "target_page": target,
        "entered_from": row["entered_from"],
        "source_text": row["text"],
        "text": text,
        "text_edit": ("bits as values: %r -> %r" % TEXT_EDITS[fn]) if fn in TEXT_EDITS else None,
        "anchors": row["anchors"],
        "evidence": [{"line": line_of(target, q), "quote": q} for q in quotes],
    })
json.dump({"date": DATE, "by": "OPUS", "target_heading":
           "## Homed bodies re-homed here for host fit (OPUS, %s)" % DATE, "moves": out},
          open(os.path.join(HERE, "moves.json"), "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("moves", len(out), "missing evidence lines:",
      [(m["fn"], e["quote"][:40]) for m in out for e in m["evidence"] if e["line"] is None])
