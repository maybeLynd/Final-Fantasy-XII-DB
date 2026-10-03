# SWE2-AUDIT-SPEC review: FABLE PObjectAccessor<T>::Get required class descriptors

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE) · 2026-10-03 ·
Task: `FABLE-REQ-AUDITSPEC-ACCESSOR-DESCRIPTORS-1003` · Package: `_index/candidates/fable-accessor-descriptors-1003/`
(uncommitted at review time; reviewed as on disk 04:15Z) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped to the package. 591 rows, each anchored on the member's distinguishing `lea rdx,[rip+X]` and stating X and the
class name. The 156 getter-form members get no row; their reason is stated. This review is the auditor step of the T2
family-wide disposition. **Counting still requires OPUS's T2 adjudication**, which an OPUS page-lead yes satisfies only
if it explicitly covers the family-wide disposition (`FABLE-REQ-OPUS-ACCESSOR-DESCRIPTOR-ROWS-1003`).

## SWE2-AUDIT-SPEC checks

- **`desc_check.py --self-test` re-run:**
  - exit 0, stdout identical to `desc_check.out`;
  - control line: `00599770` checks verified against its own descriptor and mismatch against `02D363A0`;
  - dispositions 747 = 591 verified + 156 getter form, 0 unresolved, 0 mismatch, FAILS 0;
  - the regenerated JSON is equal to `accessor_desc.json`.
- **`applier.py` dry run:** "rows 591 checked at the bytes", WOULD PATCH, FAILS 0.
- **Route 3 at the bytes:**
  - Core constructor `006318A0` does `lea rax,[rip+…] → 00D58400` = `"PBase"`, then
    `mov qword ptr [rbx+30h],rax` (`0063190B`).
  - Static initialiser `00164180` does `lea rcx,[rip+2B940E5h] → 02CF8270`, then `call 006318A0`.
- **Route 2 at the bytes** (wrapper, for one sampled row): initialiser `00166F60` does `lea rcx → 02E518D0`, then
  `call 006B3F40`. That wrapper loads `r8 → 00D80038` = `"PNode"` and calls `00632D80`. This matches row `006B5170`
  (`PScene::PNode *`).
- **Row sample**, 10 random verified rows (seed 1003), 5 reference form and 5 pointer form: `0064CD70`, `00619300`,
  `0069ADB0`, `0064BB70`, `0064B150`, `00636CB0`, `005FC470`, `006C41C0`, `0064EA70`, `006B5170`.
  - In each one the anchor is a `lea rdx,[rip+…]` whose target equals the stated descriptor.
  - It precedes the `cmp rcx,rdx` (reference) or `cmp rax,rdx` (pointer) compare.
  - The class name matches the appendix type's leaf.
  - 10/10 exact.

## SWE2-AUDIT-SPEC notes

- The rows satisfy the ruling: an interior anchor on the distinguishing instruction plus a member-specific value,
  verified against the image. The shared shape is stated once in the section.
- The scoped family sentence (`AUDITSPEC-REQ-OPUS-EE-FAMILY-SENTENCE-1003`) is pending with OPUS. These rows count under
  the current text and under the proposed sentence alike.
