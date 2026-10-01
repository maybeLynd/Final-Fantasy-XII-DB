#!/usr/bin/env python3
"""check_novelty_claims.py - test every "the database does not have this" claim against the database.

Why this gate exists
--------------------
`check_absence_claims.py` sweeps claims about the *binary* ("nothing references this") against four
instruments. `check_already_answered.py` answers "do we already have this?" - but only when someone
*asks*, with an address or a term in hand. Neither covers the claim that bit twice:

    2026-09-08  the bridge page filed `EF-5` - "which script opcode reaches these verbs" - as an
                open question. `scriptvm-verb-table.tsv`, two directories away, held all seven rows.

    2026-09-13  the class-registry pass published a section headed "the class IS the id's top
                nibble - **and the page never says so**". `the-encoded-id-space-and-the-query-record.md`
                section 2.1 states `class = nibble + 5` outright - and the same author had
                audited that page five commits earlier.

Both were recoverable by grep. Neither was recovered, because the check was a habit rather than a
step. `check_links` and `check_consistency` both pass on a page that claims novelty: **no existing
gate can see a claim that is merely redundant.**

What it does
------------
Sweeps every document for phrasings that assert the database lacks something, pulls the addresses
and back-ticked identifiers out of the surrounding span, and reports any *other* document that
cites them. A hit means the claim of absence has a neighbour worth reading.

Why the default scope is a section, not a sentence
--------------------------------------------------
The 2026-09-13 case put the claim in a **heading** and its evidence in the **next paragraph**:

    ### The class is the id's top nibble - and the page never says so

    Section 4 calls class 1 "dynamic" and stops. `FUN_00309440`, the function it calls, ...

Sentence scope and paragraph scope both miss that, because the heading names nothing. Section scope
catches it, at the cost of associating a claim with everything under the same heading - which
`--max-tokens` bounds, by skipping a span that names so many things that proximity has stopped
meaning anything. Both motivating cases are regression fixtures in `--self-test`: **a gate that does
not catch what motivated it is not a gate.**

What it does NOT do
-------------------
It does not adjudicate. Association is by proximity, and proximity is a heuristic - the token
nearest a claim may not be its subject, and on the first live run both remaining hits were exactly
that. A document may also legitimately say it does not cover something another does.
**Every hit is a candidate for a human to read**, and the count is the point: nobody can eyeball
every such claim across the corpus.

**One noise class survives and is not filtered**, because filtering it would mean adjudicating: a
page that says *"the biggest function no document has cited"* and then cites it is making a claim
about the population at the moment before it was written, and the addresses under that heading will
legitimately appear in inventories like `the-unresolved-158.md`. Those read as hits. They are
distinguishable only by reading the sentence, which is what the tool asks for.

On the first live run: **515 documents, 76 claim sections, 26 candidates at `--max-tokens 4`.**

Usage
-----
    python check_novelty_claims.py --db "Database/FFXII TZA"
    python check_novelty_claims.py --db "Database/FFXII TZA" --scope sentence
    python check_novelty_claims.py --db "Database/FFXII TZA" --max-tokens 4
    python check_novelty_claims.py --self-test
"""
import argparse
import io
import os
import re
import sys

# Append-only history: these record what was believed at a moment, so a novelty claim inside them
# is a historical statement and not a live one. Same rule as check_stranded_unread.py.
HISTORY_FILES = ("_index/AUDIT-LOG.md", "_index/COVERAGE.md", "_index/PROGRAM-STATE.md",
                 "_index/CONTRADICTION-LEDGER.md", "_index/RESEARCH-PROVENANCE.md")
HISTORY_DIR = "_index/_inbox/"

# The claim shapes. Each asserts the DATABASE (not the binary) lacks something.
CLAIM = re.compile(
    r"(never (?:says|states|said|stated)"
    r"|nowhere (?:says|states|in the (?:database|corpus))"
    r"|(?:is|was|are|were) (?:not |un)stated(?: anywhere)?"
    r"|no (?:document|page|other page|existing coverage|prior coverage)"
    r"|not (?:in|anywhere in) (?:the|this) (?:database|corpus)"
    r"|the (?:database|corpus) (?:does not|doesn't|did not)"
    r"|nothing in (?:the|this) (?:database|corpus)"
    r"|(?:none|neither) of (?:them|these) could see"
    r"|only ever in"
    r"|had (?:no|never had) (?:a )?(?:mapping|name|record))",
    re.I)

# A concordance is not a document that "cites" an address - it lists every address in the corpus, so
# it matches every claim of the form "nothing cites this" and never means anything. Excluded from the
# index only; its own text is still scanned for claims. (First false positive: three interpreter
# addresses "cited nowhere in the corpus", all three duly present in ADDRESS-INDEX.md.)
INDEX_FILES = ("_index/ADDRESS-INDEX.md", "_index/CALL-CHAINS.md", "_index/TYPE-COVERAGE.md",
               "_index/UNEXPLAINED-GLOBALS.md")

# A claim inside a retraction or a struck passage is already handled.
STRIKE = re.compile(r"~~.*?~~", re.S)
# Narrative past tense: "X WAS the largest function no document had ever cited" is a statement about
# the state before this page, and this page citing it is what made it false. (Second false positive:
# a-512-byte-widget-that-registers-itself-once.md on 00565E00.)
PAST = re.compile(r"\b(?:originally|first (?:ran|read|said|published)|had (?:said|read|claimed)"
                  r"|had (?:ever|never) (?:been )?cited|this (?:section|page|row) first|retracted"
                  r"|corrected (?:same day|20\d\d)|used to|until (?:now|this|today))\b", re.I)
# Author- or page-scoped absence: "no document OF MINE cites this" is a claim about one author's
# output, not about the database, so another author's citation does not contradict it. (Third false
# positive: binding-profiles-remapping-and-control-state.md on 00197710.)
SCOPED = re.compile(r"\bno (?:document|page)s? (?:of mine|of my own|in this (?:folder|category))\b"
                    r"|\b(?:this|the present) (?:document|page) does not\b", re.I)

ADDR = re.compile(r"\b(0[0-9A-Fa-f]{7})\b")
# A back-ticked word is only a symbol if it looks like one: an underscore, or a capital after the
# first character. Without this, `switch`, `ret`, `float` and friends match every document in the
# corpus and bury the real pairs. (Fourth false positive: the console page's `switch`, ten
# "neighbours", every one of them meaningless.)
_IDENT = re.compile(r"`([A-Za-z_][A-Za-z0-9_]{5,})`")
_SYMBOLIC = re.compile(r"_|(?<=.)[A-Z]")


class IDENT(object):
    @staticmethod
    def findall(text):
        return [t for t in _IDENT.findall(text) if _SYMBOLIC.search(t)]


def sentences(text):
    """Split into sentences without crossing a markdown table row or a fence line."""
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            continue
        for cell in line.split("|"):
            for part in re.split(r"(?<=[.!?;:])\s+", cell):
                if part.strip():
                    yield part


def load(db):
    docs = {}
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in (".git",)]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace("\\", "/")
            try:
                docs[rel] = io.open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                pass
    return docs


def is_history(rel):
    return rel in HISTORY_FILES or rel.startswith(HISTORY_DIR)


def is_index(rel):
    return rel in INDEX_FILES


def build_index(docs):
    """token -> set of documents citing it. Struck text does not count as a citation."""
    addr_idx, ident_idx = {}, {}
    for rel, text in docs.items():
        if is_history(rel) or is_index(rel):
            continue
        body = STRIKE.sub(" ", text)
        for a in set(x.upper() for x in ADDR.findall(body)):
            addr_idx.setdefault(a, set()).add(rel)
        for i in set(IDENT.findall(body)):
            ident_idx.setdefault(i, set()).add(rel)
    return addr_idx, ident_idx


def units(body, scope):
    """The span a claim is associated with. See --scope in the docstring for why this matters."""
    if scope == "sentence":
        return sentences(body)
    if scope == "paragraph":
        return re.split(r"\n\s*\n", body)
    return re.split(r"\n(?=#{2,6} )", body)          # section: heading to next heading


def scan(db, scope="section", max_tokens=8, docs=None):
    if docs is None:
        docs = load(db)
    addr_idx, ident_idx = build_index(docs)
    findings = []
    phrasings = 0
    skipped = 0
    for rel, text in sorted(docs.items()):
        if is_history(rel):
            continue
        body = STRIKE.sub(" ", text)
        for unit in units(body, scope):
            # Markdown wraps prose, so "no existing\ncoverage" is one phrase to a reader and two
            # tokens to a regex. Match against a flattened copy; report from the original.
            flat = re.sub(r"\s+", " ", unit)
            if not CLAIM.search(flat) or PAST.search(flat) or SCOPED.search(flat):
                continue
            phrasings += 1
            toks = set(x.upper() for x in ADDR.findall(unit)) | set(IDENT.findall(unit))
            # A span naming many things associates the claim with none of them: the wider the
            # span, the weaker proximity gets. The cap is what keeps section scope readable.
            if len(toks) > max_tokens:
                skipped += 1
                continue
            others = {}
            for t in toks:
                for d in (addr_idx.get(t) or ident_idx.get(t) or ()):
                    if d != rel:
                        others.setdefault(d, set()).add(t)
            if others:
                claim = CLAIM.search(flat) or CLAIM.search(unit)
                lo = max(0, claim.start() - 90)
                findings.append((rel, unit[lo:claim.end() + 90].replace("\n", " ").strip(), others))
    return findings, phrasings, len(docs), skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--scope", choices=("sentence", "paragraph", "section"), default="section",
                    help="how far from the claim a token may sit and still be its subject "
                         "(default: section - the scope that catches a claim made in a heading)")
    ap.add_argument("--max-tokens", type=int, default=8,
                    help="skip a span naming more than this many addresses/identifiers (default 8)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.db:
        ap.error("--db is required")
    findings, phrasings, ndocs, skipped = scan(a.db, a.scope, a.max_tokens)
    print("scanned %d documents, scope=%s, max-tokens=%d" % (ndocs, a.scope, a.max_tokens))
    print("novelty / absence-of-coverage claims found: %d" % phrasings)
    print("  skipped as too token-dense to associate: %d" % skipped)
    print("  naming a token another document also cites: %d" % len(findings))
    print()
    for rel, sent, others in findings:
        print("%s" % rel)
        print("   claim: ...%s..." % sent[:190])
        for d, toks in sorted(others.items()):
            print("      also cited in %s  (%s)" % (d, ", ".join(sorted(toks))[:90]))
        print()
    print("A hit is not a verdict. Association is by proximity, and proximity is a heuristic: a page")
    print("may legitimately say it does not cover something another page does, and the token nearest")
    print("a claim may not be its subject. Each pair is a candidate for a human to read - the value is")
    print("that nobody can eyeball every such claim across the corpus.")
    return 0


def self_test():
    """The two cases that motivated the gate, verbatim in shape, plus the filters.

    A gate that does not catch what motivated it is not a gate. REGRESSION-1 is the 2026-09-13
    class-registry claim - **the claim is in the heading and its evidence is in the next
    paragraph**, which is exactly why the default scope is `section` and not `sentence`.
    """
    ok = True

    def check(name, docs, expect_docs, scope="section"):
        nonlocal ok
        f, ph, n, sk = scan(None, scope=scope, docs=docs)
        got = sorted(set(r for r, _, _ in f))
        if got != sorted(expect_docs):
            print("FAIL %s: expected findings in %s, got %s" % (name, sorted(expect_docs), got))
            ok = False

    # REGRESSION-1 - the claim that motivated this gate. Heading asserts, prose evidences.
    reg1 = {
        "00-E/registry.md":
            "### The class is the id's top nibble - and the page never says so\n\n"
            "Section 4 calls class 1 dynamic and stops. `FUN_00309440`, the function it calls,\n"
            "is 30 bytes and reaches 01EEBCF8.\n",
        "00-E/space.md":
            "### 2.1 The id space\n\n`FUN_00309440` (30 B) is the whole derivation; the table\n"
            "begins at 01EEBCC0 and the class field is 01EEBCF8.\n",
    }
    check("REGRESSION-1 (heading claim, prose evidence)", reg1, ["00-E/registry.md"])
    f, _, _, _ = scan(None, scope="sentence", docs=reg1)
    if f:
        print("NOTE: sentence scope now catches REGRESSION-1; the section default may be loosened.")

    # REGRESSION-2 - a question filed whose answer is a sibling file's content.
    reg2 = {
        "01-S/bridge.md": "`EF-5` asks which opcode reaches these verbs; there is no existing\n"
                          "coverage of `btlAtelSetUnit` anywhere.\n",
        "01-S/verbs.md": "The table lists `btlAtelSetUnit` and six more.\n",
    }
    check("REGRESSION-2 (question already answered)", reg2, ["01-S/bridge.md"])

    # Filters, each from a real false positive on 2026-09-13.
    check("strike-through is not a live claim",
          {"a/p.md": "~~nowhere states `FUN_00309440`~~ corrected.\n",
           "b/q.md": "`FUN_00309440` is here.\n"}, [])
    check("a concordance is not a citing document",
          {"a/p.md": "`FUN_00309440` is cited nowhere in the corpus.\n",
           "_index/ADDRESS-INDEX.md": "`FUN_00309440` 00309440\n"}, [])
    check("history records what was believed, not what is",
          {"_index/AUDIT-LOG.md": "no document covers `FUN_00309440`.\n",
           "b/q.md": "`FUN_00309440` is here.\n"}, [])
    check("narrative past tense",
          {"a/p.md": "`FUN_00309440` was the largest function no document had ever cited.\n",
           "b/q.md": "`FUN_00309440` is here.\n"}, [])
    check("an author-scoped absence is not a database claim",
          {"a/p.md": "no document of mine cites `FUN_00309440`.\n",
           "b/q.md": "`FUN_00309440` is here.\n"}, [])
    check("a claim naming nothing else cited is not reported",
          {"a/p.md": "nowhere states `SomethingUniqueHere`.\n",
           "b/q.md": "unrelated.\n"}, [])
    # The token cap must actually suppress a token-dense span.
    dense = {"a/p.md": "## H\n\nnowhere states this. " + " ".join(
        "`Ident%02d`" % i for i in range(12)) + "\n",
        "b/q.md": " ".join("`Ident%02d`" % i for i in range(12)) + "\n"}
    check("a token-dense span is skipped rather than guessed at", dense, [])

    print("self-test: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
