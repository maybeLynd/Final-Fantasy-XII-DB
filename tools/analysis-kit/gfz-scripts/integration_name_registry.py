#!/usr/bin/env python3
"""integration_name_registry.py - the reconstruction against the RUNNING GAME'S OWN LIST.

The difference from `diff_name_registry.py`
-------------------------------------------
That harness compares the reconstruction against the shipped bytes under emulation, over an order
**it chooses**. Charter section 21's `INTEGRATION` asks for something stricter: *the reconstruction
exercised through the caller the game actually uses, with inputs the game actually supplies.*

Here the caller is the CRT static-initialiser sequence, which cannot be replayed -- but **its
result can be read**, and its order can be recovered from that result, because the list is
push-front and therefore preserves the order it was built in. So:

    inputs   the real nodes, read out of the live process at their real addresses
    order    the real registration order, recovered by reversing the live chain
    oracle   THE GAME'S OWN LIST, walked from the head in the same process

The reconstruction is handed the first two and its output is compared against the third. Nothing
is synthesised and nothing is shuffled.

What a pass does and does not mean
----------------------------------
A pass says the reconstruction, given the game's nodes in the game's order, builds **the same
list the game built** -- node for node, from the head. It does **not** say the reconstruction
would be *called* the way the game calls it: the initialiser sequence is still not executed here,
and a reconstruction that inserted correctly but was never invoked would look identical.

**Read-only on the game.**
"""
import argparse
import os
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP
import runtime_poke as PK
import walk_name_registry as W


def build_regions(rw, nodes):
    """One region covering every node, one covering every name string. Bytes come from the LIVE
    process, so the reconstruction is given exactly what the game is holding."""
    node_vas = [n[0] for n in nodes]
    name_vas = [n[1] for n in nodes if n[1]]
    regions = []
    for label, vas, pad in (("nodes", node_vas, 0x20), ("names", name_vas, 0x40)):
        lo, hi = min(vas), max(vas) + pad
        size = hi - lo
        blob = rw.read(lo, size)
        if blob is None:
            raise SystemExit("could not read the %s region %016X..%016X" % (label, lo, hi))
        regions.append((lo, blob))
        print("  region %-6s %016X .. %016X  (%d bytes)" % (label, lo, hi, size))
    return regions


def write_regions(path, regions):
    with open(path, "wb") as f:
        f.write(struct.pack("<I", len(regions)))
        for va, blob in regions:
            f.write(struct.pack("<QI", va, len(blob)))
            f.write(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--driver", required=True)
    ap.add_argument("--registry", default="PInputChannelSemantic",
                    choices=[r[0] for r in W.REGISTRIES])
    a = ap.parse_args()

    hits = RP.find_process(a.process)
    if not hits:
        sys.stderr.write("integration_name_registry: no %r process running\n" % a.process)
        return 2
    pid = hits[0][0]
    rw = PK.RW(pid)

    label, head_va, _insert = next(r for r in W.REGISTRIES if r[0] == a.registry)
    nodes, problem = W.walk(rw, head_va)
    if problem:
        print("REFUSING: the live chain is not clean -- %s" % problem)
        return 3
    print("%s: the game's own list is %d nodes, head [%08X] = %016X"
          % (label, len(nodes), head_va, nodes[0][0] if nodes else 0))

    # push-front: the chain is reverse registration order
    order = list(reversed(nodes))
    regions = build_regions(rw, nodes)

    tmp = tempfile.mkdtemp(prefix="nrint")
    rp = os.path.join(tmp, "regions.bin")
    cp = os.path.join(tmp, "cases.txt")
    write_regions(rp, regions)
    with open(cp, "w") as f:
        for n in order:
            f.write("%X\n" % n[0])

    out = subprocess.run([a.driver, rp, cp], capture_output=True, text=True)
    if out.returncode != 0:
        sys.stderr.write(out.stderr)
        raise SystemExit("driver failed (rc=%d)" % out.returncode)

    codes, got_list = [], None
    for line in out.stdout.splitlines():
        line = line.strip()
        if line.startswith("LIST"):
            got_list = [int(x, 16) for x in line.split()[1:]]
        elif line:
            codes.append(int(line))

    print()
    print("cases (the game's own registration order) : %d" % len(order))
    from collections import Counter
    cc = Counter(codes)
    print("return codes                              : %s"
          % ", ".join("%s x%d" % ({0: "OK", 0x11: "NULL_KEY", 0x12: "DUPLICATE"}.get(k, hex(k)), v)
                      for k, v in sorted(cc.items())))
    if got_list is None:
        print("the driver printed no LIST line -- no comparison is possible")
        return 1

    want = [n[0] for n in nodes]                   # the GAME'S list, head first
    print("the game's list                           : %d nodes" % len(want))
    print("the reconstruction's list                 : %d nodes" % len(got_list))
    if len(got_list) != len(want):
        print("LENGTH MISMATCH")
        return 1
    bad = [i for i in range(len(want)) if want[i] != got_list[i]]
    print("nodes differing, position by position     : %d of %d" % (len(bad), len(want)))
    for i in bad[:8]:
        print("   position %3d  game %016X  reconstruction %016X" % (i, want[i], got_list[i]))
    print()
    if bad or cc.get(0, 0) != len(order):
        print("RESULT: the reconstruction does NOT rebuild the game's own list")
        return 1
    print("RESULT: given the GAME'S OWN nodes in the GAME'S OWN order, the reconstruction")
    print("        builds the same list the game built -- %d nodes, same order." % len(want))
    print("It does NOT show the reconstruction would be CALLED as the game calls it: the CRT")
    print("initialiser sequence is not executed here, only its recovered order and its result.")
    rw.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
