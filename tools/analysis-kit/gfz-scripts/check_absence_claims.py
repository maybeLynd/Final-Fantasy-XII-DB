#!/usr/bin/env python3
"""check_absence_claims.py - test every "nothing references this" claim against five instruments.

Why this gate exists
--------------------
The contradiction ledger measured which mistakes this database actually makes
(`_index/CONTRADICTION-LEDGER.md`). Two of the four most frequent are the same one:

    no-reader-found            3 corrections   "nothing reads this"  - all three wrong
    assumed-single-instance    3 corrections   one where there were several
    E8-only-reachability       3 corrections   "who calls this", asked with one instrument

**"I could not find one" is not "there is not one", and it accounts for 6 of 33 recorded
corrections.** The existing gates check document hygiene - links, address validity, question
consistency. **None of them checks a claim.** This one does, for the single class of claim this
database has been provably worst at.

The instruments
---------------
All are built once, in a single pass, and then answered in O(1):

    E8      direct call rel32 to the address
    E9      tail jump rel32 to the address
    jcc     a `0F 8x rel32` conditional jump to the address (added 2026-09-16, OPUS).
            FABLE refuted `no static caller of any enumerated form` for 003250F0 BY HAND
            with `002E70B0 jne 003250F0`, because E8 and E9 could not see it - the same
            encoding the claim's own sweep had omitted. A gate that shares its subject's
            blind spot cannot catch it.
    operand a RIP-relative memory operand computing the address (a `lea` that materialises it)
    qword   the address as a raw little-endian qword anywhere in a section's raw bytes

**Each instrument has produced the only correct answer at least once**, which is why a claim is
only reported clean when all of them are negative.

    imagebase (added 2026-09-15, OPUS, FABLE-REQ-OPUS-ABSENCE-GATE-IMAGE-BASE-INSTRUMENT) the
            address reached as `[image-base register + disp]`, where a `lea REG, [rip+d]` targets
            exactly 00120000 and a later operand goes through REG. **THE OTHER FOUR SHARE AN
            ASSUMPTION**: each looks for the TARGET ADDRESS somewhere - as a rel32, a RIP operand, a
            stored pointer, an immediate. This idiom never materialises one, so four instruments
            were, for these 946 addresses, one instrument. FABLE published a five-instrument absence
            claim that failed exactly here and retracted it within the hour (f2e6ae19): 002AF960
            does `lea rdi,[rip-0x18FB73]` = 00120000 then `call qword ptr [rdi + r9*8 + 0x7F64D0]`,
            and 00120000+7F64D0 = 009164D0, which no other instrument sees. It refutes REFERENCE
            claims and deliberately not CALL claims - see the note beside REFUTES.
            **Blind spot, stated:** the address recorded is `base + disp`, the start of whatever the
            instruction indexes; an element reached at a run-time index is not distinguished from
            element 0. So a positive means "this table is reached", not "this element is".

    name    (added 2026-09-15, OPUS, FABLE-REQ-OPUS-ABSENCE-GATE-NAME-INSTRUMENT) a claim that an
            authored NAME has no reader, or no string in the image, tested against every name the
            image COMPOSES at run time. Two wrong claims in two days came from comparing authored
            names against string literals: UQ-339's `PresetDof N` bank (001C3D50 copies "PresetDof "
            and appends the index) and W-9's `mCascadePartitionN_M` columns (001C7940 formats
            "mCascadePartition%d_%d"). The sources are DERIVED from the image, not typed in: every
            NUL-delimited string in a data section that (a) is an identifier-shaped printf template
            or (b) is an identifier-shaped prefix ending in a space or underscore, AND is materialised
            by a RIP-relative operand inside a listed body. A name a template expands to, or a prefix
            begins, is a candidate: the composing code has to be read before the claim can stand.
            **Blind spot, stated:** a name assembled from two runtime strings, built by table lookup,
            or composed by a body the function list does not contain matches neither source. A
            negative from this instrument is a filter result, not evidence of absence. It is also LINE-scoped,
            like the address instruments: a claim whose phrase and name sit on different lines is missed.

What this tool does NOT do
--------------------------
It does not adjudicate. A line saying *"`0023B330` has zero callers"* is matched to the addresses on
that line by proximity, and **proximity is a heuristic**: the address nearest the phrase may not be
its subject. Every hit is a **candidate for a human to read**, and the output says so. The value is
that the population is 359 phrasings across 94 documents and nobody can read them all by eye.
"""
import argparse
import collections
import io
import os
import re
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
DB = os.path.join(ROOT, "Database", "FFXII TZA")
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

# A phrase names WHICH instrument it is a claim about, and only that instrument can refute it.
#
# This was the tool's own first mistake. "`0081D790` has zero callers" is a claim about CALLS.
# A `lea` that materialises the address does not contradict it - a function with no caller can
# perfectly well be address-taken, and the same document usually says so in the next clause.
# Reporting all four instruments against every phrase produced 55 hits of which the large
# majority were the documents agreeing with themselves.
CALL_PHRASES = ["no caller", "zero caller", "never called", "uncalled"]
REF_PHRASES = ["no reader", "nothing reads", "not referenced", "no writer", "no consumer",
               "unreferenced", "no xref",
               # REACHABILITY phrasings, added 2026-09-16 once the one-hop walk made them testable.
               # FABLE's judgement at the time was that adding these "would not have caught 6b, and
               # neither would both together", and that was RIGHT while the instrument recorded only
               # the table 009164D0 and the claim was about the element 002AAE40. The walk changed
               # that premise, so the conclusion changed with it: with the walk in place, this list
               # makes the gate fire on the-text-element-dispatch-table.md:169 for 002AAE40, the
               # exact sentence the retraction was about, and on 002AA800 in
               # numeric-formatting-and-character-mapping.md at two lines.
               "unreachable", "cannot be reached", "nothing indexes", "no dispatcher"]
PHRASES = CALL_PHRASES + REF_PHRASES
PHRASE_RE = re.compile("|".join(re.escape(p) for p in PHRASES), re.I)

# A REFERENCE CLAIM WEARING EMPHASIS IS STILL A REFERENCE CLAIM, and on 2026-09-16 one walked
# straight past this gate. OPUS published "`002B7B80` has no **admissible** static reference at
# all"; it is false - 002B6427 materialises the address into r8 and passes it as the Win64 third
# argument to 00245000 - and the `operand` instrument here refutes exactly that shape. The gate
# never saw the sentence, because every entry above is a LITERAL and the markdown emphasis sits
# between "no" and the noun. A first fix added "no static reference" as a literal and was thrown
# away for failing this same sentence.
# The pattern carries a CANONICAL phrase so REFUTES and the CALL/REFERENCE split keep keying on
# a phrase they know rather than on whatever text matched. Only the reference noun is patterned:
# the same hole exists in principle for "no caller", and widening every phrase at once would
# move counts nobody has measured.
# THE SECOND SENSE OF THE WORD. "no reference implementation", "reference manual",
# "reference point" are not absence claims, and one of them matched on the first control run.
# Guarded by name rather than by hoping no document says it.
OTHER_SENSE = r"(?![\s*_`]+(?:implementation|manual|point|frame|counting|count|design))"
_GAP = r"(?:[\s*_`]+[A-Za-z]+){0,3}[\s*_`]+"
PATTERN_PHRASES = [
    (re.compile(r"\bno" + _GAP + r"references?\b" + OTHER_SENSE, re.I), "not referenced"),
    # The CALL side had the identical hole, and it hid the sentence FABLE refuted by hand on
    # 2026-09-16: "003250F0 has no static caller of any enumerated form" - 003250F0 IS
    # reached, by a 0F 8x rel32 conditional from 002E70A0. Two escapes in one day, one caught
    # by a person and one by accident, is why this is here after I wrote that widening the
    # call side was a change nobody had asked for.
    (re.compile(r"\bno" + _GAP + r"callers?\b", re.I), "no caller"),
]
# Two shapes below are the DOCUMENT AGREEING WITH THE GATE rather than an absence claim.
# NEGATED_RE catches "... NOT unreferenced", which asserts the presence this gate looks for.
# BOUNDED_RE catches "no writer BUT the reset", which already names its own exception - so the
# instrument's positive IS that exception. Measured over this tool's own 67 positives on
# 2026-09-13 (OPUS): two of each. Neither is a relaxation. An unqualified claim still fails,
# and a bounded claim is not adjudicated here - it is recognised as one this gate cannot
# settle mechanically, because whether the exception is the RIGHT one needs a reader.
NEGATED_RE = re.compile(r"\bnot\b[\s*_`]*$", re.I)
BOUNDED_RE = re.compile(r"^[\s*_`]*\b(but|except|other than|apart from|besides|aside from)\b",
                        re.I)
REFUTES = {}
for _p in CALL_PHRASES:
    REFUTES[_p] = ("E8", "E9", "jcc")
for _p in REF_PHRASES:
    # `imagebase` joins the REFERENCE instruments and deliberately NOT the call ones. An address
    # reached as `[imagebase + disp]` is read or written, so it refutes "nothing reads this". Whether
    # a function CALLED through such a table has "zero callers" is the same question this file
    # already answers conservatively for address-taking - a direct-call claim is about E8/E9 - and
    # widening that is a design change nobody has asked for. Flagged to FABLE rather than assumed.
    REFUTES[_p] = ("operand", "qword", "imagebase")
ADDR_RE = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})`")

# ---- the name instrument -------------------------------------------------------------------------
# Claims about a NAME are phrased differently from claims about an address: "no string anywhere in
# the image", "nothing reads it", "authored but never read". The subject is a backticked token that is
# NOT an address.
# "no string" and "no literal" ARE NOT NAME CLAIMS and were removed 2026-09-16 (FABLE's finding).
# A composed name has no literal in the image BY CONSTRUCTION - that is this instrument's PREMISE,
# not a claim it can refute - so including them made the gate fire on its own reasoning. It read
# "46 keys are shipped with NO LITERAL string in the image, and that does not make all of them
# UNREAD" as an absence claim, when the sentence asserts the opposite. Removing these two clears
# W-9 and UQ-339 without a word of either page being changed, which is the right way round: a page
# should not have to be phrased around an instrument's blind spot.
NAME_PHRASES = ["nothing reads", "nothing in the shipped image reads", "never read", "unread",
                "no reader"]
NAME_PHRASE_RE = re.compile("|".join(re.escape(p) for p in NAME_PHRASES), re.I)
# ... and the remaining phrases can still be negated at a distance: "does not make all of them
# unread" is 25 characters of negation away, where the address-side NEGATED_RE only looks for a
# `not` immediately before. This window is wider and the self-test asserts BOTH directions, because
# a guard that suppresses the unnegated form would be worse than no guard.
NAME_NEGATED_RE = re.compile(r"\b(?:not|never|nor|n't|hardly)\b[^.;]{0,48}$", re.I)
NAME_TOKEN_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*(?: [0-9A-Za-z_]+)?)`")
# `%s` belongs here with [dux]: `luaopen_%s` at 01CCCA80 is a composed NAME, which is the whole
# subject of this instrument, and it was the one conversion the filter could not see (FABLE,
# 2026-09-15, reconciling 24+14 against 20+15 over the same materialisation test).
TEMPLATE_RE = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9_.\-]*(?:%0?\d*[duxs][A-Za-z0-9_.\-]*)+$")
# A LEADING UNDERSCORE is ordinary in an authored marker - `__naiyo__` at 00D12428, `_pic_` at
# 008F6774 - and requiring ^[A-Za-z] silently dropped them. A name a prefix filter cannot compose is
# an absence claim that passes unchallenged, which is exactly what this instrument exists to catch.
PREFIX_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{1,40}[ _]$")


def strings_in_data(d, base, secs):
    """(va, text) for every NUL-delimited printable run of 3..80 bytes in a data section."""
    out = []
    for nm, sva, vs, ra, rs in secs:
        if nm not in (".rdata", ".data", "_RDATA", ".rodata"):
            continue
        blob = d[ra:ra + rs]
        for m in re.finditer(rb"(?<=\x00)[\x20-\x7e]{3,80}(?=\x00)", blob):
            out.append((base + sva + m.start(), m.group(0).decode("ascii")))
    return out


def build_name_sources(d, base, secs, operand):
    """Templates and prefixes the code materialises -> (list of (regex, text, va), list of (prefix, va))."""
    templates, prefixes = [], []
    for va, s in strings_in_data(d, base, secs):
        if va not in operand:
            continue
        if TEMPLATE_RE.match(s):
            # A TEMPLATE MUST KEEP SOME LITERAL TEXT. `%s%s` and `%s%d` expand to "any name at all",
            # so they would report every claim as composable and the instrument would assert nothing.
            # Admitting %s to TEMPLATE_RE without this test produced 27 new templates of which 12 were
            # pure conversions (OPUS, 2026-09-15). The residue is what is left after the conversions
            # are removed; one character is enough - `.%s` is a real extension shape - but zero is not.
            if not re.sub(r"%0?\d*[duxs]", "", s):
                continue
            pat = re.escape(s)
            pat = re.sub(r"%0(\d+)[dux]", lambda m: r"\d{%s}" % m.group(1), pat)
            pat = re.sub(r"%\d*[dux]", r"\\d+", pat)
            # `%s` had no substitution at all, so every %s template compiled to a pattern matching
            # only its own literal text and could never fire. Reported as a source, inert in practice.
            pat = re.sub(r"%s", r".+", pat)
            templates.append((re.compile("^" + pat + "$"), s, va))
        elif PREFIX_RE.match(s):
            prefixes.append((s, va))
    return templates, prefixes


def name_composed_by(name, templates, prefixes):
    hits = ["template %r @%08X" % (s, va) for rx, s, va in templates if rx.match(name)]
    hits += ["prefix %r @%08X" % (p, va) for p, va in prefixes
             if name.startswith(p) and len(name) > len(p)]
    return hits


def load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        nm = d[off:off + 8].rstrip(b"\0").decode("latin1")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((nm, va, vs, ra, rs))
        off += 40
    return d, base, secs


def _text_bounds(base, secs):
    for nm, sva, vs, ra, rs in secs:
        if nm == ".text":
            return base + sva, base + sva + max(vs, rs)
    return 0, 0


def _va_to_off(base, secs, va):
    for nm, sva, vs, ra, rs in secs:
        lo = base + sva
        if lo <= va < lo + max(vs, rs):
            o = ra + (va - lo)
            return o if o < len(_va_to_off.data) else None
    return None


def walk_qword_table(d, base, secs, table_va, cap=4096):
    """Qwords upward from table_va that land in .text, stopping at the first value that is neither
    null nor a .text address. The table's own boundary terminates it, so no length is guessed."""
    _va_to_off.data = d
    lo, hi = _text_bounds(base, secs)
    out = []
    off = _va_to_off(base, secs, table_va)
    if off is None:
        return out
    for k in range(cap):
        p = off + k * 8
        if p + 8 > len(d):
            break
        v = struct.unpack_from("<Q", d, p)[0]
        if v == 0:
            continue
        if lo <= v < hi:
            out.append(v)
            continue
        break
    return out


def build_instruments(d, base, secs, funcs, verbose=True):
    """One pass over the image; six sets out."""
    e8, e9, jcc, operand, qword, imagebase = (set(), set(), set(), set(), set(), set())

    for nm, sva, vs, ra, rs in secs:
        blob = d[ra:ra + rs]
        if nm == ".text":
            for i in range(len(blob) - 5):
                op = blob[i]
                if op == 0xE8 or op == 0xE9:
                    rel = struct.unpack_from("<i", blob, i + 1)[0]
                    (e8 if op == 0xE8 else e9).add(base + sva + i + 5 + rel)
                # 0F 80..8F rel32 - the near conditional forms. Six bytes, so the loop
                # bound below is one short for these; guarded here rather than widened
                # for every opcode.
                elif op == 0x0F and i + 6 <= len(blob) and 0x80 <= blob[i + 1] <= 0x8F:
                    rel = struct.unpack_from("<i", blob, i + 2)[0]
                    jcc.add(base + sva + i + 6 + rel)
        # The raw-qword instrument scans DATA sections at 8-byte alignment only. A first version
        # scanned every section including `.text` at 4-byte stride and collected 98,285 addresses -
        # any eight consecutive bytes that happen to form a plausible VA. It produced 19 of 55 hits
        # and the instrument, not the claims, was what it was measuring. A pointer in this image is
        # 8-aligned and lives in data.
        if nm in (".rdata", ".data", "_RDATA", ".rodata"):
            for i in range(0, len(blob) - 8, 8):
                v = struct.unpack_from("<Q", blob, i)[0]
                if 0x00120000 <= v < 0x03100000:
                    qword.add(v)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    for entry, size in funcs:
        r = entry - base
        blob = None
        for nm, sva, vs, ra, rs in secs:
            if sva <= r < sva + max(vs, rs) and nm == ".text":
                o = r - sva
                if o < rs:
                    blob = d[ra + o: ra + o + size]
                break
        if not blob:
            continue
        # THE IMAGE-BASE IDIOM, the fifth instrument (FABLE-REQ, 2026-09-15). The other four all ask
        # "where does the TARGET ADDRESS appear" - as a rel32, a RIP operand, a stored pointer or an
        # immediate. This idiom never materialises one: a function does `lea REG, [rip+d]` targeting
        # exactly the image base 00120000, and then reaches `[REG + index*8 + disp]`, so the address
        # exists only as base plus a displacement inside an instruction that names neither.
        # FABLE published a five-instrument absence claim that was wrong for exactly this reason and
        # retracted it within the hour (f2e6ae19): 002AF960 does lea rdi,[rip-0x18FB73] = 00120000
        # then call qword ptr [rdi + r9*8 + 0x7F64D0], and 00120000+7F64D0 = 009164D0. The lesson is
        # not that an instrument was weak - it is that FIVE INSTRUMENTS SHARING ONE ASSUMPTION ARE
        # ONE. 594 functions, 1,411 accesses, 971 distinct addresses, none visible to the other four.
        holders = set()
        for i in md.disasm(blob, entry):
            if i.mnemonic == "lea" and len(i.operands) == 2:
                dst, src = i.operands
                if (src.type == X86_OP_MEM and src.value.mem.base == X86_REG_RIP
                        and i.address + i.size + src.value.mem.disp == base):
                    holders.add(dst.value.reg)
                    continue
            # a register that is written by anything else stops being the base
            if holders:
                _r, w = i.regs_access()
                holders -= set(w)
            for o in i.operands:
                if o.type == X86_OP_MEM and o.value.mem.base == X86_REG_RIP:
                    operand.add(i.address + i.size + o.value.mem.disp)
                elif (holders and o.type == X86_OP_MEM and o.value.mem.base in holders
                      and o.value.mem.disp):
                    # base + disp is what the instruction reaches; any index is a run-time element
                    table = base + o.value.mem.disp
                    imagebase.add(table)
                    # ONE HOP, and only when the instruction says it is a table (FABLE, 2026-09-16).
                    # `call qword ptr [rdi + r9*8 + 0x7F64D0]` is not reaching an address, it is
                    # reaching a TABLE OF QWORDS and calling one - so the elements are reachable and
                    # the first version of this instrument, which stopped at the table, could not say
                    # so. It recorded 009164D0 while the claim under test was about 002AAE40, an
                    # element inside it. The table's own boundary is the terminator, so no length is
                    # guessed: walk up from base+disp, collect values that land in .text, skip nulls,
                    # and STOP at the first value that is neither. On the control that terminates at
                    # 00916520, where 0x0000000A00000001 is not a .text address.
                    if i.mnemonic in ("call", "jmp") and o.value.mem.index:
                        for v in walk_qword_table(d, base, secs, table):
                            imagebase.add(v)
    if verbose:
        print("instrument sets built: E8 %d, E9 %d, jcc %d, operand %d, qword %d, "
              "imagebase %d"
              % (len(e8), len(e9), len(jcc), len(operand), len(qword), len(imagebase)))
    return e8, e9, jcc, operand, qword, imagebase


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--out", default=None)
    ap.add_argument("--show", type=int, default=25)
    a = ap.parse_args()

    d, base, secs = load_pe(a.exe)
    funcs = []
    f = io.open(a.funcs, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                sz = int(p[2])
                if 0 < sz <= 0x20000:
                    funcs.append((int(p[0], 16), sz))
            except ValueError:
                pass

    # CONTROLS, one per instrument, chosen because each is known positive for THAT instrument.
    # 009164D0 is the address FABLE's retraction turned on: 002AF960 reaches it as
    # [imagebase + r9*8 + 0x7F64D0] and no other instrument sees it.
    CONTROLS = {"E8": 0x001DE4F0, "E9": 0x001D1660, "operand": 0x0023B6F0, "qword": 0x005C5230,
                # 003250F0 is reached ONLY by 002E70B0 jne, which no other instrument here
                # sees - the same reason 002AAE40 and not the table is the imagebase control.
                # A control an existing instrument already finds would prove nothing.
                "jcc": 0x003250F0,
                # 002AAE40 is an ELEMENT of the table at 009164D0, not the table, and it is the
                # address the claim that motivated this instrument was actually about. Controlling
                # on the table alone would have passed while the instrument still could not answer
                # the question it was added for (FABLE, 2026-09-16).
                "imagebase": 0x002AAE40}

    e8, e9, jcc, operand, qword, imagebase = build_instruments(d, base, secs, funcs)
    sets = {"E8": e8, "E9": e9, "jcc": jcc, "operand": operand, "qword": qword,
            "imagebase": imagebase}
    print()
    print("CONTROLS - each must be positive for its own instrument, or that instrument is broken")
    ok = True
    for k, v in CONTROLS.items():
        hit = v in sets[k]
        print("  %-8s %08X  %s" % (k, v, "positive" if hit else "*** NEGATIVE - INSTRUMENT BROKEN"))
        ok = ok and hit
    # THE WALK'S OWN TERMINATION IS CONTROLLED, because a walk that runs past the table's end
    # silently manufactures reachability for whatever follows it in .rdata.
    _walk = walk_qword_table(d, base, secs, 0x009164D0)
    _want = [0x002A9F00, 0x002A9980, 0x002A8C50, 0x002AA800, 0x002AAE40]
    _walk_ok = all(v in _walk for v in _want) and len(_walk) == len(_want)
    print("  %-8s table 009164D0 -> %d entr(y/ies), terminates at 00916520  %s"
          % ("walk", len(_walk),
             "as expected" if _walk_ok else "*** WALK WRONG: %s" % [hex(v) for v in _walk[:8]]))
    ok = ok and _walk_ok
    if not ok:
        print("\nrefusing to report: a broken instrument turns every claim into a false clean")
        return 2
    print()

    claims, no_addr = [], 0
    for root, dirs, files in os.walk(a.db):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), a.db).replace("\\", "/")
            for n, line in enumerate(io.open(os.path.join(root, fn), encoding="utf-8",
                                             errors="replace").read().split("\n"), 1):
                m = PHRASE_RE.search(line)
                canon = m.group(0) if m else None
                if not m:
                    for _pat, _canon in PATTERN_PHRASES:
                        m = _pat.search(line)
                        if m:
                            canon = _canon
                            break
                if not m:
                    continue
                if NEGATED_RE.search(line[max(0, m.start() - 28):m.start()]):
                    continue
                if BOUNDED_RE.search(line[m.end():m.end() + 90]):
                    continue
                addrs = ADDR_RE.findall(line)
                if not addrs:
                    no_addr += 1
                    continue
                # proximity: the address whose position is nearest the phrase
                pos = m.start()
                best = min(ADDR_RE.finditer(line), key=lambda x: abs(x.start() - pos))
                claims.append((rel, n, canon, int(best.group(1), 16), line.strip()))

    hits = []
    for rel, n, phrase, va, line in claims:
        which = REFUTES[phrase.lower()]
        pos = [k for k in which if va in sets[k]]
        if pos:
            hits.append((rel, n, phrase, va, pos, line))

    print("absence phrasings found          : %d" % (len(claims) + no_addr))
    print("  with no address on the line    : %d  (unverifiable by this tool)" % no_addr)
    print("  address-anchored, tested       : %d" % len(claims))
    ncall = sum(1 for c in claims if c[2].lower() in CALL_PHRASES)
    print("     of those, CALL claims        : %d  (refutable by E8 / E9 / jcc)" % ncall)
    print("     of those, REFERENCE claims   : %d  (refutable only by operand / qword / imagebase)"
          % (len(claims) - ncall))
    print("  the naming instrument is NEGATIVE : %d" % (len(claims) - len(hits)))
    print("  the naming instrument is POSITIVE : %d  <- candidates for a human to read"
          % len(hits))
    print()
    c = collections.Counter(tuple(h[4]) for h in hits)
    print("  which instruments fired:")
    for k, v in c.most_common():
        print("     %-28s %4d" % ("+".join(k), v))
    print()
    for rel, n, phrase, va, pos, line in hits[:a.show]:
        print("  %s:%d  %08X  [%s]" % (rel, n, va, "+".join(pos)))
        print("     %s" % (line[:150] + ("…" if len(line) > 150 else "")))
    if len(hits) > a.show:
        print("  ... %d more" % (len(hits) - a.show))

    # ---- the name instrument ----------------------------------------------------------------------
    templates, prefixes = build_name_sources(d, base, secs, operand)
    print()
    print("NAME instrument: %d identifier-shaped templates and %d prefixes, each materialised by a "
          "RIP operand in a listed body" % (len(templates), len(prefixes)))
    NAME_CONTROLS = ["PresetDof 12", "mCascadePartition1_2"]
    name_ok = True
    for probe in NAME_CONTROLS:
        src = name_composed_by(probe, templates, prefixes)
        print("  control %-22s %s" % (probe, src[0] if src else "*** NEGATIVE - INSTRUMENT BROKEN"))
        name_ok = name_ok and bool(src)
    # THE NEGATION GUARD IS CONTROLLED BOTH WAYS. Suppressing a negated phrase is only safe if the
    # plain phrase still fires; a guard that silences both is a gate that has stopped working, and
    # it would look exactly like a clean corpus.
    _neg = "and that does not make all of them unread"
    _pos = "the key is unread"
    _nm = NAME_PHRASE_RE.search(_neg)
    _pm = NAME_PHRASE_RE.search(_pos)
    _suppressed = bool(_nm and NAME_NEGATED_RE.search(_neg[max(0, _nm.start() - 64):_nm.start()]))
    _fires = bool(_pm and not NAME_NEGATED_RE.search(_pos[max(0, _pm.start() - 64):_pm.start()]))
    print("  control negation       %s" % ("negated suppressed, plain still fires"
                                           if (_suppressed and _fires)
                                           else "*** NEGATION GUARD BROKEN (suppressed=%s fires=%s)"
                                                % (_suppressed, _fires)))
    name_ok = name_ok and _suppressed and _fires
    name_hits, name_claims = [], 0
    if not name_ok:
        print("  refusing to report name claims: a broken instrument turns every claim into a false clean")
    else:
        for root, dirs, files in os.walk(a.db):
            for fn in sorted(files):
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(root, fn), a.db).replace("\\", "/")
                for n, line in enumerate(io.open(os.path.join(root, fn), encoding="utf-8",
                                                 errors="replace").read().split("\n"), 1):
                    m = NAME_PHRASE_RE.search(line)
                    if not m or NEGATED_RE.search(line[max(0, m.start() - 28):m.start()]):
                        continue
                    if NAME_NEGATED_RE.search(line[max(0, m.start() - 64):m.start()]):
                        continue
                    for t in NAME_TOKEN_RE.finditer(line):
                        name = t.group(1)
                        if re.fullmatch(r"(?:0x)?[0-9A-Fa-f]{6,8}", name):
                            continue
                        name_claims += 1
                        src = name_composed_by(name, templates, prefixes)
                        if src:
                            name_hits.append((rel, n, m.group(0), name, src, line.strip()))
        print("  name tokens on a line carrying a name-absence phrase: %d" % name_claims)
        print("  of those, a name the image COMPOSES                  : %d  <- read the composing code"
              % len(name_hits))
        for rel, n, phrase, name, src, line in name_hits[:a.show]:
            print("  %s:%d  `%s`  [%s]" % (rel, n, name, "; ".join(src[:2])))
            print("     %s" % (line[:150] + ("…" if len(line) > 150 else "")))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("document\tline\tphrase\taddress\tinstruments_positive\tcontext\n")
            for rel, n, phrase, va, pos, line in hits:
                f.write("%s\t%d\t%s\t%08X\t%s\t%s\n"
                        % (rel, n, phrase, va, "+".join(pos), line.strip()[:300]))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
