"""timestop_interior.py [--apply] - interior citations for the F-frontier functions that the-time-stop-and-system-stop-registry.md cited
by entry only (OPUS, 2026-10-01). All 26 read by hand from the certified image; every rip target was resolved with retool.py
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

P = os.path.join(DB, "00-Engine-Core-Runtime", "System-Stop-Registry", "the-time-stop-and-system-stop-registry.md")
ROWS = [
 ("0017F250", "for a non-null `rcx`, tail-calls its virtual `+0x90`", [("0017F253", "je"), ("0017F255", "mov"), ("0017F258", "jmp")]),
 ("00229AB0", "tail-calls `002DF370(0x3F, 1, 1)` when `ecx` is non-zero, else `002DF370(0x3F, 0, 0)`", [("00229AB2", "mov"), ("00229AC1", "jmp"), ("00229ACB", "jmp")]),
 ("00238850", "calls `003846F0(0208E680, sign-extended ecx, 0)`, then tail-calls `00236C30(1)`", [("0023885A", "lea"), ("00238861", "call"), ("0023886F", "jmp")]),
 ("002544C0", "looks up `00255290(ecx AND 0x7FFF)`; a non-negative result tail-calls `00225CD0(result, -1)`; a negative one tail-calls `002260A0` when `ecx` is 11 and otherwise returns", [("002544C8", "and"), ("002544CE", "call"), ("002544E1", "jmp"), ("002544E6", "or"), ("002544F0", "jmp")]),
 ("002547C0", "stores `cx` in word `01E0C2B0` (its entry instruction), then tail-jumps to `003BBF90`", [("002547C7", "jmp")]),
 ("00264DC0", "returns 1 when qword `+0xC0` is non-null and both bit 0 of byte `+0x13` and dword `+0x170` of the `+0xC0` object are 0, else 0", [("00264DC7", "test"), ("00264DD0", "and"), ("00264DD3", "or"), ("00264DDE", "sete")]),
 ("0026B980", "calls `00226BE0(6, 0, 0, 0, ecx, flag)`, where flag is 1 when `edx` is 0, 0 when `edx` is positive, and for a negative `edx` 1 when `00377700()` is non-zero", [("0026B992", "call"), ("0026B9A0", "sete"), ("0026B9B3", "lea"), ("0026B9B6", "call")]),
 ("002DF640", "when `ecx` is -1, stores `r8d` in dword `01E0CF98` (through a compare and `cmovne` that store `r8d` either way)", [("002DF645", "mov"), ("002DF64E", "cmovne"), ("002DF652", "mov")]),
 ("002E06B0", "calls `0029D210(1)` and `00226160`, clears bits 0, 1, 9 and 20 of dword `0215F1D0`, calls `00267D40(1, 0)` and clears byte `0215F1B2`", [("002E06B9", "call"), ("002E06BE", "call"), ("002E06C3", "and"), ("002E06D2", "call"), ("002E06D7", "mov")]),
 ("002E2400", "calls `0029D210(ecx != 0)` and `00226160`, clears bits 0, 1, 9 and 20 of dword `0215F1D0`, calls `00267D40(1, 0)` and clears byte `0215F1B2`", [("002E2408", "setne"), ("002E240D", "call"), ("002E2417", "and"), ("002E2426", "call"), ("002E242B", "mov")]),
 ("002E2440", "calls `0029D290(m)`, m being (`ecx` != 0) plus 0x10 when `edx` is non-zero, then `002274E0`; sets bits 0, 1, 9 and 20 of dword `0215F1D0`, calls `00267D40(1, 1)` and sets byte `0215F1B2` to 1", [("002E2448", "setne"), ("002E2452", "cmove"), ("002E2455", "call"), ("002E245F", "or"), ("002E2475", "mov")]),
 ("002E24C0", "sets bit `ecx` of byte `0215F1B3`, then tail-jumps to `00404D70` when the byte is non-zero, else to `00404DC0`", [("002E24C7", "bts"), ("002E24CA", "mov"), ("002E24D2", "jne"), ("002E24D8", "jmp")]),
 ("002E24E0", "clears bit `ecx` of byte `0215F1B3`, then tail-jumps to `00404D70` when the byte is still non-zero, else to `00404DC0`", [("002E24E7", "btr"), ("002E24EA", "mov"), ("002E24F2", "jne"), ("002E24F8", "jmp")]),
 ("0034BB80", "tail-calls `0026B4E0(rcx, 00320790(003589B0(00263F10(00264010(00267E10(r9)))), 1))`", [("0034BB8C", "call"), ("0034BB93", "call"), ("0034BBA3", "call"), ("0034BBAF", "call"), ("0034BBBE", "jmp")]),
 ("00352000", "tail-calls `0026C5D0(00263FF0(00267E10(r9)))`", [("00352007", "call"), ("0035200E", "call"), ("0035201A", "jmp")]),
 ("0035A720", "with `edx` 0: sets bit 5 of byte `+9` and, when qword `+0x30` is non-null, calls `00233F50(rcx, 1)`, `002ED020` and `0026D6D0`; with `edx` non-zero: clears that bit, calls `00269D60(it, 0, 0)` on `002E97B0()` when that is non-null with dword `+0` not -1, then `0026A770(rcx, 0, 0)`; in both cases then calls `00226AB0` and tail-calls `00226A50`", [("0035A72D", "or"), ("0035A73D", "call"), ("0035A754", "and"), ("0035A77C", "call"), ("0035A791", "jmp")]),
 ("0035B4B0", "ORs `cl` into dword `02EC0B40`, then, among the 32 entries of 0x20 bytes from `02EC0B81`, sets byte `+0` to 3 where it is 2 and byte `+0x1B` shares a bit with `cl`", [("0035B4BA", "or"), ("0035B4C7", "cmp"), ("0035B4CC", "test"), ("0035B4D1", "mov"), ("0035B501", "sub")]),
 ("0035B510", "clears the bits of `cl` in dword `02EC0B40`, then sets back to 2 every byte `+0` that is 3 among the 32 entries of 0x20 bytes from `02EC0B81` (whatever `cl` was)", [("0035B51A", "not"), ("0035B51C", "and"), ("0035B530", "cmp"), ("0035B536", "mov"), ("0035B542", "add")]),
 ("003756B0", "zeroes a 0x60-byte and a 0x58-byte stack descriptor (`00861EC0`); returns 0 when qword `02ADB6D0` is null or dword `02ADB6D8` is not 1 to 4. Otherwise it fills the first descriptor with byte fields, `00182B20()`, `sil` and a qword of bit fields whose mode bits depend on `02ADB6D8` (values 3 and 4 also store the addresses `02ADB720` and `02ADB6E0`), packs the low nibbles of `002D8150(0x200)` and `002D8150(0x1C0)` into that qword, stores `00182B20(02ADB6D0)`, and stores `00375900` of the descriptor in dword `02EC07F4`; it fills the second descriptor (the 16 bytes at `009155F0`, `r14d` times 1/255 (`00D11104`) as a float, `sil`, the same qword), stores `00375900` of it in dword `02EC07F8` and returns 1", [("003756F4", "jne"), ("0037575A", "sub"), ("0037577C", "lea"), ("00375857", "call"), ("003758C2", "mov")]),
 ("003D9930", "copies dword `+0x64` to `+0x3CC`, then tail-jumps to `0032AEC0(rcx + 0x2B0)`", [("003D9933", "mov"), ("003D9939", "add"), ("003D9940", "jmp")]),
 ("0041D110", "calls `0041CFC0`, clears bit 12 of qword `+0x2C8`, sets bit 28 of dword `+0xC`, calls `0041D820` (`r8d` = 1, float `+0x344` in `xmm1`) unless that float is -1.0 (`01CEBC9C`), then clears bit 28 and stores 1 in word `+0x24`", [("0041D11D", "call"), ("0041D12E", "btr"), ("0041D13A", "or"), ("0041D15A", "call"), ("0041D166", "mov")]),
 ("00424A40", "when bit 20 of dword `+0x284` is set or `xmm1` is 0.0: calls `00426FA0`, sets bit 1 of dword `+0xC` of the `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC8)` record and calls `0041D790` on it when it exists, and returns `00424C40(rcx)`. Otherwise it returns 0 when the record for dword `+0xC4` exists with word `+0x24` = 1. Else, for that record: calls `0041D7E0` with floats `+0x2B0`, `+0x2B4` and `+0x2B8` and sets the three to -1.0; then calls `0041D790` (after setting bit 1 of its `+0xC` and its word `+0x24` to 1) or `0041D110`; stores 1.0 / `xmm1` in its float `+0x354`; sets bit 11 of its `+0xC` (and bit 17 when `r8d` is 1); clears bit 8 when its float `+0x344` is -1.0. It always ends with `00423AB0(rcx)` on float `+0x2BC`, returning 1 when the record existed, else 0", [("00424A56", "test"), ("00424A98", "or"), ("00424B29", "cmp"), ("00424B8A", "call"), ("00424BE5", "movss")]),
 ("0042E650", "calls `00420EA0(rcx, dword +0x38 of rdx)` when `00426220(rcx, qword +8 of rdx)` returns 0", [("0042E660", "mov"), ("0042E664", "call"), ("0042E66D", "mov"), ("0042E673", "call")]),
 ("00477E90", "for `cx` not -1, takes the 0x740-byte record (signed `cx`) of `[022C6F28]`; when its dword `+0x284` is non-zero and `003E55B0(record)` returns an object, tail-calls `00504800(object, edx)`; otherwise returns 0", [("00477EAA", "imul"), ("00477EBA", "cmp"), ("00477EC3", "call"), ("00477ED7", "jmp"), ("00477E9E", "xor")]),
 ("0051CC10", "clears byte `+4` of record `cl` of the 0x3C0-byte records at `[02CA8420]` when its dword `+0` equals `ecx`", [("0051CC13", "imul"), ("0051CC1A", "add"), ("0051CC21", "cmp"), ("0051CC25", "mov")]),
 ("0051CDC0", "stores `xmm1` in float `+8` of record `cl` of the 0x3C0-byte records at `[02CA8420]` when its dword `+0` equals `ecx`", [("0051CDC3", "imul"), ("0051CDCA", "add"), ("0051CDD1", "cmp"), ("0051CDD5", "movss")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*Functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`timestop_interior.py`](../../_index/candidates/opus-timestop-interior-1001/timestop_interior.py): every "
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
