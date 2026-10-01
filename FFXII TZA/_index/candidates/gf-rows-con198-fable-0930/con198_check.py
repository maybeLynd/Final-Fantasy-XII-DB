# con198_check.py - FABLE's re-read of OPUS's CON-198 before restating the GF / W / EA rows (2026-09-30).
# Checks from the certified image, via the FABLE disassembly helper (Database/Tools/work/FABLE/pub140-scratch/disr.py):
#  K1 0018CD90 (the post-process context constructor) passes rbx+0x378 to 00645DB0;
#  K2 00645DB0 forms the vtable address 00D625D0 (PFXAA's);
#  K3 00191DA0 calls 0065A630 on context+0x378 (the +0x4A3 == 0 arm);
#  K4 0065A630 is a tail jump into 0065A640 (PFXAA's worker).
import os, re, subprocess, sys
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch")
SCR = os.path.normpath(SCR)
def dis(fn):
    return subprocess.run([sys.executable, "disr.py", fn], capture_output=True, text=True, cwd=SCR).stdout.splitlines()
fails = 0
def check(name, ok, detail):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
a = dis("0018CD90")
k = [i for i, l in enumerate(a) if "call 0x645db0" in l]
check("K1", bool(k) and "lea rcx, [rbx + 0x378]" in a[k[0] - 1], a[k[0] - 1].strip() + " / " + a[k[0]].strip() if k else "no call")
b = dis("00645DB0")
check("K2", any("00D625D0" in l for l in b), next((l.strip() for l in b if "00D625D0" in l), "no vtable form"))
c = dis("00191DA0")
k = [i for i, l in enumerate(c) if "call 0x65a630" in l]
check("K3", bool(k) and any("add rcx, 0x378" in l for l in c[max(0, k[0] - 6):k[0]]), c[k[0]].strip() if k else "no call")
d = dis("0065A630")
check("K4", any("jmp 0x65a640" in l for l in d), next((l.strip() for l in d if "jmp" in l), "no jmp"))
print("FAILS", fails)
