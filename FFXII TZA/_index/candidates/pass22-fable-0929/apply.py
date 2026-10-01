#!/usr/bin/env python3
"""apply.py - apply FABLE's pass-22 crossing drafts (2026-09-29) to a repository root.

    python apply.py --root <repo root> --check      validate, print the plan, write nothing
    python apply.py --root <repo root>              validate, then apply all edits or none

Options:
    --head-root <git repo>   repository whose HEAD blobs the pages must equal (default: --root). Use it when
                             --root is an exported copy, e.g. a `git archive` of HEAD.
    --drafts <dir>           where the *.crossing.md drafts, registry_rows.tsv and consumer-check.md live
                             (default: this script's directory).
    --no-record              do not install the consumer-check record (see RECORD below).
    --allow-eol-only         accept files that differ from HEAD only in CRLF/LF (core.autocrlf=true checkouts);
                             they are written back with HEAD's endings. Default: refuse, as specified.

SCOPE. FABLE-attributed pages only. The two CONTRACT pages (heading-speed, level-advance) are OPUS's and are
excluded; their drafts are in for-opus.md. The battle-unit field map was attributed by folder; its creating commit
14f43ebc8 is FABLE's (body: "FABLE.md return", co-authored by Claude Fable 5.1), and routing.md gives
folder:04-Actor-Entity to FABLE. It is included and FLAGGED in the output.

SAFETY. Everything is validated before anything is written, and every problem is reported, not only the first:
  * every touched file must be byte-identical to its HEAD blob (`git -C <head-root> show HEAD:<path>`);
  * line endings must be uniform (all LF or all CRLF) and are preserved exactly;
  * every anchor must match exactly once: the section heading line, the section's expected last paragraph,
    and the REPLACE text;
  * no draft may already be present (re-running refuses);
  * no registry row may already exist for its (document, layer) key;
  * the consumer-check record must not exist yet.
Writes go to temporary files first and are then renamed into place; if any rename fails, the files already
replaced are restored from memory. Exit 0 = applied or check passed, 2 = refused, nothing written.
"""
import argparse
import difflib
import io
import os
import re
import subprocess
import sys

DBREL = "Database/FFXII TZA"
REGISTRY = "_index/candidates/neighbour-dispositions.tsv"
RECORD = "_index/candidates/pass22-fable-0929/consumer-check-0929-p22-crossings.md"
FIELD_MAP = "04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md"
EXCLUDED = {
    "06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md": "OPUS-owned CONTRACT page (for-opus.md)",
    "13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md": "OPUS-owned CONTRACT page (for-opus.md)",
}

# page -> (draft file, expected start of the section's last non-blank paragraph, or None for a REPLACE edit)
EDITS = [
    ("07-Combat-Action/how-close-a-unit-must-stand-to-act.md",
     "how-close-a-unit-must-stand-to-act.crossing.md", "Interior anchor `00334553`"),
    ("15-Input/how-a-gamepad-becomes-a-controller-object.md",
     "how-a-gamepad-becomes-a-controller-object.crossing.md", None),
    ("17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md",
     "the-rig-of-seventeen-controllers.crossing.md", "**Input — MECHANICAL (SWE2-EC7-156, 1 edge).**"),
    ("17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md",
     "an-effect-element-frame-by-frame.crossing.md", "**Audio - SHARED LEAF.**"),
    ("17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md",
     "effect-element-type-dispatch.crossing.md", "**Resource — SERVICE, CLIENT and MECHANICAL (16 edges).**"),
    ("22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md",
     "the-phyre-post-effect-class-family.crossing.md", "**UI — CLIENT (2 edges).**"),
    (FIELD_MAP,
     "the-battle-unit-field-map.crossing.md", "**CombatAI, Script VM, Spawn/Encounter — CLIENT"),
]
FLAGS = {
    FIELD_MAP: "FLAG: attributed by folder (folder:04-Actor-Entity), not by lane prefix. Owner confirmed as FABLE: "
               "creating commit 14f43ebc8 ('FABLE.md return', co-authored by Claude Fable 5.1); routing.md assigns "
               "folder:04-Actor-Entity to FABLE. Crossing home: '## Cross-subsystem neighbours — FINAL-AUDIT pass 22'.",
}
# Pages whose pairs are dispositioned only by registry rows (no page edit).
REGISTRY_ONLY = [
    "01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md",
    "17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md",
    "17-Presentation-Rendering/Model-And-Motion-Formats/the-pose-sequencer.md",
]

INS = re.compile(r'<!-- INSERT heading="(.*?)" -->\n(.*?)\n<!-- END INSERT -->', re.S)
REP = re.compile(r'<!-- REPLACE -->\n<!-- OLD -->\n(.*?)\n<!-- NEW -->\n(.*?)\n<!-- END REPLACE -->', re.S)
HEADING = re.compile(r"#{1,3} ")


class Refusal(Exception):
    pass


def head_blob(head_root, rel):
    """HEAD blob bytes of <DBREL>/<rel>, or None if the path is not in HEAD."""
    r = subprocess.run(["git", "-C", head_root, "show", "HEAD:%s/%s" % (DBREL, rel)],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def eol_of(b):
    crlf, lf = b.count(b"\r\n"), b.count(b"\n")
    if crlf == 0:
        return "\n"
    if crlf == lf:
        return "\r\n"
    return None


WARNINGS = []
ALLOW_EOL_ONLY = False


def load_page(root, head_root, rel, problems):
    path = os.path.join(root, DBREL, rel)
    if not os.path.isfile(path):
        problems.append("%s: file missing under --root" % rel)
        return None
    cur = open(path, "rb").read()
    head = head_blob(head_root, rel)
    if head is None:
        problems.append("%s: not in HEAD of %s" % (rel, head_root))
        return None
    base = cur
    if cur != head and ALLOW_EOL_ONLY and cur.replace(b"\r\n", b"\n") == head.replace(b"\r\n", b"\n"):
        WARNINGS.append("%s: worktree differs from HEAD in line endings only (CRLF %d of %d lines); accepted by "
                        "--allow-eol-only, written back with HEAD's endings" % (rel, cur.count(b"\r\n"),
                                                                              cur.count(b"\n")))
        base = head
    elif cur != head:
        if cur.replace(b"\r\n", b"\n") == head.replace(b"\r\n", b"\n"):
            problems.append("%s: differs from its HEAD blob in line endings only (worktree CRLF %d, HEAD CRLF %d) - "
                            "refused: pages must be byte-identical to HEAD (a core.autocrlf checkout does this; "
                            "see --allow-eol-only)" % (rel, cur.count(b"\r\n"), head.count(b"\r\n")))
        else:
            problems.append("%s: content differs from its HEAD blob (uncommitted or peer edit) - refused" % rel)
        return None
    nl = eol_of(base)
    if nl is None:
        problems.append("%s: mixed line endings in HEAD - refused" % rel)
        return None
    try:
        text = base.decode("utf-8")
    except UnicodeDecodeError as e:
        problems.append("%s: not UTF-8 (%s)" % (rel, e))
        return None
    return {"path": path, "bytes": cur, "nl": nl, "text": text.replace("\r\n", "\n")}


def section_bounds(lines, heading, rel, problems):
    idx = [i for i, ln in enumerate(lines) if ln.rstrip() == heading]
    if len(idx) != 1:
        problems.append("%s: heading %r matches %d lines (need exactly 1)" % (rel, heading, len(idx)))
        return None
    end = len(lines)
    for j in range(idx[0] + 1, len(lines)):
        if HEADING.match(lines[j]):
            end = j
            break
    return idx[0], end


def last_paragraph_start(lines, lo, hi):
    k = hi
    while k > lo + 1 and lines[k - 1].strip() == "":
        k -= 1
    s = k
    while s > lo + 1 and lines[s - 1].strip() != "":
        s -= 1
    return s, k          # paragraph lines[s:k]


def plan_page(rel, draft_file, last_prefix, drafts, page, problems):
    dpath = os.path.join(drafts, draft_file)
    if not os.path.isfile(dpath):
        problems.append("%s: draft %s missing" % (rel, dpath))
        return None
    draft = io.open(dpath, encoding="utf-8").read().replace("\r\n", "\n")
    t = page["text"]
    ins, reps = INS.findall(draft), REP.findall(draft)
    if len(ins) + len(reps) != 1:
        problems.append("%s: draft has %d INSERT and %d REPLACE blocks (need exactly one in total)"
                        % (rel, len(ins), len(reps)))
        return None
    notes = []
    if reps:
        old, new = reps[0]
        n = t.count(old)
        if n != 1:
            problems.append("%s: REPLACE old text matches %d times (need exactly 1)" % (rel, n))
            return None
        if new.split("\n", 1)[0] in t:
            problems.append("%s: REPLACE new text already present - already applied?" % rel)
            return None
        at = t[:t.index(old)].count("\n") + 1
        new_t = t.replace(old, new)
        notes.append("replace %d line(s) at line %d" % (old.count("\n") + 1, at))
    else:
        heading, body = ins[0]
        first = body.strip().split("\n", 1)[0][:80]
        if first in t:
            problems.append("%s: insert text already present (%r) - already applied?" % (rel, first))
            return None
        lines = t.split("\n")
        b = section_bounds(lines, heading, rel, problems)
        if b is None:
            return None
        lo, hi = b
        ps, pe = last_paragraph_start(lines, lo, hi)
        para = "\n".join(lines[ps:pe])
        if last_prefix is not None:
            if not para.startswith(last_prefix):
                problems.append("%s: section %r no longer ends with the paragraph starting %r (found %r)"
                                % (rel, heading, last_prefix, para[:80]))
                return None
            sec = "\n".join(lines[lo:hi])
            if sec.count(last_prefix) != 1:
                problems.append("%s: last-paragraph anchor %r matches %d times in the section (need 1)"
                                % (rel, last_prefix, sec.count(last_prefix)))
                return None
        new_lines = lines[:pe] + [""] + body.split("\n") + lines[pe:]
        # keep exactly one blank line before the next heading
        if pe < len(lines) and lines[pe].strip() != "":
            new_lines = lines[:pe] + [""] + body.split("\n") + [""] + lines[pe:]
        new_t = "\n".join(new_lines)
        notes.append("insert %d line(s) after line %d, in section %r (heading line %d, next heading line %s)"
                     % (body.count("\n") + 1, pe, heading, lo + 1, hi + 1 if hi < len(lines) else "EOF"))
    out = new_t.replace("\n", page["nl"]).encode("utf-8")
    return {"rel": rel, "path": page["path"], "old": page["bytes"], "new": out, "notes": notes,
            "nl": "CRLF" if page["nl"] == "\r\n" else "LF", "diff": (t, new_t)}


def plan_registry(root, head_root, drafts, problems):
    rel = REGISTRY
    page = load_page(root, head_root, rel, problems)
    src = os.path.join(drafts, "registry_rows.tsv")
    if page is None:
        return None
    if not os.path.isfile(src):
        problems.append("registry rows %s missing" % src)
        return None
    rows = [l for l in io.open(src, encoding="utf-8").read().replace("\r\n", "\n").split("\n") if l.strip()]
    t = page["text"]
    if not t.endswith("\n"):
        problems.append("%s: HEAD file does not end with a newline - refused" % rel)
        return None
    existing = set()
    for line in t.split("\n"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.split("\t")
        if len(f) >= 2:
            existing.add((f[0].strip().replace("\\", "/"), f[1].strip()))
    bad = False
    for r in rows:
        f = r.split("\t")
        if len(f) != 7:
            problems.append("registry row has %d columns (need 7): %s" % (len(f), r[:80]))
            bad = True
            continue
        if f[5] not in ("CROSSING-ACCOUNTED", "EDGE-ON-PAGE", "GENUINELY-IRRELEVANT", "FALSE-SUBJECT"):
            problems.append("registry row verdict %r outside the vocabulary: %s" % (f[5], r[:80]))
            bad = True
        if (f[0], f[1]) in existing:
            problems.append("registry already has a row for (%s, %s) - refused" % (f[0], f[1]))
            bad = True
        if r in t:
            problems.append("registry already contains this exact row: %s" % r[:80])
            bad = True
    if bad:
        return None
    new_t = t + "\n".join(rows) + "\n"
    return {"rel": rel, "path": page["path"], "old": page["bytes"],
            "new": new_t.replace("\n", page["nl"]).encode("utf-8"),
            "notes": ["append %d row(s) (%s)" % (len(rows), ", ".join("%s|%s" % (r.split("\t")[0].rsplit("/", 1)[-1],
                                                                                   r.split("\t")[1]) for r in rows))],
            "nl": "CRLF" if page["nl"] == "\r\n" else "LF", "diff": (t, new_t)}


def plan_record(root, head_root, drafts, problems):
    src = os.path.join(drafts, "consumer-check.md")
    path = os.path.join(root, DBREL, RECORD)
    if not os.path.isfile(src):
        problems.append("consumer-check draft %s missing" % src)
        return None
    if os.path.exists(path) or head_blob(head_root, RECORD) is not None:
        problems.append("%s already exists (worktree or HEAD) - refused" % RECORD)
        return None
    body = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")
    return {"rel": RECORD, "path": path, "old": None, "new": body.encode("utf-8"),
            "notes": ["create (LF, %d lines)" % body.count("\n")], "nl": "LF", "diff": ("", body)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True)
    ap.add_argument("--head-root")
    ap.add_argument("--drafts", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-record", action="store_true")
    ap.add_argument("--show-diff", action="store_true", help="with --check, print unified diffs")
    ap.add_argument("--allow-eol-only", action="store_true",
                    help="accept a file whose bytes differ from HEAD ONLY in CRLF/LF (a core.autocrlf checkout); "
                         "the edited file is written with HEAD's line endings. Off by default.")
    a = ap.parse_args()
    global ALLOW_EOL_ONLY
    ALLOW_EOL_ONLY = a.allow_eol_only
    root = os.path.abspath(a.root)
    head_root = os.path.abspath(a.head_root or a.root)
    r = subprocess.run(["git", "-C", head_root, "rev-parse", "HEAD"], capture_output=True, text=True)
    if r.returncode:
        print("REFUSED: %s is not a git repository (use --head-root)" % head_root)
        return 2
    print("apply.py: root=%s  HEAD from %s at %s  mode=%s" % (root, head_root, r.stdout.strip(),
                                                               "CHECK" if a.check else "APPLY"))
    for rel, why in sorted(EXCLUDED.items()):
        print("  excluded: %s - %s" % (rel, why))
    for rel in REGISTRY_ONLY:
        print("  registry-only (page not edited): %s" % rel)

    problems, plans = [], []
    for rel, draft, last in EDITS:
        if rel in EXCLUDED:
            problems.append("internal: %s is both edited and excluded" % rel)
            continue
        page = load_page(root, head_root, rel, problems)
        if page is None:
            continue
        p = plan_page(rel, draft, last, a.drafts, page, problems)
        if p:
            plans.append(p)
    p = plan_registry(root, head_root, a.drafts, problems)
    if p:
        plans.append(p)
    if not a.no_record:
        p = plan_record(root, head_root, a.drafts, problems)
        if p:
            plans.append(p)

    if problems:
        print("\nREFUSED - %d problem(s); nothing written:" % len(problems))
        for x in problems:
            print("  - " + x)
        return 2

    for w in WARNINGS:
        print("  WARN " + w)
    print("\nAll anchors unique, all files byte-identical to HEAD%s. Plan (%d file(s)):"
          % (" (EOL-only differences accepted, see WARN)" if WARNINGS else "", len(plans)))
    for p in plans:
        print("  %s  [%s, %d -> %d bytes]" % (p["rel"], p["nl"], len(p["old"] or b""), len(p["new"])))
        for n in p["notes"]:
            print("      " + n)
        if p["rel"] in FLAGS:
            print("      " + FLAGS[p["rel"]])
        if a.show_diff:
            for line in difflib.unified_diff(p["diff"][0].split("\n"), p["diff"][1].split("\n"),
                                             p["rel"], p["rel"], n=1, lineterm=""):
                print("      | " + line)
    if a.check:
        print("\nCHECK ONLY - nothing written.")
        return 0

    # apply: temp files first, then rename; restore on any failure
    tmps = []
    try:
        for p in plans:
            os.makedirs(os.path.dirname(p["path"]), exist_ok=True)
            tmp = p["path"] + ".p22tmp"
            with open(tmp, "wb") as f:
                f.write(p["new"])
            tmps.append((p, tmp))
    except OSError as e:
        for _, tmp in tmps:
            if os.path.exists(tmp):
                os.remove(tmp)
        print("REFUSED: could not stage temp files (%s); nothing written" % e)
        return 2
    done = []
    try:
        for p, tmp in tmps:
            os.replace(tmp, p["path"])
            done.append(p)
    except OSError as e:
        for p in done:
            if p["old"] is None:
                os.remove(p["path"])
            else:
                with open(p["path"], "wb") as f:
                    f.write(p["old"])
        for _, tmp in tmps:
            if os.path.exists(tmp):
                os.remove(tmp)
        print("FAILED mid-apply (%s); %d file(s) restored, nothing left changed" % (e, len(done)))
        return 2
    for p in plans:
        if open(p["path"], "rb").read() != p["new"]:
            print("VERIFY FAILED: %s does not hold the planned bytes" % p["rel"])
            return 2
    print("\nAPPLIED %d file(s):" % len(plans))
    for p in plans:
        print("  %s/%s" % (DBREL, p["rel"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
