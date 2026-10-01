#!/usr/bin/env python3
"""Cross-check facts the database asserts about the same address in more than one place.

Written after a document was left self-contradictory on 2026-09-02: its headline said two
modes were unreachable while a later section said they were set by the script VM. Neither
`check_links.py` (link targets) nor `verify_doc_addresses.py` (address resolution) can see a
disagreement of that kind, because both check form rather than content.

This checks three things that are mechanical and precise:

  SIZE     the same address given two different byte sizes
  NAME     the same address given two different working names
  COUNT    the same address given two different caller counts

and one lint that is deliberately advisory:

  SUPERSEDED   a document that quotes its own previous wording inside a correction block,
               where that wording still appears elsewhere in the file unmarked

Precision matters more than recall here. A checker that cries wolf gets ignored, and this
database already runs four checks at every commit.
"""
import argparse
import collections
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DEFAULT_DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")

ADDR = r"0[0-9A-Fa-f]{7}"
# `002AE610` (1,281 B)   |   `002AE610` | 1,281 B |   |   002AE610, 1281 bytes
SIZE_PATTERNS = [
    # {0,12} not {0,40}: this pattern is for the immediate parenthetical form "`ADDR` (718 B)",
    # allowing a short connector like " is " or " at ".  At 40 characters it reaches across a whole
    # clause and mis-reads an unrelated size -- it took "`0053E0B0` walks a window's line records
    # (32 bytes each)" as a claim that the FUNCTION is 32 bytes, when 32 is the RECORD STRIDE and the
    # same document correctly gives 718 B in its address table.  A checker that reports a correct
    # document as self-contradictory costs more than the defect it is hunting.
    re.compile(r"`(" + ADDR + r")`[^\n|]{0,12}?\(\s*([\d,]+)\s*(?:B|bytes)\b", re.I),
    re.compile(r"`(" + ADDR + r")`\s*\|[^|\n]*\|\s*([\d,]+)\s*(?:B|bytes)\b", re.I),
    re.compile(r"`(" + ADDR + r")`[^\n]{0,30}?\bis\s+([\d,]+)\s*bytes\b", re.I),
]
# Names appear both inline ("`00311CF0` `BattleUnit_IssueCommand`") and, far more often, as
# the next cell of a markdown table ("| `00311CF0` | `BattleUnit_IssueCommand` | 283 B |").
# The first version of this file matched only the inline form and extracted 6 names from 45
# documents -- a checker that reports "consistent" because it sees almost nothing. Positive-
# control every zero: the counts printed at the end exist so that failure is visible.
#
# The length cap was {5,60} until 2026-09-02, which silently TRUNCATED any name longer than 61
# characters and then reported the truncation as a NAME disagreement against the full name written
# elsewhere. Fully-qualified GFZ CodeDomain names routinely exceed that -- e.g.
# Phyre.PPhysics.Bullet.RigidBodyCompoundShapeAndBtRigidBodyMaterialization (73) -- so the checker
# was manufacturing disagreements out of its own reading, and NAME-EQUIVALENCES.tsv could not
# suppress them because the truncated string it wanted appears in no document. Raised to 120.
# The character class still excludes space, '-' and '|', so a longer cap cannot swallow trailing text.
# `[ \t]*` NOT `\s*`: `\s` matches newlines, so a table whose last row ends `| `ADDR` |` would pair
# that address with the first backticked identifier of the FOLLOWING PARAGRAPH, across a blank line.
# Reported by a parallel session 2026-09-02 after it fired on their own document; any table
# immediately followed by a paragraph starting with a code span does it.
NAME_PATTERNS = [
    re.compile(r"`(" + ADDR + r")`[ \t]*\|[ \t]*`?([A-Za-z_][A-Za-z0-9_:.]{5,120})`?"),
    re.compile(r"`(" + ADDR + r")`[ \t]+`([A-Za-z_][A-Za-z0-9_:.]{5,120})`"),
]

# THE CELL AFTER AN ADDRESS IS NOT ALWAYS A NAME, AND THE TABLE USUALLY SAYS SO.
#
# All three NAME disagreements standing on 2026-09-14 were this, and all three documents were right:
#
#   vtable-method-index.md   | address | class | slot | ...     -> `eastl::allocator_memory_log`
#                            is the OWNING CLASS, and the same column holds btSphereShape,
#                            OrderedObject, MapRenderObject
#   eastl-...-allocator.md   | slot | body | what it does |     -> `_aligned_malloc(...) tail call`
#                            describes BEHAVIOUR; the header says so in words
#   where-the-games-...md    | `001EDF10` | allocator_memory_log::allocate | 100 B | ...
#                            -> the actual name, and the only one of the three claiming to be one
#
# A function can be named `allocator_memory_log::allocate`, owned by class
# `eastl::allocator_memory_log`, and tail-call `_aligned_malloc`, all at once. Reading three columns
# as three names manufactured a contradiction out of three true statements.
#
# A DENYLIST, not an allowlist: skipping only headers that clearly mean something else keeps every
# unlabelled or oddly-labelled name column in scope. Losing real coverage to avoid a false positive
# would be the worse trade - this file's own history records a first version that saw almost
# nothing and called it consistency.
#
# THE EFFECT IS LARGE AND IT IS ONE TABLE. Stated names fall 5,565 -> 3,779, and the drop was
# measured by header before it was accepted: `class` 1,787, `role` 99, `callee` 6, `what it does` 4,
# `owner` 3, `evidence` 2. The 1,787 are almost all `vtable-method-index.md`, a generated table
# shaped `| address | class | slot | address | class | slot |` - it was feeding 1,787 CLASS names
# into a FUNCTION-name comparison. 88 of those addresses still contribute a real name from some
# other document, so the coverage that mattered is retained. 2026-09-14, OPUS.
NOT_A_NAME_COLUMN = re.compile(
    r"^\s*\**\s*(class|owner|owning class|what it does|does|behaviour|behavior|role|purpose|"
    r"calls|callee|call|note|notes|evidence|meaning|why|reason|kind|type|size|bytes|slot|"
    r"disposition|verdict|status)\s*\**\s*$", re.I)


def column_says_not_a_name(text, addr_pos, name_pos):
    """True when the matched cell sits under a header that means something other than a name.

    Walks back from the row to the nearest `|---|` separator and reads the header line above it,
    then counts pipes to find which column the NAME landed in. Returns False whenever anything is
    unclear - no table, no header, ragged columns - so the only effect is to drop cells the
    document itself labels as class/behaviour/etc.
    """
    line_start = text.rfind("\n", 0, addr_pos) + 1
    line_end = text.find("\n", name_pos)
    if line_end < 0:
        line_end = len(text)
    row = text[line_start:line_end]
    if not row.lstrip().startswith("|"):
        return False
    # which column does the name sit in?
    col = row.count("|", 0, name_pos - line_start) - 1
    if col < 0:
        return False
    # nearest separator above, then the header line above that
    head = text[:line_start].rstrip("\n").split("\n")
    sep = None
    for i in range(len(head) - 1, max(-1, len(head) - 400), -1):
        s = head[i].strip()
        if s.startswith("|") and set(s) <= set("|-: \t"):
            sep = i
            break
        if not s.startswith("|"):
            break
    if sep is None or sep == 0:
        return False
    cells = [c.strip() for c in head[sep - 1].strip().strip("|").split("|")]
    if col >= len(cells):
        return False
    return bool(NOT_A_NAME_COLUMN.match(cells[col]))

# A "Superseded readings" section is a MANDATORY permanent record: EVIDENCE-STANDARD.md requires a
# corrected name to be kept, never silently rewritten.  A name-per-address checker and that rule are
# in direct conflict -- without this, the checker punishes exactly the discipline the standard
# demands, and the only way to satisfy it would be to delete the trail.  So drop those sections
# before extracting names.  Raised by a parallel session, 2026-09-02.
SUPERSEDED_SECTION = re.compile(
    r"\*\*Superseded readings?\b.*?(?=\n#{1,6}\s|\n\*\*[A-Z]|\Z)", re.S | re.I)
# A caller count is only comparable to another count of THE SAME KIND.  "6 direct callers"
# and "21 callers in total" are both true of 00303EC0 -- 6 call it directly and 15 more reach
# it through a jump thunk -- and an earlier version of this checker reported them as a
# disagreement.  The qualifier is therefore part of the key, so direct/total/distinct counts
# are compared only against their own kind.
COUNT_PATTERNS = [
    # A NUMBER MUST BEGIN WITH A DIGIT. `[\d,]+` accepted a lone comma, so
    # "`0071D170` (2,140 B, caller `0071CD10`)" extracted n="," and num("") raised
    # ValueError - the gate CRASHED for every agent on correct prose rather than
    # reporting anything (FABLE, 2026-09-17, on MT-1 text that was reworded to avoid it).
    re.compile(r"`(?P<addr>" + ADDR + r")`[^\n]{0,80}?\b(?P<n>\d[\d,]*)\s+"
               r"(?P<q>distinct|direct|indirect|total)?\s*callers?\b", re.I),
    # The gap excludes backticks so this cannot step OVER a nearer quoted address to reach a
    # further one.  "`00377C20` with 65 callers and `00313F60` with 47" previously extracted
    # 00313F60 = 65, because the backward search found the nearer address first.  Reported by a
    # parallel session, 2026-09-02.
    re.compile(r"\b(?P<n>\d[\d,]*)\s+(?P<q>distinct|direct|indirect|total)?\s*callers?\b"
               r"[^\n`]{0,40}?`(?P<addr>" + ADDR + r")`", re.I),
]

# A count inside a RETRACTION is not a live claim.  The evidence standard *requires* a correction
# to quote what the row used to say -- "this row originally read `00377C20` ... with 47 callers" --
# which puts the retracted pairing back on the page, where COUNT_PATTERNS matched it and reported a
# disagreement against the corrected figure.  So every properly-written correction of a count tripped
# the checker the correction exists to satisfy.  Reported by a parallel session, 2026-09-02.
RETRACTED_NEARBY = re.compile(
    r"(?:originally read|previously (?:read|said|stated|reported)|used to (?:say|read)|"
    r"this row (?:said|read)|was wrong|incorrectly|superseded|retracted|corrected from|"
    r"~~)", re.I)

CORRECTION = re.compile(
    r"(?:\*\*)?(?:Corrected|Retracted|Superseded|That (?:was|is) wrong)(?:\*\*)?", re.I)
QUOTED = re.compile(r"[*_\"“]{1,2}([^*_\"”\n]{25,160})[*_\"”]{1,2}")


def docs(db):
    out = []
    for root, _dirs, files in os.walk(db):
        top = os.path.relpath(root, db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for f in sorted(files):
            if f.endswith(".md") and f != "README.md":
                out.append(os.path.join(root, f))
    return out


def frontmatter_audit_gaps(text):
    """A document that records an audit pass must record WHEN.

    Added 2026-09-02 after 22 documents -- nearly half the database -- were found carrying
    `passes: 1` with `last_pass: null`.  The cause was a patch idiom that bumped the counter
    and nothing else, repeated all session.  Nothing else could see it: the count was right,
    the prose was right, and only the timestamp was missing, so provenance said "audited" with
    no date to check it against.
    """
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    if end < 0:
        return []
    fm = text[3:end]
    m = re.search(r"^audit:\s*$", fm, re.M)
    if not m:
        return []
    blk = fm[m.end():]
    pm = re.search(r"^\s+passes:\s*(\d+)", blk, re.M)
    if not pm or int(pm.group(1)) == 0:
        return []
    # A MISSING key is worse than an explicitly null one, and the original version could not see it:
    # `if k and ...` reported nothing when the key was absent entirely.  Found 2026-09-02 on
    # phyre-script-object-accessors.md, which claimed `passes: 1` while the owed table listed it as
    # never attacked -- one of the two was wrong and NEITHER WAS CHECKABLE FROM THE OTHER, because
    # the three state fields simply were not there.  So `audit_coverage` counts the CLAIM of a pass,
    # not a recorded one, and the reported percentage is an upper bound.
    out = []
    for key in ("last_pass", "last_pass_state"):
        k = re.search(r"^\s+" + key + r":\s*(\S+)", blk, re.M)
        if k is None:
            out.append(key + " (absent)")
        elif k.group(1) == "null":
            out.append(key)
    return out


def frontmatter_dupes(text):
    """Top-level keys declared twice in one YAML frontmatter block.

    Added 2026-09-02 after `capability-inhibition-policy.md` was found carrying two
    `audit:` blocks -- one saying `passes: 1, crossref_clean: true`, the other
    `passes: 0, crossref_clean: false`. YAML keeps the LAST, so every tool reading that
    file saw the superseded values, and the never-audited backlog silently listed a
    document that had in fact already been audited. No other check can see this: the
    file's links resolve, its addresses resolve, and its prose is self-consistent.

    Extended 2026-09-02: the original version matched TOP-LEVEL keys only, and
    `21-RNG-And-Determinism/rng-streams.md` was then found carrying `crossref_clean` and
    `reopened_count` twice INSIDE its `audit:` block -- `true`/`2` first, `false`/`3` second.
    Exactly the defect this function exists to catch, one indentation level down, and invisible
    to it. Now keyed on (indent, key) within the enclosing block, so a repeat at any depth is
    reported as `parent.key`.
    """
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    if end < 0:
        return []
    seen, dupes = {}, []
    parents = {}                       # indent -> the key that opened this block
    for line in text[3:end].splitlines():
        m = re.match(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*):", line)
        if not m:
            continue
        indent, k = len(m.group(1)), m.group(2)
        # leaving a block invalidates everything nested under it
        for d in [d for d in list(seen) if d[0] > indent]:
            del seen[d]
        for d in [d for d in list(parents) if d > indent]:
            del parents[d]
        parents[indent] = k
        label = k if indent == 0 else "%s.%s" % (parents.get(indent - 2, "?"), k)
        key = (indent, k)
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 2:
            dupes.append(label)
    return dupes


def num(s):
    """The digits of `s`, or None when there are none.

    A FLOOR, NOT THE FIX. COUNT_PATTERNS now require a leading digit, which is what stops
    the lone-comma match; this is here because a regex is one edit away from admitting
    something else, and the next time that happens this gate should report a finding it
    cannot read rather than take the whole suite down with a ValueError.
    """
    d = s.replace(",", "")
    return int(d) if d.isdigit() else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--lint", action="store_true",
                    help="also run the advisory superseded-text lint")
    a = ap.parse_args(argv)

    sizes = collections.defaultdict(set)
    names = collections.defaultdict(set)
    counts = collections.defaultdict(set)
    lint_hits = []
    fm_dupes = []
    fm_gaps = []

    for p in docs(a.db):
        rel = os.path.relpath(p, a.db)
        t = io.open(p, encoding="utf-8", errors="replace").read()
        for k in frontmatter_dupes(t):
            fm_dupes.append((rel, k))
        for k in frontmatter_audit_gaps(t):
            fm_gaps.append((rel, k))
        # strip fenced code so example listings do not masquerade as assertions
        prose = re.sub(r"```.*?```", "", t, flags=re.S)
        # ...and strip the mandatory correction trail, which by design names one address twice
        prose = SUPERSEDED_SECTION.sub("", prose)
        # ...and strip RANGE ROWS, which state one span and several names.
        #
        # `| 4-7 | 01F2CE88...01F2CED0 | ShaderParameterF4, F3, F2, F1 | 4, 3, 2, 1 |` is correct and
        # unambiguous to a reader: four addresses, four names, in order.  A pairwise matcher takes
        # the END address with the FIRST name and reports a self-contradiction inside one file.
        #
        # **Two sessions have now spent time re-flagging this, and both were right to.** The row is
        # right, the checker cannot read it, and a limitation recorded in the log but not in the tool
        # is a limitation that gets rediscovered. **A known false positive left in place is not free:
        # it is the noise a real finding hides in** -- the same rule that cost a document seven real
        # BODY DRIFT findings behind two permanently-red gates.
        prose = re.sub(r"^\|[^|\n]*\|[^|\n]*`?0[0-9A-Fa-f]{7}`?\s*(?:\.{2,}|…|--|–|—)"
                       r"\s*`?0[0-9A-Fa-f]{7}`?[^\n]*$", "", prose, flags=re.M)

        for pat in SIZE_PATTERNS:
            for m in pat.finditer(prose):
                # num() is None when the group held no digits; a value this gate cannot
                # read is not a claim it can compare, so it is skipped rather than binned.
                v = num(m.group(2))
                if v is not None:
                    sizes[m.group(1).upper()].add((v, rel))
        for pat in NAME_PATTERNS:
            for m in pat.finditer(prose):
                nm = m.group(2)
                # table cells that are prose, sizes or placeholders are not names
                if not re.match(r"^[A-Za-z_][A-Za-z0-9_:.]*$", nm):
                    continue
                if nm.lower().startswith(("fun_", "thunk_", "the", "and", "not", "same",
                                          "unnamed", "unowned", "reads", "writes", "sets")):
                    continue
                if "_" not in nm and not re.search(r"[a-z][A-Z]", nm):
                    continue          # require snake_case or CamelCase; drops bare words
                if column_says_not_a_name(prose, m.start(1), m.start(2)):
                    continue
                names[m.group(1).upper()].add((nm, rel))
        for pat in COUNT_PATTERNS:
            for m in pat.finditer(prose):
                # skip counts sitting inside a retraction -- see RETRACTED_NEARBY
                if RETRACTED_NEARBY.search(prose[max(0, m.start() - 240):m.start()]):
                    continue
                # AMBIGUOUS OWNER.  The backward pattern claims a count for the next address it
                # sees, but if another address appears BEFORE the number, the number probably
                # belongs to that one and this match is stealing it:
                #   "`00377C20` with 65 callers and `00313F60` with 47."  -> claimed 00313F60 = 65
                # That produced a FALSE disagreement against a third document correctly stating the
                # thunk's own 47 -- and a false disagreement is worse than a missed one, because it
                # costs the next reader a re-derivation of something already settled.
                # Same rule check_answered_not_established.py needed: judge ambiguity over every
                # candidate in the window, not just the one the pattern happened to match.
                if pat is COUNT_PATTERNS[1]:
                    before = prose[max(0, m.start() - 120):m.start()]
                    if re.search(r"`" + ADDR + r"`", before):
                        continue
                q = (m.group("q") or "").lower()
                key = m.group("addr").upper() + ("  [%s]" % q if q else "")
                v = num(m.group("n"))
                if v is not None:
                    counts[key].add((v, rel))

        if a.lint:
            for cm in CORRECTION.finditer(prose):
                window = prose[cm.end():cm.end() + 600]
                for q in QUOTED.finditer(window):
                    phrase = q.group(1).strip()
                    if len(phrase) < 25:
                        continue
                    # does that superseded phrasing still appear outside the correction block?
                    before = prose[:cm.start()]
                    if phrase in before:
                        lint_hits.append((rel, phrase[:90]))

    bad = 0

    # declared equivalences: an address may legitimately carry a GFZ name and a database name
    eq = collections.defaultdict(set)
    eqf = os.path.join(a.db, "_index", "NAME-EQUIVALENCES.tsv")
    try:
        for line in io.open(eqf, encoding="utf-8"):
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) >= 3:
                eq[f[0].upper()].add(frozenset((f[1], f[2])))
    except OSError:
        pass

    def declared(addr, vals):
        return any(set(vals) <= set(pair) for pair in eq.get(addr, ()))

    def compatible(a_, b_):
        """Two names describe the same thing if one qualifies or extends the other.

        `Phyre::checkPhyreObject` vs `checkPhyreObject` -- namespace qualification.
        `PPFX::IPfxBaseRenderToTexture` vs `IPfxBaseRenderToTexture::Initialize` -- a class
        column beside a method column, which the PPFX tables genuinely have. Neither is a
        disagreement, and flagging them trains the reader to ignore this check.
        """
        sa, sb = a_.split("::"), b_.split("::")
        if a_ in b_ or b_ in a_:
            return True
        return bool(set(sa) & set(sb))

    def report(label, table, unit, names_mode=False):
        nonlocal bad
        rows = {}
        for k, v in table.items():
            vals = sorted({x[0] for x in v})
            if len(vals) < 2:
                continue
            if names_mode and all(compatible(x, y) for x in vals for y in vals):
                continue
            if names_mode and declared(k, vals):
                continue
            rows[k] = v
        print(f"\n{label}: {len(rows)} address(es) with disagreeing values")
        for k, v in sorted(rows.items()):
            bad += 1
            print(f"   {k}")
            for val, rel in sorted(v):
                print(f"      {val} {unit}   {rel}")

    report("SIZE disagreements", sizes, "B")
    report("NAME disagreements", names, "", names_mode=True)
    report("CALLER-COUNT disagreements", counts, "callers")

    if a.lint:
        print(f"\nSUPERSEDED-TEXT lint (advisory): {len(lint_hits)} hit(s)")
        for rel, phrase in lint_hits[:20]:
            print(f"   {rel}\n      still present elsewhere: {phrase!r}")

    print(f"\nFRONTMATTER audit gaps: {len(fm_gaps)}")
    for rel, k in fm_gaps:
        bad += 1
        print(f"   {rel}\n      passes > 0 but {k!r} is null")
    print(f"\nFRONTMATTER duplicate keys: {len(fm_dupes)}")
    for rel, k in fm_dupes:
        bad += 1
        print(f"   {rel}\n      key {k!r} declared twice -- YAML keeps the LAST block")
    print(f"\nchecked {len(docs(a.db))} documents")
    print(f"   {len(sizes)} addresses with a stated size")
    print(f"   {len(names)} addresses with a stated name")
    print(f"   {len(counts)} addresses with a stated caller count")
    if bad == 0:
        print("\nconsistent: no address is described two different ways")
        return 0
    print(f"\n{bad} disagreement(s) to resolve")
    return 1


if __name__ == "__main__":
    sys.exit(main())
