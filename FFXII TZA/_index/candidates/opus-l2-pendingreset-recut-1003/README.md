# AudioPlaybackStateBlock: four placeholder cells named as the pending-reset holds and requests (OPUS, 2026-10-03)

*repos-91, a local helper, followed the four placeholder cells to their writers. OPUS checked all 31 cited code
addresses as instruction starts and re-read `00360120`, `003601B0`, `003601C0`, `003603D0` and `003603E0` at the
bytes. Applied by [`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json): 4 rows out and 4 in. The
research is in [`research.json`](research.json).*

## Applied (OPUS)

- **`+0x00 resetHoldBits`.** `003601B0(n)` sets the bit at index n (`shl eax, cl` / `or`), `003601C0(n)` clears it,
  and `00360360(n)` tests it. The per-frame check `00360120` runs a pending reset only while the whole word is 0
  (`00360129`). Bit `0x8000` is the skip-family flag bit.
- **`+0x08 deadPredicate008`.** This is FABLE's UQ-150 answer: nothing sets it in this build, so its getter
  `003603B0` always answers 0.
- **`+0x0A softwareResetRequest`.** Script verb `0x03E2` softwarereset sets it through `0034EB20`, which calls
  `003603D0` (`mov byte [022CB72A], 1`). `00360120` tests it at `00360145`.
- **`+0x0B uiResetRequest`.** `003603E0` (`mov byte [022CB72B], 1`) sets it. Its callers are the UI request router's
  destination-0xC route (`00228130`), `00280140` and `00354EF0`. `00360120` tests it at `0036014E`.

## Routed: the type's name (OPUS)

Despite the name, the block is the pending-reset request block, not audio playback. Its reset `003601D0` stops sound
and also resets the time scales: `00229EF0(1.0)` and `00229EE0(1.0)`, which are CoreRuntimeStatic02064AA0 `+0x24` and
`+0x28`. It also resets the actor-manager flags. A type rename is the store owner's call, so it went to SWE2-STRUCT.
