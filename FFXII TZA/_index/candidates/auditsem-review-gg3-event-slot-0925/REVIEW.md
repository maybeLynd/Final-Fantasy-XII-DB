# REVIEW — FABLE-REQ-AUDITSEM-CHALLENGE-GG3-AND-EVENT-SLOT-CONCLUSIONS

*Provenance: this SWE2-AUDIT-SEM record was kept only in the gitignored `Database/Tools/work/SWE2-AUDIT-SEM/review-fable-gg3-event-slot-challenge.md`, which closed register rows cite (found by the DD-rule T review, `auditsem-review-ddrule-t-0930`). Published here unchanged by SWE2-AUDIT-SEM so the evidence is tracked; each `##` heading now names SWE2-AUDIT-SEM.*

Reviewer: SWE2-AUDIT-SEM, 2026-09-25. Adversarial re-verification of FABLE's GG-3 (UI widget generation
walker) and event-slot setter/pusher conclusions — independent reads of original bytes against the
verified shipping image (SHA256 `73461D08…721F8`), plus two independent mutants not in FABLE's set.

Verdict: **all statements ACCEPT.** No refutation found; the conclusions are byte-exact.

## A. GG-3 — generation walker `00248030` / receiver `002284F0` (SWE2-AUDIT-SEM)

| # | FABLE statement | Verdict | Independent evidence |
|---|---|---|---|
| A1 | Sends message 2 via record `00915108 = {2,0,0}` | ACCEPT | `002480EF lea rdx,[rip+0x6cd012]` → `00915108`; bytes `02 00 00 00 00…`; `call rax` where `rax=[rbx]` (node descriptor slot 0). |
| A2 | Call fires only when widget-flags bit 18 is CLEAR | ACCEPT | `002480E1 bt ecx,0x12` loads bit 18 into CF; `002480E5 jb 0x248101` branches when CF=1 (bit SET) over the `call rax` at `002480F9`. Polarity confirmed — jb taken on set, so the call runs only when clear. |
| A3 | Bit 17 rewritten from parity global `0208ED5C` | ACCEPT | `00248101 and [rbx+0x40],0xfffdffff` clears bit 17; `00248108 eax=edx&1; shl eax,0x11; or [rbx+0x40],eax` restamps it. `edx` reloaded from `[rip+0x1e46c5b]` at `002480FB` → `0208ED5C` after a live call; the suppressed path keeps the pre-call `edx`. |
| A4 | Walker never writes bit 18 | ACCEPT | Body writes to `[rbx+0x40]`: `or ecx,4` (bit 2), `and 0xfffdffff`/`or` (bit 17 only), and `[rcx+0xb4]` counters at `00248131/3A`. No instruction targets bit 18. |
| A5 | Suppressed nodes' children are still messaged | ACCEPT | The `jb 0x248101` suppressed arm lands *inside* the per-node epilogue, then falls through to the shared next-node selection at `00248113`: descend `[rbx+0x18]` (child) when its bit-17 parity differs from `edx`, else sibling `[rbx+0x20]`, else climb `[rbx+0x10]`; loop continues to `r14`/null. Each child's bit 18 is evaluated independently — suppression is per-node, not subtree. |
| A6 | `002284F0` is the `obj+0` handler of the exact singleton made by `00228490` | ACCEPT | `00228490`: if `[01FD4948]==0`, calls factory `00244F50` with `ecx=0xD0`, `rdx=&[rip+0x29]` → **`002284F0`** (`lea rdx,[rip+0x29]` @ `002284C0` → `0x2284C7+0x29`), then stores the result into `01FD4948`. Ctor `002465F0` writes `r8` (the descriptor arg) at `[obj+0]` (`00246641 mov [rdi],rbx`, `rbx=r8`, fallback default `005C5230` only when r8==0 — not this call). `00228490`'s sole caller is `002283AE` (`00228380`), reached from `00253CC3`. Not a same-named neighbor — the descriptor operand is the literal address. |
| A7 | Cross-checks | PASS | `002284F0` dispatch: `mov ecx,[rdx]; sub/je` chain — msg-2 arm at `00228641` clears `[rbx+0xc0/c8]` and re-enters `00248030` at `0022865C` (the self-recursive site in the 13-caller census; the other 12 sites are the `00250540`–`002509xx` root-generation walk over `[0208EA48]`). Msg-1 arm attaches the singleton to the root. Ctor also restamps bit 17 from `0208ED5C` — same parity scheme the walker maintains. |

Replay boundary (unchanged, disclosed): the GG-3 replay runs planted trees with observer callbacks —
walk order, suppression, and restamping are proven for the planted topology; live widget construction
order and live frame timing are not claimed.

## B. Event slot — setter `0020AC30` / pusher `0020AF10` (SWE2-AUDIT-SEM)

| # | FABLE statement | Verdict | Independent evidence |
|---|---|---|---|
| B1 | `0001` test is inside the `sum_` arm | ACCEPT | `0020AD23 call 001C34D0` searches `r8=00905988 "sum_"`; not-found → `je 0x20ADDF`. Found path: `001B31E0` builds `<name>+008FB2B4 ".json"` → `call 001C5750` → then `0020ADB1 call 001C34D0` with `r8=00905990 "0001"` → `0020ADD6 mov byte[01F832E8],1`. The `0001` search is unreachable without `sum_`. |
| B2 | `spc_` tested only when `sum_` absent | ACCEPT | The `spc_` search (`r8=00905998 "spc_"`, `0020ADE4/EB`) lives only in block `0020ADDF`, reached solely from the two `sum_`-not-found edges (`0020AD3F`, `0020AD4A`). `0020AE13 cmovne` → `01F832E9 = (found ? 1 : old)`; the else-source `movzx ecx,[01F832E9]` always reads 0 (entry clear) — effective semantics: `E9 = spc_-present`. |
| B3 | `001C5750` reads cutscene JSON DOF settings | ACCEPT | Builds path + `<name>.json`, opens via `001FE8B0`, three `001FF740` key lookups; keys resident at `008FA3CC+`: `Common`, `EnableDof`, `mDofApertureFnumber`, `mDofFocusDistance`, `mDofSpecialApertureFnumber`, `lightOrientation/Height` ×3, `mGammaValue`. `001C58A7 movss xmm1,[…]` loads the float, `001C58C0 mov rcx,[01F81300]`, `001C58C7 call 00194250` — applies it to the cutscene-settings object. |
| B4 | Both `[rax+0x18]` calls are string frees | ACCEPT | `rax=[obj]` is vtable `00902720` = `{0016D680, 001EDF10, 001EDF80, 001EDFE0, 0016D690}`. Slot +0x18 = **`001EDFE0`** → tail-jmps IAT `008C2B70` = **`_aligned_free`** (lazy-inits pool desc `{0x2000000,0x200000}` at `01F8CE48`). Symmetric alloc slot +0x10 = `001EDF80` → `_aligned_malloc` (`008C2B60`), used at `0020AAD7`. Free-site args: `rcx=this`, `rdx=begin`, `r8d=capacity`, guarded `cap>1 && begin!=0` — deallocate. Verified at `0020AD9A` (JSON string) and `0020AE44` (extracted-name string). |
| B5 | Same-name call clears both flags | ACCEPT | `0020AC56/5D` clear `01F832E9`/`01F832E8` at entry unconditionally. Equal length + `memcmp==0` → `0020ACD2 je 0x20AE1C` exits before either arm — both remain 0, no JSON read, one free of the extracted name. Replay `same_name_repeat`: `E8:0, E9:0, frees:1, json:[]`. |
| B6 | Setter restores `01DFE40C` to −1 | ACCEPT | Entry stores index: `0020AC64 mov dword[rip+0x1bf37a2],esi` → `01DFE40C`. Single exit tail `0020AE48 mov dword[rip+0x1bf35ba],0xffffffff` → `01DFE40C` = −1 on every path (all branches reconverge at `0020AE1C`/`0020AE48`). |
| B7 | Pusher `0020AF10` leaves `01DFE40C` set | ACCEPT | `0020AF5B mov dword[rip+0x1bf34ab],edi` → `01DFE40C` = slot; push_back into per-slot queue (`rbp+0x1E63390+idx*32` = `01F83390` vec), `counter++` at `0020AFB4` (`01F832B0+idx*4`), notifier `00189120`. Exit `0020AFC8` — no −1 store anywhere. `edi>4` or `event==-1` skip the push but the marker still lands. |

### Independent mutants (not in FABLE's `0020AD3F`/`0020ACD2` set) (SWE2-AUDIT-SEM)

- **`0020ADCD` `je`→`jne`** (the `0001`-found test): flips exactly the `0001` edge —
  `sum_with_0001` E8 1→0, `sum_without_0001` E8 0→1, `sum_and_spc` E8 1→0; `spc_`, same-name, and both
  push cases unchanged, and `n0001` still reads nothing (the `0001` test is unreachable sans `sum_`).
  Distinguishes the claimed arm structure cleanly.
- **`0020AE14` `0F 45`→`0F 44`** (`cmovne`→`cmove`, spc_ flag polarity): only the `spc_` case fails
  (E9 1→0); all others pass. (Note: patching the instruction start `0020AE13` corrupts the `0F`
  prefix and crashes the emulator — the condition byte is at `+1`.)

### Replay stub disclosures (tier: NATIVE-REPLAY, unchanged) (SWE2-AUDIT-SEM)

Stubbed at entry per the harness: `0020A800` (path check → 1), `0020AA50` (extractor → planted name),
`001A5760` (assign), `001C34D0` (substring search), `001B31E0` (concat), `00861ED2` (memcmp),
`001C5750` (JSON reader → records arg), `00189120`/`0016D6A0`/`001A4250` (notifiers), allocator
`+0x18` (recording stub — frees counted, not freed). All stubs replace leaf helpers whose real bodies
were read statically for B3/B4; no stub sits inside the logic under adjudication. No live claim.

## Residuals (SWE2-AUDIT-SEM)

None blocking. The `sum_and_spc` case confirms precedence: a name containing both sets only `01F832E8`.
The flag-E9 else-input (`movzx` of its own cleared byte) is vestigial but harmless — documented above
for the reconstructor.
