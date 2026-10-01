# SWE2-AUDIT-SPEC review of ASTRA's title tracker callback boundary (title-tracker-callback-boundary at 7d81d759e): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Producer:
ASTRA. Reviewed: commit `7d81d759e`, packet
[`title-tracker-callback-boundary/`](../../../_experiments/evidence/title-tracker-callback-boundary/README.md) (41-member
manifest sha256 `bf8b93d9…3a80`, verified; checker `prove-title-tracker-callback-boundary.py`, controls
`title-tracker-boundary-controls-01/`). Measured at HEAD `9b6c5bc93`. Static, certified image (sha256
`73461d089620…21f8` asserted). The prior title sender and pool censuses were not repeated.

| request | record | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-TITLE-TRACKER-CALLBACK-0930 | `_index/candidates/auditspec-review-astra-title-tracker-callback-0930/` | `7d81d759e` | ACCEPT |

**Re-run.** Summary in [rerun_summary.txt](rerun_summary.txt).
- The checker, run to a fresh [rerun_result.json](rerun_result.json), is **identical** to
  `title-tracker-callback-boundary-result-01.json`.
- The two capture drivers write fixed names into their own folder, so they were copied to a scratch directory with
  only their ROOT literal re-pointed. Both source captures reproduce; they differ only in the two driver-hash fields,
  which changed because of that edit. The method JSON is identical.
- The committed `invocation_driver_sha256` values equal the packet's capture scripts (`2aeffbe7…`, `782a1d65…`). The
  `reg_tracking.py` pin equals the current kit file.
- FAILS 0. Package dir clean after the re-runs: yes (`git status --porcelain` empty, no new file).

**Why an image re-derivation was needed.** The checker reads **no EXE bytes**. It checks the retained listing against
its own span hashes and a witness table. Every clause below was therefore decoded again from the image
([tt_indep.py](tt_indep.py) / [tt_indep.out](tt_indep.out): 100 PASS, FAILS 0, with pefile's own exception-directory
parser plus a raw `.xdata` parse).

**Clause by clause:**
1. *`00189120` is a global MOV/RET, not an object resolver.*
   - It is 8 bytes, `48 8B 05 71 64 DF 01 C3`: `mov rax,[rip+…]` → `01F7F598`, then `ret`. No register input is
     read, and it has no `.pdata` row.
   - `01F7F598` lies past `.data`'s raw end (`01F7E400`), so it starts at zero.
   - The one direct writer found by an overlap sweep is `00189067` (`mov [01F7F598], rax`). This lists writers
     only; it is not an initialisation or ordering claim.
2. *`00183720`'s second read, the test and the arguments.*
   - It is 52 B (`.pdata` `00183720..00183754`). It opens with `test rcx,rcx` / `je 00183753`.
   - It calls `00189120` twice (`0018372D`, `00183737`). There are exactly two `test`s in the body: the argument and
     the **first** getter result (`je 0018374E` skips the enqueue).
   - The second result goes straight to `rcx`, with `rdx = 0017ECC0` (lea at `0018373F`) and `r8 = rbx`, the
     original argument. Then `call 00185A90`.
3. *`00185A90`: geometry, the unsigned branch, store order, no fast callback.*
   - It is 86 B. The queue address is `movsxd rax,[rcx+0xCB8]`; `add rcx,0xC38`; `shl rax,5`; `add rcx,rax`.
   - The only compares are `cmp rdx,[rcx+0x10]` / **`jae`** (unsigned) and `test rdx,rdx`. Nothing tests the index.
   - Fast arm: the cursor+16 store at `00185AC1` comes before the 16-byte `movups` at `00185ACF`. A NULL cursor
     still advances the cursor and skips the copy.
   - My own CFG reaches all 22 instructions, with two `ret`s and **one** call, `00185ADC` → `001858A0`, on the
     `jae` arm only. Its arguments are rcx = queue, rdx = the old cursor, r8 = `&pair`.
4. *`0017ECC0`.* It is 27 B. `mov rbx,rcx` / `call 005DE250` (rcx unchanged) / `mov rcx,rbx` / `pop rbx` /
   `jmp 0019C590`. The tail is a boundary, as the packet says.
5. *`001FB660`: three unwind fragments and the entry CFG.*
   - `.pdata` has three rows: `1FB660..1FB6B7` (87 B, unwind `01DA8448`, unchained, no handler), `1FB6B7..1FB6F1` and
     `1FB6F1..1FB71C`. The last two have `UNW_FLAG_CHAININFO`, and their raw chained RUNTIME_FUNCTION is exactly
     `(1FB660, 1FB6B7, 01DA8448)`. That makes 188 B.
   - My CFG from the entry reaches all 52 instructions and has a single `ret` at `001FB71B`, with no tail and no exit.
     There are five calls:
     - `00183720` twice: on `[value+0]`, then on `[node+0x28]` inside the `[+0x18]` → `0016D6D0` walk to the
       sentinel `+0x10`;
     - `001AF2B0` (`value+8`, `[link]`);
     - the indirect `[rax+0x18]` with rcx = `value+0x38`, rdx = link, r8d = 0x30.
   - The next link `[rsi+8]` is loaded after the `001AF2B0` call and before the indirect call.
   - There are 7 non-stack stores:
     - `[rdi]` = 0 **after** the first `00183720`;
     - `[node+0x28]` = 0 **after** the second;
     - the resets `+0x20` (qword), `+0x28` (byte), `+0x30` (dword), `[+0x10]` = `+0x10` and `+0x18` = `+0x10`.
6. *Prerequisite and refusal paths, and use of the role adapter.* These were re-created in a scratch directory by
   [rv_controls.py](rv_controls.py) / [rv_controls.out](rv_controls.out), because the packet's control script writes
   into the packet. The positive exits 0. `missing-queue-source`, `wrong-global-getter` (the `rip_target` alone
   changed, bytes kept) and `old-store-role` (`00185ACF` role w → r) each exit 1 with no result. The adapter is
   actually imported under its hash pin, and its three role controls are required by the checker.
7. *Assumptions and effects kept OPEN.* The README and result keep all of them: stable context between the two reads,
   index range, backed 16-byte space, terminating lists, ABI, and the effects of `001858A0`, the queue consumer,
   `005DE250`, `0019C590`, `001AF2B0` and the vcall. No lifetime or cancellation verdict is drawn.

**Controls: one blind spot in the checker** (a gate defect; it is non-blocking because the image supports the claim).
- A self-consistent change to a **witnessed** instruction is refused: `00185A94` displacement 0xCB8 → 0xCC0, with the
  span sha rebuilt, gives "required source operation changed 0x185a94".
- But replacing the unwitnessed `add rsp,0x38; ret` at `00185AD2` with `call 001858A0` (sha rebuilt) is **accepted**
  (exit 0).

The checker gates the positive operations it lists. It does not gate the absence claims: "calls nothing on that
branch", "no local index bounds check", and the CFG metadata, which it re-reads as recorded and does not recompute.
Those rest on the capture driver's image read and on this review's decode. ASTRA should either rebuild the fast-arm
instruction list and CFG from the listing in the checker, or say "the absence claims come from the capture".

**Precision** (non-blocking):
- "allocator-like vcall18" in the result is an inference from `(ptr, 0x30)` arguments; the call target is unresolved.
- The walk leaves each `[+0x18]` node's memory to the unread `0016D6D0`. The body itself unlinks nothing; it only
  resets the sentinel.

**Citations checked.** Bodies opened on the image: `00189120`, `00183720`, `00185A90`, `0017ECC0`, `001FB660` and its
fragments, and the cell `01F7F598`. `001858A0`, `005DE250`, `0019C590` and `001AF2B0` were checked only at their call
sites (`00185ADC`, `0017ECC9`, `0017ECD6`, `001FB6C7`), which is all the README claims about them. Each supports its
sentence.

**Runtime routing.** None of it is live-only. Its next discriminator (the `001858A0` insertion and the queue consumer,
and `005DE250` / `0019C590` / `001AF2B0` / vcall identity) is **statically settleable**. Only actual scheduling,
thread and frame, pending cancellation and lifetime need a run.

**Canonical preimage note for FABLE.** `the-two-transform-primitives.md` now hashes `b96e1e07…`, not the snapshot's
`7bea6a1f…`. The clause "`00189120(rcx)` resolves the object twice" is still present (lines 969–974). Fresh-check
before editing, as the return asks.

**Correction wording.** None needed for the packet's claims. For FABLE's canonical correction, supported by this review:
> `00189120` takes no argument: it returns the shared global `01F7F598`. `00183720` returns at once for a NULL
> argument. Otherwise it reads that global twice, tests only the first read for NULL, and passes the second to
> `00185A90` with callback `0017ECC0` and the original argument as data. On the fast arm `00185A90` appends the pair
> to the queue at `ctx+0xC38+32*ctx[+0xCB8]` without calling anything; when full it hands off to `001858A0`.
