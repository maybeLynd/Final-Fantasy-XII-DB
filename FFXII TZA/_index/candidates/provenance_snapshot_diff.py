"""fas2_diff.py A.fas2 B.fas2 : per-function diff of two GFZFunctionAnnotationSnapshotV2 files (magic GFZANN2).
Each record: entry, name, namespace, symbol source, plate comment, repeatable comment, prototype string, signature source,
calling convention, inline/noreturn/varargs/thunk flags, thunk target, body ranges, tags (name + tag comment).
Prints the count of functions, the entries whose records differ, and per differing field how many functions moved."""
import struct, sys, collections

FIELDS = ["name", "namespace", "symsource", "plate_comment", "repeatable_comment", "prototype", "sigsource", "callconv",
          "flags", "thunk_target", "body_ranges", "tags"]


def rd_str(b, o):
    n = struct.unpack_from(">i", b, o)[0]
    o += 4
    if n < 0:
        return None, o
    return b[o:o + n].decode("utf-8", "replace"), o + n


def parse(path):
    b = open(path, "rb").read()
    assert b[:8] == b"GFZANN2\0", path
    ver, count = struct.unpack_from(">ii", b, 8)
    o = 16
    out = {}
    for _ in range(count):
        ln = struct.unpack_from(">i", b, o)[0]
        o += 4
        r = b[o:o + ln]
        o += ln
        p = 0
        entry = struct.unpack_from(">q", r, p)[0]
        p += 8
        vals = []
        for _k in range(8):
            s, p = rd_str(r, p)
            vals.append(s)
        flags = r[p:p + 4]
        p += 4
        thunk = struct.unpack_from(">q", r, p)[0]
        p += 8
        nr = struct.unpack_from(">i", r, p)[0]
        p += 4
        ranges = []
        for _k in range(nr):
            ranges.append(struct.unpack_from(">qq", r, p))
            p += 16
        nt = struct.unpack_from(">i", r, p)[0]
        p += 4
        tags = []
        for _k in range(nt):
            a, p = rd_str(r, p)
            c, p = rd_str(r, p)
            tags.append((a, c))
        assert p == len(r), ("record length", hex(entry))
        out[entry] = vals + [flags, thunk, tuple(ranges), tuple(tags)]
    assert o == len(b), "trailing bytes"
    return out


A = parse(sys.argv[1])
B = parse(sys.argv[2])
print("functions:", len(A), len(B), "entry sets identical:", set(A) == set(B))
moved = collections.Counter()
diff_entries = []
for e in sorted(set(A) & set(B)):
    fs = [FIELDS[i] for i in range(len(FIELDS)) if A[e][i] != B[e][i]]
    if fs:
        diff_entries.append((e, fs))
        for f in fs:
            moved[f] += 1
print("functions whose record differs:", len(diff_entries))
print("fields moved:", dict(moved))
for e, fs in diff_entries[:40]:
    print("  %08X %s" % (e, ",".join(fs)))
if len(sys.argv) > 3:
    open(sys.argv[3], "w").write("\n".join("%08X\t%s" % (e, ",".join(fs)) for e, fs in diff_entries) + "\n")
