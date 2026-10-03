# SWE2-AUDIT-SPEC review: ASTRA UQ147 Dismiss local preparation order

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-DISMISS-STAGE-1003` (reviews `ASTRA-PUBLISH-UQ147-DISMISS-STAGE-1003`) · commit reviewed `3a25a0be0c3a450c0d7d353d5c66096ff491a04e`, at HEAD `a19ddeadd`
Package: `_experiments/evidence/uq147-dismiss-stage/`. Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The local order claim holds at the bytes:

- Under quotient 275 (0x113), classifier selector byte 127 is 5, and jump entry 5 is `306CB0`. That gives `EBX=2`, which is stored to `022C215C`.
- `306760` reads `022C215C`, and `kind−1 = 1` selects table element 1, `306A3D`.
- On that arm, the conditional `and eax,~1` / `mov [battle+5B04h],eax` at `306A81` comes before this routine's direct `mov dword [022C2160],5` at `306ADF`. The bit-clear-already path skips the store and joins the same common suffix at `306A95`.
- No read of the state word `022C2160` guards the clear anywhere on the local path from entry to `306A81`.
- Kind 1 (`306931`) sets bit 0, which gives a distinct positive arm.

This is local order only. The package correctly does not claim any of the following:

- a first-ever state 5;
- a lasting mode clear;
- the effects of the opaque helpers;
- natural KO/Dismiss coexistence;
- invariance of row, kind or owner;
- resource success, scheduling, visible timing or whole UQ147.

## SWE2-AUDIT-SPEC identity and integrity

- `manifest.json` hashes to `8138136d62841224f88f0c756b0959fc2448d00c134cad78078b420dd78ab478`, as named. It lists 42 members, and all match size and sha256 (0 mismatches). The only unlisted files are `.gitattributes` and the manifest.
- `prove-dismiss-stage-retained.py` is `f3929d1a1ffca77e23fcb8f41482e31e2de3aabd8b169fc5790e2e6fbb3a1097`. `prove-dismiss-stage-retained-01.status.json` records that driver, `terminal: true`, `exit: 0` and `exception: null`. Its stdout is `Retained original tables bind Dismiss kind2; conditional local mode clear precedes same routine state5 write. Natural timing/KO remains OPEN.`, and stderr is empty.
- `capture-dismiss-stage-01.status.json` records the driver `e1cbb2d3…8188` and **exit 1**. Its stderr ends `ValueError: covering retained map exists: consume it`. This is the preserved refused setup, with no output and no credit.
- The five canonical dependencies the producer pins all hash as the board states, and each is byte-identical to its `retained/` copy:
  - `ov42-sequence-queue-source/source-02.json` `c7177768…`;
  - `ov42-sequence-queue-source/data-01.json` `19e148fb…`;
  - `ov42-kind-row-coherence/retained-prefix-01.json` `33276301…`;
  - `ov42-kind-row-coherence/source-01.json` `75e86a31…`;
  - `ov42-kind-row-coherence/data-01.json` `d2ee2256…`.

## SWE2-AUDIT-SPEC reproduction

Venv python 3.14.6 with capstone 5.0.7. The producer resolves its dependencies in the canonical evidence tree and its validator in the ASTRA work root (`7c4ea9f6…5f13`). It ran in place, writing its output to an absolute scratch path:

- `prove-dismiss-stage-retained.py <scratch>/result-rerun.json`: exit 0, same stdout. The output is **byte-identical** to `result-dismiss-stage-retained-01.json` (`74d8486f…409d`).
- The three validator invocations report `VERIFIED_BYTE_ANNOTATION_AGREEMENT` over 204, 167 and 37 records.

## SWE2-AUDIT-SPEC physical byte correspondence (independent of the producer)

- **Code ranges.** Every code range in the three code sources equals the image bytes:
  - `306760-306AEF` (911 B), which stops before the `306AEF` `nop` and the table at `306AF0`;
  - `306BD0-306C5B` (139 B) and `306C5B-306CEC` (145 B), which stop at the jump table `306CEC`;
  - plus prefix bodies `30CE10` and `309230`.
- **Tables, read from the image.**
  - The 7-entry jump table at `306CEC` resolves to `306CBE`, `306CC5`, `306CD1`, `306CB7`, `306CA9`, `306CB0`, `306CCC`.
  - The 128-byte map at `306D08` has map[127] = **5** → `306CB0` (`mov ebx,2`).
  - The 6-entry kind table at `306AF0` resolves to `306931`, **`306A3D`**, `3067DB`, `306848`, `3069F8`, `306A8E`.
- **Mixed `.pdata`.** The row covering `306C5B` is `306C3D-306D88`. It spans the classifier's code, its jump table and its map, so the "mixed physical body" statement is right, and so is splitting code from data before decoding.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **Classifier `306BD0`.**
  - `306C71 sub esi,eax` / `movzx ecx,word [rax+8]` / `div ecx` / `add eax,-94h` / `cmp eax,7Fh / ja 306CCC`.
  - Then byte `[306D08+idx]`, dword `[306CEC+4*byte]`, `jmp rcx`.
  - Quotient `0x113` gives idx 127 → byte 5 → `306CB0`, `EBX=2` → `306CDB mov [022C215C],ebx`.
  - The full unsigned quotient is a premise, as stated.
- **Dispatch `306760`.**
  - The prologue touches `[rcx+694h/695h]` and tests `[rdx+1Ch]==8`, with opaque calls `3098D0` and `3299B0`.
  - `3067AA mov eax,[022C215C]` / `dec eax` / `cmp eax,5 / ja` / `jmp [306AF0+4*eax]`.
  - **No load of `022C2160` occurs before the dispatch.**
- **Kind-2 arm.**
  - `306A3D` reloads `[02EBF190]` / `test byte [rax+5AD0h],1 / je` → optional `35DAE0(0)`, then `306D90`.
  - `306A6D` reloads / `mov eax,[rcx+5B04h]` / `test al,1 / je 306A95` / `and eax,0FFFFFFFEh` / **`306A81 mov [rcx+5B04h],eax`** / `call 35C620` / `jmp 306A95`.
  - `306A95` begins `236850`/`236820` and a roster loop doing `and dword [rax],0FFFFFCFFh` with stride `0F50h`. Then `332130(3)` and **`306ADF mov dword [022C2160],5`** / `ret`.
  - **Holds.**
- **Write census over the whole retained `306760` source** (non-stack `w`/`rw` roles). On the kind-2 path from entry, the direct writes are only `306785`/`30678B` (incoming object `+695/+694`), `306A81`, `306AC0` (roster flags) and `306ADF`. `306ADF` is the **only** direct writer of `022C2160` in the routine. So no earlier direct state-5 write on the path weakens "precedes".
- **Kind 1.** `306931`: `not eax / test al,1 / je` skips when bit 0 is already set; otherwise `or ecx,1` / `306949 mov [rdx+5B04h],ecx`. This is the positive set-arm, as stated.

## SWE2-AUDIT-SPEC control sensitivity

These are the four labelled controls. All re-ran with their markers required, and every refusal comes from the semantic or table detector, not a text pin:

| control | defect | refused by | sensitive? |
|---|---|---|---|
| `dismiss-selector-byte-changed` (map[127]→4) | quotient 275 no longer selects kind 2 | `full quotient275 no longer publishes kind2` | yes. Entry 4 is `306CA9`, `EBX=1` |
| `kind2-table-target-changed` (element 1→`306931`) | kind 2 dispatches to the set-arm | `kind2 dispatch is not the Dismiss arm` | yes |
| `mode-store-offset-changed` (`306A81` disp→`0x5AD0`) | the clear store is not the mode word | `selected memory identity changed 0x306a81` | yes. The text is unchanged |
| `state5-target-changed` (`306ADF` `rip_target`→`0x22C215C`) | the 5-write is not the state word | `selected memory identity changed 0x306adf` | yes |

Two detectors are absent (non-blocking):

- **Order.** No control injects an extra direct `022C2160` write before `306A81`, or reorders the two stores. The producer pins every transfer in the window and both store sites, but it does not census other writers on the selected path. The census above closes this on the shipping bytes.
- **Table dependence.** The producer re-checks the tables and physical bodies against the **image** (`original()`), so the table-level controls are not judged against stale copies.

## SWE2-AUDIT-SPEC claims audit

- The quotient-275 → selector byte 127 → entry 5 → kind 2, and the separate kind-2 table entry 1 → `306A3D`: **hold**.
- The conditional mode-bit-0 clear at `306A81` precedes the direct state-5 write at `306ADF`, the cleared-bit path skips the store into the same suffix, and kind 1 is the positive separation: **hold**.
- "Qualify the mode-ladder phrase 'when the sequence ends'": **supported**. Locally the clear sits in the state-5 preparation path, with no state-6/7 guard. Consumers should state that as local order, not as visible timing.
- The failed capture and the wrong `+34` plan are preserved and earn no credit. The FABLE consumption `1c4c5820` and the carrier `c40b2434`/`49d0564f2` are consumed, not repeated.
- The limits keep opaque-helper effects (`3098D0`, `3299B0`, `35DAE0`, `306D90`, `35C620`, `236850`/`236820`, `332130`), first-ever state 5, lasting clear, natural coexistence, row/kind/owner invariance, resource success, scheduling, visible timing and whole UQ147 OPEN. **No overclaim.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- Add a census in `derive()`: no non-stack write with `rip_target 0x22c2160` (or base+`0x5B04`) on the selected path other than `306A81`/`306ADF`. Add a FAILS control that injects one before `306A81`.
- **Exact consumer clause** (FABLE mode ladder / OPUS): "On the kind-2 (Dismiss) arm of `00306760`, if mode bit 0 is set, the routine clears it at `00306A81` before its own direct write of state 5 to `022C2160` at `00306ADF`. If the bit is already clear, the store is skipped and the same suffix runs. No state-6/7 guard surrounds the clear. This is local order under normal-returning helpers, not visible timing or a lasting clear."
