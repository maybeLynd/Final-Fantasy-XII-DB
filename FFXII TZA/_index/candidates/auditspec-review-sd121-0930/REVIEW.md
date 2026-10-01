# SWE2-AUDIT-SPEC review of SD-121 (sd121-effect-actor-slots-0930, OPUS, 06230b6a0): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `06230b6a0` (the record's only commit), [README](../sd121-effect-actor-slots-0930/README.md) and
`sd121_slots.py`. Measured at HEAD 17a959c94 (resumed from a parked draft measured at 3cae47364). Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD121-0930 | sd121-effect-actor-slots-0930 | `06230b6a0` | ACCEPT-WITH-NARROWING |

The answer stands: the three arrays are 64-slot tables of packed actor handles, filled by `effectactor` /
`bgeffectactor`, and read by the effect elements `003A40F0` / `003A4220`. Two sentences overreach: "the writers are
four script verbs" (S3), and "the readers resolve the handle and anchor at the actor's position" (S5).

**Re-run.** [rerun_sd121_slots.out](rerun_sd121_slots.out) (at 3cae47364) and
[rerun_sd121_slots_head17a959.out](rerun_sd121_slots_head17a959.out) (at 17a959c94) are both identical to the committed
`sd121_slots.out`, ignoring CR. S1-S5 PASS, `FAILS 0`. Package dir clean after re-run: yes
(`git status --porcelain` on it prints nothing).

**Re-derived independently.** The census is [sd121_indep.py](sd121_indep.py) / [.out](sd121_indep.out), which uses
the lane's `ov31_indep.py` loader, not retool. A re-run at 17a959c94 reproduced the `.out` byte for byte. The bodies
were read with `b8dis.py`: [dis_writers.out](dis_writers.out), [dis_accessors.out](dis_accessors.out),
[dis_readers.out](dis_readers.out), [dis_resolve.out](dis_resolve.out), [dis_callsites.out](dis_callsites.out),
[dis_94b0_a.out](dis_94b0_a.out) and [dis_94b0_b.out](dis_94b0_b.out). Callers were cross-checked against rawcalls.json
in [rawcalls_check.out](rawcalls_check.out).
- **S1 and S2 hold.**
  - **rip form.** 18 rip sites land in the arrays, all inside the ten accessors S1 names.
  - **image-base form.** Of 62 image-base hits in 022D9000..022DA000, only the reset's three stores
    (`0036E414` / `0036E42F` / `0036E44C`, base `lea r9, [00120000]` at `0036E3B3`) land in the arrays.
  - **Stored pointers.** 0 DIR64 slots point into the window. The 24 aligned rva32 values there are all
    displacement bytes inside instructions that are already listed.
  - **Accessor bodies.** Get is `cmp ecx, 0x3f; ja` (unsigned, so a negative slot also returns 0). Set clamps the
    slot to 0..63. The clears store 0.
- **S4 holds, polarity read.**
  - `00352297 cmp byte [rbx+0x15], 3` / `jne 003522B0`, so ==3 falls through to `003522AB jmp 0036E880` (sets
    `022D99B0`), and any other value takes `003522BA jmp 0036E7E0` (sets `022D97B0`).
  - The value is `003589B0(00263F10(ctx))`, which packs `((w[+0x16]&0x7FF)<<4 | b[+0x15]&0xF) << 16 | w[+0]`.
  - `clear_effectactor` `00342010` uses the same `+0x15 == 3` split (`0034202E` / `00342038`).
  - The verb ids agree with the image. The handlers' abs64 slots `01EEFBE0` (0x126), `01EF8500` (0x56F), `01EF8520`
    (0x570) and `01EF8540` (0x571) sit 0x20 apart per id, which fits one table.
- **S3 overreaches: two more zero-writers, both outside the verbs.**
  - **`0036E080`** is called only from `00262997`, in the area unload `002628B0`, with `ecx = edi`, the unloaded area
    index (records of 0x288 bytes at `02098E10`).
    - It walks **all three** arrays (`lea` at `0036E086` / `0036E0D1` / `0036E110`).
    - It zeroes each non-zero slot whose handle bits 16-19 equal the argument (`shr eax,0x10; and eax,0xf; cmp r9d,eax`).
      By `003589B0`'s packing, those bits are the actor's `+0x15` nibble.
    - The README's Limits bullet ("the first two arrays") is wrong. So is the world-tick page line it came from, whose
      `0036E080` update says "dual-table ... `022D97B0`/`022D98B0`"; that page's own table row (line 538) says
      "triple".
  - **`0036E3B0`** (the reset) is called only from `0026CA57`, in `ActorManager_BindLoadedDefinitionPayload`
    (`0026C8C0`).
  - Neither accessor has jcc callers or data slots. rawcalls.json agrees on every caller.
  - So the verbs are the only **non-zero** writers. The zero-writers are the two clear verbs, the unload clearer and
    the reset.
- **S5 overreaches: the position is copied only for actors without a battle record, and only by `003A40F0`.**
  - **Table choice** is as S5 says: mask `0x7000`, compare `0x3000` (bits 12-14 == 3) → `022D99B0`; else byte +0 of
    the object `[02F97348]` points to == 2 → `022D98B0`; else `022D97B0`. A zero slot in `99B0` / `98B0` also falls
    back to `97B0` (`003A4137` / `003A426D`).
  - **How `003A40F0` uses the handle.**
    - It first calls `002E9B80(handle)`. That resolves through `003588B0` and returns dword `[[actor+0xC0]]`, or -1
      when the actor has no `+0xC0` record.
    - **When `002E9B80` returns an index**, the element stores the 0x740-byte record at `[022C6F28] + i*0x740` (null
      when its `+0x284` is 0) and **copies no position** (`003A41D9`..`003A41FA`).
    - **Only when `002E9B80` returns -1** does the element resolve through `003588B0` and call `00265020`. That copies
      three dwords from `[actor+0xB8]` into `+0x30` / `+0x34` / `+0x38`; other pages name `00265020`
      `Actor_GetWorldPosition`.
  - **`003A4220` copies nothing.** It tail-jumps `002E9B80` on the first non-empty slot and returns its index, or -1
      (`003A425A`, `003A427A`).
- **Neighbour block.**
  - Every `022D94B0` record access I read clamps the record index to 0x1F. That covers `0036DDC0`..`0036DFC0`,
    `0036E1E0`, `0036E290`, `0036E320`, `0036E460`, `0036E500`..`0036E5F8`, `0036E8B0` and `0036E9B0`.
  - Two byte writes index the record's `+0x10` bitset by an unclamped id / 8: `0036E2F8` (or) and `0036E01A` (and).
    In record 31, an id of 64 or more would reach `022D97B0`.
  - I did not trace those ids. This is a latent alias, not a shown writer.

**Controls.**
- The rip census must return the ten accessors, and does: a known positive for the form.
- The image-base census must return the reset's three stores, and does: a known positive for the form a rip-only
  census misses.
- rel32 must return `00352270` for `0036E880`, and does.
- The defect the S3 claim is exposed to is an unlisted writer. The package's own S3 check tests callers of the nine
  verb-side accessors only, never of `0036E080` / `0036E3B0`, so it was blind to it. The caller scan here is
  sensitive, and it found both.
- S5's check pins only `003A40F0`'s 003588B0 / 00265020 path. It does not test `003A4220`, and it does not test the
  `002E9B80` branch.

**Citations checked.**
- `00267E10` (slot argument), `00263F10` → `003589B0` (value) and `+0x15 == 3` support S4.
- `003A4118` / `003A4122` / `003A4179` support the table choice.
- `003588B0` / `00265020` / `003A415C` support the position copy, but only for the -1 branch of `002E9B80`.

**Correction wording** (the producer applies it in the README; the register row's one-line summary can stay):
- S3 heading and first sentence:
  > **S3: the non-zero writers are two script verbs; four more paths store 0.** `effectactor` / `bgeffectactor` are
  > the only writers of a handle. Zeroes come from `clear_effectactor` / `clear_bgeffectactor`, from `0036E080`
  > (called by the area unload `002628B0` at `00262997`, it clears in all three arrays every slot whose handle bits
  > 16-19, the actor's `+0x15` nibble, equal the unloaded area index), and from the reset `0036E3B0` (called by
  > `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` at `0026CA57`).
- Limits: replace the `0036E080` bullet with:
  > `0036E080` is read (see S3). It covers all three arrays, not the first two. The world-tick page's "dual-table"
  > line is the source of the old wording.
- S5 "Using the handle":
  > `003A40F0` first maps the handle through `002E9B80` (the actor's `+0xC0` record index). For an actor that has
  > one, the element takes the 0x740-byte record `[022C6F28] + i*0x740` and copies no position. Only for an actor
  > without one does it resolve the handle through `003588B0` and copy `[actor+0xB8]`'s three dwords
  > (`Actor_GetWorldPosition`, `00265020`) into its `+0x30` / `+0x34` / `+0x38`. `003A4220` returns
  > `002E9B80(handle)` (an index, or -1) and copies nothing. An empty slot in the `99B0` / `98B0` table falls back to
  > `97B0`.
- For modding: "follows whichever actor" becomes "is anchored to (or, for an actor with a battle record, bound to the
  record of) whichever actor".
