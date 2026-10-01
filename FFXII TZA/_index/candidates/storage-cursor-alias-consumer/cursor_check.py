"""cursor_check.py - 00866A00 stores each byte before it increments the cursor in memory, and reloads the cursor every
iteration (FABLE, Claude Opus 5.5, 2026-09-28). Static binding plus a byte-level model of exactly that order.
  K1  order in the loop: cursor load 00866A3D, bound cmp/jae 00866A42/44, byte load 00866A46, store 00866A4D,
      cursor increment in memory 00866A54, loop test 00866A57/5A; the return is sete(copied == requested) at 00866A61-64
  K2  ASTRA's cases on vector 0A 14 28 3C, cursor 0, the cursor dword and the destination in one little byte space:
      count 1 disjoint -> returns 1, cursor 1, dest 0A; count 1 dest == cursor -> returns 1, cursor 0x0B, dest 0B;
      count 2 aliased -> copies 1, cursor 0x0B (past the 4-byte vector), returns 0
  C   controls: count 2 disjoint copies 2 and returns 1; count 0 aliased copies nothing, cursor 0, returns 1
"""
import os, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
B = {int(p[0], 16): p[2].split(" ;")[0] for p in (l.rstrip("\n").split(None, 2) for l in open(CACHE, encoding="utf-8", errors="replace")) if len(p) == 3 and p[1] == "00866A00"}
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
want = {0x00866A3D: "mov ecx, dword ptr [r9]", 0x00866A42: "cmp ecx, eax", 0x00866A44: "jae 0x866a5c", 0x00866A46: "movzx edx, byte ptr [rcx + rdx]",
        0x00866A4D: "mov byte ptr [r10 + rdi], dl", 0x00866A54: "inc dword ptr [r9]", 0x00866A57: "cmp r10, rsi", 0x00866A5A: "jl 0x866a30",
        0x00866A61: "cmp r11d, r8d", 0x00866A64: "sete bl"}
ok("K1", all(B.get(a) == s for a, s in want.items()), "store 00866A4D precedes the in-memory increment 00866A54; the cursor is reloaded at 00866A3D each pass")
def run(count, alias):
    mem = bytearray(64); CUR = 0; DST = CUR if alias else 16         # cursor dword at 0; destination at 0 (aliased) or 16
    vec = bytes([0x0A, 0x14, 0x28, 0x3C]); copied = 0; i = 0
    while i < count:
        cur = int.from_bytes(mem[CUR:CUR + 4], "little")              # 00866A3D
        if cur >= len(vec): break                                     # 00866A42 / 44
        mem[DST + i] = vec[cur]; copied += 1                          # 00866A46 / 4D (r11d counts)
        i += 1
        mem[CUR:CUR + 4] = ((int.from_bytes(mem[CUR:CUR + 4], "little") + 1) & 0xFFFFFFFF).to_bytes(4, "little")   # 00866A54
    return int(copied == count), int.from_bytes(mem[CUR:CUR + 4], "little"), bytes(mem[DST:DST + max(count, 1)]), copied
r1 = run(1, False); r2 = run(1, True); r3 = run(2, True)
ok("K2", r1[:3] == (1, 1, b"\x0a") and r2[:3] == (1, 0x0B, b"\x0b") and (r3[0], r3[1], r3[3]) == (0, 0x0B, 1),
   "count 1 disjoint %s; count 1 aliased %s; count 2 aliased (returns, cursor, copied) %s" % (r1[:3], r2[:3], (r3[0], r3[1], r3[3])))
c1 = run(2, False); c0 = run(0, True)
ok("C", (c1[0], c1[1], c1[3]) == (1, 2, 2) and (c0[0], c0[1], c0[3]) == (1, 0, 0), "count 2 disjoint %s; count 0 aliased %s" % ((c1[0], c1[1], c1[3]), (c0[0], c0[1], c0[3])))
print("FAILS", fails); sys.exit(1 if fails else 0)
