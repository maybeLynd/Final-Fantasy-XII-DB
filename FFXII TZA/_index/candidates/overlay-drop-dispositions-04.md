# SECTION-04 overlay: per-token drop dispositions (OPUS, 2026-09-25)

This is the gate file for `overlay-publication-plan.md` ruling 2. The owner review is
`section04-owner-review.md` (`75ed03c7b`), which ACCEPTS all five corrections. The owner-merge is done in
the worktree; FRONTIER publishes.

| file | token | disposition |
|---|---|---|
| `the-title-asset-singleton-and-its-distinct-consumer.md` | `00249320`, `00249210`, `00249660`, `00249337` | **restored**. EXP-189's class-3 node-factory paragraph was appended to the overlay page, marked "Restored by the owner". It was re-read first: `00249324 mov r9d, 3`, `00249332 call 00249210`, `00249337 lea rcx, [00249660]`, `0024933E mov [rax+0x10], rcx`, `00249342 mov rax, [rax+8]`. |
| `CONTRACT-widget-object.md` | none dropped | the rewrite removes only `last_reviewed` and the return cell it corrects |
| `the-widget-constructor-and-object-sizes.md` | none dropped | it narrows "first frame" to "initialization-message handler" |

**Status: every SECTION-04 census row is disposed.**
