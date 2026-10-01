"""The largest-unclassified page's "BI 17" item (SWE2-DATA 2026-09-30), static: do the second byte-opcode dispatcher
003CD2C0's eight arms map to the same operations as 003CCF20's?

Both dispatchers index an 8-entry table of image-relative dwords (003CD0F6 [r12 + rax*4 + 0x2AD298], 003CD3ED
[rbp + rax*4 + 0x2AD570]; the base register holds the image base 0x120000). For each opcode 1..8 the script walks
the arm linearly from its target to the next arm start (at most 60 instructions, or a ret) and lists the direct calls.
  D1 both tables decode to 8 targets inside their own dispatcher's body;
  D2 per opcode, the 0050xxxx operation each arm calls;
  C1 control: 003CCF20's arms reproduce the page's own §16 table (1 0050AC20, 2 00506B40, 3 005080A0, 4 0050A100,
     5 00509BB0, 6 00507490, 7 00508C90, 8 00507120).
And the "BI 18" item, what reaches 003CCF20's tail region (003CD239..003CD261):
  T1 the outer loop walks binding entries (rbp; next at +0x20, 003CD266..003CD270), skips an entry whose byte +1 is
     below 0x80 (003CCF60), resolves its handle +8 into rsi (raw when +1 & 0x3F is clear, else through 0036B130;
     003CCF8A..003CCFA7) and runs 003CD840 on it when non-null (003CCFBE);
  T2 its operation list (rbx = [rbp+0x28], next at +0x38) is walked, every arm returning to 003CD229; opcodes 4 and 8
     overwrite rsi with their own resolved handle (003CD16D, 003CD1FC);
  T3 when the list ends (003CD233 falls through) or is empty (003CCFCA), 003CD239 tests rsi: non-null runs the tail,
     which resolves the entry's +0x10 the same way (003CD23E..003CD24D) and calls 003D2B60 with it and word +2
     (003CD252..003CD261).
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis  # noqa

BASE = 0x120000
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def arms(fn, table):
    body = dis(fn)
    lo, hi = body[0].address, body[-1].address
    tg = [BASE + struct.unpack_from("<I", d, off(table + 4 * i))[0] for i in range(8)]
    by = {x.address: i for i, x in enumerate(body)}
    out = {}
    for op, t in enumerate(tg, 1):
        calls = []
        i = by.get(t)
        while i is not None and i < len(body):
            x = body[i]
            if x.address != t and x.address in tg:
                break
            if x.mnemonic == "call" and re.fullmatch(r"0x[0-9a-f]+", x.op_str):
                calls.append(int(x.op_str, 16))
            if x.mnemonic == "ret" or (i - by[t]) > 60:
                break
            i += 1
        out[op] = calls
    return tg, lo, hi, out


EXPECT = {1: 0x0050AC20, 2: 0x00506B40, 3: 0x005080A0, 4: 0x0050A100, 5: 0x00509BB0, 6: 0x00507490, 7: 0x00508C90,
          8: 0x00507120}
res = {}
for name, fn, table in (("003CCF20", 0x003CCF20, 0x003CD298), ("003CD2C0", 0x003CD2C0, 0x003CD570)):
    tg, lo, hi, out = arms(fn, table)
    check("D1 %s: 8 table targets inside the body" % name, all(lo <= t <= hi for t in tg),
          " ".join("%08X" % t for t in tg))
    ops = {}
    for op, calls in out.items():
        o50 = [c for c in calls if 0x00500000 <= c < 0x00510000]
        ops[op] = o50
        print("   %s op %d -> %s" % (name, op, " ".join("%08X" % c for c in calls)))
    res[name] = ops
check("C1 control: 003CCF20's arms reproduce the page's section 16 table",
      all(EXPECT[op] in res["003CCF20"][op] for op in EXPECT))
same = [op for op in EXPECT if EXPECT[op] in res["003CD2C0"][op]]
print("   003CD2C0 arms calling the same operation as 003CCF20's for the same opcode: %s" % same)
check("D2 003CD2C0's opcode map decoded (every arm calls exactly one 0050xxxx operation or none)",
      all(len(v) <= 1 for v in res["003CD2C0"].values()))
t = {x.address: x for x in dis(0x003CCF20)}
check("T1 outer entry walk: +1 >= 0x80 gate, handle +8 into rsi, 003CD840 on it",
      t[0x003CCF60].op_str == "byte ptr [rbp + 1], 0x80" and t[0x003CCF9C].op_str == "rsi, qword ptr [rbp + 8]"
      and t[0x003CCFA7].op_str == "rsi, rax" and t[0x003CCFBE].op_str == "0x3cd840"
      and t[0x003CD266].op_str == "rax, qword ptr [rbp + 0x20]" and t[0x003CD270].op_str == "0x3ccf60")
check("T2 op list [rbp+0x28] / +0x38; opcodes 4 and 8 overwrite rsi",
      t[0x003CCFC3].op_str == "rbx, qword ptr [rbp + 0x28]" and t[0x003CD229].op_str == "rax, qword ptr [rbx + 0x38]"
      and t[0x003CD16D].op_str == "rsi, rax" and t[0x003CD1FC].op_str == "rsi, rax")
check("T3 tail gated on rsi after the list (003CD239); resolves +0x10, calls 003D2B60 with word +2",
      t[0x003CCFCA].op_str == "0x3cd239" and t[0x003CD239].op_str == "rsi, rsi" and t[0x003CD23C].op_str == "0x3cd266"
      and t[0x003CD24A].op_str == "ecx, dword ptr [rbp + 0x10]" and t[0x003CD252].op_str == "r8d, word ptr [rbp + 2]"
      and t[0x003CD261].op_str == "0x3d2b60")
print("RESULT same-operation opcodes %d of 8: %s" % (len(same), same))
print("FAILS %d" % FAILS)
