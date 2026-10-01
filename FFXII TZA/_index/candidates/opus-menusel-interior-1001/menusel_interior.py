"""menusel_interior.py [--apply] - interior citations for the F-frontier functions that the-selection-the-menu-publishes.md cited by
entry only (OPUS, 2026-10-01). All 27 read by hand from the certified image; every rip target was resolved with retool.py
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

P = os.path.join(DB, "16-UI", "the-selection-the-menu-publishes.md")
PULSE = ("byte `+0x90` of `rdx` to (int)(sinf(dword `0208F570` * 3.14159 / 30) * 32 + 96) (`01CEBC50`, `008F8D80`, `009159F8`, "
         "`00915BA0`; `00861F0E` jumps to the `sinf` import), word `+0x91` to 0x3030 and byte `+0x93` to 0x80")
ROWS = [
 ("00272180", "calls `00202C50(&v, rdx, r8)` with the matrix at `rdx` and the vector at `r8`, divides v's x, y and z by w = matrix floats `+0xC`, `+0x1C`, `+0x2C` dotted with the vector plus `+0x3C`, stores w as v's fourth float, calls `00862930(rcx, &v)` and returns 1.0 (`01CEBBA8`) divided by w", [("002721AA", "call"), ("002721C5", "mulss"), ("002721F5", "divss"), ("0027221F", "divss"), ("00272223", "call")]),
 ("00272250", "calls `00272180`, then rewrites dword `+0` as ((value - 0x8000) >> 4) plus dword `01E0C1D8` >> 1 and dword `+4` as ((value - 0x8000) >> 4) plus dword `01E0C1DC` >> 1 (arithmetic shifts)", [("00272259", "call"), ("00272269", "sub"), ("00272277", "sar"), ("0027227F", "mov"), ("0027228B", "mov")]),
 ("002722A0", "calls `00272180` and keeps its float result; rewrites dword `+0` as ((value - 0x8000) >> 4) plus ((int)(dword `01E0C1D8` as a float divided by `00183280()`) >> 1) and dword `+4` as ((value - 0x8000) >> 4) plus dword `01E0C1DC` >> 1; returns the kept float", [("002722B3", "call"), ("002722C6", "call"), ("002722DF", "divss"), ("002722FB", "mov"), ("00272307", "mov")]),
 ("002737B0", "returns 1 when `0035BB00(i)` equals `ecx` for some i below `0035BB60()`, else 0", [("002737BE", "call"), ("002737C9", "call"), ("002737CE", "cmp"), ("002737EA", "mov")]),
 ("00273850", "returns 1 when `ecx` is in 0 to dword `01E0C1D8` - 1 and `edx` is in 0 to dword `01E0C1DC` - 1 (signed), else 0", [("00273852", "js"), ("00273858", "cmp"), ("00273860", "cmp"), ("00273868", "mov")]),
 ("00274BA0", "appends the node `rdx` at the end of the chain linked through qword `+0x18` from `rcx`: clears `rdx`'s `+0x18`, points the last node's `+0x18` at it and stores the last node in `rdx`'s `+0x10`", [("00274BB3", "mov"), ("00274BBC", "mov"), ("00274BC4", "mov"), ("00274BC8", "mov")]),
 ("0027BC10", "when dword `+0x500` is 0 or negative, sets qword `+0x1578` to `002F9860(0x7D2)`, " + PULSE + ", and tail-calls `002D8650(rdx, 0, 0, rcx + 0x1550)`. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: sets word `+0x5A` of `rdx` to 0x40 when bit 0 of the entry's byte `+2` is set, else 0x80; sets qword `+0x1578` to `002F9860(0x404)` when the entry's word is 0xFFFF, else to `002B58B0(qword +0x18 of 0035D380(1, word), 0)` and, when word `+0x1538` equals that word, byte `+0x15EF` to 6; calls `002D8650` the same way, then restores byte `+0x15EF` and word `+0x5A`", [("0027BC1A", "cmp"), ("0027BC58", "call"), ("0027BC91", "mov"), ("0027BCDF", "mov"), ("0027BD33", "mov")]),
 ("0027BD80", "calls `0031AB80(rcx, 0, dx, &rec)` and returns float `+0x10` of rec when the call is not negative and rec's dword `+8` is 1, else 0.0", [("0027BD97", "lea"), ("0027BD9E", "call"), ("0027BDBC", "cmp"), ("0027BDC3", "movss")]),
 ("0027D240", "when dword `+0x500` is 0 or negative, sets qword `+0x1578` to `002F9860(0x7D2)` and " + PULSE + ". Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: sets word `+0x5A` of `rdx` to 0x40 when bit 1 of the entry's byte `+3` is set, else 0x80, and qword `+0x1578` to `002B58B0(qword +0x18 of 0035D330(k, the entry's word), 0)` with k = 0x18 when bit 2 of byte `+3` is set, else 0x15. Both paths tail-call `002D8650(rdx, 0, 0, rcx + 0x1550)`", [("0027D24A", "cmp"), ("0027D288", "call"), ("0027D2C7", "test"), ("0027D2F3", "call"), ("0027D323", "jmp")]),
 ("0027D5C0", "when dword `+0x500` is 0, sets qword `+0x1578` to `002F9860(0x7D1)`, " + PULSE + ", and tail-calls `002D8650(rdx, 0, 0, rcx + 0x1550)`. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: calls `0031C5D0` on a stack record {2, the entry's dword}, sets word `+0x5A` of `rdx` to 0x40 when bit 1 of the entry's byte `+4` is set, sets qword `+0x1578` to `002B58B0(record qword +0x18, 0)`, calls `002D8650` the same way and restores word `+0x5A`", [("0027D5CD", "cmp"), ("0027D5E5", "call"), ("0027D68E", "call"), ("0027D6B9", "call"), ("0027D6E1", "mov")]),
 ("0027E530", "does nothing when bit 15 of dword `+0x1528` is set. When dword `+0x500` is 0 or negative, sets qword `+0x1578` to `002F9860(0x7D1)`, " + PULSE + ", and calls `002D8650(rdx, 0, 0, rcx + 0x1550)`. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: sets word `+0x5A` of `rdx` to 0x40 when bit 1 of the entry's byte `+4` is set, sets qword `+0x1578` to `00272CB0(the entry's dword)` and calls `002D8650`; when n = `00272C80(the entry's dword)` is positive, formats n into a stack buffer with `0024ABE0(buf, 0x20, n, 0)`, points `+0x1578` at the buffer (one byte in when `00254A10()` is 0), measures text with `0029CD00` and draws with `002D8690`. Every path restores word `+0x5A` and zeroes dword `+0x159C`", [("0027E54B", "test"), ("0027E59E", "call"), ("0027E626", "call"), ("0027E650", "call"), ("0027E765", "call")]),
 ("0028EA20", "tail-calls `002911D0(qword 0209BE80, ecx, r8, edx)`", [("0028EA23", "mov"), ("0028EA25", "mov"), ("0028EA2C", "jmp")]),
 ("0028F9E0", "returns 1 when word `+0x850` at the zero-extended low dword of `rcx` is 1 or 2, else 0", [("0028F9E2", "movzx"), ("0028F9EB", "dec"), ("0028F9F2", "setbe")]),
 ("0028FEA0", "returns 0 when qword `0209BE80` is null; otherwise calls `002BE020` on `[0209BE80] + 0x8FA0` and tail-calls `002BE1A0(that, ecx, 0, edx)`", [("0028FEAE", "mov"), ("0028FEC7", "add"), ("0028FECE", "call"), ("0028FEF3", "jmp")]),
 ("00290520", "returns 3 when qword `+0x10F78` of `[0209BE80]` is null, else tail-jumps to `00296570` on it", [("00290527", "mov"), ("00290533", "lea"), ("00290537", "jmp")]),
 ("002905B0", "tail-jumps to `002969D0(qword +0x10F78 of [0209BE80], ecx)` when that qword is non-null, else returns", [("002905B7", "mov"), ("002905B9", "mov"), ("002905C3", "jne")]),
 ("00290B70", "sets word `+0x850` at the zero-extended low dword of `rcx` to 3 when it is 2", [("00290B72", "cmp"), ("00290B81", "mov")]),
 ("00290C60", "when qword `0209BE80` is non-null, tail-jumps to `002BE270(it + 0x8FA0, ecx)`", [("00290C62", "mov"), ("00290C6E", "add"), ("00290C75", "jmp")]),
 ("00296570", "returns byte `+0xB43`, or 0 when `rcx` is null", [("00296575", "xor"), ("00296578", "movzx")]),
 ("00296ED0", "for a non-null `rcx`: when bit 8 of word `+0xB4A` is set and `edx` is 0, clears bits 0-2 and 7 of word `+0x318 + 0x160*i` for each i below byte `+0xB42`; then clears bit 8 of `+0xB4A` and sets it again when `edx` is non-zero", [("00296EDE", "test"), ("00296F05", "and"), ("00296F24", "and"), ("00296F3B", "mov")]),
 ("00321060", "when bit 4 of byte `02089340` is set and `00263E30(003588B0(ecx))` is non-null, calls `0031AA30(it, 0, word +0x714, &rec)`, stores rec's dwords `+0` and `+4` through `rdx` and `r8` when they are non-null, and returns that call's result; otherwise returns -1", [("0032106A", "test"), ("00321086", "call"), ("003210A2", "call"), ("003210B0", "mov"), ("003210C8", "or")]),
 ("00357450", "tail-calls `0026B4E0(rcx, 00264F90(003148F0(rcx)))`", [("00357459", "call"), ("00357460", "call"), ("0035746F", "jmp")]),
 ("003F34D0", "appends the node `rdx` at the end of the chain linked through qword `+0x70` from `rcx`, storing the previous last node in `rdx`'s `+0x78`, and returns `rcx`; with `rcx` null returns `rdx`", [("003F34D8", "mov"), ("003F34F3", "mov"), ("003F34FC", "mov"), ("003F3503", "mov")]),
 ("003F3510", "calls `00275550(rcx, 0x80, r8, r9)`, stores the sixth (float) argument in float `+0x64`, the fifth in dword `+0x6C` and `00272F30(fifth)` in float `+0x60`, then tail-calls `003F3660(rcx, rdx, r9d, r8)`", [("003F3535", "call"), ("003F3544", "movss"), ("003F3549", "mov"), ("003F354C", "call"), ("003F3576", "jmp")]),
 ("003F3580", "returns the first node on the chain linked through qword `+0x70` from `rcx` whose dword `+0x6C` equals `edx`, or 0", [("003F3585", "cmp"), ("003F358A", "mov"), ("003F3593", "xor"), ("003F3596", "mov")]),
 ("003F3660", "sets bit 0 of dword `+0x50`, stores `r8d` in dword `+0x48` and `rdx` in qword `+0x40`; calls `00271140(&v, r9, qword [rdx+0x30] + ((2*r8d sign-extended) << 37))` and stores v's floats `+8`, `+0xC`, `+0`, `+4` in floats `+0x20`, `+0x24`, `+0x28`, `+0x2C`; zeroes dword `+0x4C` and sets floats `+0x10`, `+0x14`, `+0x18` to 255.0, `+0x1C` to 127.0 and `+0x30` to 0.25", [("003F3675", "or"), ("003F3690", "shl"), ("003F369B", "call"), ("003F36AC", "movss"), ("003F36D3", "mov")]),
 ("003F6370", "when dwords `+0x810` and `+0x814` are non-zero and `003588B0` finds them, calls `002EA160(found, rcx + 0x10)` and `002EA0E0(found, rcx)`; combines the vectors at `+0` and `+0x10` with `00203080` and, when `002703F0` of the result is at least 1.0 (`01CEBBA8`), passes it through `00202DE0` and `00203030`, otherwise copies it to `022D9240` and `022D9260`, 1.0 to `022D925C` and three stack floats to `022D9250`-`022D9258`; after `00202B10` adds (2.0 minus floats `+0x820` and `+0x824`) times 0.75 plus 1.5 to its y (`01CEBC08`, `00901B3C`, `01CEBB70`); stores `00270F50(rcx + 0x240, ..., 3)` in dword `+0x7E0`, interpolates between the 16-byte entries `rcx + 0x240 + 16*(i-1)` and `+ 16*i` (i from (1.0 minus float `+0x838`) times the count minus one, each clamped) into `+0x1C0` with `00275490`, and adds 0.25 (`01CEBB68`) to float `+0x1C4`", [("003F63B2", "call"), ("003F6400", "call"), ("003F648E", "movups"), ("003F6512", "mov"), ("003F6580", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`menusel_interior.py`](../_index/candidates/opus-menusel-interior-1001/menusel_interior.py): every "
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
