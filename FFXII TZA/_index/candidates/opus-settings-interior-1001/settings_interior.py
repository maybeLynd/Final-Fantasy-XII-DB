"""settings_interior.py [--apply] - interior citations for the F-frontier functions that the-settings-command-table.md
cited by entry only (OPUS, 2026-10-01). All 36 read by hand from the certified image; every rip target was resolved with
retool.py and every float constant read from the image.

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

P = os.path.join(DB, "19-Save-Load-Settings", "Game-Settings-Config", "the-settings-command-table.md")
ROWS = [
 ("00181390", "forwards its six arguments to `001B0A20`, with `001B1C00()` inserted as the first", [("001813AF", "call"), ("001813D6", "call")]),
 ("00198960", "swaps the two dwords of each pair `01DF176C`/`01DF1770`, `01DF18C8`/`01DF18CC` and `01DF1A24`/`01DF1A28`, and also writes each swapped pair to `01F80164`/`01F80168`, `01F802C0`/`01F802C4` and `01F8041C`/`01F80420`", [("0019896C", "mov"), ("00198972", "mov"), ("00198978", "mov"), ("00198990", "mov"), ("001989B4", "mov")]),
 ("001DC190", "forwards its four arguments to `00211200`, with `00210B30()` inserted as the first", [("001DC1AE", "call"), ("001DC1C2", "call")]),
 ("001DC1E0", "forwards its five arguments to `00211210`, with `00210B30()` inserted as the first", [("001DC1FE", "call"), ("001DC21A", "call")]),
 ("001E0920", "on the object at qword `+0xDF8` of `00796E20()`, calls `0079AEE0(it, i)` for i = 1 to 3; then calls `0079AE40(00796E20(), i, 0)` for i = `0x1C` to `0x98`", [("001E093E", "call"), ("001E0945", "cmp"), ("001E095D", "call"), ("001E0964", "cmp")]),
 ("001E0AA0", "when `00198790()` is non-null, tail-calls `00197710(it, dl, byte 2 of 001E0650(), byte 0 of 001E0650())`", [("001E0AAC", "call"), ("001E0AC4", "shr"), ("001E0AEA", "jmp")]),
 ("001E0CE0", "returns dword `+0x184` of the object at qword `+0xDF8` of `00796E20()`, negated when `00198790()` is non-null and `001976E0` on it returns non-zero", [("001E0CFA", "call"), ("001E0D0E", "mov"), ("001E0D1A", "cmovne")]),
 ("001E0D30", "returns dword `+0x188` of the object at qword `+0xDF8` of `00796E20()`, negated when `00198790()` is non-null and `001976F0` on it returns non-zero", [("001E0D4A", "call"), ("001E0D5E", "mov"), ("001E0D6A", "cmovne")]),
 ("00231400", "returns 0 or 1. After `00233050` and `00233110(rcx, stack block, 00233050(), rdx)`, the word at stack `+0xA2` indexes a 32-byte record of `[rcx+0x10]` (a negative word returns 0); when the record's float `+4` exceeds 0.001 (`008C5B2C`) it takes the height of the record's plane (floats `+0`/`+4`/`+8` through the point at `[rcx+8] + 16*word +0x10`) at the x and z of the point `rdx`; with `r9d` 0 that height replaces the y of a stack copy of the point, otherwise a height above the y returns 0. It then turns x and z plus the integers `+0x38`/`+0x3C` into a cell of the grid at `[rcx]` (cell sizes `+0x10`/`+0x14`, odd columns shifted by half a cell, bounds `+8`/`+0xC`, -1 outside) and calls `0022F830` on a stack query {callback `0022F8B0`, `rcx`, that cell, byte 6, the point}; it returns 1 when the query's dword `+0x20` stays 0", [("00231482", "comiss"), ("002314AA", "divss"), ("00231548", "idiv"), ("002315A9", "call"), ("002315B2", "cmove")]),
 ("00232160", "for a word `r8w` below `0x5000`: from `0x4000` up, tail-calls `00381D90([rcx+0x18] + 0x90*(r8w-0x4000), rdx, r9)`; below `0x4000`, copies the first 16 bytes of the 32-byte record `[rcx+0x10] + 32*r8w` to `rdx`; from `0x5000` up it does nothing", [("0023216B", "cmp"), ("0023218B", "shl"), ("00232193", "jmp"), ("002321A0", "shl"), ("002321BE", "mov")]),
 ("0023B2E0", "when `00229E20()` is non-zero: when `002DDDA0()` is 0, calls `00229ED0(1)` and tail-calls `00182FB0(1)`; when it is 1, calls `00229ED0(2)` and tail-calls `00182FB0(2)`; any other value does nothing", [("0023B2E4", "call"), ("0023B2ED", "call"), ("0023B2FE", "call"), ("0023B30C", "jmp"), ("0023B324", "jmp")]),
 ("0023E710", "calls `00244F50(0xF0, 0023E770, record)` with a stack record {dword 0, qword `ecx`, qword `dl`}", [("0023E72F", "mov"), ("0023E737", "lea"), ("0023E743", "mov"), ("0023E74B", "call")]),
 ("00290030", "stores `xmm0` at float `+0x1D7C` of the object at qword `+0x10F80` of `[0209BE80]`, when both are non-null", [("00290037", "test"), ("0029003C", "mov"), ("00290048", "movss")]),
 ("00290060", "with `[0209BE80]` and its qword `+0x10F80` non-null: calls `002C63D0` on that object, and when `002544B0()` returns 1 sets word `+0x1D78` of that object to `0x80` and bit 2 of its word `+0x1D7A`", [("0029007E", "call"), ("00290083", "call"), ("00290099", "mov"), ("002900A7", "or")]),
 ("00290190", "tail-calls `0016D6A0([0209BE80] + 0x8FA0, ecx)`", [("00290192", "mov"), ("00290199", "add"), ("002901A0", "jmp")]),
 ("00290280", "with qword `+0x10F80` of `[0209BE80]` non-null, sets bit 1 (when `ecx` is non-zero) or bit 0 (otherwise) of that object's word `+0x1D7A` to bit 0 of `dx`", [("00290293", "and"), ("002902A3", "and"), ("002902AB", "or"), ("002902B9", "and")]),
 ("00290C00", "with `[0209BE80]` non-null: calls `003F5070` on its qword `+0x10F10` when that is non-null, then tail-calls `003F7490` on its qword `+0x10F30` when that is non-null", [("00290C1C", "call"), ("00290C28", "mov"), ("00290C38", "jmp")]),
 ("002911D0", "looks up `edx` in the list at qword `+0x10F40` (`003F3580`); a found node gets float `+0x64` = `xmm2` and dword `+0x48` = `002713B0(r9d)`. Otherwise it allocates a `0x80`-byte node (`00273A30(0, [[0209BE80]+0x10FC0], 0x80)`), loads qword `+0x10F50` once through `0024A5A0([01E0C1E0])`, fills a stack record from an entry of the table at `[[+0x10F50]+0x20] + 0x30` (word +0 plus 2, word +2, dword +4 minus 4 in the low 12 bits and unchanged in bits 12-23), initialises the node with `003F3510` and stores `003F34D0(list, node)` back in `+0x10F40`; returns the node", [("00291204", "call"), ("00291211", "movss"), ("00291234", "call"), ("002912AF", "sub"), ("002912F0", "mov")]),
 ("002DE080", "sets bit 13 of the dword at `[0215E6E0]` to bit 0 of `ecx`, then tail-calls `0035FF30(0, that bit)`", [("002DE08A", "shl"), ("002DE08D", "and"), ("002DE093", "or"), ("002DE09F", "jmp")]),
 ("002DE160", "sets bit 9 of dword `+4` of `[0215E6E0]` to bit 0 of `ecx`, then tail-calls `001E0FF0(that bit)`", [("002DE16A", "shl"), ("002DE16D", "and"), ("002DE174", "or"), ("002DE180", "jmp")]),
 ("002DE190", "sets bit 8 of dword `+4` of `[0215E6E0]` to bit 0 of `ecx`, then tail-calls `001E1020(that bit)`", [("002DE19A", "shl"), ("002DE19D", "and"), ("002DE1A4", "or"), ("002DE1B0", "jmp")]),
 ("002DF4D0", "calls `001DC1E0(ecx, edx, r8d, r9d, 1 when 002DDE20() is 0 else 0)`", [("002DF4EE", "call"), ("002DF502", "sete"), ("002DF50B", "call")]),
 ("0032CA70", "calls `003CC130(rcx + 0x350, rcx + 0x60, ...)` with three output floats and returns 0 when the one written through `r9` is above 1.3962634 (`00D108C4`). Otherwise it calls `003CC480(0, the one written through r8 plus 0.25 01CEBB68, 0)` into a stack vector, applies `00202B70` to the stack vector (0, 0, 3.0 `008F311C`, 1.0 `01CEBBA8`) and that result and stores it as the 16 bytes at `+0x300`; runs `00232490` and `00231690` (with `0x13` and `01EED410`) on qword `+0x2C8`, then `00230C00` with 4 (when `00232490` returned 0 and `00231690`'s float is not strictly between 0 and 0.27 `00D108B4`) or -1 and the float 0.27, copying its 16-byte result to `+0x300` when it returns non-zero; finally copies the 16 bytes at `+0x350` to `+0x310` and returns 1", [("0032CAAD", "call"), ("0032CAB7", "comiss"), ("0032CB5F", "movups"), ("0032CBB4", "call"), ("0032CC10", "call")]),
 ("00342F80", "when `00267310(byte +0x15 of rdx)` is non-zero, tail-calls `00360960` with word `[r8]`, dword `[r8+0xC]` and the signed low nibble of byte `[r8+2]`; otherwise, when `00360C20()` is 5 and `002DEC00()` differs from word `[r8]`, tail-calls `002DED70` (the nibble non-zero, or dword `+0xC` positive with the word `0x5A` or `0x5B`), `002DECE0` (the nibble 0 and dword `+0xC` not positive) or `002DEC80` (the rest)", [("00342F8D", "call"), ("00342F9E", "cmp"), ("00342FAB", "cmp"), ("00342FC6", "lea"), ("00342FF9", "jmp")]),
 ("0035D280", "calls the function `rdx` on the node `rcx`, and `002A2720` on the node when that returns non-zero; then recurses over the children from qword `+0x18`, each call returning the next sibling; returns qword `+0x20`", [("0035D290", "call"), ("0035D299", "call"), ("0035D2B6", "call"), ("0035D2C0", "mov")]),
 ("0035D2D0", "calls the function `rdx` on the node `rcx`, and `00246AC0` on the node when that returns non-zero; then recurses over the children from qword `+0x18`, each call returning the next sibling; returns qword `+0x20`", [("0035D2E0", "call"), ("0035D2E9", "call"), ("0035D306", "call"), ("0035D310", "mov")]),
 ("0035E580", "returns 1 when `rcx` is non-null and bits 19 and 20 of its dword `+0x44` are both set, else 0", [("0035E587", "mov"), ("0035E58A", "and"), ("0035E596", "sete")]),
 ("0035FF30", "for `ecx` below 2, sets bit 2 of byte `+9` of the `0x294`-byte record `022CAE90 + 0x294*ecx` to `edx != 0`", [("0035FF38", "imul"), ("0035FF3F", "lea"), ("0035FF49", "and"), ("0035FF55", "or")]),
 ("00382020", "returns 1 when the float at `+4` lies strictly between -1.0 (`01CEBC9C`) and 1.0 (`01CEBBA8`) and `00861F14(x*x + z*z)` of the floats at `+0` and `+8` is below 1.0, else 0", [("00382036", "comiss"), ("0038203B", "comiss"), ("00382059", "call"), ("0038205E", "comiss")]),
 ("003EF290", "calls `002DEE50(002DEC00(), edx, 0)`; then, with `2*edx`, calls `003611F0(it, 1)` and `003634B0(it, 0)` and stores it in dword `+0xC8`; stores 6 in byte `+0xC0`", [("003EF2AB", "call"), ("003EF2B0", "add"), ("003EF2B9", "call"), ("003EF2C7", "mov"), ("003EF2D2", "mov")]),
 ("003F6B30", "fills a stack block with `00271360(block, rcx)`, writes six qwords (`0x1000000000000002`, `0xE`, `0x53001`, `0x47`, `0x44`, `0x42`) at the block's write pointer (qword `+0x10`) and advances it by `0x30` (the 16 bytes first copied there from `02064AB0` are overwritten), then calls `002712E0(rcx, block, 1)`", [("003F6B41", "call"), ("003F6B6A", "mov"), ("003F6B98", "add"), ("003F6BA1", "call")]),
 ("00405150", "with `[02B62D88]` and its qword `+0xC0` non-null: calls `00244DD0` on the latter when bit 20 of its dword `+0x40` is clear, and in either case sets bit 2 of dword `+0xC8` of `[02B62D88]`; when `+0xC0` is null, sets that bit only when bit 0 of `+0xC8` is set", [("0040516C", "test"), ("00405175", "call"), ("00405181", "or"), ("0040518D", "test")]),
 ("004052D0", "with `[02B62D88]` and its qword `+0xC0` non-null and bit 2 of its dword `+0xC8` set, calls `00246AD0([02B62D88], [+0xC0])` and clears that bit", [("004052EC", "test"), ("004052F5", "call"), ("00405301", "and")]),
 ("004082D0", "with `[02B62D80]` and its qword `+0xC0` non-null, tail-jumps to `00244DD0` on the latter when bit 20 of its dword `+0x40` is clear", [("004082DC", "mov"), ("004082E8", "test"), ("004082EF", "je")]),
 ("00408AA0", "with `[02B62D80]` and its qword `+0xC0` non-null, tail-jumps to `00246AD0` when the latter's dword `+0xD8` has bit 2 set and bit 3 clear", [("00408AB8", "mov"), ("00408ABE", "test"), ("00408AC2", "test"), ("00408AC4", "je")]),
 ("0046DB10", "tail-calls `0035EEB0(0, ecx, 0)`", [("0046DB12", "xor"), ("0046DB15", "xor"), ("0046DB17", "jmp")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`settings_interior.py`](../../_index/candidates/opus-settings-interior-1001/settings_interior.py): "
        "every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
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
