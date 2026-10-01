# rc16_regfile_reads.py - RC-16 (authored data): does shipped script code read one of the eight per-actor registers
# (I0..I3 / F0..F3 at ActorStorageRecord +0x64..+0x83) that the same script never writes?
# The register opcodes (bf1-opcode-semantics): writes POPI0..3 0x36..0x39, POPF0..3 0x3A..0x3D; reads PUSHI0..3 0x3E..0x41,
# PUSHF0..3 0x42..0x45. Decode rules as bf1_opcode_histogram.py (section at 0x80 tag 0x8000000B, directory at +0x18,
# stride 0x30, start at +8; 1 byte below 0x48, 3 bytes at or above). One directory entry = one actor script's code.
# FABLE's T5 (../fable-astra-live-facts-0930/t5_regfile_reuse.md) found no native store into the range between a record's
# release and reuse, so a register a script reads but never writes holds whatever the record held before: zero after a
# fresh pool allocation (the allocation memset), or the previous occupant's value in a reused record.
# Also reported: reads that come, in linear bytecode order, before the script's first write of that register.
# Control: total register opcodes must equal the histogram's counts for 0x36..0x45 (printed).
import collections, hashlib, struct, sys
from pathlib import Path
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
W = {0x36 + k: ("I%d" % k if k < 4 else "F%d" % (k - 4)) for k in range(8)}
R = {0x3E + k: ("I%d" % k if k < 4 else "F%d" % (k - 4)) for k in range(8)}
seen = set(); scripts = 0; ops = collections.Counter()
never_written = collections.Counter()        # register -> scripts that read it and never write it
read_first = collections.Counter()           # register -> scripts whose first touch (linear) is a read
examples = collections.defaultdict(list)
readers = collections.Counter()
for p in sorted(EX.rglob("*.ebp")):
    b = p.read_bytes(); h = hashlib.md5(b).digest()
    if h in seen: continue
    seen.add(h)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        scripts += 1; code = sec[start:end]; i = 0
        wr, rd, first = set(), set(), {}
        while i < len(code):
            op = code[i]
            if op > 0x63: break
            if op in W:
                ops[op] += 1; wr.add(W[op]); first.setdefault(W[op], "w")
            elif op in R:
                ops[op] += 1; rd.add(R[op]); first.setdefault(R[op], "r")
            i += 3 if op >= 0x48 else 1
        for r in rd:
            readers[r] += 1
            if r not in wr:
                never_written[r] += 1
                if len(examples[r]) < 3:
                    examples[r].append("%s@%X" % (p.name, start))
        for r, k in first.items():
            if k == "r" and r in wr:
                read_first[r] += 1
print("distinct .ebp %d, scripts %d" % (len(seen), scripts))
print("register opcodes (control vs the histogram):", {hex(k): v for k, v in sorted(ops.items())})
print("register | scripts reading it | read but never written by the same script | first linear touch is a read (also written)")
for r in ["I0", "I1", "I2", "I3", "F0", "F1", "F2", "F3"]:
    print("  %s  %6d  %6d  %6d   e.g. %s" % (r, readers[r], never_written[r], read_first[r], ", ".join(examples[r])))
