#!/usr/bin/env python3
"""check_arithmetic.py - pass 18: recompute the arithmetic this corpus argues with.

**THE CORPUS PROVES LAYOUTS WITH ARITHMETIC AND NOTHING CHECKS THE ARITHMETIC.** "64 x `0x58` =
`0x1600`, and `0x2328 + 0x1600 = 0x3928`, exactly the offset of the index dword" is a real proof -
stride, count and index position confirming each other - and it is worthless if the multiplication
is wrong. The form is everywhere: an extent closing on a boundary, an element count times a width, a
region start plus a size landing on its neighbour.

`check_denominators.py` (percentages with no stated denominator) and `check_counts.py` (a stated
count against a tabulated one) cover pass 18's neighbourhood. Neither evaluates an expression.

WRITTEN BECAUSE IT CAUGHT ITS AUTHOR. On 2026-09-19 I wrote `0xD0 + 45 x 0xD0 = 0x2490` into a
narrowing of an 8,728-byte span. It is `0x2560`; the count is 44, not 45. A whole array hypothesis
rested on that line, and it was caught only by printing the comparison instead of asserting it.

**SCOPE: CODE SPANS ONLY, AND THAT NARROWING IS THE WHOLE INSTRUMENT.** A first version read running
prose and returned **90 findings, none of them real**. Every one came from the notation rather than
the mathematics:

* **bare hex.** This corpus writes addresses unprefixed - `01EEBCC0 + 0x38 = 01EEBCF8` is correct and
  a decimal reader sees `0 + 0x38 = 01`.
* **table cells.** Adjacent columns weld into sums: `39 + 8 + 76 = 377` was three separate cells.
* **wrapped expressions.** `51 + 111 + 92 + 39 + 8 + 76 = 377` is correct and spans a line break, so
  splitting on newlines to defeat the table problem cut this one in half and flagged the remainder.
* **percentages.** `38,161 / 38,161 = 100.00000 %` is not a quotient.
* **offset notation.** `+0x38` is a displacement, not an addition.

Prose cannot be disambiguated from the outside, so this checks only what is written **inside a single
backtick span** - which is where this corpus puts its load-bearing arithmetic anyway, because that is
how it writes offsets and sizes. What it gives up is real: a correct-looking sum in running text is
NOT checked, and pass 18 is not satisfied by this tool alone.

    python check_arithmetic.py --self-test
    python check_arithmetic.py
"""
import argparse
import io
import os
import re
import sys

import kit_paths as KP

CODE_SPAN = re.compile(r"`([^`\n]{3,120})`")
STRUCK = re.compile(r"~~.*?~~", re.S)
# A literal: 0x hex, a bare 4-8 digit hex address, comma-grouped decimal, or plain decimal.
# NO TRAILING \s* ON THE TOKEN. It used to consume the separator, which left the operator pattern
# unable to see whether there was a space before `+` - and that silently disarmed the whole check:
# the seed case this tool was written for came back clean.
TOKEN = re.compile(r"(0[xX][0-9A-Fa-f]+|[0-9A-Fa-f]{4,8}|\d{1,3}(?:,\d{3})+|\d+)")
# `A+B` and `A + B` are sums; `A +B` is this corpus's offset notation (`0209BE80 +0x10FA2`) and is
# NOT. The bare `\+` alternative can only fire immediately after a literal, so it is the glued form.
OP = re.compile(r"(?:\s+(x)\s+|\s*(\*|×|∗|/)\s*|\s+(\+)\s+|(\+))")


def value(tok):
    """AN EIGHT-DIGIT TOKEN IS AN ADDRESS, EVEN WHEN IT IS ALL DIGITS.

    `00120000 + 0x7F64D0 = 009164D0` is correct, and reading `00120000` as decimal 120,000 made it
    look wrong - which is exactly the false accusation this checker must not make. This corpus writes
    every address as eight hex digits, so an 8-character token is hex whatever its digits are.
    """
    tok = tok.replace(",", "")
    if tok.lower().startswith("0x"):
        return int(tok, 16)
    if len(tok) == 8 and re.fullmatch(r"[0-9A-Fa-f]{8}", tok):
        return int(tok, 16)
    if re.fullmatch(r"\d+", tok):
        return int(tok)
    return int(tok, 16)          # a bare hex address such as 1EEBCC0


def parse(span):
    """(numbers, operators, rhs) if the span is exactly `A op B [op C ...] = R`, else None."""
    if "=" not in span:
        return None
    lhs, _, rhs = span.partition("=")
    m = TOKEN.fullmatch(rhs.strip())
    if not m:
        return None
    lhs = lhs.rstrip()
    nums, ops, pos = [], [], 0
    while pos < len(lhs):
        while pos < len(lhs) and lhs[pos].isspace():
            pos += 1
        if pos >= len(lhs):
            break
        mt = TOKEN.match(lhs, pos)
        if not mt:
            return None
        nums.append(mt.group(1))
        pos = mt.end()
        if pos >= len(lhs):
            break
        mo = OP.match(lhs, pos)
        if not mo:
            return None
        ops.append(next(g for g in mo.groups() if g))
        pos = mo.end()
    if len(ops) < 1 or len(nums) != len(ops) + 1:
        return None
    return nums, ops, m.group(1)


def apply(a, op, b):
    if op in ("x", "*", "×", "∗"):
        return a * b
    if op == "+":
        return a + b
    if op == "/":
        return a // b if b and a % b == 0 else None
    return None


def evaluate(nums, ops):
    """Standard precedence - multiplication binds tighter than addition.

    Left-to-right made `0xD0 + 44 x 0xD0` into `(0xD0 + 44) * 0xD0`, the same shape of error this
    checker exists to catch.
    """
    nums, ops = list(nums), list(ops)
    i = 0
    while i < len(ops):
        if ops[i] != "+":
            v = apply(nums[i], ops[i], nums[i + 1])
            if v is None:
                return None
            nums[i:i + 2] = [v]
            ops.pop(i)
        else:
            i += 1
    total = nums[0]
    for i, op in enumerate(ops):
        total = apply(total, op, nums[i + 1])
        if total is None:
            return None
    return total


def scan_text(t):
    """(span, expected, stated) for each backtick expression that does not reproduce."""
    out = []
    for m in CODE_SPAN.finditer(STRUCK.sub(" ", t)):
        span = m.group(1)
        p = parse(span)
        if not p:
            continue
        nums, ops, rhs = p
        try:
            v = evaluate([value(n) for n in nums], ops)
            r = value(rhs)
        except ValueError:
            continue
        if v is None or v == r:
            continue
        out.append((span.strip(), v, r))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        ok = True
        cases = [
            ("`0xD0 + 45 x 0xD0 = 0x2490`", False),   # the real error this was written for
            ("`0xD0 + 44 x 0xD0 = 0x2490`", True),    # the correction
            ("`64 x 0x58 = 0x1600`", True),
            ("`0x2328 + 0x1600 = 0x3928`", True),
            ("`0x7370 + 40*4 = 0x7410`", True),
            ("`0xC0 * 0x80 = 0x6000`", True),
            ("`01EEBCC0 + 0x38 = 01EEBCF8`", True),   # bare hex addresses
            ("`51 + 111 + 92 + 39 + 8 + 76 = 377`", True),   # n-ary sum
            ("`8,320 / 208 = 42`", False),            # 8320/208 is 40
            ("~~`23,312 x 2 = 1`~~ corrected", True),  # struck through
            ("38,161 / 38,161 = 100.00000 %", True),  # not in a code span at all
            ("`Lua 5.2.1 = 3`", True),                # not an expression
        ]
        for text, want_clean in cases:
            bad = scan_text(text)
            good = (len(bad) == 0) == want_clean
            ok = ok and good
            print("  %-40s %-8s %s" % (text[:40], "clean" if not bad else "FLAGGED",
                                       "ok" if good else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    findings, docs, checked = [], 0, 0
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            docs += 1
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for m in CODE_SPAN.finditer(STRUCK.sub(" ", t)):
                if parse(m.group(1)):
                    checked += 1
            for expr, expected, got in scan_text(t):
                findings.append((os.path.relpath(p, a.db), expr, expected, got))

    print("documents scanned                 : %d" % docs)
    print("backtick expressions evaluated    : %d" % checked)
    print("expressions that do not reproduce : %d" % len(findings))
    print()
    for path, expr, expected, got in findings[:40]:
        print("  %s" % path)
        print("      `%s`" % expr[:110])
        print("      computes to %d (0x%X), document says %d (0x%X)" % (expected, expected, got, got))
    if len(findings) > 40:
        print("  ... and %d more" % (len(findings) - 40))
    if not findings:
        print("  none - every backtick expression in the corpus reproduces")
    print()
    print("SCOPE: code spans only. Arithmetic written in running prose is NOT checked, because the")
    print("corpus's own notation - bare hex addresses, table cells, wrapped sums - cannot be told")
    print("from mathematics out of context. Pass 18 is not satisfied by this tool alone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
