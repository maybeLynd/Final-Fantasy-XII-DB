"""inputstack_interior.py [--apply] - interior citations for the F-frontier functions that input-stack-device-channel-and-bindings.md cited
by entry only (OPUS, 2026-10-01). All 32 read by hand from the certified image; every rip target was resolved with retool.py
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

P = os.path.join(DB, "15-Input", "Input-Stack", "input-stack-device-channel-and-bindings.md")
ROWS = [
 ("0017D3E0", "returns 1 when byte `+0xD07` of the object `001D50D0()` returns is non-zero, else 0 (also 0 when there is none)", [("0017D3E4", "call"), ("0017D3F3", "movzx"), ("0017D3FE", "setne")]),
 ("00198E80", "looks up `0079D620(qword +0xDF8 of 00796E20(), edx)` and, when found, calls `007A1080(it, r9b, r8b)`", [("00198E97", "call"), ("00198EA5", "call"), ("00198EBA", "call")]),
 ("001E1120", "tail-calls `00198E80(00198790(), ecx, edx, r8d)` when `00198790()` is non-null, `00197780` on it is non-zero and `00228480()` returns 0; otherwise tail-calls `00198E80(00198790(), ecx, 0, 0)`", [("001E1148", "call"), ("001E1151", "call"), ("001E116C", "xor"), ("001E1186", "jmp")]),
 ("0035E7A0", "adds dword `022CA5D0` to dword `022CA5C4` and stores the sum S there; with P = 0x108 when `00290180()` returns 2, else 0x13A: when S < P returns P - S if `00229EA0()` returns 3, else 2P - S; otherwise returns ceil(S/P)*P - S", [("0035E7B6", "mov"), ("0035E7CE", "cmove"), ("0035E7DA", "cmp"), ("0035E7DF", "add"), ("0035E7F7", "idiv")]),
 ("005DC1B0", "zeroes qwords `+0` and `+8` and dword `+0x10`; returns `rcx`", [("005DC1B5", "mov"), ("005DC1B9", "mov"), ("005DC1BC", "mov")]),
 ("005FEF80", "returns 0 when `005C5230(rcx + 8)` is non-zero; otherwise sets bit 0 of dword `+4` and tail-calls `0061D490(rcx, edx)`", [("005FEF8F", "add"), ("005FEF93", "call"), ("005FEFA9", "or"), ("005FEFBC", "jmp")]),
 ("0060D4A0", "for slot `r8d`: with `rdx` non-null, copies 24 bytes from `rdx` to `+8 + 24*slot` and sets bit `slot` of byte `+0xE0`; with `rdx` null, clears that bit; then tail-jumps to `006283E0`", [("0060D4AF", "movups"), ("0060D4C8", "bts"), ("0060D4DE", "btr"), ("0060D4E8", "jmp")]),
 ("0060DB10", "with `rdx` non-null, copies 24 bytes from `rdx` to `+0xC8` and sets byte `+0xE1` to 1; with `rdx` null, sets it to 0; then tail-jumps to `00628630`", [("0060DB18", "movups"), ("0060DB2C", "mov"), ("0060DB38", "mov"), ("0060DB3F", "jmp")]),
 ("006106A0", "stores `005CC920()` in dword `+0x298C`, calls `005C5230(rcx + 0x20, \"RenderThread\" at 00D4A760, 0x2000)` and `005C5230(01F2ED08, rcx + 0x20)`, then loops: each pass takes the ring index dword `+0x2830` (0 to 255, 40-byte entries) and calls `005CD840` on the entry's `+0x40`; by dword `+0x28`, 0 calls `005CD500` and `005CDAA0(1, \"Render thread running without initialize\" at 00D4A770)`, 1 calls `005CD500` and `0060A410(rcx, entry qword +0x30, entry qword +0x38)`, clears entry qwords `+0x30`, `+0x38` and `+0x50` and calls `005CD650(old +0x50, 1, 0)` when it was set, and 2 ends the loop after the pass; every pass ends with `005CD650(rcx + 0x2840, 1, 0)`. After the loop it calls `005C5230(01F2ED08, rcx + 0x20)` and returns 0", [("006106CC", "mov"), ("00610700", "mov"), ("00610724", "call"), ("00610753", "call"), ("006107A3", "call")]),
 ("00615D50", "stores `rdx` in qword `+0`, zeroes dword `+8` and qwords `+0x10` to `+0x48`; returns `rcx`", [("00615D52", "mov"), ("00615D55", "mov"), ("00615D74", "mov"), ("00615D78", "mov")]),
 ("0061C150", "maps `ecx` through an 8-entry jump table: 0 to 1, 1-4 to 2-5, 5 to 7, 6 to 8, 7 to 6, and any value above 7 (unsigned) to 1", [("0061C153", "ja"), ("0061C15F", "mov"), ("0061C169", "jmp"), ("0061C195", "mov")]),
 ("0061D490", "collects up to two qwords into the array at `+0x648` from the two 24-byte entries at `+0x570` and one into `+0x688` from the entry at `+0x630`, by the kind byte `+8` of each entry's object and the flag bits in dword `+0x18` of that object's first qword, requiring every accepted entry to share dwords `+0x28`/`+0x2C` and byte `+9` (it returns 0 on a mismatch, or when `00620F60` fails for an entry whose qwords `+0x18` and `+0x28` are 0); the count goes to dword `+0x6D0`. With none accepted it falls back to `+0x4A0`/`+0x4A8`, `+0x4E0`/`+0x4E8` and the sizes of the object at `+0x480`. It stores the sizes in dwords `+0x186C`/`+0x1870`, calls `0061E6B0` six times, calls virtual `+0x108` of qword `+0x110` with (the count, the array or null, qword `+0x688`), then `0061D3D0` and `0061EA80(rcx, edx)`, whose result it returns", [("0061D50D", "call"), ("0061D5B7", "mov"), ("0061D71F", "mov"), ("0061D80D", "mov"), ("0061D906", "call")]),
 ("0061ECD0", "tail-calls `00623B10(rcx + 0x708, qword +0x110, edx)`", [("0061ECD3", "mov"), ("0061ECDA", "add"), ("0061ECE1", "jmp")]),
 ("0061ED00", "around a stack object built by `00615BC0`: calls virtual `+0x178` of qword `+0x110` of `005FD050()` with qwords `+8` and `+0x10` of `rcx`, calls `005FD050()` again when `00225690(005FCF20())` returns 1, then calls `005CD7D0(005FCF20())`", [("0061ED17", "call"), ("0061ED34", "call"), ("0061ED43", "call"), ("0061ED5A", "call")]),
 ("00621FA0", "when byte `+0x20` of `rdx` is set, calls `0061ED00(rdx)` and clears it; then calls virtual `+0x150` of qword `+0x110` with (qword `+8` of `rdx`, 0); returns 0", [("00621FAA", "cmp"), ("00621FBD", "call"), ("00621FC2", "mov"), ("00621FD3", "call")]),
 ("00622350", "with `r9d` non-zero, maps `edx` through `0061C1C0`; for a non-zero result: when it differs from dword `01F2DEF8`, stores it there and calls the function pointer in `01F2DEF0` with (qword `+0x110`, the result); then calls virtual `+0x68` of qword `+0x110` with (`r9d`, `r8d`). Returns 0 when `0061C1C0` gives 0, else 1", [("0062236F", "call"), ("00622388", "cmp"), ("0062239F", "call"), ("006223B4", "call")]),
 ("006223D0", "maps `edx` through `0061C1C0`; for a non-zero result: when it differs from dword `01F2DEF8`, stores it there and calls the function pointer in `01F2DEF0` with (qword `+0x110`, the result); when byte `+0x20` of `r8` is set, calls `0061ED00(r8)` and clears it; then calls virtual `+0x140` of qword `+0x110` with (qword `+8` of `r8`, 0). Returns 1, or 0 when `0061C1C0` gives 0", [("006223E2", "call"), ("00622407", "mov"), ("00622423", "call"), ("00622439", "call")]),
 ("00623B10", "for slot `r8d`, twice (byte counts dword `+0x20`/`+0x28` + 4*slot, targets qword `+0`/`+0x10` + 8*slot, sources qword `+0x38`/`+0x48` + 8*slot): when the count is non-zero, calls virtual `+0x70` of `rdx` with (target, 0, 4, 0, &out), copies the count of bytes from the source to the pointer in `out` with `00861EBA`, and calls virtual `+0x78` with (target, 0); returns 0, or 9 when the `+0x70` call returns negative or leaves a null pointer", [("00623B2D", "mov"), ("00623B5A", "call"), ("00623B7B", "call"), ("00623B8D", "call"), ("00623C04", "mov")]),
 ("00623F00", "returns qword `+0` of 40-byte element `edx` of an array whose count is dword `+0x18` without bit 31 (at qword `+0x20` when the count is above 1, inline at `+0x20` when it is 1); 0 when `edx` is not below the count", [("00623F03", "btr"), ("00623F0C", "jae"), ("00623F22", "mov"), ("00623F27", "lea"), ("00623F37", "mov")]),
 ("00626D90", "stores `edx` in dword `+0x6F0` and zeroes the dwords at index `edx` of `+0x728`, `+0x730`, `+0x780` and `+0x788`; returns 0", [("00626D92", "mov"), ("00626D9A", "mov"), ("00626DAF", "mov"), ("00626DB6", "xor")]),
 ("00627F10", "zeroes dword `+0xA24`; stores `dl` in `+0xA28`, `0061BF40(r8d)` in `+0xA2C`, `0061BF40(r9d)` in `+0xA30`, 5 in `+0xA38` and 6 in `+0xA3C`; sets bit 1 of `+0x9C0`; returns 0", [("00627F1A", "mov"), ("00627F36", "call"), ("00627F43", "call"), ("00627F53", "mov"), ("00627F67", "or")]),
 ("00627F80", "zeroes dword `+0xA24`; stores `dl` in `+0xA28` and `0061BF40` of `r8d`, `r9d`, the fifth and the sixth argument in `+0xA2C`, `+0xA30`, `+0xA38` and `+0xA3C`; sets bit 1 of `+0x9C0`; returns 0", [("00627F8A", "mov"), ("00627FA6", "call"), ("00627FC2", "call"), ("00627FD1", "call"), ("00627FE1", "or")]),
 ("006281A0", "unpacks `edx` as four bytes, each multiplied by 1/255 (`00D11104`): bits 16-23 into float `+0x7C0`, 8-15 into `+0x7C4`, 0-7 into `+0x7C8` and 24-31 into `+0x7CC`", [("006281AD", "shr"), ("006281C4", "movss"), ("006281DE", "movss"), ("006281F4", "movss"), ("00628208", "movss")]),
 ("00628220", "stores `xmm1`, `xmm2`, `xmm3` and the fifth (stack) float in floats `+0x7C0`, `+0x7C4`, `+0x7C8` and `+0x7CC`", [("00628226", "movss"), ("0062822E", "movss"), ("00628236", "movss"), ("0062823E", "movss")]),
 ("00628320", "sets bit 1 of dword `+0x9C0` and stores in byte `+0xA44` a mask whose bits 0-3 say which of `dl`, `r8b`, `r9b` and the fifth argument's low byte are non-zero; returns 0", [("00628325", "setne"), ("0062832D", "or"), ("00628344", "or"), ("00628356", "or"), ("0062836B", "mov")]),
 ("006283E0", "returns 5 when `r8d` is 8 or above; otherwise copies 24 bytes from `rdx` to `+0x570 + 24*r8d` and returns 0. With `rdx` null the source is a stack record zeroed by `005DC1B0`, which is passed to `0016D6A0` afterwards", [("006283F0", "cmp"), ("006283F6", "mov"), ("00628416", "movups"), ("00628437", "call"), ("00628447", "movups")]),
 ("006284B0", "sets bit 0 of dword `+0x9C0` and zeroes dword `+0x9CC`; for `edx` 0, 1 or 2 also stores `edx + 1` in dword `+0x9C8` (other values leave it); returns 0", [("006284BE", "or"), ("006284C6", "mov"), ("006284E4", "mov"), ("006284F9", "mov"), ("00628503", "or")]),
 ("00628600", "sets bit 2 of dword `+0x9C0` and stores 1 in dword `+0x9F0` when `dl` is non-zero, else 0; returns 0", [("00628604", "setne"), ("00628607", "or"), ("0062860E", "mov")]),
 ("00628630", "copies 24 bytes from `rdx` to `+0x630` and returns 0. With `rdx` null the source is a stack record zeroed by `005DC1B0`, which is passed to `0016D6A0` afterwards", [("00628643", "movups"), ("0062864F", "movsd"), ("00628662", "call"), ("0062866F", "movups"), ("00628683", "call")]),
 ("00629540", "sets bit 0 of dword `+0x9C0` and stores 2 in dword `+0x9C4` when `edx` is 1, else 3; returns 0", [("00629545", "setne"), ("00629548", "or"), ("0062954F", "add"), ("00629552", "mov")]),
 ("00629620", "calls virtual `+0x168` of qword `+0x110` with (1, &{`edx`, `r8d`, `r9d + edx`, fifth argument + `r8d`})", [("0062963E", "lea"), ("00629642", "add"), ("0062965A", "mov"), ("00629666", "call")]),
 ("007927C0", "makes `+8` and `+0x18` self-linked list heads, stores `rdx` in qword `+0x28`, links the `+8` node in before the list head `01F401E8` (updating its back pointer at `01F401F0`), sets qword `+0` to `01CB23C0` and then `01CB2430`, zeroes the 0x100 bytes at `+0x231`, `+0x30` and `+0x130` with `00861EC0`, clears byte `+0x230` and sets byte `+0x331` to 0xFF; returns `rcx`", [("007927DB", "mov"), ("007927E9", "mov"), ("00792815", "mov"), ("00792822", "mov"), ("00792859", "mov")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`inputstack_interior.py`](../../_index/candidates/opus-inputstack-interior-1001/inputstack_interior.py): every "
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
