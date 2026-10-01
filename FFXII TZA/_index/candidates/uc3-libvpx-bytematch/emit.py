"""Emit scratchpad/uc3_blocks.tsv from cover_ext.pkl + asm_hits_ext.pkl + residue.pkl."""
import pickle, collections
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "uc3_blocks.tsv"
blocks, out = pickle.load(open(HERE / "cover_ext.pkl", "rb"))
hits = pickle.load(open(HERE / "asm_hits_ext.pkl", "rb"))
res = pickle.load(open(HERE / "residue.pkl", "rb"))
info = {}
for va, n, ob, ln, mk, chk in hits:
    info[(va, n)] = (ob, ln, mk, chk)

FAM = {
    "vp8__common__x86__copy_sse2": "VP8 block copy (vp8/common/x86/copy_sse2.asm)",
    "vp8__common__x86__idctllm_mmx": "VP8 inverse DCT 4x4 (vp8/common/x86/idctllm_mmx.asm)",
    "vp8__common__x86__idctllm_sse2": "VP8 dequant+inverse DCT (vp8/common/x86/idctllm_sse2.asm)",
    "vp8__common__x86__mfqe_sse2": "VP8 postproc MFQE (vp8/common/x86/mfqe_sse2.asm)",
    "vp8__common__x86__recon_mmx": "VP8 block copy (vp8/common/x86/recon_mmx.asm)",
    "vp8__common__x86__subpixel_mmx": "VP8 bilinear subpixel predict (vp8/common/x86/subpixel_mmx.asm)",
    "vp8__common__x86__vp8_loopfilter_mmx": "VP8 loop filter MMX (vp8/common/x86/vp8_loopfilter_mmx.asm)",
    "vpx_dsp__x86__intrapred_sse2": "vpx_dsp intra predictors (vpx_dsp/x86/intrapred_sse2.asm)",
    "vpx_dsp__x86__intrapred_ssse3": "vpx_dsp intra predictors (vpx_dsp/x86/intrapred_ssse3.asm)",
    "vpx_dsp__x86__inv_txfm_ssse3_x86_64": "vpx_dsp inverse transforms 8x8/32x32 (vpx_dsp/x86/inv_txfm_ssse3_x86_64.asm)",
    "vpx_dsp__x86__quantize_avx_x86_64": "vpx_dsp quantizer (vpx_dsp/x86/quantize_avx_x86_64.asm)",
    "vpx_dsp__x86__quantize_ssse3_x86_64": "vpx_dsp quantizer (vpx_dsp/x86/quantize_ssse3_x86_64.asm)",
    "vpx_dsp__x86__sad4d_sse2": "vpx_dsp SAD x4d (vpx_dsp/x86/sad4d_sse2.asm)",
    "vpx_dsp__x86__sad_sse2": "vpx_dsp SAD (vpx_dsp/x86/sad_sse2.asm)",
    "vpx_dsp__x86__sad_sse3": "vpx_dsp SAD x3 (vpx_dsp/x86/sad_sse3.asm)",
    "vpx_dsp__x86__sad_sse4": "vpx_dsp SAD x8 (vpx_dsp/x86/sad_sse4.asm)",
    "vpx_dsp__x86__sad_ssse3": "vpx_dsp SAD x3 (vpx_dsp/x86/sad_ssse3.asm)",
    "vpx_dsp__x86__subpel_variance_sse2": "vpx_dsp sub-pixel variance (vpx_dsp/x86/subpel_variance_sse2.asm)",
    "vpx_dsp__x86__vpx_subpixel_8t_sse2": "vpx_dsp 8-tap convolve (vpx_dsp/x86/vpx_subpixel_8t_sse2.asm)",
    "vpx_dsp__x86__vpx_subpixel_8t_ssse3": "vpx_dsp 8-tap convolve (vpx_dsp/x86/vpx_subpixel_8t_ssse3.asm)",
    "vpx_dsp__x86__vpx_subpixel_bilinear_sse2": "vpx_dsp bilinear convolve (vpx_dsp/x86/vpx_subpixel_bilinear_sse2.asm)",
    "vpx_dsp__x86__vpx_subpixel_bilinear_ssse3": "vpx_dsp bilinear convolve (vpx_dsp/x86/vpx_subpixel_bilinear_ssse3.asm)",
    "vpx_ports__emms": "vpx_ports x87 control word helpers (vpx_ports/emms.asm)",
}
OPUS = {0x0014B690: "vp8_mbloop_filter_vertical_edge_mmx", 0x0014C4E6: "vp8_idct_dequant_dc_full_2x_sse2",
        0x0014B1D0: "vp8_loop_filter_horizontal_edge_mmx", 0x00129640: "vp8_short_idct4x4llm_mmx",
        0x001482A2: "vp8_copy_mem16x16_mmx", 0x00148584: "vp8_bilinear_predict8x8_mmx",
        0x0014DBD0: "vpx_dsp SSSE3 8-tap filter_block1d16", 0x00125770: "vp8_copy32xn_sse2",
        0x00129BE5: "vpx_sad4x4x3_sse3", 0x00148F41: "dc 32x32 predictor", 0x001492FF: "h 32x32 predictor",
        0x0014D080: "(unnamed, 0.847)"}
NOTLIB = {
    0x00121E11: ("none (not libvpx)", "game code: operand byte of a listed Audio function",
                 "the single byte FE is the second byte of `jmp $` (EB FE) at 00121E10, whose first byte is the last byte of listed body 00121DB0 (FUN_00121db0, owner Audio, body_bytes 97 ends at 00121E11); no libvpx routine covers it; exact-match scan finds nothing here"),
    0x00124BFB: ("none (not libvpx)", "data: inline jump table of a listed Audio function",
                 "one 90 pad byte then 7 dwords 00004A90 00004A61 00004A78 00004AB5 00004AF1 00004B16 00004B3C = image-base RVAs into 001249D0 (FUN_001249d0, owner Audio), as the admissions tsv's `table` verdict says; no libvpx routine covers it"),
    0x0015AE4A: ("none (not libvpx)", "game code: MSVC epilogue tail of a listed function",
                 "pop r14; pop r13; pop r12; pop rdi; ret - the tail of listed body 0015AC50 (FUN_0015ac50, tag Platform.Windows.DynamicLoaderRegistrySupport, body_bytes 506 ends at 0015AE4A): its prologue pushes rdi,r12,r13,r14,r15 and its body ends with pop r15 at 0015AE48; MSVC frame (mov [rsp+8],rbx ...), not a yasm routine; no libvpx routine covers it"),
}
counts = collections.Counter()
rows = []
for a, s in blocks:
    if a in NOTLIB:
        r, f, e = NOTLIB[a]
        rows.append(("%08X" % a, str(s), r, f, e, "high"))
        counts["not libvpx"] += 1
        continue
    ins = sorted(out[a]["inside"])
    # drop vp9 twin names when a vp8 twin sits at the same VA
    vas = collections.defaultdict(list)
    for va, n, ln, k in ins:
        vas[va].append((n, ln))
    names, fams, twins = [], [], []
    rod_eq = rod_ne = 0
    ext = set()
    for va in sorted(vas):
        lst = vas[va]
        if len(lst) > 1:
            keep = [x for x in lst if x[0].startswith("vp8_")] or lst[:1]
            twins += [x[0] for x in lst if x not in keep]
            lst = keep
        n, ln = lst[0]
        ob, _, mk, chk = info[(va, n)]
        tag = ""
        if va < a:
            tag = " [tail; entry %08X in the preceding block/body]" % va
        elif va + ln > a + s:
            tag = " [head; continues past block end]"
        if va < a and va + ln > a + s:
            tag = " [middle fragment; entry %08X]" % va
        names.append("%s @%08X %dB%s" % (n, va, ln, tag))
        fams.append(FAM.get(ob, ob))
        for t, sec, eq in chk:
            if sec.startswith("ext:"):
                ext.add("%s->%08X" % (sec[4:], t))
            elif eq:
                rod_eq += 1
            else:
                rod_ne += 1
    pad = sum(len(b) for va, b in res[a])
    covered = out[a]["covered"]
    fam = "; ".join(dict.fromkeys(fams))
    ev = ("exact byte match (relocation bytes masked) of yasm 1.3.0 -f win64 assembly of libvpx v1.6.0; %d routine(s); covered %d of %d B, the other %d B are multi-byte NOP alignment padding (score 100%% of non-padding bytes); "
          "%d rip-relative constant refs resolve into image .rodata 03001000.. and equal the obj .rodata bytes (%d differ)" % (len(names), covered, s, pad, rod_eq, rod_ne))
    if ext:
        ev += "; external refs " + ", ".join(sorted(ext))
        if any("vp8_bilinear_filters_x86_8" in x for x in ext):
            ev += " (01CDC060 holds vp8_bilinear_filters_x86_8 exactly as in vp8/common/x86/filter_x86.c)"
    if twins:
        ev += "; byte-identical twin(s) %s also match - vp8_ name kept because the image has only the VP8 decoder banner and no vp9 string" % ", ".join(twins)
    if a in OPUS:
        ev += ("; OPUS mnemonic-run match was '%s' - agrees" % OPUS[a]) if len(names) == 1 else ("; OPUS mnemonic-run match was '%s' - consistent, this adds the other routines in the block" % OPUS[a])
    conf = "high" if not twins else "high (bytes); vp8-vs-vp9 twin name medium"
    rows.append(("%08X" % a, str(s), " | ".join(names), fam, ev, conf))
    counts["identified"] += 1
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("block\tsize\troutine\tfamily\tevidence\tconfidence\n")
    for r in rows:
        assert all("\t" not in c for c in r)
        f.write("\t".join(r) + "\n")
print(counts, len(rows))
