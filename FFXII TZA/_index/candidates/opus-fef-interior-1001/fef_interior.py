"""fef_interior.py [--apply] - interior citations for the F-frontier functions that fef-and-motion-entries.md cited by
entry only (OPUS, 2026-10-01). All 36 read by hand from the certified image; every rip target was resolved with retool.py
and every float constant read from the image.

Verifies every anchor in the image (instruction boundary strictly inside the function's extent, recorded mnemonic) and
refuses a pipe in any sentence. Without --apply it only verifies; with --apply it appends one OPUS section
(byte-preserving, CRLF-aware, idempotent). Prints VERIFY, PATCHED / ALREADY / DRY, FAILS n."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "17-Presentation-Rendering", "Model-And-Motion-Formats", "fef-and-motion-entries.md")
ROWS = [
 ("0024D330", "returns 0 when qword `02F97340` points to a record whose byte `+0` is 3 and `003B33D0(word +4)` returns 0x34; otherwise 1", [("0024D336", "mov"), ("0024D347", "cmp"), ("0024D350", "call"), ("0024D35A", "cmove")]),
 ("0026BE90", "sets (when `edx` is non-zero) or clears bit `ecx mod 8` of byte `ecx/8` of the bit array at `0209A2A0` (signed division)", [("0026BEA3", "sar"), ("0026BEAE", "shl"), ("0026BEB0", "lea"), ("0026BEBF", "or"), ("0026BEC5", "and")]),
 ("002E7080", "tail-calls `0026BE90(0, 1)`, which sets bit 0 of `0209A2A0`", [("002E7085", "xor"), ("002E7087", "jmp")]),
 ("00325090", "for a non-null `rcx`: when `00263E30(rcx)` and its qword `+0x698` are non-null, and either (dword `+0x64` OR dword `+0x3C`) AND `0x80000003` is 0 or `00313F60()` is non-zero, calls `00319E40` on the `00263E30` result and returns 1; otherwise returns 0", [("0032509B", "call"), ("003250A8", "mov"), ("003250BA", "test"), ("003250CE", "call"), ("003250D3", "mov")]),
 ("0034B310", "when `0025C130(dword [r8])` is non-zero, calls `0026BE90([r8], 0)` and returns 0; otherwise returns 1", [("0034B31C", "call"), ("0034B329", "call"), ("0034B336", "mov")]),
 ("003AFC30", "for record `cl` of the 0x70-byte records at `02B3F570`, when its dword `+4` equals `ecx`: clears bits 0-1 of byte `+0x58`, zeroes word `+0x1C`, word `+0x54`, qword `+0x3C` and dword `+0x44`, and sets floats `+0x24` and `+0x28` to 1.0", [("003AFC33", "imul"), ("003AFC43", "cmp"), ("003AFC4F", "and"), ("003AFC57", "mov")]),
 ("003AFC80", "for record `cl` of the 0x70-byte records at `02B3F570`, when its dword `+4` equals `ecx`: clears bits 0-1 of byte `+0x58`, stores `0x11000000` in dword `+0x1C`, zeroes word `+0x54`, qword `+0x3C` and dword `+0x44`, and sets floats `+0x24`, `+0x28` and `+0x34` to 1.0", [("003AFC83", "imul"), ("003AFC93", "cmp"), ("003AFCA3", "mov"), ("003AFCC3", "mov")]),
 ("003B5CE0", "for record `cl` of the 0xE0-byte records at `[02B40528]`, when its dword `+0x10` equals `ecx`: copies dwords `+0x48`/`+0x4C` to `+0x30`/`+0x34` and word `+0x38` to `+0x3A`, stores `xmm2`/`xmm3` in floats `+0x48`/`+0x4C`, and sets word `+0x38` from word `+0x3C` when `edx` is 0, else from `+0x3E`", [("003B5CE4", "imul"), ("003B5CF2", "cmp"), ("003B5CFC", "mov"), ("003B5D12", "movss"), ("003B5D27", "mov")]),
 ("003DFF20", "for record `edx` (below word `+4` of the handle at dword `+0x2C`, resolved by `0020E600`) of the 0x60-byte records the handle's first dword resolves to: stores the difference float `+0xC` minus float `+8` in float `+0x14` and `r8d` times dword `01DFE0B4` in dword `+0x10`; when that product is non-zero, divides float `+0x14` by `r8d`, otherwise copies float `+0xC` to `+8`", [("003DFF51", "cmp"), ("003DFF7D", "subss"), ("003DFF8F", "imul"), ("003DFFA2", "divss"), ("003DFFBC", "movss")]),
 ("003E2D20", "when the handle at dword `+8` resolves (`0020E600`) and its byte `+6` differs from `dl`, stores `dl` there; then over the 0x60-byte records the handle's first dword resolves to (count byte `+4` of the handle): when the high nibble of the handle's byte `+5` is 0, zeroes each record's byte `+0x1C` and copies its dword `+0x50 + 4*dl` to `+8`; otherwise sets byte `+0x1C` to 6 times byte `01DFE0B4` and float `+0xC` to (float `+8` minus float `+0x50 + 4*dl`) times float `01DFE0BC` times 0.166667 (`00D117B0`)", [("003E2D68", "mov"), ("003E2D77", "test"), ("003E2DD0", "mov"), ("003E2DD8", "mov"), ("003E2E5F", "movss")]),
 ("003E2EA0", "when the handle at dword `+8` resolves (`0020E600`), copies consecutive dwords from `rdx + 4` into dword `+4` of each 0x60-byte record the handle's first dword resolves to (count byte `+4` of the handle)", [("003E2EC0", "add"), ("003E2EF1", "mov"), ("003E2EF7", "mov"), ("003E2F07", "movzx")]),
 ("00409190", "returns the sign-extended low dword of `rcx` plus an offset chosen by bits 0-1 and 24-25 of dword `+4`: with bits 0-1 = 0, 0x40 / 0x60 / 0xC0 for bits 24-25 = 0 / 1 / 2; with bits 0-1 = 1, 0x70 / 0x90 / (0xF0 when bit 12 is set, else 0xC0); 0 for any other combination", [("00409195", "and"), ("004091A1", "shr"), ("004091B3", "bt"), ("004091D5", "shr"), ("004091E7", "xor")]),
 ("00409710", "sets word `+0` to -1, zeroes dword `+4`, qword `+0x30` and dword `+0x40`, sets dword `+0x44` to -1, then tail-jumps to `0051EE10(rcx + 0x10)`", [("00409715", "mov"), ("0040971B", "mov"), ("00409722", "mov"), ("00409729", "jmp")]),
 ("00409930", "calls `00409780(rcx, rdx, r8, &out, &scratch)` with `out` in its own `r9` home slot and `scratch` on its stack, and returns the dword left in `out`", [("00409934", "lea"), ("00409939", "lea"), ("00409943", "call"), ("00409948", "mov")]),
 ("004173D0", "when dword `+0x35C` of `r8` is not -1, calls `003B6A90(that dword, byte +2 of rcx, &{float rcx+4, float rcx+8, 0.0, 1.0})`, the 1.0 read from `01CEBBA8`", [("004173EA", "cmp"), ("0041740A", "xorps"), ("00417413", "movss"), ("00417427", "call")]),
 ("00417440", "when dword `+0x35C` of `r8` is not -1, tail-calls `003B69B0(that dword, byte +2 of rcx)` with float `rcx+4` in `xmm2`", [("00417447", "cmp"), ("0041744C", "movss"), ("00417457", "jmp")]),
 ("00417460", "when dword `+0x35C` of `r8` is not -1, calls `003B6A10(that dword, byte +2 of rcx, &{float rcx+4, float rcx+8, 0.0, 1.0})`, the 1.0 read from `01CEBBA8`", [("0041747A", "cmp"), ("0041749A", "xorps"), ("004174A3", "movss"), ("004174B7", "call")]),
 ("004174D0", "when dword `+0x35C` of `r8` is not -1, tail-calls `003B6950(that dword, byte +2 of rcx)` with float `rcx+4` in `xmm2`", [("004174D7", "cmp"), ("004174DC", "movss"), ("004174E7", "jmp")]),
 ("00417A80", "when qword `+0x18` of `r8` equals `rdx`, sets bit 3 of dword `+0xC` of `r8`; otherwise copies word `+0x14` of `rdx` to `+0x18`, sets bit 6 of word `+0x96`, and when word `+0x5E` is -1 stores there signed word `+2` of `rcx` multiplied by word `01DFE0B4` (a value of -1 stays -1)", [("00417A86", "or"), ("00417A94", "or"), ("00417AAD", "movzx"), ("00417AC3", "mov")]),
 ("00417C60", "calls the function pointer in qword `02CA4438`, when set, with (qword `+0x2C0` of `r8`, `rcx`) and the one in `02CA4698`, when set, with (qword `+0x2E0` of `r8`, `rcx`); then sets bit 5 of qword `+0x2C8` of `r8`", [("00417C6A", "mov"), ("00417C86", "call"), ("00417C88", "mov"), ("00417C9E", "call"), ("00417CA7", "bts")]),
 ("00417DE0", "unless dword `+0xC` of `r8` has a bit of `0x24000` set, scores the entry at `rcx` against `r8`: 1 when its word `+2` is -1; otherwise word `+2` must equal the low 12 bits of word `+0x326` and one of the byte pairs at `+8` (count signed byte `+7`) must start with `r8`'s byte `+0x329` (score 3) or 0xFF (score 2). When the score is at least signed word `+0x32A` it stores it there, copies bit 7 of byte `+5` to bit 0 of dword `+0x2E8`, sets bit 1 of `+0x2E8` and float `+0x354` = 0 when byte `+4` is 0xFF (else clears the bit and stores 1.0 divided by byte `+4`, or 0 for 0), stores the low 7 bits of byte `+5` sign-extended in word `+0x358` and signed byte `+6` in word `+0x35A`, and sets bit 11 of `+0xC` (and bit 14 when bit 13 is set)", [("00417DEC", "test"), ("00417E18", "cmp"), ("00417E5C", "setne"), ("00417E83", "mov"), ("00417EF2", "divss")]),
 ("00418600", "copies bytes `+2` to `+5` of `rcx` to bytes `+0x2DC` to `+0x2DF` of `r8`; sets word `+4` of `rdx` to 1 and bit 1 of its word `+8`, and stores `r8`'s dword `+0x340` in its dword `+0x20`", [("00418604", "mov"), ("00418625", "mov"), ("00418631", "mov"), ("0041863C", "or"), ("00418641", "mov")]),
 ("00418650", "for a non-null `rcx`, stores `xmm3` in float `+0x190 + 4*(4*edx + r8d)` of `rcx` and of each object reached by resolving its dword `+0x278` through `0020E600`, until one does not resolve", [("0041866C", "lea"), ("00418670", "movss"), ("00418679", "mov"), ("0041867F", "call")]),
 ("004186A0", "unless bit 1 of byte `+0x280` of `rcx` is set, stores `xmm3` in float `+0x1D0 + 4*(4*edx + r8d)` of `rcx` and of each object reached by resolving its dword `+0x278` through `0020E600`, until one does not resolve", [("004186A4", "test"), ("004186C0", "lea"), ("004186D0", "movss"), ("004186DF", "call")]),
 ("00418700", "for a non-null `rcx`, stores `xmm3` in float `+0x1B0 + 4*(4*edx + r8d)` of `rcx` and of each object reached by resolving its dword `+0x278` through `0020E600`, until one does not resolve", [("0041871C", "lea"), ("00418720", "movss"), ("00418729", "mov"), ("0041872F", "call")]),
 ("0041E590", "returns bit 0 of dword `+8` of the object `003E55B0()` returns, or 0 when there is none", [("0041E594", "call"), ("0041E5A3", "mov"), ("0041E5A6", "and")]),
 ("00504BC0", "for a non-null `rcx` whose word `+0x64` is not 0xFFFF: looks up `004780B0(qword +0xDA0 of 0020E600(dword +0x10), word +0x64)` and calls `003CD7F0(id, edx)` for each of the 16 dwords at `+0x140` of the result that is not -1", [("00504BD4", "movzx"), ("00504BF1", "call"), ("00504C00", "lea"), ("00504C19", "call"), ("00504C22", "sub")]),
 ("00504E70", "with `rdx` non-null, copies word `[rdx]` to `+0` and stores `00409A30(rdx, r9d, fifth argument)` in dword `+0x10`; with `rdx` null, sets `+0x10` to -1. When `+0x10` is then -1, stores `00409FA0(r8, r9d, fifth argument)` in word `+0` and `00409A30(00409F50(r8, that word), r9d, fifth argument)` in `+0x10`", [("00504E90", "mov"), ("00504EA9", "call"), ("00504EB1", "cmp"), ("00504EC1", "call"), ("00504EDE", "call")]),
 ("00519100", "returns the index of the first 0x60-byte record whose dword `+0x1C` equals `edx`, among the word `+4` records the handle at dword `+0` resolves to (`0020E600`); 0xFFF when none does", [("0051911D", "movzx"), ("00519129", "add"), ("00519130", "cmp"), ("00519138", "add"), ("00519141", "mov")]),
 ("0051FB70", "zeroes dwords `+0`, `+0x20` and `+0x58`, word `+0x24` and qwords `+8`, `+0x10`, `+0x30`, `+0x38`, `+0x48` and `+0x50`; sets qwords `+0x18` and `+0x40` to -1", [("0051FB72", "mov"), ("0051FB7A", "mov"), ("0051FB87", "mov"), ("0051FB9B", "mov"), ("0051FB9E", "mov")]),
 ("00520160", "sets bit 24 of dword `+0x294`, copies byte `+2` of `rdx` to byte `+0x3D0` and returns 0", [("0052016A", "movzx"), ("0052016E", "mov"), ("00520174", "xor")]),
 ("00520740", "sets bit 23 of dword `+0x290`; writes the low 3 bits of byte `+2` of `rdx` to bits 0-2 of byte `+0x3D1` and the low 3 bits of byte `+3` to bits 3-5, keeping its other bits; returns 0", [("0052074E", "xor"), ("00520756", "xor"), ("00520767", "shl"), ("00520773", "mov")]),
 ("00520780", "stores 0x306 in word `+0x2F6` when word `+2` of `rdx` is non-zero, else 0x305; returns 0", [("00520782", "cmp"), ("00520786", "setne"), ("00520789", "add"), ("0052078D", "mov")]),
 ("005207A0", "stores 0x304 in word `+0x2F4` when word `+2` of `rdx` is non-zero, else 0x303; returns 0", [("005207A2", "cmp"), ("005207A6", "setne"), ("005207A9", "add"), ("005207AD", "mov")]),
 ("00520E90", "looks up the record `002ED570(qword +0xD98 of 0020E600(dword +0x10), dword +0x18)` (none when `+0x18` is -1); when its handle at dword `+0x94` resolves through `0020E600` twice to an object, copies bit 0 of byte `+0x1A` of `rdx` into bit 2 of that object's byte `+0x3F` and calls `0040ABF0(object, word rdx+0x16, &{floats rdx+8, +0xC, +0x10, 1.0}, word rdx+0x14, word rdx+0x18)`; in every case sets byte `+0x1A` of `rdx` to 1", [("00520ED0", "call"), ("00520F47", "movss"), ("00520F94", "xor"), ("00520FC9", "call"), ("00520FD6", "mov")]),
 ("00521000", "when word `+0x2F8` is not -1: copies bits 0-1 of byte `+0x40B` of the object at qword `+8` of `rdx` into byte `+0x40B`, calls `00427320(rcx, dword [rdx])`, then tail-calls `004272E0(rcx)`", [("00521006", "cmp"), ("0052102A", "xor"), ("00521033", "call"), ("00521040", "jmp")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`fef_interior.py`](../../_index/candidates/opus-fef-interior-1001/fef_interior.py): every "
        "anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
        "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
fails = 0
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
for fn, text, anchors in ROWS:
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        print("VERIFY FAIL %s: not a function entry" % fn); fails += 1; continue
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            print("VERIFY FAIL %s: anchor %s outside the body" % (fn, a)); fails += 1
        elif ins.get(av) != mn:
            print("VERIFY FAIL %s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn)); fails += 1
    if "|" in text:
        print("VERIFY FAIL %s: pipe in text" % fn); fails += 1
print("VERIFY %d functions, %d anchors" % (len(ROWS), sum(len(r[2]) for r in ROWS)))
if not fails:
    body = HEAD + "".join("| `%s` | %d B | %s | %s |\n" % (fn, sizes[int(fn, 16)], text, ", ".join("`%s`" % a for a, _m in anchors))
                          for fn, text, anchors in ROWS)
    b = open(P, "rb").read()
    crlf = b"\r\n" in b[:4000]
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    if HEAD.splitlines()[0].encode("utf-8") in b:
        print("ALREADY")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply writes)")
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
