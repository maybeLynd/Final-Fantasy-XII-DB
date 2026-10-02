# FABLE review: render-slot self-index, cursor and publication order (ASTRA `aac0489ac`)

**verdict: ACCEPT-WITH-NARROWING** (FABLE, Claude Opus 5.5, 2026-10-02). Request
`ASTRA-REQ-FABLE-RENDER-SLOT-IDENTITY-PUBLICATION-1002`. FABLE did not author this packet. The packet is
[`_experiments/evidence/render-slot-identity-publication/`](../../../_experiments/evidence/render-slot-identity-publication/README.md),
producer commit `aac0489ac`.

## What was re-derived

[`rv_slot.py`](rv_slot.py) -> [`rv_slot.out`](rv_slot.out): 120 PASS, 0 FAIL, exit 0. The script uses FABLE's own reader,
[`rvlib.py`](rvlib.py), built on `struct` and capstone 5.0.7. It does not import ASTRA's `prove.py` or the shared role
adapter. It checks the image sha256 `73461d089620...` and the packet manifest (sha256 `a2bcea12693d...`; all 81 members hash as
listed).

- **Bodies.** `0041F730`, `00420480`, `004269A0` and `004279B0` decode exactly to 1208, 977, 741 and 329 bytes, 3255 bytes
  in total. Each local CFG is closed, and `.pdata` tiles each body as one function. `004279B0` is four records: one root
  and three chained records.
- **Per-record clear, `0041F730`.** It calls `00861EC0`, the IAT thunk for `memset`, with rcx = arg0, edx = 0 and
  r8d = 740h. It then sets ebp = -1 at `0041F768` and stores `mov word ptr [rbx], bp` at `0041F795`. That store is a WORD
  at +0, and `0041F768` dominates it.
- **Reset, `004269A0`.** It loads the pool from `022C6F28` and calls `0041F730` 160 times at stride 740h. It then writes a
  QWORD of 0 at +48808h (`004269ED`), which covers the DWORD cursor at 48808h and the DWORD live count at 4880Ch.
- **Allocator, `004279B0`.**
  - The only compares before the first clear call (`00427A13`) are the name-lookup result at `004279DC` and the signed
    count gate at `004279E9`/`004279F3` (`jge` against 160).
  - The cursor is read by `movsxd` (a signed DWORD) at `004279FA`, and the record is base + cursor * 740h. No compare
    bounds the cursor.
  - `00427A4D` is `mov word ptr [rdi], si`, a WORD write at +0. rsi and rdi have no in-body writer between `00427A0D` and
    that store.
  - The dominance chain is clear `00427A13` -> self-index `00427A4D` -> `00420480` call `00427A71` -> +290h bit 0
    `00427A76` -> count `inc` `00427A7F`.
  - In the scan (`00427A9E`..`00427ADA`), eax = 0 throughout, the cursor wraps at 160 to 0, and the loop's only exit is a
    row whose DWORD +284h equals 0.
- **Metadata, `00420480`.** The first non-stack access is `or dword ptr [rcx + 0x284], 0x2010f9` at `0042049A`. rcx is
  unchanged before it, and it dominates every call in the body. The direct writes that overlap +0 or +284h are only the
  two ORs at `0042049A` and `004204EF`. The body has no indexed non-stack writes.
- **Forwarding.** In the factory, r14 = arg0 (`0041F361`). `0041F608` does `movsx edx, word ptr [r14]` and passes it to
  `00372350`, which stores it at rig +68h (`00372383`). `004216D3`/`004216DB` do the same for rig +6Ch.
- **Mathematical controls.** These are fixed-width Python models, not 160 machine-code runs.
  - From any cursor 0..159, the scan stays in 0..159, and 160 visits cover every row once and end at the start cursor.
  - With one stable zero flag, at any of 160 positions and from any of 160 starts, the scan stops within 160 visits.
  - With every flag nonzero, it does not stop in 1600 visits.
  - Count 0 passes the gate, but cursor -1 or 160 gives a record offset outside the 160-row pool.

## Controls (each must be rejected, and is)

Each control reruns the relevant claim group on a privately patched copy of the image. All are rejected:
- count cap 160 -> 159 (`004279EF`);
- the self-index WORD store widened to a DWORD;
- a cursor compare inserted before the clear;
- the `0042049A` OR turned into an AND;
- the memset size changed to 73Fh;
- the reset loop count changed to 159;
- a deliberately wrong `.pdata` end.

Known answer: `66 89 37` is a WORD write and `0F 11 01` is a 16-byte write. **Instrument defect found:** capstone 5.0.7
flags `0F 11 01` (`movups [rcx], xmm0`) as a read only. rvlib therefore treats a destination memory operand as written. The
`.out` records this. ASTRA's adapter has the same correction as a control.

ASTRA's own `prove.py` also passes when run with its output redirected to scratch (`PROVED ...`). This review does not rely
on it.

## Narrowing

- **The self-index is not the slot's first publication.** Before `00427A4D` writes WORD [record+0] (which the clear left at
  the all-ones WORD), the allocator writes the new index into the pool list:
  - list head +48810h (`00427A21`) on the empty-list path;
  - otherwise the old tail row's WORD +4 (`00427A37`) and the new row's +2 (`00427A43`);
  - then list tail +48814h (`00427A47`), which dominates `00427A4D`.

  The packet's order of ID, then active flag, then count is correct but omits these list writes. A consumer must not write
  "the ID is written first". It may write "the ID precedes the active flag (+284h) and the live count".
- "Clears 160 rows" means 160 calls of `0041F730`. That is a memset followed by the body's own direct sentinel and default
  writes, so a row is not all-zero after the reset. The +0 field is the all-ones WORD, and this body has no direct write
  to +284h after the memset.

## Scope (kept as the packet states it)

These are conditional static source facts. Not awarded:
- natural cursor values and initialised state;
- the `004278E0` name-lookup result (assumed, as the packet says);
- the effects of opaque callees (`0020E600` and the callees of `00420480`; memset is identified only by its import
  name);
- aliasing, atomicity and scheduling;
- all-writer coherence of the cursor, count, flags or list;
- lifetime.

The invalid-cursor and all-flags-set cases are countermodels, not observed faults or hangs. The packet's wording stays
within this scope, apart from the omission narrowed above.

run: rv_slot.py at 1f193fec9
