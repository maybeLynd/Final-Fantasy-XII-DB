"""Conservative predicate for this tracer's legacy execute-breakpoint setup.

An address match alone is insufficient. This does not claim general x86 debug
exception decoding. Nonstandard/combined causes are rejected, not normalized.
"""


def owned_step(ctx, exception_address, slots):
    if ctx is None or not 1 <= len(slots) <= 4 or len(set(slots)) != len(slots):
        return False
    if ctx.Rip != exception_address or ctx.Rip not in slots:
        return False
    index = slots.index(ctx.Rip)
    # BD/BS/BT are competing causes. BLD=0 or RTM=0 is outside this recipe.
    if ctx.Dr6 & 0xE000 or ctx.Dr6 & 0x10800 != 0x10800:
        return False
    if ctx.Dr6 & 15 != 1 << index or ctx.EFlags & 0x100:
        return False
    expected_dr7 = sum(1 << (i * 2) for i in range(len(slots)))
    # Hardware reports reserved bit10 as 1; the input recipe writes it as 0.
    if ctx.Dr7 & ~0x400 != expected_dr7:
        return False
    return all(getattr(ctx, 'Dr%d' % i) == (slots[i] if i < len(slots) else 0)
               for i in range(4))
