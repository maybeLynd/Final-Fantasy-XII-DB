"""sd6_input_source.py - is the recorded-input table [02EA5488] ever filled in retail? (OPUS, 2026-09-30; register SD-6)

Each fact below is re-read from the certified image and asserted. Uses the shared lookup tool
Database/Tools/analysis-kit/gfz-scripts/retool.py (its cached rip-reference / call scan over the v4 extents plus the UC-1 frontier).
Prints one PASS/FAIL line per fact and `FAILS n` last.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
c = T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins_at(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def refs(lo, hi=None):
    hi = hi or lo
    return sorted((g, f, a, k) for g, xs in c["refs"].items() if lo <= g <= hi for f, a, k in xs)


# F1 - the table's writers: the run loop 00796490 only clears it; the loader 0079FB10 passes its address on
w = [(g, f, a, k) for g, f, a, k in refs(0x02EA5480, 0x02EA548F) if k in ("W", "lea")]
clears = [x for x in w if x[1] == 0x00796490]
check("F1", all(ins_at(x[2]).op_str.endswith(("r14", "r14d", "edx")) for x in clears) and len(clears) == 4
      and any(x[1] == 0x0079FB10 and x[3] == "lea" for x in w),
      "stores to [02EA5480]/[02EA5488]: 00796490 x4 (r14 = 0 / edx = 0 after it: clears), lea by 0079FB10 (%s), teardown 008B7B90"
      % " ".join("%08X@%08X:%s" % (x[1], x[2], x[3]) for x in w))
# F1b - the other stores, in 008B7B90 (address taken at 00169510, a registered teardown), write zero: xor eax, eax first
tz = [ins_at(a) for a in (0x008B7BBD, 0x008B7BBF, 0x008B7BC6)]
check("F1b", tz[0].mnemonic == "xor" and tz[0].op_str == "eax, eax" and tz[1].op_str.endswith("rax") and tz[2].op_str.endswith("eax"),
      "008B7B90 frees the buffer (0x584730) and stores zero into [02EA5488]/[02EA5480] (008B7BBD..008B7BC6)")
# F2 - 0079FB10 is the input-log file loader: 'Error opening : %s' on failure, parses lines, grows the table via 007A0540
s = T.cstr(0x01CB29B0)
lea_site = [a for g, f, a, k in refs(0x02EA5480) if f == 0x0079FB10 and k == "lea"]
nxt = [i for i in R.md.disasm(R.at(lea_site[0], 16), lea_site[0], 2)][1] if lea_site else None
check("F2", s == "Error opening : %s" and nxt is not None and nxt.op_str == "0x7a0540",
      "0079FB10 logs %r on an unopened file; lea [02EA5480] then call %s" % (s, nxt.op_str if nxt else None))
# F3 - its only caller is the handler 00797A20, registered as the command 'InputSource' by 007A0180
cal = sorted(c["calls"].get(0x0079FB10, ()))
reg = [a for g, f, a, k in refs(0x00797A20) if f == 0x007A0180]
name_ok = False
if reg:
    # the name is the `lea r8, [string]` issued before the handler's `lea rdx, [00797A20]` (007A028E / 007A0298)
    body = [i for i in R.md.disasm(R.at(0x007A0180, reg[0] - 0x007A0180), 0x007A0180)]
    names = [i for i in body if i.mnemonic == "lea" and i.op_str.startswith("r8, [rip")]
    name_ok = bool(names) and T.cstr(names[-1].address + names[-1].size + names[-1].operands[1].mem.disp) == "InputSource"
check("F3", [f for f, _ in cal] == [0x00797A20] and name_ok,
      "callers of 0079FB10: %s; 00797A20 registered by 007A0180 under 'InputSource': %s" % (["%08X" % f for f, _ in cal], name_ok))
# F4 - the command objects (vtable 01CB24B8, 007A0180 registers the commands) are built only by 0079F150 and 00792760
cal2 = sorted(set(f for f, _ in c["calls"].get(0x007A0180, ())))
check("F4", cal2 == [0x00792760, 0x0079F150], "callers of the registrar 007A0180: %s" % ["%08X" % f for f in cal2])
# F5 - 0079F150 builds them only when [02EA5220] (the script path, 0079F1DD/0079F1E0) or [02EA5230] (the input source,
#      0079F2F2/0079F2F5, formatting 'InputSource(%s)\nFrames(%06i)\n') is non-null
g1, g2 = ins_at(0x0079F1DD), ins_at(0x0079F2F2)
check("F5", ins_at(0x0079F1CF).op_str.startswith("rbx, qword ptr [rip") and g1.mnemonic == "test" and ins_at(0x0079F1E0).mnemonic == "je"
      and ins_at(0x0079F2EB).op_str.startswith("r14, qword ptr [rip") and g2.mnemonic == "test" and ins_at(0x0079F2F5).mnemonic == "je"
      and T.cstr(0x01CB2C38) == "InputSource(%s)\nFrames(%06i)\n",
      "gates: test rbx ([02EA5220]) / test r14 ([02EA5230]), each je past the construction")
# F6 - 00792760's one caller is that gated site
cal3 = sorted(c["calls"].get(0x00792760, ()))
check("F6", cal3 == [(0x0079F150, 0x0079F211)], "callers of 00792760: %s" % ["%08X@%08X" % x for x in cal3])
# F7 - both globals are zero-initialised (beyond .data's raw bytes) and have exactly one reference each, a read
import pefile
pe = pefile.PE(R.b.EXE, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
d = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".data"][0]
bss = all(g - (base + d.VirtualAddress) >= d.SizeOfRawData for g in (0x02EA5220, 0x02EA5230))
r1, r2 = refs(0x02EA5220), refs(0x02EA5230)
check("F7", bss and [(f, a, k) for _, f, a, k in r1] == [(0x0079F150, 0x0079F1CF, "R")]
      and [(f, a, k) for _, f, a, k in r2] == [(0x0079F150, 0x0079F2EB, "R")],
      "zero-initialised: %s; references 02EA5220 %s, 02EA5230 %s" % (bss, r1, r2))
# F8 - no stored pointer to either global anywhere in the image, and no code address taken inside 02EA4100..02EA522F
qn = []
for s in pe.sections:
    data = s.get_data()
    for off in range(0, len(data) - 7, 8):
        if 0x02EA5210 <= struct.unpack_from("<Q", data, off)[0] <= 0x02EA5238:
            qn.append(base + s.VirtualAddress + off)
near = [x for x in refs(0x02EA4100, 0x02EA522F) if x[3] in ("W", "lea") and x[0] != 0x02EA5213]
check("F8", not qn and not near, "stored pointers to 02EA5210..02EA5238: %d; writes/leas in 02EA4100..02EA522F other than the byte "
      "02EA5213: %d" % (len(qn), len(near)))
# C1 control - the census does see a written neighbour: 02EA5213 is stored by the window procedure (00799137)
check("C1", any(f == 0x00798FF0 and a == 0x00799137 for _, f, a, k in refs(0x02EA5213)), "control: 02EA5213 written at 00799137")
print("FAILS %d" % fails)
