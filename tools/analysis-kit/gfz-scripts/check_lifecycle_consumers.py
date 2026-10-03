#!/usr/bin/env python3
"""check_lifecycle_consumers.py [--root REPO] [--self-test] - do the current entry points still say what the lifecycle
contract says? (FABLE, 2026-10-03; user's context refresh package v3 + improvement addendum.)

WHY. The project's "what happens after the database" plan was repeated across README, goals, handoffs and progress
text, and partly lost as they drifted independently. It is now written once: RECONSTRUCTION-CHARTER.md section 0, with
a machine-readable twin _index/workflow/PROJECT-LIFECYCLE.json. This check makes the most damaging drift mechanical:
  1. the JSON parses and keeps its invariants (goal L1+L2; L3 not required; user authorization required; no automatic
     transition; the original game is not the production backend);
  2. charter section 0 exists, states the JSON's current phase, and carries the rules the JSON encodes, including
     every maturity label;
  3. the current entry points (database README, TEAM.md, DASHBOARD-MEANINGS.md) link section 0 or the JSON, and the
     README's stated phase equals the JSON's;
  4. known superseded current-state phrases are absent from those surfaces unless struck through (~~...~~).
Deterministic source-to-consumer comparison only; no free-text judgement. It is NOT a completion gate.

Prints one line per finding and `FAILS N` last; exit 1 when N > 0. --self-test applies five mutations to an in-memory
copy (each must be caught) and the unmutated copy (must pass)."""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT0 = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
CHARTER = "RECONSTRUCTION-CHARTER.md"
DB = "Database/FFXII TZA"
JSONP = DB + "/_index/workflow/PROJECT-LIFECYCLE.json"
CONSUMERS = {
    DB + "/README.md": ["RECONSTRUCTION-CHARTER.md#0-project-lifecycle", "PROJECT-LIFECYCLE.json"],
    DB + "/_index/_inbox/TEAM.md": ["RECONSTRUCTION-CHARTER.md#0-project-lifecycle", "PROJECT-LIFECYCLE.json"],
    DB + "/_index/workflow/DASHBOARD-MEANINGS.md": ["PROJECT-LIFECYCLE.json"],
}
# phrases that described a superseded state as current; allowed only inside ~~strike~~
SUPERSEDED = [
    (DB + "/README.md", r"the gate is not sealed"),
    (DB + "/README.md", r"eleven fixed identities since"),
    (DB + "/_index/PROGRAM-STATE.md", r"the main transition awaits\s+the existing charter quality/readiness gate"),
]
# Supersession index (addendum section 15): a current entry point may link a historical artifact only on a line that
# also carries the artifact's label (its key word suffices: HISTORICAL, SUPERSEDED, SEALED, AS-OF, PROPOSAL).
SUPERSESSION = DB + "/_index/workflow/SUPERSESSION.json"
ENTRY_POINTS = [DB + "/README.md", DB + "/_index/_inbox/TEAM.md"]
LABEL_WORD = {"HISTORICAL CHECKPOINT": "HISTORICAL", "SUPERSEDED CURRENT-STATE VIEW": "SUPERSEDED",
              "SEALED EVIDENCE": "SEALED", "AS-OF SNAPSHOT": "AS-OF", "PROPOSAL / NOT ADOPTED": "PROPOSAL"}
PHASE_WORDS = {"DATABASE": "DATABASE", "DATABASE_READY_AWAITING_AUTHORIZATION": "DATABASE READY",
               "RECONSTRUCTION": "RECONSTRUCTION", "INTEGRATION": "INTEGRATION",
               "PARITY_CERTIFICATION": "PARITY CERTIFICATION", "HIGH_PARITY_RUNTIME": "HIGH-PARITY RUNTIME"}


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
        return f.read().replace("\r\n", "\n")


def section0(charter):
    m = re.search(r"^## 0\. Project lifecycle.*?(?=^## |\Z)", charter, re.M | re.S)
    return m.group(0) if m else None


def unstruck(text):
    return re.sub(r"~~.*?~~", "", text, flags=re.S)


def check(files):
    """files: rel path -> text. Returns a list of findings."""
    out = []
    try:
        lc = json.loads(files[JSONP])
    except Exception as e:  # noqa: BLE001
        return ["CONTRACT %s does not parse: %s" % (JSONP, e)]
    inv = [("database_goal", "L1+L2"), ("l3_required_for_database_completion", False),
           ("primary_reconstruction_requires_user_authorization", True),
           ("automatic_transition_from_database_ready", False)]
    for k, v in inv:
        if lc.get(k) != v:
            out.append("CONTRACT %s = %r, expected %r" % (k, lc.get(k), v))
    if (lc.get("original_game_role") or {}).get("production_backend") is not False:
        out.append("CONTRACT original_game_role.production_backend must be false")
    phase = lc.get("current_primary_phase")
    if phase not in {p.get("id") for p in lc.get("phases", [])}:
        out.append("CONTRACT current_primary_phase %r is not one of the declared phases" % phase)
    s0 = section0(files[CHARTER])
    if s0 is None:
        out.append("CHARTER %s has no '## 0. Project lifecycle' section" % CHARTER)
    else:
        need = ["Current phase: %s." % PHASE_WORDS.get(phase, phase), "L3 is not a prerequisite",
                "the user explicitly authorizes", "not** the production execution backend", "first divergence",
                "PROJECT-LIFECYCLE.json"]
        need += list(lc.get("maturity_ladder", []))
        for w in need:
            if w not in s0:
                out.append("CHARTER section 0 lacks %r" % w)
    for rel, links in CONSUMERS.items():
        t = files[rel]
        for l in links:
            if l not in t:
                out.append("CONSUMER %s does not link %s" % (rel, l))
    m = re.search(r"Current phase: (?:\*\*)?([A-Z][A-Z -]+?)(?:\*\*)?\.", files[DB + "/README.md"])
    if not m:
        out.append("CONSUMER %s/README.md states no 'Current phase: X.'" % DB)
    elif m.group(1).strip() != PHASE_WORDS.get(phase, phase):
        out.append("CONSUMER README phase %r != contract %r" % (m.group(1).strip(), phase))
    for rel, pat in SUPERSEDED:
        if re.search(pat, unstruck(files[rel]), re.I):
            out.append("STALE %s still states a superseded phrase /%s/ outside ~~strike~~" % (rel, pat))
    if SUPERSESSION in files:
        try:
            sup = json.loads(files[SUPERSESSION])
        except Exception as e:  # noqa: BLE001
            return out + ["SUPERSESSION %s does not parse: %s" % (SUPERSESSION, e)]
        for e in sup.get("entries", []):
            word = LABEL_WORD.get(e.get("status"))
            if word is None:
                continue
            for p in e.get("paths", []):
                tail = p.split("/")[-1] or p.rstrip("/").split("/")[-1]
                if not tail or tail.startswith("TEAM.md#"):
                    continue
                for rel in ENTRY_POINTS:
                    for ln in files[rel].split("\n"):
                        if tail in ln and word not in ln.upper():
                            out.append("RESUME %s links %s (%s) on a line without its label" % (rel, tail, e["status"]))
    return out


def load(root):
    rels = [CHARTER, JSONP] + list(CONSUMERS) + [r for r, _ in SUPERSEDED] + ENTRY_POINTS
    files = {r: read(root, r) for r in dict.fromkeys(rels)}
    if os.path.exists(os.path.join(root, SUPERSESSION)):
        files[SUPERSESSION] = read(root, SUPERSESSION)
    return files


def self_test(files):
    base = check(files)
    print("self-test: unmutated copy -> %d finding(s)" % len(base))
    ok = not base
    lc = json.loads(files[JSONP])

    def mut(name, rel, fn):
        nonlocal ok
        f2 = dict(files); f2[rel] = fn(f2[rel])
        got = check(f2)
        caught = len(got) > len(base)
        print("  %-48s %s" % (name, "caught" if caught else "MISSED"))
        ok = ok and caught

    mut("JSON: L3 made a DB prerequisite", JSONP,
        lambda t: json.dumps(dict(lc, l3_required_for_database_completion=True)))
    mut("JSON: original game as production backend", JSONP,
        lambda t: json.dumps(dict(lc, original_game_role=dict(lc["original_game_role"], production_backend=True))))
    mut("JSON: phase advanced without the charter", JSONP,
        lambda t: json.dumps(dict(lc, current_primary_phase="RECONSTRUCTION")))
    mut("README: lifecycle link removed", DB + "/README.md",
        lambda t: t.replace("RECONSTRUCTION-CHARTER.md#0-project-lifecycle", "RECONSTRUCTION-CHARTER.md"))
    mut("README: 'not sealed' wording restored", DB + "/README.md",
        lambda t: t + "\n| x | y | *the gate is not sealed* |\n")
    if SUPERSESSION in files:
        mut("README: old handoff offered as a resume point", DB + "/README.md",
            lambda t: t + "\nResume from [the handoff](../Tools/docs/NEXT_CHAT_HANDOFF_2026-09-01_Gfz9_V121_GM160_GN_READ_ONLY_FINAL_160.md).\n")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT0)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    try:
        files = load(a.root)
    except FileNotFoundError as e:
        print("MISSING %s" % e); print("FAILS 1"); return 1
    if a.self_test:
        ok = self_test(files)
        print("SELF-TEST %s" % ("PASS" if ok else "FAIL")); print("FAILS %d" % (0 if ok else 1))
        return 0 if ok else 1
    found = check(files)
    for f in found:
        print(f)
    print("checked: contract, charter section 0, %d consumers, %d superseded phrases" % (len(CONSUMERS), len(SUPERSEDED)))
    print("FAILS %d" % len(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
