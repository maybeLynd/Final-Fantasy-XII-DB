# OV-35: the indexed source's metadata is the manager's `.mot` directory (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-35, `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` §8):** "Authored
selector/metadata creation and lifetime, permitted caller indices and mode meanings."

[`metadata.py`](metadata.py) runs S, K and M: FAILS 0 ([output](metadata.out)). Static, joined to two audited pages.

- **The selector (S)** returns the resource-set index that the manager's resource-set load recorded for the group (the
  dword at `022C6D28 + 4g`), or −1 while its flag byte is clear.
- **Mode meanings (K).** The mapper turns that index into a package namespace and base id:

  | group `g` | namespace | base id |
  |---|---|---|
  | 1–3 | 8 | index × 4 (`{ebp, mot, snd, vpc}`) |
  | 4 | 1 | index + `0x6B` |
  | any other | 5 | index × 3 (`{ebp, mot, fpk}`) |

  These are the namespaces [the PKFL page](../../../26-PKFL-Package-Container/Container/pkfl-package-container.md) lists.
- **The metadata (M).** The offset and length providers:
  - read the pointer at `022C6E70 + 8g`;
  - refuse `g` > 3;
  - return −1 until that directory's first byte is non-zero (the `PKFL` magic has loaded);
  - otherwise read slot `i`'s `{offset, size}` pair.
- **Creation and lifetime.** [The voice-pack page](../../../18-Audio/the-voice-pack-slots-and-the-voice-verbs.md) §2.2 gives
  them: `022C6E70` is the per-manager `.mot` directory table. `0032F430` allocates it at boot, four `0x88`-byte buffers.
  The manager's resource-set load (`0032FCA0`) requests the `.mot` PKFL directory into it, and every later load rewrites
  it. Nothing frees it.
- **Permitted indices:**
  - `g` is 0–3. Group 4 has no metadata, since both providers return −1, so a group-4 producer fails as "inactive metadata".
  - `i` is 0–15. Every shipped `.mot` has 16 slots (the PKFL page's audited corpus of 10,314 packages), matching the
    owner array's 16 records per group.

run: metadata.py at ced7c61fd, FAILS 0.
