"""build_moves.py - writes moves.json from the source homing records (FABLE, 2026-10-03; AUDIT-SPEC batch 4).

Copy of opus-fable-home-host-moves-1003/build_moves.py, for the ten REJECT reviews of SWE2-AUDIT-SPEC commit
`95d495604`. Each row's text, entered_from and anchors are copied from the FABLE record that homed it, never retyped,
and no text is edited (every review says "re-home it unchanged"). The host for each row is the one its review's
**Repair:** block names. `evidence` quotes the target page's own lines that cite the caller; move_rows.py checks that
each quote is still on the page.

`drops` are rows the review says to remove without re-homing, because another page already binds the body.
`already_bound_on` names that page and the line found by grep; move_rows.py re-checks the quote is still there.

Rows the batch-4 reviews reject but that this package does NOT move (listed in DEFERRED, printed, not in moves.json):
- `004EB910`: its page text still has the false "1.0 (`01E0283C`)" clause at HEAD (fixed by fable-corr-004eb910-1003),
  and the VIF1 page the review names does not cite the caller `004EBE80` yet.
- `00361480`: the named target does not cite the caller `00342770`; the review says it cannot be caller-hosted.
- `00314D60`: the named target does not cite the caller `0050C8A0`; the review says non-caller stream or cite first.

    python -B build_moves.py      (rewrites moves.json beside it)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
C = os.path.join(DB, "_index", "candidates")
DATE = "2026-10-03"
SPEC = "auditspec-review-fable-home-%s-1002"

WT = "00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md"
EFX = "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md"
PFG = "00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md"
VIF = "17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md"
WID = "16-UI/Widget-Object-Model/CONTRACT-widget-object.md"
APP = "00-Engine-Core-Runtime/Application-Root/game-application.md"
SDC = "99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md"
REC = "04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md"
LOC = "06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md"
PFB = "14-Story-Event-Quest-Hunt/persistent-flag-banks.md"

Q_WT = ["### The `0022A770` exclusive subtree — the field frame's helper set"]
Q_EFX = ["`002F3BC0(element)`:", "birth step (corrected 2026-10-02, OPUS: it runs once per element) — `002F3BC0`"]
Q_PFG = ["`003C6000` (236 B) is the state-bit driver `002507C0` runs on `02B45A00`",
         "Interior anchor `003C6013` (function `003C6000`)."]
Q_VIF = ["functions in the region (`004B1190` 32,136 B, `004C8320`", "`004C8320` 28,422"]
Q_WID = ["`0027D740` (interior read 2026-09-17, SWE2-FRONTIER: `00808F10` first at",
         "`002727F0` (426 B) is the record clone `0027D740` calls",
         "`002729A0` (411 B) is the broadcast `0027D740` calls"]
Q_APP = ["different update bodies (`00189CE0`, 1,083 B",
         "`001AC950` (722 B) is the worker the renderer update `00189CE0` calls"]
Q_SDC = ["All three are read by one body, `002B5C90`",
         "| `002B5C90` | reads the `+0x400` table and the three pointer slots (§3a, §3c) |"]
Q_REC = ["caller is verb **`0176` `fieldsign`** (`00355A00`)", "Verb **`0176` `fieldsign`** (`00355A00`) calls the setter"]
Q_LOC = ["| facing publish, record loop | `00310B00`, `00310BB1`, `00310CA6` (`00310920`, caller `0037D000`) |"]
Q_PFB = ["places a world marker at the record's position (`002FB560(i, x, y)`,"]

BOOT = "contract-boot-fixups"
MOVES = [
    # fn, record/review slug, target page, evidence quotes on the target (its own text)
    ("0036F510", "active-party-reserve-and-the-moment-the", WT, Q_WT),
] + [(fn, BOOT, EFX, Q_EFX) for fn in (
    "0044D460", "0044ED90", "0044F930", "00451140", "00451890", "00453CB0", "004548F0",
    "0045BF50", "0045C920", "0045D290", "0045DCA0", "0045E8C0")] + [
    ("0035D070", BOOT, PFG, Q_PFG),
    ("004CF230", BOOT, VIF, Q_VIF),
    ("00272400", "equipment-slots-and-the-single-stat-reb", WID, Q_WID),
    ("0027C220", "equipment-slots-and-the-single-stat-reb", WID, Q_WID),
    ("001941F0", "keymap-ini-file-format-and-default-cont", APP, Q_APP),
    ("00194490", "keymap-ini-file-format-and-default-cont", APP, Q_APP),
    ("00285FE0", "keymap-ini-file-format-and-default-cont", SDC, Q_SDC),
    ("00314820", "keymap-ini-file-format-and-default-cont", WT,
     ["`00377520` (58 B) is the once-per-change gate the `0022A770` frame"] + Q_WT),
] + [(fn, "native-command-seam", REC, Q_REC) for fn in ("0026AB60", "0026BB00", "0026BDD0", "0026BFF0", "003DF790")] + [
    ("00310D30", "the-moment-an-action-is-committed", LOC, Q_LOC),
] + [(fn, "world-loot-pickups-the-ten-slot-pool-an", PFB, Q_PFB)
     for fn in ("00231F20", "0033CBF0", "003EC5B0", "003EC720", "003EC770")]

DROPS = [
    # fn, record/review slug, page that already binds it, quote on that page
    ("0026B480", "native-command-seam", REC,
     "`jmp 0026B480`. It sets the bit and does nothing else. `0026B480` is twenty-nine bytes and is"),
    ("00379D40", "scriptvm-verb-dispatch-and-parameter-en", "02-Resource-And-Asset-Pipeline/the-resource-request-queue.md",
     "## The `00379D40` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)"),
]

DEFERRED = [
    {"fn": "004EB910", "slug": BOOT, "why": "page text at HEAD still has the false `1.0 (`01E0283C`)` clause "
     "(correction package fable-corr-004eb910-1003 not yet on HEAD), and the-vif1-vu1-layer.md does not cite "
     "`004EBE80`; the review says re-home on the VIF1 page once it names `004EBE80`, otherwise park"},
    {"fn": "00361480", "slug": "contract-input-subsystem", "why": "18-Audio/Audio-Boundary/how-a-sound-request-becomes-"
     "a-voice.md does not cite the caller `00342770`; the review says the row cannot be caller-hosted (callee/table "
     "stream, or have that page cite `00342770` first)"},
    {"fn": "00314D60", "slug": "ff12config-and-debglobal", "why": "01-Script-VM-Native-Bridge/verbs-that-only-wait-and-"
     "verbs-that-do-nothing.md does not cite the caller `0050C8A0`; the review says non-caller stream, or once that "
     "page cites `0050C8A0`"},
]
TEXT_EDITS = {}


def line_of(page, quote):
    for i, l in enumerate(open(os.path.join(DB, page), encoding="utf-8", errors="replace").read().splitlines(), 1):
        if quote in l:
            return i
    return None


def record(slug):
    rec = "fable-home-%s-1002" % slug
    return rec, json.load(open(os.path.join(C, rec, "rows.json"), encoding="utf-8"))


out, drops = [], []
for fn, slug, target, quotes in MOVES:
    rec, cfg = record(slug)
    row = next(r for r in cfg["rows"] if r["fn"] == fn)
    text = row["text"]
    out.append({
        "fn": fn,
        "source_page": cfg["page"],
        "source_record": "_index/candidates/" + rec,
        "source_section_date": cfg["date"],
        "review": "_index/candidates/" + SPEC % slug + "/REVIEW.md",
        "target_page": target,
        "entered_from": row["entered_from"],
        "source_text": row["text"],
        "text": text,
        "text_edit": None,
        "anchors": row["anchors"],
        "evidence": [{"line": line_of(target, q), "quote": q} for q in quotes],
    })
for fn, slug, page, quote in DROPS:
    rec, cfg = record(slug)
    row = next(r for r in cfg["rows"] if r["fn"] == fn)
    drops.append({
        "fn": fn,
        "source_page": cfg["page"],
        "source_record": "_index/candidates/" + rec,
        "source_section_date": cfg["date"],
        "review": "_index/candidates/" + SPEC % slug + "/REVIEW.md",
        "source_text": row["text"],
        "already_bound_on": {"page": page, "line": line_of(page, quote), "quote": quote},
    })
deferred = []
for d in DEFERRED:
    rec, cfg = record(d["slug"])
    deferred.append({"fn": d["fn"], "source_page": cfg["page"], "source_record": "_index/candidates/" + rec,
                     "review": "_index/candidates/" + SPEC % d["slug"] + "/REVIEW.md", "why": d["why"]})
json.dump({"date": DATE, "by": "FABLE", "target_heading":
           "## Homed bodies re-homed here for host fit (FABLE, %s; AUDIT-SPEC batch 4)" % DATE,
           "review_commit": "95d495604", "moves": out, "drops": drops, "deferred": deferred},
          open(os.path.join(HERE, "moves.json"), "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("moves", len(out), "drops", len(drops), "deferred", len(deferred), "missing evidence lines:",
      [(m["fn"], e["quote"][:40]) for m in out for e in m["evidence"] if e["line"] is None]
      + [(d["fn"], "bound") for d in drops if d["already_bound_on"]["line"] is None])
