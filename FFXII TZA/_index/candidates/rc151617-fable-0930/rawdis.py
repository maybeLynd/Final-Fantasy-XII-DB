# rawdis.py START END : linear disassembly of an arbitrary image range (for unlisted code), rip targets resolved
import sys, os
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
exec(open('disw.py').read().split("fn = int")[0])
s = int(sys.argv[1], 16); e = int(sys.argv[2], 16)
for x in md.disasm(d[off(s):off(e)], s):
    line = f"  {x.address:08X} {x.mnemonic} {x.op_str}"
    if "rip + " in x.op_str or "rip - " in x.op_str:
        sgn = 1 if "rip + " in x.op_str else -1
        disp = int(x.op_str.split("rip + " if sgn == 1 else "rip - ")[1].split("]")[0], 16)
        t = x.address + x.size + sgn * disp
        line += f"    ; -> {t:08X} {names.get(t, '')}"
    elif x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
        t = int(x.op_str, 16); line += f"    ; {names.get(t, '')}"
    print(line)
