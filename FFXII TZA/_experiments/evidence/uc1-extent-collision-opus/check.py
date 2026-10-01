"""UC-1 extent collision - OPUS adjudication of 007EE7C0 against the listed 007EE7F0.

Question: is the listed 9-byte FUN_007ee7f0 a deliberate alternate entry, or a false entry
that the function list invented inside the body that really starts at 007EE7C0?

Discriminators (fixed before the run):
  D1  instruction extent - does the reachable path from 007EE7C0 own an instruction that
      *covers* 007EE7F0 (entry inside an instruction), and what is the complete extent?
  D2  producers - does ANY image-level producer name 007EE7F0: rel8/rel32 branch or call,
      RIP-relative operand, DIR64 relocation, absolute qword, image-relative dword,
      .pdata begin, export?  A deliberate alternate entry needs one; a false entry has none.
  Controls: the same scan must find the known LEA 007EC4F1 -> 007EE7C0 and the .pdata
  begins of the listed neighbours 007EE730 / 007EE800; a planted rel32 call to 007EE7F0
  (mutant) must be found; the 48-byte extent must be rejected and the 57-byte one accepted.
  D3  the 007C2A29 tail - instruction bytes vs inline data inside the predecessor's extent.

Wrong interpretations this rejects (the regression):
  W1  "007EE7C0 is a 48-byte body" (ends inside the 7-byte store at 007EE7EF).
  W2  "007EE7F0 is an independent/alternate entry" (it starts inside that store and has no producer).
  W3  "all 47 bytes at 007C2A29 are executable tail" (6 code + 1 pad + 40 table bytes).

Static only; no execution, no live game.  Exit status 0 = every assertion held.
"""
import hashlib, json, struct, sys, pathlib
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, __version__ as CSV

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parents[2]                      # .../FFXII TZA
EXE = DB.parent / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
FUNCS = DB.parent / "Tools" / "work" / "graph" / "functions.tsv"
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXE_SHA, "wrong executable"
pe = pefile.PE(data=raw)
IB = pe.OPTIONAL_HEADER.ImageBase           # DB addresses are VAs at this base (0x120000)
md = Cs(CS_ARCH_X86, CS_MODE_64)

def at(va, n, buf=raw):
    o = pe.get_offset_from_rva(va - IB)
    return buf[o:o + n]

text = next(s for s in pe.sections if s.Name.startswith(b".text"))
T_VA = IB + text.VirtualAddress
T_OFF = text.PointerToRawData
T_LEN = min(text.Misc_VirtualSize, text.SizeOfRawData)

def producers(targets, buf):
    """Every image-level producer of each target VA, scanned over the whole image."""
    hits = {t: [] for t in targets}
    tb = buf[T_OFF:T_OFF + T_LEN]
    for p in range(len(tb) - 6):
        va = T_VA + p
        b = tb[p]
        if b in (0xE8, 0xE9):
            t = va + 5 + struct.unpack_from("<i", tb, p + 1)[0]
            if t in hits: hits[t].append(("rel32", va))
        elif b == 0x0F and 0x80 <= tb[p + 1] <= 0x8F:
            t = va + 6 + struct.unpack_from("<i", tb, p + 2)[0]
            if t in hits: hits[t].append(("jcc32", va))
        if b == 0xEB or 0x70 <= b <= 0x7F:
            t = va + 2 + struct.unpack_from("<b", tb, p + 1)[0]
            if t in hits: hits[t].append(("rel8", va))
        # RIP-relative operand: ModRM mod=00 rm=101, disp32 follows; immediates of 0/1/4 bytes
        if (b & 0xC7) == 0x05:
            d = struct.unpack_from("<i", tb, p + 1)[0]
            for imm in (0, 1, 4):
                t = va + 5 + imm + d
                if t in hits: hits[t].append(("riprel-modrm", va))
    relocs = {}
    for blk in getattr(pe, "DIRECTORY_ENTRY_BASERELOC", []):
        for e in blk.entries:
            if e.type == 10:
                relocs.setdefault(struct.unpack_from("<Q", buf, pe.get_offset_from_rva(e.rva))[0], []).append(e.rva)
    for t in targets:
        for r in relocs.get(t, []): hits[t].append(("dir64", IB + r))
        for pat, kind in ((struct.pack("<Q", t), "abs-qword"), (struct.pack("<I", t - IB), "rva-dword")):
            i = buf.find(pat)
            while i != -1:
                hits[t].append((kind, IB + pe.get_rva_from_offset(i))); i = buf.find(pat, i + 1)
    for rf in pe.DIRECTORY_ENTRY_EXCEPTION:
        b, e = IB + rf.struct.BeginAddress, IB + rf.struct.EndAddress
        if b in hits: hits[b].append(("pdata-begin", b))
        for t in targets:
            if b < t < e: hits[t].append(("inside-pdata", b))
    for ex in getattr(getattr(pe, "DIRECTORY_ENTRY_EXPORT", None), "symbols", []):
        if IB + ex.address in hits: hits[IB + ex.address].append(("export", IB + ex.address))
    return hits

def flow(start, n):
    """Reachable-instruction walk inside [start, start+n): calls return, external branches exit."""
    code = at(start, n + 16)
    seen, pending, problems, exits, boundaries = set(), [start], [], [], {}
    while pending:
        a = pending.pop()
        if a in seen: continue
        if not (start <= a < start + n): problems.append("reach outside %X" % a); continue
        ins = next(md.disasm(code[a - start:], a), None)
        if ins is None: problems.append("undecodable %X" % a); continue
        seen.add(a); boundaries[a] = ins.size
        if a + ins.size > start + n: problems.append("insn %X len %d ends past extent" % (a, ins.size))
        if ins.mnemonic in ("ret", "int3"): exits.append(hex(a)); continue
        if ins.mnemonic.startswith("j"):
            try: tgt = int(ins.op_str, 16)
            except ValueError: exits.append(hex(a)); continue
            if start <= tgt < start + n: pending.append(tgt)
            else: exits.append("ext %X" % tgt)
            if ins.mnemonic == "jmp": continue
        pending.append(a + ins.size)
    return {"problems": problems, "exits": exits,
            "boundaries": {"%08X" % k: v for k, v in sorted(boundaries.items())}}

R = {"exe_sha256": EXE_SHA, "imagebase": hex(IB), "capstone": CSV}
C0, F0, EF = 0x7EE7C0, 0x7EE7F0, 0x7EE7EF

# ---- D1: extent -----------------------------------------------------------------------
f48, f57 = flow(C0, 48), flow(C0, 57)
R["flow_48"], R["flow_57"] = f48, f57
assert f48["problems"], "W1 not rejected: 48 B must fail"
assert not f57["problems"], "57 B must be complete: %s" % f57["problems"]
assert f57["boundaries"].get("%08X" % EF) == 7, "store at 007EE7EF must be a 7-byte reachable instruction"
assert EF < F0 < EF + 7, "listed entry must lie inside that instruction"
assert "%08X" % F0 not in f57["boundaries"], "007EE7F0 must not be a reachable boundary"
assert len(f57["exits"]) == 3 and all(e.startswith("0x") for e in f57["exits"]), f57["exits"]
R["store_bytes"] = at(EF, 7).hex()
R["decode_as_listed"] = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in md.disasm(at(F0, 9), F0)]
R["decode_as_reached"] = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in md.disasm(at(EF, 10), EF)]
assert R["store_bytes"] == "41898938010000"
R["preceding_padding_before_C0"] = at(0x7EE7BE, 2).hex()   # cc cc after 007EE730's ret
assert R["preceding_padding_before_C0"] == "cccc"

# ---- D2: producers --------------------------------------------------------------------
T = {C0: "candidate", F0: "listed 9B", 0x7EE730: "predecessor", 0x7EE800: "successor", EF: "store"}
H = producers(T, raw)
R["producers"] = {"%08X" % t: [(k, "%08X" % s) for k, s in H[t]] for t in T}
assert H[F0] == [], "W2: 007EE7F0 has a producer: %s" % H[F0]
assert H[EF] == []
assert ("riprel-modrm", 0x7EC4F3) in H[C0], "control: the LEA at 007EC4F1 -> 007EE7C0 must be found"
assert ("pdata-begin", 0x7EE730) in H[0x7EE730] and ("pdata-begin", 0x7EE800) in H[0x7EE800]
# The only non-LEA hit on C0 is a coincidental .rdata value inside a 16-slot run none of
# whose other 15 values is a listed entry; record it rather than hide it.
other = [h for h in H[C0] if h[0] != "riprel-modrm"]
assert other == [("rva-dword", 0xD8A838)], other
listed = {int(l.split("\t")[0], 16) for l in FUNCS.read_text(encoding="utf-8").splitlines()[1:]}
run = [struct.unpack_from("<I", at(0xD8A800 + 8 * k, 4))[0] + IB for k in range(16)]
R["rdata_run_D8A800"] = ["%08X" % v for v in run]
assert sum(v in listed for v in run) == 0, "the .rdata run would be a code table if its values were entries"
assert F0 in listed, "precondition: 007EE7F0 is listed"
# Mutant: plant a rel32 call to 007EE7F0 in a padding hole of a copy -> the scan must see it
mut = bytearray(raw)
hole = 0x7EE7F9                                             # cc padding after the ret
o = pe.get_offset_from_rva(hole - IB)
mut[o:o + 5] = b"\xE8" + struct.pack("<i", F0 - (hole + 5))
HM = producers({F0: "mutant"}, bytes(mut))
assert ("rel32", hole) in HM[F0], "mutant: planted call not detected"
R["mutant_planted_call_detected"] = True

# ---- D3: the 007C2A29 tail ------------------------------------------------------------
P, TAIL = 0x7C23C0, 0x7C2A29
insns = list(md.disasm(at(TAIL, 7), TAIL))
R["tail_code"] = ["%08X %s %s %s" % (i.address, i.bytes.hex(), i.mnemonic, i.op_str) for i in insns]
assert [i.mnemonic for i in insns[:3]] == ["call", "int3", "nop"] and insns[0].op_str == "0x809728"
table = [struct.unpack_from("<I", at(0x7C2A30 + 4 * k, 4))[0] + IB for k in range(10)]
R["tail_table"] = ["%08X" % v for v in table]
assert all(P <= v < TAIL for v in table), "every table entry targets the predecessor"
user = next(i for i in md.disasm(at(P, TAIL - P), P) if "0x6a2a30" in i.op_str)
R["table_user"] = "%08X %s %s" % (user.address, user.mnemonic, user.op_str)
assert user.address == 0x7C27F2
chain = [(IB + r.struct.BeginAddress, IB + r.struct.EndAddress) for r in pe.DIRECTORY_ENTRY_EXCEPTION
         if P <= IB + r.struct.BeginAddress < 0x7C2A60]
R["pdata_chain_7C23C0"] = ["%08X-%08X" % c for c in chain]
assert chain[0][0] == P and chain[-1][1] == 0x7C2A58, "native unwind extent ends after the table"
assert at(0x7C2A58, 8) == b"\xcc" * 8
R["tail_split"] = {"code": "007C2A29-007C2A2F (6 B: call __report_rangecheckfailure; int3)",
                   "pad": "007C2A2F (1 B nop)", "inline_data": "007C2A30-007C2A58 (40 B, 10 image-relative dwords)",
                   "native_extent_end": "007C2A58 (.pdata chain)"}

out = HERE / "result.json"
out.write_text(json.dumps(R, indent=1), encoding="utf-8")
print("OK  W1 rejected (48 B ends inside 007EE7EF store), 57 B complete, 3 ret exits")
print("OK  W2 rejected: 007EE7F0 inside a reachable instruction, 0 producers; controls C0-LEA, 730/800 pdata, mutant found")
print("OK  W3 rejected: 007C2A29 = 6 B code + 1 B pad + 40 B table (user 007C27F2), pdata end 007C2A58")
print("result", out.name, hashlib.sha256(out.read_bytes()).hexdigest())
