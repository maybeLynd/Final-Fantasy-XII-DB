# EXP-190 — `1D0390`/`202880` deep-init execution record

Identity: `SWE2-ORACLE-UNIT-INSTALL-EXEC`
Harness: `evidence/deep-init-1D0390-exec/check.py` (Unicorn native replay; synthetic fixtures + disclosed stubs — MODEL-PROVEN/NATIVE-REPLAY)
Result: **268/268, stable ×3**, zero faults. Both functions run real inside `t1ccb20`/`t1d50d0-null` (the `1CCB20` singleton ctor path).

## Structure

`1CCB20` (the `1D50D0` singleton ctor body) calls `1D0390(obj)` then `202880(obj+0xA98)` — the "name/dictionary object" initializer.

### `1D0390` — name-table object initializer

- `1EA3C0(obj+8)` — std::map-style init (**scripted boundary `s1ea3c0`**: zeroes `d[+0x28]` count + `q[+0x30]` slots = the empty-map contract, returns 0).
- `1EAC30(obj+8,0)` → `d[obj+0xFA]=0`; `2F79E0` → `xmmword q[0x22BE930]` = const `0xD0F9E0` (verified `00ED00EA00E700F1`).
- `d[obj+0xAE4]=0x46464F` ("OFF"), blob strings `+0xB04..+0xBE4`, immediates `"Torrent"`@+0xBA4, `"Inferno"`@+0xBE4.
- `ebx==0` (success) → `b[+0xA68]=1`, ~40-entry string-pointer table `+0x138..+0xA50` (`+0x138=0x8FD5E0`, `+0x140=0x1CEB638` empty-string, `+0x818=0x8FD5F0` …), zero `+0xA6C/+0xA88/+0xA90`.
- **22-iteration loop** (`d[0x8FCE00 + row*4]`, all 22 nonzero in image): `1CD0E0(obj, strid, &buf)` (**stubbed `s1cd0e0`**, empty → fallback blob `0x8FF950` "None con…") → `1EA1E0(obj+8, key)` **real** — map insert; `d[+0xA90]++` → 0x16.
- `1EA1E0`/`1EA6C0`/`1C2720`/`1C19A0`/`1C26B0`/`674A00`/`584730` — **the whole hash-map grow+rehash chain ran real**: count 0→0x16, slot array bump-alloc'd, per-insert rehash (`17D260`/`19C580`=_aligned_malloc → `s19c580` allocx bump; `584730`→`19C570`=_aligned_free → `s19c570` nop). Same-key inserts append (multiset semantics — count reaches 22).
- Tail: `1EAC40(obj+8,0)` → `b[+0xF2]=0`; `1EAD20(obj+8,-0.06,-0.614)` → `f[+0xF8]/+0xFC`, `b[+0xF1]=1`; `1EAC50(obj+8,0x16)` → `d[+0xF4]=22`; CRT locale trio `615BC0`/`624670`/`624660`/`616700` (**stubbed — `gs:[0x58]` TLS**; `624660` real = `rax=rcx+0x18C0` → `q[+0xA80]=fakeloc+0x18C0` verified).
- Failure path (`ebx!=0`): `1EAC40` + `b[+0xA68]=0` only.

### `202880` — typed-field release

`2001F0(obj+0xA98)` jump-table destroy on `d[field]`∈[0..5] — the ctor leaves `d=6` (out of range → early-ret, no free) → then `d=6`, `q+8=0` re-stamp. Verified.

## New disclosed boundaries

`s1ea3c0` (map-init: zero header, ret 0), `s1cd0e0` (format fetcher → empty → fallback key), `s19c580` (`_aligned_malloc` → bump-alloc), `s19c570` (`_aligned_free` → nop), `s615bc0`/`s624670`/`s616700` (TLS locale machinery — `s624670` returns planted `fakeloc`), `qpczero` retkey on `s5cc930` (QPC → xmm0=0.0). `861EBA` memcpy gets real on_code semantics (like `861EC0` memset).

## Harness additions

- `0x861EBA` memcpy hook (records `memcpys`).
- `initmap`/`fakeloc`/`qpczero` retkeys.
- REAL trace tags: `z1d0390`, `z202880`, `z2001f0`, `z1ea1e0`, `z1ea6c0`, `z17d260`, `z2f79e0`, `z1eac30/40/50`, `z1ead20`, `z1c19a0`, `z1c26b0`, `z1c2720`, `z674a00`, `z584730`.
