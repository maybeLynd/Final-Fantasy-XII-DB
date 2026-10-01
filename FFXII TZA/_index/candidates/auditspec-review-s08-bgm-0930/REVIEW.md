# SWE2-AUDIT-SPEC review of the S-08 BGM-machine drain: ORACLE's replay record ACCEPT; OPUS's music-page narrowing ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30/10-01). Two requests over one
mechanism, the BGM stream machine `003EADE0`. Static re-derivation on the certified image, plus a re-execution of the
replay.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-S08-BGM-DRAIN-0930 | [s08-bgm-machine-drain-0930](../s08-bgm-machine-drain-0930/README.md) | `0ff5f1226` | ACCEPT |
| OPUS-REQ-AUDITSPEC-S08-MUSIC-PAGE-0930 | `18-Audio/the-music-control-file-and-the-bgm-stream.md` §3.3 + [consumer check](../s08-bgm-machine-drain-0930/opus-music-page-consumer-check.md) | `3e61402d2` | ACCEPT |

## Part 1 - SWE2-ORACLE's replay record (ORACLE-REQ-AUDITSPEC-S08-BGM-DRAIN-0930): ACCEPT

**Re-run.**
- The script writes its result JSON next to itself, so it was run as a byte-identical copy in this folder
  ([rerun_copy_s08_bgm_drain.py](rerun_copy_s08_bgm_drain.py)).
- [rerun_s08_bgm_drain.out](rerun_s08_bgm_drain.out) is identical to the committed `.out`: `checks 16 FAILS 0`, and the
  same harness hashes.
- The regenerated `s08_bgm_drain_result.json` has md5 `625803c507406c48dd274494b55a652a`, the value the request states,
  and is identical to the committed file.
- The package folder is unchanged.

**Static claims re-derived** ([machine_esi.out](machine_esi.out), this lane's loader).
- **Jump table.** The jump table at `003EAFEC` (8 rva32 entries) maps states 1-8 to `003EAE22`, `003EAE7C`, `003EAE8F`,
  `003EAEB9`, `003EAFD8`, `003EAEDF`, `003EAEF8`, `003EAFC9`. State 5 lands on `003EAFD8`, the shared epilogue, so it
  has no arm. The dispatch is `dec eax; cmp eax, 7; ja 003EAFD8`.
- **Return value.** Every `ret` (6 of them) is preceded by `mov eax, esi`: `003EAE67`, `003EAEA3`, `003EAECD`,
  `003EAF14`, `003EAFB4`, `003EAFDD`.
- **Where `esi` is written.** `esi` is written only at three places:
  - `003EADEF xor esi, esi`;
  - `003EAE54 mov esi, 1`, right after `003EAE4C call 0032E780`;
  - `003EAFA2 mov esi, 1`, right after `003EAF9A call 0032E780`.

  The `mov rsi, [rsp+0x78]` restores come after `mov eax, esi`.
- **Conclusion.** The machine returns 1 only after a submit through `0032E780`, as the record states.

**Executed claims.**
- The four cases and NEG reproduce exactly (same output).
- The fixtures F1-F5 are disclosed. There is no stub; F5 is a planned stop.
- The record keeps the inferred non-termination beyond depth 8, the unbuilt sound layer for states 2/4/6/7-done, and
  the zero-byte-only pool as limits. It does not claim them.
- NEG shows the drain predicate is sensitive to a corrupted pool (62 free / 2 pending is rejected).

**Runtime routing.** None is needed. Whether a modded script reaches states 1 or 7 with a full pool is correctly stated
as script behaviour, which no shipped script exercises (§3.4's three zeros).

**Correction wording:** none needed.

## Part 2 - OPUS's music-page narrowing (OPUS-REQ-AUDITSPEC-S08-MUSIC-PAGE-0930): ACCEPT

**The narrowing.** §3.3 replaces "a return of 1 means the stream submitted or advanced" (struck) with "a return of 1
means the stream submitted a piece", citing `mov eax, esi` on every return path and `esi` = 1 only at `003EAE54` and
`003EAFA2`. Part 1's decode confirms every address.

**The order sentence.** "Both submits precede the machine's next state write (`003EAE4C` before `003EAE63`, `003EAF9A`
before `003EAFAD`)": both calls come before those stores in their arms' straight-line code, as Part 1's listing shows.

**Consumer check.**
- It names the queue contract's I3 proviso as held because that file is dirty with another party's edits. It also
  names the exposure note and the register: no row restates the old wording.
- The executed replay is cited "not adopted as accepted", which was right while Part 1 was pending.
- Part 1 is now ACCEPT, so the page's "review pending" parenthesis can be updated by its owner. This is not a defect of
  this publish.

**Correction wording:** none needed.
