#!/usr/bin/env python3
"""Subtree-section emitter for the exclusive-subtree frontier.

The ONLY legal way to append an exclusive-subtree binding section.
Computes the _index/ADDRESS-INDEX.md backlink prefix from the
receiving page's own directory depth -- the bug that kept PASS 29 red
was a hardcoded ../../ on pages at depth 1 and 3.

Usage:
    python subtree_emit.py PAGE_MD ROOT "header prose line" member1:desc member2:desc ...

Example:
    python subtree_emit.py "Database/FFXII TZA/18-Audio/sead-function-identification.md" \\
        007EAA60 "~926 B -- big SEH frame" "007F6FB0:the body"

The emitted section is appended to PAGE_MD. Run interior_cite and
check_links afterwards as usual.
"""
import os
import re
import sys

import kit_paths as KP

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

_STATED = re.compile(r"\(\s*[0-9,]+\s*B\s*\)")


def certified_sizes() -> dict:
    """Address -> body size from the certified function list.

    The published `(N B)` figures must agree with this list -- the defect
    OPUS census found (stated size measured to the terminator's start, or
    to a mid-body `ret`, or past the end into padding) only exists because
    each batch derived the figure by hand. The emitter now stamps it.
    """
    out = {}
    with open(FUNCS, encoding="utf-8", errors="replace") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            try:
                out[int(p[0], 16)] = int(p[2])
            except (ValueError, IndexError):
                pass
    return out


def index_prefix(page_path: str) -> str:
    """Depth of the page file under Database/FFXII TZA -> ../ prefix."""
    rel = os.path.relpath(os.path.abspath(page_path), DB).replace("\\", "/")
    depth = rel.count("/")  # directories between DB root and the file
    return "../" * depth + "_index/ADDRESS-INDEX.md"


def emit_section(page_path: str, root: str, prose: str,
                 members: list[str], shared: str = "none") -> str:
    """Return the markdown section. members: 'ADDR:description' pairs.

    The member cell's size is stamped from the certified function list.
    A `(N B)` figure inside the description that disagrees is corrected;
    one that agrees is left alone (it will simply not be duplicated).
    """
    prefix = index_prefix(page_path)
    sizes = certified_sizes()
    lines = [
        "",
        f"## The `{root}` exclusive subtree -- {len(members)} member(s) bound (SWE2-FRONTIER, followup queue)",
        "",
        prose,
        "",
        "| member | role | interior |",
        "| --- | --- | --- |",
    ]
    for spec in members:
        addr, _, desc = spec.partition(":")
        addr = _STATED.sub("", addr).strip().rstrip("`").strip().upper()
        desc = desc.strip()
        size = sizes.get(int(addr, 16))
        if size is None:
            print(f"warning: {addr} absent from certified function list",
                  file=sys.stderr)
            cell = f"`{addr}`"
        else:
            m = _STATED.match(desc)
            if m:
                if int(m.group(0).strip("()B, ")) != size:
                    print(f"warning: {addr} stated size {m.group(0)} "
                          f"corrected to {size} B", file=sys.stderr)
                desc = desc[m.end():].lstrip(" —-")
            for m2 in _STATED.finditer(desc):
                if int(m2.group(0).strip("()B, ")) != size:
                    print(f"warning: {addr} description carries disagreeing "
                          f"size {m2.group(0)}; ledger says {size} B",
                          file=sys.stderr)
            cell = f"`{addr}` ({size} B)"
        lines.append(f"| {cell} | {desc} | [`{addr}`]({prefix}) |")
    lines += ["", f"Shared callees outside the census: {shared}.", ""]
    return "\n".join(lines)


def fix_page_links(page_path: str) -> int:
    """Repair any wrong-depth ADDRESS-INDEX backlinks already on a page.

    Returns the number of links rewritten.
    """
    prefix = index_prefix(page_path)
    with open(page_path, encoding="utf-8", errors="ignore") as f:
        txt = f.read()
    pat = re.compile(r"\]\((\.\./)*_index/ADDRESS-INDEX\.md\)")
    new, n = pat.subn("](" + prefix + ")", txt)
    if n and new != txt:
        with open(page_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
    return n if new != txt else 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--fix":
        total = 0
        for p in sys.argv[2:]:
            total += fix_page_links(p)
        print(f"fixed {total} link(s)")
        sys.exit(0)
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    page, root, prose = sys.argv[1], sys.argv[2].upper(), sys.argv[3]
    members = sys.argv[4:]
    section = emit_section(page, root, prose, members)
    with open(page, "a", encoding="utf-8", newline="\n") as f:
        f.write(section)
    print(f"appended {root} -> {page} (prefix {index_prefix(page)})")
