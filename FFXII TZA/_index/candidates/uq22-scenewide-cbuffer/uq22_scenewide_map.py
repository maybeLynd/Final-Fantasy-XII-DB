"""UQ-22: which SceneWideParameterConstantBuffer variable each console tunable becomes (OPUS, 2026-09-27).

Chain, each link read from bytes or shipped data:
  L1 006084B0 (only caller 00604750) stages the tunables block 02CB7FD0 whole into a CPU snapshot at its rcx
     (00604750's rbp+0x270): block +0x000..+0x0CF -> snap +0x110.., +0x0D0..+0x18F -> snap +0x1E0.., +0x190.. -> snap
     +0x2A0 via 005DEC50 (lea rdx, [rip -> 02CB8160]).
  L2 00604750 then writes the GPU-layout buffer through r14, one field at a time, from that snapshot. This driver maps
     every `store [r14 + X]` back to the `load [rbp + Y]` that fed its register, with a straight-line register
     tracker: a register's source is killed by any other write to it. A store whose register came from arithmetic is
     reported as COMPUTED, not mapped.
  L3 the layout the store offsets land in is the compiled SceneWideParameterConstantBuffer of the shipped shaders:
     one layout (0x5F0 B, 154 variables) in every phyrechrshader.fx / phyredefaultlitshader.fx blob that declares
     it (RDEF chunk of each DXBC), and the exe's semantic table binds that name to parameter type 0x13 / data type
     0x34.
Output: map.tsv (block offset, tunable address, snapshot offset, cbuffer offset, HLSL variable) and result.json.
Controls: K1 the shadow matrices (block +0x190.., snap +0x2A0..) must land on mShadowCascadeProjection0..7;
          K2 the loader-keyed chrFresnelSpecular* (block +0xD0..+0xDC) must land on the same-named HLSL variables;
          K3 no two stores disagree about one cbuffer offset;
          K4 every one of UQ-22's 80 (console-tunables-consumers.tsv, in-block +0x000..+0x18F, no outside reader) maps.
"""
import json, os, struct, sys, collections, pathlib
sys.path.insert(0, r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
import check_default_instance_writers as W  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_REG  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract"
BLOCK, SNAP = 0x02CB7FD0, 0x270
FN = 0x00604750


def cstr(b, o):
    return b[o:b.index(b"\0", o)].decode("latin1")


def rdef(blob):
    n = struct.unpack_from("<I", blob, 28)[0]
    for k in range(n):
        co = struct.unpack_from("<I", blob, 32 + 4 * k)[0]
        if blob[co:co + 4] == b"RDEF":
            r = blob[co + 8:co + 8 + struct.unpack_from("<I", blob, co + 4)[0]]
            cbn, cbo, _bn, _bo, ver, _pt, _fl, _cr = struct.unpack_from("<IIIIHHII", r, 0)
            vsz = 40 if (ver >> 8) & 0xFF >= 5 else 24
            for c in range(cbn):
                nm, vc, vo, sz, _cf, _ct = struct.unpack_from("<6I", r, cbo + 24 * c)
                yield cstr(r, nm), sz, [(cstr(r, struct.unpack_from("<I", r, vo + vsz * v)[0]),
                                         struct.unpack_from("<I", r, vo + vsz * v + 4)[0],
                                         struct.unpack_from("<I", r, vo + vsz * v + 8)[0]) for v in range(vc)]


def layouts():
    lay = {}; count = collections.Counter(); files = collections.defaultdict(set)
    for dp, _dn, fn in os.walk(ROOT):
        for f in fn:
            if not f.endswith(".phyre"):
                continue
            b = open(os.path.join(dp, f), "rb").read()
            if b"SceneWideParameterConstantBuffer" not in b:
                continue
            i = 0
            while True:
                i = b.find(b"DXBC", i)
                if i < 0:
                    break
                try:
                    tot = struct.unpack_from("<I", b, i + 24)[0]
                    for nm, sz, vs in rdef(b[i:i + tot]):
                        if nm == "SceneWideParameterConstantBuffer":
                            k = json.dumps([sz, vs]); lay[k] = (sz, vs); count[k] += 1; files[k].add(f.split("#")[0])
                except (struct.error, ValueError, IndexError):
                    pass
                i += 4
    return lay, count, files


def store_map(img):
    src = {}          # normalised register -> ("rbp", Y) or "COMPUTED"
    out = collections.defaultdict(set)
    for i in img.body(FN):
        ops = i.operands
        if len(ops) == 2 and ops[0].type == X86_OP_MEM and W.norm(ops[0].value.mem.base) == W.norm(W.capstone.x86.X86_REG_R14) \
                and not ops[0].value.mem.index and ops[1].type == X86_OP_REG:
            r = W.norm(ops[1].reg); s = src.get(r, "UNKNOWN"); width = ops[0].size or 4
            for k in range(0, width, 4):     # a wide store maps each of its dwords to the matching source dword
                out[ops[0].value.mem.disp + k].add(((s[0], s[1] + k) if isinstance(s, tuple) else s,
                                                    i.mnemonic, "%08X" % i.address))
            continue
        try:
            _rd, wr = i.regs_access()
        except Exception:
            wr = []
        if len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM and i.mnemonic in ("movss", "movsd", "mov", "movups", "movaps", "movq", "movd", "movzx", "movsx") \
                and W.norm(ops[1].value.mem.base) == W.norm(W.capstone.x86.X86_REG_RBP) and not ops[1].value.mem.index:
            src[W.norm(ops[0].reg)] = ("rbp", ops[1].value.mem.disp); continue
        if len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and i.mnemonic in ("movaps", "movups", "mov", "movss") \
                and W.norm(ops[1].reg) in src:
            src[W.norm(ops[0].reg)] = src[W.norm(ops[1].reg)]; continue
        for r in wr:
            src[W.norm(r)] = "COMPUTED"
    return out


def main():
    img = W.Image()
    lay, count, files = layouts()
    key = max(count, key=count.get); size, vs = lay[key]
    byoff = {}
    for n, o, s in vs:
        for k in range(0, s, 4):
            byoff[o + k] = (n, k)
    sm = store_map(img)
    rows = []; conflicts = []
    for x in sorted(sm):
        srcs = {s[0] for s in sm[x]}
        if len(srcs) > 1:
            conflicts.append("0x%X" % x)
        s = next(iter(srcs))
        name = byoff.get(x, ("(outside layout)", 0))
        if isinstance(s, tuple):
            snap = s[1] - SNAP; blk = snap - 0x110 if 0x110 <= snap < 0x110 + 0x470 else None
            # L1's block->snapshot copy is identity-offset (+0x110) over the whole block
            rows.append((x, name, snap, blk))
        else:
            rows.append((x, name, s, None))
    k1 = all(any(r[0] == 0x2F0 + 0x40 * m and r[3] == 0x190 + 0x40 * m for r in rows) for m in range(8))
    k2 = all(any(r[1][0] == n and r[3] == b for r in rows) for n, b in (("chrFresnelSpecularIntensity", 0xD0),
             ("chrFresnelSpecularPower", 0xD4), ("chrFresnelSpecularClampValue", 0xD8), ("chrFresnelSpecularSkinIntensity", 0xDC)))
    with open(HERE / "map.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("cbuffer_off\thlsl_variable\telement_byte\tsnapshot_off\tblock_off\ttunable_addr\n")
        for x, (n, k), snap, blk in rows:
            f.write("0x%03X\t%s\t%d\t%s\t%s\t%s\n" % (x, n, k, ("0x%03X" % snap) if isinstance(snap, int) else snap,
                    ("0x%03X" % blk) if blk is not None else "-", ("%08X" % (BLOCK + blk)) if blk is not None else "-"))
    mapped_block = sorted({r[3] for r in rows if r[3] is not None})
    # K4: UQ-22's population - the console-tunables table's in-block rows with no outside reader, +0x000..+0x18F
    import csv, io
    tsv = HERE.parents[2] / "00-Engine-Core-Runtime" / "Developer-Tuning-Console" / "members" / "console-tunables-consumers.tsv"
    body = "".join(l for l in open(tsv, encoding="utf-8") if not l.startswith("#"))
    pop = [r for r in csv.DictReader(io.StringIO(body), delimiter="\t")
           if r["outside_readers"].strip() in ("", "-") and 0 <= int(r["addr"], 16) - BLOCK < 0x190]
    got = {BLOCK + b for b in mapped_block}
    k4_unmapped = [r["addr"] for r in pop if int(r["addr"], 16) not in got]
    out = {"layouts": len(lay), "layout_blobs": count[key], "layout_files": sorted(files[key]), "cbuffer_size": size,
           "variables": len(vs), "r14_store_offsets": len(rows), "block_offsets_mapped": len(mapped_block),
           "computed_or_unknown": sum(1 for r in rows if not isinstance(r[2], int)),
           "K1_shadow_matrices": k1, "K2_chrFresnel": k2, "K3_conflicts": conflicts,
           "K4_population": len(pop), "K4_unmapped": k4_unmapped,
           "controls_pass": k1 and k2 and not conflicts and len(lay) == 1 and len(pop) == 80 and not k4_unmapped}
    (HERE / "result.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
