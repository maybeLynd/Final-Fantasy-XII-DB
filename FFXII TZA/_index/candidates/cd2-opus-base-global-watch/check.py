"""CD-2 (OPUS, 2026-09-26): does anything write the base global 01F83530? STATIC + NATIVE-REPLAY.
  C1 STATIC. 01F83530 lies in .data's zero-fill tail, past the raw backing, and starts at 0. The only instructions
     naming it are the reads at 0020E602 (`add rax, [01F83530]`) and 0020E620 (`sub ecx, [01F83530]`). The census
     decodes every rip-relative disp32 in .text at every candidate length. No DIR64 relocation points into
     01F83500-01F83560.
  C2 STATIC. The static object just below, AmdAdapterInfo at 01F83460 (vtable 009064B8, constructed by 0020D2F0 from
     the initialiser at 0015DC84, destroyed by 008A7360), is 0xD0 bytes, so it ends exactly at 01F83530. Its
     constructor zeroes +0x08..+0xCF with qword, dword and byte stores of a zero register; the only bytes it skips are
     +0x29..+0x2B, the padding between the byte at +0x28 and the dword at +0x2C. No displacement at or beyond 0xD0 off any base register appears in
     its constructor, destructor or three virtual slots; the one `lea rdx, [rax + 0x118]` in slot 1 is off a loaded
     record pointer, not `this`. So a member write of the neighbour cannot reach the global.
  C3 NATIVE-REPLAY. In the S-15 boot world, a write-watch on 01F83530..01F83537 and an entry hook on the texture-id
     writer 00210570 are armed before the CRT runs. Across the CRT tables, main, app slot 2, the init job, the save
     reset, UI message 16, two field-script binds and the field-pass frames: no write, 00210570 never entered, value 0
     at the end.
Scope: C3 covers what the boot world runs, not a whole play session. The undriven signed-index route through 00210570
(CD-2 / J-C) is untouched: it is not reached here. Writes result.json; exit 1 on any FAIL."""
import os, sys, re, struct, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[4]
import pefile, capstone
pe = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe")); img = pe.get_memory_mapped_image(); IB = 0x120000
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
T = 0x1F83530
cases = {}; res = {}
# ---- C1
ds = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".data"][0]
zero_fill = T - (ds.VirtualAddress + IB) >= ds.SizeOfRawData
refs = set()
for o in range(0x1000, 0x8C0000 - IB - 4):
    d = struct.unpack_from("<i", img, o)[0]
    for tail in range(0, 5):
        if o + 4 + tail + IB + d != T: continue
        for back in range(1, 6):
            ins = list(md.disasm(img[o - back:o - back + 16], o - back + IB))
            if ins and ins[0].size == back + 4 + tail and "rip" in ins[0].op_str:
                refs.add((ins[0].address, ins[0].mnemonic, ins[0].op_str))   # every consistent decoding; C1 keeps the on-stream ones
# keep only instructions that lie on the listed body's own instruction stream
def on_stream(a):
    for f0 in (0x20E600, 0x20E620):
        for i in md.disasm(img[f0 - IB:f0 - IB + 16], f0):
            if i.address == a: return True
    return False
real = sorted(r for r in refs if on_stream(r[0]))
relocs = []
for b in getattr(pe, "DIRECTORY_ENTRY_BASERELOC", []):
    for e in b.entries:
        if e.type == 10 and 0x1F83500 <= struct.unpack_from("<Q", img, e.rva)[0] < 0x1F83560: relocs.append(e.rva + IB)
res["C1"] = {"zero_fill": zero_fill, "initial": struct.unpack_from("<Q", img, T - IB)[0],
             "decoded_refs": ["%08X %s %s" % r for r in sorted(refs)], "on_instruction_stream": ["%08X %s %s" % r for r in real], "dir64": relocs}
cases["C1_zero_fill_initial_0_only_two_reads_no_store_no_reloc"] = zero_fill and res["C1"]["initial"] == 0 and not relocs and \
    [(a, m) for a, m, _ in real] == [(0x20E602, "add"), (0x20E620, "sub")]
# ---- C2
F = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = l.split("\t")
    try: F[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
ctor = list(md.disasm(img[0x20D2F0 - IB:0x20D2F0 - IB + F[0x20D2F0]], 0x20D2F0))
W = {"qword": 8, "dword": 4, "word": 2, "byte": 1}
covered = set()
for i in ctor[:40]:
    m = re.match(r"(qword|dword|word|byte) ptr \[rcx \+ (0x[0-9a-f]+|\d+)\], (rbp|ebp|bp|bpl)$", i.op_str)
    if m and i.mnemonic == "mov":
        o = int(m.group(2), 0); covered |= set(range(o, o + W[m.group(1)]))
zeroed = sorted(covered)
vt_install = any(i.mnemonic == "lea" and "0x6f918b" in i.op_str for i in ctor)
q = lambda a: struct.unpack_from("<Q", img, a - IB)[0]
slots = [q(0x9064B8 + 8 * k) for k in range(3)]
far = []
for f in [0x20D2F0, 0x8A7360] + slots:
    for i in md.disasm(img[f - IB:f - IB + F[f]], f):
        for m in re.finditer(r"\[(r[a-z0-9]+) \+ (0x[0-9a-f]+)\]", i.op_str):
            if m.group(1) not in ("rsp", "rbp", "rip") and int(m.group(2), 16) >= 0xD0: far.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
init_lea = [i for i in md.disasm(img[0x15DC80 - IB:0x15DC9B - IB], 0x15DC80) if i.mnemonic == "lea" and "0x1e257d5" in i.op_str]
res["C2"] = {"zeroed_bytes": "%#x..%#x (%d bytes)" % (min(zeroed), max(zeroed), len(zeroed)) if zeroed else None, "slots": ["%08X" % s for s in slots], "displacements_ge_0xD0": far}
cases["C2_the_neighbour_AmdAdapterInfo_ends_exactly_at_the_global"] = max(zeroed) == 0xCF and set(range(0x08, 0xD0)) - set(zeroed) == {0x29, 0x2A, 0x2B} and vt_install and bool(init_lea) \
    and far == ["0020CFDF lea rdx, [rax + 0x118]"] and 0x1F83460 + 0xD0 == T
# ---- C3
PKG = HERE.parent / "s15-opus-replay-boot-world"
sys.path.insert(0, str(PKG)); WDIR = PKG.parent / "s21-opus-replay-applier-stub-free"; sys.path.insert(0, str(WDIR))
_c = os.getcwd(); os.chdir(WDIR)
import world as W
os.chdir(_c)
from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RIP
W1, E1 = [], []
_orig = W.Session.__init__
def _init(self, *a, **k):
    _orig(self, *a, **k)
    self.uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a_, sz, v, _: W1.append(("%X" % u.reg_read(UC_X86_REG_RIP), "%X" % v, sz)), begin=T, end=T + 7)
    self.uc.hook_add(UC_HOOK_CODE, lambda u, a_, n, _: E1.append(1), begin=0x210570, end=0x210570)
W.Session.__init__ = _init
import world_boot as B
src = open(PKG / "check.py", encoding="utf-8").read()
src = src.replace('json.dump(res, open(os.path.join(HERE, "result.json"), "w")', 'json.dump(res, open(os.devnull, "w")').replace('sys.exit(0 if res["ok"] else 1)', "pass")
g = {"__file__": str(PKG / "check.py"), "__name__": "probe"}
exec(compile(src, "check.py", "exec"), g)
steps = [s["step"] for s in g["R"]["steps"]]
res["C3"] = {"writes": W1[:10], "write_count": len(W1), "value_at_end": B.q(T), "entered_00210570": len(E1), "boot_steps": len(steps), "world_ok": g["res"]["ok"]}
cases["C3_replay_no_write_00210570_never_entered_value_0"] = not W1 and not E1 and B.q(T) == 0 and g["res"]["ok"]
out = {"evidence": ["STATIC", "NATIVE-REPLAY"], "live_game": False, "results": res, "cases": cases, "ok": all(cases.values())}
json.dump(out, open(HERE / "result.json", "w"), indent=1, sort_keys=True)
print(json.dumps(res, indent=1, sort_keys=True))
for k, v in cases.items(): print("%-64s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
sys.exit(0 if out["ok"] else 1)
