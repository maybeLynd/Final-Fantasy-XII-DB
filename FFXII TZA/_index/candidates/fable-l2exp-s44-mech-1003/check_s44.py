"""check_s44.py - FABLE, 2026-10-03: S-44's language code -> id mapping 0017E270, and where the id goes.

Runs against the certified image (sha256 73461d08..., base 00120000) with rvlib + capstone 5.0.7 + unicorn 2.1.4.

  A  static: the body of 0017E270 read in full; a raw reference index (E8/E9 rel32, 0F 8x rel32, EB/7x rel8,
     rip-relative, [reg+RVA], aligned pointer constants) of 0017E270, of its table 01DF0030, of the cache 01E02814
     and of 00285F60; what each caller does with eax.
  B  executed (unicorn): 0017E270 over every table index 0..9 and over crafted non-matching codes; the three
     consumers' original code over ids 0..15 (00285F60, 00229E50, the FileCache switch 001D9645..001D9753).
  C  sensitivity: a mutated image and three mutated claims; each must make a B check FAIL.

Prints PASS/FAIL lines and FAILS N last.  Writes nothing.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, X86_OP_MEM, X86_REG_RIP  # noqa: E402

import unicorn  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RSP, UC_X86_REG_R12,  # noqa: E402
                               UC_X86_REG_RIP)

FAILS = 0


def check(tag, ok, text):
    global FAILS
    FAILS += 0 if ok else 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))
    return ok


# ---------------------------------------------------------------- the claims (the section states exactly these)
CODES = ["jp", "en", "fr", "de", "it", "es", "kr", "ch", "cn", "none"]
ID_OF_INDEX = {0: 10, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 8, 8: 11, 9: 10}      # LC-1
FOLD_00285F60 = {2: 6, 3: 5, 4: 4, 5: 3, 7: 0, 8: 2, 11: 1}                        # LC-4; every other id -> 9
CJK_SET_00229E50 = {0, 7, 8, 10, 11}                                             # LC-5; returns 0 on these
FILECACHE_CODE = {0: "jp", 2: "fr", 3: "de", 4: "it", 5: "es", 7: "kr", 8: "ch", 10: "jp", 11: "cn"}  # LC-3; else "us"
CALLERS = {0x001D9640: 0x001D9400, 0x0022A0C6: 0x0022A0B0, 0x00287919: 0x002878E0, 0x00287C5A: 0x00287C32,
           0x002B5CD0: 0x002B5C90}


def fold(i):
    return FOLD_00285F60.get(i, 9)


def fc(i):
    return FILECACHE_CODE.get(i, "us")


# ---------------------------------------------------------------- unicorn harness
STACK, SCRATCH, SENT = 0x7FF00000, 0x7FE00000, 0x7FFF0000


def make_uc(img):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    pe = struct.unpack_from("<I", img.d, 0x3C)[0]
    soi = struct.unpack_from("<I", img.d, pe + 24 + 56)[0]
    mu.mem_map(img.base, (soi + 0xFFF) & ~0xFFF)
    for name, va, vs, ra, rs in img.secs:
        mu.mem_write(img.base + va, img.d[ra:ra + min(vs, rs)])
    mu.mem_map(STACK - 0x10000, 0x20000)
    mu.mem_map(SCRATCH, 0x10000)
    mu.mem_map(SENT, 0x1000)
    mu.mem_write(SENT, b"\xC3")
    return mu


def call(mu, fn, rcx=0, until=None, regs=None):
    rsp = STACK - 0x100
    mu.mem_write(rsp, struct.pack("<Q", SENT))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RCX, rcx)
    for r, v in (regs or {}).items():
        mu.reg_write(r, v)
    mu.emu_start(fn, until if until else SENT, count=100000)
    return mu.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


CFG = SCRATCH + 0x100       # a fake GameSettingConfig: only setting[0] is read
STR = SCRATCH + 0x800       # crafted code strings
TABLE = 0x01DF0030
CFGPTR = 0x01F82D20


def run_mapper(mu, index):
    mu.mem_write(CFGPTR, struct.pack("<Q", CFG))
    mu.mem_write(CFG, struct.pack("<i", index))
    return call(mu, 0x0017E270)


def run_mapper_crafted(mu, raw):
    """Point table entry 0 (emulated memory only) at a crafted string and run with index 0."""
    mu.mem_write(STR, raw + b"\0" * 8)
    saved = bytes(mu.mem_read(TABLE, 8))
    mu.mem_write(TABLE, struct.pack("<Q", STR))
    try:
        return run_mapper(mu, 0)
    finally:
        mu.mem_write(TABLE, saved)


def measure_B(img):
    mu = make_uc(img)
    ids = dict((i, run_mapper(mu, i)) for i in range(10))
    folds = dict((i, call(mu, 0x00285F60, rcx=i)) for i in range(16))
    cjk = {}
    for i in range(16):
        mu.mem_write(0x01E02814, struct.pack("<i", i))
        cjk[i] = call(mu, 0x00229E50)
    codes = {}
    for i in range(16):
        buf = SCRATCH + 0x2000
        mu.mem_write(buf, b"\xEE" * 0x200)
        mu.reg_write(UC_X86_REG_R12, buf)
        mu.reg_write(UC_X86_REG_RAX, i)
        mu.reg_write(UC_X86_REG_RSP, STACK - 0x100)
        mu.emu_start(0x001D9645, 0x001D9753, count=1000)
        b = bytes(mu.mem_read(buf + 0x1B8, 4))
        codes[i] = b
    return mu, ids, folds, cjk, codes


def B_checks(img, claim_ids=None, claim_cjk=None, quiet=False):
    """Return the number of failing B checks for a given image and claim set (used by the controls)."""
    claim_ids = ID_OF_INDEX if claim_ids is None else claim_ids
    claim_cjk = CJK_SET_00229E50 if claim_cjk is None else claim_cjk
    mu, ids, folds, cjk, codes = measure_B(img)
    bad = 0
    bad += sum(1 for i in range(10) if ids[i] != claim_ids[i])
    bad += sum(1 for i in range(16) if folds[i] != fold(i))
    bad += sum(1 for i in range(16) if (cjk[i] == 0) != (i in claim_cjk))
    bad += sum(1 for i in range(16) if codes[i][:3] != fc(i).encode() + b"\0" or codes[i][3:4] != b"\xEE")
    return bad


def main():
    img = Img.load()
    print("FABLE check_s44 - 0017E270 language code -> id (S-44), image %s..." % "73461d08")
    print("unicorn %s" % unicorn.__version__)
    check("U0", unicorn.__version__ == "2.1.4", "unicorn is the pinned 2.1.4")

    # ------------------------------------------------------------ A: static
    check("A1", img.pdata(0x0017E270) is None, "0017E270 has no .pdata entry (a leaf; function-list censuses can miss it)")
    body = list(img.cs.disasm(img.read(0x0017E270, 0x197), 0x0017E270))
    end = body[-1].address + body[-1].size if body else 0
    check("A2", end == 0x0017E407 and body[-1].mnemonic == "ret" and img.read(0x0017E407, 9) == b"\xCC" * 9,
          "body 0017E270..0017E406 decodes exactly (407 B), last instruction `ret` at %08X, int3 padding after" % body[-1].address)
    calls = [i for i in body if i.mnemonic == "call" or (i.mnemonic == "jmp" and not (0x0017E270 <= (i.operands[0].imm if i.operands[0].type == 2 else 0) < 0x0017E407))]
    writes = [i for i in body for k, op in enumerate(i.operands) if op.type == X86_OP_MEM and k == 0 and i.mnemonic not in ("cmp", "test")]
    check("A3", not calls and not writes, "0017E270 makes no call, no out-of-body jump and no memory store (calls %d, stores %d)" % (len(calls), len(writes)))
    rets = [i.address for i in body if i.mnemonic == "ret"]
    check("A4", len(rets) == 10, "0017E270 has 10 exits (9 compare arms + default): %s" % ["%08X" % a for a in rets])
    cmps = []
    for i in body:
        for op in i.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and i.mnemonic == "cmp":
                cmps.append(i.address + i.size + op.mem.disp)
    want = [0x008C5904 + 4 * k + j for k in range(9) for j in range(3)]
    check("A5", cmps == want, "27 byte compares: bytes 0,1,2 of the nine literals 008C5904+4k (k=0..8; jp..cn) in table order")
    first = body[0]
    tgt = first.address + first.size + first.operands[1].mem.disp
    check("A6", first.mnemonic == "mov" and tgt == CFGPTR and body[2].mnemonic == "movsxd" and body[3].op_str == "rdx, qword ptr [rdx + rcx*8]",
          "0017E270 reads [01F82D20] (no null test), sign-extends dword +0x00 (0017E27E) and indexes 8-byte table entries without a bound (0017E281)")
    for k in range(10):
        p = img.u64(TABLE + 8 * k)
        s = img.read(p, 8).split(b"\0")[0].decode()
        if not check("A7.%d" % k, s == CODES[k], "table[%d] = %08X -> %r" % (k, p, s)):
            pass

    refs, unc = text_refs(img, 0x0017E270)
    sites = dict((r["site"], r["func"]) for r in refs)
    check("A8", sites == CALLERS and all(r["form"] == "call" for r in refs) and not unc and not data_refs(img, 0x0017E270),
          "raw index: 0017E270 has exactly 5 references, all E8 calls, no jmp/jcc/data pointer: %s" %
          ", ".join("%08X(fn %08X)" % (s, f) for s, f in sorted(sites.items())))
    trefs, tunc = text_refs(img, TABLE, TABLE + 0x50)
    check("A9", [r["site"] for r in trefs] == [0x0017E277] and not data_refs(img, TABLE, TABLE + 0x50),
          "raw index: the table 01DF0030..01DF007F is referenced by one instruction image-wide, 0017E277 `%s`; no pointer constant" %
          (trefs[0]["text"] if trefs else "-"))
    crefs, _ = text_refs(img, 0x01E02814, 0x01E02818)
    w = [r["site"] for r in crefs if r["text"].startswith("mov dword ptr [rip")]
    rd = [r["site"] for r in crefs if r["site"] not in w]
    check("A10", w == [0x0022A0CB] and rd == [0x00229E40, 0x00229E50, 0x0022A146, 0x0022A172],
          "raw index: cache 01E02814 has one writer 0022A0CB and four reads 00229E40, 00229E50, 0022A146, 0022A172")
    after = {0x001D9645: "cmp eax, 0xb", 0x0022A0CB: "mov dword ptr [rip + 0x1bd8743], eax", 0x0028791E: "mov ecx, eax",
             0x00287C5F: "mov ecx, eax", 0x002B5CD5: "mov ecx, eax"}
    got = {}
    for a, t in after.items():
        i = next(img.cs.disasm(img.read(a, 16), a))
        got[a] = (i.mnemonic + " " + i.op_str)
    check("A11", got == after, "each caller consumes eax at once: 001D9645 cmp eax,0xb (switch); 0022A0CB store to 01E02814; "
                               "0028791E/00287C5F/002B5CD5 mov ecx,eax")
    nxt = {0x00287920: 0x00285F60, 0x00287C61: 0x00285F60, 0x002B5CD7: 0x00285F60}
    ok = all(next(img.cs.disasm(img.read(a, 5), a)).op_str == "0x285f60" for a in nxt)
    frefs, _ = text_refs(img, 0x00285F60)
    check("A12", ok and sorted(r["site"] for r in frefs) == sorted(nxt),
          "00285F60 has exactly 3 call sites (00287920, 00287C61, 002B5CD7), each passing 0017E270's return in ecx")
    for a, t in ((0x0022A146, "mov ecx, dword ptr [rip + 0x1bd86c8]"), (0x0022A159, "call 0x2df9a0"),
                 (0x0022A172, "mov ecx, dword ptr [rip + 0x1bd869c]"), (0x0022A178, "call 0x862bd0")):
        i = next(img.cs.disasm(img.read(a, 16), a))
        check("A13.%08X" % a, i.mnemonic + " " + i.op_str == t, "%08X `%s`" % (a, t))
    jt = [img.base + img.u32(0x001D9770 + 4 * k) for k in range(12)]
    check("A14", next(img.cs.disasm(img.read(0x001D9648, 6), 0x001D9648)).op_str == "0x1d9734" and len(set(jt)) == 9,
          "001D9645 cmp eax,0xb / ja 001D9734 (default arm) then a 12-entry image-base-relative table at 001D9770")

    grefs, gunc = text_refs(img, 0x00229E40)
    gf = set(r["func"] for r in grefs)
    check("A15", len(grefs) == 36 and len(gf) == 17 and all(r["form"] == "call" for r in grefs) and not gunc,
          "getter 00229E40: %d call sites in %d functions by the raw index (section says 36 in 17)" % (len(grefs), len(gf)))
    us = img.read(0x009005E0, 3)
    t734 = [next(img.cs.disasm(img.read(a, 16), a)) for a in (0x001D9734, 0x001D9744)]
    check("A16", us == b"us\0" and all(i.address + i.size + i.operands[1].mem.disp in (0x009005E0, 0x009005E2) for i in t734),
          "the FileCache default arm 001D9734/001D9744 reads 009005E0 = 'us\\0'")
    span = list(img.cs.disasm(img.read(0x0022A14C, 0x0022A159 - 0x0022A14C), 0x0022A14C))
    clob = [i for i in span if "rcx" in i.op_str.split(",")[0] or "ecx" in i.op_str.split(",")[0] or i.mnemonic == "call"]
    check("A17", not clob and span[-1].address + span[-1].size == 0x0022A159,
          "no instruction between 0022A146 and the call 0022A159 writes ecx or calls: ecx = id at 002DF9A0")
    fw = [(i.mnemonic + " " + i.op_str) for i in img.cs.disasm(img.read(0x00862BD0, 0x1C), 0x00862BD0)]
    check("A18", fw == ["push rbx", "sub rsp, 0x20", "mov ebx, ecx", "call 0x1d69f0", "mov rcx, rax", "mov edx, ebx",
                        "add rsp, 0x20", "pop rbx", "jmp 0x1d68f0"],
          "00862BD0 keeps the id in ebx across 001D69F0() and tail-jumps 001D68F0(rcx = that return, edx = id)")
    rr = [i for i in img.cs.disasm(img.read(0x001D95CF, 3), 0x001D95CF)]
    check("A19", rr and rr[0].mnemonic + " " + rr[0].op_str == "mov r12, rbx",
          "001D95CF `mov r12, rbx`: the switch's +0x1B8 base is the constructed object")

    # ------------------------------------------------------------ B: executed
    mu, ids, folds, cjk, codes = measure_B(img)
    print("      0017E270 executed: " + ", ".join("%d:%s->%d" % (i, CODES[i], ids[i]) for i in range(10)))
    for i in range(10):
        check("B1.%d" % i, ids[i] == ID_OF_INDEX[i], "setting[0]=%d (%s) -> id %d" % (i, CODES[i], ids[i]))
    crafted = [(b"en\x01", 10, "terminator byte compared: 'en' + 0x01"), (b"EN", 10, "case-sensitive: 'EN'"),
               (b"", 10, "empty string"), (b"us", 10, "'us' (the FileCache's en code) is not an input code"),
               (b"cnx", 10, "'cnx' falls past the cn arm"), (b"en", 1, "'en' in a fresh buffer (value compare, not pointer)"),
               (b"cn", 11, "'cn' in a fresh buffer")]
    for k, (raw, want_id, why) in enumerate(crafted):
        got_id = run_mapper_crafted(mu, raw)
        check("B2.%d" % k, got_id == want_id, "%s -> %d" % (why, got_id))
    print("      00285F60 executed: " + ", ".join("%d->%d" % (i, folds[i]) for i in range(16)))
    for i in range(16):
        check("B3.%d" % i, folds[i] == fold(i), "00285F60(%d) = %d" % (i, folds[i]))
    print("      00229E50 executed (0 = in set): " + ", ".join("%d->%d" % (i, cjk[i]) for i in range(16)))
    check("B4", set(i for i in range(16) if cjk[i] == 0) == CJK_SET_00229E50,
          "00229E50 returns 0 exactly for ids %s (mask 0xD81), else 1" % sorted(i for i in range(16) if cjk[i] == 0))
    print("      FileCache switch executed: " + ", ".join("%d->%s" % (i, codes[i][:2].decode('latin1')) for i in range(16)))
    for i in range(16):
        check("B5.%d" % i, codes[i][:3] == fc(i).encode() + b"\0" and codes[i][3:4] == b"\xEE",
              "001D9645..001D9753 with id %d writes %r to +0x1B8..+0x1BA, +0x1BB untouched" % (i, codes[i][:3]))
    print("      chain (setting[0] -> code -> id -> FileCache code / 00285F60 / 00229E50):")
    for i in range(10):
        d = ids[i]
        print("        %d %-4s -> %2d -> %s / %d / %d" % (i, CODES[i], d, codes[d][:2].decode(), folds[d], cjk[d]))
    rt = [i for i in range(9) if codes[ids[i]][:2].decode() != CODES[i]]
    check("B6", rt == [1], "round trip code -> id -> FileCache code returns the input code for 8 of 9 languages; "
                           "only en becomes 'us' (indices differing: %s)" % rt)

    # ------------------------------------------------------------ C: sensitivity
    mut = img.patched(0x0017E2D2, struct.pack("<I", 6))      # en arm: mov eax,1 -> mov eax,6
    n = B_checks(mut)
    check("C1", n > 0, "mutated image (0017E2D1 mov eax,1 -> 6) makes %d B check(s) fail" % n)
    n = B_checks(img, claim_cjk={0, 7, 10, 11})
    check("C2", n > 0, "mutated claim: the locale page's 00229E50 set {0,7,10,11} fails %d B check(s)" % n)
    n = B_checks(img, claim_cjk={0, 6, 7, 8, 10, 11})
    check("C3", n > 0, "mutated claim: the chain page's set {0,6,7,8,10,11} fails %d B check(s)" % n)
    bad = dict(ID_OF_INDEX)
    bad[6] = 6
    n = B_checks(img, claim_ids=bad)
    check("C4", n > 0, "mutated claim: kr -> 6 (table position) fails %d B check(s)" % n)
    n = B_checks(img)
    check("C5", n == 0, "the unmutated image and the section's claims: %d failing B checks" % n)

    print("FAILS %d" % FAILS)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
