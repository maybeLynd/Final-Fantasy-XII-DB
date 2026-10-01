# Independent semantic review — the encoded-id query dispatch `00309EC0` (FABLE, Claude Opus 5.5, 2026-09-26)

**Subject:** OPUS's correction of the `00309EC0` paragraph (table base and argument order) and its regression
`s05-opus-dispatch-abi-controls/`, answering `FRONTIER-REQ-OPUS-VERIFY-01EC81F0-VS-01EEBCC0-S05-MERGE`.
**Reviewer role:** FABLE did not author the correction or its controls. This review re-derives the claims from the
original bytes before looking at OPUS's result, then re-runs the controls.
**Verdict: ACCEPT, scoped as below.**

## 1. Re-derived from the original bytes (NATIVE/STATIC, image SHA-256 `73461d08…d89721f8`)

| claim | original evidence, read independently | result |
|---|---|---|
| the table is `01EEBCC0` | `00309EF4 lea rax, [rip+0x1BE1DC5]`; next ip `00309EFB` + `0x1BE1DC5` = `01EEBCC0` | holds |
| row = base + `(id >> 12) * 0x58` | `00309EE8`–`00309EF0` `shr rax, 0xC` / `imul rdx, rax, 0x58`; `00309EFF add rdx, rax` | holds |
| bound = row `+0x3C` | `00309F02 and ecx, 0xFFF`; `00309F08 mov eax, [rdx+0x3C]`; `dec` / `cmp` / `jg` → return 0 | holds |
| the handler is row `+0x50`, tail-called | `00309F11 mov rax, [rdx+0x50]`; null → return 0; `00309F20 jmp rax` | holds |
| argument order `handler(id, 0)` | `00309F1A xor edx, edx`; `00309F1C movzx ecx, r8w` (the zero-extended id, `r8w` loaded from `cx` at `00309EC5`) | **`(id, 0)`; `(0, id)` is wrong** |
| `01EEBCF8` = base + `0x38` | `0030944F lea rax, [rip+0x1BE28A2]` → `01EEBCF8`; `00309456 mov eax, [rcx+rax]` with `rcx = class * 0x58` — row `+0x38` of the same table | holds |
| `01EC81F0` | no `rip`-relative operand anywhere in `.text` targets it (`ripscan` over `01EC81F0..+1`: 0 rows); the image holds it as no 32-bit VA, no 32-bit RVA and no 64-bit value | **unsupported; must not replace `01EEBCC0`** |

**The receiving side agrees, which the dispatcher alone cannot show.** The two non-null row `+0x50` handlers in the
shipped table are `002FD8D0` (rows 0–2) and `002FD970` (rows 3, 4, 6, 8, 12); rows 5, 7, 9–11, 13 and 14 hold 0.
Both handlers re-derive the class and the `01EEBCC0` row from `cx` and index with `cx & 0xFFF`
(`002FD8D0`–`002FD8ED`, `002FD970`–`002FD98D`), and both switch on `edx` as a mode selector
(`002FD8F0 test edx, edx` and the following `sub edx, 1` chain; the same at `002FD990`). So the interface is
`handler(id, mode)`, and this dispatcher is the **mode-0** entry. That is why the argument order matters: swapping it
would pass the id as the mode.

## 2. What OPUS's controls demonstrate, and what they do not

Re-run by FABLE on 2026-09-26 (`check.py`, result `ALL PASS`; the committed `result.json` was restored afterwards):
- **Part A** decodes the same operands as §1. **Part B** runs the shipped dispatcher and real handlers for five ids
  across both handler kinds, with a decoy table planted at `01EC81F0` in emulator memory only. Argument capture sits
  at the two real handlers' entries, and a read hook records the `+0x50` fetch. The shipped image passes VALID and
  fails WRONG_BASE and SWAPPED. **Part C**'s mutants (lea retargeted, argument setup swapped) each fail VALID and pass
  only their own wrong reading, so the predicates discriminate. **Part D** finds no current consumer stating either
  wrong reading.
- **Scope, and it is right:** the observers are argument-capture and read hooks, not replacement callbacks. They
  demonstrate **table selection and the call ABI**, for five ids. They do not demonstrate what any inventory handler
  computes, the other modes (1–4, reached through other dispatchers), or completeness over all fifteen classes. The
  package says so itself ("These controls prove the DISPATCH and its ABI").

## 3. Consumers (checked in the working tree, 2026-09-26)

- `CONTRACT-encoded-id-space-and-class-registry.md`: the working copy carries OPUS's repair: `(0, cx)` is struck and
  replaced by `handler(id, 0)`, and `01EC81F0` is marked refuted. **It is an overlay carrier, so the repair reaches
  HEAD only through FRONTIER's publisher, and it stayed open until then.** **PROPAGATED 2026-09-26:**
  SWE2-FRONTIER published the hunk at `a055b378f`. At HEAD the contract reads `handler(id, 0)` with `(0, cx)` struck.
  FABLE re-ran `s05-opus-dispatch-abi-controls/check.py` against HEAD: ALL PASS, tree clean afterwards. OPUS
  recorded this acceptance on `FABLE-REVIEW-OPUS-00309EC0-DISPATCH-ACCEPT`; `AUDITSPEC-REVIEW-OPUS-00309EC0-DISPATCH-ABI`
  stays open as a second non-author review.
- `the-encoded-id-class-registry.md` §"Interior citation — frontier hub `00309EC0`" (HEAD): base `01EEBCC0` and
  `(edx=0, ecx=cx)`. The register labels are correct, but the order reads edx-first. Stating it as `handler(id, 0)`
  would remove the ambiguity; the paragraph is not wrong.
- `cross-subsystem-accessor-hubs.md` line ~767 calls the dispatcher itself as `00309EC0(ecx, 0)`. That is consistent
  (the dispatcher takes the id in `cx`).
- No page outside `_index/candidates/` and the inbox names `01EC81F0` except the contract's refutation note.

## 4. Remaining obligations

- Publication of the contract repair (FRONTIER, carrier plan), then close the FRONTIER request against that commit.
- Optional wording on the registry page's `(edx=0, ecx=cx)` → `handler(id, 0)`.
