"""apply.py [--apply] - insert FABLE's registration event-0 clause on the-box-renderer-that-is-never-called.md, after the
`00296360` paragraph's interior-anchor line (FABLE, 2026-10-03, on ASTRA-REQ-FABLE-OV42-REGISTER-EVENT0-1003 after
SWE2-AUDIT-SPEC's ACCEPT of ASTRA's ov42-register-event0 evidence, review commit bff21d191).

Anchored on one unique line; refuses a page with content changes (an EOL-only difference is allowed), with ONE named
exception: the pending sibling edit fable-ov42-handler-edge-1003 (its exact OLD -> NEW substitution on the UI crossing
line) may already be applied - the page must then equal HEAD with exactly that substitution. Line endings are kept.
Idempotent (ALREADY when the clause is present). Dry run unless --apply. Prints FAILS N last."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REL = "99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md"
P = os.path.normpath(os.path.join(HERE, "..", "..", "..", *REL.split("/")))

ANCHOR = "Interior anchor `002963E7` (function `00296360`)."

CLAUSE = (
    "*Registration does not start a bar update through these two callbacks (FABLE, 2026-10-03, on "
    "ASTRA-REQ-FABLE-OV42-REGISTER-EVENT0-1003 after SWE2-AUDIT-SPEC's ACCEPT; record "
    "[`fable-ov42-event0-consumption-1003`](../../_index/candidates/fable-ov42-event0-consumption-1003/README.md)):* "
    "`003F89C0` zeroes the `0x58`-byte record and then fills it itself - bit 0 of word `+0x26` (`003F89EF`), the "
    "fifth-argument callback at `+0x38` (`003F89F4`), the third-argument dword at `+0x40` (`003F89F8`) and the "
    "fourth-argument context at `+0x48` (`003F89FB`) - and only then calls a non-null callback synchronously with "
    "`rcx` = the record, `edx` = 0 and `r8` = its zero-extended second argument (`003F8A04`-`003F8A0C`). At this "
    "event 0 both prescribed handlers return 0 with no bar update: each first reads the qword at `+0x48` of `rcx` "
    "(`0029B7D7`, `0029B814`), before any test of `edx`; then `0029B7D0` branches at `0029B7DE` and `0029B810` at "
    "`0029B823` (`edx` - 1 is neither 0 nor 1) to `xor eax,eax` / `ret` (`0029B7FB`, `0029B82F`), with no call, no "
    "memory write and no use of the loaded context or of `r8`. The bar update is event 1 only (the rows below). "
    "The `+0x48` read is unconditional, so a bad record pointer can still fault at event 0. Evidence: ASTRA's "
    "[`ov42-register-event0`](../../_experiments/evidence/ov42-register-event0/README.md) (commit `0d55f8417`, a "
    "static path proof, nothing executed). Still OPEN: which callback a matched `00297C10` row keeps at `+0x38` (that "
    "path skips `003F89C0`), the record's natural initialisation, scheduling, lifetime and the first draw."
)

SIB_OLD = "and the installed callbacks `0029B7D0`/`0029B810` are themselves called by UI's `002973E0`"
SIB_NEW = ("and the installed callbacks `0029B7D0`/`0029B810` ~~are themselves called by UI's `002973E0`~~ themselves call "
           "UI's `002973E0` (at `0029B7EA` and `0029B851`; `002973E0` reaches neither handler) *(corrected 2026-10-03, "
           "FABLE, on ASTRA-REQ-FABLE-OV42-GAUGE-BINDING-1003 and SWE2-AUDIT-SPEC's ACCEPT of its evidence; "
           "[`fable-ov42-handler-edge-1003`](../../_index/candidates/fable-ov42-handler-edge-1003/README.md))*")


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=os.path.dirname(P), capture_output=True).stdout


def head_text():
    top = git("rev-parse", "--show-toplevel").decode().strip()
    rel = os.path.relpath(P, top).replace("\\", "/")
    return git("show", "HEAD:" + rel).decode("utf-8").replace("\r\n", "\n")


def patch(t):
    """Return (status, new_text) for LF-normalised page text t."""
    if CLAUSE in t:
        return "ALREADY", t
    n = t.count(ANCHOR + "\n")
    if n != 1:
        return "MISS anchor (%d)" % n, None
    return "OK", t.replace(ANCHOR + "\n", ANCHOR + "\n\n" + CLAUSE + "\n", 1)


def main():
    fails = 0
    raw = io.open(P, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    t = raw.replace("\r\n", "\n")
    num = git("diff", "--numstat", "--", P).decode().strip()
    if num:
        h = head_text()
        if t == h.replace(SIB_OLD, SIB_NEW, 1) and h.count(SIB_OLD) == 1:
            print("NOTE  content diff is exactly the pending sibling fable-ov42-handler-edge-1003 edit; allowed")
        elif patch(h)[1] is not None and t in (patch(h)[1], patch(h.replace(SIB_OLD, SIB_NEW, 1))[1]):
            pass  # our own clause already applied (with or without the sibling); idempotent path below
        else:
            print("REFUSED: content changes on the page:", num)
            print("FAILS 1")
            return 1
    st, new = patch(t)
    if st == "ALREADY":
        print("ALREADY")
    elif new is None:
        print(st)
        fails += 1
    elif "--apply" in sys.argv:
        io.open(P, "w", encoding="utf-8", newline="").write(new.replace("\n", nl))
        print("PATCHED (%s line endings kept)" % ("CRLF" if nl == "\r\n" else "LF"))
    else:
        print("WOULD PATCH: insert 1 paragraph after the line %r (%s line endings kept)"
              % (ANCHOR, "CRLF" if nl == "\r\n" else "LF"))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
