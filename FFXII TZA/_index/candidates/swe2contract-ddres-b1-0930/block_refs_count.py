"""block_refs_count.py - regression for the console-tunes page's corrected count (SWE2-CONTRACT, 2026-09-30).
Rejects the old "25 functions reference / read the block": re-runs rip_refs over [02CB7FD0, 02CB843C) and requires
28 referencing functions, 24 accessing it and the four lea-only functions 00162410, 001BC9D0, 00607F00, 008AB7C0.
Positive control: rip_refs.py's own store-to-02064ACC control must pass. Static. Reads only."""
import collections, sys
import rip_refs


def main():
    hits = rip_refs.scan(0x02064ACC, 0x02CB843C)
    ctl = any(a == 0x0022A1A7 and k == "w" for _, a, k, _, _, t in hits if t == 0x02064ACC)
    fn = collections.defaultdict(set)
    for f, a, k, m, ops, t in hits:
        if 0x02CB7FD0 <= t < 0x02CB843C:
            fn[f].add(k)
    acc = sorted(f for f, k in fn.items() if k - {"lea"})
    lea = sorted(f for f, k in fn.items() if k == {"lea"})
    ok = ctl and len(fn) == 28 and len(acc) == 24 and lea == [0x00162410, 0x001BC9D0, 0x00607F00, 0x008AB7C0]
    print("%s  control=%s referencing=%d accessing=%d lea-only=%s (old claim 25 rejected: %s)" % (
        "PASS" if ok else "FAIL", ctl, len(fn), len(acc), ["%08X" % x for x in lea], 25 not in (len(fn), len(acc))))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
