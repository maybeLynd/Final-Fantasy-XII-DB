#!/usr/bin/env python3
"""check_names.py - verify every function name the database quotes against the ledger.

Written 2026-09-02 after this database published an invented name. `002778C0` appeared in a
listing cut at `BattleMenu_UpdateCommandSelectionAndDisp`; the ending was completed rather than
looked up, and `...AndDisplay` propagated to five places in three files before a full-width
listing showed the real ending, `...AndDispatch`.

A truncated identifier invites completion, and completion feels like reading. This makes that
class of error impossible to keep.

Three verdicts:

  TRUNCATED  the quoted name is a strict prefix of exactly one real name  -> almost certainly a
             name copied from a capped column. Reported with the full name so it can be fixed.
             SUPPRESSED when the same file also contains the full name: a document correcting a
             truncation must be able to quote the wrong form.
  SHORTHAND  the quoted name is a real name minus its `Subsystem_` prefix -> legitimate; the
             database refers to functions by their short form throughout. Counted, not listed.
  INVENTED   the quoted name is not a real name and not a prefix of one   -> either wrong, or
             from a source outside functions.tsv (Ghidra, RTTI, an upstream library). Judgement
             needed; the checker cannot tell those apart and does not try.
  AMBIGUOUS  a strict prefix of several real names -> under-specified, worth completing.

WHAT THIS CANNOT SEE
--------------------
  * Names quoted for a DIFFERENT binary (a Windows API, an upstream library symbol, a C++ class
    from RTTI). Those legitimately do not appear in functions.tsv and land in INVENTED. The
    allow-list below carries the ones already judged; extend it rather than silencing the check.
  * A name that is real but attached to the WRONG address. Membership is all this proves.
"""
import argparse, collections, io, os, re, sys
import kit_paths as KP  # noqa: E402
import os

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

# Prefixes of names that legitimately are not in functions.tsv: RTTI class names, upstream
# libraries, Windows APIs, and this database's own tooling.
ALLOW_PREFIX = (
    "Phyre", "SQEX", "PPFX", "Yebis", "bt", "mkvparser", "JsonBox", "eastl", "std", "sead",
    "IAudioClient", "IMkvReader", "DynGeo", "Chr", "Sep", "Seb", "Shout", "Stream", "Music",
    "Audio", "Game", "Input", "Async", "Asset", "Primitive", "Character", "Ordered", "Map",
    "Font", "VCSteam", "Vorbis", "Mdct", "Inflate", "PClass", "PMethod", "PInternal",
)
ALLOW_EXACT = {
    "_initterm", "_initterm_e", "_aligned_free", "_guard_check_icall", "_guard_dispatch_icall",
    "_register_thread_local_e", "_get_narrow_winmain_comm", "_cexit", "exit", "rand",
    "memcpy", "printf", "atexit", "main",
    # In-database type names (registered in _types/types.tsv), not functions: backticked uses
    # like "`BattleTargetBuffer`" name the 0x208-byte struct, and flagging them against the
    # `BattleTargetBuffer_*` function family cannot be fixed by spelling a struct "in full".
    "BattleTargetBuffer",
}
# Shape of a GFZ-style function name: at least one underscore between word characters,
# or a long CamelCase run. Filters out ordinary prose in backticks.
NAMEISH = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{5,}$")
FENCE = re.compile(r"```.*?```", re.S)
TICKED = re.compile(r"`([^`\n]+)`")


def load_names(path):
    out = set()
    for i, l in enumerate(io.open(path, encoding="utf-8", errors="replace")):
        if i == 0:
            continue
        p = l.rstrip("\n").split("\t")
        if len(p) > 1 and p[1] and not p[1].startswith(("FUN_", "sub_", "Unwind@", "Catch_All@")):
            out.add(p[1])
    return out


def _all_mentions_inside(text, token):
    """True when every occurrence of `token` in `text` is introduced by the word "inside".

    "`actor` inside `PackedActorHandle`" is a claim about one string containing another. The page
    that makes such a claim has to write the containing string, and doing so must not read as a
    citation of a function whose name it is a prefix of.
    """
    if not text or not token:
        return False
    hits = 0
    for m in re.finditer(re.escape(token), text):
        # An occurrence INSIDE a longer identifier is not a citation of anything - the page also
        # writes `PartyFocus_CommitPendingPackedActorHandle_Thunk`, and the token is a substring of
        # it. Only standalone occurrences can be citations, so only those are judged. (This is the
        # page's own subject applied to reading the page.)
        pre = text[m.start() - 1] if m.start() else ""
        post = text[m.end()] if m.end() < len(text) else ""
        if pre.isalnum() or pre == "_" or post.isalnum() or post == "_":
            continue
        hits += 1
        before = text[max(0, m.start() - 40):m.start()]
        if "inside" not in before.lower():
            return False
    return hits > 0


def looks_like_a_name(s):
    if not NAMEISH.match(s):
        return False
    if s in ALLOW_EXACT or s.startswith(ALLOW_PREFIX):
        return False
    if "_" in s:
        return True
    # CamelCase with >= 3 humps
    return len(re.findall(r"[A-Z][a-z]+", s)) >= 3


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--functions", default=FUNCS)
    a = ap.parse_args(argv)

    real = load_names(a.functions)
    by_prefix = collections.defaultdict(list)
    for n in real:
        by_prefix[n[:12]].append(n)

    # POPULATION, narrowed 2026-09-14 (OPUS) to match the rest of the kit.
    #
    # _inbox/* are other agents' raw transcripts, which COVERAGE.md explicitly does not count as
    # documents and which no one maintains for name accuracy; AUDIT-LOG.md is append-only by its
    # own first rule, so a name written there in 2026-09 cannot be corrected later without
    # rewriting the record the log exists to preserve. check_self_contradiction and
    # check_denominators already scope themselves exactly this way. Before this, seven of the
    # thirteen truncations this check reported were unfixable by construction: they sat in the log
    # and the inboxes, so the gate could not reach zero without someone editing history.
    def in_population(rel):
        parts = rel.replace("\\", "/").split("/")
        return "_inbox" not in parts and parts[-1] != "AUDIT-LOG.md"

    quoted = collections.defaultdict(set)
    files = 0
    for root, _, fs in os.walk(a.db):
        for f in fs:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            if not in_population(os.path.relpath(p, a.db)):
                continue
            files += 1
            t = FENCE.sub(" ", io.open(p, encoding="utf-8", errors="replace").read())
            for m in TICKED.finditer(t):
                s = m.group(1).strip()
                if looks_like_a_name(s):
                    quoted[s].add(os.path.relpath(p, a.db))

    # a real name minus its "Subsystem_" prefix is ordinary shorthand, not an error
    short = {}
    for n in real:
        if "_" in n:
            short.setdefault(n.split("_", 1)[1], []).append(n)

    trunc, invented, ambig, shorthand = [], [], [], []
    file_text = {}
    for root, _, fs in os.walk(a.db):
        for f in fs:
            if f.endswith(".md"):
                pth = os.path.join(root, f)
                rel = os.path.relpath(pth, a.db)
                if not in_population(rel):
                    continue
                file_text[rel] = io.open(pth, encoding="utf-8", errors="replace").read()

    for s, where in sorted(quoted.items()):
        if s in real:
            continue
        if s in short:
            shorthand.append((s, short[s]))
            continue
        cands = [n for n in by_prefix.get(s[:12], []) if n.startswith(s) and n != s]
        if len(cands) == 1:
            # A document that also carries the full name is distinguishing two things, not
            # truncating one -- CONTRACT-gameplay-generators.md writes "MSVC CRT's
            # `__isa_available`, written only by `__isa_available_init`", a DATA symbol and the
            # function that writes it, both correct on one line.
            #
            # PER FILE, not all-or-nothing (2026-09-14, OPUS). This was `all(...)`, so one file
            # that lacked the full name made the name report against EVERY file quoting it,
            # including the ones that had it right. A name is truncated in the documents that
            # truncate it.
            # `X` against a function `X_init` is a SYMBOL AND ITS INITIALISER, not a truncation.
            #
            # `__isa_available` is the MSVC CRT's dispatch variable and `__isa_available_init` is
            # the function that writes it; PARITY-STATUS.md says "forcing `__isa_available`",
            # which is a thing you do to a variable. This rule can only fire when `s` is NOT
            # itself a known function name -- that case returns above -- so it applies exactly
            # when the quoted token is some other kind of symbol and a matching initialiser
            # exists, which is the convention it is named for. 2026-09-14, OPUS.
            if cands[0] == s + "_init":
                continue
            bad = [w for w in where if cands[0] not in file_text.get(w, "")]
            # A TOKEN QUOTED AS BEING *INSIDE* ANOTHER NAME IS A MENTION, NOT A CITATION.
            # `PASS22-WHAT-ACCOUNTING-MEANS.md` is a page ABOUT substring accounting, and its two
            # occurrences of `PackedActorHandle` are both of that form - "| **`actor`** | **yes -
            # inside `...PackedActorHandle...`** |" and "OPUS's two accidental clears (`actor`
            # inside `PackedActorHandle`, `gameplay` inside `InputGameplay`)". The page is not
            # citing a function short of its name; it is naming the string that swallowed another
            # string, which is its subject.
            #
            # Third time this distinction decided a finding in two days: a dots-only link written
            # by the page documenting dots-only links, a date tallied by the page tabulating dates,
            # and now a fragment quoted by the page about fragments. A gate that cannot tell a
            # reference from an assertion will always report the documents whose subject is the
            # distinction - and those are the documents most likely to be right.
            #
            # Narrow on purpose: it fires only when EVERY occurrence in that file is introduced by
            # "inside". One ordinary citation anywhere in the file and the finding stands.
            bad = [w for w in bad if not _all_mentions_inside(file_text.get(w, ""), s)]
            if not bad:
                continue
            trunc.append((s, cands[0], bad))
        elif len(cands) > 1:
            ambig.append((s, cands, where))
        else:
            invented.append((s, where))

    print("scanned %d markdown files, %d distinct name-shaped tokens quoted" % (files, len(quoted)))
    print("   verified against the ledger: %d" % len([s for s in quoted if s in real]))
    print("   legitimate shorthand (real name minus its Subsystem_ prefix): %d" % len(shorthand))
    print()
    print("TRUNCATED (a strict prefix of exactly one real name): %d" % len(trunc))
    for s, full, where in trunc:
        print("   %s\n      -> %s\n      in %s" % (s, full, ", ".join(sorted(where))))
    print()
    print("AMBIGUOUS (prefix of several): %d" % len(ambig))
    for s, cands, where in ambig:
        print("   %s -> %d candidates: %s" % (s, len(cands), ", ".join(sorted(cands)[:3])))
    print()
    print("NOT IN THE LEDGER (judge each; may be RTTI, upstream, or wrong): %d" % len(invented))
    for s, where in invented:
        print("   %-52s %s" % (s, ", ".join(sorted(where))[:70]))
    return 1 if trunc else 0


if __name__ == "__main__":
    sys.exit(main())
