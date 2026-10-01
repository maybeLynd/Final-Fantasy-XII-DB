# DM-2 — keymap control code 27 is the 17th pad button, and only a DirectInput pad has it

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `dm2_code27.py` (5 checks, FAILS 0).

**Answer.** Code 27 is pad slot 16, the 17th, at the top of the 11–27 pad band. Only a DirectInput pad fills it, from
its 17th DirectInput button (`rgbButtons[16]`). On an XInput or Steam pad it is always 0. No channel name carries 27
because the registry's pad names stop at slot 15.

- **D1 — the band is 17 codes.** Three readers bound `code − 11` to 17 slots:
  - the raw-state getter `0079D670` reads controller `+0x43C + (code − 11)`;
  - the button-node binder `00799F40` points a node at that same byte;
  - both accept `code − 11 ≤ 0x10`;
  - the any-pad test `0079E650` tests `+0x30 + (code − 11)` for `code − 11 < 0x11`.
- **D2 — the constructor zeroes all 17.** The controller base constructor `00792940` zeroes the raw bytes
  `+0x43C`..`+0x44C`.
- **D3 — XInput and Steam fill 16.** The XInput poll `007A2140` and the Steam poll `007A1CD0` each store exactly the
  16 bytes `+0x43C`..`+0x44B`, never `+0x44C`. XInput's order is PlayStation order:
  - X/A/B/Y as Square, Cross, Circle, Triangle;
  - LB, RB, LT > 0, RT > 0;
  - Back, Start, the two thumb clicks;
  - the d-pad as Up, Right, Down, Left.

  That is exactly the sixteen names on channels 11–26.
- **D4 — DirectInput fills 17.** The DirectInput poll `007A1A50` reads a `0x110`-byte `DIJOYSTATE2` and copies
  `rgbButtons[0..16] >> 7` into `+0x43C`.. (loop `edx < 0x11`). It then overwrites slot 8 from button 13 and the
  d-pad slots 12–15 from the POV hat, and for one product reorders the four face buttons. Slot 16 stays button 16.
- **D5 — nothing else writes it.** Across `00780000`–`007C0000` the only store at displacement `0x44C` is the
  constructor's. The only loop that stores through a pointer into the raw array is the DirectInput poll's.

**With DM-2's other bands** (codes 1–3 are the three mouse buttons, 2026-09-12; 11–26 the sixteen pad buttons;
123/125/130–152 the scancodes named 2026-09-18), every code the row asked about is now identified.

**The row's remaining residue** is why `-` `=` `]` `\` `,` `.` `/` and both Alts are on the bind blacklist while `[`
`;` `'` are not. Nothing in the image separates the two groups except the blacklist itself. That makes it an intent
question, and it goes to OPUS as [review package 5](../nas-package-5-2026-09-27/README.md).
