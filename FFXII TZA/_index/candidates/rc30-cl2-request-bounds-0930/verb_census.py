"""verb_census.py - how many times the shipped script bytecode calls given verb ids (ORACLE, 2026-09-30).
Reads every distinct .ebp under the extract (default D:/FFXII_TZA_extract, or argv[1]). The decode rules are FABLE's
(../rc151617-fable-0930/rc16_regfile_reads.py, after bf1_opcode_histogram.py):
- section at 0x80, tagged 0x8000000B;
- directory at +0x18, stride 0x30, code start at +8;
- 1 byte per opcode below 0x48, 3 bytes (opcode + u16 operand) at or above.
The four verb-call opcodes 0x58, 0x59, 0x5D and 0x5E carry the verb id as their u16 operand (the verb-dispatch page's
table of call opcodes). Usage: python verb_census.py [extract] 0x2006 0x2007 ...
Control: debug_mapjump (0x2026) must be found (the decompiled us corpus prints it 297 times).
"""
import collections, hashlib, struct, sys
from pathlib import Path

EX = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("0x") else Path("D:/FFXII_TZA_extract")
IDS = [int(a, 16) for a in sys.argv[1:] if a.startswith("0x")] or [0x2006, 0x2007]
CALL = {0x58, 0x59, 0x5D, 0x5E}
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]


def scripts():
    seen = set()
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
            if start < len(sec) and end > start:
                yield p, start, sec[start:end]


def main():
    hits = collections.Counter()
    where = collections.defaultdict(list)
    nfiles, nscripts = set(), 0
    for p, start, code in scripts():
        nfiles.add(p)
        nscripts += 1
        i = 0
        while i < len(code):
            op = code[i]
            if op > 0x63:
                break
            if op >= 0x48:
                if op in CALL and i + 3 <= len(code):
                    v = struct.unpack_from("<H", code, i + 1)[0]
                    hits[v] += 1
                    if v in IDS and len(where[v]) < 5:
                        where[v].append("%s@%X+%X" % (p.name, start, i))
                i += 3
            else:
                i += 1
    print("distinct .ebp files with a code section: %d; actor scripts: %d" % (len(nfiles), nscripts))
    ok = hits[0x2026] > 0
    print("%s  control: debug_mapjump 0x2026 calls = %d" % ("PASS" if ok else "FAIL", hits[0x2026]))
    for v in IDS:
        print("verb 0x%04X: %d calls %s" % (v, hits[v], where[v]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
