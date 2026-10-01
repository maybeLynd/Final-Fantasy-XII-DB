#!/usr/bin/env python3
"""walk_name_registry.py - read the two input name registries out of a RUNNING game.

Why
---
`CONTRACT-input-name-registry.md` section 13 is empty: nothing in it had ever been observed live.
Its section 14 names two unresolved items, and **one walk settles both**:

  1. **the real registration order** -- it is CRT static-initialiser order, which no static read
     can recover, and which `INTEGRATION` parity needs;
  2. **whether 143 and 97 are complete** -- they are the complete sets of *static* registrations
     found in the image, and a name registered at runtime from data would not appear. A live
     chain longer than the static set is exactly that evidence.

The list is built by push-front, so **walking from the head yields REVERSE registration order**.
This tool reverses it back and says so, rather than quietly presenting one as the other.

What it checks rather than assumes
----------------------------------
* every `next` is either zero or a node the walk has not already seen -- a cycle is reported, not
  looped on;
* the chain length is bounded, so a corrupt `next` cannot hang the tool;
* each recovered name is compared against the statically recovered set, and **names present live
  but absent statically are reported separately from the reverse** -- they answer different
  questions.

**Read-only.** It opens the process for READ and never requests write access.
"""
import argparse
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP
import runtime_poke as PK

REGISTRIES = [
    ("PInputChannelSemantic", 0x02EB9D80, 0x00879570),
    ("PInputKeySemantic", 0x02EB83B8, 0x00876C80),
]
NODE_NAME = 0x08
NODE_NEXT = 0x10
NODE_VALUE = 0x18
MAX_NODES = 4096


def cstring(rw, va, limit=64):
    b = rw.read(va, limit)
    if not b:
        return None
    z = b.find(b"\0")
    if z < 0:
        return None
    try:
        return b[:z].decode("ascii")
    except UnicodeDecodeError:
        return None


def walk(rw, head_va):
    """-> (nodes, problem). nodes are in LIST order, i.e. reverse registration order."""
    head = rw.q(head_va)
    if head is None:
        return [], "the head at %08X is unreadable" % head_va
    out, seen = [], set()
    n = head
    while n:
        if n in seen:
            return out, "cycle: node %016X is already in the chain" % n
        if len(out) >= MAX_NODES:
            return out, "chain exceeded %d nodes; stopping" % MAX_NODES
        seen.add(n)
        name_va = rw.q(n + NODE_NAME)
        name = cstring(rw, name_va) if name_va else None
        v = rw.read(n + NODE_VALUE, 4)
        value = struct.unpack("<i", v)[0] if v else None
        out.append((n, name_va or 0, name, value))
        nxt = rw.q(n + NODE_NEXT)
        if nxt is None:
            return out, "node %016X's next is unreadable" % n
        n = nxt
    return out, None


def load_static(path):
    """-> {registry_entry: [names]} from the recovered TSV."""
    by = {}
    with io.open(path, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        ir, iname = head.index("registry"), head.index("name")
        for line in f:
            c = line.rstrip("\n").split("\t")
            if len(c) <= max(ir, iname):
                continue
            by.setdefault(c[ir].upper(), []).append(c[iname])
    return by


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--static", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "..", "FFXII TZA", "15-Input", "Input-Name-Registry",
        "input-name-registry.tsv"))
    ap.add_argument("--order-out", help="write the recovered REGISTRATION order here, one per line")
    a = ap.parse_args()

    hits = RP.find_process(a.process)
    if not hits:
        sys.stderr.write("walk_name_registry: no %r process running\n" % a.process)
        return 2
    pid = hits[0][0]
    rw = PK.RW(pid)
    static = {}
    if os.path.isfile(a.static):
        static = load_static(a.static)
        print("static set: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(static.items())))
    else:
        print("static TSV not found at %s -- comparison skipped" % a.static)
    print()

    rc = 0
    for label, head_va, insert_va in REGISTRIES:
        head = rw.q(head_va)
        nodes, problem = walk(rw, head_va)
        print("%s   head [%08X] = %016X" % (label, head_va, head or 0))
        print("  chain length            : %d" % len(nodes))
        if problem:
            print("  PROBLEM                 : %s" % problem)
            rc = 1
        named = [n for n in nodes if n[2]]
        print("  nodes with a readable name: %d of %d" % (len(named), len(nodes)))

        live = [n[2] for n in named]
        s = static.get("%08X" % insert_va, [])
        if s:
            ls, ss = set(live), set(s)
            print("  static set              : %d" % len(s))
            print("  live only               : %d  %s"
                  % (len(ls - ss), sorted(ls - ss)[:8]))
            print("  static only             : %d  %s"
                  % (len(ss - ls), sorted(ss - ls)[:8]))

        # The list is push-front, so registration order is the chain reversed.
        order = list(reversed(named))
        print("  FIRST registered         : %s"
              % ", ".join("%s=%d" % (n[2], n[3]) for n in order[:6]))
        print("  LAST registered          : %s"
              % ", ".join("%s=%d" % (n[2], n[3]) for n in order[-6:]))
        if a.order_out:
            p = "%s.%s.txt" % (a.order_out, label)
            io.open(p, "w", encoding="utf-8", newline=chr(10)).write(
                "".join("%016X\t%s\t%d\n" % (n[0], n[2], n[3]) for n in order))
            print("  wrote                   : %s" % p)
        print()
    rw.close()
    return rc


if __name__ == "__main__":
    sys.exit(main())
