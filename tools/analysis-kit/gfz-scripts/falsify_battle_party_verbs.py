"""Falsification pass 1 on how-a-script-changes-the-battle-party (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  B0  the seventeen cited sizes, and the verb table's begin / poll pairs for 0x353..0x35C
  B1  section 2: the flag pair - 003601B0 sets bit cl of 022CB720, 003601C0 clears it; every begin raises 0x13; the preamble
      (roster slots 0-3, 0026DC40(actor, 0)) in setbattlemember, setbattlememberone and addguestbattlemember
  B2  section 3, setbattlemember 0034D4E0: three pops into a descending array, negatives skipped, the leader noted; the
      reconcile 00328DB0(array, 3) only when the mask is a subset of 0035A050(00359C00()) = the non-guest mask & 0x7F; the
      first non-negative selector made leader (00327850) whenever the leader was not requested, reconcile or not
  B3  section 3: setbattlememberone (guest -> nothing; in roster -> 003287A0(sel); else the first roster member), removebattlemember
      (guest -> nothing; 003286E0 only when the roster count > 1), removeguest / addguest (guests only), the lock (main only,
      flag as 0 / 1), and the add/remove begin 0034C030 storing the selector at state +4
  B4  section 4: 003506A0 returns 003596B0's pending answer and clears flag 0x13 when it is 0; 003596B0 = (00324360() != 1),
      00324360 = (0037CB50() != 0); 0037CB50 answers 1 with no task (02EBF400), or with the cursor 02EBF3FE >= 4 on a positive
      step 02EBF3FD, or < 0 otherwise
  B5  section 4: the remove poll 0034CDF0 (0 -> 1 falls through; remove, then raise; state 2) and the add poll 0034C370 (raise,
      then add) - the two orders differ
  B6  section 5: 00320800 walks slots 0-8 through 00322C50(0x17, slot) and keeps a selector <= 6 or in 0x1A..0xFE
  B7  precision on section 2: setbattlemember runs the preamble and raises the flag before popping its three arguments; the
      other begins pop first
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
VERBS = os.path.join(ROOT, "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
at = lambda fa: {x.address: S(x) for x in body(fa)}
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}

SZ = {0x0034D4E0: 277, 0x00350CD0: 159, 0x00350160: 98, 0x00352AF0: 57, 0x0034C030: 33, 0x00352190: 94, 0x00351A40: 81,
      0x003506A0: 33, 0x003596B0: 24, 0x0037CB50: 46, 0x0034CDF0: 97, 0x0034C370: 96, 0x003596D0: 107, 0x00359BA0: 93,
      0x00359C00: 93, 0x00359740: 107, 0x00320800: 144}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
rows = {}
for line in io.open(VERBS, encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if p[0] in ("0353", "0354", "0355", "0358", "0359", "035A", "035B", "035C"):
        rows[p[0]] = (p[3], p[10], p[11])
want = {"0353": ("addpartymember", "0034C030", "0034C370"), "0354": ("removepartymember", "0034C030", "0034CDF0"),
        "0355": ("setbattlemember", "0034D4E0", "003506A0"), "0358": ("removebattlemember", "00350160", "003506A0"),
        "0359": ("setbattlememberone", "00350CD0", "003506A0"), "035A": ("setbattlememberlock", "00351A40", "003506A0"),
        "035B": ("addguestbattlemember", "00352190", "003506A0"), "035C": ("removeguestbattlemember", "00352AF0", "003506A0")}
check("B0", not bad and rows == want, "sizes %s; verb rows %s" % (bad or "all 17 as cited", "as tabled" if rows == want else rows))

FL = (txt(0x003601B0), txt(0x003601C0))
raise13 = {fa: any(s == "call 0x3601b0" for s in txt(fa)) for fa in (0x0034D4E0, 0x00350CD0, 0x00350160, 0x00352AF0, 0x00352190, 0x00351A40)}
pre = {fa: sum(1 for s in txt(fa) if s == "call 0x26dc40") == 1 and "cmp ebx, 4" in txt(fa) for fa in (0x0034D4E0, 0x00350CD0, 0x00352190)}
check("B1", FL[0][:3] == ["mov eax, 1", "shl eax, cl", "or dword ptr [rip + 0x1f6b563], eax"] and FL[1][2] == "not eax"
      and all(raise13.values()) and all(pre.values()),
      "003601B0 sets / 003601C0 clears bit cl of 022CB720; every begin raises 0x13; the slot-0..3 preamble in the three verbs")
M = at(0x0034D4E0)
check("B2", M.get(0x0034D563) == "js 0x34d574" and M.get(0x0034D570) == "cmove ebp, r13d" and M.get(0x0034D574) == "sub rsi, 4"
      and M.get(0x0034D57D) == "call 0x359c00" and M.get(0x0034D584) == "call 0x35a050" and txt(0x0035A050) == ["and ecx, 0x7f", "mov eax, ecx", "ret"]
      and M.get(0x0034D58C) == "cmp eax, r14d" and M.get(0x0034D59B) == "call 0x328db0" and M.get(0x0034D591) == "mov edx, 3"
      and M.get(0x0034D5A0) == "test ebp, ebp" and M.get(0x0034D5C3) == "call 0x327850",
      "negatives skipped; the leader noted; reconcile only on a subset of (non-guest & 0x7F); leader set from the first requested "
      "selector whenever the leader was not requested - independent of the reconcile branch")
O, R, G, A, L, B = at(0x00350CD0), at(0x00350160), at(0x00352AF0), at(0x00352190), at(0x00351A40), at(0x0034C030)
check("B3", O.get(0x00350D27) == "jne 0x350d57" and O.get(0x00350D2B) == "call 0x3596d0" and O.get(0x00350D4D) == "movzx ecx, byte ptr [rsp + 0x20]"
      and O.get(0x00350D52) == "call 0x3287a0" and R.get(0x00350193) == "jne 0x3501af" and R.get(0x003501A2) == "cmp eax, 1" and R.get(0x003501A5) == "jle 0x3501af"
      and G.get(0x00352B14) == "je 0x352b23" and G.get(0x00352B1E) == "jmp 0x3288f0" and A.get(0x003521D8) == "je 0x3521e3" and A.get(0x003521DE) == "call 0x3170e0"
      and L.get(0x00351A75) == "jne 0x351a86" and L.get(0x00351A7E) == "setne dl" and L.get(0x00351A81) == "call 0x328fb0"
      and B.get(0x0034C039) == "mov dword ptr [r8], 0" and B.get(0x0034C048) == "mov dword ptr [rbx + 4], eax",
      "setbattlememberone, removebattlemember (count > 1), the guest-only pair, the main-only lock, the add/remove begin")
P, Q, T = at(0x003506A0), txt(0x003596B0), at(0x0037CB50)
check("B4", P.get(0x003506AF) == "jne 0x3506bb" and P.get(0x003506B1) == "lea ecx, [rax + 0x13]" and P.get(0x003506B4) == "call 0x3601c0"
      and Q[1:5] == ["call 0x324360", "xor ecx, ecx", "cmp eax, 1", "setne cl"] and txt(0x00324360)[1:5] == ["call 0x37cb50", "xor ecx, ecx", "test eax, eax", "setne cl"]
      and {0x02EBF400, 0x02EBF3FD, 0x02EBF3FE} == rips(0x0037CB50) and T.get(0x0037CB63) == "cmp byte ptr [rip + 0x2b42894], 4" and T.get(0x0037CB79) == "jl 0x37cb6c",
      "pending = !(read-in ended); ended = no task, or the cursor past 3 on a positive step, or below 0 otherwise; the flag cleared when done")
X, Y = at(0x0034CDF0), at(0x0034C370)
check("B5", X.get(0x0034CE25) == "mov dword ptr [r8], 1" and X.get(0x0034CE31) == "call 0x328b20" and X.get(0x0034CE3B) == "call 0x3601b0" and X.get(0x0034CE40) == "mov dword ptr [rbx], 2"
      and Y.get(0x0034C3B1) == "call 0x3601b0" and Y.get(0x0034C3BA) == "call 0x3172e0" and Y.get(0x0034C3BF) == "mov dword ptr [rbx], 2",
      "remove: mutate, then raise; add: raise, then mutate; state 0 falls through into 1; state 2 waits")
N = at(0x00320800)
check("B6", N.get(0x0032083A) == "lea ecx, [r8 + 0x17]" and N.get(0x0032083E) == "call 0x322c50" and N.get(0x00320852) == "cmp cl, 6"
      and N.get(0x00320857) == "lea eax, [rcx - 0x1a]" and N.get(0x0032085A) == "cmp al, 0xe4" and N.get(0x00320870) == "cmp ebx, 9",
      "nine slots, validity class 0x17, kept when <= 6 or 0x1A..0xFE")
first_pop = min(a for a, s in M.items() if s == "call 0x267e10")
flag_at = min(a for a, s in M.items() if s == "call 0x3601b0")
others = {fa: min(a for a, s in at(fa).items() if s == "call 0x267e10") < min(a for a, s in at(fa).items() if s == "call 0x3601b0")
          for fa in (0x00350CD0, 0x00350160, 0x00352AF0, 0x00352190, 0x00351A40)}
check("B7", flag_at < first_pop and all(others.values()),
      "(PRECISION on section 2) setbattlemember raises the flag at %08X before its first pop at %08X; the other begins pop first"
      % (flag_at, first_pop))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
