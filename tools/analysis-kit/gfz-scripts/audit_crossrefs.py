#!/usr/bin/env python3
"""
audit_crossrefs.py - mechanically detect documents that have gone stale or incomplete.

A document is not fact because someone wrote it down. This tool attacks the database with
the CURRENT program state and reports every place a document and the binary disagree.

It exists to catch the case nobody remembers to check: you document Movement, close it, and
three checkpoints later a newly-classified function proves Movement also feeds battle logic.
Nothing in a human workflow surfaces that. This does.

Checks performed per document:

  1. GHOST ADDRESS      a cited address is not a function in the current program
  2. BODY DRIFT         a cited body size disagrees with the current body extent
  3. CLASSIFICATION     a doc calls a function unresolved that is now classified,
                        or cites a classification that no longer matches its tags
  4. UNACCOUNTED NEIGHBOUR
                        a cited address has a caller/callee owned by a subsystem the
                        document never mentions  <- the "Movement touches battle" detector
  5. ORPHAN             a documented system's addresses gained new callers since the
                        recorded audit baseline (requires --baseline)

Inputs (regenerate both from the CURRENT parent before every audit pass):
  functions.tsv   DumpFullCoverageGraph.java  arg 1
  edges.tsv       DumpFullCoverageGraph.java  arg 2

Usage:
  audit_crossrefs.py --docs "<db root>" --functions functions.tsv --edges edges.tsv
                     [--baseline prev_report.json] [--out report.md] [--json report.json]

Exit code is 1 when any finding is reported, so it can gate a checkpoint.
"""
import argparse
import collections
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uc1_band

ADDR = re.compile(r'\b([0-9A-F]{8})\b')
# R5 (FABLE §9.2, voted; applied to the shipped instrument 2026-09-15 by OPUS).
#
# "A citation is a citation in any spelling." `ADDR` above is uppercase-bare only, so a page that
# cites its whole subject matter as `0x0022a0b0` or `FUN_0022a0b0` was INVISIBLE TO THIS PASS WHILE
# PASSING IT. Measured before the rule: 487 functions across 195 documents are cited only that way
# (§7). Demonstrated after it: writing one address in upper case on the Steam page imported six real
# edges at once, all of which had been there for days.
#
# Every spelling normalises to bare uppercase hex and is still filtered by `functions.tsv`
# membership downstream, so this widens the SPELLING accepted and not the population admitted.
# NARROWED per §9.7, which narrowed R5 on OPUS's own widening measurement: `0x`-prefixed hex in
# EITHER case and `FUN_` / `sub_` / `thunk_FUN_` names in either case, but **bare hex stays
# uppercase as shipped**. Bare lowercase moved no finding in either test (43/168 with and without
# it), and it is the one spelling that can match an eight-character hex word that is not an address
# at all - a digest fragment. The first version of this applied R5 wider than the rule it cites;
# corrected 2026-09-15 on FABLE-NOTICE-OPUS-R6-SCOPE-AND-R5-LOWERCASE.
ADDR_R5 = re.compile(r'\b0[xX]([0-9A-Fa-f]{8})\b')
ADDR_NAMED = re.compile(r'\b(?:thunk_FUN_|FUN_|sub_)([0-9A-Fa-f]{8})\b')


def cited_addresses(text):
    """Every address the document cites, in any of R5's accepted spellings, as bare uppercase.

    Kept separate from `ADDR` because `ADDR` is also the shape a BODY-SIZE row is matched against,
    and widening that would change a different check.
    """
    out = {m.group(1) for m in ADDR.finditer(text)}          # bare, uppercase only - as shipped
    for pat in (ADDR_R5, ADDR_NAMED):                        # 0x… and FUN_/sub_/thunk_, either case
        out.update(m.group(1).upper() for m in pat.finditer(text))
    return out
# `B` must END the size cell.  `\b` is satisfied by the `/` in `24 B/entry`, so a STRIDE in a
# stride column was read as a BODY EXTENT and its address reported as a GHOST -- a data address in
# a compliant data table, flagged as a defect it never had.
#
# **An undispositioned false positive is not free: it is the noise a real finding hides in.** That
# document sat with two continuously-red gates, both false, while carrying seven genuine BODY DRIFT
# findings nobody had looked at.
BODYSIZE = re.compile(r'`?([0-9A-F]{8})`?[^\n|]*\|\s*[^|\n]*\|\s*([\d,]+)\s*B(?:ytes)?\s*(?=\||$)',
                      re.M)
OWNER_PREFIX = "GFZ.V120.PrimaryOwner."
DOMAIN_PREFIX = "GFZ.V121.CodeDomain."

# R7's named substrate - see `is_substrate`.
NAMED_SUBSTRATE = {"0020E600", "0020E620", "00249C60"}

# R3 clause 1 (voted 3-0, 2026-09-15; FABLE §7.4, PASS22-WHAT-ACCOUNTING-MEANS.md §10).
#
# The alias test runs on BODY TEXT ONLY. A front-matter `status:` field and a link path into another
# layer's folder are pointers, not sentences about what crosses, and §4.2 asks for a sentence.
# FABLE's 14-pair sample of the clause-1 delta found only those two kinds and nothing else.
#
# The page's OWN folder path still counts, which is why `folder_low` is passed separately and is not
# stripped here.
CONTROL_WORD = re.compile(r"\bcontrol\b", re.I)
UNRES_PHRASE = re.compile(r"currently unresolved|still unresolved|\*\(unresolved\)\*", re.I)
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
LINK_TARGET = re.compile(r"\]\([^)]*\)")
INLINE_LINK_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*\S+\s*$", re.M)


# R6's section boundary. Both spellings are in the corpus - OPUS's pages head the section
# "Cross-subsystem neighbours" and FABLE's "Crossings into other layers" - and a rule that knows one
# of them silently does nothing on half the database.
CROSSING_SECTION = re.compile(
    r"^#{2,3} +(?:Cross-subsystem neighbours|Crossings into other layers)"
    r"[^\n]*\n.*?(?=^#{1,3} |\Z)", re.M | re.S)


def body_text(text):
    """The document minus its front matter and minus every link TARGET (link text is kept)."""
    t = FRONTMATTER.sub("", text)
    t = INLINE_LINK_DEF.sub("", t)
    return LINK_TARGET.sub("]", t)

# Subsystem vocabulary. A document "accounts for" a subsystem if any of these appear in it.
SUBSYSTEM_ALIASES = {
    "ActorEntity": ["actorentity", "actor entity", "actormanager", "actor/entity", "04-actor"],
    "Audio": ["audio", "sqex", "18-audio"],
    "CombatAI": ["combatai", "combat ai", "gambit", "09-combat-ai"],
    "CombatAction": ["combataction", "combat action", "battleunit", "07-combat-action"],
    "CombatFormula": ["combatformula", "combat formula", "08-combat-formula"],
    "CoreRuntimeScheduling": ["coreruntimescheduling", "core runtime", "main loop", "00-engine-core"],
    "Input": ["input", "15-input"],
    "Items/Equipment/Shops/License": ["items", "equipment", "shops", "license", "licence", "12-items"],
    "Movement": ["movement", "navigation", "locomotion", "06-movement"],
    "Party": ["party", "partyfocus", "11-party"],
    "Platform/Online/Achievements": ["platform", "achievements", "dxgi", "20-platform"],
    "Presentation": ["presentation", "rendering", "17-presentation"],
    "RNG": ["rng", "mt19937", "random", "21-rng"],
    "Resource": ["resource", "asset", "02-resource"],
    "Rewards/Progression/Economy": ["rewards", "progression", "economy", "13-rewards"],
    "Save/Load/Settings": ["save", "load", "settings", "saveimage", "19-save"],
    "Script/VM Native Bridge": ["scriptvm", "script vm", "ebp", "native bridge", "01-script"],
    "Spawn/Encounter/Lifecycle": ["spawn", "encounter", "lifecycle", "05-spawn"],
    "Status/Periodic/Terminal": ["status", "periodic", "terminal", "augment", "10-status"],
    "Story/Event/Quest/Hunt": ["story", "event", "quest", "hunt", "14-story"],
    "UI": ["ui", "menu", "screen", "16-ui"],
    "WorldAreaField": ["worldareafield", "world area", "worldfield", "field", "weather", "03-world"],
}


def load_functions(path):
    fn = {}
    with io.open(path, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        idx = {n: i for i, n in enumerate(header)}
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < len(header):
                continue
            e = p[idx["entry"]].upper()
            tags = p[idx["tags"]] if "tags" in idx else ""
            domains = [t[len(DOMAIN_PREFIX):] for t in tags.split(";")
                       if t.startswith(DOMAIN_PREFIX)]
            fn[e] = {
                "entry": e,
                "name": p[idx["name"]],
                "body_bytes": int(p[idx["body_bytes"]] or 0),
                "owner": p[idx["owner"]],
                "final_no": (p[idx["final_no_owner"]].lower() == "true"),
                "domains": domains,
                "classified": bool(p[idx["owner"]]) or
                              (p[idx["final_no_owner"]].lower() == "true") or
                              bool(domains),
            }
    # UC-1 band (2026-09-28 series break) when the input IS the shared census.
    if os.path.realpath(path) == os.path.realpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..",
            "work", "graph", "functions.tsv")):
        _b = uc1_band.load()
        for e in _b["removed"]:
            fn.pop("%08X" % e, None)
        for e, en in _b["extend"].items():
            k = "%08X" % e
            if k in fn:
                fn[k]["body_bytes"] = en - e
        for st, sz in _b["frontier"].items():
            k = "%08X" % st
            fn[k] = {"entry": k, "name": "UC1-FRONTIER-%s" % k,
                     "body_bytes": sz, "owner": "", "final_no": False,
                     "domains": [], "classified": False}
    return fn



def load_unlisted_blocks(db):
    """Registered blocks of .text the function list does not contain. -> [(start, end), ...]

    WHY THE GHOST CHECK NEEDS THIS. "Not a function in the current program" is true of two very
    different things: a DATA address a document mis-presented as code, and REAL CODE the exporter
    never created a function for. Pass 17 is `Data vs function`, so only the first is its subject;
    calling the second a ghost reports the census's shortfall as the document's defect.

    The corpus already measures the second and has since 2026-09-13 - 1,471 blocks in
    `99-Unresolved-Residual/Unlisted-Code/unlisted-code-blocks.tsv`, of which 142 are provably
    referenced by something in the image via a pass-6-admissible route (143 before 2026-09-17,
    when the .pdata route was split out of `unlisted_admissions.py`'s `referenced`). This reads that register rather than inventing a waiver
    list, so the two classes are separated by EVIDENCE ALREADY GATHERED and nothing is suppressed:
    a citation landing in a registered block is reported as UNLISTED CODE and counted on its own.
    """
    blocks = []
    for name in ("unlisted-code-blocks.tsv",):
        p = os.path.join(db, "99-Unresolved-Residual", "Unlisted-Code", name)
        if not os.path.isfile(p):
            continue
        for line in io.open(p, encoding="utf-8", errors="replace"):
            if line.startswith("#") or not line.strip():
                continue
            f = line.split("	")
            if len(f) < 2:
                continue
            try:
                start = int(f[0], 16)
                size = int(f[1])
            except ValueError:
                continue
            blocks.append((start, start + size))
    blocks.sort()
    return blocks


def in_unlisted(blocks, v):
    import bisect
    i = bisect.bisect_right(blocks, (v, float("inf"))) - 1
    return i >= 0 and blocks[i][0] <= v < blocks[i][1]


def load_edges(path):
    callers = collections.defaultdict(set)
    callees = collections.defaultdict(set)
    with io.open(path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 2:
                continue
            a, b = p[0].upper(), p[1].upper()
            callees[a].add(b)
            callers[b].add(a)
    return callers, callees


# Compiler/runtime substrate reached by almost every function. A CFG stub or CRT helper
# appearing as a "neighbour" says nothing about a system and only creates noise.
HUB_FANIN = 100   # see the measured distribution at the use site

SUBSTRATE = {"CompilerRuntime", "CompilerGeneratedEH", "CompilerGeneratedCpp",
             "CompilerGeneratedCFG", "Microsoft", "Thunk", "CxxStandardLibrary",
             "CxxObjectLifecycle", "EASTL"}


def is_substrate(rec):
    """True when the function ITSELF is compiler/runtime substrate.

    `subsystem_of` returns None for substrate, which is not the same question: an owned function
    and a substrate function both answer None only when the owner field is empty.  This asks
    directly, so a cited substrate address can be skipped as a SUBJECT and not only as a neighbour.
    """
    if not rec:
        return False
    # R7 (FABLE §9.6, voted; applied 2026-09-15 by OPUS). The image-address codec is substrate by
    # NAME, not by a generic caller cut. `0020E600` adds the base at `01F83530` to a 32-bit stored
    # offset and `0020E620` subtracts it again - ten and nine bytes, 815 and 279 callers, owned
    # between them by 21 and 11 subsystems. A pointer add called from twenty-one layers belongs to
    # none of them.
    #
    # Named rather than generic on purpose: a `callers > N` cut gives the same -12 today and would
    # silence the next hundred-caller function that is a real service, with nobody seeing it happen.
    #
    # `00249C60` (added 2026-09-18, FRONTIER ruling on OPUS-NOTICE-99-CALLERS): a 51-B
    # "play the current context's sound" leaf, 99 callers spanning the image by construction -
    # one under HUB_FANIN's measured cut yet substrate by the same definition. Its crossing is
    # already accountable through the-shared-neighbours-pass-22-keeps-finding.md, so naming it
    # here loses no reachable accounting.
    if rec.get("entry") in NAMED_SUBSTRATE:
        return True
    if rec["owner"]:
        return False
    for d in rec["domains"]:
        if d.split(".")[0] in SUBSTRATE:
            return True
    return False


def subsystem_of(rec):
    """Best subsystem label for a function: PrimaryOwner, else CodeDomain family."""
    if not rec:
        return None
    if rec["owner"]:
        return rec["owner"]
    for d in rec["domains"]:
        head = d.split(".")[0]
        if head in SUBSTRATE:
            return None
        if head in ("Phyre", "Bullet", "Lua", "EASTL", "Media", "Microsoft",
                    "CompilerGeneratedEH", "CompilerGeneratedCpp", "CompilerGeneratedCFG",
                    "Thunk", "CxxStandardLibrary", "CxxObjectLifecycle", "ThirdParty",
                    "NativeRoutine", "NativeAdapter", "NativeInline", "NativeLeaf",
                    "NativeDispatch", "Runtime", "Boundary", "Math", "Algorithm"):
            return None          # substrate / shape classes are not interesting neighbours
        return head
    return None


# Subsystem labels arrive from functions.tsv with underscores
# (`Items_Equipment_Shops_License`) while the alias keys above are written with slashes.
# Normalising both sides prevents a document that DOES discuss a subsystem from being
# reported as ignoring it - a false finding that trains readers to distrust the tool.
def _canon(s):
    """Canonical subsystem key: alphanumerics only.

    Normalising `/` and space to `_` was not enough.  The ledger writes
    `PlatformOnlineAchievements` (no separators at all) while the curated key is
    `Platform/Online/Achievements`, so the two normalised to `platformonlineachievements` and
    `platform_online_achievements` and **never met**.  The curated aliases -- `platform`,
    `achievements` -- therefore never applied, and a document writing the subsystem out in prose
    was still reported as ignoring it.  Third alias mismatch found in this table, and the first
    that survived a fix aimed at the same class of bug.
    """
    return re.sub(r"[^a-z0-9]", "", s.lower())


_ALIAS_NORM = {}
for _k, _v in SUBSYSTEM_ALIASES.items():
    _ALIAS_NORM[_canon(_k)] = _v


def register_domain_aliases(heads):
    """Register CodeDomain family heads, and merge them with the owner key they mean.

    The two taxonomies spell the same subsystem differently: the ledger's PrimaryOwner is
    `Save_Load_Settings` (87 functions) while the CodeDomain path head is `SaveLoad`, which
    exists ONLY as a domain.  `subsystem_of` falls back to the domain head for an unowned
    function, so the checker can report a subsystem under either taxonomy while the alias
    table knows only one of them.  **That recurs for every unowned neighbour whose domain
    head differs in spelling from its owner counterpart -- it is not one row to add.**

    Merging is by canonical PREFIX in either direction, so `saveload` and
    `saveloadsettings` share an alias list, and `rng` merges into `rngrandomselection`.
    """
    for head in sorted(heads):
        h = head.strip()
        if not h:
            continue
        key = _canon(h)
        forms = {h.lower(), h.lower().replace("_", " "), h.lower().replace("_", "")}
        forms.update(w for w in re.split(r"[_/ ]+", h.lower()) if len(w) > 3)
        _ALIAS_NORM.setdefault(key, [])
        for f in forms:
            if f and f not in _ALIAS_NORM[key]:
                _ALIAS_NORM[key].append(f)
    # R4 (FABLE ruling 2026-09-14, PASS22-WHAT-ACCOUNTING-MEANS.md 4.6, applied by OPUS):
    # A STEM MERGES ONLY WHEN ITS EXTENSIONS ARE ONE CHAIN OF SPELLINGS.
    #
    # The merge below was written for spelling variants - `saveload` / `saveloadsettings`,
    # `rng` / `rngrandomselection` - and it is sound when the longer keys are successive
    # spellings of ONE subsystem: core -> coreruntimescheduling, actor -> actorentity,
    # world -> worldarea -> worldareafield, storyevent -> storyeventquesthunt.
    #
    # It is NOT sound when the stem is shared by keys that BRANCH. `combat` is a prefix of
    # `combatai`, `combataction` and `combatformula`, which are three separately owned layers
    # with three separate folders, and the old loop chained all four into one alias list: after
    # that, the word "combat", "gambit" or "battleunit" on a page accounted for all three at
    # once. A shared stem is not a spelling of any one of its extensions.
    #
    # The test is structural, not a deny-list: sort a stem's extensions by length and require
    # each to be a prefix of the next. On today's table only `combat` fails it, and a future
    # label that branches is caught without anyone having to notice it.
    #
    # THIS RULE DOES NOT CLEAR ANYTHING. FABLE measured +124 findings across 87 pages, and the
    # pairs it opens are real crossings whose page speaks only a sibling's vocabulary.
    def _branching(stem):
        ext = sorted((k for k in _ALIAS_NORM if k != stem and k.startswith(stem)), key=len)
        return any(not ext[i + 1].startswith(ext[i]) for i in range(len(ext) - 1))

    for a in list(_ALIAS_NORM):
        for b in list(_ALIAS_NORM):
            if a == b:
                continue
            stem = b if a.startswith(b) else (a if b.startswith(a) else None)
            if stem is None or _branching(stem):
                continue
            merged = list(dict.fromkeys(_ALIAS_NORM[a] + _ALIAS_NORM[b]))
            _ALIAS_NORM[a] = merged
            _ALIAS_NORM[b] = merged


def register_ledger_aliases(owners):
    """Make every subsystem's OWN LEDGER SPELLING an accepted alias.

    The normalisation above was written to stop a document that discusses a subsystem being
    reported as ignoring it -- and it stopped one step short.  It normalises the KEYS on both
    sides and never adds the ledger's own spelling to the VALUES, so on 2026-09-02 a document
    dispositioning script-VM callers in the ledger's exact vocabulary, `Script_VM_Native_Bridge`,
    was reported as ignoring that subsystem: none of `scriptvm`, `script vm`, `ebp`,
    `native bridge`, `01-script` is a substring of the underscored form.  `InputGameplay` had no
    entry at all and passed only by accident, via the substring `input` inside a function name.

    That is worse than a false finding.  **A checker that a magic token can satisfy teaches authors
    to insert the token** -- the reporting session noticed they were one careless step from
    "fixing" a document by pasting a keyword, which is precisely what EVIDENCE-STANDARD warns
    against.  A hand-maintained alias list drifts from the ledger it describes; deriving the
    aliases from the ledger cannot.
    """
    for owner in owners:
        o = owner.strip()
        if not o:
            continue
        key = _canon(o)
        forms = {o.lower(), o.lower().replace("_", " "), o.lower().replace("_", "")}
        # Registering a key REPLACES the word-split fallback in doc_accounts_for, which fires only
        # when `_ALIAS_NORM.get(key)` is None.  Without the words below this "fix" would TIGHTEN
        # two subsystems instead of loosening them: `RNG_Random_Selection` had no alias entry, so
        # it fell back to ["random", "selection"] and matched ordinary prose -- while the three
        # derived forms are `rng_random_selection` / `rng random selection` /
        # `rngrandomselection`, none of which a human would ever write.  A document discussing RNG
        # correctly would have started being reported.
        #
        # **This is the same one-step-short shape as the defect being fixed**, committed while
        # fixing it, and it was caught by a peer asking whether the change could produce new
        # findings against their documents.  A change that only adds accepted spellings cannot;
        # a change that also switches off a fallback can.
        forms.update(w for w in re.split(r"[_/ ]+", o.lower()) if len(w) > 3)
        _ALIAS_NORM.setdefault(key, [])
        for f in forms:
            if f and f not in _ALIAS_NORM[key]:
                _ALIAS_NORM[key].append(f)


# --- R1: the registry of dispositions ---------------------------------------------------------
# Pass 22 fails on a neighbour that is "unexplained AND UNDISPOSITIONED". This half of the clause
# had no implementation: the registry carried 298 verdicts written by FABLE and SWE2-FRONTIER and
# the instrument could not see one of them. Applied 2026-09-14 (OPUS) on FABLE's ruling R1.
#
# ITS MEASURED EFFECT TODAY IS ONE PAIR, AND THE FIRST VERSION OF THIS COMMENT SAID OTHERWISE.
# It claimed "the pass could not go green however much work the fleet did", and that is wrong:
# all 298 verdict rows had ALREADY stopped being findings, because a CROSSING-ACCOUNTED verdict
# means the crossing was written into the page's prose, and prose satisfies the word test. The
# dispositioning work clears itself; only a verdict that adds NO prose - GENUINELY-IRRELEVANT,
# EDGE-ON-PAGE, FALSE-SUBJECT - needs this code, and exactly one such pair exists today.
#
# It matters more as the word test tightens (FABLE's R3): every alias dropped from the test is a
# page that can no longer clear a crossing by containing a common English word, and the registry
# becomes the mechanism rather than a record of one.
#
# The VERDICT COLUMN IS THE KEY; FABLE's relationship classes (SERVICE / CLIENT / DEPENDENCY /
# MECHANICAL / LABEL-UNSUPPORTED / OUT-OF-SCOPE) are what the note must SAY. This instrument reads
# the key and never judges the content - an instrument that graded prose would be a second opinion
# nobody voted for.
DISPOSITION_VERDICTS = {
    "CROSSING-ACCOUNTED",     # the document now names the crossing in prose near the citation
    "EDGE-ON-PAGE",           # the crossing is visible in the document's own structure
    "GENUINELY-IRRELEVANT",   # a mechanical neighbour, with the reason given per row
    "FALSE-SUBJECT",          # the cited subject was mis-seeded
}
DISPOSITION_FILE = os.path.join("_index", "candidates", "neighbour-dispositions.tsv")


def load_dispositions(db):
    """{(document, subsystem): verdict} plus the rows whose verdict is not in the vocabulary.

    -> (dispositioned, unknown). An UNKNOWN VERDICT IS NOT A DISPOSITION: a typo must not clear a
    finding silently, which is how a gate becomes decorative.
    """
    path = os.path.join(db, DISPOSITION_FILE)
    ok, unknown = {}, []
    if not os.path.isfile(path):
        return ok, unknown
    for line in io.open(path, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 6:
            continue
        doc, sub, verdict = f[0].strip().replace("\\", "/"), f[1].strip(), f[5].strip().upper()
        if not verdict:
            continue
        if verdict in DISPOSITION_VERDICTS:
            ok[(doc, sub)] = verdict
        else:
            unknown.append((doc, sub, verdict))
    return ok, unknown


_WORD_CACHE = {}


def doc_accounts_for(text_lower, folder_lower, subsystem):
    key = _canon(subsystem)
    aliases = _ALIAS_NORM.get(key)
    if aliases is None:
        # fall back to the individual words of the label
        aliases = [w for w in re.split(r"[_/ ]+", subsystem.lower()) if len(w) > 3]
    # R3 clause 2 (voted 3-0, 2026-09-15). WHOLE-WORD alias matching.
    #
    # Substring matching cannot hold R4. R4 separated the `combat` stem from CombatAI, CombatAction
    # and CombatFormula - and under substring matching, writing a correct disposition for any of the
    # three re-clears the stem through its own label. **A gate that undoes its own rule when it is
    # used correctly is broken whether it reports 219 or 0.** The same defect cleared `UI` through
    # the letters in `requires` and `ActorEntity` through `PackedACTORHandle`.
    #
    # Hyphenated folder aliases such as `15-input` keep working: `-` is a non-word character on
    # both sides.
    for alias in aliases:
        pat = _WORD_CACHE.get(alias)
        if pat is None:
            pat = _WORD_CACHE[alias] = re.compile(r"(?<![0-9a-z])" + re.escape(alias)
                                                  + r"(?![0-9a-z])")
        if pat.search(text_lower) or pat.search(folder_lower):
            return True
    return False


TRIPWIRE_HEADER = [
    "# PASS-22 TRIPWIRES - pairs held back from being findings by R6 ALONE.",
    "# REGENERATED BY audit_crossrefs.py ON EVERY RUN. Do not hand-edit: a snapshot goes stale",
    "# silently, and 'which of the forty moved' then becomes archaeology. That is the defect this",
    "# replaces (FABLE 2026-09-14 section 3).",
    "#",
    "# Each row becomes a live UNACCOUNTED NEIGHBOUR the moment any document names its far-end",
    "# subject OUTSIDE a crossing section. Not hypothetical: it happened at a1812431 (17:30) to a",
    "# zero measured at 60c846be (16:14), from one note.",
    "#",
    "# THIS FILE IS EVIDENCE, NOT VERDICTS. No row disposes of anything and it must not be copied",
    "# into neighbour-dispositions.tsv to keep a streak alive - a row written to keep a number",
    "# still is evidence produced to make a metric agree, and is inadmissible. The guard is",
    "# check_publish_neighbours.py, not a registry row.",
    "#",
    "# A page whose LAST section is its crossing section extends that section to end of file, so",
    "# appending there is safe and inserting above the heading is not. Found by a positive control",
    "# that failed first (61fc48ad).",
    "doc\tsubsystem\tedges\tdetail",
]


def write_tripwires(docs_root, tripwires):
    """Rewrite the tripwire register from this run.

    Only when the docs root actually has an `_index/candidates/` to write into, so a self-test or a
    scratch export - `check_publish_neighbours.py` runs the audit against a temporary HEAD worktree -
    produces no side effect on the real corpus."""
    cand = os.path.join(docs_root, "_index", "candidates")
    if not os.path.isdir(cand):
        return None
    path = os.path.join(cand, "pass22-tripwires.tsv")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(TRIPWIRE_HEADER) + "\n")
        for r in sorted(tripwires):
            f.write("%s\t%s\t%d\t%s\n" % r)
    print("wrote %s (%d tripwire row(s))" % (path, len(tripwires)), file=sys.stderr)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docs", required=True)
    ap.add_argument("--functions", required=True)
    ap.add_argument("--edges", required=True)
    ap.add_argument("--baseline")
    ap.add_argument("--out")
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    fn = load_functions(a.functions)
    # Derive the alias list from the ledger that produced the labels, so a document written in the
    # ledger's own vocabulary always satisfies the check.  See register_ledger_aliases.
    register_ledger_aliases({v["owner"] for v in fn.values()})
    register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
    callers, callees = load_edges(a.edges)
    baseline = {}
    if a.baseline and os.path.exists(a.baseline):
        with io.open(a.baseline, encoding="utf-8") as f:
            baseline = json.load(f).get("neighbours", {})

    findings = []
    dispositioned, unknown_verdicts = load_dispositions(a.docs)
    disposed = []
    # The code range, from the census itself. Used to keep the GHOST ADDRESS check off data.
    unlisted_blocks = load_unlisted_blocks(a.docs)
    _addrs = [int(a, 16) for a in fn]
    code_lo = min(_addrs) if _addrs else 0
    code_hi = (max(_addrs) + 0x1000) if _addrs else 0
    neighbours_now = {}
    tripwires = []

    for dirpath, _dirs, files in os.walk(a.docs):
        if os.sep + "_templates" in dirpath:
            continue
        for name in sorted(files):
            if not name.lower().endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, a.docs).replace(os.sep, "/")
            with io.open(path, encoding="utf-8") as f:
                text = f.read()
            if "_index/" in rel or rel.startswith("_"):
                continue

            # R3 clause 1: the alias test sees body text only (link targets stripped); the folder
            # path is passed separately and still counts.
            folder_low = rel.lower()
            # The ACCOUNTING text is the crossing sections only, not the document (FABLE contra
            # FABLE-CONTRA-CROSSREF-PROSE-WORD-CLEARS-A-LAYER, ruled 2026-09-22). Aliases like
            # `input`, `party`, `world`, `movement`, `audio` and `application` are ordinary
            # English: under whole-document matching a page that *discusses* a layer in prose was
            # credited with *dispositioning* its crossings - a silent permissive clear. A layer is
            # accounted for when a page names it where dispositions live (a crossing/neighbours
            # section) or when the page's own folder is that layer's - kept via folder_low.
            xlow = "".join(m.group(0) for m in CROSSING_SECTION.finditer(
                body_text(text))).lower()
            # R5: every accepted spelling, normalised.
            cited = sorted(cited_addresses(text))
            if not cited:
                continue

            # An address cited ONLY on control lines is an INSTRUMENT CONTROL, not a subject.
            #
            # We have spent this session pushing every session to name its controls in the document,
            # which is right -- and the consequence is that every control address drags its whole
            # neighbourhood into this check.  `00378540` appears in the glyph document exactly once,
            # as *"positive control 2: 00378540 -> MWeather PASS"*, and the checker inherited its
            # Resource edges as a claim the document never made.
            #
            # **Publishing your controls should not cost audit noise.** That is a tool decision, not
            # a document one -- the alternative is authors quietly dropping controls from documents
            # to keep a gate green, which is the token-satisfaction failure aimed at the evidence
            # rather than at the prose.
            #
            # Narrow by construction: an address survives as a subject if it appears even ONCE on a
            # line that is not a control line, so a real subject that also happens to serve as a
            # control is unaffected.
            # NOTE: `a` is the argparse namespace in this function.  The first version of this
            # block used `for a in cited:` and left `a` bound to an address string, so the NEXT
            # document in the walk died on `a.docs` with `AttributeError: 'str' object has no
            # attribute 'docs'`.  Single-document runs passed; every category-wide run crashed.
            # **A loop variable is a claim about the enclosing scope.**
            control_only = set()
            doc_lines = text.split("\n")
            # Case-insensitive since R5: the same address can be written `0022A0B0`, `0x0022a0b0`
            # or `FUN_0022a0b0`, and a control line naming the lowercase form would otherwise not
            # be recognised as the line that cites it.
            lines_upper = [ln.upper() for ln in doc_lines]
            # 2026-10-03 (OPUS): the control test per line once, not once per (address, line) - same result.
            is_control = [bool(CONTROL_WORD.search(ln)) for ln in doc_lines]
            for cited_addr in cited:
                idxs = [i for i, ln in enumerate(lines_upper) if cited_addr in ln]
                if idxs and all(is_control[i] for i in idxs):
                    control_only.add(cited_addr)
            cited = [c for c in cited if c not in control_only]

            # R6 (FABLE §9.4, voted, GUARDED; applied 2026-09-15 by OPUS, with or before R5 and
            # never after, per the ruling's own ordering).
            #
            # A function named ONLY inside a page's pass-22 crossing section is the far end of an
            # edge that section is accounting for, not a subject the page documents. Without this,
            # **writing a correct disposition creates findings about functions the page never
            # discusses** - the mechanism §9.3 predicted from a census and §9.8 then met three times
            # in one afternoon, for six edges.
            #
            # GUARDED: the exclusion applies only when the function is adjacent in `edges.tsv` to a
            # function the page cites OUTSIDE the section. That adjacency is *why* a correct note
            # names it. Without the guard a crossing section becomes a place to park a real subject
            # out of the pass's sight, and the unguarded form clears five pairs whose functions are
            # adjacent to nothing outside.
            far_ends = set()
            sec_spans = [m.span() for m in CROSSING_SECTION.finditer(text)]
            if sec_spans:
                outside = text
                for lo, hi in reversed(sec_spans):
                    outside = outside[:lo] + outside[hi:]
                outside_cited = cited_addresses(outside)
                for cited_addr in cited:
                    if cited_addr in outside_cited:
                        continue
                    near = {x.upper() for x in callers.get(cited_addr, ())} | \
                           {x.upper() for x in callees.get(cited_addr, ())}
                    if near & outside_cited:
                        far_ends.add(cited_addr)
            # SCOPED TO THE NEIGHBOUR ENUMERATION ONLY. The first version removed far ends from
            # `cited` outright, which also took them out of checks 1-3 - ghost address, body drift
            # and classification drift. R6's justification says nothing about those: it says a
            # function named as the far end of an accounted edge is not a SUBJECT whose neighbours
            # the page must account for. **It does not say a size quoted beside that far end may be
            # wrong.** Removing it from the body-drift check would let exactly that escape.
            # Raised by FABLE (FABLE-NOTICE-OPUS-R6-SCOPE-AND-R5-LOWERCASE) with the measurement
            # that it hides nothing today, which is the reason to fix it now rather than after it
            # does. Corrected 2026-09-15.

            # ---- 1. ghost addresses / 2. body drift / 3. classification drift
            # Note on what survives this filter: an address in the code range, cited with a size,
            # and absent from the census is a fact about the CENSUS as often as about the document.
            # 002FE7D0 is a live 106-byte handler reached only through a table pointer, and the
            # census does not contain it; 00431410 is a jump table that happens to live in .text.
            # Both are findings worth surfacing and neither is a defect.
            declared_sizes = {m.group(1).upper(): int(m.group(2).replace(",", ""))
                              for m in BODYSIZE.finditer(text)}
            has_unres = UNRES_PHRASE.search(text) is not None
            for addr in cited:
                rec = fn.get(addr)
                if rec is None:
                    # Globals/tables are cited too and are legitimately not functions.
                    # Only flag when the doc presents it as a function (name/body given) AND the
                    # address is in the code range. A BODY size is a FUNCTION body's size, and a
                    # data address cannot have one - so `022D9300 | the input point | 16 B` is a
                    # DATA size and was never capable of being a defect. That shape produced 20 of
                    # the 22 findings this class had, which made a genuine ghost invisible inside
                    # it. The range comes from the census itself; no new input is needed.
                    if addr in declared_sizes and code_lo <= int(addr, 16) < code_hi:
                        # Registered unlisted code is a CENSUS shortfall, not a document defect,
                        # and pass 17 is about data cited as a function. Reported, never dropped.
                        if in_unlisted(unlisted_blocks, int(addr, 16)):
                            findings.append(("UNLISTED CODE", rel, addr,
                                             "real .text the function list does not contain - "
                                             "registered in Unlisted-Code/unlisted-code-blocks.tsv; "
                                             "census debt, not a document defect"))
                        else:
                            findings.append(("GHOST ADDRESS", rel, addr,
                                             "cited with a body size but is not a function "
                                             "in the current program"))
                    continue
                if addr in declared_sizes and declared_sizes[addr] != rec["body_bytes"]:
                    findings.append(("BODY DRIFT", rel, addr,
                                     "document says %d B, current body is %d B"
                                     % (declared_sizes[addr], rec["body_bytes"])))
                # 2026-10-03 (OPUS): the per-address pattern can only match when the page holds one of the
                # three phrases and only matters for a classified body; test those first (same findings,
                # ~53k fewer one-off regex compiles per run).
                calls_unres = rec["classified"] and has_unres and re.search(
                    r'`?' + addr + r'`?[^\n]{0,400}?(currently unresolved|still unresolved|'
                    r'\*\(unresolved\)\*)', text, re.I)
                if calls_unres and rec["classified"]:
                    findings.append(("CLASSIFICATION", rel, addr,
                                     "document calls it unresolved; it is now classified as "
                                     + (rec["owner"] or ";".join(rec["domains"]))))

            # ---- 4. unaccounted neighbours
            seen = {}
            # THE TRIPWIRES, COMPUTED IN THE SAME PASS (FABLE 2026-09-14 section 3: the population
            # "should be regenerated by the audit on every run"). A tripwire is a pair that R6 and
            # R6 ALONE holds back: the far end is excluded as a SUBJECT here, and the moment any
            # document names it outside a crossing section it becomes one and this pair becomes a
            # finding. FABLE suggested measuring it as "R6 on minus R6 off", which is two full
            # sweeps; the same answer falls out of one, because the only difference between the two
            # runs is which addresses reach the enumeration below.
            trip = {}
            acct_memo = {}
            for addr in cited:
                if addr not in fn:
                    continue
                # R6 applies HERE and nowhere else: a function named only as the far end of an
                # accounted edge is not a subject whose neighbourhood this page must account for.
                # It is still a subject for checks 1-3 above, because the rule says nothing about
                # whether a size or a classification quoted beside it is right.
                held_by_r6 = addr in far_ends
                # The SUBSTRATE test was applied to the NEIGHBOUR only, never to the CITED side.
                # So a document citing `0016D6A0` -- `_guard_check_icall`, which every indirect call
                # in the image passes through -- imported its **2,479 distinct callers across 16
                # owner subsystems** as unaccounted neighbours.  On 2026-09-03 that produced
                # **8 of 20** findings against `15-Input`, none of them an input relationship;
                # enumerating them would have said only that the executable uses CFG.
                #
                # **A substrate function is uninformative as a subject for exactly the reason it is
                # uninformative as a neighbour**, and the asymmetry was invisible because the
                # findings looked like real cross-subsystem edges.
                if is_substrate(fn.get(addr)):
                    continue
                # A HUB is uninformative as a subject for the same reason substrate is: its
                # caller set spans the image by construction, so importing it says nothing
                # about the citing document.  `is_substrate` misses hubs that carry a real
                # PrimaryOwner -- `ImageAddress_ResolveRuntimePointer` (`0020E600`) has **815
                # callers across 18 owners** and is classified `CoreRuntimeScheduling`, and it
                # alone produced four of five CoreRuntimeScheduling findings in one category.
                #
                # Threshold measured, not guessed, over the 19,995 functions with >=1 caller:
                #   p50=1  p75=2  p90=5  p95=9  p99=46  p99.5=76  p99.9=461  max=2479
                # >100 callers is **74 functions, 0.37%** of called functions -- far out on the
                # tail, and it captures both known hubs (815 and 2,479) while leaving ordinary
                # shared accessors alone.
                if len(callers.get(addr, ())) > HUB_FANIN:
                    continue
                for direction, table in (("caller", callers), ("callee", callees)):
                    for other in table.get(addr, ()):
                        # R7 applies on the NEIGHBOUR side, which is the side UQ-35 asked about.
                        # `is_substrate` alone was not enough: the codec pair is OWNED by
                        # CoreRuntimeScheduling, so `subsystem_of` answers with a real subsystem and
                        # the pair went on importing that layer into every page whose functions
                        # unpack a 32-bit stored pointer. Applying the named-substrate test here is
                        # what FABLE's -12 measured.
                        if is_substrate(fn.get(other)):
                            continue
                        sub = subsystem_of(fn.get(other))
                        if not sub or sub in SUBSTRATE:
                            continue
                        # 2026-10-03 (OPUS): memoised per document - xlow and folder_low are fixed for the page.
                        acc = acct_memo.get(sub)
                        if acc is None:
                            acc = acct_memo[sub] = doc_accounts_for(xlow, folder_low, sub)
                        if not acc:
                            (trip if held_by_r6 else seen).setdefault(sub, []).append(
                                (addr, direction, other))
            neighbours_now[rel] = sorted(seen.keys())
            # THE EDGE LIST IS SORTED BEFORE IT IS SAMPLED OR PRINTED, and that is not cosmetic.
            # The hits arrive in the traversal order of an upstream set, so two runs over identical
            # inputs produced the same rows with the members permuted - and, where a list is
            # truncated to four, a different four. Consequences, both real and both seen:
            #   * `pass22-tripwires.tsv` showed up modified after every regeneration (8 lines on
            #     2026-09-14), so the register's diff was noise and a reviewer reading it learned
            #     nothing about the corpus.
            #   * `check_publish_neighbours.py` compares findings as tuples INCLUDING this detail
            #     string, so a permutation made one run's finding differ from the next run's and the
            #     guard could report an added or accounted-for neighbour that was neither.
            # Determinism is a precondition for both files meaning what they say.
            for d in (trip, seen):
                for sub in d:
                    d[sub].sort()
            for sub, hits in sorted(trip.items()):
                # A PAIR THE REGISTRY ALREADY ANSWERS IS NOT A TRIPWIRE. The first cut of this
                # reported 94 rows against the 40 measured by diffing FINDINGS with R6 on and off,
                # and the whole difference is R1: promoting a far end makes the pair a SUBJECT, and
                # a subject the registry disposes is reported-not-failed, so it cannot reset a
                # streak. 54 of the 94 are in that state. Counting them would have overstated the
                # risk by more than double and made the register mean something other than its name.
                if (rel, sub) in dispositioned:
                    continue
                tripwires.append((rel, sub, len(hits),
                                  "; ".join("%s %s %s" % h for h in hits[:4])))
            for sub, hits in sorted(seen.items()):
                sample = hits[:4]
                detail = "; ".join("%s %s %s" % (h[0], h[1], h[2]) for h in sample)
                if len(hits) > len(sample):
                    detail += " (+%d more)" % (len(hits) - len(sample))
                # R1: a registry verdict clears the pair. Reported in its own class, never dropped.
                verdict = dispositioned.get((rel, sub))
                if verdict:
                    disposed.append((rel, sub, verdict, len(hits)))
                    continue
                findings.append(("UNACCOUNTED NEIGHBOUR", rel, sub,
                                 "%d edge(s) to/from %s, never mentioned: %s"
                                 % (len(hits), sub, detail)))

            # ---- 5. new neighbours since baseline
            if rel in baseline:
                new = sorted(set(neighbours_now[rel]) - set(baseline[rel]))
                for sub in new:
                    findings.append(("NEW SINCE BASELINE", rel, sub,
                                     "subsystem relationship appeared since the last audit - "
                                     "REOPEN this document"))

    # ---------------- report ----------------
    by_kind = collections.Counter(f[0] for f in findings)
    lines = ["# Cross-reference audit report", ""]
    lines.append("Generated against the current program state. Every finding is a place a")
    lines.append("document and the binary disagree, or a relationship the document does not")
    lines.append("account for. **Findings are not automatically defects** - some neighbours are")
    lines.append("genuinely irrelevant - but each one must be dispositioned, not ignored.")
    lines.append("")
    lines.append("| Finding | Count |")
    lines.append("|---|---:|")
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        lines.append("| %s | %d |" % (k, v))
    lines.append("| **total** | **%d** |" % len(findings))
    lines.append("")
    if findings:
        cur = None
        for kind, rel, subj, detail in sorted(findings):
            if kind != cur:
                lines.append("")
                lines.append("## " + kind)
                lines.append("")
                cur = kind
            lines.append("- **%s** — `%s` — %s" % (rel, subj, detail))
    else:
        lines.append("No findings. Every documented address resolves, every body size matches,")
        lines.append("and every cross-subsystem neighbour is accounted for in prose.")
    report = "\n".join(lines) + "\n"

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
        print("wrote %s" % a.out, file=sys.stderr)
    if a.json:
        with io.open(a.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"findings": findings, "neighbours": neighbours_now,
                       "tripwires": tripwires}, f, indent=2)
        print("wrote %s" % a.json, file=sys.stderr)
    write_tripwires(a.docs, tripwires)
    if not a.quiet and not a.out:
        print(report)

    if disposed:
        import collections as _c
        hist = _c.Counter(v for _d, _s, v, _n in disposed)
        print("dispositioned by the registry, reported not failed: %d pair(s) - %s"
              % (len(disposed), ", ".join("%s %d" % (k, n) for k, n in sorted(hist.items()))),
              file=sys.stderr)
    if unknown_verdicts:
        print("REGISTRY ROWS WITH A VERDICT OUTSIDE THE VOCABULARY - NOT dispositioned: %d"
              % len(unknown_verdicts), file=sys.stderr)
        for doc, sub, v in unknown_verdicts[:6]:
            print("    %-58s %-22s %s" % (doc[:58], sub, v), file=sys.stderr)
    print("audit: %d finding(s) across %d document(s)"
          % (len(findings), len(neighbours_now)), file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
