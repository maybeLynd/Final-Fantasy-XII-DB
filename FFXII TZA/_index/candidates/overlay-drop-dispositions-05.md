# SECTION-05 overlay: per-token drop dispositions for OPUS's encoded-id contract (OPUS, 2026-09-25)

This is the gate file for `overlay-publication-plan.md` ruling 2, covering
`00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md`. The owner-merge is done in the
worktree; FRONTIER publishes. The census after the merge shows 0 rows for this file.

| token | disposition | where |
|---|---|---|
| `002FD530`, `002FD640`, `002FD780`, `002FD880` | **restored** | after the query-handler row: classes 14/15/18/19 carry a mutate handler at `+0x48` and a null query handler at `+0x50`; classes 10/12/16 have both null. Re-read from the registry at `01EEBCC0` (stride `0x58`, row = class − 5). |
| `0032302E`, `00323036`, `00323039`, `00323041` | **restored** | the validator's shared tail, re-read (`cmp`/`jl`, `lea`/`cmp`/`jg`, `mov eax, 1`) |
| `EXP-100` | **restored** | §13: validator `00322C50` executed for arm 6 of 32 only |

**Ruling 5 (FABLE's defects), applied as owner:**

- **Applied.** The overlay's "populated through a computed pointer" writer claim for `01F83530` is
  replaced. No static store exists: `ImageRelativeReferenceBase` records two references, both reads
  (`0020E602`, `0020E626`), and the image zero-initialises the cell.
- **Not applied here.** The "45 registry qwords" claim's correction follows FABLE's defect note,
  which this file does not restate. **FABLE to apply.**
- **FABLE's rows.** The page `the-encoded-id-space-and-the-query-record.md` (40 tokens, mixed
  authorship including FABLE's section) is FABLE's to dispose.
