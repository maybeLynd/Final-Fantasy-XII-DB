"""chained_tail_errata.py - the chained-tails apply (OPUS, 2026-09-30; FRONTIER-REQ-OPUS-UC1-EXTENT-V3-APPLY).

Ruling: `_index/candidates/register-triage/batch-K-scope-rulings.md`, extension 2026-09-29 "catalogue chained tails -
the executable view extends, the catalogue does not". 270 catalogue functions end before their own chained .pdata
fragments (measured by fragment_size_sweep.py, `_index/candidates/fragment-size-sweep-0929/`). This emits one
`underrun-extend` row per such root into `_index/FUNCTION-EXTENT-ERRATA.tsv`, mechanically:

  - a root is a .pdata entry whose UNWIND_INFO is not chained; its chain is every entry whose chained-to walk ends at it;
  - the chain must be contiguous (each fragment begins where the previous one ends) - re-verified per row;
  - corrected_end = the chain union's end, and must exceed the listed end (functions.tsv entry + size);
  - the extension must not overlap the next listed entry (overlap_into_next = 0), else the row is refused and reported;
  - an entry that already carries an `underrun-extend` row: the same corrected_end is skipped (one adjudication, one
    row); an instruction-scan row that stops short of the chain's end gets this row beside it (a second finding, one row
    per detector, the ledger's convention since 906d5480a) and consumers take the furthest adjudicated end; a ledger row
    that already runs PAST the chain is a conflict, reported, never written.

Extent, not semantics: a chain says which bytes belong to the function, never what the code does.

Controls (measured 2026-09-29, 624e3534e): 3,828 chained roots, all contiguous; 270 short roots; 16,361 bytes.
Usage: chained_tail_errata.py [--apply]   (without --apply it only reports)
"""
import io, os, struct, sys
import pefile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
ERRATA = os.path.join(ROOT, "FFXII TZA", "_index", "FUNCTION-EXTENT-ERRATA.tsv")
DETECTOR = "pdata-chain"


def chains(exe=EXE):
    blob = io.open(exe, "rb").read()
    pe = pefile.PE(exe, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    secs = [(base + s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b"\0").decode()) for s in pe.sections]

    def off(va):
        for st, raw, rs, _n in secs:
            if st <= va < st + rs:
                return raw + va - st
        raise ValueError("%08X outside the image" % va)

    pd = next(s for s in secs if s[3] == ".pdata")
    praw = blob[pd[1]:pd[1] + pd[2]]
    pent = {}
    for j in range(0, len(praw) - 11, 12):
        b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
        if b_:
            pent[base + b_] = (base + e_, base + u_)

    def chained_to(begin):
        u = pent[begin][1]
        h = blob[off(u):off(u) + 4]
        if not (h[0] >> 3) & 4:
            return None
        c = off(u) + 4 + 2 * ((h[2] + 1) & ~1)
        return base + struct.unpack("<I", blob[c:c + 4])[0]

    frags = {}
    for b in pent:
        r, seen = b, set()
        while r in pent and r not in seen:
            seen.add(r)
            n = chained_to(r)
            if n is None:
                break
            r = n
        frags.setdefault(r, []).append((b, pent[b][0]))
    return {r: sorted(fs) for r, fs in frags.items() if len(fs) > 1}


def listed(path=FUNCS):
    out = {}
    for i, line in enumerate(io.open(path, encoding="utf-8", errors="replace")):
        p = line.rstrip("\n").split("\t")
        if i and len(p) > 2:
            try:
                out[int(p[0], 16)] = (p[1], int(p[2]))
            except ValueError:
                pass
    return out


def existing(path=ERRATA):
    ex = {}
    for i, line in enumerate(io.open(path, encoding="utf-8")):
        p = line.rstrip("\r\n").split("\t")
        if i and len(p) >= 15 and p[13].startswith("underrun-extend") and p[12]:
            ex.setdefault(int(p[0], 16), set()).add(int(p[12], 16))
    return ex


def rows(ch, fns, ex):
    starts = sorted(fns)
    import bisect
    out, refused, skipped, conflicts, wider = [], [], [], [], []
    noncontig = [r for r, fs in ch.items() if any(fs[k][0] != fs[k - 1][1] for k in range(1, len(fs)))]
    for r, fs in sorted(ch.items()):
        if r not in fns or r in noncontig:
            continue
        name, size = fns[r]
        end, cend = r + size, fs[-1][1]
        if cend <= end:
            continue
        k = bisect.bisect_right(starts, r)
        nxt = starts[k] if k < len(starts) else None
        if nxt is not None and nxt < cend:
            refused.append((r, cend, nxt))
            continue
        if r in ex:
            if cend in ex[r]:
                skipped.append((r, cend, sorted(ex[r])))
                continue
            if max(ex[r]) > cend:              # the ledger already grows the entry past its own chain: a contradiction
                conflicts.append((r, cend, sorted(ex[r])))
                continue
            wider.append((r, cend, sorted(ex[r])))   # an instruction-scan row that stops short of the chain: a second finding
        out.append([ "%08X" % r, name, str(size), "%08X" % end, "", "", "", "", "", "0", "-",
                     "%08X" % nxt if nxt is not None else "", "%08X" % cend,
                     "underrun-extend (%d bytes past body_bytes, %d chained fragments)" % (cend - end, len(fs)), DETECTOR])
    return out, refused, skipped, conflicts, noncontig, wider


def main(argv):
    ch = chains()
    fns = listed()
    ex = existing()
    out, refused, skipped, conflicts, noncontig, wider = rows(ch, fns, ex)
    short = len(out) + len(refused) + len(skipped) + len(conflicts)
    nbytes = sum(int(r[12], 16) - int(r[3], 16) for r in out) + sum(c - (a + fns[a][1]) for a, c, _ in skipped + conflicts)
    print("chained roots: %d (control 3,828); non-contiguous: %d (control 0)" % (len(ch), len(noncontig)))
    print("catalogue roots ending before their chain: %d (control 270); bytes past listed ends: %d (control 16,361)" % (short, nbytes))
    print("rows to emit: %d (of them %d beside an instruction-scan row that stops short of the chain); already in the ledger "
          "with the same end: %d; conflicts (ledger past the chain): %d; refused (overlap next entry): %d" % (
        len(out), len(wider), len(skipped), len(conflicts), len(refused)))
    for a, c, e in wider:
        print("  BESIDE   %08X chain end %08X, instruction-scan row %s (+%d)" % (a, c, " ".join("%08X" % x for x in e), c - max(e)))
    for a, c, e in conflicts:
        print("  CONFLICT %08X chain end %08X, ledger %s" % (a, c, " ".join("%08X" % x for x in e)))
    for a, c, n in refused:
        print("  REFUSED  %08X chain end %08X overlaps next entry %08X" % (a, c, n))
    ok = len(ch) == 3828 and not noncontig and short == 270 and nbytes == 16361 and not conflicts and not refused
    print("%s  controls" % ("PASS" if ok else "FAIL"))
    if "--apply" in argv:
        if not ok:
            print("REFUSED: controls failed; nothing written")
            return 1
        if not out:
            print("nothing to write (already applied)")
            return 0
        raw = io.open(ERRATA, "rb").read()
        with io.open(ERRATA, "ab") as o:
            if not raw.endswith(b"\n"):
                o.write(b"\n")
            for r in out:
                o.write(("\t".join(r) + "\n").encode("utf-8"))
        print("appended %d rows to %s" % (len(out), os.path.relpath(ERRATA, ROOT)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
