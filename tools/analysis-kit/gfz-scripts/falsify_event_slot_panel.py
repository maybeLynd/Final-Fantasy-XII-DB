"""Falsification pass 1 on the-event-slot-panel-and-its-dead-feeder (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. FABLE's original-code replay
(members/event_slot_setter_replay.py, 8/8 with two mutants) is carried, not re-run.

  S0  sizes: 0020AC30 572, 0020AF10 203, 0020A800 554, 0020A760 146, the two 5-byte thunks, 001EC680 16
  S1  section 3: the thunks 001EC660 -> jmp 0020AC30 (one caller, 0032FD64) and 001EC6A0 -> jmp 0020AF10 (callers 0026B775,
      00354B6D, 00354EDA); the regex literal at 00905958
  S2  section 3, the setter: both flags cleared and the index stored first; the same-name exit at 0020ACD2; the eviction
      0020A760 at 0020ACE5; the sum_ flag 01F832E8 set at 0020ADD6 inside the sum_ arm; the spc_ arm (0020ADDF..0020AE16)
      reached only when sum_ is absent, setting 01F832E9 by cmovne; one ret, preceded by the single -1 restore at 0020AE48
  S3  section 3, the pusher: the name copy (0020AF4A..0020AF56) before the bound check at 0020AF61; the -1 and empty-name
      refusals; the marker stored and never restored; the counter indexed by the reloaded marker
  S4  section 4: 001EC5C0 at 0025E0F0 and 001EC5E0 at 0025E100 inside 0025DF00; 00180120 called at 00229A53; 001EC4B0's
      three caller functions
  S5  section 3 reachability table (REFUTES "each site first calls 001EC680 = min(slot,4); [01DFE40C] = slot"): 001EC680 is
      `slot > 4 ? -1 : slot` (cmova), as section 2's own table says, and only two of the three sites call it (00354B63,
      00354ED0); 0026B750 calls the pusher thunk directly with [[02099D70] + 0x28]
  S6  section 4 (REFUTES "001CD0E0 ... reads 01F832B0 at three sites"): four base-relative reads (00120000 + 0x1E632B0)
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
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
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x0020AC30: 572, 0x0020AF10: 203, 0x0020A800: 554, 0x0020A760: 146, 0x001EC660: 5, 0x001EC6A0: 5, 0x001EC680: 16}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("S0", not bad, "mismatches %s" % bad if bad else "all seven sizes as cited")
lit = blob[OFF(0x00905958):OFF(0x00905958) + 64].split(b"\0")[0].decode()
check("S1", txt(0x001EC660) == ["jmp 0x20ac30"] and txt(0x001EC6A0) == ["jmp 0x20af10"] and callers(0x001EC660) == [0x0032FD64]
      and callers(0x001EC6A0) == [0x0026B775, 0x00354B6D, 0x00354EDA] and callers(0x0020AC30) == [0x001EC660] and callers(0x0020AF10) == [0x001EC6A0]
      and lit == r"(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)",
      "thunk routes and their sites as stated; regex %s" % lit)
St = {x.address: (S(x), rip(x)) for x in body(0x0020AC30)}
rets = [a for a, (s, _r) in St.items() if s == "ret"]
past = [a for a, (s, _r) in St.items() if s.startswith("j") and s.split()[-1].startswith("0x") and int(s.split()[-1], 16) > 0x0020AE48]
check("S2", St[0x0020AC56][1] == [0x01F832E9] and St[0x0020AC5D][1] == [0x01F832E8] and St[0x0020AC64][0].endswith("], esi")
      and St[0x0020ACD2][0] == "je 0x20ae1c" and St[0x0020ACE5][0] == "call 0x20a760" and St[0x0020AD3F][0] == "je 0x20addf"
      and St[0x0020ADD6] == ("mov byte ptr [rip + 0x1d7850b], 1", [0x01F832E8]) and St[0x0020AE13][0] == "cmovne ecx, edx"
      and St[0x0020AE16][1] == [0x01F832E9] and St[0x0020AE48][0].endswith("0xffffffff") and rets == [0x0020AE6B] and not past,
      "flags cleared first; same-name exit; eviction; sum_ -> 01F832E8 inside its arm; spc_ (sum_ absent) -> 01F832E9; one ret after the -1 restore")
P = at(0x0020AF10)
check("S3", P.get(0x0020AF4A) == "cmp rbx, rcx" and P.get(0x0020AF56) == "call 0x1a5760" and P.get(0x0020AF5B) == "mov dword ptr [rip + 0x1bf34ab], edi"
      and P.get(0x0020AF61) == "cmp edi, 4" and P.get(0x0020AF66) == "cmp esi, -1" and P.get(0x0020AF6F) == "cmp qword ptr [rbx], rax"
      and P.get(0x0020AFA3) == "movsxd rax, dword ptr [rip + 0x1bf3462]" and not any(s.endswith("], 0xffffffff") for s in P.values()),
      "name copied before the bound check; -1 and empty-name refusals; marker stored, never restored; counter by the reloaded marker")
check("S4", 0x0025E0F0 in callers(0x001EC5C0) and 0x0025E100 in callers(0x001EC5E0) and callers(0x00180120) == [0x00229A53]
      and len({f for f in (0x00350960, 0x00356D40, 0x00360120)}) == 3
      and all(any(f <= c < f + sizes[f] for c in callers(0x001EC4B0)) for f in (0x00350960, 0x00356D40, 0x00360120)),
      "the driver's two flag reads; 00180120 at 00229A53; 001EC4B0 from three functions")
E = txt(0x001EC680)
pusher_site = at(0x0026B750)
check("S5", E == ["or eax, 0xffffffff", "cmp ecx, 4", "cmova ecx, eax", "mov dword ptr [rip + 0x1c11d7d], ecx", "ret"]
      and callers(0x001EC680) == [0x00354B63, 0x00354ED0] and pusher_site.get(0x0026B772) == "mov ecx, dword ptr [rax + 0x28]"
      and 0x02099D70 in {r for x in body(0x0026B750) for r in rip(x)} and not any(s == "call 0x1ec680" for s in pusher_site.values()),
      "(REFUTES) 001EC680 stores slot or -1 above 4 (cmova), not min(slot, 4); its only callers are 00354B63 / 00354ED0 - "
      "0026B750 reaches the pusher without it")
reads = [x.address for x in body(0x001CD0E0) for o in x.operands
         if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP and 0x1E632B0 <= o.mem.disp < 0x1E632C4]
check("S6", len(reads) == 4, "(REFUTES 'three sites') 001CD0E0 reads the counter array base-relative at %s" % ["%08X" % a for a in reads])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
