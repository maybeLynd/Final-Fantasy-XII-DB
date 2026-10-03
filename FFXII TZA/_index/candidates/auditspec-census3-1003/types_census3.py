#!/usr/bin/env python3
"""types_census3.py - census2 with its blind spots closed (SWE2-AUDIT-SPEC, 2026-10-03,
AUDITSEM-REQ-AUDITSPEC-CENSUS2-BLINDSPOT-AND-RULES-1003 part 1; drafted by a SWE2-AUDIT-SEM helper).

WHY. census2 (`../auditspec-l2-expansion-1003/types_census2.py`, published, not edited) reported no system with an
undeclared contract-named item after the 2026-10-03 declarations. A hand sweep of the twelve PARTIAL rows
(`../auditsem-types-rescore-2-1003/README.md`) then found seven real residuals that census2 cannot see. In those
twelve rows, census2's record extractor left 165 of 175 offset-bearing lines of the ruled sections unread. This copy
reads the forms census2 misses, keeps census2's classes, its OBJECT (bare-base) rule and the ruled sections
(`contract_named_state_census.state_sections`, unchanged), and reports what it cannot attribute reliably as
UNATTRIBUTED with a kind, instead of guessing.

NEW FORMS (each has an embedded fixture control: census3 finds it, census2's extractor misses it):
  LC      record-relative state under a name census2's NAME regex cannot take - lower-case (`unit + 0x698`,
          `statsRecord + 0x194`) or all-caps (`BKEI + 0x19`). The name resolves ONLY through ALIASES3 (each entry
          carries the contract text that binds it). CPU registers are mechanism, not state, and are skipped (counted).
          Any other name -> UNATTRIBUTED kind LC-NAME. A width word with no record (`byte[+0x80]`) -> WIDTH-OFFSET.
  CONT    continuation offsets after a record name: `unit +0x00, +0x10, +0x40`, `+0xE98`/`+0xE99`.
  LAYOUT  fenced layouts whose head is not a bare CamelCase type name. The head resolves, in order, by (1) a leading
          declared type or alias, (2) a data address on the head line: a pointer-cell route at exactly that address
          (`*(char**)0x0208E690 + ...`, `[02EBF190] -> ...`), else a data span starting there, (3) exactly one declared
          type name on the line, (4) `alias + 0xNN` whose declared field is a typed pointer (`BKEI (unit + 0x6A0)`).
          Unresolved head -> its rows are UNATTRIBUTED kind LAYOUT-HEAD.
  TABLE   `| +0xNN | ...` rows: the type is the single declared type (or alias) named on the last non-blank line before
          the table. None, or more than one -> UNATTRIBUTED kind TABLE (census2's behaviour).
  SYM     globals named by symbol: `DAT_XXXXXXXX` / `uRam_XXXXXXXX` / `PTR_x_XXXXXXXX` carry their address; `g_name`
          resolves through the store first (a STATIC route of a type whose rows mention the symbol), else through the
          pages: the single data address that appears beside the symbol on a page line (flag SYM-VIA-PAGE:<page>).
          No single address -> UNATTRIBUTED kind SYMBOL.
  SLASH   slash lists `02EBF150/168/148/140`, `` `02AEE054`/`58`/`5C` ``: each suffix replaces the low digits.
  INDEX   `ADDR[n]`: element size from a width word before the address (byte/word/dword/qword), else from the declared
          array field at ADDR; neither -> UNATTRIBUTED kind INDEX-UNSIZED.
  CELL    contracts credited only in a row's L2 contract cell (unstruck text), not in important-subsystems.tsv col 6.

FLAGS beside the class (worklist, not verdicts): width-aware checks where the contract states a width -
  GAP-EXACT (a gap row of exactly the named extent: the ruled "extent only" case), GAP-COARSER (a gap row wider than
  the named item), NO-ROW (no field row at all), WIDER-THAN-FIELD (the named item is wider than the declared field,
  e.g. a 14-element array declared as 12).

LIMITS. Prose outside the ruled sections is not read (census2's ruling). State named only in words is invisible.
ALIASES3 is hand-built: a lower-case name not in it is UNATTRIBUTED, never guessed. Every finding needs a hand read.

    types_census3.py [--selftest] [--store DIR]   writes census3.tsv, census3_systems.tsv, census3_unattributed.tsv
                                                  next to this file (DIR holds _types/types.tsv and fields.tsv;
                                                  default: the worktree store)
"""
import collections
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
C2DIR = os.path.normpath(os.path.join(HERE, "..", "auditspec-l2-expansion-1003"))
sys.dont_write_bytecode = True     # importing census2 must not leave a __pycache__ in its published folder
sys.path.insert(0, KIT)
sys.path.insert(0, C2DIR)
import contract_named_state_census as OLD  # noqa: E402
import types_census2 as C2  # noqa: E402  (imported, never run or edited: its extractor is the control's "old")

STORE = DB
if "--store" in sys.argv:
    STORE = os.path.abspath(sys.argv[sys.argv.index("--store") + 1])
OLD.G.DB = STORE

REGISTERS = set("rax rbx rcx rdx rsi rdi rbp rsp rip r8 r9 r10 r11 r12 r13 r14 r15 eax ebx ecx edx esi edi ebp esp "
                "r8d r9d r10d r11d r12d r13d r14d r15d ax bx cx dx al bl cl dl xmm0 xmm1 xmm2 xmm3".split())
WIDTH_WORDS = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
# English words that precede a bare offset in prose ("the byte at +0x5A90", "+0x10 and +0x40"): the record is named
# elsewhere in the sentence, so the offset is UNATTRIBUTED kind PROSE-OFFSET (counted, never guessed).
PROSE_WORDS = set("at and of the from to with so for while when through this is into as its past writes reads read "
                  "sets resets zeroes zeroing uses whose words fields or by on in then than plus until after before "
                  "over under between each every both all any one two The Its On So Only Rows IN OR no minus "
                  "except beyond owns reaches spans tests leaves leave leaving covers computes alongside confirms "
                  "equals clears fixes dereference resolving s y x A B".split())

# Lower-case / all-caps record names -> declared type. Key (contract basename or "*", name). Each entry quotes the
# contract text that binds the name; a name not here is UNATTRIBUTED.
ALIASES3 = {
    ("*", "unit"): ("BattleUnit", "CONTRACT-battle-unit-construction.md 3: 'The receiver is BattleUnit ... Its +0x698'; "
                                  "group-completion 3: 'physical offsets on the battle unit'"),
    ("*", "statsRecord"): ("BattleStatsRecord", "CONTRACT-license-check.md 3: 'rec is the BattleStatsRecord'"),
    ("*", "stats"): ("BattleStatsRecord", "the stats record behind unit +0x698 (BattleUnit +0x698 statsRecord "
                                          "BattleStatsRecord*)"),
    ("CONTRACT-battle-unit-construction.md", "spawn"): ("SpawnRecord", "3: 'the particular SpawnRecord's embedded "
                                                                       "stats at spawn+0x80'"),
    ("CONTRACT-group-completion-and-respawn.md", "record"): ("SpawnRecord", "3: 'SpawnRecord, 0x250' / 'records: "
                                                                            "*(char**)0x0208E690 + slot * 0x250'"),
    ("CONTRACT-gambit-walk.md", "set"): ("AiOrderSet", "3: 'AiOrderSet at 0x02089378 + setIndex * 0x170'"),
    ("CONTRACT-gambit-walk.md", "record"): ("AiOrderRecord", "3: 'AiOrderRecord, 24 bytes'"),
    ("CONTRACT-enmity.md", "BKEI"): ("SpawnRecord", "3: 'BKEI (unit + 0x6A0)'; BattleUnit +0x6A0 spawnRecord SpawnRecord*"),
    ("CONTRACT-authored-table-row-lookup.md", "header"): ("AuthoredTableHeader", "3: 'AuthoredTableHeader, at least 0x20'"),
    ("CONTRACT-resource-section-addressing.md", "entry"): ("RenderResourceEntry", "3: 'ResourceEntry' = census2 alias "
                                                                                  "RenderResourceEntry"),
    ("CONTRACT-widget-object.md", "self"): ("Widget", "3: tree links 'from the broadcast walker ... [self+0x10]' on the "
                                                      "Widget header"),
    ("CONTRACT-script-to-native-bridge.md", "entry"): ("ActorWaitSlot", "3: 'The result entry is the actor's current "
                                                                        "ActorWaitSlot'"),
    ("CONTRACT-facing-and-steering.md", "actor"): ("ActorStorageRecord", "3: 'actor +0x03 packed (kind << 5) | sequence', "
                                                                         "'actor +0xB8 -> movement context' = "
                                                                         "ActorStorageRecord +0x003 / +0x0B8 contextPtr"),
    ("CONTRACT-facing-and-steering.md", "context"): ("MovementContext", "3: 'context +0x120 SteeringRecord[0]'; "
                                                                        "MovementContext is reached through "
                                                                        "ActorStorageRecord +0xB8 and holds the two "
                                                                        "SteeringRecords at +0x120/+0x1A0"),
    ("CONTRACT-battle-runtime-mode.md", "state"): ("BattleSystemState", "3: '*(void **)0x02EBF190 ... the "
                                                                        "BattleSystemState block'; 'state + 0x5B04'"),
    ("CONTRACT-character-transform-publish.md", "object"): ("CharacterRenderObject", "3: 'CharacterRenderObject (0x668) "
                                                                                     "holds the two matrix banks at "
                                                                                     "+0x4C4 and +0x584'"),
    ("CONTRACT-manager-slot-entry-tables.md", "entry"): ("ActorManagerSlotEntry", "3: 'ActorManagerSlotEntry, 0x18'"),
    ("CONTRACT-experience-and-licence-award.md", "subject"): ("BattleUnit", "3: 'subject +0x698 Stats pointer'"),
    ("CONTRACT-experience-and-licence-award.md", "recipient"): ("BattleStatsRecord", "3: 'recipient +0x3C, +0x64 Status "
                                                                                     "words' = BattleStatsRecord "
                                                                                     "statusWord2/statusWord1"),
    ("CONTRACT-status-write.md", "target"): ("BattleStatsRecord", "3: 'BattleStatsRecord ... +0x38 statusWord3 ... "
                                                                  "+0x3C statusWord2'; 5: 'target +0x38 / +0x3C / +0x64'"),
    ("CONTRACT-battle-target-buffer.md", "buffer"): ("BattleTargetBuffer", "3: 'BattleTargetBuffer, total size 0x208'"),
    ("CONTRACT-corridor-query-family.md", "agent"): ("CorridorNavAgent", "3: 'the agent (CorridorNavAgent, declared "
                                                                         "2026-09-25)'"),
    ("CONTRACT-periodic-tick.md", "result"): ("BattleResultRecord", "3: 'computed by stage 2 into the result record "
                                                                    "(result + 0xDC ...)'; BattleResultRecord +0xDC[32]"),
    ("CONTRACT-apply-result-to-target.md", "record"): ("BattleResultRecord", "5: 'record +0x2C bit19' = "
                                                                             "BattleResultRecord +0x2C flags"),
    ("CONTRACT-apply-result-to-target.md", "owner"): ("BattleUnit", "5: 'Temporary owner +0xE9A' = BattleUnit +0xE9A"),
    ("CONTRACT-weather.md", "ActorManager"): ("ActorManagerSlot", "2: '002620E0(rcx = ActorManager record)'; its "
                                                                  "+0x28 test (002620E6) is ActorManagerSlot +0x028 "
                                                                  "slotIndex and +0x10 (002620F3/002621A4) is "
                                                                  "+0x010 slotFlags"),
    ("CONTRACT-per-frame-update-gate.md", "singleton"): ("ManagerSingleton0209BE80", "group-handler section: "
                                                                                    "'ManagerSingleton0209BE80's 24 "
                                                                                    "declared UNKNOWN spans'"),
}

TICK = C2.TICK
ADDR_IN = C2.ADDR_IN
NAME = C2.NAME
REC_INLINE2 = re.compile(NAME + r"\s*`?\s*(?:\[\s*)?\+\s*`?\s*0x([0-9A-Fa-f]{1,5})\b")
ANYREC = re.compile(r"(?<![0-9A-Za-z_.])([A-Za-z_][A-Za-z0-9_]*)\s*`?\s*(?:\[\s*)?\+\s*`?\s*0x([0-9A-Fa-f]{1,5})\b")
CONT = re.compile(r"`?\]?\s*(?:,|/|\band\b|\bor\b|&)\s*`?\s*(?:\[\s*)?\+\s*`?\s*0x([0-9A-Fa-f]{1,5})\b`?")
LAYOUT_ROW = C2.LAYOUT_ROW
STRUCT_HEAD = re.compile(r"^\s*(?:typedef\s+)?struct\s+([A-Za-z_][A-Za-z0-9_]*)")
STRUCT_ROW = re.compile(r"/\*\s*\+\s*0x([0-9A-Fa-f]{1,5})\s*\*/")
ROWCELL = re.compile(r"^\|\s*([^|]*)\|")
OFFS = re.compile(r"\+\s*0x([0-9A-Fa-f]{1,5})\b")
INDEX = re.compile(r"(?<![0-9A-Za-z_])(?:0x)?(0[0-9A-Fa-f]{7})\[(0x[0-9A-Fa-f]+|\d+)\]")
SLASH = re.compile(r"(?<![0-9A-Za-z_])(?:0x)?(0[0-9A-Fa-f]{7})`?((?:\s*/\s*`?(?:0x)?[0-9A-Fa-f]{1,7}`?(?![0-9A-Za-z_]))+)")
SLASH_ITEM = re.compile(r"/\s*`?(?:0x)?([0-9A-Fa-f]{1,7})`?")
SYM_ADDR = re.compile(r"\b(?:DAT|[a-z]{0,2}Ram|PTR_\w+?)_(0[0-9A-Fa-f]{7})\b")
SYM_G = re.compile(r"(?<![0-9A-Za-z_])(g_[A-Za-z][A-Za-z0-9_]*)")
CTYPE = re.compile(r"(?<![0-9A-Za-z_])(u8|s8|i8|int8|uint8|char|byte|u16|s16|i16|int16|uint16|word|u32|s32|i32|int32|"
                   r"uint32|dword|float|f32|u64|s64|i64|int64|uint64|qword|double|f64|ptr|pointer|void\*+|"
                   r"[A-Z][A-Za-z0-9_]*\*?)(?:_t)?(?:\s*\[\s*(\d+|0x[0-9A-Fa-f]+)\s*\])?")
CSIZE = {"u8": 1, "s8": 1, "i8": 1, "int8": 1, "uint8": 1, "char": 1, "byte": 1, "u16": 2, "s16": 2, "i16": 2,
         "int16": 2, "uint16": 2, "word": 2, "u32": 4, "s32": 4, "i32": 4, "int32": 4, "uint32": 4, "dword": 4,
         "float": 4, "f32": 4, "u64": 8, "s64": 8, "i64": 8, "int64": 8, "uint64": 8, "qword": 8, "double": 8,
         "f64": 8, "ptr": 8, "pointer": 8}
STRUCK = re.compile(r"~~.*?~~", re.S)
CONTRACT_REF = re.compile(r"((?:[0-9A-Za-z_.\-]+/)*CONTRACT-[A-Za-z0-9_\-]+\.md)")


# ----------------------------------------------------------------------------------------------- store helpers
class Store:
    def __init__(self):
        self.names, self.meaning = C2.load_types() if STORE == DB else self._load_types()
        self.spans, self.fields, self.sizes = OLD.load_store()
        self.rows_text = collections.defaultdict(str)
        for fn in ("types.tsv", "fields.tsv"):
            for line in io.open(os.path.join(STORE, "_types", fn), encoding="utf-8"):
                t = line.split("\t", 1)[0]
                self.rows_text[t] += line
        self.static = {}
        for line in io.open(os.path.join(STORE, "_types", "types.tsv"), encoding="utf-8"):
            p = line.rstrip("\n").split("\t")
            if len(p) > 12:
                m = re.match(r"\s*STATIC\s+(0x[0-9A-Fa-f]+)", p[12])
                if m:
                    self.static[p[0]] = int(m.group(1), 16)

    def _load_types(self):
        import csv
        names = set()
        for r in csv.DictReader(io.open(os.path.join(STORE, "_types", "types.tsv"), encoding="utf-8"), delimiter="\t",
                                quoting=csv.QUOTE_NONE):
            names.add(r["type"])
        meaning = {}
        for r in csv.DictReader(io.open(os.path.join(STORE, "_types", "fields.tsv"), encoding="utf-8"),
                                delimiter="\t", quoting=csv.QUOTE_NONE):
            try:
                meaning[(r["type"], int(r["offset"], 16))] = (r.get("readiness") or "", r.get("meaning") or "")
            except (ValueError, TypeError):
                pass
        return names, meaning

    def ptr_cell_type(self, v):
        for lo, hi, t, kind, _s in self.spans:
            if kind == "pointer cell" and lo == v:
                return t
        return None

    def span_base_type(self, v):
        for lo, hi, t, kind, _s in self.spans:
            if kind != "pointer cell" and lo == v:
                return t
        return None

    def field_row(self, t, off):
        for fo, fs, nm, rd, ct in self.fields.get(t, ()):
            if fo <= off < fo + max(fs, 1):
                return fo, fs, nm, rd, ct
        return None

    def pointee(self, t, off):
        r = self.field_row(t, off)
        if r and r[0] == off:
            base = r[4].strip().rstrip("*").strip()
            if r[4].strip().endswith("*") and base in self.sizes:
                return base
        return None


def alias3(contract, name):
    return ALIASES3.get((contract, name)) or ALIASES3.get(("*", name))


def width_of(snippet, store):
    """Bytes of the C type that OPENS snippet (after spaces, backticks, pipes, '..'), or None. Only the first token
    counts: prose after an inline offset is not a width."""
    m = CTYPE.match(re.sub(r"^[\s`|.:=]*", "", STRUCK.sub("", snippet)))   # a struck (superseded) type is history
    if not m:
        return None
    base, n = m.group(1), m.group(2)
    if base.endswith("*"):
        sz = 8
    elif base in CSIZE:
        sz = CSIZE[base]
    elif base in store.sizes and store.sizes[base]:
        sz = store.sizes[base]
    else:
        return None
    return sz * (int(n, 0) if n else 1)


# ----------------------------------------------------------------------------------------------- symbol resolution
_PAGES = None


def page_lines():
    global _PAGES
    if _PAGES is None:
        _PAGES = []
        for p in glob.glob(os.path.join(DB, "**", "*.md"), recursive=True):
            rp = os.path.relpath(p, DB).replace(os.sep, "/")
            if rp.startswith("_index/") or rp.startswith("_experiments/"):
                continue                     # _index pages are verdicts and registers, not owners of addresses
            try:
                for line in io.open(p, encoding="utf-8", errors="replace"):
                    if "g_" in line:
                        _PAGES.append((rp, line))
            except OSError:
                pass
    return _PAGES


_SYMCACHE = {}


def resolve_symbol(sym, store):
    """-> (address or None, how)."""
    if sym in _SYMCACHE:
        return _SYMCACHE[sym]
    hit = [t for t, txt in store.rows_text.items() if re.search(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])" % re.escape(sym), txt)]
    stat = [t for t in hit if t in store.static]
    if len(stat) == 1:
        out = (store.static[stat[0]], "SYM-VIA-STORE:%s" % stat[0])
    else:
        cands = collections.Counter()
        where = {}
        rx = re.compile(r"(?<![0-9A-Za-z_])%s(?![0-9A-Za-z_])" % re.escape(sym))
        for rp, line in page_lines():
            for m in rx.finditer(line):
                for a in re.finditer(r"(?<![0-9A-Za-z_])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])", line):
                    # a BINDING, not a mention: only separators and at most one type word between address and symbol
                    between = line[a.end():m.start()] if a.end() <= m.start() else line[m.end():a.start()]
                    if len(between) > 40 or re.sub(r"[\s`|()\[\]:=,]|\b(?:%s)\b" % "|".join(CSIZE), "", between):
                        continue
                    v = int(a.group(1), 16)
                    if OLD.DATA_LO <= v < OLD.DATA_HI:
                        cands[v] += 1
                        where.setdefault(v, rp)
        if len(cands) == 1:
            v = next(iter(cands))
            out = (v, "SYM-VIA-PAGE:%s" % where[v])
        elif cands:
            (v1, c1), (v2, c2) = cands.most_common(2)
            out = (v1, "SYM-VIA-PAGE:%s (%d of %d mentions)" % (where[v1], c1, sum(cands.values()))) if c1 >= 3 * c2 \
                else (None, "SYMBOL: %d candidate addresses" % len(cands))
        else:
            out = (None, "SYMBOL: no store row and no page line binds it to an address")
    _SYMCACHE[sym] = out
    return out


# ----------------------------------------------------------------------------------------------- extraction
def layout_head_type(line, contract, store):
    s = line.strip()
    m = re.match(r"\[?\s*([A-Za-z_][A-Za-z0-9_]*)", s)
    if m:
        w = m.group(1)
        if w in store.names:
            return w, "head names %s" % w
        if w in C2.ALIASES:
            return C2.ALIASES[w][0], "head alias %s" % w
        a = alias3(contract, w)
        if a:
            return a[0], "head alias3 %s" % w
    indexed = re.search(r"indexed by|\+\s*\(?\s*\w+[^,]*\*|\brow\b|\belement\b", s)
    derefd = re.search(r"\[\s*(?:0x)?0[0-9A-Fa-f]{7}\s*\]|\*\s*\(|->", s)
    for a in re.finditer(r"(?<![0-9A-Za-z_])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])", s):
        v = int(a.group(1), 16)
        if not (OLD.DATA_LO <= v < OLD.DATA_HI):
            continue
        cell = [sp for sp in store.spans if sp[3] == "pointer cell" and sp[0] == v]
        if cell:
            t, stride = cell[0][2], cell[0][4]
            if indexed and not stride:
                return None, "head indexes through %08X, whose route (%s) points at one object, not rows" % (v, t)
            return t, "head pointer cell %08X" % v
        t = store.span_base_type(v)
        if t:
            if derefd:
                p = store.pointee(t, 0)
                if p:
                    return p, "head dereferences %08X (%s +0 -> %s)" % (v, t, p)
                return None, "head dereferences %08X but %s +0 is not a typed pointer" % (v, t)
            kind = [sp[3] for sp in store.spans if sp[0] == v and sp[2] == t][0]
            if indexed and kind != "elements":
                return None, "head indexes rows but %08X is the single object %s" % (v, t)
            return t, "head span base %08X" % v
    typed = sorted({w for w in re.findall(r"(?<![0-9A-Za-z_])([A-Z][A-Za-z0-9_]*[a-z][A-Za-z0-9_]*)", s)
                    if w in store.names})
    if len(typed) == 1:
        return typed[0], "head line names %s" % typed[0]
    for m in ANYREC.finditer(s):
        a = alias3(contract, m.group(1))
        t = a[0] if a else (m.group(1) if m.group(1) in store.names else None)
        if t:
            p = store.pointee(t, int(m.group(2), 16))
            if p:
                return p, "head %s+0x%s -> %s" % (m.group(1), m.group(2), p)
    return None, "unresolved head: %s" % s[:50]


def table_type(prev_lines, contract, store):
    """The single declared type named in the paragraph right before a table (up to 4 lines), else None."""
    para = []
    for pl in reversed(prev_lines):
        if not pl.strip():
            if para:
                break
            continue
        if pl.startswith("|"):
            break
        para.insert(0, pl)
        if len(para) == 4:
            break
    names = set()
    for pl in para:
        for w in re.findall(r"(?<![0-9A-Za-z_])([A-Za-z_][A-Za-z0-9_]*)", pl):
            if w in store.names:
                names.add(w)
            elif w in C2.ALIASES:
                names.add(C2.ALIASES[w][0])
    txt = " ".join(p.strip() for p in para)[:60]
    return (names.pop() if len(names) == 1 else None), txt


BARE = re.compile(r"(?<![0-9A-Fa-f])(0[0-9A-Fa-f]{7})?\s*`?\s*\+\s*`?\s*0x[0-9A-Fa-f]{1,5}\b")


def extract3(text, contract, store):
    """extract3_core plus the catch-all: on every ruled line, `+0xNN` offsets that no extractor consumed (and that
    are not a code-site citation `ADDR+0xNN`) are reported as UNATTRIBUTED kind BARE-OFFSET, one row per line with
    the count - so nothing the census cannot read goes uncounted."""
    cur, used = None, 0

    def flush(key):
        if key is None:
            return None
        sec, line = key
        total = 0
        for m in BARE.finditer(line):
            if m.group(1):
                continue                    # ADDR+0xNN: a code site or a data displacement (ABS reads the latter)
            total += 1
        if total > used:
            return dict(sec=sec, form="UNATTRIBUTED", kind="BARE-OFFSET", token=line.strip()[:60], line=line,
                        flag="%d of %d offsets on the line unread" % (total - used, total), n=total - used)
        return None

    for e in extract3_core(text, contract, store):
        if e["form"] == "LINE":
            b = flush(cur)
            if b:
                yield b
            cur, used = (e["sec"], e["line"]), 0
            continue
        if e["form"] in ("REC", "SKIP") or (e["form"] == "UNATTRIBUTED" and e["kind"] in (
                "PROSE-OFFSET", "LC-NAME", "WIDTH-OFFSET", "LAYOUT-HEAD")):
            used += 1
        elif e["form"] == "UNATTRIBUTED" and e["kind"] == "TABLE":
            rc = ROWCELL.match(e["line"])
            used += len(OFFS.findall(rc.group(1))) if rc else 1
        yield e
    b = flush(cur)
    if b:
        yield b


def extract3_core(text, contract, store):
    """Yield dicts: sec, form (ABS/REC/UNATTRIBUTED), kind (C2 or a new-form tag), token, v, d, line, flag, width."""
    layout = None           # (type or None, how) for a non-CamelCase head
    struct = None
    c2layout = None
    in_table = False
    thead = {}
    ttype = None
    prev = []
    for sec, line, fenced in OLD.state_sections(text):
        yield dict(sec=sec, form="LINE", line=line)
        # ---------------- census2's own forms (kind C2)
        spans = [line] if fenced else TICK.findall(line)
        for sp in spans:
            for m in ADDR_IN.finditer(sp):
                v = int(m.group(1), 16)
                if OLD.DATA_LO <= v < OLD.DATA_HI:
                    yield dict(sec=sec, form="ABS", kind="C2", token=m.group(0).strip(), v=v,
                               d=int(m.group(2), 16) if m.group(2) else 0, line=line)
            # INDEX: ADDR[n]
            for m in INDEX.finditer(sp):
                v, n = int(m.group(1), 16), int(m.group(2), 0)
                if not (OLD.DATA_LO <= v < OLD.DATA_HI):
                    continue
                ww = re.search(r"\b(byte|word|dword|qword)\s*`?\s*(?:\[\s*)?(?:0x)?%s" % m.group(1), line, re.I)
                esz = WIDTH_WORDS[ww.group(1).lower()] if ww else None
                if esz is None:
                    cls, t, _w = OLD.resolve(v, store.spans, store.fields, store.sizes)
                    r = store.field_row(t, 0) if t else None
                    am = re.search(r"\[(\d+)\]", r[4]) if r else None
                    if r and am and int(am.group(1)):
                        esz = r[1] // int(am.group(1))
                if esz:
                    yield dict(sec=sec, form="ABS", kind="INDEX", token=m.group(0), v=v, d=n * esz, line=line)
                else:
                    yield dict(sec=sec, form="UNATTRIBUTED", kind="INDEX-UNSIZED", token=m.group(0), line=line)
        # SLASH lists (over the raw line: the suffixes are often separate backtick spans)
        for m in SLASH.finditer(line):
            base = m.group(1)
            v0 = int(base, 16)
            if not (OLD.DATA_LO <= v0 < OLD.DATA_HI):
                continue
            for it in SLASH_ITEM.finditer(m.group(2)):
                suf = it.group(1)
                v = int(base[:8 - len(suf)] + suf, 16) if len(suf) < 8 else int(suf, 16)
                if len(suf) < 8 and OLD.DATA_LO <= v < OLD.DATA_HI:
                    yield dict(sec=sec, form="ABS", kind="SLASH", token="%s/%s" % (base, suf), v=v, d=0, line=line)
        # SYM: DAT_/uRam_/PTR_ addresses, g_ symbols
        for m in SYM_ADDR.finditer(line):
            v = int(m.group(1), 16)
            if OLD.DATA_LO <= v < OLD.DATA_HI:
                yield dict(sec=sec, form="ABS", kind="SYM", token=m.group(0), v=v, d=0, line=line)
        for m in SYM_G.finditer(line):
            v, how = resolve_symbol(m.group(1), store)
            if v is None:
                yield dict(sec=sec, form="UNATTRIBUTED", kind="SYMBOL", token=m.group(1), line=line, flag=how)
            else:
                yield dict(sec=sec, form="ABS", kind="SYM", token=m.group(1), v=v, d=0, line=line, flag=how)
        # ---------------- record-relative
        c2names = set()
        for m in REC_INLINE2.finditer(line):
            nm = m.group(1)
            if nm in store.names or nm in C2.ALIASES or C2.CAMEL.match(nm):
                c2names.add(m.start())
                if nm not in store.names and nm not in C2.ALIASES and alias3(contract, nm):
                    nm = alias3(contract, nm)[0]          # a CamelCase working name bound by ALIASES3
                yield dict(sec=sec, form="REC", kind="C2" if C2.REC_INLINE.match(line, m.start()) else "LC",
                           token=m.group(0), v=nm, d=int(m.group(2), 16), line=line,
                           width=width_of(line[m.end():m.end() + 90], store))
                pos = m.end()
                while True:
                    c = CONT.match(line, pos)
                    if not c:
                        break
                    yield dict(sec=sec, form="REC", kind="CONT", token="%s +0x%s" % (nm, c.group(1)), v=nm,
                               d=int(c.group(1), 16), line=line, width=None)
                    pos = c.end()
        for m in ANYREC.finditer(line):
            if m.start() in c2names:
                continue
            nm = m.group(1)
            if nm == "s" and m.start() >= 2 and line[m.start() - 1] in "'’":
                pw = re.search(r"([A-Za-z_][A-Za-z0-9_]*)$", line[:m.start() - 1])   # possessive: "the unit's +0x6B7"
                nm = pw.group(1) if pw else nm
            if re.match(NAME + "$", nm) and (nm in store.names or nm in C2.ALIASES or C2.CAMEL.match(nm)):
                continue
            if nm.lower() in REGISTERS:
                yield dict(sec=sec, form="SKIP", kind="REGISTER", token=m.group(0), line=line)
                continue
            if nm in PROSE_WORDS:
                yield dict(sec=sec, form="UNATTRIBUTED", kind="PROSE-OFFSET", token=m.group(0), line=line)
                continue
            if nm.lower() in WIDTH_WORDS:
                yield dict(sec=sec, form="UNATTRIBUTED", kind="WIDTH-OFFSET", token=m.group(0), line=line)
                continue
            a = alias3(contract, nm)
            if not a:
                if fenced and layout is None and c2layout is None and LAYOUT_ROW.match(line) is None:
                    pass
                yield dict(sec=sec, form="UNATTRIBUTED", kind="LC-NAME", token=m.group(0), line=line)
                continue
            yield dict(sec=sec, form="REC", kind="LC", token=m.group(0), v=a[0], d=int(m.group(2), 16), line=line,
                       width=width_of(line[m.end():m.end() + 90], store))
            pos = m.end()
            while True:
                c = CONT.match(line, pos)
                if not c:
                    break
                yield dict(sec=sec, form="REC", kind="CONT", token="%s +0x%s" % (nm, c.group(1)), v=a[0],
                           d=int(c.group(1), 16), line=line, width=None)
                pos = c.end()
        # ---------------- fenced layouts
        if fenced:
            h = C2.LAYOUT_HEAD.match(line)
            r = LAYOUT_ROW.match(line)
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            sm = STRUCT_HEAD.match(line)
            if sm:
                struct = sm.group(1)
            elif struct and stripped.startswith("}"):
                struct = None
            cm = STRUCT_ROW.search(line) if struct else None
            if cm:
                yield dict(sec=sec, form="REC", kind="STRUCT", token="%s +0x%s" % (struct, cm.group(1)), v=struct,
                           d=int(cm.group(1), 16), line=line, width=width_of(line, store))
                continue
            if sm:
                continue
            if h and not r:
                c2layout, layout = h.group(1), None          # census2's own layout form
            elif r and c2layout:
                pass                                         # census2 yields it (below)
            elif r and layout is not None:
                off = int(r.group(1) or r.group(2), 16)
                if layout[0]:
                    more = re.match(r"((?:\s*/\s*\+?0x[0-9A-Fa-f]{1,5})*)", line[r.end():])     # "+0x069 / +0x079"
                    tail = line[r.end() + len(more.group(1)):]
                    for o in [off] + [int(x, 16) for x in re.findall(r"0x([0-9A-Fa-f]{1,5})", more.group(1))]:
                        yield dict(sec=sec, form="REC", kind="LAYOUT", token="%s +0x%X" % (layout[0], o), v=layout[0],
                                   d=o, line=line, width=width_of(tail[:30], store), how=layout[1])
                else:
                    yield dict(sec=sec, form="UNATTRIBUTED", kind="LAYOUT-HEAD", token=stripped[:50], line=line,
                               flag=layout[1])
            elif r:
                yield dict(sec=sec, form="UNATTRIBUTED", kind="LAYOUT-HEAD", token=stripped[:50], line=line,
                           flag="offset row with no head line")
            elif not stripped:
                layout, c2layout = None, None
            elif not r and (indent >= 6 or stripped[0] in ".|\\/(<-"):
                pass                                         # continuation line: keep the head
            elif not r:
                layout, c2layout = layout_head_type(line, contract, store), None
            if r and c2layout:
                yield dict(sec=sec, form="REC", kind="C2", token="%s +0x%s" % (c2layout, r.group(1) or r.group(2)),
                           v=c2layout, d=int(r.group(1) or r.group(2), 16), line=line,
                           width=width_of(line[r.end():r.end() + 30], store))
        else:
            layout, c2layout, struct = None, None, None
            # ---------------- tables
            if line.startswith("|"):
                if not in_table:
                    in_table = True
                    ttype = table_type(prev[-12:], contract, store)
                    hcells = [c.strip().strip("*` ").lower() for c in line.strip().strip("|").split("|")]
                    thead = {}
                    if hcells and not re.match(r"\+?\s*0x", hcells[0]):
                        for i, hc in enumerate(hcells[1:]):
                            if hc in ("size", "bytes", "width") and "size" not in thead:
                                thead["size"] = i
                            elif hc in ("type", "ctype", "c type", "width / type") and "type" not in thead:
                                thead["type"] = i
                rc = ROWCELL.match(line)
                if rc and re.match(r"\s*`?\+\s*0x", rc.group(1)):
                    offs = [int(x, 16) for x in OFFS.findall(rc.group(1))]
                    rest = line[rc.end():]
                    cols = [c.strip() for c in rest.split("|")]
                    w = None        # a width only from a column the header calls size/width/bytes or type/width
                    if thead.get("size") is not None and thead["size"] < len(cols):
                        sm_ = re.match(r"^`?~?~?(\d+|0x[0-9A-Fa-f]+)`?", cols[thead["size"]])
                        w = int(sm_.group(1), 0) if sm_ else None
                    if w is None and thead.get("type") is not None and thead["type"] < len(cols):
                        w = width_of(cols[thead["type"]], store)
                    if w is None and not thead:
                        w = width_of(rest[:80], store)   # header-less row: only a type that opens the next cell
                    if ttype and ttype[0]:
                        for off in offs:
                            yield dict(sec=sec, form="REC", kind="TABLE", token="%s +0x%X" % (ttype[0], off),
                                       v=ttype[0], d=off, line=line, width=w if len(offs) == 1 else None,
                                       how="table after: %s" % ttype[1])
                    else:
                        yield dict(sec=sec, form="UNATTRIBUTED", kind="TABLE", token=line.strip()[:60], line=line,
                                   flag="no single type on the line before the table: %s" % (ttype[1] if ttype else ""))
            else:
                in_table = False
                ttype = None
        prev.append(line)


# ----------------------------------------------------------------------------------------------- credited contracts
def contract_index():
    idx = {}
    for p in glob.glob(os.path.join(DB, "**", "CONTRACT-*.md"), recursive=True):
        rp = os.path.relpath(p, DB).replace(os.sep, "/")
        if rp.startswith("_index/candidates/") or rp.startswith("_experiments/"):
            continue
        idx.setdefault(os.path.basename(p), []).append(os.path.normpath(p))
    return idx


def verdict_rows(path=None):
    path = path or os.path.join(DB, "_index", "L2-VERDICTS.md")
    lines = io.open(path, encoding="utf-8").read().splitlines()
    rows = {}
    start = None
    for i, l in enumerate(lines):
        if l.startswith("| system | contract |"):
            start = i
            break
    for l in lines[start + 2:]:
        if not l.startswith("|"):
            break
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]]
        m = re.match(r"\*\*(S-\d+)\*\*", cells[0])
        if m:
            rows[m.group(1)] = cells
    return rows


def cell_contracts(cell, idx):
    """Contracts named in the UNSTRUCK text of an L2 contract cell -> (paths, unresolved names)."""
    out, bad = [], []
    for ref in CONTRACT_REF.findall(STRUCK.sub("", cell)):
        cands = idx.get(os.path.basename(ref), [])
        if len(cands) > 1:
            cands = [c for c in cands if c.replace(os.sep, "/").endswith(ref)] or cands
        if len(cands) == 1:
            if cands[0] not in out:
                out.append(cands[0])
        else:
            bad.append(ref)
    return out, bad


def credited3():
    """{path: {system: source}} with source 'col6' (census2's) or 'cell' (L2 contract cell only)."""
    out = collections.defaultdict(dict)
    for path, systems in C2.credited().items():
        for s in systems:
            out[os.path.normpath(path)][s] = "col6"
    idx = contract_index()
    unresolved = []
    for s, cells in verdict_rows().items():
        paths, bad = cell_contracts(cells[1], idx)
        unresolved += [(s, b) for b in bad]
        for p in paths:
            out[os.path.normpath(p)].setdefault(s, "cell")
    return out, unresolved


# ----------------------------------------------------------------------------------------------- classification
def unnamed_bytes(t, lo, hi, store):
    """Bytes of [lo, hi) not inside a named (non-gap) field row of t."""
    n = 0
    for b in range(lo, hi):
        r = store.field_row(t, b)
        if r is None or r[2].lower().startswith(("unobserved", "gap", "unresolved")) or "Span" in r[2]:
            n += 1
    return n


def classify_rec(t, d, width, store):
    size = store.sizes.get(t)
    if size is not None and d >= size:
        return "OUT-OF-EXTENT", "+0x%X >= size 0x%X" % (d, size), ""
    cls, where = OLD.field_at(t, d, store.fields, store.sizes)
    flag = ""
    r = store.field_row(t, d)
    if width and size is not None:
        width = min(width, size - d)
    if cls == "GAP-SPAN":
        if r is None:
            flag = "NO-ROW"
        elif width:
            flag = "GAP-EXACT" if (r[0] == d and r[1] == width) else ("GAP-COARSER" if r[1] > width else "GAP")
    elif cls == "FIELD" and width and width > 1:
        n = unnamed_bytes(t, d, d + width, store)
        if n:
            flag = "WIDER-THAN-FIELD (%d of the %d named bytes are not in a named field)" % (n, width)
    if cls == "FIELD" and t:
        rd, mn = store.meaning.get((t, d), ("", ""))
        if rd in ("DISCOVERED", "UNKNOWN") or C2.OPEN.search(mn or ""):
            flag = (flag + " MEANING-OPEN").strip()
    return cls, where, flag


def classify_abs(e, store):
    v, d, line = e["v"], e["d"], e["line"]
    spans, fields, sizes = store.spans, store.fields, store.sizes
    cls, tname, where = OLD.resolve(v + d, spans, fields, sizes)
    ends = {int(m.group(2), 16) for m in OLD.RANGE.finditer(line)}
    starts = {int(m.group(1), 16): int(m.group(2), 16) for m in OLD.RANGE.finditer(line)}
    derefd = any(("%08X" % v).lower() in m.group(0).lower() for m in C2.DEREF.finditer(line))
    if d and not derefd and cls == "UNDECLARED" and e["kind"] == "C2":
        bcls, btype, _bw = OLD.resolve(v, spans, fields, sizes)
        if bcls == "PTR-CELL" or btype.endswith("Pointer"):
            cls, tname, where = "AMBIGUOUS-DEREF", btype, ("ADDR+0x%X where ADDR is a declared pointer cell (%s):"
                                                            " likely the pointee's +0x%X - hand read" % (d, btype, d))
    if d and derefd and e["kind"] == "C2":
        cls, tname, where = OLD.resolve(v, spans, fields, sizes)
        where = "DEREF pointee +0x%X (pointee type needs a hand read); cell: %s" % (d, where)
    bb = C2.bare_base(v + d if e["kind"] != "C2" else v, d if e["kind"] == "C2" else 0, cls, spans)
    if bb:
        cls, tname, where = "OBJECT", bb, "the base of the declared %s span (bare-base ruling)" % bb
    if cls in ("UNDECLARED", "GAP-SPAN") and (v + d) in ends:
        cls = "RANGE-END"
    elif cls == "UNDECLARED" and (v + d) in starts and starts[v + d] > v + d:
        if OLD.covered_fraction(v + d, starts[v + d], spans) >= 0.9:
            cls, where = "RANGE-START", "start of a range >=90% declared (old census rule)"
    return cls, tname, where


# ----------------------------------------------------------------------------------------------- selftest
FIX = {
    "LC": "# F\n## 3. Types\n\n`unit + 0x698` is the stats pointer.\n",
    "CONT": "# F\n## 5. State\n\n| read | unit `+0x00`, `+0x10`, `+0x40` |\n",
    "LAYOUT-PTRCELL": "# F\n## 3. Types\n\n```\nrecords:  *(char**)0x0208E690 + slot * 0x250\n  +0x08  u16  death count\n```\n",
    "LAYOUT-POINTEE": "# F\n## 3. Types\n\n```\nthe stats (unit + 0x698)\n  +0x194  uint8[46]  owned bits\n```\n",
    "TABLE": "# F\n## 3. Types\n\n`AuthoredTableHeader`, at least 0x20:\n\n| offset | size | field |\n|---|---|---|\n"
             "| `+0x04` | 4 | `rowCount` |\n",
    "SYM-DAT": "# F\n## 5. State\n\nthe gate `DAT_02089300`.\n",
    "SYM-G": "# F\n## 5. State\n\n`g_nSpawnKeepReturnWindow` (seconds, default 300).\n",
    "SLASH": "# F\n## 5. State\n\nenemy joins `02EBF150/168/148/140`; the triple `02AEE054`/`58`/`5C`.\n",
    "INDEX": "# F\n## 5. State\n\n| written | byte `0209A2C4[2]` |\n",
    "STRUCT": "# F\n## 3. Types\n\n```\nstruct WidgetMessage {\n    uint64_t a;   /* +0x08 */\n};\n```\n",
    "NEG": "# F\n## 3. Types\n\n`rbx + 0x30` is a register; `foo + 0x10` is unknown; `0215F1C0[3]` has no width.\n",
}


def selftest(store):
    def new(k, contract="CONTRACT-fixture.md"):
        return list(extract3(FIX[k], contract, store))

    def old(k):
        return list(C2.extract_new(FIX[k]))

    def has_rec(es, t, d):
        return any(e["form"] == "REC" and (e["v"] == t) and e["d"] == d for e in es)

    def has_abs(es, a):
        return any(e["form"] == "ABS" and e["v"] + e["d"] == a for e in es)

    def old_rec(os_, d):
        return any(f == "REC" and dd == d for _s, f, _t, _v, dd, _l in os_)

    def old_abs(os_, a):
        return any(f == "ABS" and v + dd == a for _s, f, _t, v, dd, _l in os_)

    lay = new("LAYOUT-PTRCELL")
    pte = new("LAYOUT-POINTEE")
    neg = new("NEG")
    cell_paths, _b = cell_contracts("~~`11-Party/CONTRACT-party-slot-assignment.md`~~ `16-UI/CONTRACT-ui-request-router.md` (FABLE)",
                                    contract_index())
    c2cred = C2.credited()
    router = [p for p in cell_paths if p.endswith("CONTRACT-ui-request-router.md")]
    checks = [
        ("LC: new finds unit + 0x698 -> BattleUnit", has_rec(new("LC"), "BattleUnit", 0x698)),
        ("LC: census2 misses it", not old_rec(old("LC"), 0x698)),
        ("CONT: new finds unit +0x10 and +0x40", has_rec(new("CONT"), "BattleUnit", 0x10) and has_rec(new("CONT"), "BattleUnit", 0x40)),
        ("CONT: census2 misses them", not old_rec(old("CONT"), 0x10)),
        ("LAYOUT: pointer-cell head -> SpawnRecord +0x08", has_rec(lay, "SpawnRecord", 0x08)),
        ("LAYOUT: pointer-field head -> BattleStatsRecord +0x194", has_rec(pte, "BattleStatsRecord", 0x194)),
        ("LAYOUT: census2 misses both", not old_rec(old("LAYOUT-PTRCELL"), 0x08) and not old_rec(old("LAYOUT-POINTEE"), 0x194)),
        ("TABLE: new attributes +0x04 to AuthoredTableHeader", has_rec(new("TABLE"), "AuthoredTableHeader", 4)),
        ("TABLE: census2 leaves it unattributed", not old_rec(old("TABLE"), 4)),
        ("SYM: new finds DAT_02089300", has_abs(new("SYM-DAT"), 0x02089300)),
        ("SYM: census2 misses DAT_02089300", not old_abs(old("SYM-DAT"), 0x02089300)),
        ("SYM: g_nSpawnKeepReturnWindow -> 0208936C", has_abs(new("SYM-G"), 0x0208936C)),
        ("SYM: census2 misses it", not old_abs(old("SYM-G"), 0x0208936C)),
        ("SLASH: new finds 02EBF168, 02EBF148, 02EBF140, 02AEE058, 02AEE05C",
         all(has_abs(new("SLASH"), a) for a in (0x02EBF168, 0x02EBF148, 0x02EBF140, 0x02AEE058, 0x02AEE05C))),
        ("SLASH: census2 misses 02EBF168", not old_abs(old("SLASH"), 0x02EBF168)),
        ("INDEX: new finds 0209A2C6", has_abs(new("INDEX"), 0x0209A2C6)),
        ("INDEX: census2 misses it", not old_abs(old("INDEX"), 0x0209A2C6)),
        ("STRUCT: new finds WidgetMessage +0x08 from a C-struct comment", has_rec(new("STRUCT"), "WidgetMessage", 8)),
        ("STRUCT: census2 misses it", not old_rec(old("STRUCT"), 8)),
        ("CELL: router contract credited from an unstruck cell mention", len(router) == 1),
        ("CELL: the struck mention is not credited", not any(p.endswith("CONTRACT-party-slot-assignment.md") for p in cell_paths)),
        ("CELL: census2 does not credit the router contract to S-36",
         not any(p.endswith("CONTRACT-ui-request-router.md") and "S-36" in s for p, s in c2cred.items())),
        ("NEG: a register offset is skipped, not a record", not any(e["form"] == "REC" for e in neg)),
        ("NEG: an unknown lower-case name is UNATTRIBUTED", any(e["form"] == "UNATTRIBUTED" and e["kind"] == "LC-NAME" for e in neg)),
        ("NEG: an index with no width is UNATTRIBUTED", any(e["kind"] == "INDEX-UNSIZED" for e in neg)),
    ]
    for k, v in checks:
        print("  %-66s %s" % (k, "PASS" if v else "FAIL"))
    print("census2's own selftest:")
    ok2 = C2.selftest(store.names)
    return all(v for _k, v in checks) and ok2, sum(1 for _k, v in checks if v), len(checks)


# ----------------------------------------------------------------------------------------------- main
def ucount(r):
    """Offsets an UNATTRIBUTED row stands for (a BARE-OFFSET row carries 'N of M offsets on the line unread')."""
    m = re.match(r"(\d+) of \d+ offsets", r[9]) if r[5] == "BARE-OFFSET" else None
    return int(m.group(1)) if m else 1


def main():
    store = Store()
    print("store:", os.path.join(STORE, "_types"))
    print("selftest:")
    ok, npass, n = selftest(store)
    print("census3 selftest %d/%d" % (npass, n))
    if not ok:
        print("SELFTEST FAILED - census not run")
        return 1
    if "--selftest" in sys.argv:
        return 0
    cred, unresolved = credited3()
    rows, unat = [], []
    skipped = collections.Counter()
    for path in sorted(cred):
        systems = cred[path]
        sysl = ",".join(sorted(systems, key=lambda x: int(x[2:])))
        src = ",".join("%s:%s" % (s, systems[s]) for s in sorted(systems, key=lambda x: int(x[2:])))
        rel = os.path.relpath(path, DB).replace(os.sep, "/")
        if not os.path.exists(path):
            rows.append((sysl, rel, src, "-", "MISSING", "", "", "", "", "", ""))
            continue
        text = io.open(path, encoding="utf-8", errors="replace").read()
        contract = os.path.basename(path)
        seen = set()
        for e in extract3(text, contract, store):
            if e["form"] == "SKIP":
                for s in systems:
                    skipped[s] += 1
                continue
            if e["form"] == "UNATTRIBUTED":
                key = ("U", e["kind"], e["token"])
                if key in seen:
                    continue
                seen.add(key)
                rows.append((sysl, rel, src, e["sec"][:40], "UNATTRIBUTED", e["kind"], e["token"][:60], "UNATTRIBUTED",
                             "", e.get("flag", ""), ""))
                continue
            if e["form"] == "ABS":
                key = ("A", e["v"] + e["d"])
                if key in seen:
                    continue
                seen.add(key)
                cls, tname, where = classify_abs(e, store)
                rows.append((sysl, rel, src, e["sec"][:40], "ABS", e["kind"],
                             "%08X%s" % (e["v"], "+0x%X" % e["d"] if e["d"] else ""), cls, tname, where,
                             e.get("flag", "")))
                continue
            nm, d = e["v"], e["d"]
            if not (nm in store.names or nm in C2.ALIASES or C2.CAMEL.match(nm)):
                continue
            t = nm if nm in store.names else (C2.ALIASES[nm][0] if nm in C2.ALIASES else None)
            key = ("R", t or nm, d)
            if key in seen:
                continue
            seen.add(key)
            if t is None:
                cls, where, flag = "UNTYPED", "no declared type or alias named %s" % nm, ""
            else:
                cls, where, flag = classify_rec(t, d, e.get("width"), store)
                if e.get("how"):
                    where = "%s [%s]" % (where, e["how"])
            rows.append((sysl, rel, src, e["sec"][:40], "REC", e["kind"], e["token"].strip()[:60], cls, t or "", where,
                         flag))
    with io.open(os.path.join(HERE, "census3.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("systems\tcontract\tcredited\tsection\tform\tkind\ttoken\tclass\ttype\twhere\tflag\n")
        for r in rows:
            f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    per = collections.defaultdict(collections.Counter)
    for r in rows:
        for s in r[0].split(","):
            per[s][r[7]] += ucount(r) if r[7] == "UNATTRIBUTED" else 1
            if r[5] not in ("C2",):
                per[s]["NEW-FORM"] += 1
            for fl in ("NO-ROW", "GAP-COARSER", "WIDER-THAN-FIELD", "GAP-EXACT"):
                if fl in r[10]:
                    per[s][fl] += 1
    bad = ("UNDECLARED", "UNTYPED", "OUT-OF-EXTENT")
    cols = ["FIELD", "OBJECT", "GAP-SPAN", "PTR-CELL", "UNDECLARED", "UNTYPED", "OUT-OF-EXTENT", "RANGE-END",
            "RANGE-START", "AMBIGUOUS-DEREF", "UNATTRIBUTED", "NO-ROW", "GAP-COARSER", "WIDER-THAN-FIELD", "GAP-EXACT",
            "NEW-FORM"]
    with io.open(os.path.join(HERE, "census3_systems.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("system\t" + "\t".join(cols) + "\tREGISTER-SKIPPED\n")
        for s in sorted(per, key=lambda x: int(x[2:]) if x[2:].isdigit() else 999):
            f.write(s + "\t" + "\t".join(str(per[s][c]) for c in cols) + "\t%d\n" % skipped[s])
    ua = collections.Counter()
    for r in rows:
        if r[7] == "UNATTRIBUTED":
            ua[(r[0], r[5])] += ucount(r)
    with io.open(os.path.join(HERE, "census3_unattributed.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("systems\tkind\tcount\n")
        for (s, k), n in sorted(ua.items()):
            f.write("%s\t%s\t%d\n" % (s, k, n))
    tot = collections.Counter(r[7] for r in rows)
    print("rows %d  %s" % (len(rows), dict(tot)))
    print("unresolved contract-cell references: %d %s" % (len(unresolved), unresolved[:10]))
    print("systems with UNDECLARED/UNTYPED/OUT-OF-EXTENT:",
          sorted((s for s in per if any(per[s][b] for b in bad)), key=lambda x: int(x[2:])))
    print("systems with NO-ROW/GAP-COARSER/WIDER-THAN-FIELD:",
          sorted((s for s in per if any(per[s][b] for b in ("NO-ROW", "GAP-COARSER", "WIDER-THAN-FIELD"))),
                 key=lambda x: int(x[2:])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
