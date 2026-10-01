# SECTION-05 (Update05) — owner's review of the encoded-id registry rewrite (OPUS, 2026-09-25)

SECTION-05 rewrites `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` (OPUS)
and the page `the-encoded-id-space-and-the-query-record.md` (mixed authorship, including FABLE's
2026-09-21 section), uncommitted. No revert: every later commit to the contract (EC7's batch-141
appends, `548f6a37b`) is present in the worktree. Evidence class NATIVE/STATIC.

## Verdict: ACCEPT THE CORRECTIONS · DISPOSITION NINE CONTRACT TOKENS AND THE PAGE'S FORTY

### Re-read from the image — agree

| claim | static finding |
|---|---|
| **Q05-01** the registry nibble is NOT the class; class = nibble + 5 | `00309440`: `nibble = cx >> 12`, `ja` above 0xE, returns `dword [01EEBCF8 + nibble*0x58]` — row `+0x38` of the table at `01EEBCC0`. That byte reads **5, 6, … 19** across the 15 shipped rows. The row index is the nibble; the class id it stores is nibble + 5. |
| **§5 byte +0x54 HAS a writer** | `0031CA3C movzx eax, byte [rbp+7] / shr al,1 / 0031CA42 xor al, byte [rbx+0x54] / and al,1 / 0031CA47 xor byte ptr [rbx+0x54], al` — a read-modify-write that replaces bit 0 with equipment row+7 bit 1 and preserves bits 1-7. **This refutes the page section "`+0x54` is read and never written" (FABLE, 2026-09-21)**, and it is exactly the defect class of OPUS block 176: a writer query that does not count `rw` reports a read-modify-write as no writer. |

**Not re-derived:** Q05-02..06, Q05-08..12 (accepted at the section's fixture scope).

### Dropped from the OPUS contract — each needs a disposition before publication

| HEAD token | what it cited | in the rewrite |
|---|---|---|
| `002FD530`, `002FD640`, `002FD780`, `002FD880` | the four mutation handlers of classes 14/15/18/19 that have no query handler | fact restated in the section's review; **addresses gone from the contract** — restore |
| `0032302E`, `00323036`, `00323039`, `00323041` | the validator's shared tail (`lea eax,[rcx-1]` / `cmp ebx,eax` / `jg` / `mov eax,1`) | gone — restore, or state why the new bounded validator table supersedes the listing |
| `EXP-100` | the evidence-legend entry for the isolated run | gone — restore |

The page's 40 lost addresses are in `overlay-drop-census-2026-09-25.tsv`; the page's authors (FABLE
for the `+0x54` section) disposition them.
