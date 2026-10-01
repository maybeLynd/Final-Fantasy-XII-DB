#!/usr/bin/env python3
"""field_music_table.py - read the REAL field-music table out of the running game, and parse it.

Why this exists
---------------
`FieldMusic_Select` (`003EAA70`) is the program's first differential pilot, and its harness feeds
it **synthetic** tables: `DG-1` recorded that `0x02B5E0D0` holds an allocated buffer whose filler
(`0032E620`) was unread, so nothing knew what the real table looked like. `CONTRACT-field-music-
selection.md` section 15 carries the row *"What fills the table -- not established"*, and
`diff_field_music.py` declares `INTEGRATION: NOT COVERED -- tables here are synthetic`.

The game will simply tell you, once it is running. This reads the pointer, walks the table under
the format the contract documents, and **reports every place the real bytes disagree with that
format** rather than assuming they agree.

What it checks, and why each check earns its place
--------------------------------------------------
    magic          the first dword -- the contract does not mention one, and there IS one
    max field id   the second dword
    page count     ceil((max_field + 1) / 128) pages must be present and in range
    run chains     packed u16: start = v & 0x7FF, length = v >> 11; stride 4 + 3*count
    thresholds     must not run past the end of the buffer

**A chain has no terminator.** The walk in the shipped function stops only when a run's start
exceeds the query, so a page whose chain ends below the highest reachable field id runs on into
whatever follows. `diff_field_music.py` learned that by generating tables that crashed the
emulator. This tool therefore reports, per page, the **highest start it saw** -- the shipped data
should end every page above its own field range, and that is checkable rather than assumed.

Read-only. It opens the process for READ and takes no write access.
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP
import runtime_poke as PK

TABLE_PTR_VA = 0x02B5E0D0
PAGE_STRIDE = 128


def parse(blob, base):
    """-> (report lines, problems). `base` is the table's virtual address, because page[]
    entries are ABSOLUTE addresses and only mean anything relative to it."""
    out, bad = [], []
    if len(blob) < 8:
        return out, ["the buffer is shorter than a header"]
    magic = blob[0:4]
    max_field = struct.unpack_from("<i", blob, 4)[0]
    out.append("magic          %s   %r" % (magic.hex(), magic))
    out.append("max field id   %d" % max_field)
    if max_field < 0:
        bad.append("max field id is negative")
        return out, bad
    npages = (max_field + PAGE_STRIDE) // PAGE_STRIDE
    out.append("pages          %d   (ceil((%d + 1) / %d))" % (npages, max_field, PAGE_STRIDE))

    pages = []
    for p in range(npages):
        off = 8 + 4 * p
        if off + 4 > len(blob):
            bad.append("page %d's entry is past the end of the read" % p)
            break
        pages.append(struct.unpack_from("<I", blob, off)[0])

    empty = [p for p, a in enumerate(pages) if a == 0]
    out.append("empty pages    %d of %d%s"
               % (len(empty), len(pages), ("  %s" % empty) if empty else ""))

    header_end = 8 + 4 * npages
    rows = []
    for p, addr in enumerate(pages):
        if addr == 0:
            rows.append((p, 0, 0, None, None))
            continue
        rel = addr - base
        if rel < header_end or rel >= len(blob):
            bad.append("page %d points to %08X, which is outside the buffer read" % (p, addr))
            rows.append((p, 0, 0, None, None))
            continue
        runs = tracks = 0
        hi = -1
        cur = rel
        lo = p * PAGE_STRIDE
        # Walk until a run's start is above this page's own range -- the same stop condition the
        # shipped function uses. A page that never reaches it is the dangerous shape.
        while cur + 4 <= len(blob):
            packed, count, track = struct.unpack_from("<HBB", blob, cur)
            start = packed & 0x7FF
            length = packed >> 11
            if start > hi:
                hi = start
            runs += 1
            if track:
                tracks += 1
            cur += 4 + 3 * count
            if start >= lo + PAGE_STRIDE - 1:
                break
            if runs > 4096:
                bad.append("page %d's chain did not stop after 4096 runs" % p)
                break
        else:
            bad.append("page %d's chain ran past the end of the buffer read" % p)
        rows.append((p, runs, tracks, hi, lo + PAGE_STRIDE - 1))
    out.append("")
    out.append("| page | field ids | runs | runs with a track | highest start | covers its top? |")
    out.append("|---:|---|---:|---:|---:|---|")
    for p, runs, tracks, hi, top in rows:
        if hi is None:
            out.append("| %d | %d..%d | *(empty page)* | | | n/a |"
                       % (p, p * PAGE_STRIDE, p * PAGE_STRIDE + PAGE_STRIDE - 1))
            continue
        ok = "yes" if hi >= top else "**NO**"
        if hi < top:
            bad.append("page %d's chain stops at start %d, below its top field id %d -- the walk "
                       "would run into whatever follows" % (p, hi, top))
        out.append("| %d | %d..%d | %d | %d | %d | %s |"
                   % (p, p * PAGE_STRIDE, top, runs, tracks, hi, ok))
    return out, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--size", type=lambda s: int(s, 0), default=0x20000)
    ap.add_argument("--save", help="write the raw table bytes here")
    a = ap.parse_args()

    hits = RP.find_process(a.process)
    if not hits:
        sys.stderr.write("field_music_table: no %r process running\n" % a.process)
        return 2
    pid = hits[0][0]
    rw = PK.RW(pid)
    base = rw.q(TABLE_PTR_VA)
    print("pid %d   [%08X] = %016X" % (pid, TABLE_PTR_VA, base or 0))
    if not base:
        print("the pointer is NULL -- the table has not been built yet")
        return 3
    # The allocation is sized from a table (DG-1) and nothing here knows how big it is, so the
    # read backs off rather than failing. **How much was readable is reported**, because a run
    # that silently read less would under-count runs and call a truncated walk a clean one.
    blob, size = None, a.size
    while size >= 0x400:
        blob = rw.read(base, size)
        if blob is not None:
            break
        size //= 2
    if blob is None:
        print("could not read even 0x400 bytes at %016X" % base)
        return 3
    if size != a.size:
        print("readable extent: 0x%X bytes (asked for 0x%X -- the allocation is smaller)"
              % (size, a.size))
    lines, bad = parse(blob, base)
    print()
    for l in lines:
        print(l)
    print()
    if bad:
        print("PROBLEMS (%d):" % len(bad))
        for b in bad:
            print("  - %s" % b)
    else:
        print("The real table parses cleanly under the format the contract documents.")
    if a.save:
        open(a.save, "wb").write(blob)
        print("wrote %s (%d bytes)" % (a.save, len(blob)))
    rw.close()
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
