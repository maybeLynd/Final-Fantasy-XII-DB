# SECTION-04 (Update04): contract owner's review of the widget receiver rewrite (OPUS, 2026-09-25)

**What changed.** SECTION-04 rewrites `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`, which
OPUS owns: it was authored 2026-09-08 and falsification pass 1 is OPUS's. It also rewrites two pages
in the same folder. All three are an **uncommitted overlay** on the 2026-09-22 snapshot. Its one
type row, `WidgetSingleton02AEE4C0`, is already in HEAD (SWE2-STRUCT `7abc4cad5`).

**Evidence class.** NATIVE/STATIC; every claim below was re-read from the shipping image. The
section's fixture was not replayed.

## Verdict: ACCEPT ALL FIVE CORRECTIONS · RESTORE ONE DROPPED PARAGRAPH BEFORE PUBLICATION

### Re-read from the image: all agree

| claim | static finding |
|---|---|
| raw `002465F0` has no object-pointer return guarantee | The tail leaves RAX from `001EDDA0` (`0024674A`, `jne` to the epilogue) or `00314960` (`00246753`); `00808C40` is the cookie check and preserves RAX. There is no `mov rax, <obj>` before `0024677A ret`. |
| `00245000` restores the object | `00245006 mov rbx, rcx` … `00245016 mov rax, rbx` |
| `00244F50` restores the object | `00244FB7 mov rbx, rax` (the allocation) … `00244FD7 mov rax, rbx` |
| the consumer's receiver is RSI and the message is RBX | `003939D1 mov rbx, rdx` / `003939D6 mov rsi, rcx`; RSI is never reassigned in the body |
| `003939F7 [rbx+8]` is the message; `00393A23` is arithmetic | `003939F7 movzx eax, byte [rbx+8]`, then `003939FB xor ebx, ebx`, so `00393A23 lea edx, [rbx+0x15]` = 21 with no memory access |
| two objects: 0xD8 asset widget, 0x1D0 consumer | `00394460` makes its preliminary calls, then allocates `0xD8` under the `02AEE4C0` guard (`0039449F`). `00394530` allocates `0x1D0` (`0039456C`). The consumer publishes **itself** at `02AEE4C8` (`00393A11`). |
| the asset widget's +0xC0/+0xC8/+0xD0 are its own | Its handler `00394070` sets `00394076 mov rbx, rcx` (self) and addresses them through RBX: `00394097` (+0xC8), `003940A8`/`003940B9` (+0xD0), `003940E3`/`003940FC` (+0xC0). *(The later +0xC0/+0xC8 sites at `0039420B`/`003942CE` belong to a different body starting after `0039412C`, whose receiver is not re-derived here.)* |

The replaced sentence on the constructor page, "a widget's first frame runs before its parent's
constructor has returned", becomes "its initialization-message handler runs … not proof that a
frame/tick has elapsed". That is a **narrowing** of the claim, and it is right: the handler call
inside construction is a message dispatch, not a frame.

### Dropped by the overlay: restore before publication

| file | HEAD text | in the overlay |
|---|---|---|
| `the-title-asset-singleton-and-its-distinct-consumer.md` | the `00249320` paragraph: the class-3 node factory the consumer calls (`00249210(rcx, rdx, r8, 3, 0)`, `00249660` installs at `qword[+0x10]`, `qword[+8]` returns), and "Interior anchor `00249337`" | **gone**. It was added after the overlay's base (the file's latest commit is `500157896`, EXP-189, 2026-09-25), so this is the snapshot artefact again, not a correction. |

Nothing else is dropped. The contract loses only `last_reviewed` and the corrected return cell, and
the constructor page loses only frontmatter it restates and the narrowed sentence above.
`overlay-drop-census-2026-09-25.tsv` did not list these files, because the paragraph arrived after
it ran.

### Added from this review (published with it)

- **`WidgetConsumer02AEE4C8`** (0x1D0, `PTR 0x02AEE4C8`): the consumer had no type, and it was the
  contract-named-state census's one widget UNDECLARED. Its fields come from its handler (RSI = self
  throughout) and a cell-seeded fixpoint census:
  - `+0xC0`: a byte copied from the creation message;
  - `+0xC4`: flags;
  - `+0xC8`: a pointer;
  - `+0xD0`: a 256-byte text buffer (`002B4090` with size 0x100), ending exactly at 0x1D0;
  - `+0x00..+0xBF`: the shared widget header, not re-censused.

**Publication path.** Restore the paragraph above, then publish the three files. OPUS will
re-verify the merged file. This review publishes none of the overlay files itself: they are an
external section's production, and their acceptance is recorded here, not absorbed.
