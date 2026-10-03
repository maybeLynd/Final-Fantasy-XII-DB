"""SWE2-AUDIT-SEM: semantic review of FABLE's GR-2 answer (8583801b7): what each free-target type value denotes.
Two halves:
  S-checks (static, capstone/pefile on Tools/work/exe/FFXII_TZA.exe): the paths from a verb's argument to the nibble -
  the {1,5,3,4} table, BattleUnit_SetRuntimeUnitCategoryMode's spawn-flag side effect, the refresh's rewrites, every
  writer of the nibble (idiom census) - which decide whether "argument -> type" holds unconditionally.
  D-checks (data, the shipped scripts through the kit decoder gen_req_channel_census.py): the producer's join re-tallied
  with the nine language copies folded, and the scripts that set btlAtelSetUnitType(3).
F-checks are findings this review adds (PASS when the finding reproduces). Positive controls are marked CONTROL.

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-gr2-0930/gr2_sem.py"
"""
import collections, csv, io, os, struct, sys
import capstone, pefile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[os.pardir] * 5))  # repo root, not the cwd (OPUS-REQ-AUDITSEM-SEM-REGRESSIONS-UNRUNNABLE-1003, SWE2-AUDIT-SEM 2026-10-03)
DB = os.path.join(ROOT, "Database")
EXE = os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(DB, "Tools", "work", "graph", "functions.tsv")
pe = pefile.PE(EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
X86 = capstone.x86
FAILS = []
FT = {int(r["entry"], 16): (int(r["body_bytes"] or 0), r["name"]) for r in csv.DictReader(open(FUNCS, encoding="utf-8"), delimiter="\t")}
size = {k: v[0] for k, v in FT.items()}
TEXT = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"][0]
TVA = BASE + TEXT.VirtualAddress
TDATA = TEXT.get_data()


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def raw(va, n):
    o = pe.get_offset_from_rva(va - BASE)
    return bytes(pe.__data__[o:o + n])


def s(i): return f"{i.mnemonic} {i.op_str}"


def body(fn):
    n = size[fn]
    return {i.address: i for i in md.disasm(raw(fn, n + 16), fn) if i.address < fn + n}


def ripv(i):
    for op in i.operands:
        if op.type == X86.X86_OP_MEM and op.mem.base == X86.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def tgt(i):
    if (i.mnemonic == "call" or i.mnemonic.startswith("j")) and i.operands and i.operands[0].type == X86.X86_OP_IMM:
        return i.operands[0].imm
    return None


starts = sorted(size)
import bisect
def fn_of(a):
    k = bisect.bisect_right(starts, a) - 1
    f = starts[k] if k >= 0 else None
    return f if f is not None and a < f + max(size[f], 1) else None


def rel_callers(t):
    out = []
    for op in (b"\xe8", b"\xe9"):
        p = 0
        while True:
            k = TDATA.find(op, p)
            if k < 0: break
            p = k + 1
            if k + 5 <= len(TDATA) and TVA + k + 5 + struct.unpack("<i", TDATA[k + 1:k + 5])[0] == t:
                f = fn_of(TVA + k)
                if f is None or (TVA + k) in body(f): out.append(TVA + k)
    return sorted(out)


# =============================== static ===============================================================================
b6b = body(0x002396B0)
check("S1 btlAtelSetUnitType's target 002396B0: v <= 3 reads dword table 01E09EE8 = {1, 5, 3, 4}; v > 3 stores 0; the "
      "result goes to the battle unit's +0x58 (002396D6), not to the nibble",
      ripv(b6b[0x002396C8]) == 0x01E09EE8 and struct.unpack("<4I", raw(0x01E09EE8, 16)) == (1, 5, 3, 4)
      and s(b6b[0x002396C3]) == "cmp ebx, 3" and s(b6b[0x002396D4]) == "xor edx, edx"
      and s(b6b[0x002396D6]) == "mov byte ptr [rax + 0x58], dl")
check("F1 the same function touches the spawn record's flag bit 5 (0x20) only when that record's bits 0 and 2 are both "
      "clear (002396E2 test cl, 5 / jne): it clears bit 5, then raises it again only for mode 4 (002396EC-002396F9)",
      s(b6b[0x002396D9]) == "mov rdx, qword ptr [rax + 0x6a0]" and s(b6b[0x002396E2]) == "test cl, 5"
      and s(b6b[0x002396E5]) == "jne 0x2396fc" and s(b6b[0x002396E7]) == "and ecx, 0xffffffdf"
      and s(b6b[0x002396EC]) == "cmp byte ptr [rax + 0x58], 4" and s(b6b[0x002396F9]) == "or dword ptr [rax], 0x20")
br = body(0x00238BF0)
check("F2 the unit refresh 00238BF0: with spawn flag bit 5 set the mode is kept (00238D98 -> 00238E06); with it clear "
      "a mode of 4 becomes 1 (00238DBD-00238DC3), and a mode of 1 becomes 7 for an enemy row (+0x698 byte +5 == 1) "
      "whose definition byte +0x03 has bit 4 (00238DEF-00238E02)",
      s(br[0x00238D98]) == "test byte ptr [rax], 0x20" and s(br[0x00238D9B]) == "je 0x238dbd" and s(br[0x00238DBB]) == "jmp 0x238e06"
      and s(br[0x00238DBD]) == "cmp byte ptr [rbx + 0x58], 4" and s(br[0x00238DC3]) == "mov byte ptr [rbx + 0x58], 1"
      and s(br[0x00238DEF]) == "cmp byte ptr [rax + 5], 1" and s(br[0x00238DFC]) == "test byte ptr [rax + 3], 0x10"
      and s(br[0x00238E02]) == "mov byte ptr [rbx + 0x58], 7")
check("F2 the refresh writes the nibble from the mode (00238E0D edi = mode, 00238E3E call 00269FE0) and skips the write "
      "when the mode is 0 (00238E34 test edi / 00238E36 je)",
      s(br[0x00238E0D]) == "movsx edi, byte ptr [rbx + 0x58]" and s(br[0x00238E34]) == "test edi, edi"
      and s(br[0x00238E36]) == "je 0x238e43" and tgt(br[0x00238E3E]) == 0x00269FE0)
cw = rel_callers(0x00269FE0)
check("S2 CONTROL the nibble writer 00269FE0 (and byte [+0xe], 0xf0 / or the value's low nibble, 0026A033-0026A03B) has "
      "exactly two callers: setfreetargettype's 003528C0 (003528D6) and the refresh (00238E3E)",
      cw == [0x00238E3E, 0x003528D6] and s(body(0x00269FE0)[0x0026A033]) == "and byte ptr [rbx + 0xe], 0xf0",
      str(["%08X" % a for a in cw]))
# idiom census: every `and byte ptr [reg + 0xe], imm` in .text (disp8 0x0E, opcode 80 /4)
idi = []
for m in range(0x60, 0x68):
    for pre in (b"", b"\x41"):
        pat = pre + bytes([0x80, m, 0x0E]); p = 0
        while True:
            k = TDATA.find(pat, p)
            if k < 0: break
            p = k + 1
            ins = next(md.disasm(TDATA[k:k + 16], TVA + k), None)
            if ins is None or ins.mnemonic != "and": continue
            f = fn_of(TVA + k)
            if f is not None and (TVA + k) not in body(f): continue
            if (ins.operands[1].imm & 0xF) != 0xF:      # clears at least one low-nibble bit
                idi.append((TVA + k, f, s(ins)))
idi.sort()
check("S3 CONTROL the image-wide census of `and byte [reg+0xe], imm` that clears low-nibble bits finds 00269FE0's 0026A033",
      any(a == 0x0026A033 for a, _, _ in idi), "; ".join("%08X %s" % (a, t) for a, _, t in idi))
bi = body(0x00266530); bs = body(0x00265FF0)
check("F3 value 0 is the record initialiser's: ActorStorage_InitializeRecord 00266530 clears the nibble (002666F8 and "
      "byte [rbx+0xe], 0xf0), then calls 00265FF0 (0026681B), which seeds 4 only for actor kind 1 (00266025 -> "
      "002663A3-002663B7) and 5 only for kind 3 (00266034 -> 002660D3 / 002660DE); kind 2's branch writes +8, not +0xE "
      "(0026636A-0026639B), and every other kind leaves 0",
      s(bi[0x002666F8]) == "and byte ptr [rbx + 0xe], 0xf0" and tgt(bi[0x0026681B]) == 0x00265FF0
      and s(bs[0x0026601F]) == "shr ecx, 5" and s(bs[0x00266025]) == "je 0x2663a3" and s(bs[0x0026602E]) == "je 0x26636a"
      and s(bs[0x00266034]) == "cmp ecx, 1" and s(bs[0x00266037]) == "jne 0x266484"
      and s(bs[0x002663AE]) == "and al, 0xb4" and s(bs[0x002663B0]) == "or al, 4" and s(bs[0x002663B7]) == "mov byte ptr [rbp + 0xe], al"
      and s(bs[0x002660D3]) == "and byte ptr [rbp + 0xe], 0xf5" and s(bs[0x002660DE]) == "or byte ptr [rbp + 0xe], 5"
      and s(bs[0x0026639B]) == "mov byte ptr [rbp + 8], al"
      and not any("+ 0xe]" in s(x) and x.operands[0].type == X86.X86_OP_MEM for a, x in bs.items() if 0x0026636A <= a < 0x002663A3))
check("F3 the idiom census finds the full clear (and 0xf0) at exactly two places, 002666F8 (initialiser) and 0026A033 "
      "(the writer)", [a for a, _, t in idi if t.endswith(", 0xf0")] == [0x002666F8, 0x0026A033])
# every low-nibble writer in the actor-record range, and what it can store
W = {0x002659B8: ("and byte ptr [rcx + 0xe], 0xf5", 0x002659BC, "or byte ptr [rcx + 0xe], 5"),
     0x00265ACA: ("and byte ptr [rbx + 0xe], 0xf1", 0x00265ACE, "or byte ptr [rbx + 0xe], r14b"),
     0x00267D28: ("and byte ptr [rbx + 0xe], 0xf4", 0x00267D2C, "or byte ptr [rbx + 0xe], 4")}
ok = True
for a, (t1, a2, t2) in W.items():
    bb = body(fn_of(a)); ok &= s(bb[a]) == t1 and s(bb[a2]) == t2
bb = body(0x00265A20)
ok &= s(bb[0x00265A99]) == "mov r14d, 1" and s(bb[0x00265A65]) == "mov r14d, r12d" and s(bb[0x00265A30]) == "xor r12d, r12d"
check("F8 three more nibble writers the record does not name: 002659A0 stores 5, 00267CC0 stores 4, and "
      "ActorSystem_BindBattleUnitsForEligibleRecords 00265A20 stores 1 for each record it binds (r14d = 1 at 00265A99, "
      "else 0 from 00265A65, OR-ed into a nibble cleared to bit 0)", ok and set(idi_a for idi_a, _, _ in idi) ==
      {0x002659B8, 0x00265ACA, 0x002660D3, 0x002666F8, 0x00267D28, 0x0026A033},
      "and-idiom sites: " + " ".join("%08X" % a for a, _, _ in idi))
c67 = rel_callers(0x00267CC0); c59 = rel_callers(0x002659A0)
check("F8 00267CC0 and 002659A0 are each called by the refresh and by one 8-byte adapter, 0034DA20 / 0034DD80, which "
      "the verb table holds at 01EF68E0 / 01EF6900 (the verb-adapter census names them npc_to_gimmick 0x048E and "
      "gimmick_to_npc 0x048F)", c67 == [0x00238DA0, 0x0034DA23] and c59 == [0x00238DD0, 0x0034DD83]
      and struct.unpack("<Q", raw(0x01EF68E0, 8))[0] == 0x0034DA20 and struct.unpack("<Q", raw(0x01EF6900, 8))[0] == 0x0034DD80,
      "%s / %s" % (["%08X" % a for a in c67], ["%08X" % a for a in c59]))
VAD = os.path.join(DB, "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "members", "scriptvm-verb-adapter-callbacks.tsv")
vad = [l.rstrip("\r\n").split("\t") for l in open(VAD, encoding="utf-8")]
check("F8 record: scriptvm-verb-adapter-callbacks.tsv rows 0034DA20 -> 048E npc_to_gimmick -> 00267CC0 and 0034DD80 -> "
      "048F gimmick_to_npc -> 002659A0", ["0034DA20", "0", "048E", "npc_to_gimmick", "result", "00267CC0"] in vad
      and ["0034DD80", "0", "048F", "gimmick_to_npc", "result", "002659A0"] in vad)

# =============================== data =================================================================================
sys.path.insert(0, os.path.join(DB, "FFXII TZA", "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
cwd = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "agent_flow", "tools"))  # the census imports vbfextract from a cwd-relative path (SWE2-AUDIT-SEM 2026-10-03)
import gen_req_channel_census as G  # noqa: E402
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x265: "setfreetargettype", 0x3005: "btlAtelSetUnitType", 0x48E: "npc_to_gimmick", 0x48F: "gimmick_to_npc"}
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
rows = []; seen = set(); total = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    pool = U32(sec, 0x4C); sname = {}
    for k in range(cnt):
        o = pool + U32(sec, diroff + 4 + k * 0x30)
        sname.setdefault(U32(sec, diroff + 4 + k * 0x30 + 8), sec[o:sec.find(b"\0", o)].decode("cp932", "replace"))
    st = sorted(sname); bounds = sorted(set(st) | {diroff, len(sec)})
    for start in st:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        ins, _ = G.decode(sec[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E): continue
            total += 1
            if imm not in WANT: continue
            key = (path, start + pc)
            if key in seen: continue
            seen.add(key)
            v = verbs.get(imm)
            need = (v[0] if v and v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
            args, stt = G.resolve_args(ins, j, need, verbs)
            a = args[0][1] if args else None
            rows.append((path, sname[start], start + pc, WANT[imm], stt, a))
gim = [r for r in rows if r[3] in ("npc_to_gimmick", "gimmick_to_npc")]
rows = [r for r in rows if r[3] not in ("npc_to_gimmick", "gimmick_to_npc")]
by = collections.Counter((r[3], r[5]) for r in rows)
EXP = {("btlAtelSetUnitType", 0): 59814, ("btlAtelSetUnitType", 1): 234, ("btlAtelSetUnitType", 2): 297,
       ("btlAtelSetUnitType", 3): 369, ("setfreetargettype", 1): 18, ("setfreetargettype", 3): 315,
       ("setfreetargettype", 4): 2340, ("setfreetargettype", 6): 45}
norm = {(k[0], int(k[1])): n for k, n in by.items() if k[1] is not None}
check("D1 CONTROL the decode reproduces sd160_census.out's eight (verb, argument) counts over every CALL-family site",
      norm == EXP and sum(by.values()) == 63432, "%d CALL-family sites, %r" % (total, dict(norm)))
lang = lambda p: p.split("/")[2]
fold = lambda p: "/".join(p.split("/")[:2] + p.split("/")[3:])
langs = sorted({lang(r[0]) for r in rows})
perlang = collections.defaultdict(collections.Counter)
for r in rows:
    perlang[lang(r[0])][(fold(r[0]), r[1], r[3], int(r[5]))] += 1
usd = collections.Counter()
for (fp, sc, vb, a), n in perlang["us"].items():
    usd[(vb, a)] += n
check("F4 every count in the record is nine language copies of one list: %d languages carry the same (file, script, verb, "
      "argument) multiset, so each count is 9 x the us count" % len(langs),
      len(langs) == 9 and all(perlang[l] == perlang["us"] for l in langs) and all(norm[k] == 9 * usd[k] for k in EXP),
      "us counts %r" % dict(usd))
MAP = {0: 1, 1: 5, 2: 3, 3: 4}
ty = lambda verb, a: MAP[int(a)] if verb == "btlAtelSetUnitType" else int(a)
tsite = collections.Counter(ty(r[3], r[5]) for r in rows)
check("D2 the producer's per-type sums reproduce: 1 = 59,832, 3 = 612, 4 = 2,709, 5 = 234, 6 = 45; nothing for 0, 2, 7",
      dict(tsite) == {1: 59832, 3: 612, 4: 2709, 5: 234, 6: 45})
# the btlAtelSetUnitType(3) monsters: does the same (file, script) also set 0?
us = [r for r in rows if lang(r[0]) == "us"]
per = collections.defaultdict(set)
for r in us:
    per[(r[0], r[1])].add((r[3], int(r[5])))
m3 = {k: v for k, v in per.items() if ("btlAtelSetUnitType", 3) in v}
both = {k for k, v in m3.items() if ("btlAtelSetUnitType", 0) in v}
mon = {k for k in m3 if not k[1].startswith(("たからば",))}
check("F5 the type-4 'monsters': in the us copy, %d (file, script) pairs call btlAtelSetUnitType(3); %d of them also call "
      "btlAtelSetUnitType(0) in the same script, so the script switches the unit's mode between 4 and 1"
      % (len(m3), len(both)), len(m3) > 0 and len(both) > 0,
      "; ".join(sorted("%s:%s%s" % (k[0].split("/")[-1], k[1], "*" if k in both else "") for k in m3)))
d3 = [r for r in us if r[1].startswith("disp_tama")]
check("F6 type 3's largest group is five disp_tama scripts (35 distinct sites, 315 with copies) in seven rbl zones; "
      "they are set by setfreetargettype(3) only", len(d3) == 35 and {r[3] for r in d3} == {"setfreetargettype"},
      "%d us sites" % len(d3))
six = sorted({(r[0].split("/")[-1], r[1]) for r in us if r[3] == "setfreetargettype" and int(r[5]) == 6})
one = sorted({(r[0].split("/")[-1], r[1]) for r in us if r[3] == "setfreetargettype" and int(r[5]) == 1})
check("F7 type 6 is set in three scripts, two with the STAY_ prefix; BOSS_D-wall also passes 1 to the same verb",
      len({x[1] for x in six}) == 3 and sum(1 for x in {y[1] for y in six} if x.startswith("STAY_")) == 2
      and {x[1] for x in one} <= {x[1] for x in six},
      "6: %s ; 1: %s" % (six, one))

gu = [r for r in gim if lang(r[0]) == "us"]
gc = collections.Counter(r[3] for r in gu)
gs = collections.Counter((r[3], r[1]) for r in gu)
check("F9 CONTROL the kit's verb catalogue names the four ids: 0x265 setfreetargettype, 0x3005 btlAtelSetUnitType, "
      "0x48E npc_to_gimmick, 0x48F gimmick_to_npc (the last two take no argument)",
      [verbs[k][2] for k in (0x265, 0x3005, 0x48E, 0x48F)] == ["setfreetargettype", "btlAtelSetUnitType", "npc_to_gimmick",
      "gimmick_to_npc"] and verbs[0x48E][0] == 0 and verbs[0x48F][0] == 0)
check("F9 the two verbs the record leaves out are authored: in the us copy npc_to_gimmick (-> type 4) has %d sites and "
      "gimmick_to_npc (-> type 5) %d; scripts: %s" % (gc["npc_to_gimmick"], gc["gimmick_to_npc"],
      "; ".join("%s %s x%d" % (k[0], k[1], n) for k, n in gs.most_common(12))), sum(gc.values()) > 0)

print("FAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
