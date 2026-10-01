> and mover `0036A2A0`. Membership makes a block eligible for those moves, subject to mask `0x04`.
> This supersedes the earlier statement that no such tree walker had been read. The release front `003AB7C0` sends
> a tagged value to the handle release `00369800` and an untagged one to `003697F0`
> (`003AB7C5`–`003AB7DE`). The resource-storage allocator `003AB8B0` pushes selection (6, 6) and allocates
> **kind 0 as a raw block** (`0036A100`, full pointer) or **kind 1 as a handle** (`0036B160` → `0036C4B0`, a 32-bit
> value, `003AB8D5`–`003AB8E1`). One width detail for reconstruction: the storage append `0051EF90` passes
> `memcpy` a destination built in 32 bits — `low32(resolved base) + used` (`0051EFED`–`0051EFF8`) — so it is one
> more below-4 GiB condition on that storage's blocks; the growth copy `0051EEB0` uses full width.
>
> **The free routine and the 64 KiB buckets** ([lifetime evidence](../../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md) §19; FABLE re-read `00369860`,
> `0036ACE0`, `0036B5F0` 2026-09-12). `00369860(payload)` is gated three ways before it reclaims anything: a header
> (`payload − 0x40`) without the `FF12` word takes a diagnostic path ending in an imported `exit(1)`; a **non-zero
> header word `+0x3E`** takes the "MCB broken" diagnostic and the same exit (`00369A80`); header byte `+0x14` mask 1
> clear is reported as already free and returns (`00369ABE`). Only then does it clear mask 1, debit the payload
> length from the counters indexed by header `+0x16` and `+0x17` (`00369B05`–`00369B1B`), clear metadata including
> `+0x3E` (`00369B4F`), coalesce with free physical neighbours or insert through the bucket searches. Those searches
> (`0036ACE0` / `0036AE00`) give the record's two initializer arrays their role: a block's **bucket is
> `(header − first header +0x10) >> 16`**, the qword array `+0x28` holds a representative free header per 64 KiB
