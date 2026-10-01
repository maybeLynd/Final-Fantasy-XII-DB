"""sd161_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the SD-161 review (2026-09-30).

Not the author's census (objflow.py): ov31_indep.py loader (sha256 asserted) and raw byte scans.
  A  direct references to the field 0216FCDC (window 0216FCC0..0216FCF0): rip-relative, image-base-relative
     (disp32 = VA - 0x120000 on a non-rip base), and abs64 / rva32 anywhere in the file
  B  every rip-relative reference to the record-pointer cell 020927C0 (writes marked W) and what the writers store
  C  every rip-relative / image-base-relative reference that FORMS the address of the save image, the record or
     the field (lea / mov imm) for the targets 02164280, 0216C480, 021BA940 (snapshot) and 02211000 (save buffer):
     these are the only static ways to get a bulk destination pointer into the image without a load of 020927C0
  D  data_refs of 02164280 / 0216C480 / 0216FCDC (stored pointers)
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

FIELD = 0x0216FCDC


def show(rows, lo=None):
    for a, mn, op, sz in rows:
        w = "W" if mn.startswith(("mov", "and", "or", "add", "sub", "inc", "dec", "xor")) and op.split(",")[0].strip().endswith("]") \
            and "ptr [" in op.split(",")[0] else " "
        print("   %s %08X  %s %s  (size %s)" % (w, a, mn, op, sz))


print("A  references into 0216FCC0..0216FCF0")
print("  rip-relative:")
show(T.rip_refs(0x0216FCC0, 0x0216FCF0))
print("  image-base-relative:")
show(T.imagebase_refs(0x0216FCC0, 0x0216FCF0))
for t in (FIELD, FIELD - 0x10):
    print("  data_refs %08X: %s" % (t, T.data_refs(t)))

print("B  rip-relative references to the record-pointer cell 020927C0..020927C8")
rows = T.rip_refs(0x020927C0, 0x020927C8)
show(rows)
print("   (count %d)" % len(rows))
print("  image-base-relative:")
show(T.imagebase_refs(0x020927C0, 0x020927C8))

for tgt, name in ((0x02164280, "save image"), (0x0216C480, "record = image+0x8200"), (0x021BA940, "snapshot"),
                  (0x02211000, "save buffer")):
    print("C  address-forming references to %08X (%s): lea / rip-relative, then image-base-relative" % (tgt, name))
    rr = [r for r in T.rip_refs(tgt, tgt + 1)]
    show(rr)
    show(T.imagebase_refs(tgt, tgt + 1))
    print("  data_refs: %s" % T.data_refs(tgt))
