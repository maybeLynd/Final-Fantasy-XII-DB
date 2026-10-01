"""vbf_index.py - capture the installed VBF archive's own name/size index for the dashboard (OPUS, 2026-09-29).

The VBF view used to read a static listing (Tools/work/repos-2d/vbf_list.txt, 2026-09-02), so an archive update would
have gone unseen. This reads the archive's SRYK header on every build instead - header only (about 12 MB of a 31 GB
file), no payload, no decompression - and writes one JSON the generation snapshots like any other captured input.

The header parser is ASTRA's `archive_index` from Tools/work/ASTRA/migration-a23-current-release/a17-vbf-archive-index-check.py
(7b73151a5, A17), kept byte-for-byte in its checks: SRYK magic, header length within the file, a plausible entry count,
table bounds, UTF-8 names, terminators and duplicates. Any failure is written as {"failed": reason}; the view then reports
FAILED for the archive side and never falls back silently to the old listing.

    python vbf_index.py --archive <FFXII_TZA.vbf> [--listing <vbf_list.txt>] --out <json>
"""
import argparse, hashlib, json, os, struct, sys

DEFAULT_ARCHIVE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf"


def archive_index(path):
    """(names {path: uncompressed size}, receipt) from the archive's own header (ASTRA A17 parser)."""
    with open(path, "rb") as stream:
        preamble = stream.read(16)
        if len(preamble) != 16:
            raise ValueError("short VBF preamble")
        magic, header_length, count = struct.unpack("<4sIQ", preamble)
        if magic != b"SRYK" or header_length > os.path.getsize(path):
            raise ValueError("invalid VBF header")
        if not (0 < count <= 1_000_000):
            raise ValueError("implausible VBF entry count")
        stream.seek(0)
        header = stream.read(header_length)
    if len(header) != header_length:
        raise ValueError("short VBF header")
    entries_start = 16 + count * 16
    strings_start = entries_start + count * 32
    if strings_start + 4 > header_length:
        raise ValueError("entry table overruns header")
    string_length = struct.unpack_from("<I", header, strings_start)[0]
    string_table = header[strings_start + 4:strings_start + string_length]        # the length counts its own four bytes
    if len(string_table) != string_length - 4:
        raise ValueError("string table overruns header")
    names = {}
    for index in range(count):
        _, _, size, _, name_offset = struct.unpack_from("<IIQQQ", header, entries_start + index * 32)
        if name_offset >= len(string_table):
            raise ValueError("entry %d name offset out of range" % index)
        end = string_table.find(b"\0", name_offset)
        if end < 0:
            raise ValueError("entry %d name unterminated" % index)
        name = string_table[name_offset:end].decode("utf-8")
        if not name or name in names:
            raise ValueError("entry %d empty or duplicate name" % index)
        names[name] = size
    return names, {"magic": magic.decode("ascii"), "header_length": header_length, "entry_count": count,
                   "header_sha256": hashlib.sha256(header).hexdigest()}


def read_listing(path):
    rows = {}
    for line in open(path, encoding="utf-8").read().splitlines():
        size, sep, name = line.partition(" ")
        if sep and size.isdecimal() and name:
            rows[name] = int(size)
    return rows


def capture(archive, listing=None):
    try:
        names, rec = archive_index(archive)
    except (OSError, ValueError) as e:
        return {"failed": "%s: %s" % (type(e).__name__, e), "archive_path": archive}
    st = os.stat(archive)
    out = {"archive_path": archive, "archive_file_bytes": st.st_size, "archive_mtime_ns": st.st_mtime_ns, "archive_index": rec,
           "entries": sorted([n, s] for n, s in names.items()), "uncompressed_bytes": sum(names.values())}
    if listing and os.path.isfile(listing):
        old = read_listing(listing)
        out["vs_listing"] = {"listing_path": listing, "missing_from_archive": len(old.keys() - names.keys()),
                             "missing_from_listing": len(names.keys() - old.keys()),
                             "size_mismatch": sum(1 for n in names.keys() & old.keys() if names[n] != old[n])}
    return out


def format_claims(db):
    """ext -> sorted disposition words claimed by `archive_formats:` frontmatter (check_assets.claimed_formats)."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis-kit", "gfz-scripts"))
    import check_assets as CA
    return {ext: sorted({d for _doc, d, _n in rows}) for ext, rows in CA.claimed_formats(db).items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive", default=os.environ.get("FF12_VBF", DEFAULT_ARCHIVE))
    ap.add_argument("--listing")
    ap.add_argument("--db", help="database root: also capture each extension's claimed format dispositions")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    r = capture(a.archive, a.listing)
    if a.db:
        try:
            r["format_claims"] = format_claims(a.db)
        except Exception as e:          # a failed claim read is reported, never an empty "no claims"
            r["format_claims_failed"] = "%s: %s" % (type(e).__name__, e)
    tmp = a.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(r, f)
    os.replace(tmp, a.out)
    print("failed: " + r["failed"] if "failed" in r else "entries %d header %s" % (len(r["entries"]), r["archive_index"]["header_sha256"][:12]))
    return 1 if "failed" in r else 0


if __name__ == "__main__":
    sys.exit(main())
