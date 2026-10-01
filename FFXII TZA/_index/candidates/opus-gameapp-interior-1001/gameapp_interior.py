"""gameapp_interior.py - interior citations for the F-frontier functions that game-application.md cited by entry only
(OPUS, 2026-10-01). Every body was read by hand from the certified image (anchor_prep.py / retool.py); every rip-relative
address named in a sentence was resolved with retool's annotation (the IAT slot 008C2F70 by the PE import table).
Skipped: 0061D490 (1,211 B, several viewport / render-target paths with six 0061E6B0 calls - not stated in one honest
sentence here).

Before writing, the script VERIFIES every anchor against the image: it must be an instruction boundary strictly inside its
function's extent (functions.tsv) and decode to the recorded mnemonic. Any mismatch -> FAILS, nothing written.
Then it appends one OPUS section to the page (byte-preserving, CRLF-aware, idempotent). Prints VERIFY lines,
PATCHED / ALREADY, FAILS n. Same pattern as opus-boot-interior-1001/boot_interior.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "00-Engine-Core-Runtime", "Application-Root", "game-application.md")
ROWS = [
 ("001850B0", "calls `0062DD70` on `+0x298` and on `+0x108`, and stores the address `008C5D50` at `+0x190` and at `+0`", [("001850C4", "call"), ("001850D7", "mov"), ("001850DE", "call"), ("001850E3", "mov")]),
 ("00185FB0", "calls `00188730` and `0018B4E0` and sets the returned object's dword `+0x20` to -1; calls `00861EC0([this+0xDB0], 0, 0x17BB000)` and `00600070([this+8], [this+0xDB0])`; calls vtable slot `+0x10` of `[this+8]` and tail-calls `00610330([this+8])`", [("00185FBE", "call"), ("00185FCB", "mov"), ("00185FD9", "call"), ("00185FF5", "call"), ("00186001", "jmp")]),
 ("0018A820", "stores `dl` in byte `+0`; when it is 0 also clears the word at `+1`", [("0018A822", "test"), ("0018A826", "mov")]),
 ("00194AA0", "stores the dwords `0x49` at `+0` and `0x4A` at `+4`", [("00194AA6", "mov"), ("00194AAD", "ret")]),
 ("00194AB0", "calls `0016D6A0(qword 01F7FFD8 is null)`; when `01F7FFD8` is null, allocates 8 bytes through `00210EC0` and stores the block there", [("00194AC0", "call"), ("00194AD4", "call"), ("00194ADE", "mov")]),
 ("00198750", "when the qword `01F7FFE0` is null, allocates `0x40` bytes through `00210EC0`, constructs them with `00195060` and stores the result there", [("0019876C", "call"), ("0019877E", "call"), ("00198784", "mov")]),
 ("00199790", "when the qword `01F810F0` is null, allocates 1 byte through `00210EC0`, zeroes it and stores it there", [("001997A3", "call"), ("001997B2", "mov"), ("001997B5", "mov")]),
 ("0019F060", "when `edx` is non-zero, allocates `edx` * 0x18 bytes through vtable slot `+0x10` of the allocator at `+0x18`, then copies the 0x18-byte elements of [`r8`, `r9`) into the new block", [("0019F081", "lea"), ("0019F089", "call"), ("0019F0A9", "movups"), ("0019F0B2", "movsd")]),
 ("001A1130", "brings the count of 0x140-byte elements between `[rcx]` and `[rcx+8]` to `edx`: grows through `0019FC30` by the difference, or passes the excess range to `001A08F0`", [("001A1151", "imul"), ("001A117D", "call"), ("001A118A", "lea"), ("001A119F", "jmp")]),
 ("001A11B0", "when the qword `01F81160` is null, allocates `0x140228` bytes through `00584740`, constructs them with `0019F620` and stores the result there", [("001A11CC", "call"), ("001A11DE", "call"), ("001A11E4", "mov")]),
 ("001A1240", "while byte `+0x1A0` is set: when byte `+0x68` is set, sets `+0x69` and calls `005CCB80(1)`; otherwise clears `+0x69` and, between `005CD4F0(+0x28)` and `005CD820(+0x28)`, unlinks the first node of the list at `+0x50`, releases it through vtable slot `+0x18` of the allocator at `+0x60`, sets `+0x68` when the list is then empty, and passes the value it took (`+0x10` of the node at `+0x58`) to `001A07B0`; returns 0", [("001A1274", "call"), ("001A1285", "call"), ("001A12C4", "call"), ("001A12CD", "mov"), ("001A12E4", "call")]),
 ("001A1420", "allocates `edx` bytes through `0017D260(edx, 0x10)`, stores the block at `+0` and `+8` and its end at `+0x10`, and returns `rcx`", [("001A1436", "call"), ("001A143B", "mov"), ("001A144A", "mov")]),
 ("001A14E0", "calls `001A1420(rcx, 0x2000000)` and returns `rcx`", [("001A14E6", "mov"), ("001A14EE", "call")]),
 ("001ACF10", "stores `edx` at `+0x248`, then makes two objects through `001EE040(0x200, 0x200, ...)` with `02CF76E8` and `02CF79C0`, storing them at `+0xD0` and `+0xC8`", [("001ACF1A", "mov"), ("001ACF40", "call"), ("001ACF51", "mov"), ("001ACF71", "mov")]),
 ("001AD3E0", "calls `0016D6A0(qword 01F811C8 is null)`; when it is null, allocates `0x258` bytes through `00210EC0`, constructs them with `001AA9E0` and stores the result at `01F811C8`", [("001AD3FD", "call"), ("001AD410", "call"), ("001AD422", "call"), ("001AD42A", "mov")]),
 ("001AD8E0", "copies the 0x40-byte elements of [`rcx`, `rdx`) to `r8` - qword `+0` directly, the rest through `001AE4B0` - and returns the destination end", [("001AD923", "mov"), ("001AD92E", "call"), ("001AD94F", "mov")]),
 ("001ADAB0", "sets `[rcx]` = `r9`, then builds a copy of each 0x40-byte element of [`rdx`, `r8`) at `[rcx]` (qword `+0`, the rest through `0021A920`), advancing `[rcx]` by 0x40; returns `rcx`", [("001ADACB", "mov"), ("001ADAF5", "mov"), ("001ADB05", "call"), ("001ADB1D", "add")]),
 ("001ADB30", "builds `edx` copies of the 0x40-byte element at `r8` at `rcx` (qword `+0`, the rest through `0021A920`)", [("001ADB72", "mov"), ("001ADB7D", "call"), ("001ADB83", "add")]),
 ("001B1580", "calls `001B1630`, then `001AF470`, then tail-calls `001C6C00`, all on the same object", [("001B1589", "call"), ("001B1591", "call"), ("001B159B", "jmp")]),
 ("001B1BA0", "calls `0016D6A0(qword 01F811E8 is null)`; when it is null, allocates `0x4300` bytes through `00210EC0`, constructs them with `001ADD30` and stores the result at `01F811E8`", [("001B1BBD", "call"), ("001B1BD0", "call"), ("001B1BE2", "call"), ("001B1BEA", "mov")]),
 ("001B24D0", "fills the 16 qwords at `rcx` with `0x0000271000002710`, then stores `rcx + 0x40` at `+0x88` and `rcx` at `+0x80`; returns `rcx`", [("001B24DE", "mov"), ("001B2518", "mov"), ("001B251C", "mov"), ("001B2526", "mov")]),
 ("001B3320", "copies the 0x38-byte elements of [`rcx`, `rdx`) to `r8`: the first 0x20 bytes through `001A5760` (skipped when source and destination are the same), then qwords `+0x20`, `+0x28` and dword `+0x30`; returns the destination end", [("001B3353", "call"), ("001B335B", "mov"), ("001B336E", "mov"), ("001B3383", "mov")]),
 ("001B6BC0", "when the qword `01F81210` is null, allocates `0x20` bytes, zeroes `+0`..`+0x17`, calls `001EDF00(block + 0x18, 008C5F58)`, copies `+0` to `+8` and stores the block at `01F81210`", [("001B6BF2", "mov"), ("001B6C08", "call"), ("001B6C10", "mov"), ("001B6C19", "mov")]),
 ("001B7CE0", "returns 1 when `[rcx+0x28]` is null; otherwise looks for `[rcx+0x30]` on the chain from that record's `+0x50` through `+0x78`, and returns 1 only when it is found and the record's dword `+0x74` is non-zero", [("001B7CF6", "cmp"), ("001B7CFB", "mov"), ("001B7D05", "cmp"), ("001B7D0E", "mov")]),
 ("001B80C0", "with the count = dword `+0` without bit 31: returns 3 when `edx` is at or above the count; otherwise stores `r8` in slot `edx` - of the array at `[rcx+8]` when the count is above 1, else of the inline slots at `rcx+8` - and returns 0", [("001B80C2", "btr"), ("001B80CA", "mov"), ("001B80DB", "mov"), ("001B80F1", "mov")]),
 ("001B82A0", "when byte `+8` is set: calls `00229AE0(0)`, sets dword `+4` = 3, calls `0067A440(+0x678)` and `0067A970(+0x678, 0)`, and tail-calls `002E1C20(1, 0x15)`", [("001B82B1", "call"), ("001B82BD", "mov"), ("001B82D2", "call"), ("001B82E4", "jmp")]),
 ("001B9C80", "allocates a 0x58-byte node through vtable slot `+0x10` of the allocator at `+0x30`, copies 0x38 bytes from `rdx + 0x20` into node `+0x20`, sets node `+0x10` = `r8`, `+0` and `+8` = 0 and byte `+0x18` from `rdx`'s byte `+0x18`; returns the node", [("001B9C9F", "call"), ("001B9CAF", "movups"), ("001B9CCE", "mov"), ("001B9CE2", "mov")]),
 ("001BB120", "returns 0 unless `rdx` and its `+8` are set; otherwise asks `0019EB00(0019EF80(), [rdx+8])`, calls `001BAA30(rcx, rdx)` when the answer is true, and returns the answer", [("001BB143", "call"), ("001BB14E", "call"), ("001BB160", "call"), ("001BB165", "movzx")]),
 ("001BDA50", "calls `0016D6A0(qword 01F81248 is null)`; when it is null, allocates `0x108` bytes through `00210EC0`, constructs them with `001BC9D0` and stores the result at `01F81248`", [("001BDA6D", "call"), ("001BDA80", "call"), ("001BDA92", "call"), ("001BDA9A", "mov")]),
 ("001C0D40", "calls `0016D6A0(qword 01F81258 is null)`, then always allocates `0x1B8` bytes through `00210EC0`, constructs them with `001BE730` and stores the result at `01F81258` (0 when the allocation fails)", [("001C0D59", "call"), ("001C0D63", "call"), ("001C0D75", "call"), ("001C0D7B", "mov")]),
 ("001C0DD0", "when `[rcx]` is set, byte `+8` is clear and `0019EB00(0019EF80(), [rcx])` is true, calls `001BF2E0(rcx)` and sets byte `+8` to 1", [("001C0DE5", "cmp"), ("001C0DF6", "call"), ("001C0E02", "call"), ("001C0E07", "mov")]),
 ("001C1710", "atomically swaps byte `+0x10` with 0 and tail-jumps to `001C1810`", [("001C1712", "xchg"), ("001C1715", "jmp")]),
 ("001C18A0", "when the qword `01F81260` is null, allocates `0xA78` bytes through `00210EC0`, constructs them with `001C0E20` and stores the result there", [("001C18BC", "call"), ("001C18CE", "call"), ("001C18D4", "mov")]),
 ("001D5600", "zeroes qword `+0` and word `+8` and returns `rcx`", [("001D5607", "mov"), ("001D560A", "mov")]),
 ("001D58F0", "for 128 entries of 0x18 bytes from `+0x30`: zeroes the entry's first qword, copies the empty string `01CEB638` into the next 15 bytes through the CRT `strncpy` (IAT slot `008C2F70`) and zeroes the entry's byte `+0x17`; then zeroes dword `+0x1C`", [("001D5926", "mov"), ("001D5934", "call"), ("001D593E", "mov"), ("001D595A", "mov")]),
 ("001D6990", "calls `0016D6A0(qword 01F82CB8 is null)`; when it is null, allocates 8 bytes through `00210EC0`, zeroes them and stores the block there", [("001D69A0", "call"), ("001D69B4", "call"), ("001D69C3", "mov"), ("001D69CA", "mov")]),
 ("001D8AB0", "calls `001D8700`; when byte `+0x1C` is set, calls `001D8690`, adds the double argument (rounded to float) to float `+0x20` and to double `+0x10`, stores the new `+0x10` (as float) times the float at `01CEBC50` at `+0x18`, and passes that to `001D7A20(001D8210(), value)`", [("001D8AC6", "cmp"), ("001D8ADE", "addss"), ("001D8AE3", "addsd"), ("001D8AF6", "mulss"), ("001D8B0E", "call")]),
 ("001D8CD0", "when the qword `01F82CE0` is null, allocates `0x38` bytes through `00210EC0`, zeroes byte `+0`, bytes `+4`..`+0xF`, qword `+0x28` and dword `+0x30`, sets dword `+0x10` = 3 and stores the block there (0 when the allocation fails)", [("001D8CE3", "call"), ("001D8CF6", "mov"), ("001D8CFD", "mov"), ("001D8D0B", "mov")]),
 ("001DB500", "when the qword `01F82D00` is null, allocates `0x20` bytes, runs `001A1420(block, 0x800000)` and stores the block there", [("001DB51C", "call"), ("001DB52B", "mov"), ("001DB533", "call"), ("001DB539", "mov")]),
 ("001F0570", "stores the high 16 bits of `001DE5A0(*01F82D20)` at `+0x844` and the signed low 16 bits of a second such call at `+0x848`", [("001F0580", "call"), ("001F0585", "sar"), ("001F0588", "mov"), ("001F059A", "movsx")]),
 ("0020B840", "releases entries of the list at `+0x30` (sentinel `+0x28`) until `rdx` bytes are freed: an entry is skipped when its record (`+0x28`) has byte `+0x10` set or dword `+0x14` = 5, and, unless `r9b` is set, when its non-negative word `+0xE` equals word `+0xE8` of `[+0x18]` or its positive word `+0xC` equals dword `+0x80` (or `+0x84`, unless `r8b` is set); each release subtracts the record's dword `+8` from qword `+0x90`, calls `0020B0F0` and `002124C0(+0x98, ...)`, decrements `+0x48`, unlinks the entry and frees it through vtable slot `+0x18` of the allocator at `+0x50`; a pass that falls short is repeated once with `r8b` set", [("0020B894", "cmp"), ("0020B8BA", "cmp"), ("0020B8EB", "sub"), ("0020B914", "dec"), ("0020B93F", "call"), ("0020B970", "mov")]),
 ("0020BFA0", "tries `0020B130(this, size)`; when that fails, between `005CD4F0(+0x58)` and `005CD820(+0x58)` it releases entries of the `+0x30` list (the skip tests of `0020B840`) until max(3 * size, `0xBEBC200`) bytes are freed, falls back to `0020B840(this, remainder, 1, 0)` when short, retries `0020B130`, and repeats while that fails and its stop flag stays clear; returns the `0020B130` result", [("0020BFD0", "call"), ("0020BFEA", "call"), ("0020BFFA", "cmova"), ("0020C070", "sub"), ("0020C0F5", "call"), ("0020C10F", "call")]),
 ("0020E9F0", "calls `0016D6A0(1)`, allocates `0xC0` bytes through `001A1470(*01F7F4C0, 0xC0)`, stores `009068B8` at the block's `+0`, stores the block at `+8` and returns block `+0x10` (0 when the allocation fails)", [("0020E9FE", "call"), ("0020EA0F", "call"), ("0020EA23", "mov"), ("0020EA29", "mov"), ("0020EA32", "add")]),
 ("00292260", "for the ids 10, 20 and 14 in turn: when `002F8040(id)` is 0, calls `002491B0(rcx, id)`", [("0029226E", "call"), ("0029227D", "call"), ("00292296", "call"), ("002922B4", "jmp")]),
 ("002922C0", "when `002F8040(0x11)` is 0, tail-calls `002491B0(rcx, 0x11)`", [("002922CE", "call"), ("002922E2", "jmp")]),
 ("0035E700", "clears dword `022CA634`, calls `00863800` on the handles `*022CA610` and `*022CA618`, calls `008635F0(1)` while dword `022CA630` is non-zero, then calls `00863590` on both handles", [("0035E70B", "mov"), ("0035E715", "call"), ("0035E735", "call"), ("0035E74B", "call")]),
 ("00368AD0", "sign-extends `ecx` and tail-jumps to `00863800`", [("00368AD3", "jmp")]),
 ("00369050", "stores `rdx` at `022D7F70` and tail-jumps to `00863800` with the handle `*022D7F68`", [("00369057", "mov"), ("0036905E", "jmp")]),
 ("003690F0", "tail-jumps to `00863800` with the handle `*022D7F90`", [("003690F7", "jmp")]),
 ("00369100", "with the index = byte `[rcx]`: calls `0016D6A0(0x7C)`, then loops forever - `00863650` on the handle at the dword table `022CFEEC`, the callback at the qword table `022CFF10` when it is set, and, when `0017D3E0()` returns 0, `00863800` on the handle at the dword table `022CFEF0`", [("00369112", "call"), ("00369128", "call"), ("0036913A", "call"), ("0036914D", "call")]),
 ("003691B0", "tail-jumps to `00863800` with the handle in the dword table `022CFEEC` at index `ecx`", [("003691B3", "lea"), ("003691BA", "movsxd"), ("003691BE", "jmp")]),
 ("0050CE40", "passes the format string at `00D22938` (`++ debug_sound_info_regist ++ syncv = %ld`) and `0035E810()`'s result to `0017D280`, then calls `0016D6A0(1)` and tail-calls `0016D6A0`", [("0050CE44", "call"), ("0050CE53", "call"), ("0050CE5D", "call"), ("0050CE66", "jmp")]),
 ("0050D780", "resolves an id (`00267E10(r9)`, or word `[rdx]` when that is negative) to a record through `00358940(002640C0(), id)`; when the record's byte `+3` has top bits `0x60`, `002EA6A0(record)` is non-zero and `+0xC0` is set, passes the format string at `00D22A0C` (`%d `) and the signed byte `+0x14D` of `+0xC0` to `0017D280`", [("0050D7A0", "call"), ("0050D7B1", "call"), ("0050D7C5", "cmp"), ("0050D7F0", "call")]),
 ("0067A010", "unless dword `+0x260` is 1, repeats until it is: takes an item with `006CC4F0`, feeds its bytes (`+0x10`, count `+4`) to `0016DFE0(+0x2A8)` and calls `006CC550`; for each output `0016E040(+0x2A8)` yields it takes a slot with `006CC6A0(+0xA8, [+0x52C])` (stopping when there is none), waits with `006CC920` while dword `+0x2F0` minus `006CC580()` is below 3, writes the output's three sources (`+0x30`, `+0x38`, `+0x40` with the dwords `+0x50`, `+0x54`, `+0x58`) through `00679570` and submits with `006CC710`; finally calls `006CC670(+0xA8)` and clears byte `+0x2E8`", [("0067A06C", "call"), ("0067A091", "call"), ("0067A0D0", "call"), ("0067A107", "call"), ("0067A14D", "call"), ("0067A1B4", "call"), ("0067A214", "mov")]),
 ("0067F280", "copies the twelve floats at `rcx` (`+0`..`+0x2C`), the floats `+0x20`..`+0x28` of `rdx` and the float at `01CEBBA8` into stack operands, calls `001EB4B0` on them, and writes 48 bytes of the result back over `rcx` `+0`..`+0x2F`", [("0067F293", "movss"), ("0067F2CB", "movss"), ("0067F2D8", "movss"), ("0067F383", "call"), ("0067F3A3", "movups"), ("0067F3CA", "movss")]),
 ("008B1B10", "calls `001A49C0(02D3ECA8, *02D3ECC0)`", [("008B1B1D", "mov"), ("008B1B24", "lea"), ("008B1B2B", "call")]),
 ("008B1C00", "calls `0067F580(01F2EA70)`", [("008B1C0D", "lea"), ("008B1C14", "call")]),
]
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*The functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`gameapp_interior.py`](../../_index/candidates/opus-gameapp-interior-1001/gameapp_interior.py): every "
        "anchor is an instruction boundary inside its function and decodes to the recorded mnemonic. `0061D490` is not "
        "stated here (1,211 B, several paths).*\n\n"
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
