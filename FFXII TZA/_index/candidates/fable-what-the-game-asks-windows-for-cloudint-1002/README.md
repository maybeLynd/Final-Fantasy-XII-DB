# Interior citations, cloud-drafted: what-the-game-asks-windows-for.md's entry-cited functions (FABLE, 2026-10-02)

The page named 9 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01EX8gVEnmWxiC6Ukpc8Fzck, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 9 staged with 45 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `00159CA0`: content verified (IAT slots resolve to VerSetConditionMask, VerifyVersionInfoW, GetFullPathNameW, LocalAlloc, LocalFree; `00159DC4` jbe gives up unless the second result is below the length); the compare callee, new to the page, is now cited by its site +0x161 (`00159E01`)
- `0015AE60`: a null allocation result branches past the free to the close call (`0015AFA8` je to `0015B033`), a path the text did not state
- `0015B820`: two callees new to the page are now cited by their sites (+0x35 at `0015B855`, +0x24C at `0015BA6C`); 'dir' and 'join' named purposes the listing does not show, so the operand is called d; a null d skips the call (`0015BA77` je); the 0 return calls the 0x7E setter only when the getter returns 0 (`0015BAF7` jne), now stated as such
- `0015BB30`: content verified (`0015BB9E` jne on eax 1, `0015BBDB` null test after the getter call at `0015BBD5`, `0015BC0B` je 0x7E falls through to the last call); two callees new to the page are now cited by their sites (+0x91 at `0015BBC1`, +0xB5 at `0015BBE5`)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
