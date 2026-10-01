# image_address_base_writer_bounds.py - what the image says about writers of the image-address base 01F83530.
#
# Separates two questions the database had merged:
#   INITIALISED  - the value the image gives the cell at load (section bounds: raw-backed or virtual tail).
#   WRITABLE     - which in-image routes could store to it later, each swept with a KNOWN-POSITIVE control.
# Routes swept (listed function bodies, capstone, whole .text of every entry in functions.tsv):
#   R1 rip-relative operands resolving into [BASE-0x100, BASE+0x100): mnemonic, width, read/write by
#      operand position (never capstone's op.access - wrong for movups stores in this build).
#   R2 address materialisation of the same window: rip `lea`, `mov r, imm` / `mov r, imm64`.
#   R3 the address as data: 64-bit VA, 32-bit VA and 32-bit RVA in every section's raw bytes.
#   R4 the adjacent objects whose address IS taken nearby: 01F83460 below (stores at +0xC0..+0xDF over its
#      users, ctor, dtor, vtable slots and compiland) and 01F83580 above (stores at a negative displacement
#      or through an index register over the functions that take its address). An indexed store is a
#      ROUTE, not a verdict: whether its index can go negative is read by hand (see the owning page).
#   R5 bulk writers: memset / memcpy / memcpy_s / memmove / wmemset calls and rep stos / rep movs whose
#      destination resolves (straight-line backward scan) to a static address, with the length.
# NOT swept, and therefore NOT excluded: stores through a register whose value is computed from an
# unrelated base (pointer arithmetic, heap/stack aliases), bulk writes with an unresolved destination,
# code outside this executable (CRT/Phyre DLLs, the OS, injected modules). A zero on R1-R5 is a fact
# about R1-R5 only.
# Usage: python image_address_base_writer_bounds.py [--exe PATH] [--funcs functions.tsv] [--out JSON]
import sys, struct, json, argparse, pathlib, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP

HERE = pathlib.Path(__file__).resolve()
WORK = HERE.parents[3] / "Tools" / "work"
BASE_VA = 0x120000
TARGET = 0x01F83530
NONWRITE = {"cmp", "test", "bt", "push", "lea", "nop", "call", "jmp", "ucomiss", "ucomisd", "comiss", "comisd",
            "prefetch", "prefetchw", "prefetcht0", "prefetcht1", "prefetcht2", "prefetchnta"}
BLOCKNAMES = ("memset", "memcpy", "memcpy_s", "memmove", "memmove_s", "wmemset")
REGS = {"rcx": ("rcx", "ecx"), "rdi": ("rdi", "edi"), "r8": ("r8", "r8d"), "rdx": ("rdx", "edx")}


class Image:
    def __init__(self, exe):
        self.d = open(exe, "rb").read()
        d = self.d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        n = struct.unpack_from("<H", d, pe + 6)[0]
        opt = struct.unpack_from("<H", d, pe + 20)[0]
        self.secs = []
        for i in range(n):
            o = pe + 24 + opt + i * 40
            name = d[o:o + 8].rstrip(b"\0").decode()
            vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
            self.secs.append((name, va, vs, rs, ro))

    def section_of(self, addr):
        r = addr - BASE_VA
        for s in self.secs:
            if s[1] <= r < s[1] + max(s[2], s[3]):
                return s
        return None

    def off(self, addr):
        s = self.section_of(addr)
        if not s or addr - BASE_VA - s[1] >= s[3]:
            return None
        return s[4] + addr - BASE_VA - s[1]


def load_funcs(path):
    funcs, names = {}, {}
    for line in open(path, encoding="utf-8", errors="replace"):
        p = line.rstrip("\n").split("\t")
        try:
            e = int(p[0], 16); size = int(p[2])
        except (ValueError, IndexError):
            continue
        funcs[e] = size; names[e] = p[1]
    return funcs, names


def decode_all(img, funcs, md):
    for f in sorted(funcs):
        o = img.off(f)
        if o is None or funcs[f] <= 0:
            continue
        yield f, list(md.disasm(img.d[o:o + funcs[f]], f))


def rip_target(x, op):
    return x.address + x.size + op.mem.disp


def is_write(x, i):
    return i == 0 and x.mnemonic not in NONWRITE


def backward(insns, i, reg):
    names = REGS[reg]
    for j in range(i - 1, max(-1, i - 25), -1):
        x = insns[j]
        if x.mnemonic == "call" or x.mnemonic.startswith("j") or x.mnemonic == "ret":
            return None
        if not x.operands:
            continue
        op0 = x.operands[0]
        if op0.type == X86_OP_REG and x.reg_name(op0.reg) in names:
            if x.mnemonic == "lea" and x.operands[1].type == X86_OP_MEM and x.operands[1].mem.base == X86_REG_RIP \
                    and x.operands[1].mem.index == 0:
                return rip_target(x, x.operands[1])
            if x.mnemonic == "mov" and x.operands[1].type == X86_OP_IMM:
                return x.operands[1].imm & 0xFFFFFFFFFFFFFFFF
            if x.mnemonic == "xor" and x.operands[1].type == X86_OP_REG and x.operands[1].reg == op0.reg:
                return 0
            return None
    return None


def replay_texture_bind(img, ids):
    """R6: original-code replay of 00210570 (GiSetTexture's bind) then 0020E600 (the resolver) - unmodified
    image bytes under Unicorn; returns, per id, the base qword after the bind and resolve(0x1234)."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RAX
    end = max(s[1] + max(s[2], s[3]) for s in img.secs)
    res = {}
    for i in ids:
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        mu.mem_map(BASE_VA, (end + 0xFFFF) & ~0xFFFF)
        for name, va, vs, rs, ro in img.secs:
            mu.mem_write(BASE_VA + va, img.d[ro:ro + min(vs, rs)])
        mu.mem_map(0x70000000, 0x10000); mu.mem_write(0x7000F000, struct.pack("<Q", 0x7000FF00))
        mu.mem_write(0x7000FF00, bytes([0xF4]))       # hlt at the return address
        for entry, regs in ((0x210570, {UC_X86_REG_RCX: i, UC_X86_REG_RDX: 0x0000000123456789, UC_X86_REG_R8: 0x77}),
                            (0x20E600, {UC_X86_REG_RCX: 0x1234})):
            mu.reg_write(UC_X86_REG_RSP, 0x7000F000)
            mu.mem_write(0x7000F000, struct.pack("<Q", 0x7000FF00))
            for r, v in regs.items():
                mu.reg_write(r, v)
            mu.emu_start(entry, 0x7000FF00, count=100)
        res[f"{i:04X}"] = {"base_after_bind": f"{struct.unpack('<Q', bytes(mu.mem_read(TARGET, 8)))[0]:016X}",
                           "resolve_0x1234": f"{mu.reg_read(UC_X86_REG_RAX):016X}"}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=str(WORK / "exe" / "FFXII_TZA.exe"))
    ap.add_argument("--funcs", default=str(WORK / "graph" / "functions.tsv"))
    ap.add_argument("--out", default=str(HERE.with_suffix(".json")))
    a = ap.parse_args()
    img = Image(a.exe)
    funcs, names = load_funcs(a.funcs)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    out = {"target": f"{TARGET:08X}", "routes": {}, "controls": {}}

    s = img.section_of(TARGET)
    rel = TARGET - BASE_VA - s[1]
    out["initialised"] = {"section": s[0], "offset_in_section": hex(rel), "raw_size": hex(s[3]),
                          "virtual_size": hex(s[2]), "raw_backed": rel < s[3],
                          "value_at_load": "zero (virtual tail of the section)" if rel >= s[3] else "raw bytes"}

    lo, hi = TARGET - 0x100, TARGET + 0x100
    ADJ_LO, ADJ_HI = 0x01F83460, 0x01F83580                   # the two neighbours whose address is taken
    r1, r2, adj_users, r5, ctl = [], [], {ADJ_LO: set(), ADJ_HI: set()}, [], {}
    blockfn = {e for e, n in names.items() if n in BLOCKNAMES}
    decoded = {}
    sites = static_sized = 0
    for f, insns in decode_all(img, funcs, md):
        decoded[f] = insns
        for i, x in enumerate(insns):
            for k, op in enumerate(x.operands):
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and op.mem.index == 0:
                    t = rip_target(x, op)
                    if x.mnemonic == "lea":
                        if lo <= t < hi:
                            r2.append([f"{f:08X}", f"{x.address:08X}", f"lea {x.op_str}", f"{t:08X}"])
                        if t in adj_users:
                            adj_users[t].add(f)
                    elif lo <= t < hi:
                        r1.append([f"{f:08X}", f"{x.address:08X}", x.mnemonic, op.size,
                                   "write" if is_write(x, k) else "read", f"{t:08X}"])
                if op.type == X86_OP_IMM and x.mnemonic == "mov" and lo <= (op.imm & 0xFFFFFFFFFFFFFFFF) < hi:
                    r2.append([f"{f:08X}", f"{x.address:08X}", f"mov {x.op_str}", f"{op.imm:08X}"])
            kind = None
            if x.mnemonic == "call" and x.op_str.startswith("0x") and int(x.op_str, 16) in blockfn:
                kind = names[int(x.op_str, 16)]; dreg, sreg, w = "rcx", ("rdx" if kind == "memcpy_s" else "r8"), 1
            elif x.mnemonic.startswith("rep") and ("stos" in x.mnemonic or "movs" in x.mnemonic):
                kind = x.mnemonic; dreg, sreg = "rdi", "rcx"
                w = {"b": 1, "w": 2, "d": 4, "q": 8}.get(x.mnemonic[-1], 1)
            if kind:
                sites += 1
                dst, n = backward(insns, i, dreg), backward(insns, i, sreg)
                if dst is not None and img.section_of(dst) and img.section_of(dst)[0] in (".data", ".bss"):
                    if n is not None:
                        static_sized += 1
                        r5.append([f"{f:08X}", f"{x.address:08X}", kind, f"{dst:08X}", n * w])
                    elif dst <= TARGET < dst + 0x100000:
                        r5.append([f"{f:08X}", f"{x.address:08X}", kind, f"{dst:08X}", None])
    out["routes"]["R1_rip_operands"] = r1
    out["routes"]["R2_address_materialisation"] = r2
    # R3: the address as data
    needles = {"va64": struct.pack("<Q", TARGET), "va32": struct.pack("<I", TARGET),
               "rva32": struct.pack("<I", TARGET - BASE_VA)}
    r3 = {}
    for k, nb in needles.items():
        hits = []
        for name, va, vs, rs, ro in img.secs:
            blob = img.d[ro:ro + rs]; p = blob.find(nb)
            while p != -1:
                if k != "va32" or p % 4 == 0:
                    hits.append(f"{name}+{p:#x}")
                p = blob.find(nb, p + 1)
        r3[k] = hits
    out["routes"]["R3_address_as_data"] = r3
    # R4: adjacent objects. Below (01F83460, the static ADL wrapper): every register-base store at
    # displacement 0xC0..0xDF over the functions that take its address, its constructor 0020D2F0, its
    # destructor 008A7360, its class's vtable slots (009064B8 x3) and its whole compiland 0020C600..0020E600.
    # A store at +0xD0.. through `this`, or at +0xC0.. through the `this+0x10` pointer handed to 0020E420,
    # would reach TARGET. Above (01F83580): stores at a NEGATIVE displacement through any register in the
    # functions that take that address.
    vt = img.off(0x009064B8)
    slots = [struct.unpack_from("<Q", img.d, vt + 8 * k)[0] for k in range(3)]
    adl_set = set(adj_users[ADJ_LO]) | {0x20D2F0, 0x8A7360} | set(slots) | {f for f in decoded if 0x20C600 <= f < 0x20E600}
    r4 = []
    for f in sorted(adl_set):
        for x in decoded.get(f, []):
            if x.operands and is_write(x, 0) and x.operands[0].type == X86_OP_MEM                     and x.operands[0].mem.base not in (0, X86_REG_RIP) and 0xC0 <= x.operands[0].mem.disp < 0xE0:
                r4.append(["01F83460", f"{f:08X}", f"{x.address:08X}", f"{x.mnemonic} {x.op_str}"])
    # Above: a store at a negative displacement, OR any INDEXED store (an index register can be negative -
    # a signed 16-bit index guarded only from above reaches below the table; 00210570 is exactly that).
    for f in sorted(adj_users[ADJ_HI]):
        for x in decoded.get(f, []):
            if x.operands and is_write(x, 0) and x.operands[0].type == X86_OP_MEM                     and x.operands[0].mem.base not in (0, X86_REG_RIP)                     and (x.operands[0].mem.disp < 0 or x.operands[0].mem.index != 0):
                r4.append(["01F83580", f"{f:08X}", f"{x.address:08X}", f"{x.mnemonic} {x.op_str}"])
    out["routes"]["R4_adjacent_object_users"] = {f"{b:08X}": sorted(f"{f:08X}" for f in fs) for b, fs in adj_users.items()}
    out["routes"]["R4_functions_scanned_for_01F83460"] = len(adl_set)
    out["routes"]["R4_stores_C0_to_DF_or_negative"] = r4
    covers = [r for r in r5 if r[4] is not None and int(r[3], 16) <= TARGET < int(r[3], 16) + r[4]]
    unsized = [r for r in r5 if r[4] is None]
    out["routes"]["R5_bulk"] = {"sites_decoded": sites, "static_destination_with_length": static_sized,
                                "covering_target": covers, "static_below_target_length_unresolved": unsized}
    # Controls, each a known positive for its route.
    ctl["R1_reads_found"] = sorted(r[1] for r in r1 if r[5] == f"{TARGET:08X}") == ["0020E602", "0020E620"]
    ctl["R1_detects_a_write"] = any(r[4] == "write" for r in r1)          # e.g. neighbour 01F83564 stores
    ctl["R2_detects_lea_of_neighbour"] = any(r[3] == f"{ADJ_LO:08X}" for r in r2) or bool(adj_users[ADJ_LO])
    ctl["R3_detects_a_stored_va"] = img.d.find(struct.pack("<Q", 0x0020CEF0)) != -1   # ADL vtable slot 0 is data
    probe = [r for r in r5 if r[4] is not None and int(r[3], 16) <= 0x01F81000 < int(r[3], 16) + r[4]]
    ctl["R5_covers_known_static_memset_01F80F90"] = bool(probe)
    ctor_store = any(x.address == 0x20D397 for x in decoded.get(0x20D2F0, []))
    ctl["R4_ctor_last_store_is_plus_C8"] = ctor_store
    ctl["R4_indexed_writer_00210570_found"] = any(r[1] == "00210570" for r in r4)
    r6 = replay_texture_bind(img, (0x0005, 0x3FFF, 0x4000, 0x8000, 0xFFFB, 0xFFFC))
    out["routes"]["R6_replay_00210570_then_0020E600"] = r6
    ctl["R6_in_range_id_leaves_base_zero"] = r6["3FFF"]["base_after_bind"] == "0" * 16
    out["controls"] = ctl
    json.dump(out, open(a.out, "w"), indent=1, sort_keys=True)
    print("initialised:", out["initialised"])
    for k, v in out["routes"].items():
        print(k, ":", v if not isinstance(v, list) or len(v) < 12 else f"{len(v)} rows")
    print("controls:", ctl)
    sys.exit(0 if all(ctl.values()) else 1)


if __name__ == "__main__":
    main()
