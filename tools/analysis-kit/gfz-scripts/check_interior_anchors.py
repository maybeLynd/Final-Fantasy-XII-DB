#!/usr/bin/env python3
"""check_interior_anchors.py - an "Interior anchor" that is not an instruction boundary.

WHY THIS EXISTS. A recurring documentation shape in this store is

    `0051F9F0` (380 B window) is the descriptor writer's arm cluster ...
    Interior anchor `0051F9F2` (the `movups` arm head).

The anchor is the one address a later reader can check the paragraph against. On 2026-09-18 OPUS
read `0051F9F0`'s 380 bytes while closing `RenderModelInstance`'s lifetime and found **no SSE
instruction anywhere in the body** - and `0051F9F2` is not an instruction at all: the entry
instruction `48895c2408` spans `0051F9F0`-`0051F9F4`, so the quoted anchor sits two bytes INSIDE it.

That is the whole signal. **x86-64 is not self-synchronising**: start one or two bytes late and the
decoder produces a fluent, plausible, entirely fictional instruction stream - which is exactly what
a paragraph describing `movups` arms in a function containing only integer moves looks like. An
anchor that is not a boundary is evidence the prose was written from a misaligned decode.

WHAT IT DOES NOT DO. A boundary anchor does NOT make a paragraph right: `001823B0`'s anchor
`001823B9` is a real `test rax, rax`, and the paragraph around it still describes a `mod-4` index
sequence that the 46-byte body does not contain. This check screens for one specific, mechanical,
high-confidence failure; it never certifies prose.

    python check_interior_anchors.py --self-test    controls, no corpus needed
    python check_interior_anchors.py                census the whole database
    python check_interior_anchors.py --db <dir>

CONTROLS, and why they are these two. `004090A3` is a boundary (it is the key load its own paragraph
claims) and must pass; `0051F9F2` is mid-instruction and must fail. One of each, from the same
document, written by the same pass on the same day - so the check is separating the two cases that
actually occur, not a synthetic pair.
"""
import argparse
import os
import re
import struct
import sys

import kit_paths as KP
import uc1_band

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
except ImportError:
    sys.stderr.write("check_interior_anchors: needs capstone (pip install capstone)\n")
    raise SystemExit(2)

EXE = os.path.join(KP.WORK, "exe", "FFXII_TZA.exe")
GRAPH = os.path.join(KP.WORK, "graph", "functions.tsv")

ANCHOR = re.compile(r"[Ii]nterior anchor\s+`?([0-9A-F]{6,8})`?")

# A paragraph that REFUTES an anchor has to quote it, so without this the check flags its own
# corrections for ever - the same self-reference `check_stale_reasons` had to grow a skip for. The
# marker must be in the SAME paragraph, so a refutation elsewhere in a document excuses nothing.
#
# THE MARKERS ARE DELIBERATELY NARROW, and the first draft of this list was wrong. It included the
# bare phrase "mid-instruction", which silently excused FOUR real findings: those paragraphs say, of
# their own subject, "the window opens mid-instruction". **That is the defect announcing itself, not
# a refutation.** A pass that knew its decode was misaligned and published the description anyway is
# the worst case this check exists for, so an author's own caveat must never suppress the flag.
REFUTED = re.compile(r"REFUTED|WITHDRAWN|CORRECTED|is not an instruction|"
                     r"not an instruction boundary", re.I)


def paragraph_at(text, pos):
    """The blank-line-delimited paragraph containing `pos`."""
    start = text.rfind("\n\n", 0, pos)
    start = 0 if start < 0 else start + 2
    end = text.find("\n\n", pos)
    end = len(text) if end < 0 else end
    return text[start:end]


class Image(object):
    def __init__(self, path):
        d = open(path, "rb").read()
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        opt = struct.unpack_from("<H", d, pe + 20)[0]
        self.base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
        self.secs = []
        for i in range(nsec):
            o = pe + 24 + opt + i * 40
            vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
            self.secs.append((va, vsz, ptr, rsz))
        self.d = d

    def read(self, va, n):
        r = va - self.base
        for sva, vsz, ptr, rsz in self.secs:
            if sva <= r < sva + rsz:
                avail = rsz - (r - sva)
                return self.d[ptr + (r - sva):ptr + (r - sva) + min(n, avail)]
        return None


def load_functions():
    fns = []
    with open(GRAPH, encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            try:
                entry = int(f[0], 16)
                size = int(f[2])
            except (ValueError, IndexError):
                continue
            if size > 0:
                fns.append((entry, size, f[1]))
    # UC-1 band (2026-09-28): the shared census is always the input.
    _b = uc1_band.load()
    fns = [(e, s, n) for e, s, n in fns if e not in _b["removed"]]
    fns = [(e, _b["extend"].get(e, e + s) - e, n) for e, s, n in fns]
    fns += [(st, sz, "UC1-FRONTIER-%08X" % st)
            for st, sz in _b["frontier"].items()]
    fns.sort()
    return fns


def owner_of(fns, addr):
    lo, hi = 0, len(fns) - 1
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if fns[mid][0] <= addr:
            best = fns[mid]
            lo = mid + 1
        else:
            hi = mid - 1
    if best and best[0] <= addr < best[0] + best[1]:
        return best
    return None


def boundaries(img, md, entry, size):
    """The set of instruction start addresses decoding forward from the entry."""
    code = img.read(entry, size)
    if not code:
        return None
    out = set()
    for ins in md.disasm(code, entry):
        out.add(ins.address)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    img = Image(a.exe)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fns = load_functions()

    if a.self_test:
        ok = True
        for addr, want_boundary, why in ((0x004090A3, True, "the key load its paragraph names"),
                                         (0x0051F9F2, False, "two bytes inside the entry push")):
            fn = owner_of(fns, addr)
            if fn is None:
                print("  %08X  CONTROL BROKEN: not inside any known function" % addr)
                ok = False
                continue
            bs = boundaries(img, md, fn[0], fn[1])
            got = addr in bs
            good = (got == want_boundary)
            ok = ok and good
            print("  %08X  boundary=%-5s expected=%-5s  %s  %s"
                  % (addr, got, want_boundary, "ok" if good else "CONTROL BROKEN", why))
        # and the self-reference control: a paragraph that refutes an anchor must not be flagged,
        # while a paragraph that merely states one must still be.
        quoting = "Interior anchor `0051F9F2`, which is not an instruction at all."
        # the control that the first draft failed: an author's own caveat is not a refutation
        plain = "the window opens mid-instruction. Interior anchor `0051F9F2` (the first lea)."
        skipped = bool(REFUTED.search(paragraph_at(quoting, quoting.find("0051F9F2"))))
        still = bool(REFUTED.search(paragraph_at(plain, plain.find("0051F9F2"))))
        ok = ok and skipped and not still
        print("  a refuting paragraph is skipped             %s" % ("yes" if skipped else "BROKEN"))
        print("  a plain claim is still checked              %s" % ("yes" if not still else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    seen = []
    refuted = 0
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for m in ANCHOR.finditer(text):
                if REFUTED.search(paragraph_at(text, m.start())):
                    refuted += 1
                    continue
                addr = int(m.group(1), 16)
                line = text.count("\n", 0, m.start()) + 1
                seen.append((os.path.relpath(path, a.db).replace("\\", "/"), line, addr))

    cache = {}
    bad, unmapped, good = [], [], 0
    for rel, line, addr in seen:
        fn = owner_of(fns, addr)
        if fn is None:
            unmapped.append((rel, line, addr))
            continue
        key = fn[0]
        if key not in cache:
            cache[key] = boundaries(img, md, fn[0], fn[1])
        bs = cache[key]
        if bs is None:
            unmapped.append((rel, line, addr))
        elif addr in bs:
            good += 1
        else:
            bad.append((rel, line, addr, fn))

    if not a.quiet:
        for rel, line, addr, fn in bad:
            print("MID-INSTRUCTION  %08X  in %s (%08X, %d B)" % (addr, fn[2], fn[0], fn[1]))
            print("    %s:%d" % (rel, line))
        if bad:
            print()
        for rel, line, addr in unmapped:
            print("UNMAPPED         %08X  %s:%d" % (addr, rel, line))
        if unmapped:
            print()

    print("interior anchors checked : %d" % len(seen))
    print("on an instruction boundary: %d" % good)
    print("MID-INSTRUCTION           : %d" % len(bad))
    print("not inside a known body   : %d" % len(unmapped))
    print("skipped, already refuted  : %d" % refuted)
    print()
    print("A mid-instruction anchor means the prose around it was written from a misaligned decode:")
    print("x86-64 resynchronises, so a late start yields a fluent but fictional instruction stream.")
    print("A boundary anchor is NOT a certificate - it only removes this one failure mode.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
