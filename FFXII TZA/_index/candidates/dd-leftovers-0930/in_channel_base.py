"""Input-stack channel record: one base for every reader and writer (SWE2-DATA 2026-09-30), static.

The record is R = 022CAE90 + channel * 0x294. Each site below is pinned to the instruction that forms its pointer and
the displacement it applies, so every field reads as R + k:
  B1 the updater 0035FCA0 walks rbx = 022CAE90, += 0x294, bumps the write cursor byte [rbx] (R+0) mod 16, clears
     flag bit 4 of [rbx+9] (R+9), and calls the poll with rcx = rbx (0035FD8A) - so the poll's and the transition
     builders' 'channel' pointer IS R;
  B2 the mask accessors form R themselves (lea 022CAE90; imul 0x294) and index from the read cursor [R+1];
  B3 GetHistoryLookbackCount 0035F130 reads [022CAE98 + ch*0x294] = R+8;
  B4 0035FF90 walks rdi = 022CAE98 (R+8): [rdi-8] is R+0 (write cursor), [rdi-7] R+1 (read cursor); it stores
     R+8 = write - read (0035FFE1) and moves the read cursor R+1 (0035FFFA);
  B5 the initialiser 0035F260 is the one site that addresses the record from R+1: rdi = 022CAE91 and rbx = rdi-1 = R,
     so its [rdi] is R+1, [rdi+1] R+2 (the channel index), [rdi+3] R+4 (dword 0x50C: the repeat delays R+4 = 0x0C,
     R+5 = 0x05), [rdi+8] R+9 (the flags byte);
  B6 the repeat filter 0035FBD0 reloads its countdowns from the channel's +4 / +5 through the same pointer the
     builders receive (R).
  B7 the poll 0035F420 receives R (B1), reads the channel index [R+2] (0035F43A) and calls both builders with rcx = R
     (0035F514 / 0035F526); the analog builder 0035F760 keeps it in rsi (0035F774) and reads the dead zone [R+0x0D]
     (0035F7BD, 0035F83F), the flags [R+9] (0035F8A9), the stick threshold [R+3] (0035F8AE) and the scale byte
     [R+0x0C] (0035F90D);
  B8 so, in the builders' base, the initialiser writes R+3 = 0x68 ([rdi+2], 0035F319), R+0x0B..R+0x0C = word 0x0090
     ([rdi+0xA], 0035F31D: R+0x0B = 0x90, R+0x0C = 0), R+0x0D = 0x20 ([rdi+0xC], 0035F323) and clears flag bit 1 of
     R+9 ([rdi+8] and 0xFD, 0035F34B): the dead-zone radius the analog builder reads starts at 0x20, not 0.
Controls: C1 a mask accessor reads its frame word at R + 0x48 + 36*i (ring R+0x44, field +4) - the page's §10
layout; C2 the lookback accessor's base differs from the mask accessors' by exactly 8; C3 the initialiser's own
R-based store (rbx = R) of the frame rest bytes uses the same displacement +0x58 over R + 36*cursor as the analog
builder's frame stores over rdi = R + 36*cursor (0035F3AD vs 0035F835 / 0035F866), so the one-byte shift is confined to
the rdi-based stores - the control would fail if the initialiser's whole body used another base.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: x for x in dis(fn)}


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


u = ins(0x0035FCA0)
check("B1 updater: rbx = 022CAE90, write cursor [rbx] += 1 mod 16, flags [rbx+9], poll called with rcx = rbx, rbx += 0x294",
      rip_t(u[0x0035FCB7]) == 0x022CAE90 and u[0x0035FCE0].op_str == "eax, byte ptr [rbx]"
      and u[0x0035FCEE].op_str == "byte ptr [rbx], al" and u[0x0035FCE8].op_str == "byte ptr [rbx + 9], 0xef"
      and u[0x0035FD8A].op_str == "rcx, rbx" and u[0x0035FD92].op_str == "rbx, 0x294")
a = ins(0x0035EF10)
check("B2 mask accessor: R = 022CAE90 + ch*0x294, read cursor [R+1]",
      rip_t(a[0x0035EF25]) == 0x022CAE90 and a[0x0035EF1E].op_str == "rdx, rax, 0x294"
      and a[0x0035EF2F].op_str == "ecx, byte ptr [rdx + 1]")
check("C1 control: the accessor's word is R + 0x48 + 36*i (ring +0x44, field +4)",
      a[0x0035EF59].op_str == "rax, 2" and a[0x0035EF5D].op_str == "rax, [rax + rax*8]"
      and a[0x0035EF61].op_str == "eax, word ptr [rdx + rax*4]")
l = ins(0x0035F130)
check("B3 lookback accessor reads [022CAE98 + ch*0x294] = R + 8", rip_t(l[0x0035F13A]) == 0x022CAE98)
check("C2 control: the two accessor bases differ by exactly 8", rip_t(l[0x0035F13A]) - rip_t(a[0x0035EF25]) == 8)
f = ins(0x0035FF90)
check("B4 0035FF90: rdi = R+8; [rdi-8] write cursor, [rdi-7] read cursor; R+8 = write - read; read cursor stored",
      rip_t(f[0x0035FFB1]) == 0x022CAE98 and f[0x0035FFC7].op_str == "ecx, byte ptr [rdi - 7]"
      and f[0x0035FFCD].op_str == "ebx, byte ptr [rdi - 8]" and f[0x0035FFE1].op_str == "byte ptr [rdi], al"
      and f[0x0035FFFA].op_str == "byte ptr [rdi - 7], bl" and f[0x0035FFFD].op_str == "rdi, 0x294")
n = ins(0x0035F260)
check("B5 initialiser: rdi = 022CAE91 = R+1, rbx = rdi-1 = R; [rdi+3] dword 0x50C = R+4..R+7; [rdi+8] = R+9 flags",
      rip_t(n[0x0035F2A8]) == 0x022CAE91 and n[0x0035F2E3].op_str == "rbx, [rdi - 1]"
      and n[0x0035F312].op_str == "dword ptr [rdi + 3], 0x50c" and n[0x0035F30C].op_str == "byte ptr [rdi + 8], al"
      and n[0x0035F301].op_str == "byte ptr [rdi + 1], sil")
rf = dis(0x0035FBD0)
d45 = [x for x in rf if re.search(r"byte ptr \[r\w+ \+ [45]\]", x.op_str)]
for x in d45:
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
rfd = {x.address: x for x in rf}
bd = ins(0x0035FAC0)
check("B6 the repeat filter reads +4 / +5 (the delays) through r11 = its rcx, and the digital builder passes rcx = r10 = "
      "its own channel argument (the poll's R)",
      len(d45) >= 2 and rfd[0x0035FBF6].op_str == "r11, rcx" and bd[0x0035FAD1].op_str == "r10, rcx"
      and bd[0x0035FBB1].op_str == "rcx, r10")
pl = ins(0x0035F420)
an = ins(0x0035F760)
check("B7 poll: [R+2] channel index; both builders called with rcx = R; analog builder rsi = R reads +0x0D, +9, +3, +0x0C",
      pl[0x0035F43A].op_str == "eax, byte ptr [rcx + 2]" and pl[0x0035F43E].op_str == "rbx, rcx"
      and pl[0x0035F514].op_str == "rcx, rbx" and pl[0x0035F517].op_str == "0x35fac0"
      and pl[0x0035F526].op_str == "rcx, rbx" and pl[0x0035F529].op_str == "0x35f760"
      and an[0x0035F774].op_str == "rsi, rcx" and an[0x0035F7BD].op_str == "edx, byte ptr [rsi + 0xd]"
      and an[0x0035F83F].op_str == "eax, byte ptr [rsi + 0xd]" and an[0x0035F8A9].op_str == "r9d, byte ptr [rsi + 9]"
      and an[0x0035F8AE].op_str == "eax, byte ptr [rsi + 3]" and an[0x0035F90D].op_str == "r10d, byte ptr [rsi + 0xc]")
check("B8 initialiser (rdi = R+1): R+3 = 0x68, word R+0x0B = 0x0090, R+0x0D = 0x20, R+9 bit 1 cleared",
      n[0x0035F319].op_str == "byte ptr [rdi + 2], 0x68" and n[0x0035F31D].op_str == "word ptr [rdi + 0xa], 0x90"
      and n[0x0035F323].op_str == "byte ptr [rdi + 0xc], 0x20" and n[0x0035F34B].op_str == "byte ptr [rdi + 8], 0xfd")
check("C3 control: the initialiser's R-based frame store and the analog builder's use the same +0x58 displacement",
      n[0x0035F38C].op_str == "rdx, [rbx + rcx*4]" and n[0x0035F3AD].op_str == "byte ptr [rdx + rax + 0x58], cl"
      and an[0x0035F793].op_str == "rdi, [rsi + rcx*4]" and an[0x0035F835].op_str == "r10d, byte ptr [rdi + 0x58]"
      and an[0x0035F866].op_str == "byte ptr [rdi + 0x58], r10b")
print("RESULT one base R = 022CAE90 + ch*0x294: +0 write cursor, +1 read cursor, +2 channel index, +4/+5 repeat "
      "delays, +8 frames between the cursors, +9 flags; the initialiser alone addresses it from R+1, so its +0xA word "
      "and +0xC byte are R+0x0B..0x0C = 0x0090 and the dead zone R+0x0D = 0x20")
print("FAILS %d" % FAILS)
