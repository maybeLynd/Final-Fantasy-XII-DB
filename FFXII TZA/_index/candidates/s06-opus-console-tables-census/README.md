# S-06: the console's authored-code table re-derived from the image (I-6, I-7), and I-7 corrected (OPUS, 2026-09-26)

**Evidence class: STATIC (a census of the SHA-asserted image), not an execution.** `CONTRACT-developer-tuning-console.md`
files I-5..I-7 under **STRUCTURAL** (§16: *"the three tables' strides and extents, and the id-space alignment of
I-5"*). S-06's runtime cell lists them among what is not covered. This census re-derives the two claims that the image
alone can settle.

`census.py` gives `census.json`, byte-identical over two runs (md5 `1dc7f57f2eb760ec3ea5da4e2cb23b51`).

| claim | observed |
|---|---|
| **I-6** | `001CDBF7` is `mov rax, qword ptr [rsi + rdx*8 + 0x1cd6e68]`. With `rsi` = the image base, the table is at `0x1CD6E68 + 0x120000` = **`01DF6E68`, in `.data`**. The literal `01CD6E68` lies in `.rdata`, which is also mapped, so reading it as an address succeeds and does not fault |
| **I-7** | Across 294 entries (stride 16, ids 0–293), `+0x08 == id + 1` for all. **111 code pointers are non-NULL**, and every one points at *three lowercase letters + four digits*. **15 prefixes in 17 id bands.** `nal` is split by `rwr` at 48–49 / 50 / 51, and `dst` has two bands, 129–133 and 227–233. **`dst0104` appears at ids 230 and 232** |

## I-7 corrected in the contract (OPUS's own)

The contract said *"about twenty prefixes occupying contiguous id bands"* and *"`dst0104` at ids 232 and 233"*. The
renderer indexes the table by the id itself (`[base + id*16 + 0x1CD6E68]`, `001CDBDF`–`001CDBF7`), and `+0x08` holds
`id + 1`. So the duplicate sits at ids **230 and 232**, whose `+0x08` fields read 231 and 233; "232 and 233" matched
no convention. The same edit corrects the prefix count and the banding.

## Not covered

- **I-5's label half.** The label table is a runtime context array (`ctx + id*8 + 0x130`). Its 293 names are carried
  from `console-command-names.md`. The dispatcher half (id 294 is refused) is block 291's I-2.
- The renderer `001CD0E0` itself (11,276 bytes, dozens of drawing calls).
- A live game.
