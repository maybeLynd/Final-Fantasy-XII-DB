"""order_record.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
BattleUnit +0x708 is an AiOrderRecord* (the committed order record), and BattleUnit +0xBA0..+0xBB7 is an embedded
AiOrderRecord (the issued command's record) - so the rows that called +0xBA2 and +0xBA6..+0xBB7 unaccessed were
displacement-census artifacts: those bytes are read through +0x708.

  P  PRODUCER: BattleUnit_CommitAction 0030F760 keeps its second argument in r12 (0030F782) and stores it at unit +0x708
     (0030F7F9); r12 is used nowhere else in the body, so 0030F760 reads no field of the record itself
  S  SOURCES: the five rel32 calls to 0030F760 pass as rdx: the unit's own +0xBA0 (00305B19 lea rdx, [rbx + 0xba0]); the
     static records 01EEC298 (00305C86) and 01EEC2B0 (003130CB); a gambit set's record, set + 0x20 + 0x18 * k (00305D93 /
     00305D97, then 00305DE0 mov rdx, rbx); and the current +0x708 itself (0030FA4D, a re-commit)
  I  THE ISSUED RECORD: BattleUnit_IssueCommand 00311CF0 writes the action id at +0xBA0 (00311D7A) and ORs 0x8000 into
     +0xBA4 (00311DB6 / 00311DBB); BattleUnit_SelectAndCommitNextAction 00305AB0, when unit flag 0x4000 is set, clears it,
     reads +0xBA0 and commits unit + 0xBA0 with r9d = +0xBB8 (00305AE4..00305B2F)
  R  READERS THROUGH +0x708 (BattleUnit bodies): word +2 read signed (002FDDBE, 002FE68D, 002FE8ED; 002FE929 unsigned),
     word +4 tested (002FFCB1 0x2000, 00325C83 0x200, 00325CAA 0x100, 00325DF4 byte 4, 00308736 / 00328604 cmp 0 + jl = the
     sign bit), word +6 (002FE682); the gambit walk compares candidates with it by identity (00305D53 / 00305DA4) and tests
     its +4 for 0x4000 (00305D7F). Record +4 bit 15 is exactly the bit IssueCommand sets in +0xBA4
  D  THE STATIC RECORDS (.data): 01EEC298 = {0x4021, 0, flags 0x2000}, 01EEC2B0 = {0x0096, 0, flags 0x2000}, the rest zero;
     01EEC2D0 has AiOrderSet's head shape: count byte 0 = 1 and, at +0x20, one record {0x0096, 0, 0, selector0 = 0x000A}
     (IssueCommand installs 01EEC2D0 at +0x6F8, 00311DD4 / 00311DE1)
  W  REGRESSION (FAILS before): +0x708 is AiOrderRecord*; one embedded AiOrderRecord row at +0xBA0 replaces the four rows,
     keeping their names and texts; AiOrderRecord's instance cell names the new homes
Not claimed: what writes the issued record's +2 and +6..+0x17 (none found in IssueCommand; it may be zeroed with the unit);
01EEC2D0's full extent as an AiOrderSet (other data may follow +0x50); the meaning of the flags bits; 001CC515 / 0042016B,
which load +0x708 of an object not proven to be a BattleUnit.
Usage: python order_record.py [--patch]
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def dis(lo, hi): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)]
def has(lo, hi, pairs):
    A = {a: (m, o) for a, m, o in dis(lo, hi)}
    miss = [hex(a) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss)
    return not miss
def rip(a, size, disp): return a + size + disp
body = dis(0x30F760, 0x30F99A)
r12 = [(a, m, o) for a, m, o in body if "r12" in o]
check("P", [(a, m, o) for a, m, o in r12 if m not in ("push", "pop")] == [(0x30F782, "mov", "r12, rdx"), (0x30F7F9, "mov", "qword ptr [rbx + 0x708], r12")]
      and body[-1][1] == "ret" and body[-1][0] < 0x30F99A,
      "0030F760: rdx -> r12 (0030F782) -> unit +0x708 (0030F7F9); r12 has no other use up to the ret")
text = [s for s in pe.sections if s.Name.startswith(b".text")][0]
tb = B + text.VirtualAddress; buf = d[text.PointerToRawData:text.PointerToRawData + text.SizeOfRawData]
callers = sorted(tb + m.start() for m in re.finditer(rb"\xE8", buf) if m.start() + 5 <= len(buf)
                 and tb + m.start() + 5 + struct.unpack_from("<i", buf, m.start() + 1)[0] == 0x30F760)
check("S", callers == [0x305B2F, 0x305C9B, 0x305DF4, 0x30FA5C, 0x3130DC]
      and has(0x305B12, 0x305B34, [(0x305B19, ("lea", "rdx, [rbx + 0xba0]")), (0x305B2F, ("call", "0x30f760"))])
      and has(0x305C7E, 0x305CA0, [(0x305C86, ("lea", "rdx, [rip + 0x1be660b]")), (0x305C9B, ("call", "0x30f760"))]) and rip(0x305C86, 7, 0x1BE660B) == 0x1EEC298
      and has(0x3130CB, 0x3130E1, [(0x3130CB, ("lea", "rdx, [rip + 0x1bd91de]")), (0x3130DC, ("call", "0x30f760"))]) and rip(0x3130CB, 7, 0x1BD91DE) == 0x1EEC2B0
      and has(0x305D93, 0x305DF9, [(0x305D93, ("lea", "rbx, [r10 + 0x20]")), (0x305D97, ("lea", "rbx, [rbx + rcx*8]")), (0x305DC7, ("mov", "rdx, rbx")),
                                   (0x305DE0, ("mov", "rdx, rbx")), (0x305DF4, ("call", "0x30f760"))])
      and has(0x30FA4D, 0x30FA61, [(0x30FA4D, ("mov", "rdx, qword ptr [rbx + 0x708]")), (0x30FA5C, ("call", "0x30f760"))]),
      "five rel32 callers; rdx = unit+0xBA0, 01EEC298, 01EEC2B0, set+0x20+0x18k, [unit+0x708]")
check("I", has(0x311CF0, 0x311DC2, [(0x311D7A, ("mov", "word ptr [rbx + 0xba0], si")), (0x311DB6, ("mov", "eax, 0x8000")), (0x311DBB, ("or", "word ptr [rbx + 0xba4], ax"))])
      and has(0x305ACD, 0x305B34, [(0x305AD0, ("mov", "ecx, 0x4000")), (0x305ADF, ("test", "rcx, rax")), (0x305AE4, ("movzx", "esi, word ptr [rbx + 0xba0]")),
                                   (0x305AEB, ("btr", "rax, 0xe")), (0x305B12, ("mov", "r9d, dword ptr [rbx + 0xbb8]")), (0x305B19, ("lea", "rdx, [rbx + 0xba0]"))]),
      "IssueCommand writes +0xBA0 and ORs 0x8000 into +0xBA4; flag 0x4000 makes SelectAndCommitNextAction commit unit+0xBA0 with r9d = +0xBB8")
RD = [(0x2FDDA6, [(0x2FDDA6, ("mov", "rax, qword ptr [rcx + 0x708]")), (0x2FDDBE, ("movsx", "ecx, word ptr [rax + 2]"))]),
      (0x2FE67B, [(0x2FE67B, ("mov", "rcx, qword ptr [rcx + 0x708]")), (0x2FE682, ("movzx", "eax, word ptr [rcx + 6]")), (0x2FE68D, ("movsx", "ebx, word ptr [rcx + 2]"))]),
      (0x2FE8E2, [(0x2FE8E2, ("mov", "rax, qword ptr [rcx + 0x708]")), (0x2FE8ED, ("movsx", "edx, word ptr [rax + 2]"))]),
      (0x2FE922, [(0x2FE922, ("mov", "rax, qword ptr [rcx + 0x708]")), (0x2FE929, ("movzx", "ecx, word ptr [rax + 2]"))]),
      (0x2FFCA5, [(0x2FFCA5, ("mov", "rax, qword ptr [rbx + 0x708]")), (0x2FFCAC, ("mov", "ecx, 0x2000")), (0x2FFCB1, ("test", "word ptr [rax + 4], cx"))]),
      (0x30872A, [(0x30872A, ("mov", "rax, qword ptr [rbx + 0x708]")), (0x308736, ("cmp", "word ptr [rax + 4], 0")), (0x30873B, ("jl", "0x308751"))]),
      (0x325C72, [(0x325C72, ("mov", "rax, qword ptr [rdi + 0x708]")), (0x325C7E, ("mov", "ecx, 0x200")), (0x325C83, ("test", "word ptr [rax + 4], cx"))]),
      (0x325C99, [(0x325C99, ("mov", "rax, qword ptr [rdi + 0x708]")), (0x325CA5, ("mov", "ecx, 0x100")), (0x325CAA, ("test", "word ptr [rax + 4], cx"))]),
      (0x325DE8, [(0x325DE8, ("mov", "rax, qword ptr [rdi + 0x708]")), (0x325DF4, ("test", "byte ptr [rax + 4], 4"))]),
      (0x3285F8, [(0x3285F8, ("mov", "rax, qword ptr [rbx + 0x708]")), (0x328604, ("cmp", "word ptr [rax + 4], 0")), (0x328609, ("jl", "0x328612"))]),
      (0x305D53, [(0x305D53, ("mov", "r14, qword ptr [r13 + 0x708]")), (0x305D74, ("mov", "eax, 0x4000")), (0x305D7F, ("test", "word ptr [r14 + 4], ax")), (0x305DA4, ("cmp", "r14, rbx"))])]
check("R", all(has(a, max(x for x, _ in pr) + 8, pr) for a, pr in RD),
      "through +0x708: +2 signed word (002FDDBE, 002FE68D, 002FE8ED), +2 word (002FE929), +4 tests 0x2000 / 0x200 / 0x100 / 4 / sign "
      "(002FFCB1, 00325C83, 00325CAA, 00325DF4, 00308736, 00328604), +6 (002FE682); the walk's identity compare 00305DA4")
def words(v, n): o = off(v); return list(struct.unpack_from("<%dH" % n, d, o))
data = [s for s in pe.sections if s.Name.startswith(b".data")][0]
in_data = B + data.VirtualAddress <= 0x1EEC298 and 0x1EEC320 <= B + data.VirtualAddress + data.SizeOfRawData
check("D", in_data and words(0x1EEC298, 12) == [0x4021, 0, 0x2000] + [0] * 9 and words(0x1EEC2B0, 12) == [0x0096, 0, 0x2000] + [0] * 9
      and d[off(0x1EEC2D0)] == 1 and not any(d[off(0x1EEC2D1):off(0x1EEC2F0)]) and words(0x1EEC2F0, 12) == [0x0096, 0, 0, 0x000A] + [0] * 8
      and has(0x311DD4, 0x311DE8, [(0x311DD4, ("lea", "rax, [rip + 0x1bda4f5]")), (0x311DE1, ("mov", "qword ptr [rbx + 0x6f8], rax"))]) and rip(0x311DD4, 7, 0x1BDA4F5) == 0x1EEC2D0,
      "01EEC298 {0x4021,0,0x2000}, 01EEC2B0 {0x96,0,0x2000}, 01EEC2D0 count 1 + record {0x96,0,0,sel0 0xA}, installed at +0x6F8 by IssueCommand")
REC = "_index/candidates/battleunit-order-record-opus/order_record.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
OLD = ["0xBA0", "0xBA2", "0xBA4", "0xBA6"]
M708 = ("THE COMMITTED ORDER RECORD (AiOrderRecord*; %s P S R): BattleUnit_CommitAction 0030F760 stores its second argument here (0030F7F9) and reads no "
        "field of it; the sources are a gambit set's record (set + 0x20 + 0x18k, 00305DE0), the unit's own issued record +0xBA0 (00305B19), the static "
        "records 01EEC298 / 01EEC2B0 (00305C86 / 003130CB) and itself (0030FA4D). Readers go through it to +2 (signed), +4 (flag tests incl. the sign) and +6. " % REC)
MBA0 = ("THE ISSUED COMMAND'S ORDER RECORD (embedded AiOrderRecord; %s I R). SelectAndCommitNextAction commits unit + 0xBA0 when unit flag 0x4000 is set "
        "(00305B19), so its fields are read through +0x708 like any set record. +0x00 actionSelector = the former flagBit14ActionId (FABLE's name; "
        "IssueCommand writes it, 00311D7A); +0x02 actionParameter = the former issuedCommandWordBA2 ('unaccessed' - read through +0x708 at +2); +0x04 flags "
        "= the former commandIssueFlags (IssueCommand ORs 0x8000, read through +0x708 as the sign, 00308736 / 00328604); +0x06..+0x17 selectors = the "
        "former blockBA6 ('unaccessed tail' - +6 is read through +0x708, 002FE682). Who writes +2 and +6..+0x17 here is not established" % REC)
AIO = "; also BattleUnit +0xBA0 (the issued command's record, embedded), the static records 01EEC298 and 01EEC2B0, and 01EEC2F0 (order 0 of the static command set 01EEC2D0) - all passed to BattleUnit_CommitAction as its record (OPUS 2026-09-28, %s)" % REC
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    out, was, first = [], [], None
    for l in fl:
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == "BattleUnit" and c[1] == "0x708" and c[4] == "ptr":
            c[4] = "AiOrderRecord*"; c[5] = M708 + "|| " + c[5]
            c[8] += " || RETYPED 2026-09-28 (OPUS, %s P S R): ctype was ptr. %s" % (REC, EXE); out.append("\t".join(c) + ee); continue
        if c[0] == "BattleUnit" and c[1] in OLD:
            was.append("%s %s %s %s: %s [%s %s]" % (c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
            if first is None: first = (len(out), ee)
            continue
        out.append(l)
    if first is not None:
        row = ["BattleUnit", "0xBA0", "24", "issuedCommandOrder", "AiOrderRecord", MBA0, "TYPE RESOLVED", "PROVEN",
               "RE-CUT 2026-09-28 (OPUS, %s I R W): four rows replaced by the embedded record; was: %s. %s" % (REC, " || ".join(was), EXE)]
        out.insert(first[0], "\t".join(row) + first[1])
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i_, l in enumerate(tl):
        c = cells(l); ee = l[len(l.rstrip("\r\n")):]
        if c[0] == "AiOrderRecord" and "BattleUnit +0xBA0" not in c[3]: c[3] += AIO; tl[i_] = "\t".join(c) + ee
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "BattleUnit"]
Tt = [cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "AiOrderRecord"]
r708 = [c for c in F if c[1] == "0x708"]; rba = [c for c in F if c[1] in OLD]
check("W", len(r708) == 1 and r708[0][4] == "AiOrderRecord*" and len(rba) == 1 and rba[0][1] == "0xBA0" and rba[0][2] == "24" and rba[0][4] == "AiOrderRecord"
      and "flagBit14ActionId" in rba[0][5] and "blockBA6" in rba[0][8] and len(Tt) == 1 and "BattleUnit +0xBA0" in Tt[0][3],
      "+0x708 is AiOrderRecord*; +0xBA0 is one embedded AiOrderRecord row keeping the old names and texts; AiOrderRecord lists its new homes")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
