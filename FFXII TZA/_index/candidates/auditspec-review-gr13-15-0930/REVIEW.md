# SWE2-AUDIT-SPEC review of GR-13 / GR-14 / GR-15, the shop list rows and list kinds (OPUS lane SWE2-STRUCT, 9c71391a8): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). This
resumes a parked draft; its STATE notes (removed on publication) are superseded by this record. Reviewed:
[`gr13-15-shop-list-widget-0930/`](../gr13-15-shop-list-widget-0930/README.md) at `9c71391a8`, measured at HEAD
`48de14c6b`. The evidence is static, from the certified image (sha256 asserted by the lane loader `ov31_indep.py`).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-GR13-15-0930 | `_index/candidates/gr13-15-shop-list-widget-0930/` | `9c71391a8` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_gr13_15_shop_list_check.out](rerun_gr13_15_shop_list_check.out) is identical to the committed `.out`
when CR is ignored. It prints `FAILS 0`. After the re-runs, `git status --porcelain` on the package directory is empty.

**Re-derived independently.** Scripts: [gr1315_indep.py](gr1315_indep.py) / [.out](gr1315_indep.out),
[gr1315_q2.py](gr1315_q2.py) / [.out](gr1315_q2.out), [gr1315_q2b.py](gr1315_q2b.py) / [.out](gr1315_q2b.out),
[gr1315_q2c.py](gr1315_q2c.py) / [.out](gr1315_q2c.out), [gr1315_fwd.py](gr1315_fwd.py) / [.out](gr1315_fwd.out) and
[gr1315_rest.py](gr1315_rest.py) / [.out](gr1315_rest.out). None of them uses retool or structflow.

- **GR-13 layout A.** Re-based to the entry, `0057DAD0` stores:
  - a qword at `+0` (`0057DB98`);
  - the id word at `+8` (`0057DB7E`);
  - a byte at `+0xA`;
  - words at `+0xC` and `+0xE`;
  - the dword at `+0x10` (`0057DB9F`, `0057DBCC`, `0057DBE0`).

  This confirms A1.
- **The 14 price reads.** All 14 are dword reads at `+0x10`. Five are `cmp ..., 0x80000000` and nine are
  `btr ..., 0x1f`. This matches A4a/A4b.
- **The price-reader census, image-wide (gr1315_q2, which replaces the parked draft's blind Q sweep).**
  - **Method.**
    - Every qword load `mov|add r64, [base+0xC8|0xD0|0xE0]` is a seed: 865 loads in 445 .pdata functions.
    - A forward may-taint dataflow runs over each function's whole CFG. It covers every .pdata chunk, takes the union at
      joins, and follows 8-byte stack slots.
    - It is interprocedural: a tainted rcx/rdx/r8/r9 at a call or tail jmp taints the callee (6 rounds).
  - **Positive control: 14 of 14 package sites found.** The old 24-instruction window found 1.
  - **Inside the UI windows.** The only other `+0x10` accesses through a holder-derived register are:
    - family-A bodies the package already names: `005651E0` (message 26) and `00565BD0` (whole-row moves);
    - widgets with other procedures:
      - `0056A1D0` / `0056A890` / `0056AE80` / `0056B100` sit under procedures `005691E0` (0x368-byte widgets,
        installed at `00568B80`) and `0056B4D0` (a 0x5A8-byte widget, installed at `0056B3BE`). Their word ids are at
        `+0x10` / `+0x12`, which is not the shop row layout.
      - `0057FB00` sits under `0057F8C0`.
    - the equip menu's own row callback `003FF1F0`: a qword read, lea'd at `003FF648`.
  - **Outside the UI windows.** There are 12 dword hits, in 8 roots. Seven roots are seeded by their own holder loads.
    The eighth, `0085E740`, is fed from `0085EA40`. None is fed from the shop family.
  - **What the shop family's tainted values reach.** Their only stores are `0056E55A` (`+0xC8`) and `0056D56F`
    (`+0xD0`). The callees that receive them are the known helpers, plus `003697F0`, `003933B0` and `00567690`. None of
    those touches `+0x10`. So A4's "14 readers" holds image-wide for holder-derived reads.
- **GR-14 reach.**
  - `005651E0` is entered only by the 4 tail jmps.
  - The 4 list procedures are named only by the 4 leas in `00564B90`, and `0056E140` only by `0056DD65`.
  - None of these has a jcc, an abs64 or an image-base form.
  - Every rva32 hit of these targets is a `.pdata` BeginAddress or a chained-unwind RUNTIME_FUNCTION (R2 / R2b). The
    one exception is an unaligned `.data` byte match (`01DFC587`).
  - `0056E140` sends message 26 (msg-1 = 25 > 0x13) to `005C5230` (`xor eax, eax / ret`).
- **The message-26 forward hop (not stated by the package).**
  - `002D2600` and `002D28E0` send 26 with `call [control]`, where control = r8 = `[helper+0x10]` (`002D279E`,
    `002D2B5C`). The same control's `+0x120` is the row callback that the driver installs at `0056D7EE`.
  - The control's procedure is `002D2DB0`, installed at `002D14ED`. It forwards 26 (`002D2DFF cmp ecx, 0x15` =
    msg - 5) to the procedure of `[control+0xC8]` (`002D2E11`..`002D2E29`).
  - For the shop's list control, `+0xC8` is set at creation. The chain is `0056D776 mov r9, rdi` (the driver) →
    `002432B0` (`002432CB mov r13, r9`) → `00243488` → `0029F930` (`0029F9AC` descriptor `+0x28` = r8) →
    `002D14E0` (`002D16B0 mov [rbx+0xc8], rax` from descriptor `+0x28`).
  - So the hop lands on the driver `0056D370`, whose message 26 goes to the stub (`0056D3B8`). B6's conclusion stands,
    but its route skips this hop.
- **K (`+0x17F`).**
  - Image-wide there are exactly two byte stores, `005647B4` and `003FD371`. The draft's `002D8442` is a misdecode of
    `002D8443 mov edx, 0x17f`.
  - Word stores at `+0x17E` exist outside the 97-function closure:
    - `005527E8` in widget procedure `00552250` (lea'd at `00550449`) writes back the value it read at `005527B7`;
    - `00311834` is in battle code `003112F0`.

  Neither is a family-A/B/C widget. C4's closure-scoped "any width" claim stands.
- **GR-15 tables.**
  - `00D23920` read as u32 is `0x5AF, 0x5A2, 0x5AE, 0`. The loop bound is `0057BEA0 cmp esi, 3`. The index is
    `0057C0F7`/`0057C0FE` `[rax+rsi*4]`.
  - `00D233A0` gives 0x5AF→32, 0x5A2→19 and 0x5AE→31, and 0x405..0x409 / 0x40D..0x40F → 0..7.
  - `00D0F990` as i32 is `4, -1, 7, 6, 5, 8, 9, 10`.
  - `003FDA20` has a sole caller, `003FF0A2`, and `003FF040` has a sole caller, `003FF765`. Neither has jcc, rip or
    abs64 references. The only rva32 hit is `.pdata`.
  - `003FE30B`..`003FE324` decode as C3a says.

**Controls.**
- The Q2 census is checked by the 14 known sites (sensitive to a short window or a missing interprocedural step). The
  old window scored 1/14.
- R is checked by `00563721` and `00564C0A` (both found).
- K is checked by the two known byte stores. Both were found; one sits under a prefix-shifted decode.
- The forward-hop read has no separate positive control: it is a direct read of the four stores named above.

**Citations checked.**
- `0056D66E`..`0056D6A5` and `0056D7EE` install the callbacks and set the control's `+0x120`.
- `0056DD66`, `00563721`/`53`/`41`/`43` and `00564C0A`..`25` all say what the README says.
- B6 cites `002D279E` / `002D2B5C` correctly, but "the target's own procedure" is `002D2DB0` (the control), not the
  shop's.

**Runtime routing.** GR-15 Limits routes family C's upper bound ("read `+0x17E` of the equip-slot list widget").
Static evidence can settle this: the question is whether the 5-row list control can report a row index of 5 or more,
which is the control's cursor clamp. It was not read here or by the package. It does not affect any selector overlap
with the shop family.

**Correction wording.** In README GR-14's last bullet and step B6, replace "They call the target's own procedure" with:

> They call the list control's procedure (`002D2DB0`, `002D279E` / `002D2B5C`), which forwards message 26 to the
> procedure of the control's `+0xC8` (`002D2E11`–`002D2E29`). For the shop's list control, that is the driver
> `0056D370`: it is set at creation from the layout loader's owner argument (`0056D776` → `002432CB` → `0029F9AC` →
> `002D16B0`). The driver sends message 26 to the stub (`0056D3B8`).

In B6's check text, "whatever target, the shop widget and the driver route it to the stub" should read "the shop list
control forwards it to the driver, which routes it to the stub".

Package-gate note: A4a's census is closure-scoped. The image-wide dataflow above supports the same 14, so no wording
change is needed there. `__pycache__/` in `auditspec-review-ov31-type-store-0929/` (dated 17:04, before this worker
started, and gitignored) was not created by this worker.
