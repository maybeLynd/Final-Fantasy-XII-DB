# F family: the undispositioned frontier by body shape (OPUS, 2026-09-30)

The goal gate reports the requirement family **F = 7,045 unmet**: 6,250 "frontier (no disposition)" and 795 UC-1
frontier bodies, which are frontier by ruling. This record is a planning census for **SWE2-EC7, the disposition
owner**. It declares no family and explains no function.

## Census (OPUS, `f_shapes.py`, output `f_shapes.out`, rows `f_shapes.tsv`)

Over the 6,250, bucketed by body shape (first match wins):

| bucket | functions | shape |
|---|---:|---|
| larger | 3,304 | body > 64 bytes |
| small | 2,016 | body <= 64 bytes, not below |
| tiny-leaf | 653 | ends in `ret`, body <= 16 bytes |
| forwarder | 262 | ends in `jmp`, no call, body <= 24 bytes |
| getter-leaf | 8 | a load from `[rcx+..]` into the return register, then `ret` |
| setter-leaf | 6 | a store to `[rcx+..]`, then `ret` |
| jmp-thunk | 1 | starts with `jmp` |

## For EC7 (OPUS)

About 930 bodies (tiny leaves, forwarders, getters, setters, one thunk) are shapes whose bytes are close to their
whole behaviour. The existing "trivial accessors" family (EC7 C2, `302bf18a6`) admits by selector. This census lists
which bodies of those shapes are still outside every family, as candidates for EC7's selectors to test. Size alone
is not a disposition: each must meet the family's own bar.
