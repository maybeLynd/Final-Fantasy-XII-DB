# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-accessor-call-form-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-ACCESSOR-CALL-FORM-1003` · Package: `_index/candidates/opus-ee-accessor-call-form-1003/` (rows committed in `c49f03691`; checker, README and `members.tsv` revised in `c480be543` with `rows.tsv` unchanged; reviewed at HEAD `33eb7192f`, package unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`, section "Per-member rows: the descriptor function each call-form accessor calls"

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 153 rows are correct against the bytes. An independent re-derivation matches all 153 on every column. Two statements are wrong, though, and need narrowing:

- The lead says "What differs from member to member is G". That is false. Every member also differs at two `lea`s of its own `__FUNCTION__` string (`"Phyre::PScripting::PScriptAccessors::PObjectAccessor<class Phyre::T const &>::Get"`). That string is unique per member, across both templates.
- The two "value shared" exclusions (`00676700` and `00683040`) give the reason "no member-specific instruction". That is false for the same reason. Each loads its own `__FUNCTION__` string (`PBase const &` and `PBase &`). The pair also contradicts the lead's "inside each template no two members call the same one": both are reference-form members, and both call `006372A0`.

There is also a members-list defect. The other six exclusions are not `PObjectAccessor<T>::Get` bodies at all, and none of the six is in the page's 747-entry appendix. That contradicts the members file's own selector, "the page's appendix Get bodies (747)".

No row changes are needed.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** `fam_rows.py check` was run in place with `-B` under the analysis venv python, which has capstone and pefile. It wrote nothing.
  - Exit 0: `members 161, committed rows 153, declared exclusions 8` / `control swapped-value: refused (2 ...)` / `control moved-anchor: refused (1 ...)` / `control swapped-group: refused (1 ...)` / `known answer 005A05D0: anchor 005A060A references 005A02D0 in its raw bytes = committed value` / `FAILS 0`.
  - The output is identical to the committed `fam_rows_check.out`, apart from line endings.
- **What the checker tests.**
  - `ex_accessor_call` decodes the census extent (`check_dispositions.load_functions`), not a fixed window. It takes every direct call outside `skip_calls` (`00682980`, `00811130`, `00812960`) and `form_calls` (`0063BC00`, `008119F0`), and requires that they all go to one G.
  - It requires exactly one form call, then anchors the first call to G and names G's class from the `r8` string before G's call to `00632C90`/`00632D80`.
  - `derive_all` drops members whose (template, G) pair is shared.
  - `compare` checks all six columns.
  - It does not check the `__FUNCTION__` string, the base-chain walk, or any other part of the lead's shared shape.
- **Controls' sensitivity.** The three mutation controls run in-memory mutations of `rows.tsv` through `compare`. Run in memory:
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, `cmd_check` still printed all three controls "refused", the known answer matched, and the result was `FAILS 0`. **The three mutation controls cannot fail while the extractor returns anything.** They test `compare`, not the derivation.
  - The comparison is sensitive. Mutations of row 76 each failed (FAILS 1): value taken from row 77, anchor + 1, template flipped, name changed, and row deleted.
  - **The known answer can fail.** It decodes the anchor's `E8 rel32` without capstone. When row 0's value was wrong in both the extractor and `rows.tsv`, the line printed FAIL. The same wrong value placed on row 76 instead gave FAILS 0, so it guards row 0 only.
- **Independent census.** This used the disw.py image reader over `graph/functions.tsv` extents, not retool and not fam_rows.
  - **153 of 153 rows are identical** to `rows.tsv`: G, first-call anchor, `call`, and template.
  - **Template cross-check:** each member's `__FUNCTION__` string ends in `&>::Get` for every reference-form row and `*>::Get` for every pointer-form row (153 of 153).
  - **Name column:** 14 rows are named, and all 14 agree with the class in the member's `__FUNCTION__` string. 139 are empty, because G passes the name through a global (for example `005B6E00`: `mov r8, [02CB5C08]` before `call 00632D80`) and not as a literal `lea r8`. "Empty otherwise" holds in that sense.
  - **G sharing:** 76 G are shared by one pointer and one reference row, and 1 G is pointer-only. (template, G) is unique across the rows.
  - **Four masked forms:**

    | members | template | size | calls to G |
    |---|---|---|---|
    | 69 | reference | 270 B | 2 |
    | 7 | reference | 260 B | 2 |
    | 70 | pointer | 320 B | 1 |
    | 7 | pointer | 318 B | 1 |

    Within each form, the only positions that vary (in-body jumps excepted) are the call(s) to G and **two `lea`s of the member's `__FUNCTION__` string**. For example, in `005A05D0` they are `005A0646` and `005A06A3`, `lea rax, [00D27D60]` -> `"...PObjectAccessor<class Phyre::PTimer const &>::Get"`. In `005A06E0` they are `005A075D` and `005A07F3`, `[00D27D00]` -> `"...<class Phyre::PTimer *>::Get"`. Each stores its string to `02E41010` before `call 00812960`.
  - The `__FUNCTION__` string is distinct for each of the 155 Get bodies: the 153 rows plus `00676700` and `00683040`. The `__LINE__` immediates (`02E41008`) and the message strings are form-constant.
- **Lead shape, read against `005A05D0` / `005A06E0` and the census.**
  - `00682980` then `00811130`, G, the walk over `[descriptor + 0x78]` comparing against G's result, and the diagnostic via `00812960`: all exact.
  - The reference form calls `0063BC00(G())` only on the null-object path, and returns its result. `0063BC00` returns `[rcx+0xD8]`, or builds an object from `+0xC0`/`+0xF8`, so "a default object" is fair.
  - The pointer form's `008119F0` is likewise on the null path. The form call is exclusive (exactly one form for every row).
  - "Each row anchors the member's first call to G" is exact. In the reference form, that call is on the null-object branch (for example `005A060A`).
  - **"What differs from member to member is G" is not exact:** see the `__FUNCTION__` `lea`s above. "Inside each template no two members call the same one" is true of the rows, but not of the family: `00676700` and `00683040` are both reference form, and both call `006372A0`.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 11, 22, 33, 43, 54, 65, 76, 87, 98, 109, 119, 130, 141 and 152: `005A05D0`, `005B8D40`, `005BB990`, `005F0E90`, `005F1930`, `005F5CE0`, `005F6AA0`, `005F7860`, `0061A610`, `0066B180`, `0066D0C0`, `0067EBC0`, `006BDB30`, `006D3350` and `0087A410`.
  - Anchor, G and template match the bytes. Names agree: `005A02D0` -> PTimer (`lea r8, [00D27BA8]` before `call 00632C90`), `006143B0` -> D3D11_DEPTH_STENCILOP_DESC and `006B33F0` -> PMatrix4x3. G is empty where it is passed by global.
  - **15 of 15 exact.**
- **Exclusions: all 8 inspected.**
  - `00676700` and `00683040` are genuine reference-form Gets (260 B form) that share G `006372A0`. The stated reason "no member-specific instruction" is **false**: each has its own `__FUNCTION__` `lea`. Leaving them without a row is conservative, and it costs them only credit they could earn.
  - `005D8CA0`, `005D8D70` and `0068F0F0` (206 B each) are lazily initialised static enum-descriptor getters, and the page describes them as such (§7, "the identical shape ... `PSamplerStateFilterFormatType` ..."). Their only calls are `_Init_thread_header` `008092FC`, `atexit` `00808B90` and `_Init_thread_footer` `0080929C`. The reason "3 distinct member-specific call targets" is mechanically true, but these are CRT calls, not member-specific.
  - `00810810` (299 B), `00811470` and `00811640` (190 B each) are Lua 5.2 value helpers. The page itself calls `00811640` "a Lua 5.2 value helper", and `00811470` ends in `cvttss2si`. Their single calls are `00821520` / `00823220`.
  - **None of the six calls `00682980` or `00811130`, none has a `__FUNCTION__` string, and none is in the page's 747-entry appendix.** None is in `members/object-pointer-accessors.tsv` or `members/object-reference-accessors.tsv`. They are outside the family, so `members.tsv` over-includes, against its own selector line.
  - **Defect (b), a fixed byte window, does not arise:** the extractor reads the census extent, and every row's anchor lies inside it (`finish_check`).
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction that distinguishes the member within its template: the first call to G, with (template, G) unique. Each row states G and the template, both read from the image.
  - The checker derives every row from the image and refuses a swapped value through `compare`.
  - **Conditions met for the 153 rows.** Credit is unaffected by the narrowings: the six non-Gets earn nothing from this family either way.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing 1: the lead, in spec.json `lead` and the page section.** Replace:

> What differs from member to member is G: inside each template no two members call the same one (the pointer and reference Get of one class share it).

with:

> What differs from member to member is G and the member's own `__FUNCTION__` string (`"...PObjectAccessor<T &>::Get"` / `"...<T *>::Get"`, loaded by two `lea`s before the diagnostic). Among the rows, no two members of one template call the same G (the pointer and reference Get of one class share it). The two `PBase` reference Gets, `00676700` and `00683040`, share G `006372A0` and have no row.

**Narrowing 2: `excluded.tsv` reasons and README counts.**
- For `00676700` and `00683040`, replace "no member-specific instruction" with "G shared with the other PBase reference Get (`006372A0`); the member is distinguished only by its `__FUNCTION__` string, which this checker does not derive".
- For `005D8CA0`, `005D8D70`, `0068F0F0`, `00810810`, `00811470` and `00811640`, either drop them from `members.tsv`, or give the reason "not a `PObjectAccessor<T>::Get` body (no `00682980`/`00811130` call, no `__FUNCTION__` string, not in the page's appendix)".
- Change the README's "3: 3 distinct member-specific call targets / 3: template form not decided" to match.
- If the six stay in `members.tsv`, its selector line ("the page's appendix Get bodies (747)") is false. Under the progress.py implementation of §1, declaring them as members of this family would also make their other citations on this page count only through a row, which none of them has.

**Notes (non-blocking):**
- **Control repair.** The three mutation controls test `compare`, not the derivation. T6 (an echo extractor) passes all of them with FAILS 0. The raw-byte known answer is sensitive but covers row 0 only. For this kind, extend it to every row: `_raw_ref(anchor) == value` decodes `E8 rel32` for all 153 rows. Cross-check the template against the `__FUNCTION__` suffix as well.
- **A stronger anchor exists.** The `__FUNCTION__` `lea` distinguishes every member uniquely, across templates, including the two PBase Gets. It would also fill the 139 empty class cells. This is optional; the current anchors meet §1.
