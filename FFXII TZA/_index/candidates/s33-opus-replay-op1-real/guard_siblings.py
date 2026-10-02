"""guard_siblings.py [--apply] - put the S-33 upstream verdict guard into the eight sibling replays that import an
upstream check the same unguarded way (OPUS, 2026-10-01, follow-up to ASTRA-REQ-OPUS-S33-UPSTREAM-VERDICT-GUARD-1001).

Each sibling gets, right after its upstream import (after the os.chdir back, when there is one), a call to
upstream_guard.verdict(C) that exits 2 with REFUSED unless the upstream's allok is True and every case passed.
The guard module is appended to sys.path, so the sibling's own upstream directory stays first and `import check`
still resolves to it (checked here with importlib.util.find_spec). Dry run by default; idempotent; FAILS n.
"""
import ast
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
SIBLINGS = ["s20-opus-replay-commit", "s25-opus-commit-refusal-unreachable", "s26-opus-replay-status-write",
            "s30-opus-replay-bazaar-shipped", "s36-opus-replay-arbiter-input-gate", "s40-opus-replay-post-process-init",
            "s45-opus-replay-counters", "s45-opus-replay-steam-manager"]
MARK = "upstream_guard.verdict(C)"
BLOCK = [
    "# THE UPSTREAM'S VERDICT GATES THIS REPLAY (2026-10-01, OPUS): the import used to be trusted, so an upstream that",
    "# printed FAIL still let every case below run. Same guard as s33-opus-replay-op1-real (upstream_guard.py, tested there).",
    "sys.path.append(os.path.normpath(os.path.join(HERE, \"..\", \"s33-opus-replay-op1-real\")))",
    "import upstream_guard                                     # noqa: E402",
    "_ok, _why = upstream_guard.verdict(C)",
    "if not _ok:",
    "    print(\"REFUSED: %s\" % _why)",
    "    sys.exit(2)",
]


def upstream_dir(src_lines):
    """The directory the sibling inserts at sys.path[0] before importing check (BASE or D or an inline join)."""
    env = {"os": os, "HERE": None}
    for l in src_lines:
        s = l.strip()
        if s.startswith(("BASE = ", "D = ")) and "os.path" in s:
            return s.split("=", 1)[1].strip()
        if s.startswith("sys.path.insert(0, os.path") and "s2" in s or s.startswith("sys.path.insert(0, os.path") and "s3" in s:
            return s[len("sys.path.insert(0, "):-1]
    return None


def main():
    apply = "--apply" in sys.argv
    fails = 0
    for d in SIBLINGS:
        p = os.path.join(CAND, d, "check.py")
        raw = open(p, "rb").read()
        crlf = b"\r\n" in raw
        lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
        if MARK in raw.decode("utf-8"):
            print("ALREADY", d)
            continue
        idx = [i for i, l in enumerate(lines) if l.strip().startswith("import check as C")]
        if len(idx) != 1:
            print("REFUSING", d, "import lines:", len(idx)); fails += 1; continue
        i = idx[0]
        j = i + 1 if lines[i + 1].strip() == "os.chdir(cwd)" else i
        if lines[j].startswith((" ", "\t")):
            print("REFUSING", d, "insertion point is indented"); fails += 1; continue
        new = lines[:j + 1] + BLOCK + lines[j + 1:]
        text = "\n".join(new)
        ast.parse(text)
        # module resolution as the sibling sets it up: its upstream first, the guard directory appended
        up = upstream_dir(lines)
        updir = eval(up, {"os": os, "HERE": os.path.join(CAND, d)}) if up else None
        saved = list(sys.path)
        try:
            sys.path.insert(0, updir)
            sys.path.append(os.path.join(CAND, d, "..", "s33-opus-replay-op1-real"))
            sys.modules.pop("check", None)
            spec_c = importlib.util.find_spec("check")
            spec_g = importlib.util.find_spec("upstream_guard")
        finally:
            sys.path[:] = saved
        okres = (spec_c and os.path.normcase(os.path.dirname(spec_c.origin)) == os.path.normcase(os.path.normpath(updir))
                 and spec_g and os.path.basename(os.path.dirname(spec_g.origin)) == "s33-opus-replay-op1-real")
        if not okres:
            print("REFUSING", d, "resolution:", spec_c and spec_c.origin, spec_g and spec_g.origin); fails += 1; continue
        if apply:
            out = text.replace("\n", "\r\n") if crlf else text
            open(p, "wb").write(out.encode("utf-8"))
            print("PATCHED", d, "after line", j + 1, "upstream", os.path.basename(updir))
        else:
            print("WOULD PATCH", d, "after line", j + 1, "upstream", os.path.basename(updir))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
