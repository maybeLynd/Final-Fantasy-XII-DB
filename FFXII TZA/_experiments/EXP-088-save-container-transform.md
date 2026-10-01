---
experiment: EXP-088
title: Save container transform under isolated original execution
contract: ../19-Save-Load-Settings/CONTRACT-save-container-transform.md
method: B
live_game: false
tool: evidence/save-container-transform/check.py
# Transcribed from this record's own prose header by OPUS 2026-09-16; status and dates
# are SWE2-ORACLE's to state and are deliberately left absent.
---
# EXP-088 — save container transform execution

**Date:** 2026-09-14 · **Worker:** SWE2-ORACLE · **Method:** B (isolated original-code execution, Unicorn)
**Subject:** writer `00866200`, reader `008666B0`, reader inner `00865D90`, decrypt `00865840`, encrypt `00865AE0`
**Contract:** `Database/FFXII TZA/19-Save-Load-Settings/CONTRACT-save-container-transform.md`
**Board task:** `SWE2-ORACLE-SAVE-CONTAINER-EXEC`
**Evidence:** `evidence/save-container-transform/` (`check.py`, `result.json`, `bodies.json`)

## Result

**46/46 cases pass; 9/9 byte-level mutants detected.**

This is the experiment the contract's §13 names verbatim: *"a `SWE2-ORACLE`-shaped experiment, not
an `ASTRA` one"*. It was the last contract in the nothing-executed bucket — its §4 admitted *"no
malformed save was constructed and no failure path was executed."* All five entry bodies now execute
at canonical VAs against synthetic fixtures, along with every bounded real callee: the deflate
wrapper `0087AF40` and the **entire shipped zlib deflate subtree under it** (`0087C9F0` deflateInit2_,
`0087BD60` deflate, `0087C6C0` deflateEnd + internals — real code, real mallocs), the inflate wrapper
`0080C5A0`/`0080C5C0` and its zlib subtree, the vector helpers `00866150`/`00865720`, the CRT
locked-IO wrapper `0019C580`, the `__security_check_cookie` `00808C40`, and the memcpy/memset import
thunks `00861EBA`/`00861EC0` resolving through their real IAT slots.

## Executed confirmations

- **Writer order, end to end** (`w-write`): `GetTempPathW` → build `sav_tmp`/`sav_org` paths →
  `SetFileAttributesW` ×3 (target, tmp, org) → `_wfopen_s(tmp, "wb")` → `rand` →
  branchless `abs` → signed `%32` → store to `[02EB3868]` and header+8 → `fwrite` the 12-byte
  `SAFH`+declared+rot header → `_aligned_malloc` ×2 → deflate level 9 → `00865AE0` →
  `fwrite` ciphertext → `fclose` → verify-`_wfopen(target, "rb")` → `CopyFileW(tmp → target)`.
  Round-trip: a python-built `ref_container` fed to the reader reproduces the payload exactly, and
  the writer's own output feeds the reader back to the same bytes (`w-roundtrip`).
- **The key derivation executed, not just read**: `CryptCreateHash(CALG_MD5=0x8003)` → `strncpy`
  the 32-char title → two `memcpy`s producing `rotl(title, n)` → `B[31]=0` → inline `strlen` →
  `CryptHashData` measured at **len=31** with the rotated bytes logged verbatim
  (`"ANTASY XII THE ZODIAC AGEFINAL "` for n=7) → `CryptDeriveKey(CALG_RC4=0x6801, flags=0x800000)`
  → `CryptEncrypt`. The contract's "31 is computed, not written down" claim is confirmed in
  execution — mutant `m-strlen-null` (`B[31]=1`) pushes the hashed length past 31.
- **`abs(rand()) % 32` measured**: `rand=INT_MIN` → n=0 (contract's §5 pass-1 claim executed);
  `rand=-3` → n=3; `rand=31` → n=31 accepted; header+8 mirrors `[02EB3868]` every time.
- **Encrypt/decrypt units share one signature**: `rcx`=dst, `rdx`=cap→len in/out dword,
  `r8`=src, `r9d`=src len. The chunk loop is **1000 bytes** with `Final = (chunk < 0x3E8)` — and the
  compare is against the *literal* `0x3E8`, so a multiple-of-1000 input never sets Final
  (`enc-chunk-2000` → `[final=0, final=0]`); 1500 → `[0,1]`; 999 → `[1]`. CryptEncrypt's
  `dwBufLen` arg is the *remaining dst capacity*, decremented per chunk.
- **CryptoAPI failure paths**: first `CryptAcquireContextW` failing → retry with
  `flags=8 (CRYPT_NEWKEYSET)` then success; both failing → return 0 before any hashing;
  `CryptHashData`/`CryptDeriveKey` failures → 0 with the hash still destroyed.
- **Reader admission gates, all executed in order**: `size<=4` and bad-magic do **not** bare-return —
  they push the **raw file bytes into the output vector** (a fallback fill the contract does not
  describe); `size<=12` **truncates** the vector to empty; `n>31` unsigned-rejects **before**
  `[02EB3868]` is stored but **still truncates** the vector (contract's "untouched" intuition was
  wrong on that detail); `declared>1MiB` rejects **after** the n store (`g_n=7` persists);
  `declared=0`, `declared≠actual`, and truncated ciphertext all reach decrypt+inflate and die at
  the exact-length `jne` or positive `jle`.
- **Reader mode split**: mode 0 + open-fail returns a `0x210`-byte result object `{0, mode, path}`
  (not NULL — "no file" is distinguishable from "reject"); mode 1 + open-fail returns 0.
- **Writer mode≠0** frees the context and truncates the global vector — no `rand`, no file activity.
- **`rcx=0` writer faults at VA 4** reading the mode field (measured).
- **Ciphertext is not plain zlib** (`w-cipher-not-plain` control): bytes after the 12-byte header
  differ from `zlib.compress(payload, 9)` — the RC4 layer is really applied.
- **The unmapped-vector-helper detail**: `00866150` calls `memmove(dst, 0, 0)` on empty vectors —
  real CRT semantics never dereference at n=0 (the harness initially faulted on it; fixed to match).

## Findings

- **F1 — the writer's return value cannot express failure.** eax=0 on the full commit **and** on
  the deflate-overflow abort: a 64-byte incompressible payload overflows the payload-sized dst,
  the wrapper returns nonzero, and the writer skips encrypt+commit — the 12-byte header-only
  `sav_tmp` is **abandoned in the temp dir, not removed**, and the caller sees the same `0` as a
  successful save. Only the missing target file distinguishes the two outcomes.
- **F2 — the sav_org backup protocol is keyed on `02B40E04`.** With the flag clear, an existing
  target is overwritten by a single `CopyFileW(tmp→target)` after the verify-open. With the flag
  set, the writer first `CopyFileW(target→sav_org)`, then commits — and clears the flag on the way.
- **F3 — `Final` edge in the chunk loop.** `Final` is `chunk < 0x3E8`, not "is this the last
  chunk" — a 2000-byte input emits two `Final=0` calls and none with `Final=1`. Harmless for RC4
  (a stream cipher), but it means the shipped code never asserts CryptoAPI finalization semantics
  on exact multiples.
- **F4 — reader fills to the DECLARED size.** With the exact-length check nop'd out (`m-exact`),
  `declared = actual+1` is accepted and the vector ends up 1025 bytes — the push loop iterates the
  declared count over the decompress output.
- **F5 — three different reader failure shapes are observable.** raw-fill (size≤4, bad magic) vs
  truncate (size≤12, n>31) vs store-then-reject (declared>1MiB). Any reconstruction that treats the
  gates as uniform bare-returns will mismatch.

## Mutation campaign (9/9 detected)

| mutant | site | effect measured |
|---|---|---|
| `cmp byte[rsi],0x53` → `0x54` | 008667C4 | valid file rejected at magic byte 0 (raw-fill fires instead of payload) |
| `cmp eax,0x1F` → `0x3F` | 00866807 | n=0x20 admitted — n stored to `02EB3868`, CryptDecrypt runs with the wrong rotation |
| `cmp edx,0x100000` → `0x10` | 00866819 | declared 0x400 rejected by the shrunken bound |
| exact-length `jne` → nops | 0086686D | declared=actual+1 accepted; vector filled to 1025 (declared, not actual) |
| positive `jle` → `jmp` | 00866871 | every file fails the positive check |
| `mov ecx,0x3E8` → `0x3E7` | 00865C67 | chunk bound 999, but the Final test still compares `0x3E8` — first 999-byte chunk is already "final", tail silently dropped |
| `mov byte[rbp-0x12],0` → `1` | 00865C04 | B[31] not NUL'd → strlen runs past 31 → `CryptHashData` length changes |
| `and eax,0x8000001F` → `0x1F` | 008663D1 | rand=-35: signed %32 would give -3; without the sign bit the header gets +3 |
| `jne` → `je` (acquire retry) | 00865B57 | a successful first `CryptAcquireContextW` is treated as failure → NEWKEYSET retry always runs |

## Deviations and limits (disclosed)

- **CryptoAPI is a faithful HLE model, not Windows' advapi32.** `CryptDeriveKey` is modeled as
  "RC4 KSA over the MD5 digest" and `CryptEncrypt`/`CryptDecrypt` keep keystream state per key
  handle across calls. Every *boundary* fact — call order, algorithm constants, flags, hash length
  and bytes, chunking, capacity bookkeeping, failure returns — is measured from shipped code. The
  **derived key bytes themselves are not proven against real advapi32**: if Microsoft's RC4
  derivation differs, real ciphertext will differ. §16 bounds INTEGRATION at the ADVAPI32 import
  exactly for this reason; closing it needs a real `.sav` cross-check or live advapi32 — flagged
  in the OPUS request.
- **File I/O is a synthetic filesystem** (path→bytearray map with handle semantics); `rand` is
  scripted per case. The temp-path commit protocol (`sav_tmp`, `sav_org`, verify-open) is measured
  call-for-call, but real filesystem edge cases are out of scope.
- **`__security_check_cookie` returns** because the planted cookie matches — the gs-failure tail is
  not exercised.
- The zlib subtree executes as shipped bytes (mallocs/deflate internals observable in the trace);
  full-library parity is not claimed — only what these callers touch.
- `NATIVE-REPLAY`/live claims are not made — this is isolated original-code evidence under
  synthetic fixtures.

## Kill set

Every mutant diverged on observable state: gate admission, stored globals, CryptHashData length,
chunk finals, or produced ciphertext. The suite is sensitive to: all four magic bytes' compare
sites (byte-0 tested), both reader bounds, the exact-length and positive checks, the chunk-size
constant (and its separation from the Final literal), the B[31] NUL store, the `%32` sign bit, and
the acquire-retry branch.
