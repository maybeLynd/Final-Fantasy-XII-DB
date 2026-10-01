#!/usr/bin/env python3
"""call_graph.py - direct call/jump graph over the shipping image, rebuilt from tracked inputs.

Why this exists (2026-09-14, OPUS-REQ-SWE2-FRONTIER-ATLAS-GENERATOR-INPUTS): the two member
generators (ui_atlas.py, wm_family.py) read an untracked cache, tools/rawcalls.json, which recorded
every direct call AND tail-jump site per callee. work/graph/edges.tsv is not a substitute: it
carries call edges only and drops tail jumps (verified: 0037ED70 jmp 0037EB90 absent from
edges.tsv, present in rawcalls). This module derives the same maps from the two tracked sources -
the shipping EXE and functions.tsv - so the generators run on a clean checkout.

call_maps(exe_path, funcs_path) -> (callers, callees, sites)
    callers[callee_entry] -> set of caller function entries
    callees[caller_entry] -> set of callee function entries
    sites[callee_entry]   -> set of instruction addresses (the raw calls/jmps)

An edge is recorded when a direct `call` or `jmp` inside a listed body targets a function entry.
Tail jumps are included deliberately: a tail-jumped callee is the caller's continuation, and
family-closure rules that follow it stay sound.

Since EC-2 (2026-09-25) the maps resolve E9 thunk tails: a listed body whose only direct edge is
`jmp <target>` folds its callers and sites into the target's, so `callers[X]` answers "who calls
X" through 5-byte stubs instead of reporting the stub alone.
"""
import bisect
import collections
import io
import struct

IMAGE_BASE = 0x120000


def _text_section(blob):
    pe = struct.unpack_from("<I", blob, 0x3C)[0]
    nsec = struct.unpack_from("<H", blob, pe + 6)[0]
    opt = struct.unpack_from("<H", blob, pe + 20)[0]
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        if blob[o:o + 8].rstrip(b"\0") == b".text":
            vs, va = struct.unpack_from("<II", blob, o + 8)
            ro = struct.unpack_from("<I", blob, o + 20)[0]
            return va + IMAGE_BASE, vs, ro
    raise ValueError("no .text section")


def call_maps(exe_path, funcs_path):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64

    blob = io.open(exe_path, "rb").read()
    tva, tvs, tro = _text_section(blob)
    entries = []   # (va, size)
    for n, line in enumerate(io.open(funcs_path, encoding="utf-8", errors="replace")):
        if n == 0:
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) < 3 or p[1].startswith(("Unwind@", "Catch_All@")):
            continue
        try:
            entries.append((int(p[0], 16), int(p[2])))
        except ValueError:
            pass
    entries.sort()
    ks = [e for e, _ in entries]
    eset = set(ks)

    def own(s):
        i = bisect.bisect_right(ks, s) - 1
        if i >= 0 and ks[i] <= s < ks[i] + entries[i][1]:
            return ks[i]
        return None

    callers = collections.defaultdict(set)
    callees = collections.defaultdict(set)
    sites = collections.defaultdict(set)
    edge_mnem = collections.defaultdict(set)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    for va, sz in entries:
        off = tro + (va - tva)
        if off < 0 or off + sz > len(blob):
            continue
        for ins in md.disasm(blob[off:off + sz], va):
            if ins.mnemonic not in ("call", "jmp") or not ins.operands:
                continue
            op = ins.operands[0]
            if op.type != 2:   # CS_OP_IMM
                continue
            tgt = op.imm
            if tgt in eset:
                callers[tgt].add(va)
                callees[va].add(tgt)
                sites[tgt].add(ins.address)
                edge_mnem[va].add(ins.mnemonic)
    # E9 thunk hop (EC-2, 2026-09-25; ABSENCE-CLAIM-GATE 2a). A listed body whose only
    # direct-immediate edges are one jmp -> one target is a thunk: whoever calls it calls the
    # target semantically. 0020AC30 measured "0 callers" because every real caller names the
    # stub (001EC660 jmp 0020AC30, called at 0032FD64) and never the leaf. Fold one hop: the
    # thunk's callers and sites join the target's, so "who calls X" sees through the stub.
    # The thunk edge itself stays - the stub does jump to the leaf.
    for va in list(callees):
        if len(callees[va]) == 1 and edge_mnem.get(va) == {"jmp"}:
            tgt = next(iter(callees[va]))
            for c in callers[va]:
                callers[tgt].add(c)
                callees[c].add(tgt)
            sites[tgt] |= sites[va]
    return callers, callees, sites


if __name__ == "__main__":
    import os
    import sys
    import time
    here = os.path.dirname(os.path.abspath(__file__))
    graph = os.path.join(here, "..", "..", "work", "graph")
    exe = os.path.join(here, "..", "..", "work", "exe", "FFXII_TZA.exe")
    t0 = time.time()
    callers, callees, sites = call_maps(exe, os.path.join(graph, "functions.tsv"))
    print("callees %d, callers %d, edges %d, in %.1fs"
          % (len(callers), len(callees), sum(len(v) for v in callees.values()), time.time() - t0))
    # regression control: the tail jump edges.tsv drops must be present
    if 0x0037EB90 in callers.get(0x0037EB90, set()):
        pass
    ok = 0x0037ED70 in callers.get(0x0037EB90, set())
    print("tail-jump control 0037ED70 -> 0037EB90:", "present" if ok else "MISSING")
    # EC-2 thunk control: 0032FD64 calls the stub 001EC660 (jmp 0020AC30). The fold must put
    # the real call site in sites[0020AC30] and the real caller in callers[0020AC30] -
    # pre-fix the only entries were the stub itself.
    ok2 = (0x0032FD64 in sites.get(0x0020AC30, set())
           and callers.get(0x0020AC30, set()) - {0x001EC660})
    print("thunk-hop control 0032FD64 -> 0020AC30:", "present" if ok2 else "MISSING")
    sys.exit(0 if ok and ok2 else 1)
