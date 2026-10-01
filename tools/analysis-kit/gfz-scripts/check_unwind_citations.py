"""check_unwind_citations.py - FINAL-AUDIT-PROTOCOL pass 6, by ADDRESS rather than by word.

WHY THIS EXISTS. `check_banned_evidence.py` sweeps documents for the WORDS `.pdata`, `.xdata`,
`unwind`, `RUNTIME_FUNCTION`, `IP-to-state` and friends. It reported pass 6 clean, and on 2026-09-16
pass 6 turned out to have a genuine violation it could not see: `the-blinking-icon-and-its-atlas.md`
rested its reachability claim on `01D70800` and `01D70810`, which are CHAINED `RUNTIME_FUNCTION`
records, while calling them *"a dispatch table of 4-byte RVAs"*. THE PAGE NEVER USED A BANNED WORD,
so a lexical sweep was structurally incapable of catching it. A page that knows it is quoting unwind
data says so; a page that has been fooled by it does not - and the second is the case pass 6 exists
for.

So this checks the ADDRESSES. It builds the extent of every unwind structure in the image from
`.pdata` outward, then asks which addresses the corpus cites land inside one.

  RUNTIME_FUNCTION   12 bytes in `.pdata`: {Begin, End, UnwindInfoAddress}
  UNWIND_INFO        byte 0 = Version(3) | Flags(5); byte 2 = CountOfCodes; codes are 2 bytes each,
                     padded to an even count
  CHAINED ENTRY      when UNW_FLAG_CHAININFO (4) is set, what follows the codes IS a RUNTIME_FUNCTION
                     - AND IT LIVES IN `.rdata`, BELOW `.pdata`. This is the class that was missed,
                     and it is missed by every guard phrased as "above the start of .pdata", because
                     the ban names a CLASS and that rule tests a SECTION.
  HANDLER + LANGDATA when EHANDLER/UHANDLER (3) is set, a handler RVA follows, then language data -
                     a `SCOPE_TABLE` for `__C_specific_handler`, a `FuncInfo` for C++ EH.

A hit is NOT automatically a failure: a page whose SUBJECT is unwind metadata must cite it, and the
protocol, the evidence standard and the audit log necessarily quote it. Those are exempted the same
way `check_banned_evidence.py` exempts them, and everything else is reported for adjudication.

Usage:  python check_unwind_citations.py --db "Database/FFXII TZA" [--exe <image>] [--quiet]
Exit 1 if any unexempt citation lands inside unwind metadata, 2 on a broken control.
"""
import argparse
import bisect
import io
import os
import re
import struct
import sys

BASE = 0x00120000
DEFAULT_EXE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "work", "verify", "embedded_exe.bin")

# Pages whose SUBJECT is the metadata, or which define/record the ban. Same principle as
# check_banned_evidence.py: quoting the thing you are documenting is not resting on it.
EXEMPT = (
    "_index/FINAL-AUDIT-PROTOCOL.md",
    "_index/EVIDENCE-STANDARD.md",
    "_index/AUDIT-LOG.md",
    "_index/PROGRAM-STATE.md",
    "24-Compiler-And-CRT-Runtime/",
)

CITE = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})`")


def load_image(path):
    data = io.open(path, "rb").read()
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe:pe + 4] != b"PE\0\0":
        raise SystemExit("not a PE image: %s" % path)
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    optsz = struct.unpack_from("<H", data, pe + 20)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + optsz + 40 * i
        name = data[o:o + 8].rstrip(b"\0").decode("latin1")
        # VirtualSize@8, VirtualAddress@12, SizeOfRawData@16, PointerToRawData@20 - reading these
        # from the wrong offset produces a .text of 0x1000 bytes and silently breaks everything.
        vsz, va, rsz, ptr = struct.unpack_from("<IIII", data, o + 8)
        secs.append((name, BASE + va, vsz, ptr, rsz))
    return data, secs


class Image(object):
    def __init__(self, path):
        self.d, self.secs = load_image(path)

    def off(self, va):
        for _n, s, vsz, ptr, rsz in self.secs:
            if s <= va < s + vsz:
                d = va - s
                return ptr + d if d < rsz else None
        return None

    def dw(self, va):
        o = self.off(va)
        return None if o is None or o + 4 > len(self.d) else struct.unpack_from("<I", self.d, o)[0]

    def by(self, va):
        o = self.off(va)
        return None if o is None else self.d[o]

    def sec(self, name):
        for n, s, vsz, ptr, rsz in self.secs:
            if n == name:
                return s, vsz, ptr, rsz
        raise SystemExit("no %s section" % name)


def build_extents(img):
    """Every byte of unwind metadata reachable from .pdata, tagged with its class."""
    spans = []
    ps, pvsz, pptr, prsz = img.sec(".pdata")
    seen = set()

    def walk_unwind(uva, depth=0):
        if uva in seen or depth > 8:
            return
        seen.add(uva)
        h = img.by(uva)
        if h is None or (h & 7) != 1:
            return
        flags = (h >> 3) & 0x1F
        cc = img.by(uva + 2)
        if cc is None:
            return
        slots = cc + (cc & 1)
        body_end = uva + 4 + 2 * slots
        spans.append((uva, body_end, "UNWIND_INFO"))
        if flags & 4:                               # UNW_FLAG_CHAININFO
            spans.append((body_end, body_end + 12, "CHAINED_RUNTIME_FUNCTION"))
            nxt = img.dw(body_end + 8)
            if nxt:
                walk_unwind(BASE + nxt, depth + 1)
        elif flags & 3:                             # EHANDLER / UHANDLER
            spans.append((body_end, body_end + 4, "EH_HANDLER_RVA"))
            lang = body_end + 4
            fi = img.dw(lang)
            if fi and img.dw(BASE + fi) in (0x19930520, 0x19930521, 0x19930522, 0x1993052F):
                spans.append((lang, lang + 4, "FuncInfo_ptr"))
                spans.append((BASE + fi, BASE + fi + 0x28, "FuncInfo"))
            else:
                c = img.dw(lang)
                if c and c < 4096:
                    e = img.d[img.off(lang + 4):img.off(lang + 4) + 16] if img.off(lang + 4) else b""
                    if len(e) == 16:
                        b0, e0, _h0, _j0 = struct.unpack_from("<IIII", e, 0)
                        ts, tvsz, _p, _r = img.sec(".text")
                        if b0 < e0 and ts <= BASE + b0 < ts + tvsz and ts < BASE + e0 <= ts + tvsz:
                            spans.append((lang, lang + 4 + 16 * c, "SCOPE_TABLE"))

    for i in range(min(pvsz, prsz) // 12):
        b, e, u = struct.unpack_from("<III", img.d, pptr + 12 * i)
        if not u:
            continue
        spans.append((ps + 12 * i, ps + 12 * i + 12, "RUNTIME_FUNCTION(.pdata)"))
        walk_unwind(BASE + u)

    spans = [s for s in spans if s[1] > s[0]]
    spans.sort()
    return spans


def make_lookup(spans):
    starts = [lo for lo, _hi, _k in spans]

    def which(va):
        i = bisect.bisect_right(starts, va) - 1
        while i >= 0 and spans[i][0] <= va:
            if va < spans[i][1]:
                return spans[i][2]
            i -= 1
        return None
    return which


def controls(which, img):
    """A detector that never fires, or always fires, has proved nothing."""
    ok = True
    for va, want in ((0x01D70800, "CHAINED_RUNTIME_FUNCTION"),
                     (0x01D70810, "CHAINED_RUNTIME_FUNCTION"),
                     (0x01D6CC48, "CHAINED_RUNTIME_FUNCTION"),
                     (0x01D6F79C, "CHAINED_RUNTIME_FUNCTION")):
        got = which(va)
        if got != want:
            print("   CONTROL FAILED (positive): %08X expected %s, got %s" % (va, want, got))
            ok = False
    for va in (0x002B7B80, 0x002B8EE0, 0x00121000):
        got = which(va)
        if got is not None:
            print("   CONTROL FAILED (negative): %08X is code, reported %s" % (va, got))
            ok = False
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    img = Image(a.exe)
    spans = build_extents(img)
    which = make_lookup(spans)

    print("FINAL-AUDIT-PROTOCOL pass 6 - unwind metadata cited BY ADDRESS")
    print("  %d unwind structures mapped from .pdata outward" % len(spans))
    kinds = {}
    for _lo, _hi, k in spans:
        kinds[k] = kinds.get(k, 0) + 1
    for k in sorted(kinds):
        print("     %-28s %6d" % (k, kinds[k]))
    print("")
    print("  CONTROLS")
    if not controls(which, img):
        print("  controls failed - the sweep is not trustworthy, reporting nothing")
        return 2
    print("     4 positive (known chained entries), 3 negative (code addresses): all pass")
    print("")

    hits = []
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if d not in ("_templates",)]
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), a.db).replace("\\", "/")
            if "_inbox" in rel or any(rel.startswith(e) for e in EXEMPT):
                continue
            text = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for i, line in enumerate(text.split("\n"), 1):
                for h in sorted(set(CITE.findall(line))):
                    k = which(int(h, 16))
                    if k:
                        hits.append((rel, i, h.upper(), k, line.strip()))

    print("  CITATIONS LANDING INSIDE UNWIND METADATA: %d" % len(hits))
    if hits and not a.quiet:
        for rel, i, h, k, line in hits:
            print("     %-56s :%-5d %s  %s" % (rel[:56], i, h, k))
            print("        %s" % line[:150])
    if hits:
        print("")
        print("  A hit is a QUESTION, not a verdict: a page may cite one of these to say it is NOT")
        print("  evidence, which is what a corrected page looks like. Read the line before ruling.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
