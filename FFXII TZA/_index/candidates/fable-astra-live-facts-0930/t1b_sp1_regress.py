# t1b_sp1_regress.py - regression for t1b_sp1_counts.py's terminal status (ASTRA-CONTRA-FABLE-OV33-SP1-PREREQUISITE-0930).
# Part A runs the producer as a subprocess, exactly as ASTRA did (sp1-prerequisite-02), on two fixtures copied from
# ASTRA's disclosed inputs (sha256 as in its result.json):
#   A1 two_nonmpk_entries.vbf (fe50bd5a...): a valid VBF index with two non-.mpk entries -> must exit 2 with
#      "STATUS INCOMPLETE", and print no "FAILS" line (the defect: MISMATCH (0,0,0) then "FAILS 0", exit 0);
#   A2 corrupt_magic.vbf (0054cc9f...): bad archive magic -> must exit non-zero with no STATUS COMPLETE.
# Part B calls census()/verdict() on synthetic pack bytes for the malformed cases a VBF fixture cannot easily hold:
#   B1 an offset array running past the block; B2 a referenced record past the block; B3 a truncated pack header;
#   each must yield an INCOMPLETE reason. B4 is the sensitivity control: one well-formed pack gives no malformed reason
#   (only the corpus-control mismatch, since one record is not 2,326).
# Prints PASS/FAIL per case; exit 0 only if every case passes.
import sys, os, subprocess, struct, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "t1b_sp1_counts.py")
FX = os.path.join(HERE, "sp1_fixtures")
sys.path.insert(0, HERE)
import t1b_sp1_counts as P

fails = 0


def check(name, ok, detail):
    global fails
    fails += (not ok)
    print("%-4s %s  %s" % ("PASS" if ok else "FAIL", name, detail))


def run(fx):
    r = subprocess.run([sys.executable, "-B", PROD, os.path.join(FX, fx)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


for fx, want in (("two_nonmpk_entries.vbf", "fe50bd5aed88d761a094e911f596ec3006728abbdddb8eacb855a0bc698cd94f"),
                 ("corrupt_magic.vbf", "0054cc9fa2a031e8e89d9a47447940b0acf970f4421ddd1e8d3c296c277ddb80")):
    got = hashlib.sha256(open(os.path.join(FX, fx), "rb").read()).hexdigest()
    check("fixture " + fx, got == want, got[:16])

rc, out, err = run("two_nonmpk_entries.vbf")
last = out.strip().splitlines()[-1] if out.strip() else ""
check("A1 no-.mpk corpus", rc == 2 and last.startswith("STATUS INCOMPLETE") and "FAILS" not in out,
      "exit %d, last line %r" % (rc, last))
rc, out, err = run("corrupt_magic.vbf")
check("A2 corrupt magic", rc != 0 and "STATUS COMPLETE" not in out, "exit %d, %s" % (rc, err.strip().splitlines()[-1:]))


def pack(sp1):
    """A pack whose only non-empty slot is 16, holding sp1 (layout as slot16() reads it)."""
    sz = [0] * 32; sz[16] = len(sp1)
    hdr = struct.pack('<I32I', 32, *sz)                 # cnt = 32 slots, so the data area starts past the 0x84-byte header
    off = ((32 + 1) * 4 + 0x3F) & ~0x3F
    body = hdr.ljust(off, b'\0') + b'\0' * 0x40 + sp1
    return body


def sp1(bound, offs, size, rec=None):
    b = bytearray(size)
    b[0:4] = b'SP1\0'; struct.pack_into('<I', b, 0x0C, 0x20)
    struct.pack_into('<H', b, 0x20, bound)
    for i, o in enumerate(offs):
        if 0x22 + 2 * i + 2 <= size:
            struct.pack_into('<H', b, 0x22 + 2 * i, o)
    if rec is not None:
        o, shape, n = rec; b[o + 9] = shape; struct.pack_into('<I', b, o + 0x14, n)
    return bytes(b)


def reasons(entries):
    r = P.census(entries)
    return P.verdict(r)[1] + ["records %d shape2 %d" % (r["recs"], r["shape"][2])]


why = reasons([("m/b1.mpk", pack(sp1(200, [0x40], 0x60)))])
check("B1 offset array past the block", any("bad_index" in w for w in why), why)
why = reasons([("m/b2.mpk", pack(sp1(1, [0x50], 0x60)))])
check("B2 referenced record past the block", any("bad_ref" in w for w in why), why)
why = reasons([("m/b3.mpk", b'\x01\0\0\0' + b'\0' * 8)])
check("B3 truncated pack header", any("bad_pack" in w for w in why), why)
why = reasons([("m/b4.mpk", pack(sp1(1, [0x40], 0x80, rec=(0x40, 2, 5))))])
check("B4 control: well-formed pack", not any(k in w for w in why for k in ("bad_pack", "bad_index", "bad_ref"))
      and any("control mismatch" in w for w in why) and "records 1 shape2 1" in why, why)
print("REGRESSION", "PASS" if not fails else "FAIL (%d)" % fails)
sys.exit(1 if fails else 0)
