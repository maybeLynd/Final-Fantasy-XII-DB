"""apply.py [--apply] - FABLE's reconciliation of production status residue (the user's
FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03, sections 2-4): re-status the two stale REOPENED pages, register the
kind-0x54 page's four open items as SD-196..SD-199, and carry FABLE's 2026-09-30 RC-12 adjudication to the register
cell it never reached. Anchored, exact, all-or-nothing; refuses dirty files. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
REC = "[`fable-status-residue-1003`](candidates/fable-status-residue-1003/README.md)"
K54 = "[effect-mesh-records-kind-54.md](../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md)"
REG = "registered by FABLE from the kind-`0x54` page's status line, on the user's independent corpus audit; record " + REC

ENC = os.path.join(DB, "00-Engine-Core-Runtime", "the-encoded-id-space-and-the-query-record.md")
SCH = os.path.join(DB, "01-Script-VM-Native-Bridge", "Interpreter-Core",
                   "how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md")
K = os.path.join(DB, "17-Presentation-Rendering", "Effect-File-Formats", "effect-mesh-records-kind-54.md")
OQ = os.path.join(DB, "_index", "OPEN-QUESTIONS.md")

ENC_OLD = 'status: "REOPENED — SECTION-05 corrects producer semantics; historical audit retained, independent acceptance pending (the open row is OV-5)"'
ENC_NEW = ('status: "PARTIAL — owner re-status 2026-10-03 (FABLE) from REOPENED: SECTION-05\'s producer-semantics correction '
           'was independently ACCEPTED 2026-10-01 (SWE2-AUDIT-SPEC, auditspec-review-section05-1001), so the reopening cause '
           'is resolved; historical audit retained; open: OV-5 (c) a state base at or above 4 GiB and (d) over-reservation, '
           'both runtime, carried by FABLE-REQ-ASTRA-RT-REMAINDERS-0929 (status line current 2026-10-03, FABLE) (was — '
           'REOPENED: independent acceptance of SECTION-05 pending, the open row OV-5)"')
SCH_OLD = ('status: "REOPENED — SECTION-12 trigger resolved (SECTION-12 accepted by a non-author review 2026-09-29) and the '
           'page returns through the owner read; the wait kinds answered (OV-14); the footer slots answered on ORACLE\'s record '
           'with a premise correction, FABLE adjudication pending (RC-12); the run-state promoters answered (RC-14); RC-13 '
           'answered for the question as asked (the shipped scripts\' dominant use of each channel; an author\'s intent is a '
           'stated limit); whether shipped play exhausts the notification pool stays on OV-10 (status line current 2026-09-30, '
           'SWE2-CONTRACT)"')
SCH_NEW = ('status: "PARTIAL — owner re-status 2026-10-03 (FABLE) from REOPENED: the SECTION-12 trigger is resolved (SECTION-12 '
           'accepted by a non-author review 2026-09-29); the wait kinds answered (OV-14); the footer slots answered on '
           'ORACLE\'s record with a premise correction (RC-12: the footer is 0-based; FABLE accepted it and corrected its own '
           'slot table at a8aed6ca9, auditsem-corrections-fable-0930); the run-state promoters answered (RC-14); RC-13 '
           'answered for the question as asked (the shipped scripts\' dominant use of each channel; an author\'s intent is a '
           'stated limit); open: whether shipped play exhausts the notification pool (OV-10, runtime) (status line current '
           '2026-10-03, FABLE) (was — REOPENED with the RC-12 adjudication shown as pending; that adjudication was made '
           '2026-09-30 and never reached this line)"')
K_OLD = ("open: what the matrices hold at draw time, the non-constant planar scalars, and what +0x1F1 bit 3 changes in the "
         "drawing (status line current 2026-10-03, SWE2-DATA, applying FABLE's fable-k54-residue-1003)")
K_NEW = ("open, registered 2026-10-03 (FABLE, on the user's independent corpus audit): SD-196 what the matrices hold at "
         "draw time (runtime), SD-197 the planar scalars authored as resource or curve tracks (static), SD-198 the runtime "
         "pass index after a failed texture lookup (runtime), SD-199 what +0x1F1 bit 3 changes in the drawing beyond "
         "selecting the path (static) (status line current 2026-10-03, FABLE; the line SWE2-DATA applied from "
         "fable-k54-residue-1003 named three of these four without register rows)")
RC12_OLD = "FABLE adjudication pending (`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`). |"
RC12_NEW = ("~~FABLE adjudication pending (`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`).~~ *Restated 2026-10-03 on FABLE's "
            "adjudication at `a8aed6ca9` ([`auditsem-corrections-fable-0930`](candidates/auditsem-corrections-fable-0930/consumer-check.md)): "
            "FABLE accepted ORACLE's 0-based footer and corrected its own slot table, every reader slot of which was one too "
            "high. This cell was not updated at the time (FABLE, 2026-10-03, " + REC + ").* |")
SD195_TAIL = "the authoring tool is not shipped. |"
NEW_ROWS = [
    "| SD-196 | What the matrices hold at draw time for a kind-`0x54` mesh: `02AEEA20` serves pass modes 1 and 3 (79 shipped "
    "slots), `02AEEBF0` modes 2 and 4 (269), and `02AEEAA0` holds mode 1's V (" + K54 + " section 8) | **OPEN 2026-10-03 "
    "(" + REG + "), runtime:** which global serves each mode is static (`fable-k54-residue-1003`); what the frame's camera "
    "and light setup leaves in them at the draw is a live observation. |",
    "| SD-197 | What the planar scalars are when a pass slot authors them as a resource or curve track rather than a "
    "constant: the track kinds `004309C0`, `00430540` and `004307C0` are not decoded (" + K54 + " section 8) | **OPEN "
    "2026-10-03 (" + REG + "), static:** decode the three track kinds and evaluate the shipped tracks; 21 of the 152 "
    "type-`0x05` mode-2 slots author the constant 0.0. |",
    "| SD-198 | Which pass index each kind-`0x54` pass has at run time when a texture lookup fails: a failed lookup drops the "
    "slot and the later passes move down, so the census numbers passes as if every lookup succeeds (" + K54 + " section 8) "
    "| **OPEN 2026-10-03 (" + REG + "), runtime, with a static narrowing:** whether any shipped slot names a texture its "
    "archive lacks can be counted from the data; the drop itself is shown statically (`fable-k54-residue-1003`, C2). |",
    "| SD-199 | What `+0x1F1` bit 3 changes in the drawing beyond selecting the path: `00437130` against the inline path, "
    "and `00444340` against `004434D0`; the grid paths' matrix preparation is call shape only (" + K54 + " section 8) | "
    "**OPEN 2026-10-03 (" + REG + "), static:** read both pairs whole and state the difference; the selector itself is "
    "answered (`+0x590` bit 0 or bit 5, executed over all 256 values). |",
]

EDITS = {ENC: [(ENC_OLD, ENC_NEW)], SCH: [(SCH_OLD, SCH_NEW)], K: [(K_OLD, K_NEW)],
         OQ: [(RC12_OLD, RC12_NEW), (SD195_TAIL, SD195_TAIL + "\n" + "\n".join(NEW_ROWS))]}

fails, out = 0, []
for p, edits in EDITS.items():
    if subprocess.run(["git", "diff", "--quiet", "--", p], cwd=HERE).returncode != 0:
        print("REFUSED: %s has uncommitted changes" % os.path.relpath(p, DB)); fails += 1; continue
    raw = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    for old, new in edits:
        if new.split("\n")[-1] in text and new in text:
            continue
        n = text.count(old)
        if n != 1:
            print("MISS %s (%d): %r" % (os.path.relpath(p, DB), n, old[:80])); fails += 1; continue
        text = text.replace(old, new)
    out.append((p, text.replace("\n", nl), raw))
if fails == 0 and "--apply" in sys.argv:
    for p, t, raw in out:
        if t != raw:
            io.open(p, "w", encoding="utf-8", newline="").write(t); print("PATCHED %s" % os.path.relpath(p, DB))
elif fails == 0:
    print("WOULD PATCH %d files" % sum(1 for p, t, raw in out if t != raw))
print("FAILS %d" % fails)
