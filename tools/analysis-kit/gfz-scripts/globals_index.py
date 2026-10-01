#!/usr/bin/env python3
"""globals_index.py - answer charter section 7's first two queries about global state.

    "Show every known writer of this field."
    "Show every reader of this global."

The data already existed
------------------------
`Tools/work/h78/rip_data_refs.tsv` holds 164,489 rows of
`function_entry, referenced_address, kind, site` with **writes separated from reads** and
address-takings separated from both. It was sitting on disk unused: at the time this tool was
written, **1,134 of 35,879 referenced globals (3.16 %) were mentioned in any document.**

This script indexes it, joins it to the documents, and - most usefully - ranks the globals that
nothing explains, which is a research frontier generator rather than another report.

Two properties of the data you must not forget
----------------------------------------------
**1. It is RIP-relative only, and that is a real blind spot.** This binary also addresses globals as
`[reg + index*8 + disp]` after loading the image base into a register:

    0032FB87  lea  r14, [rip - 0x20fb8e]           ; r14 = 0x00120000
    0032FB9B  mov  [r14 + rcx*8 + 0x21a6da8], rdx  ; = 0x022C6DA8[rcx]

`0x022C6DA8` has **zero rows here** while being demonstrably referenced. So **absence from this
index is not absence from the binary** - it is absence from one instrument. Use
`data_xref_scan.py` (which decodes both forms from function entries) to settle any negative.

**2. Cross-validated where it can be.** Three addresses whose reference counts this database
established independently agree exactly: `01F82D20` 157, `01DFE0B4` 212, `02CACC90` 64. That is
why the positive numbers here are trustworthy even though the negatives are not.

EH funclet callers are excluded from every "function" figure, per the mission prompt's ban on
unwind data as semantic evidence.

Usage
-----
    globals_index.py --addr 01F82D20            who reads/writes it, and which documents cite it
    globals_index.py --fn 001EDDC0              which globals a function touches
    globals_index.py --frontier 40              hottest globals no document mentions
    globals_index.py --frontier 200 --out FILE  write the frontier artifact
    globals_index.py --owner-summary            per-owner global counts, cited vs not
"""
import argparse
import collections
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402
import uc1_band  # noqa: E402

HEX8 = re.compile(r"^[0-9A-F]{8}$")
ANY_HEX8 = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
BLIND = ("RIP-relative only. Globals reached as `[reg + index*8 + disp]` do not appear here, and "
         "NEITHER DOES A STORE THROUGH A WALKING POINTER. Two worked examples, both 0 rows and both "
         "demonstrably written: `0x022C6DA8`, and **`0x0208EA28`**, which a startup loop writes at "
         "`00247D9F mov [rdi], rbx` after `00247D20 lea rdi, [0208EA20]` - an array base, three "
         "iterations, `+8` stride. "
         "**Absence from this index is not absence from the binary.** "
         "Added 2026-09-13: a 0 in the writers column of this table was quoted as 'never written, "
         "NULL for the life of the process' in a CONTRACT, and the contract was wrong. "
         "THIS CALLOUT EXISTED AT THE TIME. An instrument that declares its own blind spot has "
         "done its part; reading past the declaration is the reader's defect.")


DEFAULT_EXE = os.path.join(KP.ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")


def load_image(path):
    """(imports {VA: 'DLL!name'}, qword(VA) -> int or None, iat_lo, iat_hi) from the PE.

    Added 2026-09-13 (OPUS-REQ-GLOBALS-INDEX-IAT). Four of the forty hottest "unexplained"
    globals were named Windows imports -- `memmove`, `EnterCriticalSection`,
    `LeaveCriticalSection`, `_invalid_parameter_noinfo_noreturn`. Their 0 in the writers column
    is not a mystery: **the loader writes them.** They are fully resolvable from the PE headers
    and are not FFXII state a reconstruction has to discover, so ranking them as frontier invites
    exactly the wrong reading.
    """
    import struct
    try:
        d = io.open(path, "rb").read()
    except (IOError, OSError):
        return {}, (lambda va: None), 0, 0
    e = struct.unpack_from("<I", d, 0x3C)[0]
    base = struct.unpack_from("<Q", d, e + 24 + 24)[0]
    nsec = struct.unpack_from("<H", d, e + 6)[0]
    optsz = struct.unpack_from("<H", d, e + 20)[0]
    secs, off = [], e + 24 + optsz
    for _ in range(nsec):
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", d, off + 8)
        secs.append((va, vsz, rsz, rptr))
        off += 40

    def fileoff(rva, raw_only=False):
        for va, vsz, rsz, rptr in secs:
            if va <= rva < va + (rsz if raw_only else max(vsz, rsz)):
                return rptr + (rva - va)
        return None

    def qword(va):
        """The file-backed qword at VA, or None when VA has no file image."""
        o = fileoff(va - base, raw_only=True)
        if o is None or o + 8 > len(d):
            return None
        return struct.unpack_from("<Q", d, o)[0]

    dd = e + 24 + 112
    iat_rva, iat_sz = struct.unpack_from("<II", d, dd + 12 * 8)
    imp_rva = struct.unpack_from("<I", d, dd + 1 * 8)[0]

    def cstr(o):
        return d[o:d.index(b"\0", o)].decode("ascii", "replace")

    imports, o = {}, fileoff(imp_rva)
    while o is not None:
        oft, _ts, _fc, nm, fthunk = struct.unpack_from("<IIIII", d, o)
        if nm == 0 and fthunk == 0:
            break
        dll = cstr(fileoff(nm))
        to, ta, k = fileoff(oft or fthunk), base + fthunk, 0
        while True:
            v = struct.unpack_from("<Q", d, to + 8 * k)[0]
            if v == 0:
                break
            name = "#%d" % (v & 0xFFFF) if v & (1 << 63) else cstr(fileoff((v & 0x7FFFFFFF) + 2))
            imports[ta + 8 * k] = "%s!%s" % (dll, name)
            k += 1
        o += 20
    return imports, qword, base + iat_rva, base + iat_rva + iat_sz


def die(m):
    sys.stderr.write("globals_index: %s\n" % m)
    raise SystemExit(2)


def load_functions(work):
    path = os.path.join(work, "graph", "functions.tsv")
    if not os.path.exists(path):
        die("missing %s" % path)
    fns = {}
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        i = {n: k for k, n in enumerate(head)}
        for ln in fh:
            p = ln.rstrip("\n").split("\t")
            if not p or not HEX8.match(p[0]):
                continue
            tags = p[i["tags"]] if i.get("tags", 99) < len(p) else ""
            fns[p[0]] = {
                "name": p[i["name"]] if i.get("name", 99) < len(p) else "",
                "owner": p[i["owner"]] if i.get("owner", 99) < len(p) else "",
                "size": p[i["body_bytes"]] if i.get("body_bytes", 99) < len(p) else "",
                "eh": "CompilerGeneratedEH" in tags,
                "tags": tags,
            }
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(
            os.path.join(KP.ROOT, "Database", "Tools", "work", "graph",
                         "functions.tsv")):
        _b = uc1_band.load()
        for e in _b["removed"]:
            fns.pop("%08X" % e, None)
        for e, en in _b["extend"].items():
            k = "%08X" % e
            if k in fns:
                fns[k]["size"] = str(en - e)
        for st, sz in _b["frontier"].items():
            k = "%08X" % st
            fns[k] = {"name": "UC1-FRONTIER-%s" % k, "owner": "",
                      "size": str(sz), "eh": False, "tags": ""}
    return fns


def load_refs(work, fns):
    path = os.path.join(work, "h78", "rip_data_refs.tsv")
    if not os.path.exists(path):
        die("missing %s - this index has no data source without it" % path)
    by_addr = collections.defaultdict(lambda: collections.defaultdict(set))
    by_fn = collections.defaultdict(lambda: collections.defaultdict(set))
    rows = eh_rows = 0
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        fh.readline()
        for ln in fh:
            p = ln.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            fn, ad, kind = p[0].upper(), p[1].upper(), p[2]
            rows += 1
            if fns.get(fn, {}).get("eh"):
                eh_rows += 1
                continue                      # banned as semantic evidence
            by_addr[ad][kind].add(fn)
            by_fn[fn][kind].add(ad)
    return by_addr, by_fn, rows, eh_rows


def load_doc_citations(db):
    cites = collections.defaultdict(set)
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d != "_templates"]
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), db).replace("\\", "/")
            if rel.startswith("_index/"):
                continue                      # indices echo everything; they are not explanations
            text = io.open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
            for m in ANY_HEX8.finditer(text):
                cites[m.group(1).upper()].add(rel)
    return cites


def fmt_fn(va, fns):
    f = fns.get(va)
    if not f:
        return va
    nm = f["name"] or "?"
    own = (" [%s]" % f["owner"]) if f["owner"] else ""
    return "%s %s (%s B)%s" % (va, nm, f["size"], own)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--addr")
    ap.add_argument("--fn")
    ap.add_argument("--frontier", type=int)
    ap.add_argument("--owner-summary", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--show", type=int, default=25)
    ap.add_argument("--exe", default=DEFAULT_EXE)
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    # Walk up until the directory containing "Database/FFXII TZA" is found, rather than counting
    # dirname() levels. Miscounting them silently produced an EMPTY citation set, which read as
    # "nothing explains this global" for globals that are in fact documented - a false negative
    # that would have gone into a report as a finding.
    root = here
    for _ in range(8):
        if os.path.isdir(os.path.join(root, "Database", "FFXII TZA")):
            break
        root = os.path.dirname(root)
    work = a.work or os.path.join(root, "Database", "Tools", "work")
    db = a.db or os.path.join(root, "Database", "FFXII TZA")
    if not os.path.isdir(db):
        die("could not locate 'Database/FFXII TZA' above %s (pass --db)" % here)
    if not os.path.isdir(work):
        die("could not locate Tools/work (pass --work)")

    fns = load_functions(work)
    by_addr, by_fn, rows, eh_rows = load_refs(work, fns)
    cites = load_doc_citations(db)

    if a.addr:
        ad = a.addr.upper().replace("0X", "")
        e = by_addr.get(ad)
        print("global %s" % ad)
        if not e:
            print("  no RIP-relative reference rows.")
            print("  NOTE: %s" % BLIND)
            return 0
        for kind in ("write", "rw", "read", "addr", "other"):
            s = sorted(e.get(kind, ()))
            if not s:
                continue
            print("  %-6s %3d function(s)" % (kind, len(s)))
            for v in s[:a.show]:
                print("      %s" % fmt_fn(v, fns))
            if len(s) > a.show:
                print("      ... %d more" % (len(s) - a.show))
        d = cites.get(ad)
        print("  cited by %d document(s)%s" % (len(d or ()), ":" if d else " - UNEXPLAINED"))
        for x in sorted(d or ()):
            print("      %s" % x)
        return 0

    if a.fn:
        fv = a.fn.upper().replace("0X", "")
        e = by_fn.get(fv)
        print("function %s" % fmt_fn(fv, fns))
        if not e:
            print("  touches no global through a RIP-relative operand.")
            print("  NOTE: %s" % BLIND)
            return 0
        for kind in ("write", "rw", "read", "addr", "other"):
            s = sorted(e.get(kind, ()))
            if not s:
                continue
            print("  %-6s %3d global(s): %s%s"
                  % (kind, len(s), " ".join(s[:a.show]),
                     " ..." if len(s) > a.show else ""))
        return 0

    if a.owner_summary:
        own = collections.Counter()
        own_cited = collections.Counter()
        for ad, kinds in by_addr.items():
            writers = kinds.get("write", set()) | kinds.get("rw", set())
            owners = {fns[w]["owner"] for w in writers if fns.get(w, {}).get("owner")}
            for o in (owners or {"(no owner)"}):
                own[o] += 1
                if ad in cites:
                    own_cited[o] += 1
        print("%-46s %8s %8s %7s" % ("owner of at least one writer", "globals", "cited", "share"))
        for o, n in own.most_common(40):
            c = own_cited[o]
            print("%-46s %8d %8d %6.1f%%" % (o[:46], n, c, 100.0 * c / n))
        return 0

    n = a.frontier or 40
    imports, qword, iat_lo, iat_hi = load_image(a.exe)
    ranked, imported = [], []
    for ad, kinds in by_addr.items():
        if ad in cites:
            continue
        w = len(kinds.get("write", ())) + len(kinds.get("rw", ()))
        r = len(kinds.get("read", ())) + len(kinds.get("rw", ()))
        t = len(kinds.get("addr", ()))
        va = int(ad, 16)
        if va in imports or (iat_lo <= va < iat_hi):
            imported.append((w + r + t, w, r, t, ad, imports.get(va, "(IAT slot, unnamed)")))
            continue
        ranked.append((w + r + t, w, r, t, ad))
    ranked.sort(reverse=True)
    imported.sort(reverse=True)

    # A container sentinel whose root field points back at itself shows up as TWO hot rows -- the
    # object and the field -- and they read as two separate discoveries. Detect it from the image
    # instead of naming addresses: a ranked row whose file-backed qword holds another ranked row's
    # address (or its own) is part of that object. 2026-09-13, OPUS-REQ-GLOBALS-INDEX-IAT.
    top = {ad for _t, _w, _r, _tk, ad in ranked[:n]}
    same_object = {}
    for _t, _w, _r, _tk, ad in ranked[:n]:
        v = qword(int(ad, 16))
        if v is None:
            continue
        tgt = "%08X" % v
        if tgt == ad:
            same_object[ad] = (None, "its own address is stored in it — a container sentinel "
                                     "whose root field points back at itself, i.e. empty")
        elif tgt in top:
            same_object[ad] = (tgt, "+0x%X, and holds that address" % (int(ad, 16) - v))

    L = []
    out = L.append
    total_addrs = len(by_addr)
    cited_addrs = sum(1 for ad in by_addr if ad in cites)
    out("# Unexplained global state — the frontier, ranked")
    out("")
    out("*Generated by `Database/Tools/analysis-kit/gfz-scripts/globals_index.py`. Regenerate it; "
        "do not quote these numbers from memory.*")
    out("")
    out("| | count | denominator |")
    out("|---|---:|---:|")
    out("| reference rows read | %d | — |" % rows)
    out("| rows discarded (EH funclet referrer, banned evidence) | %d | %d (%.2f %%) |"
        % (eh_rows, rows, 100.0 * eh_rows / rows))
    out("| distinct globals referenced | %d | — |" % total_addrs)
    out("| **cited by at least one system document** | **%d** | %d (%.2f %%) |"
        % (cited_addrs, total_addrs, 100.0 * cited_addrs / total_addrs))
    out("| **explained by nothing** | **%d** | %d (%.2f %%) |"
        % (total_addrs - cited_addrs, total_addrs,
           100.0 * (total_addrs - cited_addrs) / total_addrs))
    # The denominator is spelled "N of D" rather than left as a bare column number: it is the
    # explained-by-nothing count, which is NOT one of check_denominators.py's known populations,
    # and with only the bare number the checker matched 1.52 % against 34,270 instead. An explicit
    # "N of D" is self-declaring. 2026-09-14, OPUS.
    out("| of those, Windows import (IAT) slots, held out of the ranking below | %d | "
        "%d of %d explained by nothing (%.2f %%) |"
        % (len(imported), len(imported), total_addrs - cited_addrs,
           100.0 * len(imported) / max(1, total_addrs - cited_addrs)))
    out("")
    out("> **Holding the imports out does not explain anything.** They were never FFXII state. "
        "Four of them ranked in the top forty of this table before 2026-09-13 — `memmove` at rank "
        "3, `LeaveCriticalSection` at 5, `EnterCriticalSection` at 6, "
        "`_invalid_parameter_noinfo_noreturn` at 38 — and their `0` in the writers column is not a "
        "mystery to solve: **the loader writes them.** They are named in the PE import directory "
        "and resolvable without reading a single FFXII instruction. Removing a row that was never "
        "frontier is not progress on the frontier, and the count above is printed so that the "
        "change in the denominator is visible rather than silent. They are listed in full below.")
    out("")
    out("> **Blind spot, stated up front.** %s" % BLIND)
    out(">")
    out("> **Why the positives are trustworthy anyway.** Three reference counts this database "
        "established by a different instrument agree exactly with this one: `01F82D20` **157**, "
        "`01DFE0B4` **212**, `02CACC90` **64**.")
    out("")
    out("## The %d hottest globals nothing explains" % n)
    out("")
    out("Ranked by total referencing functions. **A global with many writers across many owners is "
        "shared mutable state** — the most expensive kind to discover late in a reconstruction.")
    out("")
    out("| rank | global | writers | readers | addr-taken | owners of writers |")
    out("|---:|---|---:|---:|---:|---|")
    for i, (tot, w, r, t, ad) in enumerate(ranked[:n], 1):
        owners = collections.Counter()
        for f in by_addr[ad].get("write", set()) | by_addr[ad].get("rw", set()):
            owners[fns.get(f, {}).get("owner") or "(none)"] += 1
        os_ = ", ".join("%s×%d" % (k.split(".")[-1] or k, v) for k, v in owners.most_common(3))
        note = ""
        if ad in same_object:
            tgt, how = same_object[ad]
            note = (" — **same object as `%s`** (%s)" % (tgt, how) if tgt
                    else " — **%s**" % how)
        out("| %d | `%s`%s | **%d** | %d | %d | %s |" % (i, ad, note, w, r, t, os_ or "—"))
    out("")
    if same_object:
        out("> **Rows marked *same object* are not separate discoveries.** The marker is derived "
            "from the image, not from a list: the file-backed qword at the row's address holds "
            "another ranked row's address, which is what a container sentinel whose root field "
            "points back at itself looks like from a reference count. Counting both as frontier "
            "counts one object twice.")
        out("")
    if imported:
        out("## Held out: Windows imports (%d)" % len(imported))
        out("")
        out("Resolved from the PE import directory, not guessed. These are named external "
            "functions; the IAT data directory is `%08X`–`%08X`." % (iat_lo, iat_hi))
        out("")
        out("| global | import | writers | readers | addr-taken |")
        out("|---|---|---:|---:|---:|")
        for tot, w, r, t, ad, nm in imported[:n]:
            out("| `%s` | `%s` | %d | %d | %d |" % (ad, nm, w, r, t))
        if len(imported) > n:
            out("")
            out("*(%d more, same kind.)*" % (len(imported) - n))
        out("")
    out("## How to use this")
    out("")
    out("```")
    out("globals_index.py --addr <VA>    every writer, reader and address-taking, plus citing docs")
    out("globals_index.py --fn <VA>      every global a function touches, split by kind")
    out("globals_index.py --owner-summary")
    out("```")

    text = "\n".join(L) + "\n"
    if a.out:
        io.open(a.out, "w", encoding="utf-8", newline="\n").write(text)
        sys.stdout.write("wrote %s (%d lines)\n" % (a.out, len(L)))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
