"""peek.py <addr> [before] [after] - print the owner and the instructions around an address (review helper)."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk  # noqa: E402
a = int(sys.argv[1], 16); nb = int(sys.argv[2]) if len(sys.argv) > 2 else 12; na = int(sys.argv[3]) if len(sys.argv) > 3 else 3
o, how = tk.owner(a)
print(tk.fname(a))
n = tk.fsize(o) if how == "listed" else next(e - b for b, e in tk.pdata if b == o)
xs = tk.dis(o, o + n)
k = next(i for i, x in enumerate(xs) if x.address == a)
for x in xs[max(0, k - nb):k + na + 1]:
    print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
