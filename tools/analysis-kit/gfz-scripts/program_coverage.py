#!/usr/bin/env python3
"""program_coverage.py - the charter section 9 multidimensional coverage report.

Why this exists
---------------
`progress.py` emits a single weighted composite percentage. Charter section 9 explicitly forbids
relying on one number, because it collapses three different states that must stay separate:

    "we found most functions"  !=  "we understand most functions"  !=  "we could reimplement them"

This script reports each dimension independently, always with its denominator, and prints
**UNMEASURED** with a reason rather than inventing a number for a dimension the current data cannot
support. An empty cell is a finding; a fabricated one is a lie that compounds.

Honesty rules encoded here
--------------------------
1. Every ratio prints its denominator.
2. A proxy is labelled a proxy. "Address appears in a document" is evidence of *citation*, not of
   *understanding*, and is reported under that name.
3. Caller/callee counts EXCLUDE edges whose caller is a `CompilerGeneratedEH` funclet or catch
   handler. Those are banned as semantic evidence (mission prompt), and `edges.tsv` contains 3,834
   of them. See EC-1.
4. Generated families (unwind funclets, thunks, reflection stubs) are counted separately from code
   a human would have to reimplement, because including them inflates every denominator.

Usage
-----
    python program_coverage.py --db "<database dir>" [--work <Tools/work dir>] [--out FILE]
"""
import argparse
import collections
import hashlib
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uc1_band

HEX8 = re.compile(r"^[0-9A-F]{8}$")
ANY_HEX8 = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")

# Tag substrings that mark compiler/template output rather than authored engine behaviour.
GENERATED = (
    "CompilerGeneratedEH",
    "CompilerGeneratedCFG",
    "CompilerGeneratedCpp",
    "Runtime.Callback.ReturnValueAdapter",
    "Runtime.Callback.OwnedBufferResetAdapter",
    "Reflection.PClassDescriptorForType",
    "Reflection.DataMemberMetadataStaticTeardown",
    "Reflection.ClassDescriptorStaticTeardown",
    "Reflection.AnnotationStaticTeardown",
    "Reflection.ReflectionStaticTeardown",
    "Reflection.ObjectTraversalAdapter",
    "ScriptVM.ObjectPushAdapter",
    "ScriptVM.NullableObjectPushAdapter",
    "Thunk.",
)
UNNAMED = re.compile(r"^(FUN_|Unwind@|Catch_All@|thunk_FUN_|j_FUN_|caseD_|switchD_)")
# `ANY_HEX8` requires a non-word character before the digits, so `FUN_002f9860` -- the GFZ
# ledger's own spelling for an unnamed function -- was not counted as a citation of
# 002F9860. Measured 2026-09-08: 226 authored functions were cited only that way, including
# a 160-caller resolver that a document had read line by line.
SYMBOL_HEX8 = re.compile(r"(?:FUN|LAB|DAT|PTR|SUB|UNK|thunk_FUN)_(0[0-9A-Fa-f]{7})", re.I)
BACKTICK_HEX8 = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})`")
FENCED = re.compile(r"```.*?```", re.S)
# A sha256 opens with eight hex digits and every document states the exe hash.
LONGHEX = re.compile(r"\b(0[0-9A-Fa-f]{7})[0-9A-Fa-f]{8,}")


def cited_addresses(text):
    """Three forms that cannot be anything but an address reference.

    A code span holding just the address; a GFZ symbol containing it (`FUN_002f9860` --
    the ledger's spelling for every UNNAMED function, so the form most often used for
    exactly the functions a coverage query hunts for); and a quoted disassembly listing.

    A bare address in a SENTENCE is deliberately not among them. This function used to
    count those, and they cannot be told from a constant of the same width: `+0x118 =
    0x003C0000` read as a citation of FUN_003bfff0, and `0x00555556` -- the compiler's
    divide-by-3 magic -- as one of 00555400. Dropping the form costs 9 of 6195; adding
    the symbol form gains 226. Same rule as `knowledge_db.cited` and `gen_address_index`.
    """
    t = LONGHEX.sub(" ", text)
    out = set(m.group(1).upper() for m in BACKTICK_HEX8.finditer(t))
    out |= set(m.group(1).upper() for m in SYMBOL_HEX8.finditer(t))
    for blk in FENCED.findall(t):
        out |= set(m.group(1).upper() for m in ANY_HEX8.finditer(blk))
    return out

# Charter section 8 confidence labels and section 2 readiness rungs.
CONFIDENCE = ["PROVEN", "VERY HIGH CONFIDENCE", "HIGH CONFIDENCE", "PROBABLE",
              "HYPOTHESIS", "UNKNOWN", "CONTRADICTED", "SUPERSEDED"]
READINESS = ["DISCOVERED", "CLASSIFIED", "SEMANTICALLY UNDERSTOOD", "TYPE RESOLVED",
             "DEPENDENCIES RESOLVED", "RUNTIME VALIDATED", "BEHAVIORAL CONTRACT READY",
             "IMPLEMENTATION READY", "IMPLEMENTED", "PARITY TESTED", "PARITY CERTIFIED"]
# Words that would indicate a claim was checked against a live process.
RUNTIME_MARKERS = ("cheat engine", "breakpoint", "livelab", "live process", "runtime trace",
                   "observed in game", "debugger", "attached to the process", "tier 10",
                   "runtime-confirmed", "runtime confirmed")

# THE METRIC COUNTED DENIALS AS CITATIONS (DR-1). A plain substring test scores a document that
# says *"Nothing in this contract has been observed in a live process"* exactly as it scores one
# that reports a breakpoint. Two contracts in the corpus carry that sentence verbatim.
#
# OPUS measured the size of it on 2026-09-14: of 26 documents carrying a marker, 9 have every
# occurrence negated and 4 are mixed, so the true value is **at least 13 and at most 17**. The floor
# was the soft end, because a 110-character negation window catches a sentence and cannot see a
# marker sitting under a "What this document does not claim" heading.
#
# So negation is tested at two scales, and a document counts only if SOME occurrence survives both:
#   SENTENCE  the marker's own sentence denies it.
#   SECTION   the marker sits under a heading that declares the section is about what is not
#             claimed, not observed, or not established. The whole section is a denial.
NEGATION = re.compile(
    r"\b(?:no|not|never|none|nothing|nobody|without|absent|lacks?|lacking|cannot|can't|"
    r"unconfirmed|unobserved|untested|unverified|awaits?|awaiting|would need|needs? a)\b", re.I)
DENIAL_HEADING = re.compile(
    r"^#{1,6}\s+.*\b(?:does not claim|not claimed|what is not|is not known|not established|"
    r"not observed|no runtime|without runtime|limitations?|caveats?)\b.*$", re.I | re.M)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n\n")


def _denied_sections(text):
    """(start, end) spans of every section headed as a statement of what is NOT claimed."""
    spans = []
    for m in DENIAL_HEADING.finditer(text):
        level = len(m.group(0)) - len(m.group(0).lstrip("#"))
        nxt = re.compile(r"^#{1,%d}\s" % max(level, 1), re.M).search(text, m.end())
        spans.append((m.start(), nxt.start() if nxt else len(text)))
    return spans


def cites_runtime_evidence(text):
    """True when at least one runtime marker is NOT inside a denial.

    Returns False for a document whose only mentions are denials - which is the whole point, and
    the reason this is a function rather than an `any(m in text)`.
    """
    low = text.lower()
    denied = _denied_sections(text)
    for marker in RUNTIME_MARKERS:
        start = 0
        while True:
            i = low.find(marker, start)
            if i < 0:
                break
            start = i + 1
            if any(a <= i < b for a, b in denied):
                continue                       # the section says it is not claiming this
            # the marker's own sentence
            lo = max(0, low.rfind(".", 0, i) + 1, low.rfind("\n\n", 0, i))
            hi = len(low)
            for end_m in SENTENCE_SPLIT.finditer(low, i):
                hi = end_m.start()
                break
            if NEGATION.search(text[lo:hi]):
                continue                       # the sentence denies it
            return True
    return False


def die(msg):
    sys.stderr.write("program_coverage: %s\n" % msg)
    raise SystemExit(2)


def read_tsv(path, required=True):
    if not os.path.exists(path):
        if required:
            die("missing required input: %s" % path)
        return None, []
    rows = []
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        for ln in fh:
            p = ln.rstrip("\n").split("\t")
            if p and p[0]:
                rows.append(p)
    return head, rows


def load_functions(work):
    head, rows = read_tsv(os.path.join(work, "graph", "functions.tsv"))
    idx = {n: i for i, n in enumerate(head)}
    fns = {}
    for p in rows:
        if not HEX8.match(p[0]):
            continue
        try:
            size = int(p[idx["body_bytes"]])
        except (KeyError, ValueError, IndexError):
            size = 0
        tags = p[idx["tags"]] if idx.get("tags", -1) < len(p) else ""
        fns[p[0]] = {
            "size": size,
            "name": p[idx["name"]] if idx.get("name", -1) < len(p) else "",
            "owner": p[idx["owner"]] if idx.get("owner", -1) < len(p) else "",
            "thunk": (p[idx["thunk"]].lower() == "true") if idx.get("thunk", -1) < len(p) else False,
            "tags": tags,
            "generated": any(g in tags for g in GENERATED),
            "eh": "CompilerGeneratedEH" in tags,
        }
    # UC-1 band (2026-09-28 series break) when `work` is the shared tree: the
    # frontier bodies are authored-class (no generated tags, not thunks), the
    # removed entry must leave the authored count, and extensions re-size.
    path = os.path.join(work, "graph", "functions.tsv")
    canonical = os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "work",
        "graph", "functions.tsv")
    if os.path.realpath(path) == os.path.realpath(canonical):
        _b = uc1_band.load()
        for e in _b["removed"]:
            fns.pop("%08X" % e, None)
        for e, en in _b["extend"].items():
            k = "%08X" % e
            if k in fns:
                fns[k]["size"] = en - e
        for st, sz in _b["frontier"].items():
            k = "%08X" % st
            fns[k] = {"size": sz, "name": "UC1-FRONTIER-%s" % k,
                      "owner": "", "thunk": False, "tags": "",
                      "generated": False, "eh": False}
        # the chained-tails extent rule (2026-09-30): listed extents grow to their adjudicated errata ends
        grown, _x = uc1_band.apply_extents({int(k, 16): v["size"] for k, v in fns.items()})
        for e, sz in grown.items():
            fns["%08X" % e]["size"] = sz
        EXTENT_INFO.update(_x)
    return fns


EXTENT_INFO = {}


def load_edges(work, fns):
    _, rows = read_tsv(os.path.join(work, "graph", "edges.tsv"))
    total = 0
    eh_sourced = 0
    callers = collections.defaultdict(set)
    callees = collections.defaultdict(set)
    eh_only_targets = set()
    for p in rows:
        if len(p) < 2 or p[0] == "caller":
            continue
        a, b = p[0].upper(), p[1].upper()
        total += 1
        if fns.get(a, {}).get("eh"):
            eh_sourced += 1
            eh_only_targets.add(b)
            continue                      # EC-1: banned as semantic evidence
        callers[b].add(a)
        callees[a].add(b)
    return total, eh_sourced, callers, callees, eh_only_targets


def load_docs(db):
    docs = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in ("_templates",)]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, db).replace("\\", "/")
            if rel.startswith("_index/_inbox/"):
                continue                  # peer inboxes are raw notes, not canonical documents
            text = io.open(path, encoding="utf-8", errors="replace").read()
            fm = {}
            if text.startswith("---"):
                end = text.find("\n---", 3)
                if end > 0:
                    for line in text[3:end].split("\n"):
                        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
                        if m:
                            fm[m.group(1)] = m.group(2).strip()
            docs.append({"rel": rel, "text": text, "fm": fm,
                         "index": rel.startswith("_index/")})
    return docs


def pct(n, d):
    return "-" if not d else "%.2f %%" % (100.0 * n / d)


def _canonical_work():
    return os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "work")


def input_fp(db, work):
    """sha-256 over every input this report consumes, complete bytes.

    The derived-data rule (_index/EVIDENCE-POLICY.md): a generated file proves
    its currency by carrying the fingerprint of what it read. The set mirrors
    main()'s consumption exactly: the doc walk's own exclusions are honoured
    (`.md` under `_index/_inbox/` and in `_templates/` dirs are never read),
    every `.tsv` under db IS hashed because the side-file census reads all of
    them - which also covers the `_types` store, the UC-1 band TSVs and
    `_index/FUNCTION-EXTENT-ERRATA.tsv` - and `Reconstruction/` contributes
    NAMES only, because only the file list is counted there. Absent optional
    inputs are hashed as MISSING: an appearing input must move the fp.
    """
    h = hashlib.sha256()

    def feed_bytes(rel, path):
        h.update(rel.replace("\\", "/").encode("utf-8") + b"\0")
        with io.open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)

    def feed_missing(rel):
        h.update(rel.replace("\\", "/").encode("utf-8") + b"\0MISSING\0")

    for rel in ("graph/functions.tsv", "graph/edges.tsv",
                "h78/rip_data_refs.tsv", "h94/phyre_schema.tsv"):
        p = os.path.join(work, rel)
        if os.path.exists(p):
            feed_bytes("work/" + rel, p)
        else:
            feed_missing("work/" + rel)
    # whether the UC-1 band/extent rules apply is itself an input: the same
    # bytes produce different figures when `work` is not the canonical tree.
    h.update(b"canonical_work=%d\0" % (os.path.realpath(
        os.path.join(work, "graph", "functions.tsv")) ==
        os.path.realpath(os.path.join(_canonical_work(),
                                      "graph", "functions.tsv"))))
    md_seen, tsv_seen = [], []
    # The artifact itself is not an input (the progress-report rule, CKPT10R3):
    # hashing the previous generation would make the fingerprint self-
    # referential and unreproducible. Its own content barely feeds the report
    # anyway - _index docs are neither system docs, readmes nor contracts.
    own = os.path.realpath(os.path.join(db, "_index", "COVERAGE-DIMENSIONS.md"))
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in ("_templates",)
                   and not (os.path.relpath(root, db) == "_index"
                            and d == "progress")]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, db).replace("\\", "/")
            # PROGRESS.md and _index/progress/ are consumed (a readme row, and
            # index docs in the corpus) but are DOWNSTREAM artifacts: the
            # publish pipeline regenerates them from bound inputs that include
            # this very file, so hashing them makes the fingerprint stale at
            # birth (observed at 04387af2f). They are excluded from the input
            # set, not from consumption.
            if rel.startswith("_index/_inbox/") or os.path.realpath(p) == own \
                    or rel == "PROGRESS.md" or rel.startswith("_index/progress/"):
                continue
            md_seen.append(p)
    for p in sorted(md_seen):
        feed_bytes("db/" + os.path.relpath(p, db), p)
    # the side-file census walks db WITHOUT exclusions (line ~"for _r, _d, _f
    # in os.walk(db)"), so the .tsv input set is everything, _templates
    # included.
    for root, dirs, files in os.walk(db):
        for f in files:
            if f.endswith(".tsv"):
                tsv_seen.append(os.path.join(root, f))
    for p in sorted(tsv_seen):
        feed_bytes("db/" + os.path.relpath(p, db), p)
    rec = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(db))),
                       "Reconstruction")
    if os.path.isdir(rec):
        names = []
        for r, _d, fs in os.walk(rec):
            for n in fs:
                if n.endswith(".c") or (n.startswith("diff_")
                                        and n.endswith(".py")):
                    names.append(os.path.relpath(os.path.join(r, n), rec)
                                 .replace("\\", "/"))
        for n in sorted(names):
            h.update(("rec-name/" + n).encode("utf-8") + b"\0")
    else:
        feed_missing("Reconstruction/")
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    db = a.db
    work = a.work or os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "work")
    if not os.path.isdir(work):
        die("work dir not found: %s (pass --work)" % work)

    fns = load_functions(work)
    total_fns = len(fns)
    gen = {k for k, v in fns.items() if v["generated"]}
    thunks = {k for k, v in fns.items() if v["thunk"]}
    authored = set(fns) - gen - thunks
    named = {k for k in authored if fns[k]["name"] and not UNNAMED.match(fns[k]["name"])}
    owned = {k for k in authored if fns[k]["owner"]}

    e_total, e_eh, callers, callees, eh_targets = load_edges(work, fns)
    have_caller = {k for k in authored if callers.get(k)}
    contaminable = {t for t in eh_targets if t in authored and not callers.get(t)}

    # A WRONG --db IS SILENT, AND THE REPORT IT PRODUCES LOOKS RIGHT. os.walk on a path that does
    # not exist yields nothing and raises nothing, so every numerator in this report becomes 0
    # while the denominators - which come from the ledger, not the database - stay correct. The
    # result is a COVERAGE-DIMENSIONS.md with the same prose and every percentage 0.00 %, written
    # over the canonical file at exit 0. That is how ec044d8f destroyed ADDRESS-INDEX.md, and this
    # one is worse: a stub is obviously broken, and a plausible report is read as a measurement.
    if not os.path.isdir(db):
        die("database dir not found: %s (pass --db). Refusing to report 0 %% coverage of a "
            "directory that does not exist." % db)
    docs = load_docs(db)
    if not docs:
        die("no .md documents under %s - that is a wrong --db, not an undocumented corpus. "
            "Every numerator in this report would be 0 against correct denominators." % db)
    system_docs = [d for d in docs if not d["index"] and "system" in d["fm"]]
    readmes = [d for d in docs if not d["index"] and "system" not in d["fm"]]
    cited = set()
    keytable_cited = set()
    for d in system_docs:
        cited |= cited_addresses(d["text"])
        # addresses appearing in a "Key addresses" table are a stronger signal than a mention
        for sec in re.findall(r"#+\s*[^\n]*[Kk]ey addresses[^\n]*\n(.*?)(?=\n#+\s|\Z)",
                              d["text"], re.S):
            keytable_cited |= cited_addresses(sec)
            # A *Key addresses* table is a table, not prose -- its cells are bare in the
            # `.md` too, so the table form is read here and nowhere else.
            for m in ANY_HEX8.finditer(sec):
                keytable_cited.add(m.group(1).upper())
    cited_fns = cited & set(fns)
    cited_authored = cited & authored
    key_authored = keytable_cited & authored

    # globals
    gh, grows = read_tsv(os.path.join(work, "h78", "rip_data_refs.tsv"), required=False)
    glob_total = glob_written = glob_cited = 0
    glob_writers = {}
    if grows:
        gi = {n: i for i, n in enumerate(gh)}
        addrs = set()
        for p in grows:
            if len(p) <= gi.get("referenced_address", 1):
                continue
            ad = p[gi["referenced_address"]].upper()
            addrs.add(ad)
            if p[gi.get("kind", 2)] == "write":
                glob_writers.setdefault(ad, set()).add(p[0].upper())
        glob_total = len(addrs)
        glob_written = len(glob_writers)
        glob_cited = len(addrs & cited)

    # types
    ph, prows = read_tsv(os.path.join(work, "h94", "phyre_schema.tsv"), required=False)
    ph_path = os.path.join(work, "h94", "phyre_schema.tsv")
    ph_rows_on_disk = (sum(1 for _ in io.open(ph_path, encoding="utf-8", errors="replace")) - 1
                       if os.path.exists(ph_path) else 0)
    ph_members = len(prows)
    ph_classes = len({p[0] for p in prows}) if prows else 0
    ph_typed = len([p for p in prows if len(p) > 3 and p[3]]) if prows else 0

    # documents: readiness, confidence, contracts, runtime validation
    status = collections.Counter(d["fm"].get("status", "(none)") for d in system_docs)
    tiers = collections.Counter(d["fm"].get("evidence_tier", "(none)") for d in system_docs)
    conf_used = collections.Counter()
    for d in system_docs:
        up = d["text"].upper()
        for c in CONFIDENCE:
            if c in up:
                conf_used[c] += 1
    ready_used = collections.Counter()
    for d in system_docs:
        up = d["text"].upper()
        for r in READINESS:
            if r in up:
                ready_used[r] += 1
    # A contract declares BOTH `contract:` (its subject) and `scope:` (operation/family/
    # transition/subsystem). Requiring only `contract:` counted EXP-001, whose frontmatter
    # carries `contract: <path>` as a REFERENCE to the contract it tests -- inflating the
    # count from 1 to 2, a 100 % overstatement of the program's weakest dimension.
    contracts = [d for d in docs if not d["index"]
                 and d["fm"].get("contract") and d["fm"].get("scope")]
    contract_ready = [d for d in contracts
                      if d["fm"].get("readiness") in ("CONTRACT READY", "RECONSTRUCTION READY",
                                                      "IMPLEMENTED", "DIFFERENTIAL TESTED",
                                                      "PARITY CERTIFIED")]
    runtime_docs = [d for d in system_docs if cites_runtime_evidence(d["text"])]

    # offsets cited, as a proxy for field-level knowledge of game types
    offsets = set()
    for d in system_docs:
        for m in re.finditer(r"\+0x[0-9A-Fa-f]{1,4}\b", d["text"]):
            offsets.add(m.group(0).lower())

    L = []
    w = L.append
    w("# Multidimensional coverage — charter §9")
    w("")
    w("*Generated by `Database/Tools/analysis-kit/gfz-scripts/program_coverage.py`. "
      "Re-run it; never quote these numbers from memory.*")
    w("")
    w("*Input fingerprint: `%s` - sha-256 over the complete bytes of every input "
      "this run read (the `work` TSVs, every `.md`+`.tsv` under db with the doc "
      "walk's own exclusions, `Reconstruction/` counted names). A moved input "
      "moves it; `check_surface_figures.py` reports a moved fingerprint as STALE.*"
      % input_fp(db, work))
    w("")
    w("> **Every ratio carries its denominator, every proxy is labelled a proxy, and a dimension "
      "the current data cannot support prints `UNMEASURED` with a reason.** A single composite "
      "percentage is exactly what §9 forbids, because it hides the difference between *found*, "
      "*understood* and *reimplementable*.")
    w("")

    w("## 1. Discovery — what exists")
    w("")
    _b = uc1_band.load()
    if all("%08X" % st in fns for st in _b["frontier"]):
        w("> **Population series break 2026-09-28 (UC-1):** this run counts "
          "38,160 listed + %d UC-1 frontier bodies = **%d** "
          "(34,269 non-funclet listed + %d frontier = %d; the "
          "pre-2026-09-28 series counted 34,270 non-funclet). %d band rows "
          "are held and excluded; one listed entry (007EE7F0) removed; "
          "five extents extended." % (len(_b["frontier"]), total_fns,
                                     len(_b["frontier"]),
                                     34269 + len(_b["frontier"]),
                                     len(_b["held"])))
        w("")
    if EXTENT_INFO:
        w("> **Extent series break %s (the chained-tails ruling's extent rule):** function extents are the listed range "
          "union the adjudicated `underrun` rows of `_index/FUNCTION-EXTENT-ERRATA.tsv`; this run grows %d entries by "
          "%d bytes (%d errata extents). Byte figures before %s are a different series." % (
              uc1_band.EXTENT_SERIES_BREAK, EXTENT_INFO["grown"], EXTENT_INFO["bytes_added"],
              EXTENT_INFO["errata_entries"], uc1_band.EXTENT_SERIES_BREAK))
        w("")
    w("| quantity | count | denominator |")
    w("|---|---:|---:|")
    w("| functions in the export | **%d** | — |" % total_fns)
    w("| compiler/template generated | %d | %d (%s) |" % (len(gen), total_fns, pct(len(gen), total_fns)))
    w("| thunks | %d | %d (%s) |" % (len(thunks), total_fns, pct(len(thunks), total_fns)))
    w("| **authored functions** (neither) | **%d** | %d (%s) |"
      % (len(authored), total_fns, pct(len(authored), total_fns)))
    w("")
    w("> **`authored` is the denominator that matters for reconstruction.** %d of %d functions are "
      "compiler output or thunks; nobody reimplements those by hand, and including them deflates "
      "every percentage below." % (len(gen) + len(thunks), total_fns))
    w("")

    w("## 2. Identity — naming and ownership")
    w("")
    w("| dimension | count | of | share |")
    w("|---|---:|---:|---:|")
    w("| authored functions with a semantic name | %d | %d | %s |"
      % (len(named), len(authored), pct(len(named), len(authored))))
    w("| authored functions with an owner assigned | %d | %d | %s |"
      % (len(owned), len(authored), pct(len(owned), len(authored))))
    w("")

    w("## 3. Citation — a proxy for attention, **not** for understanding")
    w("")
    w("| dimension | count | of | share |")
    w("|---|---:|---:|---:|")
    w("| authored functions cited anywhere in a system document | %d | %d | %s |"
      % (len(cited_authored), len(authored), pct(len(cited_authored), len(authored))))
    w("| authored functions in a document's *Key addresses* table | %d | %d | %s |"
      % (len(key_authored), len(authored), pct(len(key_authored), len(authored))))
    _tsv = set()
    for _r, _d, _f in os.walk(db):
        for _n in _f:
            if _n.endswith(".tsv"):
                _t = io.open(os.path.join(_r, _n), encoding="utf-8", errors="replace").read()
                for _m in ANY_HEX8.finditer(_t):
                    _tsv.add(_m.group(1).upper())
    _tonly = (_tsv & authored) - cited_authored
    w("| **recorded only in a `.tsv` side file, explained by no document** | **%d** | %d | %s |"
      % (len(_tonly), len(authored), pct(len(_tonly), len(authored))))
    w("")
    w("> **A side-file row is a transcription, not an explanation** — the database's own rule from "
      "`check_named_not_cited.py`. Those %d are findable (they are listed in `ADDRESS-INDEX.md` "
      "under *table only*) and are deliberately **not** counted as cited." % len(_tonly))
    w("")
    w("> **Citation is the weakest signal in this report.** A backticked address, a `FUN_` symbol "
      "or a quoted disassembly line means a human looked at the function once. The *Key addresses* "
      "column is stronger — it means the document treats the function as load-bearing — and it is "
      "**%s of authored code**." % pct(len(key_authored), len(authored)))
    w("")
    w("> **A bare address in a sentence is not counted.** It cannot be told from a constant of the "
      "same width — `+0x118 = 0x003C0000` and the divide-by-3 magic `0x00555556` both land inside "
      "real function bodies. Excluding the form costs 9 functions; including the `FUN_<addr>` "
      "symbol form, which this report missed until 2026-09-08, gains 226.")
    w("")

    w("## 4. Callgraph — with banned-evidence edges removed")
    w("")
    w("| quantity | count | denominator |")
    w("|---|---:|---:|")
    w("| edges in `edges.tsv` | %d | — |" % e_total)
    w("| **edges whose caller is an EH funclet/handler (excluded)** | **%d** | %d (%s) |"
      % (e_eh, e_total, pct(e_eh, e_total)))
    w("| authored functions with >=1 non-EH caller | %d | %d (%s) |"
      % (len(have_caller), len(authored), pct(len(have_caller), len(authored))))
    w("| authored functions whose **only** callers were EH edges | **%d** | — |" % len(contaminable))
    w("")
    w("> **%d authored functions have no caller left once EH edges are removed.** Any prior "
      "reachability claim about one of them was resting on banned evidence — that is the EC-1 sweep "
      "population, and it is now an exact list rather than a worry." % len(contaminable))
    w("")

    w("## 5. Globals — readers and writers")
    w("")
    if glob_total:
        w("| dimension | count | of | share |")
        w("|---|---:|---:|---:|")
        w("| distinct global addresses referenced by code | %d | — | — |" % glob_total)
        w("| of those, having at least one **writer** | %d | %d | %s |"
          % (glob_written, glob_total, pct(glob_written, glob_total)))
        w("| of those, cited in any system document | %d | %d | %s |"
          % (glob_cited, glob_total, pct(glob_cited, glob_total)))
        w("")
        w("> **This is the dataset charter §7 needs for \"show every known writer of this field\".** "
          "It already exists (`Tools/work/h78/rip_data_refs.tsv`, %d reference rows) and is **not "
          "wired into the database** — %s of referenced globals are mentioned in any document."
          % (len(grows), pct(glob_cited, glob_total)))
    else:
        w("**UNMEASURED** — `Tools/work/h78/rip_data_refs.tsv` not found.")
    w("")

    w("## 6. Types and fields")
    w("")
    if ph_members:
        w("| dimension | count |")
        w("|---|---:|")
        w("| Phyre reflected members recovered | %d |" % ph_members)
        if ph_rows_on_disk != ph_members:
            w("| *(rows on disk, incl. %d with an empty first field)* | %d |"
              % (ph_rows_on_disk - ph_members, ph_rows_on_disk))
        w("| Phyre classes covered | %d |" % ph_classes)
        w("| of those members with a resolved type | %d (%s) |" % (ph_typed, pct(ph_typed, ph_members)))
        w("| distinct `+0xNN` field offsets cited across documents | %d |" % len(offsets))
        _tp = os.path.join(db, "_types", "fields.tsv")
        if os.path.exists(_tp):
            _txt = io.open(_tp, encoding="utf-8").read().split("\n")[1:]
            _rows = [l for l in _txt if l.strip()]
            _ntypes = len({l.split("\t")[0] for l in _rows})
            _named = sum(1 for l in _rows if l.split("\t")[3] != "UNRESOLVED")
            # ENGINE types and GAME types are counted apart. On 2026-09-08 an import of 179
            # Phyre reflection classes took this store from 2 types to 181, and a single row
            # labelled "game types" would have reported a 90x jump in exactly the number the
            # charter's L2 gap is about. The category column says which is which.
            _tt = os.path.join(db, "_types", "types.tsv")
            _cat = {}
            if os.path.exists(_tt):
                for _l in io.open(_tt, encoding="utf-8").read().split("\n")[1:]:
                    if _l.strip():
                        _c = _l.split("\t")
                        _cat[_c[0]] = _c[2] if len(_c) > 2 else ""
            _engine = set(t for t in _cat if _cat[t].startswith(("22-", "23-", "24-")))
            _in_fields = set(l.split("\t")[0] for l in _rows)
            _game = _in_fields - _engine
            w("| **GAME types in the `_types/` store** | **%d** |" % len(_game))
            w("| engine / middleware types in the store | %d |" % len(_in_fields & _engine))
            w("| fields recorded / of those named | %d / %d |" % (len(_rows), _named))
            w("| *of those, fields on a GAME type* | %d |"
              % sum(1 for l in _rows if l.split("\t")[0] in _game))
            w("")
            w("> **The type store exists as of 2026-09-08** (`_types/`, validated by "
              "`types_index.py`). It records a field's offset and size even when the meaning is "
              "unknown, so unrecovered layout is **visible rather than absent**. Per-type "
              "coverage: `_index/TYPE-COVERAGE.md`.")
        if len(offsets) == ph_members:
            w("")
            w("> **The two %d figures above are a coincidence, not a bug.** They were verified "
              "independently with a separate `grep`/`sort -u` over the same documents, and count "
              "unrelated things: reflected member records versus distinct offset literals "
              "appearing in prose." % ph_members)
        w("")
        w("> **Game types are UNMEASURED.** The reflected schema covers PhyreEngine's own classes, "
          "which the engine describes at runtime. **FFXII's own structures have no equivalent "
          "table** — the %d cited offsets are scattered through prose, not collected into typed "
          "structures, so \"field-resolution coverage\" for game types cannot be computed. That "
          "gap is the single largest obstacle to charter §5." % len(offsets))
    else:
        w("**UNMEASURED** — no `phyre_schema.tsv`.")
    w("")

    w("## 7. Documents — status, confidence, contracts, runtime validation")
    w("")
    w("| dimension | count | of | share |")
    w("|---|---:|---:|---:|")
    w("| system documents (carrying a `system:` key) | %d | — | — |" % len(system_docs))
    w("| category READMEs (not documents) | %d | — | — |" % len(readmes))
    w("| **behavioural contracts** | **%d** | %d systems | %s |"
      % (len(contracts), len(system_docs), pct(len(contracts), len(system_docs))))
    w("| of those at `CONTRACT READY` or beyond | %d | %d | %s |"
      % (len(contract_ready), len(contracts), pct(len(contract_ready), len(contracts))))
    w("| documents citing any runtime/live-process evidence | %d | %d | %s |"
      % (len(runtime_docs), len(system_docs), pct(len(runtime_docs), len(system_docs))))
    w("")
    w("**`status:` frontmatter values** — " + ", ".join(
        "`%s` %d" % (k, v) for k, v in status.most_common()))
    w("")
    w("**`evidence_tier:` values** — " + ", ".join(
        "`%s` %d" % (k, v) for k, v in tiers.most_common()))
    w("")
    if conf_used:
        w("**Charter §8 confidence labels in use** — " + ", ".join(
            "`%s` in %d doc(s)" % (k, v) for k, v in conf_used.most_common()))
    else:
        w("**Charter §8 confidence labels are not used by any document.** The database uses a "
          "numeric `evidence_tier` instead. These are different vocabularies and the charter asks "
          "for the named one; reconciling them is a schema decision, not a relabelling.")
    w("")
    if ready_used:
        w("**Readiness rungs named in documents** — " + ", ".join(
            "`%s` in %d" % (k, v) for k, v in ready_used.most_common()))
    else:
        w("**No document names a readiness rung.** Every system document is `status: DOCUMENTED`, "
          "which maps to at most *SEMANTICALLY UNDERSTOOD* on the charter §2 ladder and says "
          "nothing about type resolution, runtime validation or implementability.")
    w("")

    w("## 8. Goals 2 and 3")
    w("")
    w("| dimension | state |")
    w("|---|---|")
    _rec = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(db))), "Reconstruction")
    _impl = _diff = 0
    if os.path.isdir(_rec):
        for _r, _d, _f in os.walk(_rec):
            for _n in _f:
                if _n.endswith(".c") and "Tests" not in _r:
                    _impl += 1
                if _n.startswith("diff_") and _n.endswith(".py"):
                    _diff += 1
    w("| source implementation | **%d** reimplemented operation(s) | `Reconstruction/` |" % _impl)
    w("| differential-test coverage | **%d** harness(es) | vs the shipped bytes under emulation |" % _diff)
    w("| parity-certified coverage | **0** | calculation parity is not certification |")
    w("")
    w("**Parity-certified stays 0 deliberately.** Calculation parity over synthetic inputs is not "
      "certification: `field_music` matches the shipped bytes on 1,200 generated tables, and the "
      "real table's contents are still unread, so `INTEGRATION` parity is untested. **A green "
      "differential test proves the algorithm, not the outcome.**")
    w("")

    w("## 9. What this report deliberately does not say")
    w("")
    w("- **It does not emit an overall percentage.** There is no defensible way to weigh "
      "\"functions named\" against \"behaviours reimplementable\", and averaging them would hide "
      "the fact that the second is near zero.")
    w("- **It does not treat citation as understanding.** §3 is labelled a proxy throughout.")
    w("- **It does not estimate game-type field coverage.** The data to compute it does not exist "
      "yet; §6 says so instead of guessing.")
    w("- **It does not count `_index/_inbox/` peer notes as documents.** They are raw handoffs.")

    out = "\n".join(L) + "\n"
    if a.out:
        io.open(a.out, "w", encoding="utf-8", newline="\n").write(out)
        sys.stdout.write("wrote %s (%d lines)\n" % (a.out, len(L)))
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
