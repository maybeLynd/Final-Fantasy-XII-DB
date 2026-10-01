"""load_order.py - CJ-2: where XIIOnlineNet's DllMain lands against entry and the stack cookie (FABLE, Claude Opus 5.5, 2026-09-26).

The deployed clients load XIIOnlineNet.dll through the FF12 module loader: a proxy dinput8.dll with hook.ini and a
modules/ folder (D:/FFXII MP Mod/FFXII_TestClient{1,2}/x64). This control reads the shipping exe and that proxy.
  L1 FFXII_TZA.exe imports DINPUT8.dll statically, so the proxy's DllMain runs during static-import initialisation,
     before `entry`.
  L2 the proxy's DllMain (rva 44E0, sha256 below) handles reason 1 (DLL_PROCESS_ATTACH) and never calls the module
     loader rva 4140. It passes 4140 to the trampoline's createHook as the detour for exe base + 0x6E8E8A.
  L3 in the game, 00808E8A is the CRT startup's `call 007A3770` (WinMain) inside 00808D78. It comes after
     _initterm_e (00808DDB) and _initterm (00808DFC), and `entry` 00808EE4 calls __security_init_cookie (00809B8C)
     before it jumps to 00808D78.
  L4 the detour 4140 reaches the proxy's module initialiser (rva 8890, the "Initialized module" log) and ends by
     calling exe base + 0x683770, the real WinMain.
So every module, XIIOnlineNet included, is loaded at the CRT's call to WinMain: after entry, after the cookie is
randomised, and after all C and C++ static initialisers.
Planted negative: the proxy's hash must be the audited build; a different loader fails L2 instead of passing on
assumption.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import hashlib, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
PROXY = Path("D:/FFXII MP Mod/FFXII_TestClient1/x64/dinput8.dll")
PROXY_SHA = "1a335f09ce60ca246d27bb1bfa2cdd00f40aa7ccba515a9690606b6859ee71df"
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
class PE:
    def __init__(s, b):
        s.d = b; pe = struct.unpack_from("<I", b, 0x3C)[0]; n = struct.unpack_from("<H", b, pe + 6)[0]
        opt = struct.unpack_from("<H", b, pe + 20)[0]; s.oh = pe + 24
        s.secs = [struct.unpack_from("<IIII", b, pe + 24 + opt + i * 40 + 8) for i in range(n)]
    def ro(s, rva):
        for vs, va, rs, r in s.secs:
            if va <= rva < va + max(vs, rs): return rva - va + r
    def imports(s):
        ir = struct.unpack_from("<I", s.d, s.oh + 112 + 8)[0]; o = s.ro(ir); dlls = {}
        while True:
            ilt, ts, fc, name, iat = struct.unpack_from("<IIIII", s.d, o)
            if name == 0: return dlls
            dll = s.d[s.ro(name):s.ro(name) + 64].split(b"\0")[0].decode(); k = 0
            while True:
                e = struct.unpack_from("<Q", s.d, s.ro(ilt or iat) + 8 * k)[0]
                if e == 0: break
                dlls[iat + 8 * k] = (dll, "#%d" % (e & 0xFFFF) if e >> 63 else s.d[s.ro(e & 0x7FFFFFFF) + 2:s.ro(e & 0x7FFFFFFF) + 64].split(b"\0")[0].decode())
                k += 1
            o += 20
    def dis(s, rva, size): return list(cs.disasm(s.d[s.ro(rva):s.ro(rva) + size], rva))
def rip(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return None if not m else x.address + x.size + (int(m.group(2), 16) * (1 if m.group(1) == "+" else -1))

g = PE(EXE.read_bytes()); BASE = 0x120000
check("L1 the exe imports DINPUT8.dll statically", any(v[0].lower() == "dinput8.dll" for v in g.imports().values()))
if not PROXY.exists():
    check("L2 proxy present", False, str(PROXY)); print("FAILS", fails); sys.exit(1)
pb = PROXY.read_bytes()
check("planted: proxy is the audited build", hashlib.sha256(pb).hexdigest() == PROXY_SHA)
p = PE(pb); pimp = p.imports()
M = p.dis(0x44E0, 0x4C6E - 0x44E0); A = {x.address: x for x in M}
calls_4140 = [x for x in M if x.mnemonic in ("call", "jmp") and x.op_str == "0x4140"]
hook = [x for x in M if x.mnemonic == "call" and rip(x) in pimp and pimp[rip(x)][1] == "createHook"]
check("L2 DllMain: reason 1; no direct call to 4140",
      "%s %s" % (A[0x4520].mnemonic, A[0x4520].op_str) == "cmp edx, 1" and calls_4140 == [])
check("L2 createHook(exe base + 0x6E8E8A, detour 4140)",
      any(h.address == 0x4AF1 for h in hook) and "%s %s" % (A[0x4ADD].mnemonic, A[0x4ADD].op_str) == "add rcx, 0x6e8e8a"
      and rip(A[0x4AEA]) == 0x4140 and A[0x4AEA].op_str.startswith("rdx"),
      "createHook sites %s" % [hex(h.address) for h in hook])
def gva(va, size): return list(cs.disasm(g.d[g.ro(va - BASE):g.ro(va - BASE) + size], va))   # VA-addressed, so targets are VAs
G = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in gva(0x808D78, 0x14A)}          # 00808D78, body 330 B
E = ["%s %s" % (x.mnemonic, x.op_str) for x in gva(0x808EE4, 0x12)]
check("L3 00808E8A is the WinMain call, after _initterm_e and _initterm; entry calls the cookie first",
      G.get(0x808E8A) == "call 0x7a3770" and G.get(0x808DDB) == "call 0x862022" and G.get(0x808DFC) == "call 0x86201c"
      and E[1] == "call 0x809b8c" and E[3] == "jmp 0x808d78")
D = p.dis(0x4140, 0x400)
check("L4 detour reaches the module initialiser 8890 and calls exe base + 0x683770",
      any(x.mnemonic == "call" and x.op_str == "0x8890" for x in D)
      and any(x.mnemonic == "add" and x.op_str.endswith(", 0x683770") for x in D))
print("FAILS", fails)
sys.exit(1 if fails else 0)
