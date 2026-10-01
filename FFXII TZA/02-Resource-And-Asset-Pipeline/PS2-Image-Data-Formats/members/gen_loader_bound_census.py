#!/usr/bin/env python3
"""Census of the thirteen file families bound by static loaders.

FABLE-REQ-SWE2-DATA-LOADERS-FOR-UNNAMED-FILES: every family in the request has
a numeric kind/subtype request site (constant-resource-requests.tsv) but no
path literal in the loader. This script walks every shipped instance of each
family and re-derives the structure facts the sheet cites:

  * the `*pack_ys` / `fontpack_*` files share a directory container:
    a fixed-width u32 self-relative-offset directory at +0
    (0x40-byte = 16 slots, 0x80-byte = 32 slots), unused slots filled with
    0xFFFFFFFF, each used slot pointing at a packed sub-file.
  * the singletons decode by their own headers.

Emits members/loader-bound-census.tsv and prints the per-family summary.

Usage: gen_loader_bound_census.py [vbf-path]
"""
import io, os, sys, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "..", "agent_flow", "tools")))
import vbfextract as V

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]

# family -> (request kind, subtype, loader, binder/callback)
FAMILIES = [
    ("texpack_ys",         "7/0xD6", "002467A0", "00246A10"),
    ("tex2pack_ys",        "7/0xD7", "00280750", "00280740->00280670"),
    ("mrppack_ys",         "7/0xD3", "002808D0", "002808D0 loop"),
    ("clutpack_ys",        "7/0xD4", "002808D0", "00280AD0"),
    ("fontpack_fs",        "7/0xD2", "003658F0", "003643A0"),
    ("fontpack_it",        "7/0xD5", "0039C3F0", "0039C150"),
    ("menuhandbook",       "7/0xC8", "003158B0", "->022C2550"),
    ("menuhandbook_order", "7/0xC9", "00572D80", "->rbx+0x1200"),
    ("mini_guest_face",    "7/0x0D", "0035C5B0", "->022CA470"),
    ("fontcolor",          "7/0x05", "0029CED0", "002DD810"),
    ("monotone_chr",       "7/0x74", "002C8EE0", "002C9040"),
    ("summoneffectdata",   "9/0x2A", "003B53C0", "->02AD9B60"),
    ("behindcamera",       "9/0x03", "00259DF0", "00259370->00259FE0"),
    ("pc_skillmotion",     "9/0x05", "003DCBC0", "003DC330"),
]

PACK_FAMILIES = {"texpack_ys", "tex2pack_ys", "mrppack_ys", "clutpack_ys",
                 "fontpack_fs", "fontpack_it"}


def directory(blob):
    """Read the u32 self-relative-offset directory. Returns (slots, dir_bytes)
    where slots are the used entries in order and dir_bytes is the directory
    span (the first used offset, or 0)."""
    offs = []
    first = None
    for i in range(0, 64):
        v = U32(blob, i * 4)
        if v == 0xFFFFFFFF:
            continue
        if v >= len(blob):
            break
        if first is None:
            first = v
        offs.append(v)
        if i * 4 + 4 >= first:
            break
    return offs, (first or 0)


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    out = ["family\tfile\tsize\theader\tused_slots\tdir_bytes\tsub_magics\t"
           "kind_subtype\tloader\tbinder"]
    for fam, ks, loader, binder in FAMILIES:
        files = sorted(p for p in names
                       if os.path.basename(p).lower() == fam + ".bin")
        slot_hist = collections.Counter()
        for p in files:
            b = V.read_entry(f, names, blocks, p)
            magic = b[:4].decode("latin-1").replace("\t", " ")
            slots, dirb = "", ""
            if fam in PACK_FAMILIES:
                offs, dirb = directory(b)
                slot_hist[len(offs)] += 1
                mags = ",".join(
                    b[o:o + 4].decode("latin-1").replace("\t", " ")
                    for o in offs)
                slots = str(len(offs))
            else:
                mags = ""
            out.append("\t".join(map(str, (
                fam, p.replace("/", "\\"), len(b),
                "0x" + b[:4].hex() if not magic.isprintable() else magic,
                slots, hex(dirb) if dirb else "", mags,
                ks, loader, binder))))
        print(f"{fam:20} files={len(files):2} slot_hist={dict(slot_hist)}")
    tsv = os.path.join(HERE, "loader-bound-census.tsv")
    with open(tsv, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote", tsv, len(out) - 1, "rows")


if __name__ == "__main__":
    main()
