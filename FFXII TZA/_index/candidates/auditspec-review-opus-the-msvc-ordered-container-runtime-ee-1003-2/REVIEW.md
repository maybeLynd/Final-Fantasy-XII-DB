# SWE2-AUDIT-SPEC review: OPUS engine_explained interior citations (opus-the-msvc-ordered-container-runtime-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MSVC-ORDERED-CONTAINER-RUNTIME-EE-E950F` · Package: `_index/candidates/opus-the-msvc-ordered-container-runtime-ee-1003-2/` · Page: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md` (commit a19ddeadd)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 6 rows, fewer than 15, so all 6 were read clause by clause against the bytes. All 6 rows are correct, and so are their 30 anchors. All six corrections listed in the README are present in the `rows.json` text.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh from the package folder without `--apply` (`python -B`, at HEAD f49bb4021): `VERIFY 6 functions, 30 anchors`, `ALREADY`, `FAILS 0`, exit 0. The output matches the committed `.out`. `git status` on the package and the page was clean afterwards. `ALREADY` means the page block headed `... cloud-drafted, opus-the-msvc-ordered-container-runtime-ee-1003-2)` (page line 420) equals the rows.json rendering.
- `rows.json`: 6 rows, 30 anchors; rejected 0, skipped 8 (all marked as too large), missing 0, corrections 6.
- Semantic pass. **Every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...). Function extents come from `check_dispositions.load_functions`. rip targets were resolved to their sections: the gate dwords `01F3BA80`/`01F3BA8C`/`01F3BA90` are in `.data`, the `02EA0Bxx` globals are in the zero-initialised `.data` tail, and every format string is in `.rdata`.
  - `006DAFB0`: correct.
    - The first log has no line argument. The second log takes `edx`=0x43D (`006DAFF5`).
    - Every gate is `cmp dword,1` / `jb`, so the test is unsigned at least 1.
    - The `c` = `02EA0B70` test is at `006DB012`. Slot `+8` is called at `006DB03B` and `006DB054`, and each zero store sits inside its own non-null arm.
    - `00705520(c, 0)` (`006DB065` `xor edx,edx`, `006DB067`).
    - Negative `r` (`jns` at `006DB070`): the log uses 0x468 and `0071B3C0(r)` as `r8`, and `006DB0E2 mov eax, ebx` returns `r`.
    - `006FF840(d)` / `006DA8A0([01F3BA68], d)` and the zero store at `006DB11F` all sit inside the `d` non-null arm.
    - `006DB129 call 006E0370` with `rcx` = the incoming `rcx` (`rsi`), then `006DB133 mov qword [rax], rbp` with `rbp` = 0. This is the qword AT the returned pointer, so the correction is in the text.
    - Tail logs 0x47A, `00D8E9C8`/`00D8E7C8` and `00D8E85C`/`00D8E8B8`. `xor eax,eax` returns 0, and the null-`c` path joins it at `006DB136`.
  - `006DEB40`: correct.
    - Log 0x1C56.
    - Null `c`: log gated on `01F3BA8C`, 0x1C5A, then `006DEBBA mov al, 1`.
    - `00705520(c, 0)` at `006DEBD2`.
    - Negative `r`: 0x1C62 with `0071B3C0(r)` (`006DEC02`). Otherwise 0x1C66.
    - `02EA0B70` is re-read at `006DEC49`. The `006FF840` / `006DA8A0` calls follow under `je 006DEC6F`.
    - `006DEC80 mov qword [02EA0B70], 0` comes after the join, so it is unconditional (the correction is in the text). The flags for `jns` come from `006DEC74 test ebx,ebx`, and the `mov` instructions between leave them intact.
    - Byte returns: `006DEC8D xor al, al`, `006DECC3 mov al, 1`, with the 0x1C71 log on the non-negative path.
  - `0070E600`: correct.
    - `cmp byte [rcx],0` / `je`. The log is gated on `01F3BA80`/`01F3BA90` (0x72DC, `00D965F8`, `00D96640`). `0x80004005` is returned whatever the gate.
    - The descent over head `[rcx+0xB8]` is a lower bound: `0070E660 cmp [rcx+0x20], rdx` / `jae` records the node and goes `+0`, otherwise `+0x10`, and it stops on byte `+0x19`.
    - `0070E678..86`: node == head or `rdx` < key gives head, so `0x80070057`. The hit is therefore the equal key (unsigned).
    - `v` = `[node+0x28]` (`0070E69F`).
    - The second tree is at `rcx+0xC8` (`r14`), searched the same way. `w` = 0 when absent (`0070E6EA` / `0070E6EF`).
    - `00714DC0(rcx+0xB8, &t, node)` at `0070E701` (`r8` still holds the node). `00714DC0(r14, &t, m)` only when `w` is non-null (`0070E706`).
    - Slot `+8` of `v` at `0070E730`, `006E1130(w)` at `0070E740`, and the function returns 0.
  - `00713210`: correct.
    - `h` = `[rcx]`, `k` = `[r9]` (`00713246`).
    - `r10b` = the incoming `r8b`. When it is non-zero, `cmp [rax+0x20],rdx` / `setae` (left when the key is at least `k`). When it is zero, `cmp rdx,[rax+0x20]` / `setb`. Left is `+0` and right is `+0x10`.
    - `0071323D mov r8b, 1` before the nil-root skip, so an empty tree counts as "went left" with `p` = `h`.
    - `0071328A cmp r9, [r11]`: a leftmost `p` inserts at once, with `r8b` = 1 (`0071329E`).
    - `007132BD..16`: if `p` is the head, `q` = `[h+0x10]`. Otherwise `q` is the in-order predecessor: the rightmost node of the left subtree, or the ancestor climb with `cmove`. When the last step went right, `q` = `p`.
    - `0071331D cmp [rbx+0x20], [r9]` / `jae` means insertion happens only when `q`'s key is below `k` (unsigned).
    - The calls to `00712F60` at `007132A6` and `00713337` take `rcx` (unchanged), `&t` = `rsp+0x50`, `r8b`, `r9` = `p`, the incoming `r9` and the fifth argument (`[rsp+0x70]`).
    - `mov rax,[rax]` / `mov [rdi],rax` (`007132AB`, `0071333C`) stores the qword AT the returned pointer (the correction is in the text). Byte `[rdx+8]` = 1.
    - Otherwise `00713350 call 00210EB0(fifth)`. That thunk jumps to `0019C590`, which jumps through IAT `008C2B48` to `free`. Then `[rdx]` = `q` and byte 0. The function returns `rdx` (`rdi`).
  - `00713370` and `007134D0`: correct, and identical to `00713210`.
    - A listing normalised over the 351-byte extents (intra-body branch targets made relative, external targets named) shows 98 instructions in each, with 0 differences.
    - The external calls are `00712F60` at +0x96 and +0x127 and `00210EB0` at +0x140 in all three.
    - All three rows carry the same text and the same anchor offsets (+0x48 `cmp`, +0x96 `call`, +0x127 `call`, +0x13B `mov`, +0x140 `call`). Each row therefore names its own callees, which are the same callees in all three.
  - Anchors: all 30 are instruction boundaries strictly inside their bodies and have the recorded mnemonics. Each one sits on a clause of its own row: log calls, the vtable calls, the `00705520` / `006E0370` / `00714DC0` / `006DA8A0` / `006E1130` / `00712F60` / `00210EB0` calls, the descent `cmp` instructions, the `02EA0B70` zero store, and the fifth-argument load.
- Family rule (SWE2-DATA's family-declaring-page rule, `progress.cite_credits` / `family_rule_inputs`).
  - This page declares the accepted family `MSVC ordered-container (std::_Tree) runtime` (22 members). That family is **not in scope**: the page has no committed `fam_rows.py` + `spec.json` + `rows.tsv` checker, and no accessor-descriptor record. The base rule therefore applies.
  - None of the 6 functions is a member of that family. All 6 are members of `PPFX post-effect library`, which is declared on another page.
  - A strictly interior anchor here credits `engine_explained`, so the README's "All 6 rowed functions now measure A" is consistent with the rule.
  - `interior_applier.py` is not a family-checker shape that progress.py reads. It checks anchor boundaries and mnemonics, and does not derive values from the image or refuse a swapped value. None of these rows depends on it being one.
- Non-blocking notes.
  - The README's correction notes say the three insert bodies have "99 instructions each". The census extents decode to 98, ending at `ret`. That is a count slip in the README prose and touches no row.
  - In `006DAFB0`, `00705520` receives `02EA0B70` re-read at `006DB05E`, after the two slot-`+8` calls, rather than the `c` tested at `006DB012`. The sentence binds `c` once. A callee that rewrote `02EA0B70` would make these differ. That has not been shown, so the sentence is not false.
- Limits hold: body statements only, static evidence. The drafting agent and OPUS's re-read are not independent review; this record is.
