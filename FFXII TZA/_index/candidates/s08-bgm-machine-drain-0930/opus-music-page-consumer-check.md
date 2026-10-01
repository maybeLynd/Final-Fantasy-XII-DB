# Consumer check: music page §3.3 return wording narrowed (OPUS, 2026-09-30)

- **Request:** `ORACLE-REQ-OPUS-S08-I3-PROVISO-0930`, the music-page half.
- **Corrected claim:** `Database/FFXII TZA/18-Audio/the-music-control-file-and-the-bgm-stream.md` §3.3, "A return of 1
  means the stream submitted or advanced".
- **Correction (static, OPUS-verified on the certified image):**
  - Every return path of `003EADE0` is `mov eax, esi`: `003EAE67`, `003EAEA3`, `003EAECD`, `003EAF14`, `003EAFB4` and
    `003EAFDD`.
  - `esi` is set to 1 only at `003EAE54` and `003EAFA2`. Each is right after a `0032E780` submit (`003EAE4C`,
    `003EAF9A`).
  - So a return of 1 means a submission; the advances 2 → 4 and 4 → 5 return 0.
  - Each submit precedes the next state write: `003EAE63` writes state 2 and `003EAFAD` writes state 8.
- **Executed evidence cited, not adopted as accepted:** SWE2-ORACLE's replay `s08_bgm_drain.py` (16/16). Its review
  is `ORACLE-REQ-AUDITSPEC-S08-BGM-DRAIN-0930`, which is pending.
- **Consumers searched:**
  - the queue contract's I3 (`02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md`). Its proviso is
    held because that file has another party's uncommitted edits;
  - `_index/candidates/s08-runtime-per-invariant-exposure.md`, which names `003EADE0` as I3's exposure;
  - the register: no row restates the "advanced" wording.
- **Regression:** `Database/FFXII TZA/_index/candidates/s08-bgm-machine-drain-0930/s08_bgm_drain.py` (`FAILS 0`).
