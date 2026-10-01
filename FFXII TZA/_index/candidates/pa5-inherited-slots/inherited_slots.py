"""inherited_slots.py - PA-5: what the deferred requests and slots 29/30 of the inherited PApplication do
(FABLE, Claude Opus 5.5, 2026-09-26).

Slots 12, 13, 18 and 19 only record a request (flag byte plus arguments; the Phyre application page). The inherited
per-frame update, slot 28 0079C140, consumes the requests:
  R1 flag +0x20 (slot 12; argument +0xD20) is a screen-mode change. It logs "change to full screen" when +0xD20 is set,
     else "change to window screen"; applies +0xD24/+0xD28 as the resolution through 00629690; and on failure logs
     "Change FullScreen Failed Return to Window Mode".
  R2 flag +0x22 (slot 19) is a monitor re-check: "Main Screen change", "Monitor no change", "Reset Screen Mode".
  R3 flag +0x21 (slot 13; argument +0x26) calls 0079F0F0, which is ShowWindow(hwnd, 9 = restore) when the argument
     is set, else ShowWindow(hwnd, 6 = minimise) ("FocusCallBack RESTORE" / "MINMIZE").
  R4 flag +0x29 (slot 18; arguments +0x2C/+0x30) resizes through 0062AAB0(device, [+0x2C], [+0x30]).
  S29 007A08A0 returns 9 when +0x69 is set. Otherwise it runs vtable +0x48 on the first call only (+0x64 == 0),
     increments the frame counter +0x64, and tail-jumps to 0079BDF0, the playback reader ("Frames",
     "Unrecognised command %s(%s)").
  S30 0079E880 returns 0x13 without a stream at +0xD98. Otherwise it formats "%d:%s:%s:+:%d" (frame +0x64 first) into a
     0xFF buffer and hands the line and its strlen to 0059F450 on that stream: an input RECORDER, not a parser.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def S(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
def s(a): return d[off(a):off(a) + 120].split(b"\0")[0].decode("latin1")
def lea_target(ins, at):
    t = ins[at].split("rip + ")[1].rstrip("]"); nxt = min(k for k in ins if k > at)
    return nxt + int(t, 16)
def imp(slot):
    r = struct.unpack_from("<I", d, off(slot))[0]; return d[off(BASE + r + 2):off(BASE + r + 2) + 40].split(b"\0")[0].decode()
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

U = S(0x79C140, 0x57C)
check("R1 +0x20/+0xD20 screen-mode change",
      U[0x79C3A6] == "cmp byte ptr [rdi + 0x20], bl" and U[0x79C3E7] == "cmp byte ptr [rdi + 0xd20], 0"
      and "full screen" in s(lea_target(U, 0x79C3F0)) and "window screen" in s(lea_target(U, 0x79C424))
      and U[0x79C3D0] == "mov ecx, dword ptr [rdi + 0xd24]" and U[0x79C444] == "call 0x629690"
      and "Return to Window Mode" in s(lea_target(U, 0x79C498)))
check("R2 +0x22 monitor re-check", U[0x79C30F] == "cmp byte ptr [rdi + 0x22], bl" and U[0x79C318] == "mov byte ptr [rdi + 0x22], bl"
      and "Main Screen change" in s(lea_target(U, 0x79C34E)) and "Monitor no change" in s(lea_target(U, 0x79C357))
      and "Reset Screen Mode" in s(lea_target(U, 0x79C384)))
F = S(0x79F0F0, 0x4F)
check("R3 +0x21/+0x26 focus: ShowWindow 9 / 6",
      U[0x79C56C] == "cmp byte ptr [rdi + 0x21], 0" and U[0x79C572] == "movzx ecx, byte ptr [rdi + 0x26]" and U[0x79C576] == "call 0x79f0f0"
      and imp(0x8C2928) == "ShowWindow" and F[0x79F0FF] == "mov edx, 9" and F[0x79F11F] == "mov edx, 6"
      and s(lea_target(F, 0x79F10A)).startswith("FocusCallBack RESTORE") and s(lea_target(F, 0x79F12A)).startswith("FocusCallBack MINMIZE"))
check("R4 +0x29 resize to +0x2C/+0x30", U[0x79C57F] == "cmp byte ptr [rdi + 0x29], 0" and U[0x79C5B0] == "mov r8d, dword ptr [rdi + 0x30]"
      and U[0x79C5B4] == "mov edx, dword ptr [rdi + 0x2c]" and U[0x79C5BA] == "call 0x62aab0" and U[0x79C5BF] == "mov byte ptr [rdi + 0x29], 0")
A = S(0x7A08A0, 0x41); P = S(0x79BDF0, 0x177)
check("S29 status 9 / first-call init / frame counter / playback reader",
      A[0x7A08A6] == "cmp byte ptr [rcx + 0x69], 0" and A[0x7A08AF] == "mov eax, 9" and A[0x7A08BA] == "cmp dword ptr [rcx + 0x64], 0"
      and A[0x7A08C3] == "call qword ptr [rax + 0x48]" and A[0x7A08CA] == "inc dword ptr [rbx + 0x64]" and A[0x7A08D6] == "jmp 0x79bdf0"
      and s(lea_target(P, 0x79BE22)) == "Frames" and s(lea_target(P, 0x79BEE6)).startswith("Unrecognised command"))
R = S(0x79E880, 0x318)
check("S30 recorder: 0x13 without a stream; formatted line + strlen -> 0059F450 on +0xD98",
      R[0x79E889] == "cmp qword ptr [rcx + 0xd98], 0" and R[0x79E896] == "mov eax, 0x13"
      and s(lea_target(R, 0x79E9DF)) == "%d:%s:%s:+:%d\n" and R[0x79E9DB] == "mov r9d, dword ptr [r14 + 0x64]"
      and R[0x79E9EA] == "mov edx, 0xff" and R[0x79EA03] == "call 0x19c5d0" and R[0x79EA13] == "cmp byte ptr [rbx + r8], 0"
      and R[0x79EA1A] == "mov rcx, qword ptr [r14 + 0xd98]" and R[0x79EA24] == "call 0x59f450")
W = S(0x59F450, 0x3A)
check("S30 0059F450 advances the stream position by the length it is given",
      W[0x59F463] == "call qword ptr [rax + 0x28]" and W[0x59F46A] == "add dword ptr [rbx + 0x18], edi" and W[0x59F45D] == "mov edi, r8d")
print("FAILS", fails)
sys.exit(1 if fails else 0)
