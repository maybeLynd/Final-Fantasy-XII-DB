"""sd103_slots.py - SD-103: who fills the drawing context's pointer slots +0x1060 / +0x1078 / +0x1090, and SD-104:
the 24-byte row itself (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py; the object-writer census
is Database/Tools/analysis-kit/gfz-scripts/objflow.py, whose output sd103_objflow.out this checker reads (re-run:
python -B objflow.py --ptr 0209CC40 --static 0209D490 0209E598 --region 0x1060 0x1098 --out sd103_objflow.tsv).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# C1 - the census (every function that loads [0209CC40] or addresses the static context 0209D490..0209E598, followed
#      through callees): of the stores that can reach [0x1060, 0x1098), one is the publisher's zero fill and the rest are
#      the row builder 002432B0 writing through ctx + 24 * row
out = open(os.path.join(HERE, "sd103_objflow.out"), encoding="utf-8").read()
reach = re.findall(r"^  (REGION|INDEXED-BELOW|INDEXED-UNKNOWN)\s+([0-9A-F]{8}) ([0-9A-F]{8}) (.*?)\s+size", out, re.M)
check("C1", "stores that can reach [0x1060, 0x1098): 6 in 2 functions" in out
      and sorted(set(f for _, f, _, _ in reach)) == ["002432B0", "008620A0"]
      and [r for r in reach if r[0] == "REGION"] == [("REGION", "008620A0", "008620A5", "jmp 0x861ec0")]
      and "escape 002B3550 002B356A" in out and "escapes 1, indirect calls carrying the object 0, recursion/depth cuts 0" in out,
      "census: only the zero fill (memset via 008620A0 from the publisher 002B3550) and 002432B0's row stores reach them")
# C2 - the three slots are the third qword (+0x10) of rows 174, 175 and 176 of the context's 24-byte row table (rows
#      end at 0x10C8, the control block: 178 rows fit)
check("C2", [24 * k + 0x10 for k in (174, 175, 176)] == [0x1060, 0x1078, 0x1090] and 0x10C8 // 24 == 179,
      "24*174+0x10 = 0x1060, 24*175+0x10 = 0x1078, 24*176+0x10 = 0x1090")
# C3 - 002B3480 builds the rows: rows 0.. from 0029CB50()'s records ([src+0x1C] of them) and rows 42.. (0x2A + k) from
#      0029CB60()'s, each by 002432B0(ctx + 24 * row, src, k, 0) - then calls 002B5C90, which reads the three slots
check("C3", txt(0x002B348A) == "call 0x29cb50" and txt(0x002B3492) == "call 0x29cb60" and txt(0x002B34CC) == "lea rcx, [rax + rax*2]"
      and txt(0x002B34D7) == "lea rcx, [rax + rcx*8]" and txt(0x002B34DB) == "call 0x2432b0" and txt(0x002B3506) == "add rax, 0x2a"
      and txt(0x002B351F) == "call 0x2432b0" and txt(0x002B3524) == "inc ebx" and txt(0x002B3529) == "jb 0x2b3500"
      and txt(0x002B352B) == "call 0x2b5c90" and txt(0x002B5F53) == "mov rcx, qword ptr [rbx + 0x1060]"
      and txt(0x002B601A) == "mov rcx, qword ptr [rbx + 0x1078]" and txt(0x002B60A6) == "mov rcx, qword ptr [rbx + 0x1090]",
      "002B3480: rows k <- source 1, rows 42 + k <- source 2, then 002B5C90 reads +0x1060 / +0x1078 / +0x1090")
# C4 - 002432B0 writes row +0x10: 0 when the record's elements need no storage, else 002497B0(size) - a buffer whose
#      first n qwords (n = the record's 10-bit count) are followed by the decoded elements
check("C4", txt(0x002432E3) == "and esi, 0x3ff" and txt(0x002432F2) == "lea ebx, [rsi*8]" and txt(0x0024338C) == "mov qword ptr [r15 + 0x10], 0"
      and txt(0x002433A5) == "call 0x2497b0" and txt(0x002433AA) == "mov qword ptr [r15 + 0x10], rax"
      and txt(0x002433B7) == "lea rbx, [rax + rsi*8]",
      "row +0x10 = 0 or 002497B0(8n + element sizes): n pointers, then the elements")
# C5 - so the slots hold source 2's records 132, 133 and 134 (rows 174 - 42 .. 176 - 42); the page's '+0x400 table' is
#      the same field of rows 42.. (0x400 = 24 * 42 + 0x10): [ctx + 24 * sel + 0x400] is source 2's record sel's buffer
check("C5", 174 - 42 == 132 and 176 - 42 == 134 and 24 * 42 + 0x10 == 0x400,
      "slots = source-2 records 132..134; '+0x400' = row 42 + sel's +0x10")
# C6 (SD-104) - the 24-byte row 002432B0 writes: dword +0x00 = the record's 10-bit ITEM COUNT shifted left by 2, bit 1
#      set, bit 0 = the record's bit 28; qword +0x08 = a pointer to the 20-byte source record (r12); qword +0x10 = the
#      list's one allocation (C4). The 10-bit field drives the walk (edx = esi, the loop at 00243340 runs that many
#      times) - a count, as a-typed-list-measured-once-and-built-in-one-allocation.md sections 3-5 already read it
check("C6", txt(0x002432E9) == "lea r12, [rax + r10*4]" and txt(0x00243305) == "mov qword ptr [r15 + 8], r12"
      and txt(0x002432FE) == "lea edx, [rsi*4]" and txt(0x00243313) == "and edx, 0x3fffc" and txt(0x0024331F) == "or edx, 2"
      and txt(0x00243329) == "shr ecx, 0x1c" and txt(0x00243333) == "mov dword ptr [r15], ecx"
      and txt(0x0024333A) == "mov edx, esi" and txt(0x00243382) == "sub rdx, 1" and txt(0x00243386) == "jne 0x243340",
      "row: +0x00 = count << 2 | 2 | bit 28 of the record, +0x08 = the source record, +0x10 = the allocation")
print("FAILS %d" % fails)
