"""S-05: CONTRACT-transform-primitives.md and CONTRACT-transform-workbench-save-restore.md executed as shipped code, stub-free
(OPUS, 2026-09-26).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The whole SHA-asserted image is mapped. NO application stub, no stop
boundary, no bridged import: every IAT slot points at a trap and reaching one fails the case. ALLOWED = the static closures of
the four entries (the graph's call edges); entering any other function fails the case. The four bodies are leaves apart from
the stack-cookie check 00808C40, which runs as shipped.
Entries: the point transform 00398F90 (rcx = in, rdx = out), the composer 00397910 (rcx = a, rdx = b, r8 = out), Save
0036D930 (ecx = count, then the pointers, variadic) and Restore 0036D8E0.
Fixtures: planted data only - the workbench matrix rows M[r] at 022D91B0 + r*0x10, the software vf00 image's w lane
[01EF93FC], and caller buffers.
Cases:
 P1  the point's own w is ignored and replaced by the live load of [01EF93FC]: in.w = 7 gives the same result as in.w = 1;
     [01EF93FC] = 1 adds M[3], = 0 adds nothing (a direction), = 2 adds 2*M[3].
 P2  no perspective divide: all four sums are emitted as they are (w lane included).
 P3  the four deposits: 022D9300 = the input verbatim, 022D91A0 = the sum WITHOUT the translation row, 022D9310 and
     022D8F90 = the result; [rdx] = the result.
 C1  the composer computes out = b x a (out[i][j] = sum_k b[i][k] a[k][j]), not a x b.
 C2  aliasing is safe: out == a and out == b give the same bytes as three distinct buffers.
 C3  the composer writes exactly the 64 bytes of out (outside its own stack frame).
 S1  Save is variadic: 1, 3, 4, 5 and 8 items (4+ pass pointers on the stack) each record every pointer at 02EC0A00 + i*8 and
     its 16 bytes at 02EC0800 + i*16, and depth [022D8F08] = count.
 S2  it is not a stack: save rows A, B; save row C on top; Restore brings back only C, A and B keep their clobbers, and the
     outer frame's saved pointer 0 is overwritten by C's.
 S3  Restore writes each saved row back, zeroes depth, and a second Restore does nothing.
Writes result.json next to this file.
"""
import collections
import csv
import hashlib
import json
import os
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
IMG = 0x120000
STACK, STACK_SZ, RET, BUF, TRAP = 0x70000000, 0x100000, 0x71000000, 0x72000000, 0x74000000
POINT, COMPOSE, SAVE, RESTORE = 0x398F90, 0x397910, 0x36D930, 0x36D8E0
M, VF00W, DEP_IN, DEP_ACC, DEP_RES, DEP_RES2 = 0x22D91B0, 0x1EF93FC, 0x22D9300, 0x22D91A0, 0x22D9310, 0x22D8F90
PTRS, VALS, DEPTH = 0x2EC0A00, 0x2EC0800, 0x22D8F08

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
graph = collections.defaultdict(set)
for row in csv.DictReader(open(os.path.join(GRAPH, "edges.tsv"), encoding="utf-8"), delimiter="\t"):
    if row["callee_external"] != "true":
        graph[int(row["caller"], 16)].add(int(row["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x not in seen:
            seen.add(x)
            st.extend(graph[x])
    return seen


ALLOWED = set().union(*(closure(e) for e in (POINT, COMPOSE, SAVE, RESTORE)))
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(os.path.join(GRAPH, "functions.tsv"), encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec, optsz = struct.unpack_from("<H", raw, pe + 6)[0], struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40
uc = Uc(UC_ARCH_X86, UC_MODE_64)
for v, vs, ra, rs in secs:
    lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
for base, size in ((STACK, STACK_SZ), (RET, 0x1000), (BUF, 0x10000), (TRAP, 0x4000)):
    uc.mem_map(base, size)
uc.mem_write(RET, b"\xF4")
uc.mem_write(TRAP, b"\xC3" * 0x4000)
imp_rva = struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]


def r2o(rva):
    for v, vs, ra, rs in secs:
        if v - IMG <= rva < v - IMG + max(vs, rs):
            return ra + rva - (v - IMG)


TRAPS, dd, k = {}, r2o(imp_rva), 0
while True:
    oft, _, _, name, ft = struct.unpack_from("<IIIII", raw, dd)
    if not (oft or name or ft):
        break
    i = 0
    while struct.unpack_from("<Q", raw, r2o(oft or ft) + 8 * i)[0]:
        uc.mem_write(IMG + ft + 8 * i, struct.pack("<Q", TRAP + 4 * k))
        TRAPS[TRAP + 4 * k] = True
        i += 1
        k += 1
    dd += 20
st = {"bad": [], "faults": []}


def on_code(u, a, n, _):
    if a in TRAPS:
        st["bad"].append("import trap %X" % a)
        u.emu_stop()
    elif a in FSTARTS and a not in ALLOWED:
        st["bad"].append("%08X" % a)
        u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_code)
writes = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: writes.append((a, n)))


def call(entry, rcx=0, rdx=0, r8=0, r9=0, stack=()):
    sp = STACK + STACK_SZ - 0x1000 - 8
    uc.mem_write(sp, struct.pack("<Q", RET))
    for i, v in enumerate(stack):
        uc.mem_write(sp + 0x28 + 8 * i, struct.pack("<Q", v))
    uc.reg_write(UC_X86_REG_RSP, sp)
    for reg, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
        uc.reg_write(reg, v)
    st.update(bad=[], faults=[])
    del writes[:]
    try:
        uc.emu_start(entry, RET, count=1000000)
    except UcError as e:
        st["faults"].append(str(e))
    return uc.reg_read(UC_X86_REG_RIP) == RET and not st["bad"] and not st["faults"]


def wf(a, *v):
    uc.mem_write(a, struct.pack("<%df" % len(v), *v))


def rf(a, n):
    return list(struct.unpack("<%df" % n, bytes(uc.mem_read(a, 4 * n))))


results, cases = {}, {}
ROWS = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [100, 200, 300, 400]]
for rr, row in enumerate(ROWS):
    wf(M + 0x10 * rr, *row)
IN, OUT = BUF, BUF + 0x100
x, y, z = 2.0, 3.0, 5.0
acc = [x * ROWS[0][c] + y * ROWS[1][c] + z * ROWS[2][c] for c in range(4)]


def point(inw, vfw):
    wf(IN, x, y, z, inw)
    wf(VF00W, vfw)
    uc.mem_write(OUT, bytes(16))
    ok = call(POINT, IN, OUT)
    return {"ok": ok, "out": rf(OUT, 4), "dep_in": rf(DEP_IN, 4), "dep_acc": rf(DEP_ACC, 4), "dep_res": rf(DEP_RES, 4),
            "dep_res2": rf(DEP_RES2, 4), "stop": (st["bad"] or st["faults"])[:1]}


p = {"in1_vf1": point(1.0, 1.0), "in7_vf1": point(7.0, 1.0), "in1_vf0": point(1.0, 0.0), "in1_vf2": point(1.0, 2.0)}
results["point"] = p
want = lambda k: [acc[c] + k * ROWS[3][c] for c in range(4)]
cases["P1_w_is_the_live_vf00_load_not_the_point"] = all(v["ok"] for v in p.values()) and p["in7_vf1"]["out"] == p["in1_vf1"]["out"] \
    and p["in1_vf1"]["out"] == want(1) and p["in1_vf0"]["out"] == want(0) and p["in1_vf2"]["out"] == want(2)
cases["P2_no_perspective_divide"] = p["in1_vf1"]["out"][3] == want(1)[3] and p["in1_vf1"]["out"][3] != 1.0
cases["P3_four_deposits"] = p["in7_vf1"]["dep_in"] == [x, y, z, 7.0] and p["in1_vf1"]["dep_acc"] == acc \
    and p["in1_vf1"]["dep_res"] == want(1) and p["in1_vf1"]["dep_res2"] == want(1)

A = [[1, 2, 0, 0], [0, 1, 3, 0], [4, 0, 1, 0], [1, 1, 1, 1]]
Bm = [[2, 0, 1, 0], [1, 3, 0, 0], [0, 1, 2, 0], [5, 6, 7, 1]]
bxa = [[sum(Bm[i][kk] * A[kk][j] for kk in range(4)) for j in range(4)] for i in range(4)]
axb = [[sum(A[i][kk] * Bm[kk][j] for kk in range(4)) for j in range(4)] for i in range(4)]
PA, PB, PO = BUF + 0x1000, BUF + 0x1100, BUF + 0x1200


def compose(dst, a_at, b_at):
    wf(PA, *sum(A, []))
    wf(PB, *sum(Bm, []))
    if dst not in (PA, PB):
        uc.mem_write(dst, bytes(64))
    ok = call(COMPOSE, a_at, b_at, dst)
    outside = sorted({(a, n) for a, n in writes if not (STACK <= a < STACK + STACK_SZ)})
    return ok, rf(dst, 16), outside


okc, res_c, outside_c = compose(PO, PA, PB)
oka, res_a, _ = compose(PA, PA, PB)
okb, res_b, _ = compose(PB, PA, PB)
results["compose"] = {"distinct": res_c, "out_is_a": res_a, "out_is_b": res_b, "writes_outside_stack": [["%X" % a, n] for a, n in outside_c]}
cases["C1_out_is_b_times_a"] = okc and res_c == sum(bxa, []) and res_c != sum(axb, [])
cases["C2_aliasing_is_safe"] = oka and okb and res_a == res_c and res_b == res_c
cases["C3_writes_exactly_the_64_bytes_of_out"] = {a for a, n in outside_c for a in range(a, a + n)} == set(range(PO, PO + 64))

# ---- save / restore ----
ROWBASE = BUF + 0x2000


def rows_init(n):
    for i in range(n):
        uc.mem_write(ROWBASE + 0x10 * i, bytes([0x10 + i]) * 16)


s1 = {}
for n in (1, 3, 4, 5, 8):
    rows_init(8)
    ptrs = [ROWBASE + 0x10 * i for i in range(n)]
    regs = (ptrs + [0, 0, 0])[:3]
    ok = call(SAVE, n, *regs, stack=tuple(ptrs[3:]))
    rec = [struct.unpack("<Q", bytes(uc.mem_read(PTRS + 8 * i, 8)))[0] for i in range(n)]
    vals = [bytes(uc.mem_read(VALS + 16 * i, 16)) for i in range(n)]
    s1[n] = {"ok": ok, "depth": struct.unpack("<I", bytes(uc.mem_read(DEPTH, 4)))[0], "ptrs_ok": rec == ptrs,
             "vals_ok": vals == [bytes([0x10 + i]) * 16 for i in range(n)]}
results["save_variadic"] = s1
cases["S1_save_is_variadic_and_assigns_depth"] = all(v["ok"] and v["depth"] == n and v["ptrs_ok"] and v["vals_ok"] for n, v in s1.items())

rows_init(3)
RA, RB, RC = ROWBASE, ROWBASE + 0x10, ROWBASE + 0x20
call(SAVE, 2, RA, RB)
uc.mem_write(RA, b"\xAA" * 16)
uc.mem_write(RB, b"\xBB" * 16)
call(SAVE, 1, RC)
uc.mem_write(RC, b"\xCC" * 16)
ptr0_after_inner = struct.unpack("<Q", bytes(uc.mem_read(PTRS, 8)))[0]
okr = call(RESTORE)
after = [bytes(uc.mem_read(a, 16)) for a in (RA, RB, RC)]
depth_after = struct.unpack("<I", bytes(uc.mem_read(DEPTH, 4)))[0]
results["not_a_stack"] = {"ptr0_after_inner_save": "%X" % ptr0_after_inner, "rows_after_restore": [b.hex() for b in after], "depth": depth_after}
cases["S2_not_a_stack_inner_save_overwrites_the_outer_frame"] = okr and ptr0_after_inner == RC and after[2] == bytes([0x12]) * 16 \
    and after[0] == b"\xAA" * 16 and after[1] == b"\xBB" * 16 and depth_after == 0

rows_init(3)
call(SAVE, 3, RA, RB, RC)
for a in (RA, RB, RC):
    uc.mem_write(a, b"\xEE" * 16)
ok1 = call(RESTORE)
back = [bytes(uc.mem_read(a, 16)) for a in (RA, RB, RC)]
for a in (RA, RB, RC):
    uc.mem_write(a, b"\x77" * 16)
ok2 = call(RESTORE)
second_writes = [(hex(a), n) for a, n in writes if not (STACK <= a < STACK + STACK_SZ)]
kept = [bytes(uc.mem_read(a, 16)) for a in (RA, RB, RC)]
results["restore"] = {"restored": [b.hex() for b in back], "second_restore_writes": second_writes, "rows_after_second": [b.hex() for b in kept]}
cases["S3_restore_writes_back_zeroes_depth_and_is_idempotent"] = ok1 and ok2 and back == [bytes([0x10 + i]) * 16 for i in range(3)] \
    and kept == [b"\x77" * 16] * 3 and second_writes == [(hex(DEPTH), 4)]

out = {"ok": all(cases.values()), "cases": cases, "allowed_functions": len(ALLOWED), **results}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k2, v2 in cases.items():
    print("%-58s %s" % (k2, "PASS" if v2 else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED", "(allowed %d functions)" % len(ALLOWED))
