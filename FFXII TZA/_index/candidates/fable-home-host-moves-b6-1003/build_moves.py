"""build_moves.py - writes moves.json for AUDIT-SPEC batch 6 host-fit repairs (FABLE, 2026-10-03).

Built on fable-home-host-moves-b5-1003/build_moves.py. It covers SWE2-AUDIT-SPEC's REJECT and ACCEPT-WITH-NARROWING
reviews of FABLE's 1003 homing records (batches P11, P12, P14) that no earlier FABLE repair settled:
- twelve REJECTs (glyph quads, spawn placement, dyngeo, lazy statics, encoded-id, source-block mover, 3d-or-flat,
  ee-vu0 bank, license-board widgets, five small bin tables, external source owner, vbf/st2e);
- four narrowings (effect-element-type-dispatch, element types 40-42, and the cloud F-homing records of the battle
  action handler table and of the numeric-formatting page, whose reviews SWE2-AUDIT-SPEC committed in e8b1a961a and
  c84cc1deb).
Only reviews whose REVIEW.md is committed are taken (`git ls-files`).

THE HOST RULE (new in batch 6, subjects.py): a target must DOCUMENT the caller (for a callee host, the callee) as a
subject - an address in a heading, the first address of a table row, or the first address of a paragraph or list
item - outside this record's own section. A passing mention does not qualify. When a review's named target fails the
rule, the row takes the review's alternative, or is dropped back to the frontier with the reason (`host_fails`).

Each moved row's text, entered_from and anchors are copied from its SOURCE PAGE's FABLE homed section as it stands at
HEAD, never retyped; page and record must agree (checked here). Two moved rows take the review's replacement wording
(REPLACE below); the target page never said the old wording, so it receives the new wording without a strike, and
the record keeps both. Rows that stay where they are and only change text are `edits`: strike-and-replace on the
row's current page, each struck span checked to be on that row (count included), and the record's rows.json text set
to the page cell so its applier stays ALREADY.

Rows whose target or source page is dirty in the shared tree are marked `held`; README.md gives the --only list.

    python -B build_moves.py      (rewrites moves.json beside it)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import subjects  # noqa: E402

C = "_index/candidates/"
DATE = "2026-10-03"
FABLE_HEAD = "## Homed frontier bodies called from this page's functions (FABLE, %s" % DATE
F_HOMING_HEAD = "## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)"
TARGET_HEADING = "## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 6)"

# target pages
GI = "17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md"
UILAYOUT = "16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md"
WTICK = "00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md"
HSPD = "06-Movement-And-Navigation/heading-speed-to-position-delta.md"
FRAMES = "22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md"
HUD = "16-UI/Battle-Hud/the-battle-hud-layout-readers.md"
AUTH = "17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md"
DIALOG = "16-UI/Shared-Dialogs/the-shared-dialog-widgets.md"
CRR = "17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md"
R2 = "15-Input/Modal-Toggles/r2-force-fight-toggle.md"
EFX = "17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md"
# pages a review names that fail the host rule (drops) or that already document a body
GAMEAPP = "00-Engine-Core-Runtime/Application-Root/game-application.md"
NUMERIC = "16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md"
MSGWIN = "16-UI/Message-Windows/the-message-window-layout-readers.md"
TA = "02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md"
ACTOR = "04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md"


def rec(slug):
    return C + "fable-home-%s-1003" % slug


def rev(slug):
    return C + "auditspec-review-fable-home-%s-1003/REVIEW.md" % slug


DIRTY_TARGET = "held: the target page is modified in the shared tree (git status M)"

# fn, record/review slug, target, host, held
MOVES = [
    ("00623EB0", "dyngeo-instance-family", GI, {"by": "caller"}, DIRTY_TARGET),
    ("00624040", "dyngeo-instance-family", GI, {"by": "caller"}, DIRTY_TARGET),
    ("00624690", "dyngeo-instance-family", GI, {"by": "caller"}, DIRTY_TARGET),
    ("006246E0", "dyngeo-instance-family", GI, {"by": "caller"}, DIRTY_TARGET),
    ("0029D4D0", "five-small-bin-tables", UILAYOUT, {"by": "caller"}, None),
    ("00408AD0", "how-a-line-of-text-becomes-glyph-quads", WTICK,
     {"by": "thunk", "thunk": "003EC850", "thunk_callers": ["`002628B0` + 0x2E4", "`0026C8C0` + 0x192"],
      # the review's Repair 2 line, word for word; it is the lead of its own bullet in this record's section
      "lead": "`003EC850` is a 5-byte thunk to `00408AD0`; `002628B0` + 0x2E4 and `0026C8C0` + 0x192 call it"},
     None),
    ("003DB150", "how-the-engine-chooses-3d-or-flat-movem", HSPD, {"by": "caller"}, DIRTY_TARGET),
    ("003AC870", "the-ee-and-vu0-register-bank", FRAMES, {"by": "caller"}, DIRTY_TARGET),
    ("00243EE0", "the-encoded-id-class-registry", HUD, {"by": "caller"}, DIRTY_TARGET),
    ("003AED50", "the-external-source-owner-and-borrowed-", AUTH, {"by": "caller"}, DIRTY_TARGET),
    ("0027F150", "the-license-board-screen-widgets", DIALOG, {"by": "caller"}, None),
    ("003FF160", "the-license-board-screen-widgets", DIALOG, {"by": "caller"}, None),
    ("003FF9F0", "the-license-board-screen-widgets", DIALOG, {"by": "caller"}, None),
    ("00420860", "the-source-block-mover-and-separate-con", CRR, {"by": "caller"}, None),
    ("004209F0", "the-source-block-mover-and-separate-con", CRR, {"by": "caller"}, None),
    ("00366A30", "effect-element-type-dispatch", R2, {"by": "caller"}, None),
    ("004FF230", "effect-element-type-dispatch", EFX,
     {"by": "caller", "why": "This page already read the body in its own text (\"Each body runs `004FF230`\"); "
                             "the row adds its interior anchors."}, None),
    ("004FE4A0", "effect-element-type-dispatch", EFX, {"by": "caller"}, None),
]

# the review's replacement wording for a moved row: (old span, new span, the review's full sentence or None)
REPLACE = {
    "0029D4D0": ("the address loaded by the `lea` at `0029D4DB`", "the procedure `0029D550`", None,
                 "the five-small-bin-tables review, Repair 2: name the procedure (the `lea` at `0029D4DB` loads "
                 "`0029D550`; move_rows.py checks it)"),
    "00420860": ("`rdx`, `r8` and `r9` passed through", "the floats `xmm1`, `xmm2` and `xmm3` passed through",
                 "calls the site `00420860` + 0x19 with `rcx+0x210`, the floats `xmm1`, `xmm2` and `xmm3` passed "
                 "through, and 1.0 (`01CEBBA8`) as the fifth (stack) argument, then returns",
                 "the source-block-mover review, Repair 3: the callee `006C0520` reads `xmm1`-`xmm3`, never "
                 "`rdx`, `r8` or `r9`"),
}
LEA_CHECKS = {"0029D4D0": [["0029D4DB", "0029D550"]]}  # (lea site, address it loads)

# in-place narrowings: fn, page, section heading prefix, record, review, spans (old, new, count), full wording
R_EFFECT = rev("effect-element-type-dispatch")
R_BATTLE = C + "auditspec-review-fable-battle-action-handler-table-homing-1003/REVIEW.md"
EFFECT_PAGE = "17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md"
BATTLE_PAGE = "07-Combat-Action/Action-Dispatch/battle-action-handler-table.md"
EDITS = [
    ("00623D70", EFFECT_PAGE, FABLE_HEAD, rec("effect-element-type-dispatch"), R_EFFECT,
     [("clears bit 31 of dword `rcx+0x18`; when the result is above 1 (unsigned)",
       "takes dword `rcx+0x18` with bit 31 masked off in a register (memory is not written); when that value is "
       "above 1 (unsigned)", 1),
      ("`edx` * 0x10", "zero-extended `edx` * 0x10", 3)], None,
     "N1: `btr eax, 0x1F` clears bit 31 in a register copy only; the index is `edx` zero-extended (`mov eax, edx`)"),
    # the cloud F-homing review of the battle action handler table (committed in e8b1a961a): the two `xmm0` rewordings
    ("00346780", BATTLE_PAGE, F_HOMING_HEAD, C + "fable-battle-action-handler-table-homing-1003", R_BATTLE,
     [("with `xmm1` = the scaled float", "with `xmm0` = that call's float result, `xmm1` = the scaled float", 1)],
     "calls `00267E10(r9)` and `00267DB0(r9)`, scaling the float result by 0.5 (`01CEBB70`); takes pointer A = "
     "`00265060(rdx)` and pointer B = `00265060(00264010(the 00267E10 result))`; calls `00346780+0x65` with `rdx`, "
     "then `00346780+0x8B` with `xmm0` = that call's float result, `xmm1` = the scaled float, `xmm2`/`xmm3` = floats "
     "A `+0`/A `+8` and stack arguments B `+0` (first) and B `+8` (second); tail-jumps to `00346780+0xB4` with the "
     "incoming `rcx` and that call's result in `edx`",
     "the angle call's first argument is `xmm0`, the `00265200` result, which `003A1BB0` uses"),
    ("00346EF0", BATTLE_PAGE, F_HOMING_HEAD, C + "fable-battle-action-handler-table-homing-1003", R_BATTLE,
     [("with `xmm1` = scaled f3", "with `xmm0` = that call's float result, `xmm1` = scaled f3", 1)],
     "calls `00267DB0(r9)` three times (results f1, f2, f3, with f3 scaled by 0.5 (`01CEBB70`)); takes pointer B = "
     "`00265060(rdx)`; calls `00346EF0+0x60` with `rdx`, then `00346EF0+0x7E` with `xmm0` = that call's float "
     "result, `xmm1` = scaled f3, `xmm2`/`xmm3` = floats B `+0`/B `+8` and stack arguments f2 (first) and f1 "
     "(second); tail-jumps to `00346EF0+0xA7` with the incoming `rcx` and that call's result in `edx`",
     "the angle call's first argument is `xmm0`, the `00265200` result, which `003A1BB0` uses"),
    # the cloud F-homing review of the numeric-formatting page (committed in c84cc1deb): the review's old/new clause
    ("003CA530", NUMERIC, F_HOMING_HEAD, C + "fable-numeric-formatting-and-character-mapping-homing-1003",
     C + "auditspec-review-fable-numeric-formatting-and-character-mapping-homing-1003/REVIEW.md",
     [("(int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`)*pi/30)*64+128)",
       "(int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`, converted as an unsigned 32-bit value)*pi/30)"
       "*64+128)", 1)], None,
     "`mov eax, r14d` / `sub eax, ebx` zero-extends `rax`, and `cvtsi2ss xmm0, rax` at `003CA620` converts the "
     "32-bit difference as unsigned"),
]

# drops: fn, record/review slug, kind and its data
DROPS = [
    ("001AD670", "how-the-engine-chooses-3d-or-flat-movem", {
        "host_fails": {
            "reason": "held by the review: no page reads its caller 0017F5B0 as a body; home it with its caller "
                      "(the review names ta-texture-animation-lists.md once 0017F5B0 is cited there)",
            "callers": {"0017F5B0": ["0017F5D3"]},
            "pages": [{"page": TA, "addr": "0017F5B0", "quotes": []}]}}),
    ("001D9F70", "lazy-statics-and-the-one-time-init-lock", {
        "host_fails": {
            "reason": "returned to the frontier: the review's host game-application.md names the caller 0017D940 "
                      "only in passing, inside the 001A07B0 paragraph; it is not a subject there, and the review "
                      "names no alternative host",
            "callers": {"0017D940": ["0017D957"]},
            "pages": [{"page": GAMEAPP, "addr": "0017D940", "quotes": ["`001A1240` run: `0017D940(0)`"]}]}}),
    ("004068B0", "spawn-placement-and-retirement", {
        "host_fails": {
            "reason": "returned to the frontier: the review's host numeric-formatting-and-character-mapping.md does "
                      "not cite the caller 004061F0; the review's repair homes the callers there first, which needs "
                      "new sentences for them (a homing package, not a move)",
            "callers": {"004061F0": ["00406481", "004064B1"]},
            "pages": [{"page": NUMERIC, "addr": "004061F0", "quotes": []}]}}),
    ("00407240", "spawn-placement-and-retirement", {
        "host_fails": {
            "reason": "returned to the frontier: the review's host numeric-formatting-and-character-mapping.md does "
                      "not cite the caller 004061F0; the review's repair homes the callers there first, which needs "
                      "new sentences for them (a homing package, not a move)",
            "callers": {"004061F0": ["00406552"]},
            "pages": [{"page": NUMERIC, "addr": "004061F0", "quotes": []}]}}),
    ("00408140", "spawn-placement-and-retirement", {
        "host_fails": {
            "reason": "returned to the frontier: the review's host numeric-formatting-and-character-mapping.md does "
                      "not cite the caller 00406770; the review's repair homes the callers there first, which needs "
                      "a new sentence for it (a homing package, not a move)",
            "callers": {"00406770": ["00406831"]},
            "pages": [{"page": NUMERIC, "addr": "00406770", "quotes": []}]}}),
]
for fn, site in (("0028FF80", "0035C639"), ("003C98E0", "0035C643"), ("003CA280", "0035C63E")):
    DROPS.append((fn, "vbf-archive-and-st2e-tables", {
        "host_fails": {
            "reason": "returned to the frontier: the review's host the-message-window-layout-readers.md names the "
                      "caller 0035C630 only inside the call chain of its 002BDCE0 row (that row's first address is "
                      "002BDCE0); it is not a subject there, and the review names no alternative host",
            "callers": {"0035C630": [site]},
            "pages": [{"page": MSGWIN, "addr": "0035C630",
                       "quotes": ["| `002BDCE0` (→`0028E220`→`0035C630`→`00253780`, the battle log) |"]}]}}))
DROPS.append(("003B6DE0", "the-element-types-40-42-a0-ab-d0-d1", {
    "already_bound_on": {"page": ACTOR, "quote": "`003B6DE0`, the routine `003B6F80` hands its list to."}}))

REVIEW_SLUG = {"the-element-types-40-42-a0-ab-d0-d1": "the-element-types-40-42-a0-ab-d0-d1"}


def lines_of(page):
    return subjects.page_lines(os.path.join(DB, *page.split("/")))


def page_row(page, head, fn):
    lines = lines_of(page)
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    for l in lines[i + 1:]:
        if l.startswith("## "):
            break
        if l.startswith("| `%s` |" % fn):
            return [c.strip() for c in l.strip().strip("|").split(" | ")]
    raise SystemExit("%s not in the section %r of %s" % (fn, head[:50], page))


def record(recp):
    return json.load(open(os.path.join(DB, *recp.split("/"), "rows.json"), encoding="utf-8"))


def record_row(recp, fn):
    return next(x for x in record(recp)["rows"] if x["fn"] == fn)


def evidence(page, addrs):
    """every subject unit of each address on the page, as (line, quote): the quote is the unit's first line."""
    ls = lines_of(page)
    out = []
    for a in addrs:
        for kind, ln in subjects.subject_lines(ls, a):
            l = ls[ln - 1].strip()
            k = l.find(a) if a in l else 0
            out.append({"addr": a, "kind": kind, "line": ln, "quote": l[max(0, k - 60):k + 60].strip()})
    return out


out = {"date": DATE, "by": "FABLE", "target_heading": TARGET_HEADING,
       "target_before": {EFX: "## 2c. "},
       "review_batches": "SWE2-AUDIT-SPEC P11, P12, P14 (auditspec-review-fable-home-*-1003, *-homing-1003)",
       "moves": [], "edits": [], "drops": []}
for fn, slug, target, host, held in MOVES:
    recp = rec(slug)
    src = record(recp)["page"]
    cells = page_row(src, FABLE_HEAD, fn)
    rr = record_row(recp, fn)
    if cells[3] != rr["text"]:
        raise SystemExit("%s: page text differs from the record" % fn)
    anchors = [a[len("Interior anchor `"):-1] for a in cells[4].split("; ")]
    if anchors != [a for a, _ in rr["anchors"]] or cells[2] != rr["entered_from"]:
        raise SystemExit("%s: page anchors/site differ from the record" % fn)
    text, edit = rr["text"], None
    if fn in REPLACE:
        old, new, full, why = REPLACE[fn]
        if text.count(old) != 1:
            raise SystemExit("%s: replacement span not found once" % fn)
        text = text.replace(old, new)
        if full and text != full:
            raise SystemExit("%s: replaced text differs from the review's wording" % fn)
        edit = {"why": why, "removed": old, "kept": new}
    caller = rr["entered_from"].strip("`").split("`")[0]
    hx = [caller] if host["by"] == "caller" else []
    if host["by"] == "thunk":
        hx = [s.strip("`").split("`")[0] for s in host["thunk_callers"]]
    m = {"fn": fn, "source_page": src, "source_record": recp, "source_section_date": DATE, "review": rev(slug),
         "target_page": target, "entered_from": rr["entered_from"], "source_text": rr["text"], "text": text,
         "text_edit": edit, "anchors": rr["anchors"], "host": host, "evidence": evidence(target, hx)}
    if fn in LEA_CHECKS:
        m["lea_checks"] = LEA_CHECKS[fn]
    if held:
        m["held"] = held
    if not m["evidence"]:
        print("NOTE %s: %s does not document %s as a subject" % (fn, target, ", ".join(hx)))
    out["moves"].append(m)

for fn, page, head, recp, review, spans, full, why in EDITS:
    cells = page_row(page, head, fn)
    rr = record_row(recp, fn)
    if cells[-2] != rr["text"]:
        raise SystemExit("%s: page text differs from the record" % fn)
    plain = rr["text"]
    for old, new, n in spans:
        if plain.count(old) != n:
            raise SystemExit("%s: span %r occurs %d times, recorded %d" % (fn, old, plain.count(old), n))
        plain = plain.replace(old, new)
    if full and plain != full:
        raise SystemExit("%s: narrowed text differs from the review's wording" % fn)
    out["edits"].append({"fn": fn, "page": page, "section": head, "record": recp, "review": review,
                         "source_text": rr["text"], "spans": [list(s) for s in spans], "plain": plain,
                         "why": why})

for fn, slug, kind in DROPS:
    recp = rec(slug)
    src = record(recp)["page"]
    rr = record_row(recp, fn)
    cells = page_row(src, FABLE_HEAD, fn)
    if cells[3] != rr["text"]:
        raise SystemExit("%s: page text differs from the record" % fn)
    d = {"fn": fn, "source_page": src, "source_section_date": DATE, "source_record": recp, "review": rev(slug),
         "source_text": rr["text"]}
    d.update(kind)
    out["drops"].append(d)

open(os.path.join(HERE, "moves.json"), "w", encoding="utf-8", newline="\n").write(
    json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print("moves %d (held %d), edits %d, drops %d" % (
    len(out["moves"]), sum(1 for m in out["moves"] if m.get("held")), len(out["edits"]), len(out["drops"])))
