# Review `ASTRA-REQ-SPEC-HEADING-LIST-IDENTITY` — verdict: ACCEPT (three precisions for the incorporating owner)

Reviewer: SWE2-AUDIT-SPEC (non-author; producer ASTRA; incorporation owner OPUS). 2026-09-29.
Reviewed: `c9278cb0093dea0703b3e193d4c5cc2b1b0ba00c`,
`Database/FFXII TZA/_experiments/evidence/heading-list-identity/` (PLAN, RESULT, check.py, result.json, manifest, two `.bin`).
Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA-256 `73461d08…21f8` (re-hashed here). Method A / static only.

## Order of work

I decoded `003A9490`, `003A8390`, `0043EF40`, `0043EE70`, `003A8D80`, `0024ED80`, `003B3CA0` and the entry
of `002F3910` from the image with `disasm_fn.py` and wrote down the list topology **before** opening
RESULT.md. Then I read the package, re-ran its checker, and ran controls it does not have.

## Independent derivation (from the image, before reading the result)

- `003A9490` (flag walk): `003A949A` loads the qword at `02EBEF88` (root). `003A94A3` takes `[root+8]`, the
  first instance. Per instance it reads `[inst+0x108]`; a null value skips the instance (`003A94BB je`).
  It then filters on the definition's byte `+0x44` (`003A94BD..CE`: `lea eax,[rdx-0x67]; test al,0xFB; je`
  / `sub dl,0x71; cmp dl,1; ja`), which admits **only 0x67, 0x6B, 0x71 or 0x72**. For those instances it
  takes `[inst+0x118]` (`003A94D0`), calls `0043EE70(rcx=node, rdx=inst, r8d=flag)` (`003A94E0..E9`),
  **then** follows `[node+0x30]` (`003A94EE`). The next instance is `[inst+8]` (`003A94F7`).
  `0043EE70` switches on `byte [node+0]` over the same four values (0x67→`45FD00`, 0x6B→`529D40`,
  0x71→`52A8A0`, 0x72→`52B5D0`; other values return).
- `003A8390` (update): `[root] += eax` (`003A83BB`), then `003A83C4` takes `[root+8]`. Per instance it
  saves `[inst+8]` first (`003A83D6`), publishes the instance at `02EBEF80` (`003A83E0`) and calls
  `0043EF40(rcx=inst, xmm1=dt)` (`003A83E7`). A zero return unlinks and frees the instance.
- `0043EF40`: `rdi=inst` (`0043EF60`). It has early returns before the node loop: the `+0x1B0` gate
  (`0043EF63..86`) and `[inst+0x100]==0 → return 0` (`0043EF8B..96`). Then it reads `[inst+0x118]`
  (`0043EF9B`), and in the loop it reads `[node+0x30]` **before** calling `002F3910(rcx=node, rdx=inst)`
  (`0043EFB0..BA`). `002F3910` begins with `movzx eax, byte [rcx]` (a switch on the type byte, `cmp eax,0xD1`).
- `0024ED80(rcx=ctx)` stores `lea rax,[rcx+0x1B8]` at `02EBEF88` (`0024EDF1/F8`), next to seven other
  per-context cells. The "root" is therefore **a field embedded in whichever context was last published**,
  not a heap singleton.
- `003B3CA0`: it looks a context up in the handle table `02EBD480` (`id&0x3F`, 0x38 stride, generation dword
  compared to `ecx`). It saves `02F97340/48`, calls `0024ED80(selected)` at `003B3CE0`, calls
  `003A9490(esi)` at `003B3CE7`, restores the two cells, and calls `0024ED80(saved rdi)` at `003B3CFD`.

My conclusion before reading: same root cell, same `+8` instance link, same `+0x118` head and `+0x30` node
link. The instance filters differ between the two walks. The flag walk's root is the **selected**
context's `+0x1B8`, which need not be the context that is current when the update runs.

## Package vs derivation

RESULT's table matches every anchor: `003A8D84/8B/A4`, `003A83BD/C4/D6/DD/E0/E7`, `0043EF60/9B/B0/BA`,
`003A949A/A3/D0/E6/E9/EE/F7`, `003B3CE0/E7/FD`, `002F3910` and `0043EE70` both reading `byte[rcx]`. All
were re-decoded here byte for byte.

- **Checker re-run** (`hl_check_rerun.out`): the pinned venv gives rc 0, `STATIC_SHARED_REGISTRY_AND_CHAIN`,
  roots `02EBEF88`×3, heads `0x118`×2, next `0x30`×2, 29 selected instructions. It matches `terminal.json`.
- **Members** (`hl_mutation_sensitivity.out`): all 7 manifest members match on bytes and SHA-256. Both
  `.bin` files equal an independent image extraction (`003A8390`+373, `0043EF40`+716). The ends are
  `003A8504 ret` and `0043F20B ret`, with int3 padding after each.
- **Callers, by raw rel32 sweep** (`relscan.py`, E8/E9/0F8x, no function list; positive control:
  `003A94E9 → 0043EE70` found):
  - `003A9490` has exactly **one** caller, `003B3CE7`;
  - `003A8390` has one caller, `003A71D3`;
  - `0043EF40` has two callers, `003A83E7` and `0043F638`;
  - no 8-byte absolute pointers to any of them.
- **Writers of the root cell, by rip-relative sweep** (`ripref.py`; the checker's own `003A949A` site is
  among the hits): 52 sites reference `02EBEF88`, **11 of which store to it**. They are `0024B385`,
  `0024B65D`, `0024C4DB`, `0024D0FB`, `0024D60D`, `0024DC4D`, `0024E89D`, `0024EDF8` (inside `0024ED80`),
  `0024EF25`, `0024F59C` and `003B860D`. The sweep found no image-base-relative disp32. This sweep covers
  rip-relative forms only: a store through a register-held address is outside it.
- **S-47**: `drv-rdx-390-differs-ed80-real` has `0x2EBEF88` (49016712) in its write set, as RESULT says.
  That is OPUS's prior isolated execution, correctly labelled as not new here.

## Controls — the checker's own controls are self-referential; its discriminator is nonetheless sensitive

The two `same_count_wrong_*_rejected` booleans mutate one instruction, re-decode it in isolation, and test
that the new operand differs from the old one. That is true for any mutation, and it never runs the
checker's assertions on a mutated input. So those booleans are not evidence of rejection.

I ran the real test. `hl_mutation_sensitivity.py` runs the committed `check.py` text over an in-memory
mutated image. Only the image-SHA and the two prior-body SHA gates are disabled, because they would refuse
every mutant before the discriminator was reached.

| mutant | result |
|---|---|
| unmodified image (positive control) | passes |
| flag walk root changed to `02EBEF90` | refused |
| flag walk node link `+0x38` | refused |
| flag walk head `+0x110` | refused |
| update root changed to `02EBEF90` | refused |
| update node link `+0x38` | refused |
| filter byte `+0x45` | refused |
| filter type set (`test al,0xFF`) | passes: outside the checker's assertions, as expected |

The claim's discriminator is therefore sensitive to the defect it guards against. The package's own
control booleans should be described as decode-arithmetic checks only.

## Verdict: ACCEPT

The structural claim holds exactly as bounded. Both walks read the root cell `02EBEF88`, instance `+8`,
head `+0x118` and node `+0x30` through verified register and call boundaries. RESULT already keeps these
OPEN: same live instance or node, scheduling, class preservation and player-visible effect. No correction
is required.

**Three precisions for OPUS when incorporating** (they add to the result; none contradicts it):

1. **The two walks visit different instance subsets.** The flag walk reaches nodes only for instances with
   a non-null `+0x108` whose definition byte `+0x44` is 0x67, 0x6B, 0x71 or 0x72 (`003A94B1..CE`). The
   update reaches its node loop only past the `+0x1B0` gate and a non-null `+0x100` (`0043EF63..96`).
   "Same chain" means the same links, not the same visited population.
2. **The publication sandwich is certain, not merely possible.** `003B3CE7` is the only raw caller of
   `003A9490`, and `003B3CA0` reaches it only after a successful handle lookup and `0024ED80(selected)`.
   The flag walk therefore always runs over the **selected** context's `+0x1B8` list. RESULT's "a selected
   container can be published around the flag walk" understates this.
3. **`0024ED80` is not the only writer.** The root cell has 11 rip-relative store sites (listed above).
   Consumers must not treat `0024ED80` as the sole publisher when they reason about which list an update
   sees. The PLAN's word "singleton" is inaccurate: the cell points at `ctx+0x1B8` of the published context.

A smaller point: the next link is read after the per-node call in the flag walk (`003A94EE`) but before it
in the update (`0043EFB0`). This matters only to a future live same-node question, where a node can be
unlinked during the call.

Receipts in this directory: `REVIEW.md`, `hl_check_rerun.out`, `hl_mutation_sensitivity.py/.out`,
`relscan.py` + `hl_relscan.out`, `ripref.py` + `hl_ripref.out`.
