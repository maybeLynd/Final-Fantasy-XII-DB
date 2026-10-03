#!/usr/bin/env python3
"""knowledge_db.py - charter section 7: make the knowledge machine-queryable.

What this is, and what it is NOT
--------------------------------
It is an **index built from the sources that already exist**, not a replacement for them. The
markdown documents stay authoritative; this file is regenerated from them and can be deleted at any
time without losing a single fact. Charter section 7 asks for structure, and the cheapest honest
structure is a derived index, because a derived index **cannot silently disagree with the documents
it came from** - rebuild it and any disagreement vanishes.

Eight sources go in:

    documents         every .md with frontmatter, under the database root
    doc_fields        the long tail of frontmatter keys, unflattened
    citations         address -> document, resolved to the containing function
    functions         work/graph/functions.tsv
    edges             work/graph/edges.tsv, WITH the EH flag as a column
    global_refs       work/h78/rip_data_refs.tsv, 164k read/write rows
    field_access      _types/field-access-index.tsv, the per-type object-field xref (F-6)
    types / fields    _types/*.tsv
    questions         _index/OPEN-QUESTIONS.md
    script_verbs      01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv
    contradictions    _index/CONTRADICTIONS.tsv
    reconstructions   Reconstruction/, walked

Why `edges.caller_is_eh` is a column and not a habit
----------------------------------------------------
`edges.tsv` contains caller edges whose source is an unwind funclet or catch handler. That is the
exact evidence class the mission prompt bans, a prior branch lost 182 classifications to it, and an
ordinary `awk` over the file hands it to you by default. **Materialising the flag as a column turns
"remember to filter" into "write a WHERE clause you can see".** Every built-in query below either
filters it or prints both counts.

Honesty about coverage
----------------------
`knowledge_db.py queries` prints charter section 7's own list of required queries with, for each,
whether this schema can answer it and - when it cannot - **which source would have to exist first**.
That list is the real deliverable of this tool. A schema that answers four of thirteen questions and
says so is worth more than one that answers thirteen by inventing data.
"""
import argparse
import datetime
import hashlib
import io
import os
import re
import sqlite3
import subprocess
import sys

# Imported HERE, not 60 lines below with the sibling-module imports: `ROOT = KP.ROOT` on the very
# next line runs at import time, so a later import leaves this module raising NameError before
# anything can call it. That is how it stood at HEAD after fa68c18e4 - `knowledge_db.py build`,
# which is a step of the publication chain, could not be run at all.
import kit_paths as KP

ROOT = KP.ROOT
DB_DIR = os.path.join(ROOT, "Database", "FFXII TZA")
TOOLS = os.path.join(ROOT, "Database", "Tools")
OUT = os.path.join(TOOLS, "work", "knowledge", "knowledge.sqlite")
FUNCS = os.path.join(TOOLS, "work", "graph", "functions.tsv")
EDGES = os.path.join(TOOLS, "work", "graph", "edges.tsv")
GREFS = os.path.join(TOOLS, "work", "h78", "rip_data_refs.tsv")
RECON = os.path.join(ROOT, "Reconstruction")

# `ADDR(args)` is the corpus's normal call-form citation and is the STRONGEST form, not
# prose: the unextended pattern required the backtick immediately after the hex, so 1,048
# backticked call-forms fell through to ADDR_BARE and were scored prose - excluded from
# `cited` entirely (measured 2026-09-19, 672 docs / 141,083 classified addresses).
ADDR = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})(?:\([^`]*?\))?`")
# A citation is a document TALKING ABOUT an address, and `ADDR` alone sees only one of the
# four ways this database writes one. It requires the address to fill a code span by itself,
# so `FUN_002f9860`, a quoted `mov` inside a fenced listing, and a bare address in prose were
# all invisible. **The blind spot was aligned with the search space**: the GFZ ledger names an
# unnamed function `FUN_<addr>`, so the form most often missed was the form used for exactly
# the functions the "what is undocumented?" queries hunt for. 375 authored functions the
# corpus discusses were reported uncited, and one of them -- `002F9860`, 160 callers -- was
# picked as an undocumented target by this tool's own high-connectivity query while a
# document had read it in full. Form is recorded, not flattened: `form='backtick'`
# reproduces the pre-2026-09-08 number exactly.
ADDR_SYMBOL = re.compile(r"(?:FUN|LAB|DAT|PTR|SUB|UNK|thunk_FUN)_(0[0-9A-Fa-f]{7})", re.I)
ADDR_BARE = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])")
# A sha256 begins with eight hex digits too. `73461d0896204b1c...` would resolve into a real
# function body and be indexed as a citation in every document that states the exe hash --
# which is all of them. Strip long runs before extracting anything.
ADDR_LONGHEX = re.compile(r"\b(0[0-9A-Fa-f]{7})[0-9A-Fa-f]{8,}")
FENCED = re.compile(r"```.*?```", re.S)
CITE_FORMS = ("backtick", "symbol", "code", "prose")


def citation_forms(text):
    """{address -> strongest form}. Priority: backtick > symbol > code > prose."""
    safe = ADDR_LONGHEX.sub(" ", text)
    fenced = " ".join(FENCED.findall(safe))
    prose = FENCED.sub(" ", safe)
    out = {}
    for form, src, pat in (("prose", prose, ADDR_BARE), ("code", fenced, ADDR_BARE),
                           ("symbol", safe, ADDR_SYMBOL), ("backtick", safe, ADDR)):
        for m in pat.finditer(src):
            out[m.group(1).upper()] = form
    return out
# Runtime evidence is asserted in the BODY, not the frontmatter. A query that looked for it in
# `verified_against` returned zero for all 28 categories while `program_coverage.py` counted 13.
# COPYING that tool's marker list then produced 11, because the copy dropped four markers. So the
# list is IMPORTED, not copied - the same fix already applied to the question-ledger parser, and
# for the same reason: two definitions of one concept drift, and the drift is silent.
import program_coverage as _pc
RUNTIME_MARKERS = _pc.RUNTIME_MARKERS
# A contract's section 13 runs to the next `## ` heading. Only contracts are trimmed; a prose page
# has no section 13 and is scanned whole.
RT_S13 = re.compile(r"^##\s*13\.[^\n]*\n.*?(?=^##\s|\Z)", re.S | re.M)
ADDR_BARE = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])")
# The question ledger is parsed by IMPORTING the gate that already owns it. A first attempt here
# wrote a second regex and read 813 rows where `check_questions.py` reads 824 - eleven questions
# invisible to any query built on this index. **Two parsers of one file that disagree is the defect
# class this project keeps paying for**, so there is now one parser and this file is a caller.
import check_questions as _cq
# Names are IMPORTED the same way, and for a sharper reason than symmetry. The audit of 2026-09-08
# found this database names 5,812 of the 7,376 function entries it cites while `functions.tsv`
# names 677 - an eight-to-one understatement of the charter's Identity dimension, caused entirely
# by names living in prose that nothing indexed. `check_consistency.py` already owns the patterns
# AND the rule that a "Superseded readings" section is a permanent record rather than a live name,
# so this file is a caller, never a second definition. `DU-1`.
import check_consistency as _cs

SCHEMA_VERSION = 4

# ---------------------------------------------------------------- freshness (schema 4)
# The mirror is a DATED SNAPSHOT of its inputs; the defect it must never commit is answering
# as if current when its sources moved. `provenance` therefore records, per (table, dependency):
# the dependency file-set/content hash (trees carry a manifest digest over
# sorted relpath + per-file hash, so added/deleted files and uncommitted edits both count),
# the generator identity (the module set that determines output + schema version), and the
# output identity (a digest over the table's own rows). `check` recomputes those fingerprints
# against the CURRENT worktree and answers CURRENT or STALE + which dependencies moved - a
# timestamp or a HEAD rev-parse alone establishes neither. The same dependency spec serves
# build AND check, because two definitions of one dependency set drift silently.
GENERATOR_MODULES = ["knowledge_db.py", "kit_paths.py", "check_questions.py",
                     "check_consistency.py", "program_coverage.py"]
# table -> dependencies. Joined sources are real dependencies: citations/doc_names resolve
# through functions.tsv, edges.caller_is_eh is computed from it. `cited` is a VIEW - it
# depends on every table it reads (VIEW_DEPS expands it).
VIEW_DEPS = {"cited": ["citations"]}


def _types_dir_files():
    tp = os.path.join(DB_DIR, "_types", "types.tsv")
    fp = os.path.join(DB_DIR, "_types", "fields.tsv")
    fap = os.path.join(DB_DIR, "_types", "field-access-index.tsv")
    qp = os.path.join(DB_DIR, "_index", "OPEN-QUESTIONS.md")
    sp = os.path.join(DB_DIR, "01-Script-VM-Native-Bridge", "Verb-Dispatch",
                      "scriptvm-dispatch.tsv")
    cp2 = os.path.join(DB_DIR, "_index", "CONTRADICTIONS.tsv")
    return tp, fp, fap, qp, sp, cp2


def table_deps():
    """{table: [("file", path) | ("tree", dir, suffix)]} - the ONLY dependency list."""
    tp, fp, fap, qp, sp, cp2 = _types_dir_files()
    docs = ("tree", DB_DIR, ".md")
    fn = ("file", FUNCS)
    return {
        "functions": [fn],
        "edges": [("file", EDGES), fn],
        "global_refs": [("file", GREFS)],
        "documents": [docs], "doc_fields": [docs], "contract_sections": [docs],
        "contract_claims": [docs],
        "citations": [docs, fn], "doc_names": [docs, fn],
        "types": [("file", tp)], "fields": [("file", fp)],
        "field_access": [("file", fap)],
        "questions": [("file", qp)],
        "script_verbs": [("file", sp)],
        "contradictions": [("file", cp2)],
        "reconstructions": [("tree", RECON, None)],
    }


def _norm_sha256(b):
    """Content hash ignoring CRLF/LF checkout normalisation - a byte-identical blob and its
    CRLF worktree checkout are the SAME input (the 2026-09-25 fields.tsv false-stale class);
    real edits still change it. git_blob remains the exact-bytes identity."""
    return hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest() if b is not None else None


def _tree_file_digest(b, suffix):
    """Per-file digest inside a tree dependency, exactly as build() writes its manifest: .md documents are hashed
    after a utf-8 decode with errors='replace' (build reads them as text), other trees as raw bytes. Hashing raw
    bytes for .md made every doc table falsely STALE whenever a document holds invalid utf-8 (3 at 14bd5582d -
    SWE2-DATA 2026-10-03)."""
    if b is None:
        return "-"
    if suffix == ".md":
        b = b.decode("utf-8", "replace").replace("\r\n", "\n").encode("utf-8")
    return _norm_sha256(b) or "-"


def dep_key(desc):
    """Stable source label stored in provenance.source: 'file:<rel>' or 'tree:<rel>;<suffix>'."""
    if desc[0] == "file":
        return "file:" + _git_rel(desc[1])
    return "tree:%s;%s" % (_git_rel(desc[1]), desc[2] or "*")


AGAINST = None  # set by `check --against REV`: digests come from REV's blobs instead of the worktree


def _rev_blobs(rev, rel_prefix):
    """{root-relative path: bytes} for every file under rel_prefix at rev, read in ONE `git cat-file --batch`
    stream (thousands of documents; one process per file would take minutes)."""
    r = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", rev, "--", rel_prefix], capture_output=True)
    ents = []
    for line in r.stdout.decode("utf-8", "replace").splitlines():
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if len(parts) == 3 and parts[1] == "blob":
            ents.append((path, parts[2]))
    if not ents:
        return {}
    p = subprocess.run(["git", "-C", ROOT, "cat-file", "--batch"], input="".join(o + "\n" for _p, o in ents).encode(),
                       capture_output=True)
    out, i, blobs = p.stdout, 0, {}
    for path, _o in ents:
        nl = out.index(b"\n", i)
        size = int(out[i:nl].split()[2])
        blobs[path] = out[nl + 1:nl + 1 + size]
        i = nl + 1 + size + 1
    return blobs


def dep_digest_at(desc, rev):
    """The same fingerprint as dep_digest, computed from rev's committed blobs (`check --against REV`). A source with
    no versioned home (an untracked Tools/work TSV) is read from the worktree, as a pinned build reads it."""
    rel = _git_rel(desc[1])
    if desc[0] == "file":
        r = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (rev, rel)], capture_output=True)
        if r.returncode == 0:
            return _norm_sha256(r.stdout)
        global AGAINST
        saved, AGAINST = AGAINST, None   # worktree fallback must not re-enter this function
        try:
            return dep_digest(desc)
        finally:
            AGAINST = saved
    blobs = _rev_blobs(rev, rel)
    h = hashlib.sha256()
    for p in sorted(k for k in blobs if not desc[2] or k.endswith(desc[2])):
        h.update((p + "\n" + _tree_file_digest(blobs[p], desc[2]) + "\n").encode("utf-8"))
    return h.hexdigest()


def dep_digest(desc):
    """Current-state fingerprint of one dependency. Worktree always - `check` compares what a
    build RECORDED against what the inputs are NOW; a pinned build's pin is information, not
    an exemption. Missing files hash as None (deletion IS a change). Under `check --against REV`
    (AGAINST set) the committed state of REV is the comparison instead (SWE2-DATA 2026-10-03,
    OPUS-REQ-DATA-MIRROR-COMMITTED-FRESHNESS-1003): in an active fleet the worktree always holds
    uncommitted edits, so a checkpoint could never carry a CURRENT mirror. Live queries keep the
    worktree rule - AGAINST is set only by that explicit mode."""
    if AGAINST:
        return dep_digest_at(desc, AGAINST)
    if desc[0] == "file":
        if not os.path.exists(desc[1]):
            return None
        with open(desc[1], "rb") as f:
            return _norm_sha256(f.read())
    h = hashlib.sha256()
    base = desc[1]
    # The file list is sorted GLOBALLY before hashing: tree_files() returns a sorted list,
    # so a per-directory walk order would digest the same set differently - the false-stale
    # class this manifest exists to avoid.
    files = []
    for root, dirs, names in os.walk(base):
        for fn in names:
            if desc[2] and not fn.endswith(desc[2]):
                continue
            files.append(os.path.join(root, fn))
    for p in sorted(_git_rel(x) for x in files):
        with open(os.path.join(ROOT, p.replace("/", os.sep)), "rb") as f:
            b = f.read()
        h.update((p + "\n" + _tree_file_digest(b, desc[2]) + "\n").encode("utf-8"))
    return h.hexdigest()


def current_fingerprints():
    """{dep_key: digest} over every distinct dependency - build's mid-flight guard and
    check's comparison both use this one computation."""
    seen = {}
    for deps in table_deps().values():
        for d in deps:
            seen.setdefault(dep_key(d), dep_digest(d))
    return seen


def generator_digest():
    """Digest of the module set that determines the mirror's contents + the schema version.
    A parser or schema change stales EVERY table even when no input moved."""
    here = os.path.dirname(os.path.abspath(__file__))
    h = hashlib.sha256()
    for rel in GENERATOR_MODULES:
        p = os.path.join(here, rel)
        h.update(rel.encode("utf-8") + b"\n")
        h.update((_sha256_file(p) if os.path.exists(p) else "MISSING").encode("utf-8"))
        h.update(b"\n")
    h.update(("schema=%d" % SCHEMA_VERSION).encode("utf-8"))
    return h.hexdigest()


def _table_digest(cur, t):
    """Output identity: digest over the table's rows in column order, so a hand-edited DB is
    distinguishable from what the generator wrote."""
    cols = [r[1] for r in cur.execute("PRAGMA table_info(%s)" % t)]
    h = hashlib.sha256()
    h.update(("\x1e".join(cols) + "\n").encode("utf-8"))
    q = "SELECT * FROM %s ORDER BY %s" % (t, ", ".join('"%s"' % c for c in cols))
    for row in cur.execute(q):
        h.update(("\x1f".join("N" if v is None else
                             "B" + v.hex() if isinstance(v, bytes) else str(v)
                             for v in row) + "\n").encode("utf-8"))
    return h.hexdigest()


def freshness_report(db_path, tables=None):
    """-> (status, stale_lines, meta). The one check every agent-facing reader wires in.
    status: 'no-index' | 'old-schema' | 'stale' | 'current'. stale_lines name the table and
    WHICH dependency moved - an unexplained 'rebuild' hint is the failure mode this replaces.
    `tables` restricts the dependency scan to the tables a query actually touches; the
    generator check always applies because a parser change stales everything downstream."""
    if not os.path.exists(db_path):
        return "no-index", ["no index at %s - run `knowledge_db.py build`" % db_path], {}
    conn = sqlite3.connect(db_path)
    cols = set()
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(provenance)")}
    except sqlite3.Error:
        pass
    need = {"table_name", "source", "source_sha256", "generator_sha256", "pinned_commit",
            "built_at", "schema_version"}
    if not need <= cols:
        conn.close()
        return "old-schema", ["provenance predates schema 4 - rebuild with "
                              "`knowledge_db.py build` before trusting any answer"], {}
    rows = conn.execute("SELECT table_name, source, source_sha256, generator_sha256, "
                        "pinned_commit, built_at FROM provenance").fetchall()
    meta = {"built_at": rows[0][5] if rows else None,
            "pinned_commit": rows[0][4] if rows else None,
            "generator_sha256": rows[0][3] if rows else None}
    gen = generator_digest()
    stale = []
    deps = table_deps()
    by_key = {}
    for t, ds in deps.items():
        for d in ds:
            by_key[dep_key(d)] = d
    for t, source, recorded, _gen, pin, _at in rows:
        if tables is not None and t not in tables:
            continue
        d = by_key.get(source)
        if d is None:
            stale.append("%s: dependency %s no longer in the spec (generator/schema moved)"
                         % (t, source))
            continue
        now = dep_digest(d)
        if now != recorded:
            stale.append("%s: %s changed since the build" % (t, source))
    if meta.get("generator_sha256") and meta["generator_sha256"] != gen:
        stale = ["generator: a parser/module or the schema changed since the build "
                 "(every table is downstream)"] + stale
    conn.close()
    return ("stale" if stale else "current"), stale, meta


_KNOWN_NAMES = set()  # populated lazily - schema tables + views


def tables_of_sql(sql):
    """Which tables/views a query text touches - ad-hoc `sql` and named `query` alike; a
    joined view expands through VIEW_DEPS to every table it uses."""
    global _KNOWN_NAMES
    if not _KNOWN_NAMES:
        _KNOWN_NAMES = set(table_deps()) | set(VIEW_DEPS)
    names = set()
    for t in _KNOWN_NAMES:
        if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(t), sql):
            names.update(VIEW_DEPS.get(t, [t]))
    return names

# ---------------------------------------------------------------- revision-pinned sources
# `knowledge_db.py build --pin HEAD` reads every tracked source from that ref's blobs, not the
# worktree. That is what makes the mirror revision-coherent: a sha256 of worktree bytes can match
# no commit at all (measured 2026-09-25 by OPUS on this tool's own provenance rows - a dirty
# types.tsv pinned to a hash no revision carries, and a CRLF-checkout fields.tsv whose worktree
# hash can NEVER equal its blob's). Sources with no versioned home at all - the Tools/work
# generated TSVs - are still read from the worktree and are marked `worktree:` in provenance,
# so the table says plainly which of the mirror's inputs have no revision behind them.
PIN = None  # set by --pin; None means the historical worktree build


def _git_rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def _git(ref, args):
    return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True)


def pinned_commit(ref):
    r = _git(ref, ["rev-parse", "--verify", ref])
    return r.stdout.decode("ascii", "replace").strip() if r.returncode == 0 else ref


def src_bytes(path):
    """(bytes, origin) - origin is 'git:<relpath>' or 'worktree:<relpath>' or None."""
    if PIN:
        r = _git(PIN, ["show", "%s:%s" % (PIN, _git_rel(path))])
        if r.returncode == 0:
            return r.stdout, "git:" + _git_rel(path)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read(), "worktree:" + _git_rel(path)
    return None, None


def src_text(path, errors="replace"):
    b, origin = src_bytes(path)
    return (b.decode("utf-8", errors), origin) if b is not None else (None, origin)


def src_lines(path):
    text, origin = src_text(path)
    return (text.splitlines(), origin) if text is not None else (None, origin)


def src_lines_stream(path):
    """Same as src_lines but shaped for the `f.readline()/for line in f` call sites."""
    lines, origin = src_lines(path)
    return (io.StringIO("\n".join(lines or [])) if lines is not None else None, origin)


WIN_DEVICES = {"CON", "PRN", "AUX", "NUL"} | {"COM%d" % i for i in range(1, 10)} | {"LPT%d" % i for i in range(1, 10)}


def tree_files(subdir_abs, suffix=None):
    """Committed files under a tree (pinned) or worktree files (unpinned). Reapository-root
    relative, forward slashes, sorted."""
    rel = _git_rel(subdir_abs)
    if PIN:
        r = _git(PIN, ["ls-tree", "-r", "--name-only", PIN, "--", rel])
        if r.returncode != 0:
            return []
        files = r.stdout.decode("utf-8", "replace").splitlines()
    else:
        files = []
        for root, dirs, names in os.walk(subdir_abs):
            for fn in names:
                # A file named like a Windows device (NUL, CON, AUX, PRN, COM1-9, LPT1-9) - left by a `> NUL` redirect in
                # a POSIX shell - resolves to the device, not the file, and made every unpinned build fail
                # ("path is on mount '\\.\NUL'", 2026-10-03). It is never a source; skip it.
                if fn.split(".")[0].upper() in WIN_DEVICES:
                    continue
                files.append(_git_rel(os.path.join(root, fn)))
    return sorted(f for f in files if suffix is None or f.endswith(suffix))


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


SCHEMA = """
CREATE TABLE documents (
    path TEXT PRIMARY KEY, system TEXT, category TEXT, status TEXT, owner_layer TEXT,
    evidence_tier TEXT, level TEXT, readiness TEXT, confidence TEXT, scope TEXT,
    last_reviewed TEXT, falsification_passes TEXT, is_contract INTEGER, is_template INTEGER,
    body_bytes INTEGER, runtime_markers INTEGER);
CREATE TABLE doc_fields (path TEXT, key TEXT, value TEXT);
CREATE TABLE citations (path TEXT, address TEXT, resolved_entry TEXT, is_entry INTEGER,
    form TEXT);   -- backtick | symbol | code | prose; see citation_forms()
CREATE TABLE doc_names (path TEXT, address TEXT, name TEXT, resolved_entry TEXT,
                        is_entry INTEGER, is_generated_index INTEGER);
CREATE TABLE contract_sections (path TEXT, num INTEGER, title TEXT, chars INTEGER,
                                bullets INTEGER, code_blocks INTEGER);
CREATE TABLE contract_claims (path TEXT, claim TEXT, evidence TEXT, tier TEXT,
                              confidence TEXT);
CREATE TABLE functions (
    entry TEXT PRIMARY KEY, name TEXT, body_bytes INTEGER, owner TEXT,
    thunk TEXT, noreturn TEXT, tags TEXT, is_eh INTEGER, is_generated INTEGER);
CREATE TABLE edges (caller TEXT, callee TEXT, callee_name TEXT, caller_is_eh INTEGER);
CREATE TABLE global_refs (function_entry TEXT, address TEXT, kind TEXT, site TEXT);
CREATE TABLE types (
    name TEXT PRIMARY KEY, size TEXT, category TEXT, instance TEXT, allocation_site TEXT,
    ctor TEXT, dtor TEXT, readiness TEXT, confidence TEXT, level TEXT, documents TEXT);
CREATE TABLE fields (
    type TEXT, offset TEXT, size INTEGER, name TEXT, ctype TEXT, meaning TEXT,
    readiness TEXT, confidence TEXT, resolved INTEGER);
CREATE TABLE questions (id TEXT PRIMARY KEY, question TEXT, state TEXT, answer TEXT);
CREATE TABLE reconstructions (name TEXT, source_path TEXT, test_path TEXT, kind TEXT);
CREATE TABLE script_verbs (call_id TEXT, verb TEXT, args TEXT, handler TEXT, handler_name TEXT,
                           owner TEXT);
CREATE INDEX ix_sv_handler ON script_verbs(handler);
CREATE TABLE contradictions (id TEXT, date TEXT, kind TEXT, category TEXT, document TEXT,
                             line TEXT, claim TEXT, correction TEXT, instrument TEXT,
                             addresses TEXT);
CREATE INDEX ix_con_cat ON contradictions(category);
CREATE INDEX ix_cit_addr ON citations(address);
CREATE INDEX ix_dn_addr ON doc_names(address);
CREATE INDEX ix_cs_path ON contract_sections(path);
CREATE INDEX ix_dn_entry ON doc_names(resolved_entry);
CREATE INDEX ix_cit_entry ON citations(resolved_entry);
-- `prose` is the one form that cannot tell an ADDRESS from a CONSTANT of the same width.
-- Measured 2026-09-08: of the 12 function entries it contributes that no other form
-- reaches, two are values -- `+0x118 = 0x003C0000` (a field default, landing inside
-- FUN_003bfff0) and `0x00555556` (the compiler's divide-by-3 magic, landing inside
-- 00555400). The other ten are entries written bare in a sentence and are real. So the
-- rows are KEPT and the form is EXCLUDED from the cited set: use `cited` to ask "does any
-- document discuss this?", `citations` to see every form including the unreliable one.
CREATE VIEW cited AS SELECT * FROM citations WHERE form <> 'prose';
CREATE INDEX ix_edge_callee ON edges(callee);
CREATE INDEX ix_edge_caller ON edges(caller);
CREATE TABLE field_access (type TEXT, disp TEXT, base TEXT, kind TEXT,
                           function_entry TEXT, site TEXT, instruction TEXT, note TEXT);
CREATE INDEX ix_gref_addr ON global_refs(address);
CREATE INDEX ix_gref_fn ON global_refs(function_entry);
CREATE INDEX ix_fa_type ON field_access(type);
CREATE INDEX ix_fa_fn ON field_access(function_entry);
-- Revision coherence (2026-09-24/25): `PRAGMA integrity_check` passing says nothing about
-- freshness - the mirror shipped 17,269 field_access rows against a 20,011-row TSV - and a
-- sha256 of WORKTREE bytes is not a pin either: it can match no commit at all. schema_version 3
-- records the pin: pinned_commit names the revision the bytes came from (NULL = worktree
-- build), git_blob is that source's blob oid at the ref (NULL = the source has no versioned
-- home - the Tools/work generated TSVs - and its hash is a worktree signature only).
CREATE TABLE provenance (table_name TEXT, source TEXT, source_sha256 TEXT, git_blob TEXT,
                         pinned_commit TEXT, rows INTEGER, built_at TEXT,
                         schema_version INTEGER, generator_sha256 TEXT,
                         output_sha256 TEXT);
CREATE INDEX ix_fields_type ON fields(type);
"""


def load_functions():
    entries, rows = [], []
    f, _origin = src_lines_stream(FUNCS)
    if f is None:
        return entries, rows
    f.readline()
    for line in f:
        p = (line.rstrip("\n").split("\t") + [""] * 9)[:9]
        try:
            e = int(p[0], 16)
        except ValueError:
            continue
        is_eh = 1 if "CompilerGeneratedEH" in p[8] else 0
        is_gen = 1 if p[1].startswith(("Unwind@", "Catch_All@")) else 0
        rows.append((p[0], p[1], int(p[2]) if p[2].isdigit() else 0, p[3], p[5], p[6], p[8],
                     is_eh, is_gen))
        if not is_gen:
            entries.append((e, int(p[2]) if p[2].isdigit() else 0))
    entries.sort()
    return entries, rows


def resolve(entries, starts, va):
    """Which function body contains this VA? None if it falls in no body."""
    import bisect
    i = bisect.bisect_right(starts, va) - 1
    if i < 0:
        return None
    e, size = entries[i]
    return e if va < e + size else None


def frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    fm, body = {}, text[end + 4:]
    key = None
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            # A trailing ` # ...` is a comment, not part of the value. Leaving it in made
            # `level` read as "L2   # calculation parity only, ..." and split one census bucket
            # into two.
            fm[key] = re.sub(r"\s+#.*$", "", m.group(2)).strip()
        elif key and line.startswith(("  ", "\t")) and ":" in line:
            k2, v2 = line.strip().split(":", 1)
            fm[key + "." + k2.strip()] = v2.strip()
    return fm, body


SECTION_RE = re.compile(r"^## (\d+)\.\s*(.+?)\s*$", re.M)


def contract_parts(text):
    """(sections, claims) for one contract.

    The seven contracts share a 16-section skeleton exactly -- every numbered heading from 2 to 16
    appears in all seven, which is what makes this parsable at all rather than a heuristic over
    prose. Section 1 is the only variance: six say `Purpose`, one says `What the player sees`.

    **Columns in the section-15 evidence table are mapped BY HEADER, not by position.** Six of the
    seven write `| claim | evidence | tier | confidence |` and `CONTRACT-widget-object.md` writes
    `| claim | evidence | tier |` with no confidence column. Reading column 4 positionally would
    have silently invented a confidence for six documents and lost it for one.
    """
    heads = [(int(m.group(1)), m.group(2), m.start(), m.end()) for m in SECTION_RE.finditer(text)]
    sections, claims = [], []
    for i, (num, title, _st, en) in enumerate(heads):
        body = text[en:heads[i + 1][2]] if i + 1 < len(heads) else text[en:]
        sections.append((num, title, len(body),
                         sum(1 for l in body.split(chr(10)) if l.lstrip().startswith("- ")),
                         body.count("```") // 2))
        if num != 15:
            continue
        rows = [l.strip() for l in body.split(chr(10)) if l.strip().startswith("|")]
        if len(rows) < 3:
            continue
        cols = [c.strip().lower() for c in rows[0].strip("|").split("|")]
        for r in rows[2:]:
            cells = [c.strip() for c in r.strip("|").split("|")]
            if len(cells) < len(cols):
                continue
            g = dict(zip(cols, cells))
            claims.append((g.get("claim", ""), g.get("evidence", ""),
                           g.get("tier", ""), g.get("confidence", "")))
    return sections, claims


def build(conn, verbose=True):
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    entries, frows = load_functions()
    starts = [e for e, _ in entries]
    cur.executemany("INSERT INTO functions VALUES (?,?,?,?,?,?,?,?,?)", frows)

    eh = set(r[0] for r in frows if r[7])
    f, _origin = src_lines_stream(EDGES)
    erows = []
    if f is not None:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4:
                erows.append((p[0], p[1], p[3], 1 if p[0] in eh else 0))
    cur.executemany("INSERT INTO edges VALUES (?,?,?,?)", erows)

    f, _origin = src_lines_stream(GREFS)
    if f is not None:
        grows = []
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4:
                grows.append((p[0], p[1].upper().replace("0X", ""), p[2], p[3]))
        cur.executemany("INSERT INTO global_refs VALUES (?,?,?,?)", grows)

    # documents + citations
    dcount = ccount = ncount = 0
    docs_manifest = hashlib.sha256()   # every .md walked, indexed or not - the tree is the source
    for frel in tree_files(DB_DIR, ".md"):
        path = os.path.relpath(os.path.join(ROOT, frel), DB_DIR).replace("\\", "/")
        text, _origin = src_text(os.path.join(ROOT, frel))
        if text is not None:
            # Manifest keys are ROOT-relative and content is CRLF-normalised - the same
            # digest dep_digest() recomputes for `check`. A mismatch here would be a
            # permanent false-stale report on every doc table.
            docs_manifest.update((frel + "\n" +
                                  _norm_sha256(text.replace("\r\n", "\n")
                                               .encode("utf-8")) +
                                  "\n").encode("utf-8"))
            fm, body = frontmatter(text)
            if fm is None:
                continue
            dcount += 1
            # `_templates/CONTRACT.md` carries `contract:` and `scope:` because it IS the shape of
            # a contract. Counting it made this index report 3 contracts against
            # `program_coverage.py`'s 2. The template is kept as a row and excluded by every query.
            is_template = 1 if path.startswith(("_templates/", "_experiments/")) else 0
            is_contract = 1 if ("contract" in fm and "scope" in fm and not is_template) else 0
            # RUNTIME MARKERS ARE COUNTED OVER THE BODY MINUS A CONTRACT'S SECTION 13, because that
            # section is where a contract states it has NO runtime validation and says what would be
            # needed - "one breakpoint on 00377C5F settles it". The marker list is a substring match
            # including 'breakpoint' and 'debugger', so ASKING for evidence was being counted as
            # HAVING it. Measured before this change: of 10 contracts with runtime_markers > 0, five
            # declared in their own section 13 that there is none, across five categories.
            scan = RT_S13.sub("\n", text) if is_contract else text
            cur.execute("INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                path, fm.get("system"), fm.get("category"), fm.get("status"),
                fm.get("owner_layer"), fm.get("evidence_tier"), fm.get("level"),
                fm.get("readiness"), fm.get("confidence"), fm.get("scope"),
                fm.get("last_reviewed"), fm.get("falsification_passes"),
                is_contract, is_template, len(text),
                sum(1 for m in RUNTIME_MARKERS if m in scan.lower())))
            cur.executemany("INSERT INTO doc_fields VALUES (?,?,?)",
                            [(path, k, v) for k, v in sorted(fm.items())])
            if is_contract:
                secs, clms = contract_parts(body)
                cur.executemany("INSERT INTO contract_sections VALUES (?,?,?,?,?,?)",
                                [(path,) + t for t in secs])
                cur.executemany("INSERT INTO contract_claims VALUES (?,?,?,?,?)",
                                [(path,) + t for t in clms])
            # A generated index is not a source of names -- it is a rendering of them. Marked
            # rather than skipped, so a query can choose, and so the flag is visible if one of
            # these ever becomes hand-edited.
            gen_index = 1 if path in ("_index/ADDRESS-INDEX.md", "_index/RULES-INDEX.md") else 0
            named = _cs.SUPERSEDED_SECTION.sub("", text)
            nseen = set()
            for pat in _cs.NAME_PATTERNS:
                for m in pat.finditer(named):
                    a, nm = m.group(1).upper(), m.group(2)
                    if (a, nm) in nseen:
                        continue
                    nseen.add((a, nm))
                    r = resolve(entries, starts, int(a, 16))
                    cur.execute("INSERT INTO doc_names VALUES (?,?,?,?,?,?)",
                                (path, a, nm, "%08X" % r if r is not None else None,
                                 1 if r == int(a, 16) else 0, gen_index))
                    ncount += 1
            for a, form in sorted(citation_forms(text).items()):
                va = int(a, 16)
                r = resolve(entries, starts, va)
                cur.execute("INSERT INTO citations VALUES (?,?,?,?,?)",
                            (path, a, "%08X" % r if r is not None else None,
                             1 if r == va else 0, form))
                ccount += 1

    # types + fields
    tp = os.path.join(DB_DIR, "_types", "types.tsv")
    rows, _origin = src_lines(tp)
    if rows:
        rows = [l.rstrip("\n").split("\t") for l in rows]
        h = rows[0]
        for r in rows[1:]:
            d = dict(zip(h, r + [""] * len(h)))
            cur.execute("INSERT INTO types VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                d.get("type"), d.get("size"), d.get("category"), d.get("instance"),
                d.get("allocation_site"), d.get("ctor"), d.get("dtor"), d.get("readiness"),
                d.get("confidence"), d.get("level"), d.get("documents")))
    fp = os.path.join(DB_DIR, "_types", "fields.tsv")
    rows, _origin = src_lines(fp)
    if rows:
        rows = [l.rstrip("\n").split("\t") for l in rows]
        h = rows[0]
        for r in rows[1:]:
            d = dict(zip(h, r + [""] * len(h)))
            if not (d.get("type") or "").strip() and not (d.get("offset") or "").strip():
                continue  # a trailing whitespace line is not a field row
            nm = (d.get("name") or "")
            # `size` is authored decimal OR hex (0x18 - two 24-byte Lua headers read as 0
            # under isdigit()); variable sizes stay 0 - that is the store's marker for them.
            sv = (d.get("size") or "").strip()
            try:
                size = int(sv, 16) if sv.lower().startswith("0x") else int(sv)
            except ValueError:
                size = 0
            cur.execute("INSERT INTO fields VALUES (?,?,?,?,?,?,?,?,?)", (
                d.get("type"), d.get("offset"), size,
                nm, d.get("ctype"), d.get("meaning"), d.get("readiness"), d.get("confidence"),
                0 if ("UNRESOLVED" in nm.upper() or not nm) else 1))

    # field_access - the F-6 (type, offset) -> accessor index. disp/base come in as `0x%X`
    # and are stored WITHOUT the prefix, uppercase, the same normalisation global_refs uses
    # and the same shape the --arg handler hands to the query.
    fap = os.path.join(DB_DIR, "_types", "field-access-index.tsv")
    fa, _origin = src_lines_stream(fap)
    if fa is not None:
        fa.readline()
        for line in fa:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 8:
                cur.execute("INSERT INTO field_access VALUES (?,?,?,?,?,?,?,?)", (
                    p[0], p[1].upper().replace("0X", ""), p[2].upper().replace("0X", ""),
                    p[3], p[4], p[5], p[6], p[7]))

    # questions - states come from check_questions.py, the gate that owns this file. In a
    # pinned build the SAME parser runs on the ref's bytes through a temp dir - one parser,
    # never a second definition (the import comment above is the rule this follows).
    qp = os.path.join(DB_DIR, "_index", "OPEN-QUESTIONS.md")
    qtext, _origin = src_text(qp)
    if PIN:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            os.mkdir(os.path.join(td, "_index"))
            io.open(os.path.join(td, "_index", "OPEN-QUESTIONS.md"), "w",
                    encoding="utf-8").write(qtext or "")
            table, _dupes = _cq.read_table(td)
    else:
        table, _dupes = _cq.read_table(DB_DIR)
    qtext = qtext or ""
    cells = {}
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % _cq.QID, qtext, re.M):
        c = [x.strip() for x in m.group(2).split("|") if x.strip() != ""]
        cells[m.group(1)] = (c[0] if c else "", c[1] if len(c) > 1 else "")
    for qid, state in table.items():
        q, ans = cells.get(qid, ("", ""))
        cur.execute("INSERT OR REPLACE INTO questions VALUES (?,?,?,?)", (qid, q, state, ans))

    # script verbs - the opcode -> native handler bridge. Its `handler` column is re-derivable
    # from the binary (scriptvm_dispatch_verify.py); `verb`/`args` come from an authored external
    # catalog and `owner` from the ledger, which is why the file carries per-column provenance.
    sp = os.path.join(DB_DIR, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-dispatch.tsv")
    splines, _origin = src_lines(sp)
    if splines:
        for line in splines:
            if not line.strip() or line.startswith("#") or line.startswith("call_id"):
                continue
            c = (line.split("\t") + [""] * 6)[:6]
            cur.execute("INSERT INTO script_verbs VALUES (?,?,?,?,?,?)", tuple(c))

    # contradictions - claims this database has overturned. Extracted mechanically from dated
    # correction headers by contradiction_index.py; the summary columns are hand-written.
    cp2 = os.path.join(DB_DIR, "_index", "CONTRADICTIONS.tsv")
    cplines, _origin = src_lines(cp2)
    if cplines:
        chead = None
        for line in cplines:
            if not line.strip() or line.startswith("#"):
                continue
            if chead is None:
                chead = line.split(chr(9))
                continue
            c = dict(zip(chead, line.split(chr(9)) + [""] * len(chead)))
            cur.execute("INSERT INTO contradictions VALUES (?,?,?,?,?,?,?,?,?,?)",
                        tuple(c.get(k, "") for k in
                              ("id", "date", "kind", "category", "document", "line",
                               "claim", "correction", "instrument", "addresses")))

    # reconstructions
    recon_manifest = hashlib.sha256()
    for frel in tree_files(RECON):
        fn = os.path.basename(frel)
        p = os.path.relpath(os.path.join(ROOT, frel), RECON).replace("\\", "/")
        b, _origin = src_bytes(os.path.join(ROOT, frel))
        if b is None:
            continue
        recon_manifest.update(
            (frel + "\n" + (_norm_sha256(b) or "-") + "\n").encode("utf-8"))
        if fn.endswith(".c") and "/Tests/" not in "/" + p:
            cur.execute("INSERT INTO reconstructions VALUES (?,?,?,?)",
                        (fn[:-2], p, None, "implementation"))
        elif fn.startswith("diff_") and fn.endswith(".py"):
            cur.execute("INSERT INTO reconstructions VALUES (?,?,?,?)",
                        (fn[5:-3], None, p, "differential-test"))

    # provenance - one row per (table, dependency), so a joined table is stale when ANY of
    # its inputs moves. `source` is the dep_key label ('file:<rel>' / 'tree:<rel>;<suffix>')
    # prefixed 'git:' when the bytes came from the pinned ref; source_sha256 is the
    # CRLF-normalised content digest (git_blob stays the exact-bytes git identity).
    # generator_sha256 names the module set that produced the rows; output_sha256 is the
    # table's own row digest - the hand-edited-DB tell.
    built_at = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    pinned = pinned_commit(PIN) if PIN else None
    gen = generator_digest()
    tree_digests = {dep_key(("tree", DB_DIR, ".md")): docs_manifest.hexdigest(),
                    dep_key(("tree", RECON, None)): recon_manifest.hexdigest()}
    output_digests = {}
    for t in table_deps():
        output_digests[t] = _table_digest(cur, t)

    def _prov(t, desc, digest, blob=None):
        # `source` is the dep_key label - `check` resolves it back to a descriptor through
        # table_deps(). git_blob non-NULL is the "these bytes have a versioned home" marker.
        if desc[0] == "file" and PIN:
            r = _git(PIN, ["rev-parse", "--verify", "%s:%s" % (PIN, _git_rel(desc[1]))])
            if r.returncode == 0:
                blob = r.stdout.decode("ascii", "replace").strip()
        cur.execute("INSERT INTO provenance VALUES (?,?,?,?,?,?,?,?,?,?)", (
            t, dep_key(desc), digest, blob, pinned,
            cur.execute("SELECT COUNT(*) FROM " + t).fetchone()[0],
            built_at, SCHEMA_VERSION, gen, output_digests[t]))

    for t, ds in sorted(table_deps().items()):
        for d in ds:
            if d[0] == "tree":
                _prov(t, d, tree_digests[dep_key(d)])
            else:
                b, _origin = src_bytes(d[1])
                _prov(t, d, _norm_sha256(b))
    conn.commit()
    if verbose:
        for t in ("documents", "doc_fields", "citations", "doc_names", "contract_sections",
                  "contract_claims", "functions", "edges",
                  "global_refs", "field_access", "types", "fields", "questions",
                  "reconstructions", "script_verbs", "contradictions"):
            print("  %-16s %8d" % (t, cur.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]))


# ---------------------------------------------------------------- charter section 7 queries
#   name: (supported, sql or the reason it is not supported)
QUERIES = {
    # One row per FUNCTION with a site count, not one row per site. The first version returned
    # sites and reported 28 readers of 02F9736C where `globals_index.py` reports 27 - both correct,
    # different questions. A query whose row count silently means something else than the tool
    # beside it is a trap, so the unit is named in the output.
    # kind 'rw' counts as BOTH a read and a write - the read-modify-write class exists
    # since the 2026-09-26 direction regeneration (gen_rip_data_refs.py); before it the
    # same sites were labelled 'write' with the read side lost.
    "writers-of-global": (True, """
        SELECT g.function_entry, f.name, COUNT(*) AS sites FROM global_refs g
          LEFT JOIN functions f ON f.entry = g.function_entry
         WHERE g.address = :arg AND g.kind IN ('write','rw')
         GROUP BY g.function_entry ORDER BY g.function_entry"""),
    "readers-of-global": (True, """
        SELECT g.function_entry, f.name, COUNT(*) AS sites FROM global_refs g
          LEFT JOIN functions f ON f.entry = g.function_entry
         WHERE g.address = :arg AND g.kind IN ('read','rw')
         GROUP BY g.function_entry ORDER BY g.function_entry"""),
    "callers": (True, """
        SELECT caller, (SELECT name FROM functions WHERE entry = caller) FROM edges
         WHERE callee = :arg AND caller_is_eh = 0 ORDER BY caller"""),
    "callers-including-banned": (True, """
        SELECT caller, caller_is_eh,
               (SELECT name FROM functions WHERE entry = caller) FROM edges
         WHERE callee = :arg ORDER BY caller_is_eh, caller"""),
    "unresolved-fields": (True, """
        SELECT type, offset, size, name, readiness FROM fields
         WHERE resolved = 0 ORDER BY type, offset"""),
    "documents-citing": (True, """
        SELECT path, address, resolved_entry FROM citations
         WHERE address = :arg OR resolved_entry = :arg ORDER BY path"""),
    "subsystem-functions": (True, """
        SELECT DISTINCT c.resolved_entry, f.name, f.body_bytes FROM citations c
          LEFT JOIN functions f ON f.entry = c.resolved_entry
         WHERE c.path LIKE :arg || '%' AND c.resolved_entry IS NOT NULL
         ORDER BY f.body_bytes DESC"""),
    "contracts": (True, """
        SELECT path, system, scope, readiness, confidence FROM documents
         WHERE is_contract = 1 AND is_template = 0 ORDER BY path"""),
    "reconstruction-ready": (True, """
        SELECT path, system, scope, readiness FROM documents
         WHERE is_template = 0
           AND readiness IN ('RECONSTRUCTION READY','IMPLEMENTED','DIFFERENTIAL TESTED')
         ORDER BY path"""),
    "implemented-without-parity": (True, """
        SELECT name, source_path FROM reconstructions WHERE kind = 'implementation'
           AND name NOT IN (SELECT name FROM reconstructions WHERE kind = 'differential-test')"""),
    # Uses the BODY-text marker count, not frontmatter - see RUNTIME_MARKERS. The frontmatter
    # version of this query returned every document, because no frontmatter key carries it.
    "high-confidence-no-runtime": (True, """
        SELECT d.path, d.confidence, d.readiness FROM documents d
         WHERE d.is_template = 0 AND d.confidence IN ('PROVEN','VERY HIGH')
           AND d.runtime_markers = 0
         ORDER BY d.path"""),
    "runtime-evidenced": (True, """
        SELECT d.category, d.path, d.runtime_markers FROM documents d
         WHERE d.is_template = 0 AND d.runtime_markers > 0
         ORDER BY d.runtime_markers DESC, d.path"""),
    "questions-by-state": (True, """
        SELECT state, COUNT(*) FROM questions GROUP BY state ORDER BY COUNT(*) DESC"""),
    # Contracts no longer carry `level:` (FABLE ruling 2026-10-03: maturity is measured, never declared in
    # front matter; grain is `scope:`). This census covers the non-contract pages that still state one.
    "level-census": (True, """
        SELECT COALESCE(level,'(unstated)') AS lvl, COUNT(*) FROM documents
         WHERE is_template = 0 AND is_contract = 0 GROUP BY lvl ORDER BY COUNT(*) DESC"""),
    "readiness-census": (True, """
        SELECT COALESCE(readiness,'(unstated)') AS r, COUNT(*) FROM documents
         WHERE is_template = 0 GROUP BY r ORDER BY COUNT(*) DESC"""),
    "eh-edge-census": (True, """
        SELECT caller_is_eh, COUNT(*) FROM edges GROUP BY caller_is_eh"""),
    # --- charter section 7 items this schema CANNOT answer, and why -----------------------
    # SUPPORTED as of 2026-09-22 (F-6). arg is `TypeName+OFFSET` with no 0x, e.g.
    # `ManagerSingleton0209BE80+80`; the type half is compared case-insensitively because
    # the arg handler uppercases the whole argument. The offset half accepts leading zeros
    # (+0, +00, +08 all normalise to the stored no-0x form). Coverage is the index's coverage:
    # 212 of 596 types are seeded; an absent type means the instrument did not run.
    "writers-of-field": (True, """
        SELECT a.function_entry, f.name, COUNT(*) AS sites FROM field_access a
          LEFT JOIN functions f ON f.entry = a.function_entry
         WHERE upper(a.type) = substr(:arg, 1, instr(:arg, '+') - 1)
           AND a.disp = CASE WHEN ltrim(substr(:arg, instr(:arg, '+') + 1), '0') = ''
                             THEN '0' ELSE ltrim(substr(:arg, instr(:arg, '+') + 1), '0') END
           AND a.kind IN ('w', 'rw')
         GROUP BY a.function_entry ORDER BY a.function_entry"""),
    "accessors-of-field": (True, """
        SELECT a.function_entry, f.name, a.kind, COUNT(*) AS sites FROM field_access a
          LEFT JOIN functions f ON f.entry = a.function_entry
         WHERE upper(a.type) = substr(:arg, 1, instr(:arg, '+') - 1)
           AND a.disp = CASE WHEN ltrim(substr(:arg, instr(:arg, '+') + 1), '0') = ''
                             THEN '0' ELSE ltrim(substr(:arg, instr(:arg, '+') + 1), '0') END
         GROUP BY a.function_entry, a.kind ORDER BY a.function_entry, a.kind"""),
    "accessors-of-type": (True, """
        SELECT a.disp, a.kind, a.function_entry, f.name FROM field_access a
          LEFT JOIN functions f ON f.entry = a.function_entry
         WHERE (:arg IS NULL OR upper(a.type) = :arg)
         ORDER BY length(a.disp), a.disp, a.function_entry"""),
    # SUPPORTED as of 2026-09-08. The claim that no machine-readable table existed was WRONG:
    # 1,224 rows had been extracted long before, into a GITIGNORED scratch directory, and the
    # dispatch document pointed readers at that path. Re-derived from the binary (1,224/1,224
    # agree) and imported with per-column provenance.
    "script-opcode-callees": (True, """
        SELECT s.call_id, s.verb, s.args, s.handler, f.name, f.body_bytes
          FROM script_verbs s LEFT JOIN functions f ON f.entry = s.handler
         WHERE (:arg IS NULL OR s.verb LIKE '%' || :arg || '%' OR s.handler = :arg)
         ORDER BY s.call_id"""),
    "script-verbs-undocumented": (True, """
        SELECT s.call_id, s.verb, s.handler, f.body_bytes FROM script_verbs s
          LEFT JOIN functions f ON f.entry = s.handler
         WHERE s.handler NOT IN (SELECT resolved_entry FROM cited
                                  WHERE resolved_entry IS NOT NULL)
         ORDER BY f.body_bytes DESC"""),
    "resources-by-subsystem": (False,
        "No resource table exists in the schema. Resource ids appear inside document prose only."),
    "behaviour-known-params-unresolved": (False,
        "Requires per-function signature records. `functions.tsv` carries no parameter data and "
        "no document set declares signatures in a parsable form outside the 2 contracts."),
    # SUPPORTED as of 2026-09-08. It WAS the single biggest gap; `contradiction_index.py` now
    # extracts dated correction headers mechanically and the summary columns are hand-written.
    "contradictions-by-subsystem": (True, """
        SELECT category, COUNT(*) FROM contradictions
         WHERE (:arg IS NULL OR category LIKE '%' || :arg || '%')
         GROUP BY category ORDER BY COUNT(*) DESC"""),
    "contradictions-by-instrument": (True, """
        SELECT instrument, COUNT(*) AS n, GROUP_CONCAT(DISTINCT category) FROM contradictions
         WHERE instrument NOT IN ('', 'UNSUMMARISED')
         GROUP BY instrument ORDER BY n DESC"""),
    # Charter section 3's BEHAVIOUR dimension, which the reconstruction-grade audit reported
    # UNMEASURABLE on 2026-09-08: "the schema has nowhere to put preconditions, postconditions,
    # invariants, state transitions or failure paths outside contract prose". There are now seven
    # contracts sharing an exact 16-section skeleton, so the prose IS the record type -- it just
    # had no index. These three queries are that index.
    "behaviour": (True, """
        SELECT s.path,
               MAX(CASE WHEN s.num = 4  THEN s.chars END) AS pre_post_invariants,
               MAX(CASE WHEN s.num = 7  THEN s.chars END) AS state_transitions,
               MAX(CASE WHEN s.num = 10 THEN s.chars END) AS failure_paths,
               MAX(CASE WHEN s.num = 5  THEN s.chars END) AS state_read_written,
               MAX(CASE WHEN s.num = 12 THEN s.chars END) AS reproduction_formula
          FROM contract_sections s
         WHERE (:arg IS NULL OR s.path LIKE '%' || :arg || '%')
         GROUP BY s.path ORDER BY s.path"""),
    "contract-claims": (True, """
        SELECT path, tier, confidence, claim FROM contract_claims
         WHERE (:arg IS NULL OR path LIKE '%' || :arg || '%')
         ORDER BY path, confidence, claim"""),
    # The honest frontier: a claim a contract itself marks UNKNOWN, or leaves untiered.
    "unresolved-claims": (True, """
        SELECT path, claim, evidence FROM contract_claims
         WHERE upper(confidence) LIKE '%UNKNOWN%' OR trim(coalesce(tier,'')) IN ('', '—', '-')
         ORDER BY path"""),
    "state-machine-dependents": (False,
        "No state-machine record type. State transitions live in contract section 7 prose."),
    # Identity, the charter section 3 dimension this index could not answer until 2026-09-08.
    #
    # `is_entry = 1` is load-bearing, not tidiness. A name written against an address INSIDE a body
    # -- "`0032ABC8` | the clear arm" -- is a name for a point, not for the function, and counting
    # it as one inflated the first run by exactly 6. Restricting to entry addresses reproduces
    # `check_consistency.py`'s 5,812 to the row, which is the control this query is checked by.
    # Generated indexes are excluded on principle: a rendering of a name is not a source of one.
    # (They currently contribute 0 rows -- the patterns do not match a generated table -- so the
    # flag is a guard against a future edit, not a filter doing present work.)
    #
    # THE ANSWER IS A RANGE, AND THAT IS THE PATTERNS' FAULT, NOT THE DATA'S. `NAME_PATTERNS` was
    # built for DISAGREEMENT detection -- two different names for one address -- where a loose
    # match is harmless because it only fires on a conflict. Used as a CENSUS the looseness shows:
    # `` `ADDR` | heaviest `` matches, and so does `` `ADDR` | PArray ``, and only one of those is
    # noise. The identifier-shaped row is the defensible lower bound; the raw row is the upper.
    # Neither is tightened further here, because the tightening rule would itself be a guess.
    "identity": (True, """
        SELECT 'cited function entries' AS k, COUNT(DISTINCT resolved_entry) AS n
          FROM cited WHERE resolved_entry IS NOT NULL
        UNION ALL SELECT '...named at its entry in a document', COUNT(DISTINCT resolved_entry)
          FROM doc_names WHERE is_generated_index = 0 AND is_entry = 1 AND resolved_entry IN
               (SELECT resolved_entry FROM cited WHERE resolved_entry IS NOT NULL)
        UNION ALL SELECT '......of those, identifier-shaped (the LOWER bound)',
               COUNT(DISTINCT resolved_entry) FROM doc_names
         WHERE is_generated_index = 0 AND is_entry = 1
           AND resolved_entry IN (SELECT resolved_entry FROM cited)
           AND (instr(name, '_') > 0 OR name GLOB '*[a-z][A-Z]*'
                OR instr(name, ':') > 0 OR instr(name, '.') > 0)
        UNION ALL SELECT '...named ONLY at an interior address', COUNT(*) FROM (
          SELECT DISTINCT resolved_entry AS e FROM doc_names
           WHERE is_generated_index = 0 AND is_entry = 0 AND resolved_entry IS NOT NULL
             AND e IN (SELECT resolved_entry FROM cited)
             AND e NOT IN (SELECT resolved_entry FROM doc_names
                            WHERE is_generated_index = 0 AND is_entry = 1))
        UNION ALL SELECT '...named in the GFZ ledger', COUNT(*) FROM functions
         WHERE substr(name,1,4) <> 'FUN_' AND entry IN (SELECT resolved_entry FROM cited)
        UNION ALL SELECT '...named in neither', COUNT(*) FROM (
          SELECT DISTINCT resolved_entry AS e FROM cited WHERE resolved_entry IS NOT NULL
           AND e NOT IN (SELECT resolved_entry FROM doc_names
                          WHERE is_generated_index = 0 AND is_entry = 1
                            AND resolved_entry IS NOT NULL)
           AND e IN (SELECT entry FROM functions WHERE substr(name,1,4) = 'FUN_'))"""),
    # The export backlog: this database HAS the name and the ledger does not carry it.
    "named-in-prose-not-in-ledger": (True, """
        SELECT d.resolved_entry, f.body_bytes, f.owner, MIN(d.name), COUNT(DISTINCT d.path)
          FROM doc_names d JOIN functions f ON f.entry = d.resolved_entry
         WHERE d.is_generated_index = 0 AND d.is_entry = 1 AND substr(f.name,1,4) = 'FUN_'
           AND (:arg IS NULL OR f.owner = :arg)
         GROUP BY d.resolved_entry, f.body_bytes, f.owner
         ORDER BY f.body_bytes DESC"""),
    # A cited function nobody has named anywhere - the real identity frontier.
    "unnamed-cited": (True, """
        SELECT f.entry, f.body_bytes, f.owner, COUNT(DISTINCT c.path) AS documents
          FROM functions f JOIN cited c ON c.resolved_entry = f.entry
         WHERE substr(f.name,1,4) = 'FUN_' AND f.is_generated = 0 AND f.is_eh = 0
           AND f.entry NOT IN (SELECT resolved_entry FROM doc_names
                                WHERE is_generated_index = 0 AND resolved_entry IS NOT NULL)
         GROUP BY f.entry, f.body_bytes, f.owner
         ORDER BY f.body_bytes DESC"""),
}


def cmd_queries(conn):
    sup = [k for k, v in QUERIES.items() if v[0]]
    uns = [k for k, v in QUERIES.items() if not v[0]]
    print("SUPPORTED (%d)" % len(sup))
    for k in sorted(sup):
        print("   %s" % k)
    print()
    print("NOT SUPPORTED (%d) - charter section 7 asks for these and the data does not exist yet"
          % len(uns))
    for k in sorted(uns):
        print("   %s\n      %s" % (k, QUERIES[k][1]))


def cmd_build(out, verbose=True):
    """Build into a staging file, guard against mid-flight input edits, then publish data and
    provenance together via os.replace. If a dependency moved during the build the staged file
    is discarded and the last usable index is left untouched - a torn snapshot must never
    land. Under --pin the inputs are immutable git blobs, so the guard has nothing to catch."""
    before = None if PIN else current_fingerprints()
    tmp = out + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    conn = sqlite3.connect(tmp)
    if verbose:
        print("building %s" % out)
    build(conn, verbose=verbose)
    conn.close()
    if before is not None:
        after = current_fingerprints()
        moved = sorted(k for k in set(before) | set(after)
                       if before.get(k) != after.get(k))
        if moved:
            os.remove(tmp)
            sys.stderr.write("inputs changed mid-build; staged build discarded, the last "
                             "usable index is kept. Moved: %s\n" % ", ".join(moved))
            return 3
    os.replace(tmp, out)
    if verbose:
        print("ok")
    return 0


def _freshness_banner(status, stale, meta, prefix=""):
    """The labeled-snapshot header: revision/hash AND stale status attached, never absent."""
    head = "%sindex built %s, pin=%s, generator=%s" % (
        prefix, meta.get("built_at"), (meta.get("pinned_commit") or "worktree")[:12],
        (meta.get("generator_sha256") or "?")[:12])
    if status != "current":
        print(head)
        for line in stale[:20]:
            print("  STALE " + line)
        if len(stale) > 20:
            print("  STALE ... %d more" % (len(stale) - 20))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["build", "check", "query", "queries", "sql", "info"])
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--pin", default=None, metavar="REF",
                    help="build sources from this git ref's blobs (e.g. HEAD) instead of the "
                         "worktree; provenance then pins every row to the resolved commit")
    ap.add_argument("--against", default=None, metavar="REV",
                    help="check only: compare the recorded inputs with REV's committed blobs instead of the "
                         "worktree (checkpoint mode); live queries keep the worktree rule")
    ap.add_argument("--refresh", action="store_true",
                    help="rebuild through the staging guard first if the index is stale")
    ap.add_argument("--snapshot", action="store_true",
                    help="explicit as-of read: run anyway, with the stale status printed")
    a = ap.parse_args()

    if a.command == "build":
        global PIN
        # Resolve the ref ONCE (SWE2-DATA 2026-10-03): a symbolic `--pin HEAD` was re-resolved by every `git show
        # HEAD:<path>` of a minutes-long build, so with the fleet committing the mirror read blobs from several commits
        # and recorded whichever HEAD came last - a pinned build that matched no commit (measured: the doc-tree digest
        # recorded 66cad161 against 14bd5582d's own f5d4558a).
        PIN = pinned_commit(a.pin) if a.pin else None
        d = os.path.dirname(a.out)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        return cmd_build(a.out)

    if not os.path.exists(a.out):
        sys.stderr.write("no index at %s - run `knowledge_db.py build` first\n" % a.out)
        return 2

    if a.command == "check":
        global AGAINST
        AGAINST = pinned_commit(a.against) if a.against else None   # resolved once, like --pin
        if AGAINST:
            print("check against the committed state of %s (%s), not the worktree" % (AGAINST, pinned_commit(AGAINST)[:12]))
        status, stale, meta = freshness_report(a.out)
        _freshness_banner(status, stale, meta)
        if status == "current":
            print("CURRENT (built %s, pin=%s)" %
                  (meta.get("built_at"), meta.get("pinned_commit") or "worktree"))
        return 0 if status == "current" else 3

    if a.command == "queries":
        conn = sqlite3.connect(a.out)
        cmd_queries(conn)
        conn.close()
        return 0

    if a.command == "info":
        conn = sqlite3.connect(a.out)
        status, stale, meta = freshness_report(a.out)
        _freshness_banner(status, stale, meta)
        for t in ("documents", "citations", "functions", "edges", "global_refs",
                  "field_access", "types", "fields", "questions", "reconstructions",
                  "script_verbs"):
            print("  %-16s %8d" % (t, conn.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]))
        conn.close()
        return 0

    # query / sql - agent-facing reads. A CURRENT answer requires the dependencies the SQL
    # actually touches; a stale index refuses rather than return apparently-current rows
    # (an absence conclusion printed from a stale index is the exact failure this exists
    # against). --refresh rebuilds through the staging guard; --snapshot runs anyway but
    # prints the as-of header so the rows can never masquerade as current.
    if a.command != "sql":
        if not a.rest:
            conn = sqlite3.connect(a.out)
            cmd_queries(conn)
            conn.close()
            return 2
        if a.rest[0] not in QUERIES:
            sys.stderr.write("unknown query %r - run `queries` for the list\n" % a.rest[0])
            return 2
        if not QUERIES[a.rest[0]][0]:
            print("NOT SUPPORTED: %s" % a.rest[0])
            print(QUERIES[a.rest[0]][1])
            return 1
    sql_for_guard = " ".join(a.rest) if a.command == "sql" else QUERIES[a.rest[0]][1]
    status, stale, meta = freshness_report(a.out, tables_of_sql(sql_for_guard) or None)
    if status != "current" and not (a.snapshot or a.refresh):
        _freshness_banner(status, stale, meta)
        print("index is not current - refusing to return apparently-fresh rows.")
        print("  `query --refresh` rebuilds through the staging guard; "
              "`--snapshot` runs a labeled as-of read.")
        return 2
    if a.refresh and status != "current":
        rc = cmd_build(a.out)
        if rc != 0:
            return rc
    if a.snapshot and status != "current":
        _freshness_banner(status, stale, meta, prefix="SNAPSHOT - ")

    conn = sqlite3.connect(a.out)
    if a.command == "sql":
        rows = conn.execute(" ".join(a.rest)).fetchall()
    else:
        sql = QUERIES[a.rest[0]][1]
        arg = a.rest[1].upper().replace("0X", "") if len(a.rest) > 1 else None
        rows = conn.execute(sql, {"arg": arg}).fetchall()

    for r in rows[:a.limit]:
        print("   " + "  ".join("" if x is None else str(x) for x in r))
    print("%d row(s)%s" % (len(rows), "" if len(rows) <= a.limit else
                           " - showing %d, pass --limit" % a.limit))
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
