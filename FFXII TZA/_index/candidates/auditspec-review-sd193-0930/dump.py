"""dump.py START END [START END ...] - print a linear decode with the reviewer's loader (rvimg.py)."""
import sys
import rvimg as V

a = sys.argv[1:]
for k in range(0, len(a), 2):
    s, e = int(a[k], 16), int(a[k + 1], 16)
    print("== %08X..%08X" % (s, e))
    V.show(s, e)
