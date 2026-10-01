#!/usr/bin/env python3
"""check_caller_claims.py - re-derive every "only caller" / "N callers" claim, four ways.

What this replaces
------------------
The 2026-09-07 version was a 46-line one-off with three defects, all of which the project had
already documented *elsewhere* and none of which it had applied here:

1. **A linear byte sweep over `.text`.** `data_xref_scan.py`'s docstring warns that `.text` contains
   data and padding, so a sweep from the section start loses instruction alignment and both invents
   call sites (a `0xE8` byte inside a longer instruction or inside embedded data) and misses real
   ones. This scan disassembles **from every function entry, bounded by the recorded body size**.
2. **No EH filtering.** `edges.tsv` and the binary both contain call sites inside
   `CompilerGeneratedEH` funclet and catch-handler bodies. Those are banned as semantic evidence.
   They are now **counted separately** rather than silently included - because for a claim like
   *"called by 99 funclets"* the funclet sources are the subject, and dropping them would be as
   wrong as merging them.
3. **A hardcoded path into one session's scratch directory**, which made it unrunnable by anyone
   else. The PE is parsed here, from the authorized EXE.

It also attributes every site to its **containing function**, so "N sites" and "N functions" - which
the Yebis claim distinguishes and the old script could not - are separate numbers.

THE POPULATION: CURATED FIXTURE + CORPUS SWEEP (built 2026-09-17)
-------------------------------------------------------------------
`DEFAULT_CLAIMS` is a hand-kept list - the 18 claims this checker was written to attack, kept as
a regression fixture. OPUS-REQ-EC7-CHECK-CALLER-CLAIMS-MUST-READ-THE-CORPUS closed the gap that
list could not cover: `--db` (on by default) walks the corpus and finds caller-count claims in
prose itself, so a page written after the fixture was frozen is still checked.

Recognition is deliberately narrow so the gate stays readable. A count is only a claim when it
is **grammatically bound** to a census address by one of the corpus's own idioms:

  * "`ADDR` (75 callers)"                        - parenthesised count;
  * "`ADDR` has/sees/with N callers|call sites"  - subject-verb form;
  * "N callers|functions of|reach|call `ADDR`"   - inbound connector form;
  * "`ADDR` ... called from/by N sites"          - passive form;
  * "| direct callers | N |"                     - table row whose label cell is ONLY a
                                                   caller-count label (a cell of prose
                                                   mentioning callers next to a number is an
                                                   evidence-source count, not a claim);
  * "the/its only|sole|no caller(s) of `ADDR`"   - genitive bare quantifier;
  * "`ADDR`'s only|no caller"                    - possessive bare quantifier;
  * "N sites in M functions"                     - only with call-context on the line, since
                                                   displacement censuses use the same phrase
                                                   for data references.

A count that merely shares a line with an address is NOT a claim: "N callers apiece. Every one
calls `ADDR`" makes `ADDR` the callee of a different subject, and "naming any one caller of `X`"
quantifies an example, not a population. Scoped claims ("one caller outside this family") are
skipped - they are true of a subset and assert nothing about the total.

Every discovered claim is re-derived with EH funclet containers separated, exactly like the
fixture, and compared **in the unit it is stated in**: "call sites" against call edges,
"callers / calling functions" against distinct call-containing functions, bare "sites" and
"references" against all (call+jmp) edges, "tail jumps" against jmp edges, and "functions"
against distinct referencing functions. A count that is right in a different unit is a
CONVENTION, not a MISMATCH - "zero call sites" of a body reached only by tail jumps is TRUE.
Verdicts:

  * OK              - the stated count reproduces excl-EH in its stated unit;
  * CONVENTION      - the stated count reproduces under a different honest convention:
                      a different unit ("231 callers" meaning all referencing functions),
                      through a pure jmp thunk ("21 including the thunk"), or a raw total
                      incl. EH;
  * FUNCLET-CARRIED - a strong semantic claim (only/exactly/sole/direct/no) whose count exists
                      ONLY because funclet edges were counted, or a claim whose entire caller
                      set is funclets - THE VIOLATION THIS GATE EXISTS FOR (EC-1's defect class).
                      Any carried claim refuses the run;
  * MISMATCH        - the count reproduces under no convention - stale or wrong prose, listed
                      for review.

The verdict engine is proven live by a self-test: a synthetic strong claim on a real census
function whose entire inbound set is EH-funclet edges MUST classify FUNCLET-CARRIED.

Positive control
----------------
`--control <VA>` (default `00861EBA`, `memcpy`) must come back with a large call count. A scan that
returns zero for memcpy is broken, and every "only caller" result it produced is worthless. The run
is **refused** if the control fails.

Usage
-----
    check_caller_claims.py --exe <FFXII_TZA.exe> --funcs <functions.tsv>
    check_caller_claims.py ... --addr 0x0059A3B0 --addr 0x00307300
    check_caller_claims.py ... --claims claims.tsv        # target<TAB>claim text
"""
import argparse
import collections
import io
import os
import re
import struct
import sys

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_IMM
except ImportError:
    sys.stderr.write("check_caller_claims: capstone is required (pip install capstone)\n")
    raise SystemExit(2)

HEX8 = re.compile(r"^[0-9A-F]{8}$")

# The claims this checker was originally written to attack, kept so the historical
# falsification result stays reproducible. Extend with --addr or --claims.
DEFAULT_CLAIMS = {
    0x0059A3B0: "cluster header validator - doc says 'exactly one caller'",
    0x0059A6F0: "packed namespace reader",
    0x0059C180: "namespace byte-swap - doc says one caller (0059A6F0)",
    0x006DF480: "Yebis log wrapper - doc says 800 sites / 160 functions",
    0x00307300: "Battle_ProcessActionTarget - doc says only caller of both gain fns",
    0x002F91A0: "target MP gain - doc says one caller",
    0x002F9240: "caster MP gain - doc says one caller",
    0x002FB6C0: "MP ladder lookup",
    0x002F9400: "periodic MP recovery step",
    0x005CCD00: "Phyre stack walker",
    # The frame-to-verb chain. Its whole point is that five of six links have exactly ONE caller -
    # there is no second route to a script verb - so the counts are claims and belong here.
    0x00314020: "World_UpdateSimulationTick - the chain says 3 callers",
    0x0025D9E0: "ActorManager_RunFieldRuntimePass - the chain says exactly one caller",
    0x0025DF00: "WorldActor_UpdateRuntimeAndScriptExecutionState - exactly one caller",
    0x0025E4C0: "WorldActorScriptVM_InterpretBytecode - exactly one caller",
    0x002621D0: "VMNativeCommand_ExecuteLifecycle - exactly one caller",
    # 2026-09-13 (OPUS): two pages gave a FUNCTION count the word "sites" on the same day. Both are
    # correct numbers wearing the wrong unit - the failure EVIDENCE-STANDARD's 2026-09-12 amendment
    # names - and both are here so the pair stays reproducible.
    0x00397910: "transform-point - page said '156 call sites between them'; 82 fns / 129 sites",
    0x00398F90: "compose-matrices - the other half of that 156; 74 fns / 102 sites",
    0x002432B0: "typed-list decoder - page said 'called from 108 sites'; 108 fns / 113 sites",
}


def die(m):
    sys.stderr.write("check_caller_claims: %s\n" % m)
    raise SystemExit(2)


class PE(object):
    def __init__(self, path):
        self.d = io.open(path, "rb").read()
        d = self.d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        if d[pe:pe + 4] != b"PE\0\0":
            die("not a PE: %s" % path)
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        optsz = struct.unpack_from("<H", d, pe + 20)[0]
        self.base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
        self.secs = []
        off = pe + 24 + optsz
        for _ in range(nsec):
            nm = d[off:off + 8].rstrip(b"\0").decode("latin1")
            vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
            self.secs.append((nm, va, vs, ra, rs))
            off += 40

    def read(self, va, n):
        r = va - self.base
        for _, sva, vs, ra, rs in self.secs:
            if sva <= r < sva + max(vs, rs):
                o = ra + (r - sva)
                return self.d[o:o + n]
        return None


NUMWORD = {"one": 1, "single": 1, "a": 1, "only": 1, "sole": 1, "two": 2, "three": 3,
           "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
           "no": 0, "zero": 0, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
           "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
           "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
           "seventy": 70, "eighty": 80, "ninety": 90}
NUM = (r"(\d[\d,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
       r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
       r"(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:-(?:one|two|three|four|"
       r"five|six|seven|eight|nine))?|a single|single|only one|exactly one|only|sole|no|zero)")
# Unit vocabulary, in match order: the stated word decides which measurement the
# count is compared against. "call sites" is NOT "sites": a body reached only by
# tail jumps has zero call sites and N sites, and both statements are true.
UNIT = r"(call[ -]?sites?|callers?|calling functions|functions? that call|tail[ -]?jumps?|references?|sites?)"
A = r"(?:0x)?([0-9A-F]{8})"

# Claim shapes, each binding a count to a specific address on the same line:
#   `ADDR` (75 callers)                              -> paren form
#   `ADDR` has/sees/with N callers|call sites        -> subject-verb form
#   N callers|functions of|reach|call `ADDR`         -> inbound-connector form
#   `ADDR` ... called from/by N sites|functions      -> passive form
#   | <label with 'caller'> | N | ... `ADDR`         -> table row
#   the|its only|sole|no caller(s) of `ADDR`         -> bare quantifier, genitive
#   `ADDR`'s only/sole/no caller                     -> bare quantifier, possessive
# "of the" inside the gap marks a partitive ("four of the six sites") - the
# number counts a subset, not the address's total.
GAP_BAD = re.compile(r"(?i)[.;|]|calls?\b|called\b|jmp\b|jumps?\b|invoke[sd]?\b|tail[ -]"
                     r"|reach(?:es|ed|ing)?\b|->|\bof the\b")
# "X (N sites)" where the lead-in verb is a data access and the frame ends in
# "in `X`" counts interior access sites inside the body, not callers.
INBODY = re.compile(r"(?i)\b(?:read|written|accessed|stores?|stored|loads?|loaded|"
                    r"clears?|cleared|sets?|set|touched|mutated|modified|referred)\b")
STRIP_TAIL = re.compile(r"(?i)[`*\s]*(?:0x)?[0-9A-F]{8}[`*\s]*$")
IN_END = re.compile(r"(?i)\bin\b[\s`*]*$")

P_PAREN = re.compile(r"(?i)" + A + r"[`*\s]*\(\s*" + NUM + r"\s+" + UNIT + r"\s*\)")
P_HAS = re.compile(r"(?i)" + A + r"(.{0,60}?)\b(?:has|have|sees?|gets?|with|shows?|takes|"
                   r"receives?)\b(.{0,30}?)\b" + NUM + r"\s+(?:distinct\s+)?(?:direct\s+)?" + UNIT)
P_INBOUND = re.compile(r"(?i)\b" + NUM + r"\s+(?:distinct\s+)?(?:direct\s+)?"
                       r"(callers?|functions?|references?)\s+(of|for|reach(?:es)?|to|into|call|"
                       r"calls|invoke|hits?|enters?|targets?|drives?)\s+(?:the\s+|an?\s+|this\s+|"
                       r"that\s+|its\s+)?[*`]{0,2}(?:0x)?([0-9A-F]{8})")
P_CALLEDFROM = re.compile(r"(?i)" + A + r"(.{0,60}?)\bcalled\s+(?:from|by)\s+" + NUM +
                          r"\s+(call[ -]?sites?|sites?|functions?|callers?|references?)\b")
# table rows only count when the labelled cell is just a caller-count label -
# "| ... and their callers | 1 (graph + bodies) |" is an evidence-source count,
# not a claim about the row's subject.
P_TABLE = re.compile(r"(?i)\|\s*([^|\n]{1,60}?)\|\s*[*_`]*" + NUM + r"[*_`]*\s*\|")
CELL_LABEL = re.compile(r"(?i)^[\s`*]*(?:(?:direct|distinct|inbound|native|semantic|raw|real|"
                        r"non-EH|EH|authored|reachable|remaining|indirect)\s+)*callers?"
                        r"[\s`*]*$")
P_OF = re.compile(r"(?i)\b(the|its|only|sole|single|a single|no|exactly one|one)\s+callers?\s+of\s+"
                  r"[*`]{0,2}(?:0x)?([0-9A-F]{8})")
P_POSS = re.compile(r"(?i)" + A + r"[`*']{0,3}s?\s+(only|sole|single|exactly one|no|one)\s+callers?\b")
P_SITESFNS = re.compile(r"(?i)\b(\d[\d,]*)\s+(?:distinct\s+)?(call[ -])?sites?\s+in\s+"
                        r"(\d[\d,]*)\s+(?:distinct\s+)?functions?\b")
ANY_GUARD = re.compile(r"(?i)\b(?:any|each|every)\s+$")
# "one caller outside this family" is a scoped claim, not a total - skip it.
# "50 references into the first cluster" likewise counts only a region.
SCOPE_GUARD = re.compile(r"(?i)^[\s`*.,—–-]*(?:outside|inside|within|excluding|excluded|"
                         r"other than|apart from|non-|into\b|in (?:this|the|that|each|one)\s+"
                         r"(?:family|module|section|subsystem|row|column|list|table|set|"
                         r"namespace|group|block|run|bucket))")
# "N sites in M functions" is only a CALL claim when call-context precedes it;
# displacement scans use the same phrase for data-reference sites.
CALL_CTX = re.compile(r"(?i)\b(call|calls|called|caller|callers|invoke[sd]?|reach(?:es|ed)?|"
                      r"jmps?|tail[ -]?calls?|census)\b")

STRONG = re.compile(r"(?i)\b(only|exactly|sole|single|direct|no other|exclusively|the only|its only)\b")
ADDR8 = re.compile(r"(?i)\b(?:0x)?([0-9A-F]{8})\b")
SKIP_DIRS = ("_inbox", "node_modules")


def _num(tok):
    t = tok.lower().strip().replace(",", "")
    if t.isdigit():
        return int(t)
    if "-" in t:
        parts = [NUMWORD.get(p) for p in t.split("-")]
        if all(p is not None for p in parts):
            return sum(parts)
    return NUMWORD.get(t, None)


def _unit(word):
    """Map the stated unit word to the measurement it is compared against.

    callsite - call edges only ("call sites")
    site     - all edges ("sites", "references")
    jmp      - jmp edges only ("tail jumps")
    cfn      - distinct functions containing a call edge ("callers",
               "calling functions", "functions that call")
    fn       - distinct functions containing any edge ("functions")
    """
    w = word.lower().replace("-", " ")
    if "call site" in w:
        return "callsite"
    if "site" in w or "reference" in w:
        return "site"
    if "jump" in w:
        return "jmp"
    if "caller" in w or "call" in w:
        return "cfn"
    return "fn"


def discover_claims(db, known):
    """Walk the corpus; yield (doc, lineno, line, addr, n, unit, strong, phrase).

    A claim is only recognised when the count is grammatically bound to the
    address - the corpus's own idioms - so a count about a family, a range, or
    the callers of a different subject is never attributed to a nearby address.
    """
    out = []
    for dirpath, _dirs, files in os.walk(db):
        if any(s in dirpath.replace("\\", "/").split("/")[-1] for s in SKIP_DIRS):
            continue
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                lines = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            rel = os.path.relpath(path, db)
            for ln, line in enumerate(lines, 1):
                addrs = [(m.start(), int(m.group(1), 16))
                         for m in ADDR8.finditer(line)
                         if int(m.group(1), 16) in known]
                if not addrs:
                    continue
                known_addrs = {a for _, a in addrs}

                # withdrawn text is not a claim: positions inside ~~..~~ spans
                strike = [i for i in range(len(line) - 1)
                          if line.startswith("~~", i)]
                strike_spans = [(strike[i], strike[i + 1])
                                for i in range(0, len(strike) - 1, 2)]
                if len(strike) % 2:  # unclosed ~~ strikes to end of line
                    strike_spans.append((strike[-1], len(line)))

                def keep(addr, n, unit, phrase, pos):
                    if addr not in known_addrs:
                        return
                    if any(s <= pos < e for s, e in strike_spans):
                        return
                    out.append((rel, ln, line.strip(), addr, n, unit,
                                bool(STRONG.search(line)), phrase))

                def last_addr(gap, default):
                    """Subject is the LAST census address before the verb, not the first."""
                    inner = [int(x, 16) for x in
                             ADDR8.findall(gap)]
                    inner = [x for x in inner if x in known_addrs]
                    return inner[-1] if inner else default

                for m in P_PAREN.finditer(line):
                    n = _num(m.group(2))
                    if n is None or SCOPE_GUARD.match(line[m.end():]):
                        continue
                    # "read/written only in `X` (N sites)" counts interior
                    # access sites, not inbound callers.
                    pre = STRIP_TAIL.sub("", line[:m.start()])
                    if INBODY.search(pre) and IN_END.search(pre):
                        continue
                    keep(int(m.group(1), 16), n, _unit(m.group(3)), m.group(0), m.start(2))
                for m in P_HAS.finditer(line):
                    if GAP_BAD.search(m.group(2)) or GAP_BAD.search(m.group(3)):
                        continue
                    n = _num(m.group(4))
                    if n is None or SCOPE_GUARD.match(line[m.end():]):
                        continue
                    keep(last_addr(m.group(2), int(m.group(1), 16)), n, _unit(m.group(5)),
                         m.group(0), m.start(4))
                for m in P_INBOUND.finditer(line):
                    n = _num(m.group(1))
                    if n is None or ANY_GUARD.search(line[:m.start(1)]) \
                            or SCOPE_GUARD.match(line[m.end():]):
                        continue
                    u = _unit(m.group(2))
                    # "N functions call X" names call-source functions; "N functions
                    # reach X" is any-edge.
                    if u == "fn" and m.group(3).lower() in ("call", "calls", "invoke"):
                        u = "cfn"
                    keep(int(m.group(4), 16), n, u, m.group(0), m.start(1))
                for m in P_CALLEDFROM.finditer(line):
                    if GAP_BAD.search(m.group(2)):
                        continue
                    n = _num(m.group(3))
                    if n is None or SCOPE_GUARD.match(line[m.end():]):
                        continue
                    u = _unit(m.group(4))
                    # "called from N sites/functions" counts call sources.
                    if u == "fn":
                        u = "cfn"
                    elif u == "site":
                        u = "callsite"
                    keep(last_addr(m.group(2), int(m.group(1), 16)), n, u,
                         m.group(0), m.start(3))
                for m in P_OF.finditer(line):
                    n = _num(m.group(1))
                    if n is None or ANY_GUARD.search(line[:m.start(1)]) \
                            or SCOPE_GUARD.match(line[m.end():]):
                        continue
                    keep(int(m.group(2), 16), n, "cfn", m.group(0), m.start(1))
                for m in P_POSS.finditer(line):
                    n = _num(m.group(2))
                    if n is None or ANY_GUARD.search(line[:m.start(2)]) \
                            or SCOPE_GUARD.match(line[m.end():]):
                        continue
                    keep(int(m.group(1), 16), n, "cfn", m.group(0), m.start(2))
                for m in P_SITESFNS.finditer(line):
                    if not CALL_CTX.search(line[max(0, m.start() - 120):m.start()]):
                        continue
                    before = [a for pos, a in addrs if pos < m.start() and m.start() - pos < 90]
                    if not before:
                        continue
                    su, fu = ("callsite", "cfn") if m.group(2) else ("site", "fn")
                    keep(before[-1], int(m.group(1).replace(",", "")), su,
                         m.group(0), m.start(1))
                    keep(before[-1], int(m.group(3).replace(",", "")), fu,
                         m.group(0), m.start(3))
                if "|" in line:
                    for m in P_TABLE.finditer(line):
                        n = _num(m.group(2))
                        if n is None or not CELL_LABEL.match(m.group(1).strip()):
                            continue
                        keep(addrs[0][1], n, "cfn", m.group(0), m.start(2))
    # dedupe: several patterns can bind the same count to the same address
    seen = set()
    dedup = []
    for rec in out:
        key = (rec[0], rec[1], rec[3], rec[4], rec[5])
        if key not in seen:
            seen.add(key)
            dedup.append(rec)
    return dedup


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(8):
        if os.path.isdir(os.path.join(root, "Database", "FFXII TZA")):
            break
        root = os.path.dirname(root)

    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=os.path.join(root, "Database", "Tools", "work", "exe",
                                                  "FFXII_TZA.exe"))
    ap.add_argument("--funcs", default=os.path.join(root, "Database", "Tools", "work", "graph",
                                                    "functions.tsv"))
    ap.add_argument("--db", default=os.path.join(root, "Database", "FFXII TZA"))
    ap.add_argument("--no-db", action="store_true",
                    help="skip corpus claim discovery; run the fixture only")
    ap.add_argument("--addr", action="append", default=[])
    ap.add_argument("--claims")
    ap.add_argument("--control", default="0x00861EBA")
    ap.add_argument("--show", type=int, default=6)
    a = ap.parse_args()

    if not os.path.exists(a.exe):
        die("missing exe: %s (pass --exe)" % a.exe)
    if not os.path.exists(a.funcs):
        die("missing functions.tsv: %s (pass --funcs)" % a.funcs)

    claims = dict(DEFAULT_CLAIMS)
    # `for x in a.addr` iterated the STRING, character by character: --addr 00861EAE
    # became eight claims for 0x0, 0x0, 0x8, 0x6, 0x1, 0xE, 0xA, 0xE. Split it.
    _raw = a.addr if isinstance(a.addr, (list, tuple)) else [a.addr or ""]
    for x in [t for one in _raw for t in str(one).replace(",", " ").split() if t]:
        claims[int(x, 16)] = "(from --addr)"
    if a.claims:
        with io.open(a.claims, encoding="utf-8") as fh:
            for ln in fh:
                p = ln.rstrip("\n").split("\t")
                if len(p) >= 1 and p[0].strip():
                    claims[int(p[0], 16)] = p[1] if len(p) > 1 else ""
    control = int(a.control, 16)

    pe = PE(a.exe)
    fns = []
    eh = set()
    name = {}
    known = set()
    with io.open(a.funcs, encoding="utf-8", errors="replace") as fh:
        head = fh.readline().strip().split("\t")
        i = {n: k for k, n in enumerate(head)}
        for ln in fh:
            p = ln.rstrip("\n").split("\t")
            if not p or not HEX8.match(p[0]):
                continue
            va = int(p[0], 16)
            sz = int(p[i["body_bytes"]]) if i.get("body_bytes", 99) < len(p) else 0
            tags = p[i["tags"]] if i.get("tags", 99) < len(p) else ""
            fns.append((va, sz))
            known.add(va)
            name[va] = p[i["name"]] if i.get("name", 99) < len(p) else ""
            if "CompilerGeneratedEH" in tags:
                eh.add(va)

    corpus_claims = []
    if not a.no_db:
        if not os.path.isdir(a.db):
            die("missing db: %s (pass --db)" % a.db)
        corpus_claims = discover_claims(a.db, known)

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    call = collections.defaultdict(list)      # target -> [(site, container)]
    jmp = collections.defaultdict(list)
    src_edges = collections.defaultdict(list)  # container -> [(mnemonic, target)]
    for va, sz in fns:
        b = pe.read(va, sz)
        if not b:
            continue
        for ins in md.disasm(b, va):
            if ins.mnemonic in ("call", "jmp") and ins.operands \
                    and ins.operands[0].type == X86_OP_IMM:
                t = ins.operands[0].imm
                if t in known:
                    (call if ins.mnemonic == "call" else jmp)[t].append((ins.address, va))
                    src_edges[va].append((ins.mnemonic, t))

    # a pure thunk is a body whose only direct-immediate edge is jmp -> one target
    thunks_of = collections.defaultdict(set)   # T -> {thunk bodies}
    for f, es in src_edges.items():
        tgts = {t for _, t in es}
        if len(tgts) == 1 and all(m_ == "jmp" for m_, _ in es):
            thunks_of[next(iter(tgts))].add(f)

    ctl = len(call.get(control, ()))
    print("CONTROL %08X %s -> %d call site(s)" % (control, name.get(control, "?"), ctl))
    if ctl < 10:
        die("control returned %d call sites. A scan that cannot see calls to this target is broken; "
            "every 'only caller' result below would be worthless. Refusing." % ctl)
    print("control passes - absence and 'exactly one' results below are meaningful")
    print()

    def measure(t):
        """Return per-target caller geometry with EH containers separated."""
        c = call.get(t, [])
        j = jmp.get(t, [])
        c_eh = [x for x in c if x[1] in eh]
        j_eh = [x for x in j if x[1] in eh]
        c_ok = [x for x in c if x[1] not in eh]
        j_ok = [x for x in j if x[1] not in eh]
        # through-thunk callers: callers of pure jmp-thunks that land on t
        te = [(s, c2) for th in thunks_of.get(t, ())
              for (s, c2) in call.get(th, []) + jmp.get(th, [])]
        te_ok = [x for x in te if x[1] not in eh]
        return dict(
            c_ok=len(c_ok), j_ok=len(j_ok),
            c_all=len(c), j_all=len(j),
            cfns_ok=len({x[1] for x in c_ok}),
            cfns_all=len({x[1] for x in c}),
            sites_ok=len(c_ok) + len(j_ok),
            c_eh=len(c_eh), j_eh=len(j_eh), sites_eh=len(c_eh) + len(j_eh),
            fns_ok=len({x[1] for x in c_ok} | {x[1] for x in j_ok}),
            fns_all=len({x[1] for x in c} | {x[1] for x in j}),
            sites_all=len(c) + len(j),
            sites_thunk=len(c_ok) + len(j_ok) + len(te_ok),
            fns_thunk=len({x[1] for x in c_ok} | {x[1] for x in j_ok}
                          | {x[1] for x in te_ok}),
            j_ok_list=j_ok, eh_list=c_eh + j_eh,
        )

    print("== regression fixture (the 18 hand claims) ==")
    print("%-10s %5s %5s %5s %5s  %s"
          % ("target", "calls", "fns", "jmps", "EH", "claim under test"))
    for t in sorted(claims):
        m = measure(t)
        flags = []
        if m["j_ok"]:
            flags.append("JMP THUNK")
        if m["sites_eh"]:
            flags.append("%d EH-sourced site(s) EXCLUDED" % m["sites_eh"])
        print("%08X   %5d %5d %5d %5d  %s%s"
              % (t, m["c_ok"], m["fns_ok"], m["j_ok"], m["sites_eh"], claims[t],
                 ("   <-- " + "; ".join(flags)) if flags else ""))
        for site, cont in m["j_ok_list"][:a.show]:
            print("             jmp  from %08X in %08X %s" % (site, cont, name.get(cont, "")))
        for site, cont in m["eh_list"][:a.show]:
            print("             EH   from %08X in %08X %s  (banned as semantic evidence)"
                  % (site, cont, name.get(cont, "")))

    # The stated unit decides the primary (excl-EH) measure; matches against a
    # DIFFERENT unit's measure are honest conventions, not mismatches.
    PRIMARY = {"callsite": "c_ok", "site": "sites_ok", "jmp": "j_ok",
               "cfn": "cfns_ok", "fn": "fns_ok"}
    INCL = {"callsite": "c_all", "site": "sites_all", "jmp": "j_all",
            "cfn": "cfns_all", "fn": "fns_all"}
    ALT = {"callsite": ("sites_ok", "sites_thunk", "j_ok", "cfns_ok"),
           "site": ("c_ok", "sites_thunk", "j_ok", "cfns_ok", "fns_ok"),
           "jmp": ("sites_ok", "sites_thunk", "c_ok"),
           "cfn": ("fns_ok", "fns_thunk", "c_ok", "sites_ok"),
           "fn": ("cfns_ok", "fns_thunk", "sites_ok")}

    def classify(n, unit, m, strong):
        """Verdict for stated n against measured geometry m, in the stated unit.

        ok         - stated == EH-excluded count IN ITS UNIT
        convention - stated == a different unit's count, the through-thunk
                     count, or the incl-EH total of its own unit
        carried    - the stated count exists only via EH-funclet edges
        mismatch   - stated matches no supported convention
        """
        excl, incl = m[PRIMARY[unit]], m[INCL[unit]]
        all_funclet = incl > 0 and excl == 0
        if n == excl:
            return "ok", excl, incl
        if any(n == m[k] for k in ALT[unit]):
            return "convention", excl, incl
        if n == incl:
            return ("carried" if (strong or all_funclet) else "convention"), excl, incl
        if all_funclet and strong:
            return "carried", excl, incl
        return "mismatch", excl, incl

    if not a.no_db:
        print()
        print("== corpus claims (%d recognised) ==" % len(corpus_claims))
        carried, mismatched, conventional, ok = [], [], [], 0
        for rel, ln, line, t, n, unit, strong, phrase in corpus_claims:
            m = measure(t)
            verdict, excl, incl = classify(n, unit, m, strong)
            rec = (rel, ln, t, n, unit, excl, incl, m["sites_eh"], strong, phrase, line)
            if verdict == "ok":
                ok += 1
            elif verdict == "convention":
                conventional.append(rec)
            elif verdict == "carried":
                carried.append(rec)
            else:
                mismatched.append(rec)

        # detector self-test: a claim matching only the incl-EH total of a
        # funclet-only-reached target MUST classify 'carried'. If no such
        # target exists in the census the detector cannot be proven live.
        probe = next((t for t in sorted(known)
                      if measure(t)["sites_ok"] == 0 and measure(t)["sites_thunk"] == 0
                      and measure(t)["sites_eh"] > 0),
                     None)
        if probe is not None:
            pm = measure(probe)
            v, _, _ = classify(pm["sites_all"], "site", pm, True)
            print("FUNCLET-CARRIED detector self-test: %08X (0 excl-EH / %d EH sites) "
                  "-> %s" % (probe, pm["sites_eh"], v.upper()))
            if v != "carried":
                die("self-test failed: a funclet-only claim did not classify as carried; "
                    "the EH-exclusion gate is dead")
        else:
            print("FUNCLET-CARRIED detector self-test: no funclet-only target exists; "
                  "detector unproven")
        print("OK %d   convention %d   MISMATCH %d   FUNCLET-CARRIED %d"
              % (ok, len(conventional), len(mismatched), len(carried)))
        print()
        for tag, rows in (("FUNCLET-CARRIED", carried), ("MISMATCH", mismatched),
                          ("convention", conventional)):
            for rel, ln, t, n, unit, excl, incl, neh, strong, phrase, line in rows:
                print("%-15s %s:%d" % (tag, rel, ln))
                print("    claim: %r -> target %08X, stated %d %s(s)%s"
                      % (phrase, t, n, unit, " [strong]" if strong else ""))
                print("    measured: %d excl-EH / %d incl-EH (%d EH-sourced site(s))"
                      % (excl, incl, neh))
                print("    line: %s" % line[:160])
        if carried:
            print()
            print("REFUSING: %d claim(s) are carried by EH-funclet edges - the asserted callers"
                  " exist only inside CompilerGeneratedEH bodies, which are banned as semantic"
                  " evidence." % len(carried))
            return 1
    print()
    print("Counts EXCLUDE call sites inside CompilerGeneratedEH funclet and catch-handler bodies; "
          "they are reported in the EH column instead. 'fns' counts distinct containing functions, "
          "which is not 'calls' when one function calls a target more than once.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
