# T2 - PC-1: can anything write the override dwords 01E02804 / 01E02810?

FABLE reader, 2026-09-29. Static only. This extends `_index/candidates/pc1-pointer-store` (2026-09-27), which read a capstone listing bounded by the function list.

## Method
`t2_pc1_override.py` with `tk.py`, run as `python t2_pc1_override.py > t2_pc1_override.out`. Result: FAILS 0.

## Positive controls (all PASS)
- S1: the known reads 00408CC3 and 00408DCB are found by the raw rip sweep.
- S2: the image-base-relative detector finds 002DF7BF `[r15+rbx*8+0x203f000]`.
- S3: the reloc sweep finds the vtable slot 01CB2508 -> 00793EB0.
- S4: the absolute-VA detector finds the imm32 at 001A14E6.
- S5: the lea sweep finds 001AF5EA and 001AF606. The one-level callee check finds 004B9A10's store `004B9A20` when told rcx is the pointer.
- S6: the consumer base `001CA63F lea rbx,[rax+0x3b00]` is found.

## Results
- **S1, rip-relative accesses covering either target: 4, all reads, all in 00408C30.** They are 00408CC3 (01E02804), 00408DCB, 00408E25 and 00408E80. None is an unverified raw hit.
- **S2, image-base-relative operands (any base or index) into 01E02600..01E028FF: 0.**
- **S3, stored pointers.** No DIR64 reloc and no raw qword anywhere in the file points into [01E02604, 01E02814), which is 0x200 below the targets up to their end. The raw dword VA/RVA count is 0 for each target.
- **S4, absolute-VA forms:** one hit, `00471727 movss xmm0,[rdx+rcx*4+0x1e02670]`. It is a read, and its base `rdx = lea 00120000` (`004716F5`), so it actually reads VA 01F22670. No store.
- **S5, every rip-relative lea into 01E02700..01E028FF, each register followed forward:**
  - 001AF5EA -> 01E027F0 and 001AF606 -> 01E027F4 escape into the layout-key registry, at `[rcx+0x3BE8]` and `[rcx+0x40C0]`.
  - 004B1190 takes 01E02828 and 01E02830 about 60 times and passes them in rdx to 004B9A10, 004B9C50, 004B9CA0, 004B9CF0, 004B9D80 and 004B9E60. None of these callees stores through rdx: they read it or overwrite it first. Both addresses are also above the targets.
  - No store through a formed address reaches a target, and none is indexed.
- **S6, what happens to the two escaped pointers:**
  - Displacements 0x3BE8 and 0x40C0 occur only in 001AF470's own stores. The other 0x40C0 hit, `00645A3A`, belongs to another object.
  - The registry's one consumer base is `001CA63F`, rbx = `001B1C00()+0x3B00`.
  - It loads slot `+0xE8` (`001CAA15`) and stores `001CAA23 mov dword [rcx], eax`. It loads `+0x5C0` (`001CBF75`) and stores `001CBF83 mov dword [rcx], eax`.
  - Both are 4-byte stores at displacement 0, so they write 01E027F0..F3 and 01E027F4..F7. They are the layout keys mPauseMenuOffsetY and PauseMenuLineOffset, matching `layout-key-slots.tsv`.
- **Direct stores to the neighbours cover only their own bytes:** 01E027F8 and 01E027FC (dword), 01E02801 (byte, `001D47F1 sete`), 01E02814 and 01E0281C (dword). None covers 04..07 or 10..13.

## Conclusion and limits
**No instruction and no stored or formed pointer in the shipped image can write 01E02804 or 01E02810.**
- The only pointers formed near them are the two registry entries. Their sole consumer writes 4 bytes at displacement 0, which stops 0x10 and 0x1C bytes short of the targets.
- So both dwords stay FFFFFFFF, and the loader's override and second-path branches are dead in shipped code. The watch request is not needed for any in-image route.

Limits:
- A bulk copy (memcpy/memset) whose base lies more than 0x200 below and is formed by arithmetic is not excluded. `bulkcalls.tsv` lists 1,622 bulk sites, and no resolved destination falls in 01E02000..01E02900.
- Writes from outside the process image are out of scope.
