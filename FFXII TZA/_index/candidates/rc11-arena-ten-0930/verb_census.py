"""verb_census.py - shipped bytecode calls of the three script verbs whose argument reaches the arena selection push
0036C1D0 (ORACLE, 2026-09-30, RC-11). Authored data. Reads only.

The verbs (scriptvm-verb-table.tsv; the handler bodies are read in the README):
  0x0395 setexpandvoicememory  -> 0034D080 -> tail 003E9AA0, whose push 003E9AC2 selects arg1 if >= 0, else 6
  0x2003 debug_tkmalloc        -> 0050DA30 (pops two, abs64 table slot 0x1e04da0) -> tail 0050D8F0
  0x2004 debug_tkmalloc_4      -> 0050D8F0 (table slot 0x1e04dc0), push 0050D93F selects a popped int
  0x2008 debug_tkmallochandle  -> 0050DBD0 (pops two, table slot 0x1e04e40) -> tail 0050DAD0
  0x2009 debug_tkmallochandle_9 -> 0050DAD0 (table slot 0x1e04e60), push 0050DB1F selects a popped int
A verb call is opcode 0x58 CALL, 0x59 CALLACT, 0x5D CALLPOPA or 0x5E CALLACTPOPA with the 16-bit call id as its
operand (worldactor-scriptvm-interpreter.md; the verb-dispatch page's opcode table). Decode rules as FABLE's
ov16_opcode_histogram.py: code section at 0x80 tagged 0x8000000B, directory at +0x18, stride 0x30, start at +8; one
byte below opcode 0x48, three bytes at or above. Every distinct .ebp (md5) under the extract is read.

Checks (exit 1 on failure):
  C1 POSITIVE CONTROL: skipexec (0x0539) is called; FABLE's decompiled US corpus shows 19 uses in 19 scripts;
  C3 the total of call opcodes 0x58/0x59/0x5D/0x5E equals FABLE's full histogram
     (../fable-astra-live-facts-0930/ov16_opcode_histogram.out: 2,904,432 + 16,009 + 22,331,684 + 542,112 = 25,794,237);
  C2 POSITIVE CONTROL: setexpandvoicememory (0x0395) is found (the decompiled US corpus shows two calls, byu_z9900 and
     rrp_z9900, both `setexpandvoicememory(-1, 0x100000)`).
Prints, per verb, the call count, the files and the two instructions before each call (the pushed arguments).
"""
import collections, hashlib, os, struct, sys
from pathlib import Path
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x0395: "setexpandvoicememory", 0x2003: "debug_tkmalloc", 0x2004: "debug_tkmalloc_4",
        0x2008: "debug_tkmallochandle", 0x2009: "debug_tkmallochandle_9",
        0x0539: "skipexec (control)"}
CALLS = (0x58, 0x59, 0x5D, 0x5E)


def main():
    seen = set()
    hits = collections.defaultdict(list)
    ncalls = 0
    for p in sorted(EX.rglob("*.ebp")):
        b = p.read_bytes()
        h = hashlib.md5(b).digest()
        if h in seen:
            continue
        seen.add(h)
        if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B:
            continue
        sec = b[0x80:0x80 + U32(b, 0x84)]
        diroff = U32(sec, 0x18)
        cnt = U32(sec, diroff)
        if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
            continue
        starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
        bounds = sorted(set(starts) | {diroff, len(sec)})
        for start in starts:
            end = min((x for x in bounds if x > start), default=len(sec))
            if start >= len(sec) or end <= start:
                continue
            code = sec[start:end]
            i, prev = 0, []
            while i < len(code):
                op = code[i]
                if op > 0x63:
                    break
                arg = struct.unpack_from("<H", code, i + 1)[0] if op >= 0x48 and i + 3 <= len(code) else None
                if op in CALLS:
                    ncalls += 1
                    if arg in WANT:
                        hits[arg].append((os.path.relpath(str(p), str(EX)).replace("\\", "/"),
                                          ["%02X:%s" % (o, "" if a is None else "%04X" % a) for o, a in prev[-2:]]))
                prev.append((op, arg))
                i += 3 if op >= 0x48 else 1
    fails = 0
    ok1 = len(hits[0x0539]) >= 19
    ok2 = len(hits[0x0395]) >= 2
    print("distinct .ebp %d, verb calls decoded %d" % (len(seen), ncalls))
    print("%s  C1 skipexec 0x0539 calls: %d (US decompiled corpus: 19)" % ("PASS" if ok1 else "FAIL", len(hits[0x0539])))
    print("%s  C2 setexpandvoicememory 0x0395 calls: %d (US decompiled corpus: 2)" % ("PASS" if ok2 else "FAIL",
                                                                                      len(hits[0x0395])))
    ok3 = ncalls == 25794237
    print("%s  C3 call opcodes decoded %d (histogram 25,794,237)" % ("PASS" if ok3 else "FAIL", ncalls))
    fails = (not ok1) + (not ok2) + (not ok3)
    for v in (0x0395, 0x2003, 0x2004, 0x2008, 0x2009):
        print("0x%04X %s: %d calls in %d distinct files" % (v, WANT[v], len(hits[v]), len({f for f, _ in hits[v]})))
        args = collections.Counter(tuple(a) for _f, a in hits[v])
        for a, n in args.most_common():
            print("    preceding instructions %s  x%d" % (" ".join(a), n))
        for f, a in hits[v][:30]:
            print("    %s" % f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
