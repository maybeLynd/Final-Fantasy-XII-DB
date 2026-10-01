#!/usr/bin/env python3
"""check_literal_citations.py - a sentence calls an address a STRING; do the bytes there say so?

WHY THIS EXISTS. `verify_doc_addresses.py` checks that a cited address RESOLVES - that it lands in a
real section, on a function entry or inside a body. It does not check that the address resolves to
the KIND of thing the sentence says it is, and it should not: that is a different question, and
making one instrument answer both changes what a green run from it means.

`OPUS-FINDING-VERIFY-DOC-ADDRESSES-CHECKS-RESOLUTION-NOT-KIND` measured the gap on a real defect. A
page said *"the literal `btlKeepCharWork1`/`btlKeepCharWork2` strings live at 007F46B8 / 007F46D0"*.
Both numbers were **the canonical `.rdata` address with the image base subtracted a second time** -
the error class that lands on a plausible `.text` address rather than on nothing.
`verify_doc_addresses` returned `ok, 134 cited`, classified one as a function entry and the other as
interior to a body, **which is exactly what they are**, and printed `0 document(s) ... to confirm`.
Nothing was wrong with that run. The question was never asked.

THE RULE IS TWO FACTORS, AND NEITHER WORKS ALONE. That is not a design preference; it is what four
measurements against this corpus showed.

    trigger                                          candidates   fired   useful
    any string-ish word on the line                       4,456   4,245   no - 95 % false
    word + preposition + address, tight window              124      63   no - 51 % false
    arithmetic alone: A+0x120000 decodes as a string    154,909   8,302   no - .rdata is
                                                                          packed with paths
    BOTH: sentence says string, bytes there are not,
          and A+0x120000 IS a string                        ---     ---   this file

The first three are recorded because a rule that has been priced is worth more than one that has
been asserted, and because the next person to propose a prose heuristic here should see the numbers
first. The loose trigger's misses were all one shape - the word describing something other than the
address: *"lea a **literal data base**"* where the addresses are functions, *"region strings, the
`00553AE0` MapName pane"*, and best of all `api-ms-win-crt-string-l1-1-0.dll!strcpy_s`, where the
word is inside a DLL name.

FOUR CALIBRATIONS THAT COST A ROUND EACH, every one my own error rather than the corpus's. The
first corpus run flagged four candidates and **all four were false**; the two below them are why:

* **`minlen` on the cited side must be 1.** At 4 it rejected `"%s"`, `"jp"` and `"\\"` - real strings
  the corpus cites correctly - and reported all three as defects. Any printable NUL-terminated run
  is a string.
* **`literal` is not a string word.** It matched `128.0 a literal at 008F3A2C`, which is a float
  constant and reads as one. Only `string`/`strings`/`asciiz`/`NUL-terminated` trigger now.
* **A log or error string contains `\n`.** Restricting "printable" to 0x20-0x7E rejected three
  correct pages at once - `009038C8` *"BigFile head wro..."*, `00D9F498` *"==== TEXSHADERSE..."* and
  `00D6FEB0` *"execute: lua_pcall failed - error code: %d"*. The post-processing page had said so in
  the very line I flagged: *"all four verbatim, `\n` and all"*. 0x09/0x0A/0x0D are text.
* **The `+0x120000` twin must land on a string START.** `007DE328` is `.text` - `4C 8D 0D ...`, the
  `lea` that loads the string, which is what its page means by *"the string at 007DE328-007DE349"*.
  Its twin `008FE328` decoded as `'ter Clamp Modifier: '`, i.e. the tail of `...Filter Clamp
  Modifier: `. A doubled subtraction of a string's start lands on a start; landing mid-run is
  coincidence, and `.rdata` is large enough that coincidence is common.

AFTER ALL FOUR the corpus is clean: 80 addresses a sentence calls a string, 0 with the shape. That
is a **zero from a rule calibrated against four of its own false positives**, not a zero from a rule
that was never exercised - which is the only reason the zero is worth anything. The defect the
notice was filed on is not in the tree; it was corrected before this instrument existed. The value
here is that the class is now checkable, and this file is the record of what the check costs.

    python check_literal_citations.py --self-test
    python check_literal_citations.py
    python check_literal_citations.py --db <dir> --quiet

CONTROLS are the notice's own measured pair: `009146B0`/`009146B8`/`009146D0` decode as `BtlWork`,
`btlKeepCharWork1`, `btlKeepCharWork2` and must pass; `007F46B8` and `007F46D0` must fail, the second
decoding as the prologue bytes `40 53 48 83 EC 20`, and both must show the +0x120000 signature.

THE SELF-REFERENCE GUARD WAS HERE IN THE FIRST VERSION, because five other checks in this kit needed
one retrofitted: a page that RECORDS a withdrawn address necessarily quotes it.
"""
import argparse
import os
import re
import struct
import sys

import kit_paths as KP

EXE = os.path.join(KP.WORK, "exe", "FFXII_TZA.exe")
IMAGE_BASE = 0x00120000

#: Factor one. A string noun, a locating preposition, then the address, in a short window.
SAYS_STRING = re.compile(
    r"\b(?:strings|string|asciiz|NUL-terminated)\b"
    r"[^.;]{0,48}?"
    r"\b(?:live at|lives at|resides at|reside at|sits at|sit at|stored at|packed at|at)\b"
    r"[^.;]{0,24}?([0-9A-F]{8})\b", re.I)

#: Written before the first run, not after it.
REFUTED = re.compile(r"REFUTED|WITHDRAWN|CORRECTED|not a string|is NOT at|was wrong|"
                     r"double-subtract|subtracted a second time|the withdrawn", re.I)


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
            name = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
            self.secs.append((name, va, vsz, ptr, rsz))
        self.d = d

    def at(self, va, n=72):
        r = va - self.base
        for name, sva, vsz, ptr, rsz in self.secs:
            if sva <= r < sva + rsz:          # rsz: initialised raw data only
                avail = rsz - (r - sva)
                return name, self.d[ptr + (r - sva):ptr + (r - sva) + min(n, avail)]
        return None, None


def printable(c):
    """A log or error string is text. 0x0A/0x0D/0x09 are text; excluding them cost a round."""
    return 32 <= c < 127 or c in (0x09, 0x0A, 0x0D)


def decodes_as_string(img, va, minlen=1):
    """(ok, why) - does `va` hold a printable NUL-terminated string of at least `minlen`?"""
    name, b = img.at(va)
    if not b:
        return False, "not inside any section with initialised raw data"
    s = b.split(b"\x00")[0]
    if len(s) < minlen:
        return False, "%s: no string here (first byte 0x%02X)" % (name, b[0])
    if not all(printable(c) for c in s):
        return False, "%s: not printable - %s" % (name, " ".join("%02X" % c for c in b[:6]))
    return True, "%s: %r" % (name, s.decode("ascii"))


def starts_a_string(img, va):
    """Is `va` the FIRST byte of its string? A doubled subtraction of a string's start lands on a
    start; landing mid-run is coincidence, which is how `007DE328` -> `'ter Clamp Modifier: '`
    (interior to `...Filter Clamp Modifier: `) reached the report as a defect."""
    _name, prev = img.at(va - 1, 1)
    return bool(prev) and prev[0] == 0x00


def signature(img, va):
    """The defect: the sentence says string, the bytes are not, but base+0x120000 they are."""
    here, _why = decodes_as_string(img, va, minlen=1)
    if here:
        return None
    there, why = decodes_as_string(img, va + IMAGE_BASE, minlen=6)
    if not there or not starts_a_string(img, va + IMAGE_BASE):
        return None
    return why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = Image(a.exe)

    if a.self_test:
        ok = True
        for va, want, why in ((0x009146B0, True, "BtlWork"),
                              (0x009146B8, True, "btlKeepCharWork1"),
                              (0x009146D0, True, "btlKeepCharWork2"),
                              (0x007F46B8, False, "the double-subtracted address"),
                              (0x007F46D0, False, "decodes as the prologue 40 53 48 83 EC 20")):
            got, _d = decodes_as_string(img, va)
            good = (got == want)
            ok = ok and good
            print("  %08X  %-5s expected %-5s  %s  %s"
                  % (va, got, want, "ok" if good else "BROKEN", why))
        for va in (0x007F46B8, 0x007F46D0):
            sig = signature(img, va)
            ok = ok and bool(sig)
            print("  %08X  +0x120000 signature %-22s %s"
                  % (va, "FIRES" if sig else "MISSING", sig or ""))
        # the short strings a minlen of 4 wrongly rejected
        for va, txt in ((0x008F4438, '"%s"'), (0x008C5904, '"jp"'), (0x009047A4, r'"\\"')):
            got, _d = decodes_as_string(img, va)
            ok = ok and got
            print("  %08X  short string %-6s accepted            %s" % (va, txt, "yes" if got else "BROKEN"))
        # log/error strings carry newlines; excluding 0x0A reported three correct pages as defects
        for va, txt in ((0x009038C8, "BigFile head... (error)"),
                        (0x00D9F498, "==== TEXSHADERSE... (log)"),
                        (0x00D6FEB0, "execute: lua_pca... (fmt)")):
            got, _d = decodes_as_string(img, va)
            ok = ok and got
            print("  %08X  newline-bearing %-26s accepted  %s" % (va, txt, "yes" if got else "BROKEN"))
        # the +0x120000 twin must land on a string START, not inside one
        mid = starts_a_string(img, 0x008FE328)
        ok = ok and not mid
        print("  008FE328 ('ter Clamp Modifier: ') seen as interior  %s" % ("yes" if not mid else "BROKEN"))
        for va in (0x009146B8, 0x009146D0):
            st = starts_a_string(img, va)
            ok = ok and st
            print("  %08X is seen as a string start                 %s" % (va, "yes" if st else "BROKEN"))
        t = "the literal `btlKeepCharWork1`/`btlKeepCharWork2` strings live at 007F46B8 / 007F46D0"
        fires = [m.group(1) for m in SAYS_STRING.finditer(t)]
        print("  the defect sentence is picked up                %s"
              % ("yes " + str(fires) if fires else "BROKEN"))
        ok = ok and bool(fires)
        for nm, s in (("a literal DATA BASE (float/functions)",
                       "`0036E320` and `0036E540` lea a literal data base and index it"),
                      ("a float literal at an address",
                       "`128.0` a literal at 008F3A2C, used twice"),
                      ("the word inside a DLL name",
                       "`008C3038` api-ms-win-crt-string-l1-1-0.dll!strcpy_s")):
            q = bool(SAYS_STRING.search(s))
            ok = ok and not q
            print("  quiet on %-40s %s" % (nm, "yes" if not q else "BROKEN"))
        skip = bool(REFUTED.search("WITHDRAWN: 007F46B8 was the address subtracted a second time"))
        ok = ok and skip
        print("  a line recording a withdrawal is skipped        %s" % ("yes" if skip else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    checked = bad = skipped = 0
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, a.db).replace("\\", "/")
            if rel.startswith("_index/_inbox/"):
                continue
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                hits = list(SAYS_STRING.finditer(line))
                if not hits:
                    continue
                if REFUTED.search(line):
                    skipped += 1
                    continue
                for m in hits:
                    va = int(m.group(1), 16)
                    checked += 1
                    sig = signature(img, va)
                    if not sig:
                        continue
                    bad += 1
                    if not a.quiet:
                        print("DOUBLE-SUBTRACTED BASE?  %08X" % va)
                        print("    %s:%d" % (rel, i))
                        print("    %s" % line.strip()[:110])
                        print("    not a string here, but %08X is %s" % (va + IMAGE_BASE, sig))

    print()
    print("addresses a sentence calls a string : %d" % checked)
    print("  with the double-subtraction shape : %d" % bad)
    print("  lines skipped as already refuted  : %d" % skipped)
    print()
    print("TWO FACTORS, because neither works alone: prose alone was 95 % false at the loose")
    print("width and 51 % at the tight one, and the arithmetic alone fires on 8,302 of 154,909")
    print("cited .text addresses because .rdata is packed with path strings. A flag here is a")
    print("CANDIDATE - the bytes agree with the error's shape, and a reader confirms the claim.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
