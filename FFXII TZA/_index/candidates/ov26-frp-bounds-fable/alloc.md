# OV-26, the allocation-failure half: the owner setup does not report a failed copy (FABLE, Claude Opus 5.5, 2026-09-29)

[`alloc.py`](alloc.py) runs A, T, C and S: FAILS 0 ([output](alloc.out)). Static.

**What happens when the copy's allocation fails:**
- **A.** The allocator `0036A100` tries the current arena, then a fallback, and returns NULL only if both fail.
- **T.** The tagged wrapper selects arena 6 and, in mode 0 (copy), passes that result through.
- **C.** The copy setup stores the pointer and the size in the entry's buffer unconditionally. The follow-up call returns 0
  for NULL, so nothing crashes here.
- **S.** The owner setup `00409A60` skips the copy when the buffer is NULL, still records the source size at entry
  `+0x40`, and returns normally.

**So a failed copy leaves an entry with a NULL buffer and a non-zero size, and the caller is not told.** Mode 1 (borrow)
allocates nothing here.

**Not claimed:**
- what a later parse does with the NULL buffer;
- whether shipped play ever exhausts both arenas.

With [the format half](README.md), OV-26 is answered at these scopes. The downstream use of a NULL buffer is the residue.

run: alloc.py at 7d9b5ec17, FAILS 0.
