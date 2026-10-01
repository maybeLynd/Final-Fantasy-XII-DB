#!/usr/bin/env python3
"""Byte-level census of the ActorDefinitionPayload (EBP2 section-0 image)
header over every shipped .ebp container in FFXII_TZA.vbf, for
OPUS-REQ-DATA-ACTORDEFINITIONPAYLOAD-HEADER-GAPS.

The payload is the 0x90-byte header of EBP2 section 0, always at file
+0x80 (every shipped container's slot-0 offset is 0x80; the slot-0
offset cell at file +0x10 is verified anyway).  +0x00 of the section is
the 0x8000000B magic, +0x04 the in-section size.  The binder is
ActorManager_BindLoadedDefinitionPayload (0026C8C0), reached from
ActorResource_OnDefinitionPayloadLoaded (0032F850).

For each of the first 0x4C bytes of the section-0 header, classifies the
offset across the whole corpus as:
    ZERO      - 0x00 in every file
    CONST     - the same non-zero byte in every file
    VARYING   - at least two distinct byte values
and emits a per-offset TSV row plus a value histogram for varying and
constant offsets.  No semantics are inferred.

Usage: gen_actdef_header_census.py [vbf-path]
    -> writes actdef-header-census.tsv beside this script.
"""
import io, os, sys, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "..", "..", "agent_flow", "tools")))

import vbfextract as V

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

HDR = 0x4C


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    ebps = sorted(p for p in names if p.lower().endswith(".ebp"))
    files = 0
    skipped = collections.Counter()
    distinct = [set() for _ in range(HDR)]
    slot0_off = collections.Counter()
    slot0_magic = collections.Counter()
    rows = []
    for path in ebps:
        try:
            b = V.read_entry(f, names, blocks, path)
        except Exception:
            skipped["read-error"] += 1
            continue
        if len(b) < 0x80 + HDR:
            skipped["short-file"] += 1
            continue
        off0 = struct.unpack_from("<I", b, 0x10)[0]
        slot0_off[off0] += 1
        if off0 + HDR > len(b):
            skipped["short-section"] += 1
            continue
        magic = struct.unpack_from("<I", b, off0)[0]
        slot0_magic[magic] += 1
        if magic != 0x8000000B:
            skipped["bad-magic"] += 1
            continue
        files += 1
        for i in range(HDR):
            distinct[i].add(b[off0 + i])

    out = os.path.join(HERE, "actdef-header-census.tsv")
    w = io.open(out, "w", encoding="utf-8", newline="\n")
    w.write("offset\tclass\tdistinct\tvalues\n")
    for i in range(HDR):
        vals = sorted(distinct[i])
        if len(vals) == 1 and vals[0] == 0:
            cls = "ZERO"
        elif len(vals) == 1:
            cls = "CONST"
        else:
            cls = "VARYING"
        if len(vals) <= 16:
            vs = ",".join("%02x" % v for v in vals)
        else:
            vs = ",".join("%02x" % v for v in vals[:8]) + \
                ",...," + ",".join("%02x" % v for v in vals[-4:]) + \
                " (%d distinct)" % len(vals)
        w.write("+0x%02X\t%s\t%d\t%s\n" % (i, cls, len(vals), vs))
    w.close()

    print("files=%d  skipped=%s" % (files, dict(skipped)))
    print("slot-0 offsets:", dict(slot0_off))
    print("slot-0 magics:", {hex(k): v for k, v in slot0_magic.items()})
    counts = collections.Counter()
    for i in range(HDR):
        vals = distinct[i]
        counts["ZERO" if vals == {0} else
                "CONST" if len(vals) == 1 else "VARYING"] += 1
    print("classes:", dict(counts))
    print("wrote", out)


if __name__ == "__main__":
    main()
