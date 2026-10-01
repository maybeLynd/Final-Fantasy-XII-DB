#!/usr/bin/env python3
"""The ONE pattern for "this page quotes decompiler state". Import it; do not retype it.

WHY THIS FILE EXISTS, and it is not a style preference.

`EVIDENCE-STANDARD.md` has named the token set since FABLE's transfer ruling
(OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144, 9bedb5e0): `DAT_`, `param_`, `local_`, `undefined`,
`PTR_`, a cast. The set is not the problem. The problem is that a sweep gets written in a hurry
and its author types a pattern from memory, which comes out NARROWER than the canonical one and
clears documents that are not clear:

  1st time  OPUS-REQ-ASTRA-NONFUNCTION-ANNOTATION-EXPORT records it in its own known_evidence:
            "an earlier narrower pattern of mine wrongly cleared one."
  2nd time  2026-09-14, OPUS again: a sweep matching only `(FUN|DAT|LAB|PTR|UNK|SUB)_<hex>`
            reported SIX of the 53 stale-provenance documents as quoting nothing. Re-tested
            against the full set, ALL SIX quote decompiler state - `param_1`, `bVar1`,
            `undefined1`, `(int *)`. The six were about to be treated as unblocked work.

A pattern that lives in prose gets retyped. A pattern that lives in a module gets imported.

WHAT THE ANSWER MEANS. Unchanged from the standard, and it cuts one way only:

    Token absence SUPPORTS a transfer; it does not PROVE one. A page that happens not to write
    `DAT_` may still rest on a decompilation. This is a filter for who must be re-read, never a
    certificate.

So `quotes_decompiler_state(text) == True` is load-bearing and `== False` is a hint.
"""
import re

# FABLE's full set. Each entry witnesses decompiler output, which depends on the non-function
# symbol table, the data type manager, instruction comments, equates and reference overrides -
# none of which the function census or GFZFunctionAnnotationSnapshotV2 captures.
PATTERNS = (
    # Ghidra's default names for functions, data, labels, pointers and unknowns
    ("auto-name", re.compile(r"\b(?:FUN|DAT|LAB|PTR|UNK|SUB)_[0-9A-Fa-f]{4,}\b")),
    # decompiler-invented parameter and local names
    ("param_", re.compile(r"\bparam_\w+\b")),
    ("local_", re.compile(r"\blocal_\w+\b")),
    # decompiler-invented temporaries: uVar1, iVar2, bVar1, auVar3 ...
    ("xVar", re.compile(r"\b[a-z]{1,3}Var\d+\b")),
    # the DTM's placeholder type, including undefined4 / undefined8
    ("undefined", re.compile(r"\bundefined\d*\b")),
    # decompiler-emitted casts
    ("cast", re.compile(r"\((?:undefined|u?int\d*|char|short|long|byte|word|dword|qword)"
                        r"\d*\s*\*?\s*\)")),
    # registers the decompiler could not resolve
    ("in_/unaff_/extraout_", re.compile(r"\b(?:in|unaff|extraout)_\w+\b")),
)


def decompiler_tokens(text):
    """-> [(kind, count, first_example)] for every token class present."""
    out = []
    for kind, rx in PATTERNS:
        hits = rx.findall(text)
        if hits:
            out.append((kind, len(hits), hits[0]))
    return out


def quotes_decompiler_state(text):
    """True if the text quotes decompiler output. True is load-bearing; False is a hint."""
    return any(rx.search(text) for _k, rx in PATTERNS)


def _self_test():
    """The six false clears of 2026-09-14, as a regression test with their real tokens."""
    must_match = [
        ("param_1", "the callee reads `param_1` and returns"),
        ("bVar1", "`bVar1` is set when the compare succeeds"),
        ("undefined1", "the field is typed `undefined1` in the DTM"),
        ("(int *)", "the value is used as `(int *)` here"),
        ("(uint16)", "truncated with a `(uint16)` cast"),
        ("FUN_00385BA0", "`FUN_00385BA0` is the applier"),
        ("DAT_02EBF138", "reads `DAT_02EBF138`"),
        ("uVar3", "`uVar3` accumulates the total"),
        ("in_EDI", "`in_EDI` is unresolved"),
    ]
    must_not = [
        "`00385BA0` reads the word at `+0x32` and stores it",
        "The table at `0215F000` holds 41 slots, each 8 bytes.",
        "BattleFormula_ResolveTargetResult is the GZF name for this body.",
    ]
    bad = 0
    for label, text in must_match:
        if not quotes_decompiler_state(text):
            print("  FAIL: %-14s not matched -- %s" % (label, text))
            bad += 1
    for text in must_not:
        if quotes_decompiler_state(text):
            print("  FAIL: matched clean prose -- %s" % text)
            bad += 1
    if bad:
        print("self-test FAILED: %d case(s). Negatives from this module are not trustworthy." % bad)
        return 1
    print("self-test passed: %d positive, %d negative" % (len(must_match), len(must_not)))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
