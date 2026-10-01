"""boot_interior.py - interior citations for the F-frontier functions that what-the-engine-fixes-at-boot.md cited by entry
only (OPUS, 2026-10-01). Every body was read by hand from the certified image (anchor_prep.py / retool.py); every
rip-relative address named in a sentence was resolved with retool's annotation.

Before writing, the script VERIFIES every anchor against the image: it must be an instruction boundary strictly inside its
function's extent (functions.tsv) and decode to the recorded mnemonic. Any mismatch -> FAILS, nothing written.
Then it appends one OPUS section to the page (byte-preserving, CRLF-aware, idempotent). Prints VERIFY lines,
PATCHED / ALREADY, FAILS n. Same pattern as opus-pfgate-interior-1001/pfgate_interior.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "00-Engine-Core-Runtime", "what-the-engine-fixes-at-boot.md")
ROWS = [
 ("0017D990", "calls `0017D9D0(*(01DF0000), 01F7F490)`, then tail-calls `0017D9D0(*(01DF0008), 01F7F4A0)`", [("0017D9A2", "call"), ("0017D9A7", "mov"), ("0017D9B9", "jmp")]),
 ("0017D9D0", "looks up `rcx` through `001D6F20(rcx, 1)`; on failure passes `008C58C0` to `0017D280`; otherwise reads the entry (size from `001D6EE0`) into a stack buffer through `001D6FA0`, calls the import at `008C2F78` on (buffer + 7, `008C58D0`), copies that many bytes from buffer + 7 to `rdx` through `00861EBA`, and releases the entry with `001D6E80`", [("0017D9FD", "call"), ("0017DA53", "call"), ("0017DA63", "call"), ("0017DA73", "call")]),
 ("0017E6E0", "calls `001DF340(*(01F82D20), 0x19, ecx)`, then `00198960(00198790(), ecx == 0)`, and tail-calls `0022A4F0`", [("0017E6F7", "call"), ("0017E6FE", "sete"), ("0017E70C", "call"), ("0017E716", "jmp")]),
 ("002216B0", "when the qword `01FD4138` is null, allocates `0x8D8` bytes through `00210EC0`, constructs them with `0021E570(object, ecx, edx)` and stores the result at `01FD4138`", [("002216C8", "cmp"), ("002216D7", "call"), ("002216EE", "call"), ("002216F4", "mov")]),
 ("0025A600", "stores `xmm0` at `02098DE0` and `xmm1` at `02098DE4`", [("0025A608", "movss"), ("0025A610", "ret")]),
 ("0026DB10", "divides `ecx` (2 when `ecx` is negative) by the dword `01DFE0B4` and tail-calls `00229F10` with the quotient", [("0026DB17", "js"), ("0026DB1B", "div"), ("0026DB23", "jmp")]),
 ("0026E1D0", "stores float constants into the dwords around `0209A6EC`, zeroes qwords beside them, sets the dword `0209A6FC` to 1, copies one 16-byte constant into the four 16-byte globals `0209A380`..`0209A3B0`, and tail-calls `0026E640`", [("0026E1E2", "movss"), ("0026E221", "mov"), ("0026E231", "movaps"), ("0026E24D", "jmp")]),
 ("0026F9F0", "clears the low three bits of byte `02F8F29E`, zeroes the dwords `02F8F220` and `02F8F238` and the 16 bytes at `02F8F228`, fills the 96 bytes `02F8F23C`..`02F8F29B` with `0x03`, and sets the word `02F8F29C` to `0x100`", [("0026F9F9", "mov"), ("0026FA12", "mov"), ("0026FA66", "movdqu"), ("0026FA6E", "mov")]),
 ("002AB7D0", "calls `00229E40`; when the result is 7, 8 or 11 stores `0x1C` at `01E0CDF8` and 1 at `0209CC38`, otherwise stores `0x18` at `01E0CDF8`", [("002AB7D4", "call"), ("002AB7DC", "test"), ("002AB7E9", "mov"), ("002AB802", "mov")]),
 ("0032EAF0", "fills the `0x100` bytes at `022C5AF0` with `0xFF` when `ecx` is non-zero, else with 0", [("0032EAF7", "lea"), ("0032EB03", "sbb"), ("0032EB08", "rep stosb")]),
 ("0032EB10", "fills the `0x100` bytes at `022C59F0` the same way, then sets bit 7 of byte `022C5A0F`", [("0032EB17", "lea"), ("0032EB28", "rep stosb"), ("0032EB2F", "or")]),
 ("00358510", "calls `00358450(0, 1)` and `00358450(1, 0)`, sets the bytes `022C7F99` and `022C7F98` to 0 and the byte `022C7F9A` to 1", [("0035851B", "call"), ("00358525", "call"), ("0035852A", "mov"), ("00358538", "mov")]),
 ("0035B270", "initialises 32 records of `0x20` bytes at `02EC0B80` (byte `+0` = index + 1, byte `+1` = 0, word `+2` = 0, qword `+8` = 0), then sets the byte `02EC0F60` to `0xFF`, clears further fields and sets the dword `02EC0B3C` to 1", [("0035B283", "mov"), ("0035B288", "mov"), ("0035B298", "cmp"), ("0035B2DC", "mov")]),
 ("0035E820", "resets the dwords and qwords around `022CA5E0`..`022CA62C` (`022CA62C` = -1), creates two objects through `00863540`, calls `008636E0` with a descriptor holding `0035EA40` and `0x4000` and passes its result to `00863610`, spins until the dword `022CA630` is non-zero, registers through `00369070(0, ...)`, and makes its `005C5230` calls", [("0035E8A7", "call"), ("0035E920", "call"), ("0035E930", "mov"), ("0035E943", "call")]),
 ("0035EB70", "compares `00368C70()` with `00862090()`; when they differ, spins until the qword `022CA5E0` has advanced by max(`ecx`, 1) and returns the advance; when they match, calls `0017D3E0` (and `003691B0(0)` / `00369190(0)` when it returns 0), recomputes its timing dwords, calls `0035E7A0` and records max(`ecx`, 1) and `edx`", [("0035EB90", "cmp"), ("0035EBB0", "mov"), ("0035EBC3", "sub"), ("0035EC05", "call")]),
 ("0035EC90", "increments the qword `022CA5E0` and the dword `022CA5F0`; when one dword counter has reached another it tests bit 13 of a mode-selected dword and may set the dword `022CA600` to 1; when that flag is set and the function pointer at `022CA5C8` is non-null, calls it and clears the pointer; then calls `0035FCA0` and tail-calls `003690F0`", [("0035EC94", "inc"), ("0035ECFE", "mov"), ("0035ED1E", "call"), ("0035ED34", "jmp")]),
 ("00368C80", "fills the block around `022D7F68` (an object from `00863540` at `022D7F68`, entry `00368C10`, `0x4000`), calls `0019C5D0`, `008636E0` and `00863610`; when a configured index is non-zero and the qword `022D7F70` (read once) is non-zero, calls `00863520` with `0x24` and `0x22`; with it zero the loop `00368D76`-`00368D81` does not re-read it", [("00368CC0", "call"), ("00368D41", "call"), ("00368D76", "test"), ("00368D93", "call")]),
 ("00368DD0", "creates two objects through `00863540`, fills a descriptor block with entry `00369100` and `0x4000`, and calls `0019C5D0`, `008636E0` and `00863610`", [("00368E06", "call"), ("00368E18", "call"), ("00368E7F", "call"), ("00368EA9", "call")]),
 ("00368ED0", "stores `00862090()`'s result at `022D7FB0` and passes it to `00863520` with `0x20`; runs `00368F70`, `00368DD0` and `00368C80`; creates an object through `00863540` stored at `022D7F90`; tail-calls `0035E820`", [("00368EE1", "mov"), ("00368EE7", "call"), ("00368EF6", "call"), ("00368F25", "jmp")]),
 ("00368F70", "when `003692C0()` has bit 2 set, creates an object through `00863540`, calls `008636E0` with a descriptor holding `00368AE0` and `0x4000`, passes the result to `00863610`, and stores `005C5230(callback, object)`'s result at `022CFF18`", [("00368F8E", "test"), ("00369000", "call"), ("0036901A", "call"), ("00369027", "mov")]),
 ("00369070", "stores `rdx` in the qword table at `022CFF10`, index `ecx`", [("00369073", "lea"), ("0036907A", "mov")]),
 ("003694D0", "calls `0032EAF0(0)` and `0032EB10(0)`, then tail-calls `0016D6A0` with 1 when `00408B50()` is 1, else with 0", [("003694D6", "call"), ("003694DD", "call"), ("003694E7", "cmp"), ("003694F2", "jmp")]),
 ("0036D260", "zeroes the qwords `022D8E30` and `022D8E38` and the dword `022D8E40`", [("0036D262", "mov"), ("0036D269", "mov"), ("0036D270", "mov")]),
 ("0036D8B0", "calls `0036C1D0(6, 5)`, `002DEE90(-1)`, `005C5230` and `002DEE90(-1)`, then tail-calls `0036C140`", [("0036D8BC", "call"), ("0036D8C4", "call"), ("0036D8C9", "call"), ("0036D8DA", "jmp")]),
 ("0036ECE0", "initialises two arrays of `0x18`-byte records, 2 at `022D9AB0` and 4 at `022D9AE0`: byte `+0` = 0, byte `+1` = index, word `+2` = 0 (1 in the second array), qwords `+4` and `+0xC` = 0, word `+0x14` = `0xFFFF`, word `+0x16` = 0", [("0036ECF0", "mov"), ("0036ED04", "mov"), ("0036ED30", "mov"), ("0036ED46", "jl")]),
 ("0036EFD0", "sets the byte `022D9B41` to 1, calls `002DF420(1)`, sets the byte `022D9B40` to 1 and tail-calls `002DF420(0)`", [("0036EFD9", "mov"), ("0036EFE0", "call"), ("0036EFE7", "mov"), ("0036EFF2", "jmp")]),
 ("0036F4D0", "calls in order `0036D280`, `00465F60(0x100)`, `003A1D50`, `00467BB0`, `0026E1D0`, `00382910`, `003ECF70`, `00475310` and `003ED820`, then tail-calls `00467AD0`", [("0036F4DE", "call"), ("0036F4E3", "call"), ("0036F501", "call"), ("0036F50A", "jmp")]),
 ("00376A80", "zeroes the byte `02ADBB30`, the dword `02ADBB34` and the dwords at `02ADBB40` + k*`0x90` for k = 0..7", [("00376A89", "mov"), ("00376A8F", "mov"), ("00376AB9", "mov")]),
 ("003773C0", "zeroes the dword `02ADBFC4` and the first dword of 128 `0x20`-byte records ending at `02ADCFC0` (walking down), then clears the byte `02ADBFC0` and the qwords `02ADBFC8` and `02ADBFD0`", [("003773C9", "mov"), ("003773D7", "mov"), ("003773DD", "jns"), ("003773E5", "mov")]),
 ("0037B390", "sets the bytes `02ADD931` = 1, `02ADD932` = 4 and `02ADD930` = 0, calls `0037B3D0`, then sets `02ADD931` = 0 and `02ADD933` = 3", [("0037B39B", "mov"), ("0037B3A9", "call"), ("0037B3B5", "mov")]),
 ("0037B3D0", "calls `0036B060(0xB)`; when the byte `02ADD930` differs from `02ADD931`, takes `0x3C0000` (when `02ADD930` is 3) or `0x400000`, calls `00369760(0xB)`, `0036D160(0xB)`, `0036D250` and `0036D240(size)`, stores that result and calls `00369D30(0xB, result, size, 0x100)`; finally sets the byte `02ADD932` to 4", [("0037B3F3", "cmovne"), ("0037B420", "call"), ("0037B43D", "call"), ("0037B442", "mov")]),
 ("0039AED0", "stores `xmm0` at `02EBEFFC` and `xmm1` at `02EBEFF8`, and copies four 16-byte constants to `02AEE5A0`..`02AEE5D0`", [("0039AEDF", "movss"), ("0039AEEE", "movups"), ("0039AF11", "movups")]),
 ("0039CD50", "between `0036C1D0(9, 10)` and `0036C140` allocates `0x20000` bytes through `0036A100` into `02AEED50`; then runs `003970D0`, calls `0039AED0` with one float constant in both arguments and `0039AF20` with another, sets the byte `02AEE910` to 8 and zeroes the dword `02AEE900` and the qword `02AEE908`", [("0039CD66", "call"), ("0039CD6B", "mov"), ("0039CD87", "call"), ("0039CD9B", "mov")]),
 ("003A1D50", "calls `004FE3C0` on `02EBEFC0` and `02EBEFD8`, clears a dword, then calls `004FE420(02EBEFC0, 0x200, 0)` and tail-calls `004FE420(02EBEFD8, 0x200, 0x200)`", [("003A1D5B", "call"), ("003A1D67", "call"), ("003A1D85", "call"), ("003A1D9D", "jmp")]),
 ("003ABB60", "in the block `*(02B3F528)`, zeroes dword `+0` and byte `+0x20` of 128 `0x70`-byte records; takes the first record whose dword `+0` is 0, increments the serial `02B3F504` (wrapping above `0xFFFFFF` to 1), stores (serial << 8) OR index at `+0`, copies a `0x50`-byte template (byte 0 = 7, byte 3 = 3) to `+0x20`, calls `003AC920`, and links the record at the end of the list headed at `02B3F508` / `02B3F510`", [("003ABB83", "mov"), ("003ABC03", "cmova"), ("003ABC1E", "mov"), ("003ABC48", "mov")]),
 ("003AC890", "when the qword `02B3F528` is 0, allocates `0x3800` bytes through `0036A100` between `0036C1D0(6, 6)` and `0036C140` and stores them there; then sets a float, a qword `0x10000` and a byte beside it, and tail-calls `003ABB60`", [("003AC8AF", "call"), ("003AC8B4", "mov"), ("003AC8D0", "mov"), ("003AC8E6", "jmp")]),
 ("003B16B0", "after `0036C1D0(8, 10)`, zeroes the `0x600` bytes at `02EBE5E0`, clears the dword `02EBEBE0` and a byte, calls `0024C460(7)` and tail-calls `0036C140`", [("003B16C3", "lea"), ("003B16D0", "call"), ("003B16DA", "mov"), ("003B16F4", "jmp")]),
 ("003B3E10", "zeroes 32 eight-byte entries from `02EBCC80` (byte `+0`, word `+2`, dword `+4`)", [("003B3E20", "mov"), ("003B3E27", "mov"), ("003B3E2D", "cmp")]),
 ("003D7F10", "zeroes the first dword of 32 `0x84`-byte records from `02EBBA00`", [("003D7F20", "mov"), ("003D7F23", "add"), ("003D7F29", "cmp")]),
 ("003ED820", "zeroes the qword `02B5F1B0` and the 16 bytes at `02B5F1A0`", [("003ED823", "mov"), ("003ED82E", "movdqa")]),
 ("004FE3D0", "unless dword `+0x14` is set, calls `003EC8A0` first; zeroes `+0`, `+8` and `+0x10`; when `rdx` is non-zero, allocates `rdx`*16 bytes through `003EC8D0(6, ...)`, stores the block at `+0` and `+8` and the count at `+0x10`", [("004FE3E6", "call"), ("004FE3ED", "mov"), ("004FE405", "call"), ("004FE411", "mov")]),
 ("00501750", "after `00501440`, reads a header from the byte stream at `rdx` (byte 0 to `+0x10`, `0xFF` ends; bytes 2 and 3 to `+0x12` / `+0x13`); for kind 0 or 1 with a non-zero count, allocates count*64 (kind 0) or count*1024 (kind 1) bytes through `0036A100` into `+0x20` and copies them from the stream through `00861EBA`; then calls `00503180` on each record of the list `003AA1F0(1, 0x50)` (stepping with `003AA240`); returns the advanced stream pointer, or 0 for another kind", [("00501771", "mov"), ("005017C1", "call"), ("005017D3", "call"), ("005017F3", "call")]),
 ("00536120", "makes `rcx` an empty self-linked list head (`+0` and `+8` = `rcx`), zeroes `+0x14` and `+0x18`, and sets `+0x10` to -1", [("00536125", "mov"), ("00536129", "mov"), ("00536130", "mov")]),
 ("00863540", "allocates 8 bytes through `00210EC0`, constructs them with `008632E0(object, [rcx+8], [rcx+4])`, passes 'non-null' to `0016D6A0` and returns the object", [("00863552", "call"), ("00863568", "call"), ("0086357D", "call")]),
 ("00863610", "passes '`rcx` non-null' to `0016D6A0`, stores `rdx` at `+0x20` of the record `rcx` points to, calls the import at `008C2330` with that record's `+8`, and returns 0", [("00863628", "call"), ("00863630", "mov"), ("0086363B", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*The functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`boot_interior.py`](../_index/candidates/opus-boot-interior-1001/boot_interior.py): every anchor is an "
        "instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
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
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
