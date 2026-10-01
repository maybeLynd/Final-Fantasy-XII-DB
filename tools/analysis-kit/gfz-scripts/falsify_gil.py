"""Falsification pass 1 on CONTRACT-gil-storage-and-movement (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. Every census runs twice - bounded
by the function list, and as a raw E8/E9 byte sweep of .text - and the two must agree (catalogue tails hide nothing).

  N0  section 2: GameState_SetGil 00254EE0 72 B; GameState_GetGil 00253690 11 B; 00309BF0 is 5 B `jmp 0x253690`
  N1  GL-1: the store takes `xor ecx, ecx; mov eax, 0x5f5e0ff; test ebx, ebx; cmovns ecx, ebx; cmp ecx, eax; cmovg ecx, eax`
      (00254F07..00254F15), then `mov dword ptr [rax + 8], ecx`
  N2  GL-2 / GL-4: 00254EF6 `jle`, 00254EF8 `mov cl, 6`, 00254EFC `jns 0x254f07` (past the call), 00254EFE `neg edx`,
      00254F00 `mov cl, 7`, 00254F02 `call 0x316a50`
  N3  GL-3: 00254EF1 `sub edx, dword ptr [rax + 8]` on the raw argument (00254EED/00254EEF copy ecx), before the clamp
  N4  GL-5 / GL-6 / section 16a: the setter has 13 callers in 13 functions - 12 calls and Debug_SetGilToMaximum's tail-jump
      (003058B5) - and no thunk; the getter body has 19 call sites plus the thunk's jmp; the thunk has 3 callers - 2 calls
      and 0032A850's tail-jump; the two caller sets are disjoint; Debug_SetGilToMaximum, the three
      BattleAction_* resource bodies and BattleFormula_ApplyTargetResult are setter callers, and the last is also a getter reader
  N5  section 14: 003F4AA0 gates on `test byte ptr [rcx], 1` and calls both GetGil and SetGil
  K1  (REFUTES section 14's "00290130 is statically orphaned: zero call/jmp edges") 00290130 has exactly one inbound edge, the
      5-byte thunk 002E1A50 `jmp 0x290130` (catalogued as thunk_FUN_00290130), and that thunk is called at 00344C9A in
      FUN_00344C60 - the begin handler of script verb 037C questresultwindow (scriptvm-verb-table.tsv, CONFIRMED).
      00290130(ecx, edx) fetches the bundle (003F8C60), applies it through 003F4AA0 when the fetch succeeds, and posts
      through 003F4BD0. The route census missed it by counting edges to 00290130 only, not to its thunk
"""
import collections, io, os, struct
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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None

SET, GET, THK, ORPH = 0x00254EE0, 0x00253690, 0x00309BF0, 0x00290130
text = next(x for x in SECS if x[0] == ".text")
calls, jmps, refs = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            t = imm(x)
            if x.mnemonic == "call" and t in (SET, GET, THK, ORPH):
                calls[t].append((x.address, fa))
            elif x.mnemonic.startswith("j") and t in (SET, GET, THK, ORPH) and not (fa <= t < fa + sizes[fa]):
                jmps[t].append((x.address, fa))
            for r in rip(x):
                if r == ORPH:
                    refs[ORPH].append(x.address)
            if any(o.type == X86_OP_IMM and o.imm == ORPH for o in x.operands) and x.mnemonic not in ("call",) and not x.mnemonic.startswith("j"):
                refs[ORPH].append(x.address)
    except ValueError:
        continue
raw = blob[text[3]:text[3] + text[4]]
rawhits = collections.defaultdict(list)
for i in range(len(raw) - 5):
    if raw[i] in (0xE8, 0xE9):
        t = text[1] + i + 5 + struct.unpack_from("<i", raw, i + 1)[0]
        if t in (SET, GET, THK, ORPH):
            rawhits[t].append((text[1] + i, "call" if raw[i] == 0xE8 else "jmp"))

W = body(SET)
check("N0", sizes[SET] == 72 and sizes[GET] == 11 and sizes[THK] == 5 and at(body(THK), THK) == "jmp 0x253690",
      "72 / 11 / 5 B; thunk %s" % at(body(THK), THK))
check("N1", [at(W, a) for a in (0x00254F07, 0x00254F09, 0x00254F0E, 0x00254F10, 0x00254F13, 0x00254F15, 0x00254F1F)] ==
      ["xor ecx, ecx", "mov eax, 0x5f5e0ff", "test ebx, ebx", "cmovns ecx, ebx", "cmp ecx, eax", "cmovg ecx, eax", "mov dword ptr [rax + 8], ecx"],
      "floor then cap at 0x5F5E0FF, then the store")
check("N2", [at(W, a) for a in (0x00254EF4, 0x00254EF6, 0x00254EF8, 0x00254EFA, 0x00254EFC, 0x00254EFE, 0x00254F00, 0x00254F02)] ==
      ["test edx, edx", "jle 0x254efc", "mov cl, 6", "jmp 0x254f02", "jns 0x254f07", "neg edx", "mov cl, 7", "call 0x316a50"],
      "gain 6 / spend 7 / zero skips the call to 00254F07")
check("N3", at(W, 0x00254EED) == "mov edx, ecx" and at(W, 0x00254EEF) == "mov ebx, ecx" and at(W, 0x00254EF1) == "sub edx, dword ptr [rax + 8]"
      and 0x00254EF1 < 0x00254F07, "delta from the raw argument at %s, clamp at 00254F07" % at(W, 0x00254EF1))
setf = {f for _a, f in calls[SET]}; getf = {f for _a, f in calls[GET]}; thkf = {f for _a, f in calls[THK]}
nm = lambda fs: sorted(names.get(f, "%08X" % f) for f in fs)
ba = [n for n in nm(setf) if n.startswith("BattleAction_")]
agree = all(sorted(a for a, _f in calls[t] + jmps[t]) == sorted(a for a, _k in rawhits[t]) for t in (SET, GET, THK))
setf |= {f for _a, f in jmps[SET]}; thkf |= {f for _a, f in jmps[THK]}
check("N4", len(calls[SET]) == 12 and jmps[SET] == [(0x003058B5, 0x003058B0)] and len(setf) == 13 and len(calls[GET]) == 19 and jmps[GET] == [(THK, THK)]
      and len(calls[THK]) == 2 and jmps[THK] == [(0x0032A852, 0x0032A850)] and len(thkf) == 3 and not (getf & thkf) and agree and "Debug_SetGilToMaximum" in nm(setf) and len(ba) == 3
      and "BattleFormula_ApplyTargetResult" in nm(setf) and "BattleFormula_ApplyTargetResult" in nm(getf | thkf),
      "setter %d calls + %d tail-jump = %d functions; getter %d calls + jmp from %s; thunk %d calls + %d tail-jump = %d functions; overlap %d; raw sweep agrees %s; %s"
      % (len(calls[SET]), len(jmps[SET]), len(setf), len(calls[GET]), ["%08X" % a for a, _ in jmps[GET]], len(calls[THK]), len(jmps[THK]), len(thkf), len(getf & thkf), agree, ba))
A = body(0x003F4AA0)
qw = blob.count(struct.pack("<Q", ORPH))
rv = struct.pack("<I", ORPH - BASE); occ = []
i = blob.find(rv)
while i >= 0:
    for n_, start, size, rw, rs in SECS:
        if rw <= i < rw + rs:
            occ.append((n_, start + i - rw))
    i = blob.find(rv, i + 1)
check("N5", any(S(x) == "test byte ptr [rcx], 1" for x in A.values()) and any(imm(x) == SET for x in A.values() if x.mnemonic == "call")
      and any(imm(x) in (GET, THK) for x in A.values() if x.mnemonic == "call"), "003F4AA0 gates on +0 bit 0 and calls GetGil and SetGil")
TH = 0x002E1A50
th_raw = [(text[1] + k, raw[k]) for k in range(len(raw) - 5) if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == TH]
O = body(ORPH)
oc = [imm(x) for a, x in sorted(O.items()) if x.mnemonic == "call"]
VT = os.path.join(ROOT, "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
verb = [l.split("	") for l in io.open(VT, encoding="utf-8") if "	00344C60	" in l]
check("K1", jmps[ORPH] == [(TH, TH)] and not calls[ORPH] and [a for a, _k in rawhits[ORPH]] == [TH] and sizes.get(TH) == 5 and names.get(TH) == "thunk_FUN_00290130"
      and at(body(TH), TH) == "jmp 0x290130" and th_raw == [(0x00344C9A, 0xE8)] and verb and verb[0][3] == "questresultwindow" and "CONFIRMED" in verb[0]
      and oc[:3] == [0x003F8C60, 0x003F4AA0, 0x003F4BD0] and not refs[ORPH] and qw == 0 and [n_ for n_, _v in occ] == [".pdata"],
      "(REFUTES '00290130 is statically orphaned') its one inbound edge is the thunk %s (%s); the thunk is called at %s in FUN_00344C60, "
      "the begin handler of verb %s %s; 00290130 calls %s; no other route form (rip/imm %d, qword %d, RVA only in %s)"
      % ("%08X" % TH, names.get(TH), ["%08X" % a for a, _ in th_raw], verb[0][0] if verb else "?", verb[0][3] if verb else "?",
         ["%08X" % c for c in oc], len(refs[ORPH]), qw, [n_ for n_, _v in occ]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
