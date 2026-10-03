"""apply_l2_table.py [--apply] - OPUS's verdict-table share of SWE2-AUDIT-SPEC's L2 expansion (AUDITSPEC-REQ-OPUS-L2EXP-
REPAIRS-1003 (b)), 2026-10-03. Without --apply: checks that every change is present (exit 0) or reports what is not.

Changes, each a cell of the main L2-VERDICTS.md table located by row id and column (positional; the other cells keep
their bytes), never a free-text search:
  contract  13 bare-MET cells get the reason SWE2-AUDIT-SPEC supplied (item 3 task A); 7 go SCOPE-SHORT (S-01, S-16, S-21
            from item 3; S-25, S-29, S-38 with SWE2-AUDIT-SEM's wordings SWE2-AUDIT-SPEC concurred with; S-08 by OPUS's
            decision (criterion c): SCOPE-SHORT, not a split row - a split moves the 52-system denominator and needs a
            ruling); 3 are narrowed with an explicit bounded exception (S-17, S-31, S-44)
  L2        rows whose contract cell is now SCOPE-SHORT and that read MET become NOT MET (S-01, S-08, S-21, S-29, S-38);
            rows already NOT MET on types record the contract gap too (S-16, S-25)
  script    7 N/A-FALSE cells become "MET (linked)" with SWE2-AUDIT-SPEC's item 3 task B text (S-02, S-18, S-19, S-20,
            S-21, S-23, S-38); S-05 keeps N/A with its stated reason; S-33 keeps N/A and records its resource link
  summary   the hand-kept "contract column" count table is replaced by a pointer to the generated recount (it drifted
            twice: 2026-09-21 and 2026-10-03; checkpoint_consistency.py C4 measured MET 47 / SCOPE-SHORT 3 against rows
            52 / 0)
Old text is struck (~~ ~~), never deleted, per the correction policy."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
L2 = os.path.normpath(os.path.join(HERE, "..", "..", "L2-VERDICTS.md"))
ITEM3 = os.path.normpath(os.path.join(HERE, "..", "auditspec-l2-expansion-1003", "item3.md"))
D = "2026-10-03"
SRC = "SWE2-AUDIT-SPEC's L2 expansion item 3, `auditspec-l2-expansion-1003`"
COL = {"contract": 2, "script": 6, "l2": 7}

REASONS = {
    "S-03": "the subsystem contract covers the ladder and all four setters",
    "S-04": "the subsystem contract covers both pages by subject",
    "S-06": "the subsystem contract implements all three console pages",
    "S-10": "one page, covered by the subsystem contract",
    "S-12": "the subsystem contract implements all three pages",
    "S-14": "both paths and both tables are in the subsystem contract",
    "S-15": "scope and system coincide (L1256)",
    "S-23": "one transition is the whole subject (the contract is still `level: L1`)",
    "S-33": "scope and system coincide",
    "S-37": "the subsystem contract implements both pages (L2706)",
    "S-39": "the scope is covered (L2705); the sample's REJECT stands on types and §10.1",
    "S-46": "the routing subsystem contract carries every cross-generator invariant",
    "S-50": "scope and system coincide",
}
SCOPE_SHORT = {
    "S-01": "the VBF mount `0017CEB0` and the startup latch writer `0017D074` sit in no credited contract",
    "S-16": "the retirement trigger `002350C0` and the keep-bank rotation `00233780` (the keep window) sit in no credited "
            "contract",
    "S-08": "the file layer sits in no credited contract (item 3 sample). OPUS's decision on criterion (c): SCOPE-SHORT, "
            "not a split row - splitting the file layer into its own row moves the 52-system denominator and needs a "
            "ruling",
}
SEM = {   # SWE2-AUDIT-SEM's wordings (auditsem-l1-verdict-items-1003), SWE2-AUDIT-SPEC concurred (README item 3)
    "S-25": "SCOPE-SHORT for page 2: `CONTRACT-enmity.md` (subsystem) covers the enmity half and `CONTRACT-gambit-walk.md` "
            "(operation) the walk of one subgroup, with the subgroup bound in its §14.1. No contract states `00305AB0`'s "
            "selection order (the player-command pre-empt, the `00377C20` gate, the four set attempts A–D with `+0x6B5` "
            "only on C, and B's null set skipping C) or the `002FDDA0` set-switch arms (`0x4112`–`0x4115` authored set "
            "via `+0x6E0`; `0x4116`–`0x4121` subgroup)",
    "S-29": "SCOPE-SHORT for page 1: `CONTRACT-equipment-compatibility.md` (subsystem) and "
            "`CONTRACT-inventory-class-storage.md` (family) cover page 2. No contract states the item-use reservation "
            "lifecycle — Prepare `0030EF20` reserves into `unit+0xDC8`/`+0xE58` and takes the item; Consume `00305640` "
            "clears the reservation and charges MP or the secondary pool; Refund `00300280` returns item and gil. "
            "EXP-064/065/066 executed parts of it with `contract: none`",
    "S-38": "MET for page 1 (`CONTRACT-character-render-object.md`, subsystem, R-1..R-7). SCOPE-SHORT for page 2: the "
            "record array is implemented by `CONTRACT-render-record-pool-lifecycle.md` (family) and "
            "`CONTRACT-coast-down-latch.md` (transition), and no contract states the array's shared layer — the `+0x18` "
            "flag word's outside-family writers (bits 0, 2, 4; pool §14) against the pool's own bit-0 bracket and bit-5 "
            "sets, and the latch's id-addressing of records the pool may retire",
}
NARROW = {
    "S-17": "the clock-across-load interaction (page 2 L83–113) is stated by no credited contract",
    "S-31": "the board grid loader and the `licenceOwnedBits` purchase writer are stated by no credited contract",
    "S-44": "the language code→id `0017E270` is stated by no credited contract",
}
L2_TO_NOT_MET = ("S-01", "S-08", "S-21", "S-29", "S-38")
L2_ALSO = ("S-16", "S-25")
SCRIPT_LINKED = ("S-02", "S-18", "S-19", "S-20", "S-23", "S-38")


def proposed(section_row, kind="text"):
    """SWE2-AUDIT-SPEC's 'Proposed text' for a task-B row, verbatim from item3.md (the S-02 one is AUDIT-SEM's)."""
    t = io.open(ITEM3, encoding="utf-8").read()
    m = re.search(r"^### %s \(item 3[^\n]*\n(.*?)(?=^### |^## )" % re.escape(section_row), t, re.S | re.M)
    if not m:
        raise SystemExit("item3.md has no section for %s" % section_row)
    lab = {"text": r"Proposed (?:script/data )?text", "contract": r"Proposed contract-cell text"}[kind]
    p = re.search(lab + r"[^:]*:\s*\"(.+?)\"(?:\.|\s|$)", m.group(1), re.S)
    if not p:
        raise SystemExit("item3.md %s has no proposed text" % section_row)
    return " ".join(p.group(1).split())


def edits():
    out = []
    for r, why in REASONS.items():
        out.append((r, "contract", lambda old, why=why: "%s — reason supplied %s (%s; recorded by OPUS): %s" % (
            old.strip(), D, SRC, why), "reason supplied %s" % D))
    for r, why in SCOPE_SHORT.items():
        out.append((r, "contract", lambda old, why=why: "~~%s~~ **SCOPE-SHORT — re-scored %s (OPUS, on %s): %s**" % (
            old.strip(), D, SRC, why), "**SCOPE-SHORT — re-scored %s (OPUS" % D))
    for r, txt in SEM.items():
        out.append((r, "contract", lambda old, txt=txt: "~~%s~~ **SCOPE-SHORT — re-scored %s (OPUS, applying "
                    "SWE2-AUDIT-SEM's wording, SWE2-AUDIT-SPEC concurred): %s**" % (old.strip(), D, txt),
                    "applying SWE2-AUDIT-SEM's wording"))
    for r, why in NARROW.items():
        out.append((r, "contract", lambda old, why=why: "%s — narrowed %s (OPUS, on %s): %s; recorded here as an "
                    "explicit bounded exception to the credited scope" % (old.strip(), D, SRC, why),
                    "explicit bounded exception"))
    for r in L2_TO_NOT_MET:
        out.append((r, "l2", lambda old: "~~%s~~ **NOT MET — the contract cell is SCOPE-SHORT (re-scored %s, OPUS, on "
                    "%s)**" % (old.strip(), D, SRC), "**NOT MET — the contract cell is SCOPE-SHORT (re-scored %s" % D))
    for r in L2_ALSO:
        out.append((r, "l2", lambda old: "%s *(and the contract cell is SCOPE-SHORT, %s, OPUS)*" % (old.strip(), D),
                    "*(and the contract cell is SCOPE-SHORT, %s" % D))
    for r in SCRIPT_LINKED:
        txt = proposed(r)
        body = txt.split(": ", 1)[-1] if txt.startswith("MET (linked)") else txt.replace("MET — linked, not N/A ", "", 1)
        out.append((r, "script", lambda old, body=body: "~~%s~~ **MET (linked) — re-scored %s (OPUS, adopting %s task B "
                    "text): %s**" % (old.strip(), D, SRC, body), "task B text):"))
    out.append(("S-21", "contract", lambda old: "~~%s~~ **SCOPE-SHORT — re-scored %s (OPUS, adopting %s task A text): "
                "%s**" % (old.strip(), D, SRC, proposed("S-21", "contract").split(" — ", 1)[-1]), "task A text):"))
    out.append(("S-21", "script", lambda old: "~~%s~~ **PARTIAL — re-scored %s (OPUS, on %s task B): N/A is false; %s. "
                "SWE2-AUDIT-SPEC: whether the table's decode is censused needs the page's §5/§7 read before MET, so the cell "
                "is PARTIAL until then**" % (old.strip(), D, SRC, proposed("S-21").split(": ", 1)[-1]), "task B): N/A is false"))
    out.append(("S-05", "script", lambda old: "%s — re-stated %s (OPUS, %s task B): %s" % (
        old.strip(), D, SRC, proposed("S-05")), "task B):"))
    out.append(("S-33", "script", lambda old: "%s — %s (OPUS, %s task B): no authored table or script reaches the pool; "
                "its resource link is the visual fetch `0024A5A0`" % (old.strip(), D, SRC), "visual fetch `0024A5A0`"))
    return out


SUMMARY_RE = re.compile(r"^\| contract column \| systems \| which \|\r?\n\|---\|---:\|---\|\r?\n(?:\|[^\n]*\r?\n){3}", re.M)
SUMMARY_NEW = ("*(The contract-column count table that stood here is retired, 2026-10-03 (OPUS): kept by hand, it drifted "
               "twice - 2026-09-21 and 2026-10-03, when it read MET 47 / SCOPE-SHORT 3 against rows reading 52 / 0. The "
               "rows below are the only source; `PROGRESS.md` and `checkpoint_consistency.py` (C3/C4) recount them.)*\n")


AMEND_MARK = "### Amendment — an exclusion may not drop registry-subject material (OPUS, 2026-10-03)"
AMEND = AMEND_MARK + """

*On AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003 (c), from SWE2-AUDIT-SPEC's expansion item 2 (`auditspec-l2-expansion-1003`,
`denominators.txt`), and under the user's root-cause directive (denominator and exclusion errors).*

**Rule.** A runtime cell may move material out of its denominator — invariant granularity (S-46's `380`), callee depth
(S-23), live-only observation (S-04/S-34), a contract's own disclosed static scope — **only when that material is not named
by the system's registry subject** (`important-subsystems.tsv` column 3 and the pages it lists). Material the registry
subject names is in the denominator whatever the contract's wording says: excluding it is not an exclusion, it is the
system scored on less than its subject, and the cell is MIXED or NOT MET until that material carries evidence or the
contract cell records a SCOPE-SHORT.

**Visibility.** A runtime cell that excludes anything names each excluded item and cites this amendment. The checkpoint
validator (`checkpoint_consistency.py` C9) lists every MET/LIVE runtime cell whose text carries exclusion wording
without that citation, so an exclusion can never leave readiness silently because the scorer does not count it.

**S-08.** Decided under this rule: its file layer is named by the registry subject and sits in no credited contract, so
the contract cell is SCOPE-SHORT (row above). Splitting the file layer into its own system was the alternative; it would
change the 52-system denominator and needs a ruling of its own, so it is not taken here.
"""


def run(apply):
    t = io.open(L2, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    lines = t.split(nl)
    idx = {}
    for i, l in enumerate(lines):
        m = re.match(r"^\| \*\*(S-\d+)\*\*", l)
        if m and l.count("|") >= 9 and m.group(1) not in idx:
            idx[m.group(1)] = i
    missing = []
    for row, col, make, marker in edits():
        i = idx[row]
        cells = lines[i].split("|")
        cur = cells[COL[col]]
        if marker in cur:
            continue
        if not apply:
            missing.append("%s %s" % (row, col))
            continue
        cells[COL[col]] = " " + make(cur) + " "
        if any("|" in c for c in cells[COL[col]:COL[col] + 1]):
            raise SystemExit("a literal | in the new %s %s cell" % (row, col))
        lines[i] = "|".join(cells)
    t2 = nl.join(lines)
    if SUMMARY_RE.search(t2):
        if apply:
            t2 = SUMMARY_RE.sub(SUMMARY_NEW.replace("\n", nl), t2, count=1)
        else:
            missing.append("summary table")
    if AMEND_MARK not in t2:
        if apply:
            t2 = t2.rstrip("\r\n") + nl + nl + AMEND.replace("\n", nl)
        else:
            missing.append("criterion amendment")
    if apply and t2 != t:
        io.open(L2, "w", encoding="utf-8", newline="").write(t2)
    for m in missing:
        print("NOT APPLIED", m)
    print("checks %d edits + summary  FAILS %d" % (len(edits()), len(missing)))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(run("--apply" in sys.argv))
