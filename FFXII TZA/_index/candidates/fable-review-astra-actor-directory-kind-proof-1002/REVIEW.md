# FABLE review: ASTRA actor-directory-kind-proof

- **Packet:** [actor-directory-kind-proof README](../../../_experiments/evidence/actor-directory-kind-proof/README.md)
- **Producer commit:** `317ebd1b8`. The manifest sha256 begins `5c2ebb1d1ec6b576` and equals the committed manifest.
  All 68 members hash as listed. The packet's six captured range hashes, both native table spans and the
  region-switch table equal the certified image's bytes.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every count, ordinal, stamp, binding, preset and request-word claim
  re-derives two ways, from the bytes and from an emulation of the original loops. The map data was re-derived from
  the extracted game file, not from the packet's retained bytes. The archive provenance was re-read from the archive.
  The narrowings make explicit that the preset follows the row index (not the kind), that the initializer cannot
  file `talkhold` / `talkterm` itself, and that the pointer-array bound is a premise. They also record that the
  label agrees for every entry and every language copy, without being the selector. None of them contradicts the
  packet.

## Method

[rv_actordir.py](rv_actordir.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is
copied unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It does not import or
run ASTRA's `prove.py`, `control.py`, `archive-member.py`, capture drivers, freeze or publication scripts, or
`reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes five bodies completely:
  - the allocator `002679F0`, the initializer `00266530` and the filer `00268EA0`, each against one `.pdata` record;
  - the leaves `00266AD0` and `00266BD0`, which have no record. Each is bounded by its closed CFG (direct edges plus
    its own 8-entry jump table, every instruction reached), its rets, int3 / nop padding, and the jump table that
    follows it.
- It takes register-write censuses for every carrier of the ordinal (EBX, R10), row (R10D in the allocator), count
  offset (RDI), table pointer (R8), record pointer (RDX, RBX) and descriptor (R12, RSI).
- It re-derives the descriptor-binding arithmetic and the jump-table targets.
- It takes a census of every direct write through the record that meets `+0x1C`..`+0x1F`, and of every write to
  `+0x0B`.
- **Data.** It parses `D:/FFXII_TZA_extract/ps2data/plan_master/us/plan_map/asp_a/asp_a03/global/asp_a03.ebp` itself:
  - the container's slot 0 is `section_000`;
  - the header `+0x14` count table, the header `+0x18` directory, and the `+0x4C` name pool.

  It also checks the other eight language copies.
- **Provenance.** It reads `FFXII_TZA.vbf` independently (magic, header digest, member record, block list). It reads
  the two compressed blocks at their indexed offsets, compares them with the packet's retained blocks, and decodes
  them strictly.
- **Emulation (unicorn) of the original code over the extract's bytes.**
  - The whole allocator runs, with the harness serving its allocation callback and memset.
  - The initializer runs for ordinal 25, with its two leaves and `0020E600` as shipped. Every other callee, and the
    `003DB280` tail, is replaced by a bare return.
  - The emulation is therefore a second reading of the loops and direct stores only. It says nothing about the
    stubbed callees.
- Controls patch a private in-memory copy of the image, or mutate an in-memory copy of the map bytes. Nothing on disk
  is written. The exe sha256 and the extract file's hash are rechecked at the end.

Raw output: [rv_actordir.out](rv_actordir.out).

## Re-derived (69 checks, 69 PASS, 0 FAIL; 16 controls among them)

### Bodies

| Claim | Result |
|---|---|
| Allocator `002679F0` + 0x1B4 (436 B), initializer `00266530` + 0x59F (1439 B), filer `00268EA0` + 0x1B7 (439 B) | PASS: each decodes exactly, and exactly one `.pdata` record covers each. |
| The initializer exits by a tail to `003DB280` | PASS: no ret. The single exit is the last instruction, `00266530` + 0x59A `jmp 0x3db280`, with RCX = the record (+ 0x57B), followed by int3. |
| Pre-preset `00266AD0` + 0xD3 (211 B) | PASS: it has no `.pdata`. `cmp eax, 7` / `ja` to its ret, then a jump table at `00266BA4`; all 8 targets are instruction boundaries and every instruction is reached. Its one ret (+ 0xD2) is followed by a nop pad, then the table, with int3 before the entry. |
| Preset `00266BD0` + 0x60 (96 B) | PASS: it has no `.pdata`. It dispatches on `+3 & 0x1F` <= 7 through the table at `00266C30`, and every instruction is reached. The last ret (+ 0x5F) abuts the table, with 12 int3 before the entry. |

### Data (re-derived from the extract, US copy)

| Claim | Result |
|---|---|
| 8 rows, counts `[9,11,0,0,0,4,72,0]`, sum 96 | PASS: `section_000` is at file+0x80. WORD +0 is 11, so the stride is 48. The count table is at header DWORD `+0x14` (0x730). The directory at `+0x18` (0xCDF0) holds 96 entries. |
| Ordinal 25 is in row 6, interval 24..95 | PASS (own model): cumulative counts 0, 9, 20, 20, 20, 20, **24**, 96. |
| Actor 25's entry is at section offset `D2A4` | PASS: 0xCDF0 + 4 + 48*25. Its WORD +4 label is 6, its pcId is 0xFF, and its name decodes strictly as CP932 to `ラバナ_通常_NPC01` (raw `8389836f83695f92ca8fed5f4e50433031`). |
| The member is the archive's | PASS. The VBF re-read gives: size 31,196,932,183; magic SRYK; 11,995,716-byte header with the packet's sha256; 89,414 members. Member 45552's record names `ps2data/plan_master/us/.../asp_a03.ebp`: 80,000 B at 24,281,213,565, from block 647240. The two compressed blocks (14,963 + 5,413 B) equal the packet's retained blocks. They decode strictly (zlib eof, no trailing data) to 65,536 + 14,464 B, and the 80,000 B equal the extract's US file (sha256 `e92d2689...`). |
| Native row 6 = kind 3, sub 0, 1760 B; stamp 0x66 | PASS: table `01E0C328` entry 6 = (3, 0, 0x6E0), and (3 << 5) \| 6 = 0x66. Entry 5 is the same (3, 0, 0x6E0); see narrowing 1. |

### The allocator's ordinal induction

| Claim | Result |
|---|---|
| Descriptor and counts | PASS: R12 = [RCX] (`002679F0` + 0x1C), and N = [RCX+0x20] is spilled to [RSP+0x50]. The row count is WORD [desc + DWORD(+0x14)] (+ 0x35) in R13D. R12, R13 and R15 have no other writer except their pops. |
| Entry state: EBX, R10D and RDI are zero; R8 is the native table | PASS: `xor ebp, ebp` (+ 0x1F), then EBX = EBP (+ 0xA4), R10D = EBP (+ 0xA9), RDI = RBP (+ 0xC8). R8 = `01E0C328` (+ 0xCB). RBP is written only at + 0x1F, at the call-loop inc and at the restore. |
| Each inner iteration publishes `pool[1 + old EBX]` and increments EBX | PASS: `movsxd rax, ebx` / `inc ebx` / `mov qword ptr [r14 + rax*8 + 8], rdx` (+ 0x100 .. + 0x105). In the row loop, EBX's only writer is that inc. R14 is the callback's result. |
| Stamps: low five bits from k, upper three from the table kind | PASS: R9B = R10B & 0x1F (+ 0xF1 / + 0xF8), and the table byte is shifted << 5 (+ 0x117 .. + 0x123). |
| Advance by the rounded native size | PASS: RDX += (WORD [R8+2] + 15) & ~15 (+ 0x126 .. + 0x131). This is RDX's only writer in the row loop. |
| The WORD count controls the iteration count; a zero row skips | PASS: R11D = count, `sub r11, 1` / `jne`. `test ecx, ecx` / `jle` goes to the row advance. |
| Outer step: k + 1, count offset + 2, table + 4 | PASS: `inc r10d`, `add rdi, 2`, `add r8, 4`, then `cmp r10d, r13d` / `jl`. Each is its register's only writer in the row loop. Both loop heads have no entries except their fall-in and their back-edge. |
| The same pool and ordinal are passed on | PASS: 00266530(RCX = manager, RDX = pool, R8D = ordinal) for ordinals 0 .. N-1 (+ 0x173 .. + 0x192). |
| The allocator never reads a directory entry | PASS: it touches the descriptor only at +0x14 and the count WORDs (+ 0x3F is an address-only `lea`). |
| **Emulated original allocator** | PASS: pool[0] = N = 96 and all 96 pointers are set, spaced by each row's rounded size. Every +3 stamp equals (kind << 5) \| model row. The ordinals stamped row 6 are exactly 24..95, and ordinal 25's +3 is 0x66. |

### The initializer: selection, binding, preset

| Claim | Result |
|---|---|
| RBX = `pool[1+i]` at `00266530` + 0x3A | PASS: `mov rbx, qword ptr [rdx + r10*8 + 8]`, with R10 = `movsxd r8d` (+ 0x26) and no RDX write before it. RBX is written only there and at the restore. |
| The volatile ordinal carrier survives | PASS: R10 has one writer. Between it and its last use (+ 0x1EF), the only calls are the two leaves, called with RCX = RBX (+ 0x76 / + 0x7E). Both leaves write only RAX, RCX, RDX, R8 and R9, so R10 and R11 (the image base) survive. |
| `actor+0x40 = desc + sDWORD(desc+0x18) + 4 + 48*i` for WORD +0 >= 8 | PASS: + 0x1E0 .. + 0x204. The 32-byte stride applies only below 8. RSI (the descriptor) has one writer before the binding, and RDI is not rewritten on the path. |
| The binding never uses the WORD +4 label | PASS: the initializer reads the entry only at +6, +8, +0x10, +0x14 and +0x18. |
| The pre-preset row-6 path does not overwrite +3 | PASS: row 6 goes to `00266AD0` + 0x84. The body's only writes are record +0xA0, +0xA8, +0xB8 and +0xC0 through RDX = the record, and nothing writes +3. |
| Row 6's preset writes 0x30004 at `00266BD0` + 0x42 | PASS: rows 5 and 6 both go to `00266BD0` + 0x3E. `mov dword ptr [rcx + 0x1c], 0x30004` is a full DWORD store; then `cmp r8b, 5` / `jne` goes to the ret. 0x30004 has bits 16 and 17. |
| The filer tests those masks | PASS: `00268EA0` + 0x3C tests bit 17 (`talkterm`) and + 0x8B tests bit 16 (`talkhold`). |
| Six later direct request-word writes preserve bits 16/17 | PASS: exactly six direct writes meet +0x1C .. +0x1F. All six come after the preset call: `and 0xffffdeff` (+ 0x1C1), `or 4`, `and ~4`, `or 0x400`, `and ~4`, `and ~0x400` (+ 0x50A .. + 0x574). Each AND mask keeps bits 16 and 17. The 0xFFFF fill (`rep stosw`, + 0x380) covers +0xC8 .. +0xEB only. |
| **Emulated initializer for ordinal 25** | PASS: it selects pool[26]. Right after the preset returns, +0x1C = 0x30004 and +3 = 0x66. At the `003DB280` tail, with the seven callees stubbed: +0x40 = descriptor + 0xD2A4, WORD +0 = 25, and +0x1C = 0x30004. |

The callees that remain after the preset and receive the record are `003DB580`, `00265FF0`, `00265B60`, `00268380`
(×2), `002681E0`, `003DBB60` (×2 reached in the emulation; 4 call sites) and `00268EA0` (2 call sites, not reached).
Then comes the tail. They are the packet's open "transitive callbacks".

### Label countermodel and controls

The **countermodel** is a mutated copy of the map in which entry 25's WORD +4 is 7. It changes nothing except the
check that states the label: row 6, 0x66, 0x30004 and the binding all still PASS, both statically and in the
emulation.

A **null control** runs first: an unchanged private image copy plus an unchanged data copy pass all 43 checks of the
control set. Each of the 15 controls below must fail a named check, and all did:

1. Allocator `add rdi, 2` → `add rdi, 4`: the count-WORD stride. Fails the outer-step check and the emulated
   stamps.
2. `inc ebx` → two nops. Fails the publish census. The emulation then faults on the null pool[26].
3. `shl al, 5` → `shl al, 4`. Fails the stamp check and the emulated stamps.
4. The native table pointer + 4. Fails the entry-state check and the emulated spacing and stamps.
5. Initializer `cmp eax, 8` → `cmp eax, 0xC`, so version 11 takes stride 32. Fails the binding check and the
   emulated +0x40.
6. `shl rdi, 4` → `shl rdi, 5` (stride 96). Fails the same two checks.
7. Pool select + 8 → + 0x10. Fails the selection check and the emulated selection.
8. Preset 0x30004 → 0x10004. Fails the preset check and both emulated +0x1C checks.
9. Preset table row 6 → the 0x40 arm. Fails the same checks.
10. Pre-preset row-6 path writes +3. Fails "nothing writes +3" and the emulated stamps.
11. Preset `and r8b` → `and r10b`, which writes the ordinal carrier. Fails the volatile-carrier check. The emulation
    cannot see this one, because 25 & 0x1F = 25.
12. The AND mask at + 0x1C1 clears bits 16/17. Fails the six-writes check and the emulated tail value.
13. Data: count[5] 4 → 6, so ordinal 25 moves to row 5. Fails the counts, the model row and the emulated row-6 set.
14. Data: version WORD 11 → 7. Fails the counts and entry-offset checks.
15. Data: row count 8 → 5, so row 6 is never carved. Fails the counts, the model and the emulation.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`, and the extract file is unchanged. The
packet's own controls (three CLI refusals, seven source mutations, two data refusals, label countermodel) were not
repeated. These replace them for this review.

## Narrowings

1. **The preset follows the row index, not the kind.** The pre-preset and preset switches take `+3 & 0x1F`, which
   is the count-prefix row. Native rows 5 and 6 are identical (kind 3, sub 0, 1760 B), and both reach the 0x30004
   arm; row 5 also sets +0x14 bit 7. Row 7 writes 0x34C85, which also has bits 16 and 17. "Category" in the packet
   therefore means the row. The kind bits never reach the preset.
2. **The initializer does not file `talkhold` / `talkterm` itself.** Its own +0x0B stores clear bit 3 (`and al,
   0xf7`, `00266530` + 0x107), and its two filer calls (+ 0x517, + 0x569) are guarded by that bit. They run only if
   a stubbed callee sets it, and in the emulation the filer was not reached. The bits 16/17 set here are a gate for
   later filer runs, such as the manager entry's own filer call or the `reqenable` / `REQCHG` paths named on the OV-16
   page. Which of those runs first in a natural scene stays open.
3. **The pointer array is not bounded by the counts.** The allocator sizes the pointer array from N = manager +0x20,
   publishes one pointer per counted record with no check against N, and calls the initializer for 0 .. N-1. For this
   file, sum(counts) = 96 = the directory count. That N = 96 at runtime is the packet's premise ("a manager count
   covering ordinal 25"). It is kept as a premise: the binder stores a sum over the same table at +0x20, but its
   accumulator initialisation was not re-read here.
4. **The label agrees throughout, and is still not the selector.** All 96 US entries' WORD +4 labels equal their
   count-prefix rows. The other eight language copies have the same counts, and the same label 6 and name for
   entry 25. This extends the packet's single-entry agreement to the whole file and to all nine copies. The
   countermodel still shows that no instruction on the path reads the label.
5. **"Version 11"** is the WORD at descriptor +0 (the low word of the `0x8000000B` marker). The code compares it only
   against 8 (stride) and 0xA (one later boundary site). OPUS's record-pool contract calls the same WORD an
   entity/field count. The name does not affect the binding.
6. **The leaves have no `.pdata`.** `00266AD0` and `00266BD0` are bounded here by closed jump-table CFGs and padding,
   as the packet's capture ranges also assume.

## Limits (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes with named stubs. The following
remain open and are not awarded:

- the effects of the transitive callees after the preset, and of the `00266530` + 0x59A → `003DB280` tail;
- the record's final live +0x1C flags;
- natural scene initialization, including when and by which caller the filer first runs for this actor;
- the `talkterm` wait, cancel, reentry and receipt timing (OV-16's live fact);
- allocation placement, ownership, lifetime, loaded-pointer identity and malformed-input safety;
- whether every shipped directory's labels match its rows (checked here for this file only);
- a complete archive hash: only header, member and block identity are certified. The extract file equals the
  archive member.

Valid, stable, disjoint descriptor, pool and frame storage, adequate allocation and the normal native ABI are
premises.

run: `rv_actordir.py` at HEAD e828e3f50 (69 checks, 69 PASS, 0 FAIL, 16 controls; output identical to [`rv_actordir.out`](rv_actordir.out))
