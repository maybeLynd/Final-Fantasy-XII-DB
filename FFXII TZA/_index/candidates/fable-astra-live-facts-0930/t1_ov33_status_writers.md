# T1 - OV-33 (i): who writes the read-layer status dword 0215EFF4

FABLE reader, 2026-09-29. Image SHA256 73461D08…21F8, image base 0x120000 included. Static only.

## Question
Do all writes to `0215EFF4` go through the pointer cell `01F82CC0`? The known stores are -1 at `001D6DD4` (archive route), -1 at `001D6FF4` (loose route) and the result at `001D6D7C`.

## Method
- `tk.py`: shared helpers. It sweeps the raw `.text` bytes for rip-relative and image-base-relative disp32 values, so it is not bounded by the function list. Every hit is checked by decoding on the owning function's instruction boundary. It also scans DIR64 relocations, raw qwords and absolute-VA imm32/disp32 values.
- `t1_status_writers.py`, run as `python t1_status_writers.py > t1_status_writers.out`. Result: FAILS 0.

## Positive controls (all PASS, see the .out file)
- A: the six known rip references to 0215EFF4 are found: the lea at 002DF719, 002DF75F, 002DF808 and 002DF838, and the reads at 0046DFE7 and 0046E0E0.
- B: the image-base-relative detector finds `002DF7BF [r15+rbx*8+0x203f000]`, which is in the same window as the target.
- C: the reloc sweep finds the vtable slot 01CB2508 -> 00793EB0.
- D: all four references to the cell 01F82CC0 are found.
- H: the absolute-VA detector finds the imm32 at `001A14E6 mov edx, 0x2000000`.

## Results
- (a) **Direct writes: none.** No rip-relative, image-base-relative or absolute-VA store covers 0215EFF4. No stored pointer (reloc or raw qword) targets 0215EE00..0215EFFF.
- (b) **The cell 01F82CC0 has exactly four references.**
  - It is loaded once, at `001D6D70`. The only store through that register is `001D6D7C mov dword [rax], ecx`: 4 bytes at displacement 0. The register is not copied, and the function returns.
  - The cell is cleared at `001D6D7E`.
  - It is stored at `001D6DCD` and `001D6FED`. The -1 stores `001D6DD4` and `001D6FF4` go through the same rax.
- (c) **The only values the cell can hold are 0215EFF4 and 0.**
  - The storers take the pointer from a stack argument. 001D6D90 takes it from the 5th argument, caller `[rsp+0x20]`. 001D6FB0 takes it from the 6th, caller `[rsp+0x28]`.
  - Their only callers are four raw E8 sites: 002DF735, 002DF777, 002DF821 and 002DF853. At each one the argument slot holds `lea 0215EFF4`.
  - Neither storer has its address taken, and neither address is stored anywhere. The completion 001D6D70 is address-taken only as the job callback, at 001D6DEF and 001D700F.
  - The cell is BSS, so its initial value is 0. No image-base-relative or absolute form of it exists.
- **Bases below the target (section G).** I read each loop by hand:
  - `002DEB40` is bounded by r8 = 0215EFD0, so its last byte is 0215EFCF.
  - `002DE360` runs 16 fixed entries from 0215EF52 and ends at 0215EFCF.
  - `002DE420` is a fixed 0xF0-byte copy from 0215E734.
  - **`002DE800`, selector-2 arm (`002DE8E1`..`002DEA44`), is NOT bounded.**

## The one remaining route (exact gap)
`002DE800` copies a polyline into the global descriptor 0215E710.
- Each point takes 16 bytes. Point i starts at `0215E734 + 16*i`: loops at `002DE940` and `002DE9CA`, plus one extra point at `002DEA18`.
- The point count n = dword `[src+0x14]` is not checked against any limit.
- The vertex area holds 128 points before the next global, 0215EF38. So **n >= 128 overflows it, and n >= 140 writes a float x-coordinate onto 0215EFF4**. For n > 140 the store is at `002DE946`; for n = 140 it is at `002DEA18`.
- Sources that reach selector 2:
  - The callers 00332C40 and 003B99D0 build a 0x40-byte stack copy of template 022CBAB0. It has count 0 (`00362F70` zeroes it), and its selector is forced to 4 (`00332E30`..`00332E38`; `003B9B6C`..`003B9B74`). So those paths do not copy.
  - The route that stays open is `003631B0` -> `003638B0` -> `002DEFA0` (`003639E5`). It passes an authored SP1 map-sound record, `[022CBAF0] + u16 offset`. Its selector (`+9`) and count (`+0x14`) come from the map-ctrl pack data. The map-ctrl page says "class-2 point count (1 x2265)" but gives no maximum.
- **What remains is a data question, not a code question: is any shipped SP1 class-2 record's count >= 140?** Even a count >= 128 already corrupts globals 0215EF38 and above. I did not scan the corpus.

## Conclusion and limits
**In code, the writer set is exactly {001D6DD4, 001D6FF4 (both -1, through rax before the cell is used), 001D6D7C (the result, through the cell)}. The cell can only hold 0215EFF4 or 0. The one exception is the unbounded polyline copy in 002DE800, which reaches 0215EFF4 only if an authored record's count is >= 140.**

Limits:
- The tracking is within a function and in linear order.
- A pointer to this BSS page built by arithmetic from an unrelated base is not excluded. The sweeps rule out every lea, reloc, image-base-relative and absolute form, but not arithmetic.
- Writes from outside the image are out of scope.

Side note, not checked: the spatial-audio page says the builder `00221940` reads vertices at `+0x28`. 002DE800 writes x at `+0x24`, and the builder reads `[r8-4]` after `lea r8,[rbx+0x28]`, which is consistent with +0x24.
