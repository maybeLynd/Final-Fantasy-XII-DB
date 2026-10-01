"""SWE2-AUDIT-SEM independent check of FABLE's 6ffdbf87c: the ff12config state-clears row now says
0035F260 "clears 022CB3C0 + ch x 0x100 (0035F29A) and the channel record 022CAE90 + ch x 0x294 (0035F2E3) with two
memset calls, then initialises the record through rdi = 022CAE91 (record + 1)".

Decoded here with capstone from the certified image (Tools/work/exe/FFXII_TZA.exe) and pefile's import table - not
SWE2-DATA's in_channel_base.py, which the correction cites.

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-cfg-memset-0930/cfg_memset_sem.py"
"""
import os
import subprocess
import sys

import capstone
import pefile

EXE = os.path.join("Database", "Tools", "work", "exe", "FFXII_TZA.exe")
PAGE = "Database/FFXII TZA/19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md"
pe = pefile.PE(EXE, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def raw(va, n):
    o = pe.get_offset_from_rva(va - BASE)
    return bytes(pe.__data__[o:o + n])


def rip(i):
    for op in i.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


F = 0x0035F260
ins = []
for i in md.disasm(raw(F, 0x200), F):
    ins.append(i)
    if i.mnemonic == "ret":
        break
at = {i.address: i for i in ins}

# M0: 00861EC0 is memset (a jmp through the IAT slot VCRUNTIME140!memset)
j = next(md.disasm(raw(0x00861EC0, 8), 0x00861EC0))
slot = rip(j)
imp = {i.address: (e.dll.decode(), (i.name or b"").decode()) for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports}
check("M0 00861EC0 = jmp [IAT] -> VCRUNTIME140.dll!memset", j.mnemonic == "jmp" and imp.get(slot) == ("VCRUNTIME140.dll", "memset"),
      f"slot {slot:08X} {imp.get(slot)}")

# M1: body size 447 B (0035F260..0035F41E ret)
check("M1 0035F260 is 447 B", ins[-1].address + ins[-1].size - F == 447, str(ins[-1].address + ins[-1].size - F))

# M2: exactly two memset calls, both inside one loop
calls = [i for i in ins if i.mnemonic == "call" and i.operands[0].type == capstone.x86.X86_OP_IMM and i.operands[0].imm == 0x00861EC0]
check("M2 exactly two calls to memset", [c.address for c in calls] == [0x0035F2DE, 0x0035F2F2], ",".join("%08X" % c.address for c in calls))

# M3: first memset: rcx = rbp = lea 022CB3C0 (0035F29A), edx = 0, r8 = r15 = 0x100
check("M3 0035F29A lea rbp,[022CB3C0]", at[0x0035F29A].mnemonic == "lea" and at[0x0035F29A].op_str.startswith("rbp") and rip(at[0x0035F29A]) == 0x022CB3C0)
check("M3 r15d = 0x100 (0035F2C3), r8 = r15, rcx = rbp, edx = 0 before 0035F2DE",
      at[0x0035F2C3].op_str == "r15d, 0x100" and at[0x0035F2D0].op_str == "r8, r15" and at[0x0035F2DB].op_str == "rcx, rbp" and at[0x0035F2D9].op_str == "edx, edx")

# M4: second memset: rbx = rdi - 1 (0035F2E3), rdi = lea 022CAE91 (0035F2A8), r8d = 0x294, edx = 0
check("M4 0035F2A8 lea rdi,[022CAE91]", rip(at[0x0035F2A8]) == 0x022CAE91 and at[0x0035F2A8].op_str.startswith("rdi"))
check("M4 0035F2E3 lea rbx,[rdi-1]; rcx = rbx; r8d = 0x294; edx = 0",
      at[0x0035F2E3].op_str == "rbx, [rdi - 1]" and at[0x0035F2E9].op_str == "rcx, rbx" and at[0x0035F2EC].op_str == "r8d, 0x294" and at[0x0035F2E7].op_str == "edx, edx")

# M5: the loop runs esi = 0, 1 and steps rbp by 0x100 and rdi by 0x294 -> ch x 0x100 and ch x 0x294
check("M5 loop: add rbp,r15; add rdi,0x294; cmp esi,2; jl 0035F2D0",
      at[0x0035F3DF].op_str == "rbp, r15" and at[0x0035F3E2].op_str == "rdi, 0x294" and at[0x0035F3E9].op_str == "esi, 2"
      and at[0x0035F3EC].mnemonic == "jl" and at[0x0035F3EC].operands[0].imm == 0x0035F2D0 and at[0x0035F2AF].op_str == "esi, r14d")

# M6: after the memsets the record is initialised through rdi (record + 1): [rdi+1], [rdi+3], [rdi+8] ... and [rbx] (record + 0)
inits = [i for i in ins if 0x0035F2F7 <= i.address < 0x0035F360 and i.mnemonic in ("mov", "or", "and") and "[rdi" in i.op_str.split(",")[0]]
check("M6 the record initialisers after the memsets write through rdi (record + 1)", len(inits) >= 15, str(len(inits)))

# M7: the two memset ranges tile 022CAE90..022CB3B8 (two 0x294 records) and 022CB3C0..022CB5C0 (two 0x100 blocks)
check("M7 two 0x294 records end at 022CB3B8 (the page's 0x528-byte channel block)", 0x022CAE90 + 2 * 0x294 == 0x022CB3B8)

# P: the page at HEAD carries the corrected text and strikes the old phrase
page = subprocess.run(["git", "show", "HEAD:" + PAGE], capture_output=True, check=True).stdout.decode("utf-8")
row = [l for l in page.splitlines() if l.startswith("| state clears |")]
check("P1 one state-clears row", len(row) == 1)
r = row[0] if row else ""
check("P2 old phrase struck, new phrase present",
      "~~sweeps the `022CBxxx` flag cells and `022CAE91` with two `memset` calls~~" in r
      and "clears `022CB3C0` + ch x `0x100` (`0035F29A`) and the channel record `022CAE90` + ch x `0x294` (`0035F2E3`)" in r
      and "`rdi` = `022CAE91` (record + 1)" in r)
check("P3 NOTE the row's site column still cites 0035F26F (push rdi, a prologue instruction), unchanged by 6ffdbf87c",
      "`0035F26F` / `0046E00E`" in r and at[0x0035F26F].mnemonic == "push")

print("FAILS", len(FAILS))
sys.exit(1 if FAILS else 0)
