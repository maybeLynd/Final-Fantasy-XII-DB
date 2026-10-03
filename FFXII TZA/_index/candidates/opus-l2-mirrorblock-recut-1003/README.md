# MirrorBlockBytes02099DA0: seven placeholder bytes named from their script verbs and readers (OPUS, 2026-10-03)

*repos-91, a local helper, followed each byte from the script verbs that set it to the code that reads it. OPUS
checked all 100 cited code addresses as instruction starts and re-read the `0026AB50`, `0025D950`, `002671C0` and
`00263FB0` bodies at the bytes. Applied by [`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json):
7 rows out and 7 in. The research is in [`research.json`](research.json).*

## Applied (OPUS)

- **`+0x00 lockCharMotionOnce`.** Verb `0x011C` lock_charmotion_once sets it. The actor-resource load arm `0025AFC0`
  then skips `002E4000` and `002E3E20` once and clears it.
- **`+0x01 primaryBattleSimVeto`.** `002671C0` answers 1 only when `002671E1 cmp byte [02099DA1], 0` is equal.
- **`+0x03 charNearFadeActive`.** `0025D950` sets it to 1, then keeps it only when the map-flags qword has bit
  `0x400000000` set (`0025D964`/`0025D973`) and `002E15F0()` is 0. While `+0x04` is set, it publishes `+0x05`
  instead (`0025D99E`, `0025D9A7`, `0025D9AD`). The getter `00263FB0` reads it sign-extended. Its one caller,
  `002E6330` at `002E6363`, goes on to `00264EA0` only when it reads 1.
- **`+0x04 forceCharNearFade` and `+0x05 forcedCharNearFadeValue`.** Verb `0x0552` set_force_char_nearfade sets them
  and `0x0553` clears them, both through `0026AB50`: `cl` goes to `+0x04` and `dl` to `+0x05`.
- **`+0x06 bonePhysicsDenyMask`.** `00267D40(index, on)` sets or clears one bit (`bts`/`btr`). The wind is held calm
  while the mask is non-zero.
- **`+0x07 enter2509A0Armed`.** A balance flag for the `002509A0`/`00250960` pair. Only the mechanism is claimed.

## Corrections made in OPUS's review

The helper's `+0x03` row said the getter's value is used "to set context +0x151 bit 7". `retool callers 00263FB0`
finds one direct caller, `002E6330`, which compares the value with 1. There are no rip or data references. The
clause was replaced by what that caller does. Bits are written as values.

## Routed (OPUS)

`06-Movement-And-Navigation/heading-speed-to-position-delta.md` line 450 names `00263FB0` the "0209BDA3 flag-byte
getter", but the getter reads `02099DA3`. The fix goes to that page's owner.
