"""widgetmsg_interior.py [--apply] - interior citations for the F-frontier functions that the-widget-message-protocol.md cited by entry
only (OPUS, 2026-10-01). All 30 read by hand from the certified image; every rip target was resolved with retool.py
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

P = os.path.join(DB, "16-UI", "Widget-Object-Model", "the-widget-message-protocol.md")
ROWS = [
 ("001E9F00", "stores `edx`, `r8d` and `r9d` in dwords `+0x13A0`, `+0x13A4` and `+0x13A8`, the fifth argument in `+0x13AC` and the sixth argument's low byte, zero-extended, in `+0x13B0`", [("001E9F04", "mov"), ("001E9F0F", "mov"), ("001E9F15", "mov"), ("001E9F1B", "mov"), ("001E9F22", "mov")]),
 ("002418E0", "copies bit 0 of `edx` into bit 5 of dword `+0x40`", [("002418E4", "and"), ("002418E7", "shl"), ("002418EA", "or")]),
 ("00244610", "compares two dword pairs: returns dword `[rdx]` minus dword `[rcx]` when that is non-zero, else dword `rcx+4` minus dword `rdx+4`", [("00244612", "sub"), ("00244614", "jne"), ("00244616", "mov"), ("00244619", "sub")]),
 ("002446E0", "calls `002448D0(rcx)`, then tail-calls `00244700(rcx, 1)`", [("002446E9", "call"), ("002446EE", "mov"), ("002446FB", "jmp")]),
 ("002478D0", "for a non-null `rcx`, copies bit 0 of `edx` into bit 18 of dword `+0x40`, then calls itself with the same `edx` on each child, starting at qword `+0x18` and following qword `+0x20`", [("002478DA", "and"), ("002478F1", "shl"), ("002478F4", "or"), ("00247905", "call"), ("0024790A", "mov")]),
 ("00250C50", "when qword `020927F0` is non-null, writes into that object: byte `+0x129` = `cl`, word `+0xE6` = 7, dword `+0x12C` = dword `0208F570`, word `+0x12A` = `dx`, dword `+0x124` = 0", [("00250C61", "mov"), ("00250C68", "mov"), ("00250C76", "mov"), ("00250C7D", "mov"), ("00250C85", "mov")]),
 ("00251EA0", "when qword `020927F0` is non-null, writes into that object: float `+0x134` = `xmm0`, dword `+0x13C` = dword `0208F570`, word `+0x13A` = `dx`, dword `+0x130` = 0, byte `+0x138` = `r8b`", [("00251EB2", "movss"), ("00251EBA", "mov"), ("00251EC0", "mov"), ("00251EC7", "mov"), ("00251ED1", "mov")]),
 ("0027BD80", "calls `0031AB80(rcx, 0, dx, &out)` with a stack record `out`; returns its float `+0x10` when the call returns a non-negative value and its dword `+8` is 1, else 0.0", [("0027BD97", "lea"), ("0027BD9E", "call"), ("0027BDBC", "cmp"), ("0027BDC3", "movss")]),
 ("0027C150", "maps `ecx` 7 to 27 through a 21-entry jump table: 7 to 0xC92, 8 to 0xC94, 9 to 0xC95, 10 to 0xC96, 11 to 0xC93, 12 to 0xC91, 14 to 0xC90, 22 to 0xC8A, 23 to 0xC8B, 24 to 0xC8D, 25 to 0xC8F, 26 to 0xC98, 27 to 0xC99; every other value to -1", [("0027C153", "cmp"), ("0027C156", "ja"), ("0027C16C", "jmp"), ("0027C1BC", "or")]),
 ("0027D700", "calls `0027B200(rcx)` first when `r8d` is 0, then tail-calls `0027B770(rcx, dword +0x510 + 8*r8d, r8d)`", [("0027D710", "test"), ("0027D715", "call"), ("0027D71A", "mov"), ("0027D731", "jmp")]),
 ("0027E4E0", "returns 0 when `0027B770(rcx, r8d, -1)` returns 0; otherwise calls `0027AF00(rcx, rdx)` and returns 1", [("0027E4F2", "or"), ("0027E4F9", "call"), ("0027E513", "call"), ("0027E51D", "mov")]),
 ("0027E7B0", "returns 0 when bit 15 of dword `+0x1528` is set; otherwise calls `0027B200(rcx)` when `r9d` is non-zero and returns 1 when `0027B770(rcx, dword +0x510 + 8*r8d, r8d)` is non-zero, else 0", [("0027E7BA", "test"), ("0027E7DE", "call"), ("0027E7E3", "mov"), ("0027E7F0", "call"), ("0027E7FE", "setne")]),
 ("00290C60", "when qword `0209BE80` is non-null, tail-calls `002BE270(it + 0x8FA0, ecx)`", [("00290C62", "mov"), ("00290C6E", "add"), ("00290C75", "jmp")]),
 ("0029BB40", "for slots 0-3: when `00273A20` on the 0x160-byte record `+0x240 + 0x160*slot` returns 0, reads byte `+0xB44 + slot`; for a value 1-3 it builds a node with `00245000(that record, 0x160, 0029A0A0, &{0, slot, value})`, stores `rcx` in the node's qword `+0x120`, calls `00244960(rcx, node)` and `00246AC0(node)` and clears the byte; otherwise, when `0035BB20(slot)` returns a record with word `+0x60` and dword `+4` not negative, sets the byte to 2 when bit 1 of its dword `+0` is set, else to 3 or 1 by its bit 2, and the result becomes 1. Returns 0 when no slot took that last path", [("0029BB95", "call"), ("0029BBDA", "call"), ("0029BBE8", "mov"), ("0029BC09", "call"), ("0029BC35", "shr")]),
 ("002C9B30", "clamps `ecx` to 0-6 and selects the 16-byte record `009170C0 + 16*ecx`; by `edx` through a 9-entry jump table returns its signed byte `+0` to `+5` (0-5), its float `+8` truncated to an integer (6), its signed byte `+0xC` (7) or the low dword of the record's address (8); 0 for any other `edx`", [("002C9B34", "cmovns"), ("002C9B3E", "cmovg"), ("002C9B44", "lea"), ("002C9B6B", "jmp"), ("002C9B90", "cvttss2si")]),
 ("002D1420", "by the kind in dword `[rdx]`: 1 returns 0. 4 calls `002D2600(qword rcx+0x38, rcx)` when bit 25 of dword `+0xE0` of qword `+0x10` of `rcx` (of address 0 when `rcx` is null) is clear, else `002D28E0` with the same arguments, then zeroes dword `02CA8F30` and returns 0. 17 clears bit 27 of dword `+0xE4` of that object when qword `rdx+8` is 1, and returns 0. Any other kind sets dword `02CA8F30` to 1 and tail-jumps to `005C5230` with the same arguments", [("002D1437", "je"), ("002D143F", "mov"), ("002D1477", "and"), ("002D14AE", "call"), ("002D14C1", "call")]),
 ("002E04E0", "clamps `ecx` to 0-7 and selects the 0x68-byte record `0215F200 + 0x68*ecx`; when its dword `+0x60` is 0, adds `dx` to its word `+0x10` and `r8w` to `+0x12`, adds them to words `+0x98`/`+0x9A` of the object at its qword `+0` when that is non-null, and sets `+0x60` to 1", [("002E04F3", "imul"), ("002E0501", "cmp"), ("002E0507", "add"), ("002E0518", "add"), ("002E052A", "mov")]),
 ("00303E90", "tail-calls `0031E860(3)` when `0030D9A0()` returns 2; otherwise returns 0", [("00303E94", "call"), ("00303E99", "cmp"), ("00303E9E", "lea"), ("00303EA5", "jmp")]),
 ("00313590", "tail-calls `0031E860(3)` when `0030D9A0()` returns 1; otherwise returns 0", [("00313594", "call"), ("00313599", "cmp"), ("0031359E", "lea"), ("003135A5", "jmp")]),
 ("0037F340", "when qword `+0xC0` is non-null and its first qword is non-null, calls that function pointer with (the object, &{dword 0x10, the 16 bytes at `00D111C0`: 8, 0, 0, 0}); then sets bit 0 of dword `+0xE0` and byte `+0xE5` to 2", [("0037F358", "mov"), ("0037F367", "movdqa"), ("0037F387", "call"), ("0037F389", "or"), ("0037F390", "mov")]),
 ("003C5FB0", "returns 1 when `00254A50()` returns 0, `00377750()` is non-zero, `0053DD10(003148F0())` is non-zero and `00264790()` is not above 0; otherwise 0", [("003C5FB4", "call"), ("003C5FBD", "call"), ("003C5FCD", "call"), ("003C5FD6", "call"), ("003C5FDD", "jg")]),
 ("003CB0C0", "builds a node with `00245000(rcx + 0xC0, 0x1E0, 003CB150, 0)`, calls `00244960(rcx, node)`, and when the node and its first qword are non-null calls that function pointer with (the node, &{dword 0x10, 16 zero bytes})", [("003CB0DC", "lea"), ("003CB0F2", "call"), ("003CB100", "call"), ("003CB12B", "call")]),
 ("003F35A0", "for `rcx` and each object along qword `+0x70`: when dword `+0x6C` differs from `edx`, clears bit 0 of dword `+0x50` and zeroes `+0x6C`", [("003F35A7", "cmp"), ("003F35AC", "and"), ("003F35B0", "mov"), ("003F35B3", "mov")]),
 ("003F8BF0", "calls the function pointer at qword `+0x38`, when set, with (`rcx`, 5, 0); unlinks `rcx` from its neighbours (the object at qword `+0x30` gets qword `+0x28` in its `+0x28`, the object at `+0x28` gets `+0x30` in its `+0x30`), zeroes qwords `+0x28`/`+0x30` and word `+0x26`; then tail-calls `+0x38`, when set, with (`rcx`, 6, 0)", [("003F8C09", "call"), ("003F8C18", "mov"), ("003F8C29", "mov"), ("003F8C37", "mov"), ("003F8C53", "jmp")]),
 ("003FCD20", "by the kind in dword `[rdx]`: 1 reads the 20-byte entry `dword rdx+0x10` of `0020E600(dword +0x20 of qword rdx+8)`, gets `r = 002432B0(rcx + 0x50, qword +0x48 of [0209AC30], 0xD, rcx)`, and when `rcx` is non-null stores words `r+4` plus entry `+4`, `r+6` plus entry `+6`, `r+8` and `r+0xA` in words `+0x98` to `+0x9E`; then calls `003FCDE0(rcx)`, clears bit 11 of dword `+0x40` and returns 0. 18 returns 0. Any other kind tail-jumps to `005C5230` with the same arguments", [("003FCD56", "call"), ("003FCD7B", "call"), ("003FCDA1", "mov"), ("003FCDC2", "call"), ("003FCDC7", "and")]),
 ("00406A60", "by the kind in dword `[rdx]`. 1: stores `rcx` in qword `02B62D88`; zeroes `+0xC0`, `+0xE8`, `+0xD8`, bytes `+0xE3`/`+0xE1`; sets dword `+0xC8` to 0x10 and qword `+0xD0` to `0051EDC0(3)`; copies its byte `+0x24` count to byte `+0xE0`; for a non-zero count, allocates `8*count` bytes with `00393590` into `+0xD8` and fills each slot from the 12-byte entries of `0020E600(dword +0x28 of it)`: `0024A440(o + 0x10, o, 2)` with `o = 0020E600(entry dword +8)` for an entry whose dword `+0` is 1, else null; sets dword `+0x98` to 0 and words `+0x9C`/`+0x9E` from dwords `01E0C1D8`/`01E0C1DC`, and calls `00244960` with the qword read from `0208EA28` and `rcx`. 2: by dword `+0xC8`, bit 1 calls `004050C0`; bit 0, when `02B62D88` is set, calls `004050C0`, stores `00405100()` in byte `+0xE1`, clears bit 3 (or, when it was clear, checks the 24-byte entries at `[+0xE8]`, count byte `+0xE3`); when that byte is not 0xFF it posts `00244F50(0xD8, 00405310, &record)`, then calls `00244960`/`00247870` on `[+0xC0]` (bit 2) or `00246AD0`, and clears bit 0 and sets bit 1 of `+0xC8`. 4: when `02B62D88` is set, stores `0031B690([02B62D88] + 0xE8)` in its byte `+0xE3`. 18: calls `0024A680(slot, 0)` on each non-null slot of `+0xD8`, frees the array with `003697F0` and clears `+0xD8`. These return 0; any other kind returns `005C5230(rcx, rdx)`", [("00406AE2", "call"), ("00406B27", "call"), ("00406C36", "call"), ("00406C86", "mov"), ("00406CF3", "call")]),
 ("004076B0", "a step counter: returns -1 when dword `+4` (the step count) is 0; otherwise increments dword `+0` and, below the count, stores t = step/count in float `+0x14` and `(int)(dword +0xC * t + dword +8)` in dword `+0x10`, returning it; at the count, stores `+8 + +0xC` in `+0x10`, zeroes `+4`, stores 1.0 in `+0x14` and returns the sum", [("004076B7", "or"), ("004076BB", "inc"), ("004076E2", "divss"), ("004076FA", "cvttss2si"), ("00407707", "mov")]),
 ("00407C90", "when dword `+0x44` masked by `0x180000` equals `0x100000`, stores word `+0x54` (plus dword `[rdx]` when `rdx` is non-null) in word `+0x98` and word `+0x56` (plus dword `rdx+4`) in `+0x9A` (skipped when `rcx` is null); then calls itself on each child from qword `+0x18`, following each call's return value, and returns qword `+0x20`", [("00407CAB", "and"), ("00407CD0", "mov"), ("00407CF6", "call"), ("00407D00", "mov")]),
 ("0057E8D0", "by the kind in dword `[rdx]`: 1 stores `rcx` in qword `02CA99D0`, zeroes qword `+0xC8` and dword `+0xC0`, calls `00244960` with the qword read from `0208EA28` and `rcx`, `00247870(rcx, 0)` and `00247930(rcx, 100)` and returns 0; 18 zeroes `02CA99D0` and returns 0; any other kind tail-jumps to `005C5230` with the same arguments", [("0057E8E6", "je"), ("0057E8F4", "mov"), ("0057E903", "mov"), ("0057E921", "call"), ("0057E938", "call")]),
 ("0057EB30", "by the kind in dword `[rdx]`: 1 stores `rcx` in qword `02CA99D8`, zeroes qword `+0xC8` and dword `+0xC0`, calls `00244960` with the qword read from `0208EA28` and `rcx`, `00247870(rcx, 0)` and `00247930(rcx, 100)` and returns 0; 18 zeroes `02CA99D8` and returns 0; any other kind tail-jumps to `005C5230` with the same arguments", [("0057EB46", "je"), ("0057EB54", "mov"), ("0057EB63", "mov"), ("0057EB81", "call"), ("0057EB98", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`widgetmsg_interior.py`](../../_index/candidates/opus-widgetmsg-interior-1001/widgetmsg_interior.py): every "
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
