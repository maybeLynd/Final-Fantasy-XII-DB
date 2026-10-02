# Consumer check: 15-Input contradictions from the reconstruction-readiness map, settled on the pages (OPUS, 2026-10-01)

The cloud readiness map for 15-Input (stream R, `session_014xapq8GYgyFvvwy2xRFAwk`; verified by OPUS and filed in
maybeLynd/Final-Fantasy-XII-RE `docs/readiness/15-input.md`, 3b5fe44) listed nine places where 15-Input pages
contradict each other. This record settles five of them on the pages. OPUS checked each against the shipping image
or the dated register answer before writing. The map is a pointer, not evidence. FABLE is inactive and OPUS edits
non-ASTRA pages under the user's 2026-10-01 authority; FABLE gets a notice.

- **Corrects:**
  - G-C1x: the input-stack page's table row and call tree said `001965E0` "returns 1 when no profile is fully in
    range". It returns 1 unless profile 1 is fully in range, and profiles 2 and 3 are not checked (`r11` fixed at
    `01F80F94`, `001965EB`).
  - G-C2x: the keymap page's row said `00196290` "copies 2 records". It copies three `0x15C` records:
    `01F80130` / `01F8028C` / `01F803E8` to `01DF1738` / `01DF1894` / `01DF19F0`.
  - G-C4x: the input-stack page's section 11 still called `0x01DF15DC` a staging buffer. The poll walks five
    `0x15C` records from `01DF1480` (`00197089`, `001970BB`), so `01DF15DC` and `01DF1738` are live records 1 and 2.
  - G-C8x: two body banners contradicted the status lines. The input-stack page said "PARTIAL." and the R2 page
    said "what the mode looks like on screen is not established"; that is answered as the `FLEEING` label.
  - G-C5x and G-C6x: open lists still carried answered rows. They now point at the dated register answers:
    - the binding contract's section 14 (`DC-2`, `DC-3`, `BP-3`, `BP-4`, `BP-5`, and the bank writers via `AU-4`)
      and section 17 (`UQ-143`, `UQ-144`, and the read surface of group 2, `00197710`);
    - the name-registry contract's section 14 (`DM-3`, `DM-1`);
    - the system page's section 7 bullet (`DM-1`).
- **Affected:** 15-Input/Input-Stack/input-stack-device-channel-and-bindings.md, 15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md, 15-Input/Modal-Toggles/r2-force-fight-toggle.md, 15-Input/Binding-Profiles/CONTRACT-binding-profiles.md, 15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md, 15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the six edited lines and lists | revised-here |
  | the keymap page's validator pseudo-code, which says profile 1 only, three times | agrees (it was already right) |
  | the binding-profile page's `00196290` reading, "for all three bases" | agrees |
  | the binding contract's section 7, which notes that `00196290` reads the profiles out | agrees |
  | SWE2-EC7-38's `00196290` update on the keymap page | agrees |
  | the keymap page's note that the input-stack page's section 11 is stale | agrees (it is now fixed and the note is history) |
  | register rows `DC-2`, `DC-3`, `BP-3`, `BP-4`, `BP-5`, `AU-4`, `UQ-143`, `UQ-144`, `DM-1`, `DM-3` | agrees (the lists now point at them) |
  | the RE repo readiness map `docs/readiness/15-input.md` | routed-to-OPUS's next repo sync (it records these as open contradictions) |

- **Not settled here (left for a later pass):**
  - G-C3x, the sign convention of a two-code axis entry. It needs the axis convention read at the translator.
  - G-C7x, the capability register row. The register is held dirty by another lane.
  - G-C9x, profile numbering 0 vs 1. That is a normalisation note, not a contradiction of fact.
- **Applier:** [`apply_input_fixes.py`](apply_input_fixes.py) runs the image check first. Each edit is a single
  exact replacement. The saved re-run [`apply_input_fixes.out`](apply_input_fixes.out) reads ALREADY with FAILS 0.
- **Regression:** Database/FFXII TZA/_index/candidates/opus-input-readiness-fixes-1001/input_fixes_check.py, verified at 7f773f19f: 16 instructions and 8 rip targets decode as cited, FAILS 0 ([`input_fixes_check.out`](input_fixes_check.out)).
