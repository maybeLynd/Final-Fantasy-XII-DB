# EO-2-a and EO-2-b closed SUPERSEDED under the runtime rule (FABLE, Claude Opus 5.5, 2026-09-27)

This uses the same rule and shape as [the EO-3 record](../register-triage/eo3-runtime-superseded.md). A runtime
observation is admissible, and a row closes SUPERSEDED when its claim is already tier-1 static. The status names
where the live remainder is carried.

| row | static claim (tier 1) | live remainder | carried by |
|---|---|---|---|
| EO-2-a | The value at `003845F0+0x10` is not an un-rebased offset. It is a rebased 32-bit address, read back sign-extended. `003846F0` rebases every battle_pack directory dword in place with a 32-bit add of the base's low half (`00384780 add dword ptr [rbx], ebp`). `00236C30` reads each entry with `movsxd` (`00236C7B`, `00236C99`, …) and passes it to `AreaData_BindAndRebaseSectionDescriptor`, whose `+0x10` is `mov eax, [rdx+0xC]`, the recorded faulting read. A section at `0x82AD88C0` gives exactly the recorded `rdx = 0xFFFFFFFF82AD88C0`. In `[2 GiB, 4 GiB)` every zero-extended access before it succeeds and this is the first to fail. | Whether the recorded crash came through this route. The fault-shaped value fits, but it is not a causal chain. | not queued; it shares EO-3's discriminator (a pack buffer at or above 2^31), carried by `FABLE-REQ-ASTRA-EO3-PATH-POINTER` |
| EO-2-b | Both faulting sites are one mechanism, so "two sites, one signature" is explained. `001D6E20` reads the raw-path request's heap pointer cut to 32 bits (EO-3, request-queue page section 7). `003845F0+0x10` reads a battle_pack directory entry rebased in 32 bits (EO-2-a). Each is sign-extended on the way back. Both fail only when the allocation lies at or above 2 GiB, so the operator-versus-harness difference is where the allocator places large blocks. | What in a harness launch puts those blocks above 2 GiB. | not queued |

**Control:** `eo2_directory_movsxd.py`, in this directory. It has four checks, including a planted below-2-GiB
negative.

run: eo2_directory_movsxd.py at 6f74a7839 (PASS, FAILS 0), 2026-09-27.

**Not claimed:** that the recorded crashes took this path, that FF12 ships an allocator that can return such a
block, or any repair.
