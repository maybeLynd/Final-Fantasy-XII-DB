"""S-04: execute the class validator 00322C50 (BattleEncodedId_IsValidForClass) for all 32 classes over the SHIPPED battle_pack
tables, bound by shipped code, at every class's range edges; and class 1's re-dispatch for every id family (OPUS, 2026-09-25,
block 328).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session) supplies the image, the IAT
traps and the named bridges. No application stub and no stop boundary. N05 ran this validator stub-free over synthetic states;
this runs it over the authored counts.
THE TABLES ARE THE SHIPPED ONES: battle_pack.bin (us) is copied raw; 003846F0(&[0208E680], blob, 0) relocates the directory
(00238850's first call); then EVERY binding call 00236C30 makes is made again with the same arguments, read from its own
instruction stream (lea rcx,[slot] / movsxd rdx,[dir+off] / call): 36 x 003845F0, 2 x 003846F0, and the inner binders
00238160 and 00238660. Not made: 00238880 (the gambit table, slot 02EBF0D8) and the tail of 00237FC0 after its first
003845F0 (both allocate from engine heap 6, which halts unbuilt), and 003847B0 if it does too (recorded below). Slots no
battle_pack call binds (02EBF120, 02EBF150, 02EBF0D0, ...) stay at the image's null, and their classes are recorded as empty.
The codec base stays at the image's 0 (block 324).
Writes result.json next to this file.
"""
import hashlib
import json
import os
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn.x86_const import UC_X86_REG_RAX

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
PACK = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "repos-2d", "vbf", "ps2data", "image", "ff12", "test_battle", "us",
                    "binaryfile", "battle_pack.bin")
PACK_SHA = "d1bb89aac759cfcd4eb181715d9e88afb78d62a9a3fcffa6242f365f182cbc98"
VALIDATE, FAMILY, RELOCATE, BIND, BIND2, BINDER = 0x322C50, 0x309440, 0x3846F0, 0x3845F0, 0x236C30, 0x238660
INNER = {0x238160: "equipment rows", 0x238660: "shop table", 0x3847B0: "003847B0"}
SKIP = {0x238880: "gambit table - heap 6", 0x237FC0: "ability lookup - heap 6 after its first 003845F0"}
W.ALLOWED |= {0x16D6A0} | set().union(*(W.closure(f) for f in (VALIDATE, FAMILY, RELOCATE, BIND) + tuple(INNER)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
B = 0x76100000


def r(a, fmt):
    return struct.unpack(fmt, bytes(uc.mem_read(a, struct.calcsize(fmt))))


def run(fn, *args):
    ok = S.call(fn, *args)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- read 00236C30's binding calls from its own instruction stream ----
raw_img = W.raw


def file_off(va):
    pe = struct.unpack_from("<I", raw_img, 0x3C)[0]
    n = struct.unpack_from("<H", raw_img, pe + 6)[0]
    o = pe + 24 + struct.unpack_from("<H", raw_img, pe + 20)[0]
    for _ in range(n):
        vs, sva, rs, ra = struct.unpack_from("<IIII", raw_img, o + 8)
        if sva + 0x120000 <= va < sva + 0x120000 + rs:
            return ra + va - sva - 0x120000
        o += 40


md = Cs(CS_ARCH_X86, CS_MODE_64)
k = file_off(0x236C70)
calls, slot, dirent, r8 = [], None, None, 0
for ins in md.disasm(raw_img[k:k + 0x3D0], 0x236C70):
    m = re.search(r"rip \+ (0x[0-9a-f]+)", ins.op_str)
    if ins.mnemonic == "lea" and ins.op_str.startswith("rcx") and m:
        slot = ins.address + ins.size + int(m.group(1), 16)
    mm = re.search(r"\[r[ac]x \+ (0x[0-9a-f]+)\]", ins.op_str)
    if ins.mnemonic in ("movsxd", "mov") and ins.op_str.startswith(("rdx", "ecx")) and mm:
        dirent = int(mm.group(1), 16)
    if ins.mnemonic == "xor" and ins.op_str == "r8d, r8d":
        r8 = 0
    if ins.mnemonic == "mov" and ins.op_str.startswith("r8d, "):
        r8 = int(ins.op_str.split(", ")[1], 16)
    if ins.mnemonic == "call":
        calls.append((int(ins.op_str, 16), slot, dirent, r8))
        slot, dirent = None, None
    if ins.mnemonic == "ret":
        break

pack = open(PACK, "rb").read()
assert hashlib.sha256(pack).hexdigest() == PACK_SHA
uc.mem_write(B, pack)
okr, _ = run(RELOCATE, 0x208E680, B, 0)
d = lambda off: r(B + off, "<I")[0]
made, skipped, failed = [], [], []
for fn, sl, off, r8v in calls:
    if fn in (BIND, 0x3846F0):
        ok, _ = run(fn, sl, d(off), r8v)
        (made if ok else failed).append("%X(%08X, +%X)" % (fn, sl, off))
    elif fn in INNER:
        ok, _ = run(fn, d(off))
        (made if ok else failed).append("%X(+%X) %s" % (fn, off, INNER[fn]))
    elif fn == 0x237FC0:
        ok, _ = run(BIND, 0x2EBF138, d(off))              # 00237FDE: its first call, 003845F0(02EBF138, dir)
        (made if ok else failed).append("003845F0(02EBF138, +%X) - 00237FC0's first call" % off)
        skipped.append("%X %s" % (fn, SKIP[fn]))
    else:
        skipped.append("%X %s" % (fn, SKIP.get(fn, "")))
record("bind_every_shipped_slot", okr and not [f for f in failed if "003847B0" not in f], made=len(made), skipped=skipped, failed=failed,
       note="every binding call of 00236C30 re-made from its own instruction stream: %d made, skipped: %s" % (len(made), "; ".join(skipped)))

# ---- the 32 arms: each class's range from what its arm reads, and the validator at the edges ----
cnt = lambda cell: (r(r(cell, "<Q")[0] + 4, "<I")[0] if r(cell, "<Q")[0] else 0)
ARMS = {2: (0x2EBF130, 0), 3: (0x2EBF120, 0), 4: (0x2EBF150, 0), 5: (0x2EBF100, 0), 6: (0x2EBF0F8, 0x1000), 7: (0x2EBF098, 0x2000),
        8: (0x2EBF0F0, 0x3000), 9: (0x2EBF0E8, 0x4000), 10: (0x2EBF0E0, 0x5000), 11: (0x2EBF0D8, 0x6000), 12: (0x2EBF0D0, 0x7000),
        14: (0x2EBF070, 0x9000), 15: (0x2EBF068, 0xA000), 16: (0x2EBF060, 0xB000), 17: (0x2EBF0C8, 0xC000), 18: (0x2EBF058, 0xD000),
        20: (0x2EBF138, 0), 21: (0x2EBF128, 0), 24: (0x2EBF110, 0), 25: (0x2EBF038, 0), 26: (0x2EBF118, 0), 27: (0x2EBF050, 0),
        28: (0x2EBF0B0, 0), 29: (0x2EBF040, 0), 30: (0x2EBF068, 0xA000), 31: (0x2EBF068, 0xA000), 32: (0x2EBF038, 0)}


def expected(c):
    if c in ARMS:
        cell, lo = ARMS[c]
        return lo, lo + cnt(cell)
    if c == 13:
        return 0x8000, 0x8000 + sum(cnt(x) for x in (0x2EBF090, 0x2EBF088, 0x2EBF080, 0x2EBF078))
    if c == 19:
        return 0xE000, 0xEFFF
    if c == 22:
        return 0, 4
    if c == 23:
        return 0, 9
    return None


per, bad = {}, []
for c in range(2, 33):
    lo, hi = expected(c)                                    # accepted ids: lo .. hi-1
    probes = sorted({lo - 1, lo, hi - 1, hi} - {-1})
    got = {}
    for i in probes:
        ok, v = run(VALIDATE, c, i)
        got["%X" % i] = v
        want = 1 if lo <= i < hi else 0
        if not ok or v != want:
            bad.append([c, "%X" % i, v, want])
    per[c] = {"range": ["%X" % lo, "%X" % (hi - 1)] if hi > lo else "empty", "probes": got}
record("arms_2_to_32_at_their_edges", not bad, per_class=per, mismatches=bad[:6],
       note="for classes 2..32 the validator accepts exactly lo .. lo+count-1 of the table its arm reads (class 13: the sum of four "
            "counts; 19: E000..EFFE; 22 / 23: 0..3 / 0..8), probed at lo-1, lo, hi-1, hi over the shipped bindings")

# ---- class 1: re-dispatch through the family code, for every family ----
fam = {}
bad1 = []
for n in range(0, 16):
    ok, code = run(FAMILY, n << 12)
    code = code - (1 << 32) if code & 0x80000000 else code
    ids = [n << 12, (n << 12) | 0x0FFF]
    if 1 <= code + 0 <= 32:
        lo, hi = expected(code) if code >= 2 else (None, None)
        if lo is not None and lo >> 12 == n and hi > lo:
            ids += [hi - 1, hi] if hi - 1 >= lo else []
    rows = {}
    for i in ids:
        v1 = run(VALIDATE, 1, i)[1]
        vc = run(VALIDATE, code, i)[1] if 1 <= code <= 32 else 0
        rows["%X" % i] = [v1, vc]
        if v1 != vc:
            bad1.append([n, "%X" % i, v1, vc])
    fam[n] = {"family_code": code, "class1_vs_code": rows}
record("class1_redispatch_every_family", not bad1, per_family=fam, mismatches=bad1[:6],
       note="class 1 on an id answers what the class named by 00309440 (the id's family code) answers, for every family 0..15 "
            "(15 has no family: 00309440 gives -1 and class 1 refuses)")

# ---- I2 on shipped data: class 6 and the inventory family disagree on the equipment range ----
eq_count = cnt(0x2EBF0F8)
inv_count = r(0x1EEBCC0 + 1 * 0x58 + 0x3C, "<I")[0]
probe = 0x1000 + inv_count
record("I2_validator_vs_inventory_count", eq_count > inv_count and run(VALIDATE, 6, probe)[1] == 1 and run(VALIDATE, 1, probe)[1] == 1,
       equipment_rows=eq_count, inventory_family_count=inv_count, id="%X" % probe,
       note="the shipped equipment table has %d rows, the inventory family counts %d: id %X passes the validator (classes 6 and 1) "
            "although the inventory registry's range ends before it - two domains, two answers" % (eq_count, inv_count, probe))

json.dump({"ok": allok, "battle_pack_sha256": PACK_SHA, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
