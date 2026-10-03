# SWE2-AUDIT-SPEC review: ASTRA UQ147 partial summon-cleanup order and Dismiss selector boundary

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-LOCAL-BOUNDARIES-1003` (reviews `ASTRA-PUBLISH-UQ147-LOCAL-BOUNDARIES-1003`) · commit reviewed `6d74079f120a000cc54d6615355a7716b46cd352`, at HEAD `a19ddeadd`
Package: `_experiments/evidence/uq147-local-boundaries/` (unchanged since `6d74079f1`). Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All three bounded results hold at the shipping bytes:

- **Defeat boundary.** On the gated leg, `0030111C xor ecx,ecx` / `call 3138D0` / `call 23B040` is straight-line, so the recompute runs in the same call immediately after `3138D0` returns normally.
- **Request tail.** The `(1,0)` tail skips `25AAD0`'s publication block.
- **Selector.** Roster index 3 → `0209A208` → `actor+30`. It has no status filter, no object write and no opaque helper.

The narrowing is to the request-tail statement. The README says only that "the earlier resolver still executes" before the tail, and the result's `unresolved` list names helpers. Neither says that **`00317E60` performs its own conditional object write**, `or qword [unit],100000000h` at `00317E9A`, before it reaches the tail. A consumer reading "excludes the publication block; earlier resolver still runs" could take the leg as write-free apart from helpers, and it is not.

**Exact replacement wording** for the README bullet that begins "`result-request-tail-boundary-02.json`":

> `result-request-tail-boundary-02.json`: every normal `317E60` tail passes `(1,0)` to `25AAD0`. Under the normal ABI the saved `EBX=1` takes `25AAE1 jne 25AB1C`. That excludes `25AAD0`'s five publication writes (`25AAF2`, `25AAF8`, `25AB00`, `25AB06`, `25AB15`) and its `2F1710` call at `25AB10`. Its `3588B0` resolver call at `25AADA` still executes.
>
> Before the tail, `317E60` itself calls `3590D0`. When byte `[02089340]&0x10` is set, it calls `3588B0` and then `263E30`. When the resolved unit is non-NULL and unit byte `+0` has bit 3 set, it performs an **own RMW write** `or qword [unit],1<<32` at `317E9A` and calls `33C9B0(unit+0x80)` at `317EA4`. Neither is excluded. This does not prove earlier helper effects or global mode preservation. Complete 87 B `317E60` and 82 B `25AAD0` qualified.

The same qualifier belongs in any consumer clause that cites the request-tail exclusion: "excludes `25AAD0`'s publication block and `2F1710` only; `317E60`'s conditional `317E9A` write and `33C9B0` call precede it". The defeat and selector results are accepted as written.

## SWE2-AUDIT-SPEC identity and integrity

- `manifest.json` hashes to `d6df38e07fca5621a9222d68f1dcb24faad7d41a7f2cf5e0b1097e84a9ca0c8f`, as named. It lists 66 members, and all match size and sha256 (0 mismatches). It is unlisted, as is `.gitattributes`. The 69-path commit is 66 members, the manifest, `.gitattributes` and `_inbox/ASTRA.md`.
- Receipts (each `terminal: true`, `exception: null`):

  | receipt | driver | exit | stdout |
  |---|---|---|---|
  | `prove-selector-01` | `1da38dc8…0663` | 0 | `Closed Dismiss slot3 read-only selector; no KO/status filter or object writes. Natural admission/lifetime/UQ147 remain OPEN.` |
  | `prove-defeat-boundary-01` | `689baa77…70e4` | 0 | `Confirmed conditional same-call Dismiss->recompute, designated-member byte/pointer identity; natural KO/mode/status preservation OPEN` |
  | `reduce-request-tail-02` | `b4a8732f…7f75f2a` | 0 | `Excluded notification write/callback block on exact tail(1,0); earlier helper effects and natural KO-order question remain OPEN` |
  | `capture-selector-01` | `4dde5e09…0737` | 0 | records 31 B / 23 B / 5 B spans |
  | `freeze-attempt01` | `e50111fe…1643` | **1** | its stderr ends in the `producer_complete` assumption |

  The failed `freeze-attempt01` is retained and not credited.
- The freezer requires the tail result's exact digest `ebcd389e…168f`, its driver, its source and its successful status. It copies files, adds `publication-tail-source-map-01.json` and does not rerun anything.

## SWE2-AUDIT-SPEC reproduction

The drivers resolve the validator as `P.parent/validate-title-source-annotations.py`, which is ASTRA's work-root layout, so they do not run from the canonical evidence folder. I rebuilt that layout in scratch: a copy of the package plus the validator, which hashes `7c4ea9f6…5f13` in both places. Venv python 3.14.6 with capstone 5.0.7. Each driver ran with the retained output name removed from the copy:

- `prove-dismiss-selector-boundary.py result-selector-01.json`: exit 0, same stdout, **byte-identical**.
- `prove-defeat-recompute-boundary.py result-defeat-boundary-01.json`: exit 0, same stdout, **byte-identical**.
- `reduce-request-tail-boundary.py result-request-tail-boundary-02.json`: exit 0, same stdout, **byte-identical**.

## SWE2-AUDIT-SPEC physical byte correspondence (`scratch/srccheck.py`, independent of the producer)

Every range in the four source files equals the image bytes (`image_match=True`).

| body | bytes | `.pdata` |
|---|---|---|
| `300FC0-301133` | 371 | single root |
| `31B770-31B7DA` | 106 | root `31B770-31B795` + chained `31B795-31B7D2`, `31B7D2-31B7DA` |
| `317E60-317EB7` | 87 | single root |
| `25AAD0-25AB22` | 82 | single root |
| `31B8C0-31B8DF` | 31 | single root |
| `263750-263767` | 23 | **no** covering row |
| `263E30-263E35` | 5 | **no** covering row |
| `3138D0-313993` (caller) | 195 | root + four chained fragments |
| `311CF0-311E0B`, `30D9A0-30DA09` | 283, 105 | single roots |

The two leaf spans really have no `.pdata` row (leaf functions), so no roots were invented. The new selector bytes total 59 (31+23+5). The retained totals are 583 (195+283+105), 169 (87+82) and 477 (371+106), as stated.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (`disr.py`)

- **Defeat leg (`300FC0`).**
  - The gates are `3010F6 test edi,edi / jne 301128`, `3010FA call 30D9A0 / cmp eax,1 / jne`, and `301104 mov rax,[02EBF190]` / `movzx ecx,byte [rax+5AD5h]` / `call 31B770` / `cmp rbx,rax / jne`.
  - Then `30111C xor ecx,ecx` / `30111E call 3138D0` / `301123 call 23B040` / `301128` epilogue. Nothing intervenes. **Holds.**
  - `31B770`:
    - `cmp cl,27h / ja` returns NULL;
    - `rdi = [02EBF190]+8+cid*1C8h`;
    - a loop over `236850`/`236820`, comparing `[unit+698h]` with `rdi`;
    - the only memory write is the `[rsp+30h],rbx` home slot.

    It has no status read of its own. Its two helpers stay opaque, as the package says.
- **Request tail.** `317E60`:
  - `call 3590D0` / `test byte [02089340],10h / je 317EA9`;
  - `call 3588B0` / NULL→`317EA9`;
  - `call 263E30` / NULL→`317EA9`;
  - `test byte [rax],8 / je 317EA9`;
  - `mov rcx,100000000h` / **`317E9A or qword [rax],rcx`** / `lea rcx,[rax+80h]` / `call 33C9B0`;
  - and on every path `317EA9 xor edx,edx` / `lea ecx,[rdx+1]` / `add rsp,28h` / `jmp 25AAD0`.

  `25AAD0` does `push rbx` / `mov ebx,ecx` (= 1) / `mov ecx,edx` / `call 3588B0` / `test ebx,ebx / jne 25AB1C`. The five `rip` stores and the `2F1710` call sit between `25AAE3` and `25AB15`, so they are skipped. `rbx` is non-volatile in the ABI. The `(1,0)` result **holds**, and the `317E9A` write is real and unstated (see the verdict).
- **Selector.**
  - `3138D0`: `call 30D9A0` / `cmp eax,1 / jne` / `lea ecx,[rax+2]` (= 3) / `call 31B8C0`.
  - `31B8C0`: `sub rsp,28h` / `call 263750` / `test rax,rax / jne` → NULL returns via `add rsp,28h; ret`. Otherwise `mov rcx,rax` / `add rsp,28h` / `jmp 263E30`.
  - `263750`: `cmp ecx,3 / ja` returns 0, else `[0209A1F0+8*idx]`. With idx 3 that is `0209A208`.
  - `263E30`: `mov rax,[rcx+30h]; ret`.
  - No writes, no calls beyond the closed pair, and no status read. **Holds.** Index 3 is a roster slot; the package correctly refuses to read it as ActorStorage class 3.
- **Caller correction (CS1 retraction).** A raw census of E8/E9/`0F 8x` rel32 and aligned RVA32 references to `311CF0` over all sections finds `311C7B` (E8), `311CA6` (E8), `31395D` (E8) and one RVA32 at `02FB3F90`, the `.pdata` row. That is three call sites in two functions, `311B20` (`311C7B`, `311CA6`) and `3138D0` (`31395D`), so the retraction is **correct**.

## SWE2-AUDIT-SPEC control sensitivity

- **Selector controls** (re-run, all three refused with the required marker):
  - `roster-base-field-changed` changes `memory.rip_target`→`0x209a208` with the text kept, so the text pin passes. It is refused by `roster base identity changed`. **Sensitive.**
  - `actor-unit-offset-changed` changes `displacement`→`0x38`. It is refused by `actor unit-pointer identity changed`. **Sensitive.**
  - `selector-tail-changed` changes the args of the `31B8DA` jmp. It is refused by the `expected` text pin, which is the right detector for a transfer target. **Sensitive.**
  - The `failed-upstream-status` control is in-process, as declared, not a CLI refusal.
  - The exact-set check (`len(ix)==len(expected)` and pc-set equality) also refuses any added or removed instruction.
- **Defeat controls:** `recompute-redirected` (text pin), and `designated-member-byte-changed` and `lookup-pointer-field-changed`, both semantic memory-field checks. All require their markers. **Sensitive.**
- **Gap (non-blocking).** In `prove-defeat-recompute-boundary.py`, `lookup_transfers` is reported but never compared with an expected set. A changed helper target inside `31B770` would pass, provided its text is not one of the pins. On the shipping bytes the calls are `236850`, `236820` and `236850`, so the fact stands on this review's reading.
- **Request-tail reducer.** No source controls. Its exact five-PC write list is a positive check, so a zero here is not a filter artefact. Nothing in the reducer looks at `317E60`'s own memory roles, which is why the `317E9A` write went unmentioned.

## SWE2-AUDIT-SPEC claims audit

- The defeat same-call order holds, and "no necessarily-later-tick claim" is respected.
- The selector's read-only, NULL early-return composition with no status filter holds.
- The `.pdata`/leaf identities hold.
- The request-tail exclusion holds, **narrowed** as above.
- Still OPEN, and correctly kept so:
  - real KO admission;
  - the roster/`+5AD5` relationship;
  - mode/KO/member persistence across helpers;
  - request versus acceptance and commit;
  - mask 7 and override-clear reachability;
  - scheduling, lifetime and presentation.

  No game, emulator or native run is claimed.
