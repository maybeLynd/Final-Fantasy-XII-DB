"""CC-5 control (OPUS, 2026-09-27): the .ard trailer at +0x0C - layout, readers, and the shipped corpus.

T1  003EA650(idx) returns base + [base+0x0C] for base = [02B5E0C0 + idx*8], idx 0..1 (the two loaded .ard roots).
T2  0035A3A0 and 0035AC60 walk it as {u32 count; {u32 key; u32 mask}[count]}: key through 002EB7A0 (special-id remap)
    and 002E99C0 (definition lookup by +0x14), then per set mask bit a call to 002ECAB0; 0037C3F0 is the third caller.
T3  over every shipped .ard (unique by content) the trailer, when present, holds count >= 0 and 4 + 8*count bytes
    before the file's next section end; a zero offset means no trailer.
T4  every record's key has a lowercase ASCII letter in its high word (the definition-key convention).
Mutant M1: a trailer walked as 12-byte records overruns its span in some shipped file.
"""
import glob, hashlib, pathlib, struct, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE.parents[3] / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe = pefile.PE(data=raw, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, n): o = pe.get_offset_from_rva(a - IB); return list(md.disasm(raw[o:o + n], a))
# T1
t1 = {i.address: (i.mnemonic, i.op_str) for i in dis(0x3EA650, 88)}
assert t1[0x3EA654] == ("cmp", "ecx, 1") and t1[0x3EA671] == ("mov", "ecx, dword ptr [rbx + 0xc]")
assert t1[0x3EA688] == ("add", "rax, rbx")
# T2
for f in (0x35A3A0, 0x35AC60):
    ins = dis(f, 240); ops = [(i.mnemonic, i.op_str) for i in ins]
    assert ("mov", "ecx, dword ptr [rax]") in ops and ("lea", "r14, [rax + 4]") in ops
    assert ("add", "r14, 8") in ops, "8-byte records"
    calls = [int(i.op_str, 16) for i in ins if i.mnemonic == "call" and i.op_str.startswith("0x")]
    assert calls[:3] == [0x3EA650, 0x2EB7A0, 0x2E99C0] and 0x2ECAB0 in calls, [hex(c) for c in calls]
assert any(i.mnemonic == "call" and i.op_str == "0x3ea650" for i in dis(0x37C3F0, 0x300))
# T3 / T4
files = sorted(glob.glob(r"D:\FFXII_TZA_extract\**\*.ard", recursive=True))
uniq = {}
for f in files:
    b = open(f, "rb").read(); uniq.setdefault(hashlib.sha256(b).hexdigest(), b)
st = collections.Counter(); keys = collections.Counter(); over12 = 0
for b in uniq.values():
    assert b[:8] == b"FF12AR03"
    tr = struct.unpack_from("<I", b, 0xC)[0]
    if not tr: st["none"] += 1; continue
    slots = [x for x in struct.unpack_from("<8I", b, 0x10) if x]
    end = min([e for e in slots + [len(b)] if e > tr] + [len(b)])
    n = struct.unpack_from("<i", b, tr)[0]
    assert n >= 0 and 4 + 8 * n <= end - tr
    st["trailer"] += 1
    if 4 + 12 * n > end - tr: over12 += 1
    for k in range(n):
        key = struct.unpack_from("<I", b, tr + 4 + 8 * k)[0]
        hi = key >> 16
        assert 0x61 <= hi <= 0x7A, hex(key)
        keys[chr(hi)] += 1
assert over12 > 0, "M1: a 12-byte reading should overrun somewhere"
print("files", len(files), "unique", len(uniq), dict(st), "records by key letter", dict(keys), "M1 overruns", over12)
print("PASS")
