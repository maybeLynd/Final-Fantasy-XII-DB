"""vp8_threading.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Vp8DecoderInstance +0x42F0..+0x4443 (one 340-byte
unread span) holds the decoder's threading state; vp8_destroy's two teardown calls read it (vp8_lifetime.py V1: 00171790 when
+0x4380 is non-zero, then 00172160).

  K  00171790 and 00172160 take the lock +0x43B8 through TryEnterCriticalSection (spinning 0xFA0 times) / EnterCriticalSection /
     LeaveCriticalSection to read +0x4380; 00172160 stores 0 there under the lock (001721E8). So +0x43B8 is a 40-byte CRITICAL_SECTION
     and +0x4380 the flag it guards
  R  00171790(inst, rows): DeleteCriticalSection on each 0x28-byte entry of the array at +0x43B0 (rows entries), frees it; frees
     +0x43A8; for each of the six pointer arrays +0x43E0, +0x43E8, +0x43F0, +0x43F8, +0x4400, +0x4408 frees each of its rows
     entries and then the array. Every free is the CRT free import on the pointer 8 bytes before (the vpx_memalign original)
  T  00172160: for i < [+0x4390]: ReleaseSemaphore([+0x4428][i], 1, 0), WaitForSingleObject([+0x4420][i], INFINITE) and CloseHandle
     of the thread when the wait returns 0; then CloseHandle of each [+0x4428][i], CloseHandle([+0x4430]), and frees +0x4420,
     +0x4428, +0x4410 (the Vp8MacroblockDecoder thread records, vp8_mbd_carve.py T1) and +0x4418
  S  REGRESSION: the span is re-cut as generated, tiling kept (FAILS before)
Usage: python vp8_threading.py [--patch]
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXE_P = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"); d = open(EXE_P, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe_ = pefile.PE(EXE_P, fast_load=True); pe_.parse_data_directories(directories=[1])
IMP = {i.address: (i.name or b"").decode() for e in pe_.DIRECTORY_ENTRY_IMPORT for i in e.imports}
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
A = lambda pairs: all(at(a)[:2] == v for a, v in pairs)
imp = lambda a: IMP.get(at(a)[2])
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
k = (A([(0x1717C0, ("lea", "rcx, [rdi + 0x43b8]")), (0x1717E8, ("mov", "ebx, dword ptr [rdi + 0x4380]")), (0x1717D3, ("cmp", "ebx, 0xfa0")),
        (0x1721E8, ("mov", "dword ptr [rbx + 0x4380], r15d")), (0x172170, ("lea", "rbp, [rcx + 0x43b8]"))])
     and [imp(a) for a in (0x1717C7, 0x1717E2, 0x1717F5, 0x172183, 0x17219A, 0x1721A9, 0x1721EF)]
     == ["TryEnterCriticalSection", "EnterCriticalSection", "LeaveCriticalSection", "TryEnterCriticalSection", "EnterCriticalSection", "LeaveCriticalSection", "LeaveCriticalSection"])
check("K", k, "+0x43B8 is the lock around the flag +0x4380 (read in both, cleared by 00172160)")
arrays = (0x43E0, 0x43E8, 0x43F0, 0x43F8, 0x4400, 0x4408)
body = [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x171790):off(0x171AC0)], 0x171790)]
arr_ok = all(any(o == "rax, qword ptr [rdi + 0x%x]" % a for ad, m, o in body) and any(o == "qword ptr [rdi + 0x%x], r14" % a for ad, m, o in body) for a in arrays)
frees = [ad for ad, m, o in body if m == "call" and IMP.get(at(ad)[2]) == "free"]
pre8 = all(any(o == "rcx, qword ptr [rcx - 8]" and ad2 < ad and ad - ad2 <= 8 for ad2, m, o in body) for ad in frees)
r = (A([(0x171820, ("mov", "rcx, qword ptr [rdi + 0x43b0]")), (0x171830, ("add", "rbx, 0x28")), (0x171857, ("mov", "rcx, qword ptr [rdi + 0x43a8]"))])
     and imp(0x17182A) == "DeleteCriticalSection" and arr_ok and pre8 and len(frees) == 14)
check("R", r, "00171790: 0x28-stride critical-section array +0x43B0 deleted and freed; +0x43A8 freed; six per-row pointer arrays freed (%d frees, each on [p-8])" % len(frees))
t = (A([(0x1721F8, ("cmp", "dword ptr [rbx + 0x4390], r15d")), (0x172210, ("mov", "rcx, qword ptr [rbx + 0x4428]")), (0x172228, ("mov", "rax, qword ptr [rbx + 0x4420]")),
        (0x172294, ("mov", "rcx, qword ptr [rbx + 0x4430]")), (0x1722DE, ("mov", "rcx, qword ptr [rbx + 0x4410]")), (0x1722FB, ("mov", "rcx, qword ptr [rbx + 0x4418]"))])
     and [imp(a) for a in (0x172222, 0x172239, 0x172246, 0x172280, 0x1722A5, 0x1722BB, 0x1722D8, 0x1722F5, 0x172312)]
     == ["ReleaseSemaphore", "WaitForSingleObject", "CloseHandle", "CloseHandle", "CloseHandle", "free", "free", "free", "free"])
check("T", t, "00172160: semaphores +0x4428 released, threads +0x4420 joined and closed, +0x4430 closed; +0x4420 / +0x4428 / +0x4410 / +0x4418 freed")
FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/vp8-macroblock-decoder/vp8_threading.py"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"; INST = "Vp8DecoderInstance"
P, U = ("TYPE RESOLVED", "PROVEN"), ("DISCOVERED", "UNKNOWN")
def row(o, sz, nm, ct, mean, rd, tag): return [INST, "0x%X" % o, str(sz), nm, ct, mean, rd[0], rd[1], "RE-CUT 2026-09-28 (OPUS, %s %s). was part of unobservedSpan42F0 uint8[340]. %s" % (REC, tag, EXE)]
FREE8 = "freed through the CRT free import on the pointer 8 bytes before it (the vpx_memalign original) and nulled"
ROWS = [row(0x42F0, 144, "unobservedSpan42F0", "u8[144]", "not read by the teardown", U, "K R T"),
        row(0x4380, 4, "threadsActive", "uint32", "the flag guarded by the lock +0x43B8: vp8_destroy runs 00171790 only when it is non-zero, both teardown routines read it under the lock, and 00172160 clears it", P, "K"),
        row(0x4384, 12, "unobservedSpan4384", "u8[12]", "not read by the teardown", U, "K"),
        row(0x4390, 4, "threadCount", "uint32", "the number of decoder threads: the bound of 00172160's semaphore / handle loops (compared signed, jle) and of vp8_decode's thread-record loop", P, "T"),
        row(0x4394, 20, "unobservedSpan4394", "u8[20]", "not read by the teardown", U, "T"),
        row(0x43A8, 8, "ownedBuffer43A8", "void*", "an owned buffer " + FREE8 + " by 00171790", P, "R"),
        row(0x43B0, 8, "rowLocks", "void*", "an array of one 0x28-byte CRITICAL_SECTION per macroblock row: 00171790 calls DeleteCriticalSection on each (count = its row argument) and frees the array (" + FREE8 + ")", P, "R"),
        row(0x43B8, 40, "lock", "u8[40]", "a Win32 CRITICAL_SECTION (TryEnterCriticalSection / EnterCriticalSection / LeaveCriticalSection) guarding threadsActive", P, "K")]
ROWS += [row(a, 8, "rowBuffers%X" % a, "void*", "an array of per-row buffers: 00171790 frees each of its row entries and then the array, each " + FREE8, P, "R") for a in arrays]
ROWS += [row(0x4410, 8, "threadRecords", "Vp8MacroblockDecoder*", "the per-thread Vp8MacroblockDecoder records (stride 0x12A0, count threadCount); 00172160 frees the array (" + FREE8 + ")", P, "T"),
         row(0x4418, 8, "ownedBuffer4418", "void*", "an owned buffer 00172160 frees (" + FREE8 + ")", P, "T"),
         row(0x4420, 8, "threadHandles", "void*", "an array of threadCount thread handles: 00172160 waits on each (WaitForSingleObject, INFINITE), closes it when the wait returns 0, and frees the array", P, "T"),
         row(0x4428, 8, "threadSemaphores", "void*", "an array of threadCount semaphore handles: 00172160 releases each once (ReleaseSemaphore) before the waits, closes each after, and frees the array", P, "T"),
         row(0x4430, 8, "handle4430", "void*", "a handle 00172160 closes (CloseHandle) after the per-thread handles", P, "T"),
         row(0x4438, 12, "unobservedSpan4438", "u8[12]", "not read by the teardown", U, "T")]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == INST and c[1] == "0x42F0" and c[2] == "340" and c[3] == "unobservedSpan42F0":
            out += ["\t".join(x) + e for x in ROWS]; continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8")); print("patched"); sys.exit(0)
F = {cells(l)[1]: cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == INST}
T = {cells(l)[0]: cells(l) for l in open(os.path.join(DB, "_types", "types.tsv"), "rb").read().decode("utf-8").splitlines()}
# a row a later record re-cut or renamed (its evidence names vp8_pbi_names.py) passes if the successor's rows still cover it exactly
# a later record in this package that re-cut or renamed a row names itself in the row's evidence
SUCC_RE = re.compile(r"vp8-macroblock-decoder/(vp8_\w+\.py)")
def by_successor(c): return any(m != os.path.basename(__file__) for m in SUCC_RE.findall(c[8]))
def kept(g):
    if g[1] in F and F[g[1]][2:6] == g[2:6]: return True
    lo = int(g[1], 16); hi = lo + int(g[2]); cov = [c for c in F.values() if lo <= int(c[1], 16) < hi]
    return bool(cov) and all(by_successor(c) for c in cov) and sum(int(c[2]) for c in cov) == int(g[2])
ok = all(kept(g) for g in ROWS) and sum(int(c[2]) for c in F.values()) == int(T[INST][1], 16) and sum(int(g[2]) for g in ROWS) == 340
check("S", ok, "+0x42F0..+0x4443 re-cut as generated (or re-cut / renamed since by a later record of this package, covering the same bytes); Vp8DecoderInstance still tiles 0x4480")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
