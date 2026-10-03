# SWE2-AUDIT-SPEC review: OPUS engine_explained interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-D81A9` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-2/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md` (commit a19ddeadd)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 5 rows, fewer than 15, so all 5 were read clause by clause against the bytes. All 5 rows and their 25 anchors are correct. No row changes. One README sentence names a spot-check on a function from another package, and it must be replaced (below).

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply`. Output: `VERIFY 5 functions, 25 anchors`, `ALREADY`, `FAILS 0`, exit 0. The page block equals `rows.json`, and `git status` on the page and the package was clean afterwards (HEAD f49bb4021).
- `rows.json`: 5 rows, 25 anchors. Rejected 0, skipped 3 (`0017AC50`, `0017B010`, `0017B580`), missing 0, corrections 2.
- Semantic pass: **every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...). The extent comes from `check_dispositions.load_functions`, and rip targets were resolved to their section, IAT name and string.
  - `0016EA80` (415 B), exact.
    - Early returns:
      - `cmp [rdx],rax` / `jne` with eax 0 (`0016EA95`).
      - `d` = `[rcx+0x1B0]` null (`0016EAA8`).
      - `[d+0x4440]==1` / `[d+0x1E68]==0` go to `xor eax,eax` (`0016EAE8`/`0016EAF5`).
    - The stack block `rsp+0x20` is zeroed (3 qwords + 1 dword). The `0x10000` bit copies `[rcx+0xFC/0x100/0x104]` (`0016EAAE`).
    - `00177A70(d+0x12C0, rsp+0x40, rsp+0x20)` (`0016EB25`), then `00125740()`, then `test ebx` / `jne` → 0.
    - The fill of `m = rcx+0x118` (`0016EB41..EBF0`) matches every offset, width and source:
      - `+0x10` = `lea eax,[rcx+0x4f]` / `and 0xfffffff0` with `ecx` = `s+4`.
      - qwords `+0x30/38/40` = `s+0x38/40/48`, `+0x70` = `s+0x58`.
    - `[rsi]=r9` (`0016EBF8`) and `rax=r9`.
  - `0016ECE0` (349 B), exact.
    - Returns 8 for `f` null or `[rcx+0x1A8]!=0` (`0016ECF3`/`0016ED00` → `0016EE30`).
    - The descriptor at `rsp+0x20..0x44`, qwords `0x58..0x68` and dword `0x84` = (`[f+0x58]`-w)>>1 are in the stated order. `w2`/`h2` = `lea +1` / `shr 1`.
    - Index select `cmp ecx,1/2/4` → `[b+0x9D4/0x9D8/0x9DC]` (`0016ED8F..EDAE`). Otherwise `0016DE20(b,1,'Invalid reference frame')`, where the string is `.rdata` `01CEB6B8`.
    - `e` = `b+0x780+0x90*idx` (`cdqe`; `lea rcx,[rax+rax*8]`; `add rcx,rcx`; `*8`). The four compares are `+4`=h (`0016EDBD`), `+0`=w, `+0x18`=h2, `+0x14`=w2.
    - `00173FA0(e, rsp+0x20)` (`0016EDF2`), else `'Incorrect buffer dimensions'` (`.rdata` `01CEB6D0`).
    - Both paths return `[rbx]` (`0016EE16`).
  - `0016F080` (355 B), exact.
    - Leaf 0 (`0016F08A`); `cmp eax,1` / `jae` → leaf 1 (`0016F0A3`).
    - The feature word is built by `cmove` chains. Bit `0x10` is set only when ecx bit `0x200` is set (`0016F0E6`).
    - `xgetbv` runs only when ecx & 0x18000000 = 0x18000000. XCR0 & 6 = 6 gives `or 0x40`.
    - When max leaf ≥ 7 (`jb`, unsigned), leaf 7 runs, and leaf-7 `ebx` bit `0x20` gives `bts 7`.
    - `and r8d,0x10` (`0016F140`) clears both bits.
    - The six `cmovne` pairs and destinations match the sentence pair for pair. Destinations are `02F97528`, `02F97510`, `02F97500`, `02F97520`, `02F97508` and `02F97518`, in the `.data` zero-initialised tail (mutable). The last store is `0016F1D6`.
  - `0016F2A0` (423 B), exact.
    - `malloc(0x44A7)` through IAT `008C2B40` (`0016F2C8`). A null result reaches `xor eax,eax` (`0016F2F1` → `0016F337`).
    - `a` = (`p`+0x27) & ~0x1F, `[a-8]=p`.
    - Thunk `00861EC0` → IAT `memset`, with 0x4480 bytes.
    - Thunk `00861EF6` → IAT `__intrinsic_setjmp` (`0016F30D`).
    - The longjmp path stores 0 to `+0x1318`, calls `00172750(a+0x12C0)` and `free([a-8])` through IAT `008C2B48` (`0016F331`), and returns 0.
    - The normal path's call and store sequence matches (`0016F350..0016F3E2`). The memset loop puts byte `i` at `a+0x2AD0+0x10i`, i<4 (`jl`).
    - The once-guard on `02EBA2EC` (`.data` tail):
      - `lock cmpxchg` 0→1 (`0016F3E9`), then `0016F1F0()` and `lock inc`.
      - Otherwise a check-first `lock cmpxchg` 2/2 (`0016F409`/`0016F411`), then `Sleep(0)` through IAT `008C21B0` in a loop.
    - Returns `[rsp+0x20]` = `a`.
  - `0017A320` (368 B), exact.
    - `movsxd rbx,[rcx+0x1E7C]`. `r` = `rcx+0x42C0`, `[rdx+2]=0`, `[rdx]=0017A180(r)` (`0017A340`).
    - When `m` = 4: `[rdx+3]=1` (`0017A381`). The loop `esi` < 0x10 (`jl`) stores to `rdi+0xC+4i` (rbx pre-incremented from `rdi+8`).
    - `a` (above):
      - `i`≥4 gives `[rbx-0xC]`, which is result `i`-4.
      - Otherwise the record at `rdi-0x4C*s`. Byte 0/1/2/3 gives 0/2/3/1, and byte 4 gives dword `[r14+rbx+rdx]`, which is result `i`+12 (`0017A3C6`). Anything else gives 0.
    - `l` (left):
      - `i`&3≠0 gives `[rbx]`, which is result `i`-1.
      - Otherwise the record at `rdi-0x4C`, where byte 4 gives result `i`+3.
    - Table `01CDBCB0` (`.rdata`) + 9*(10a+l), with signed `movsxd` (`0017A44B`).
    - Every path reaches `0017A250(r, 01CDB9C8)` → `[rdx+1]` (`0017A485`).
- Anchors: all 25 are instruction boundaries strictly inside their function, have the recorded mnemonic, and sit on the clause they are listed for.
- README corrections section: both corrections are reflected in the row text:
  - `0016F080`: the 0x40/0x80 bits are cleared by the final AND.
  - `0016F2A0`: the Sleep loop is check-first.
- Family-declaring-page rule (SWE2-DATA, `progress.py` `cite_credits` / `family_rule_inputs`, recomputed today):
  - The VP8 page declares no accepted family.
  - All 5 functions are members of `libvpx VP8 decoder object`, which is declared on another page.
  - On this page the base rule applies: a strictly interior cite credits. Each row's anchors are interior, so the README's "All 5 rowed functions now measure A" is consistent with the rule in force.
  - No family-member citation here depends on a checker row.
- Side effect, recorded for the next package: the `0016F080` row cites 12 function-pointer targets at their entry. They are `001260E7`, `001263AD`, `00126E10`, `00127104`, `00172CE0`, `00172DC0`, `00172F00`, `00173040`, `00173180`, `00173270`, `00173360` and `00173450`, all ≥128 B. They are entry-only on this page, which is where the -3 package's "Missing: 12" comes from. They are not credited and not claimed.
- Limits: body statements only, static evidence. The local draft and OPUS's re-read are not independent review; this record is.

## SWE2-AUDIT-SPEC narrowings

1. `README.md`, paragraph 1. A false provenance sentence: `00713210` is an MSVC ordered-container function (package `opus-the-msvc-ordered-container-runtime-ee-1003-2`) and is not on this page. This package's corrected rows are `0016F080` and `0016F2A0`.
   - Old: `OPUS confirmed a correction at the bytes on a sample (`00713210`: the qword stored is the one at the pointer `00712F60` returns) before applying.`
   - New: `Both corrected rows (`0016F080`, `0016F2A0`) were re-read at the bytes by the non-author review (auditspec-review-opus-the-vp8-codec-interface-and-its-control--ee-1003-2); OPUS's `00713210` spot-check belongs to the MSVC ordered-container package, not to this page.`

No row text, anchor or applier change is required.
