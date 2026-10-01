#!/usr/bin/env python3
"""named_registry.py - dump a self-registering, string-keyed registry by reading its insert calls.

The pattern
-----------
Two byte-identical 132-byte functions at `00879570` and `00876C80` are **registry inserts**:

    int Register(Node *self)
    {
        const char *key = self->key_08;
        if (!key) return 0x11;                        /* null key   */
        for (Node *n = g_head; n; n = n->next_10)
            if (!strcmp(n->key_08, key)) return 0x12; /* duplicate  */
        self->next_10 = g_head;
        g_head = self;                                /* push front */
        return 0;
    }

The `strcmp` is inlined as `movzx edx,[rax] / movzx ecx,[rax+r8]` with `r8 = key - n->key_08`, which
is why it does not look like a call to anything.

Each caller is a CRT static initialiser of the shape

    lea  rcx, [rip + …]      ; -> the node, in .data
    call 00879570            ; register it
    lea  rcx, [rip + …]      ; -> the destructor
    jmp  0x808b90            ; atexit

so **the whole registry can be recovered from the image without running the game**: walk the callers,
recover the node from the `lea`, read `node->key_08` and dereference it as a C string.

Why not just walk the list in memory? Because the list head is BSS - it does not exist until the CRT
initialisers have run. The image only contains the *registrations*.
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
EDGES = os.path.join(ROOT, "Database", "Tools", "work", "graph", "edges.tsv")


def load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        nm = d[off:off + 8].rstrip(b"\0").decode("latin1")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((nm, va, vs, ra, rs))
        off += 40
    return d, base, secs


def make_reader(d, base, secs):
    def rd(va, n):
        r = va - base
        for nm, sva, vs, ra, rs in secs:
            if sva <= r < sva + max(vs, rs):
                o = r - sva
                if o >= rs:           # past SizeOfRawData: BSS, not on disk
                    return None
                return d[ra + o: ra + o + n]
        return None
    return rd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("registry", nargs="+", help="VA of the registry-insert function, hex")
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--edges", default=EDGES)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    d, base, secs = load_pe(a.exe)
    rd = make_reader(d, base, secs)

    funcs, eh = {}, set()
    f = io.open(a.funcs, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                funcs[int(p[0], 16)] = int(p[2])
            except ValueError:
                continue
            if len(p) > 8 and "CompilerGeneratedEH" in p[8]:
                eh.add(p[0])

    targets = {}
    for t in a.registry:
        targets[int(t, 16)] = t.upper().replace("0X", "")

    callers = collections.defaultdict(set)
    f = io.open(a.edges, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2 and p[1] in targets.values() and p[0] not in eh:
            callers[p[1]].add(int(p[0], 16))

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    rows = []
    for tva, tname in sorted(targets.items()):
        found, missing = [], 0
        for entry in sorted(callers[tname]):
            size = funcs.get(entry, 0)
            code = rd(entry, size) if size else None
            if code is None:
                missing += 1
                continue
            pend = None
            for i in md.disasm(code, entry):
                if i.mnemonic == "lea" and len(i.operands) == 2:
                    dst, src = i.operands
                    if dst.type == X86_OP_REG and i.reg_name(dst.value.reg) == "rcx" and \
                            src.type == X86_OP_MEM and src.value.mem.base == X86_REG_RIP:
                        pend = i.address + i.size + src.value.mem.disp
                elif i.mnemonic == "call" and i.operands and \
                        i.operands[0].type == X86_OP_IMM and i.operands[0].value.imm == tva:
                    if pend is None:
                        missing += 1
                    else:
                        raw = rd(pend, 0x18)
                        key = None
                        if raw is not None and len(raw) >= 16:
                            kp = struct.unpack_from("<Q", raw, 8)[0]
                            s = rd(kp, 128)
                            if s is not None:
                                key = s.split(b"\0")[0].decode("latin1")
                        if key is None:
                            missing += 1
                        else:
                            vt = struct.unpack_from("<Q", raw, 0)[0]
                            found.append((key, pend, vt, entry))
                    pend = None

        print("registry insert %s  -  %d caller(s), %d name(s) recovered, %d unrecovered"
              % (tname, len(callers[tname]), len(found), missing))
        vts = collections.Counter(v for _, _, v, _ in found)
        print("   distinct type pointers at node+0x00: %d   %s"
              % (len(vts), ", ".join("%08X x%d" % (k, n) for k, n in vts.most_common(6))))
        for key, node, vt, entry in sorted(found):
            print("     %-40s node %08X  type %08X" % (key, node, vt))
            rows.append((tname, key, node, vt, entry))
        print()

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("registry\tname\tnode\ttype_ptr\tinitializer\n")
            for r in rows:
                f.write("%s\t%s\t%08X\t%08X\t%08X\n" % r)
        print("wrote %s  (%d rows)" % (a.out, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
