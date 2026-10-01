"""Bounded constructor dependencies through the reviewed capture path.

Question: does the immediate AE0 zero survive constructor completion?
Inspect original normal bodies before executing anything; omitted calls and
alias effects stay unresolved. No whole-image writer census or live setup.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W = pathlib.Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('verified_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
b = C.EXE.read_bytes()
if hashlib.sha256(b).hexdigest() != C.SHA: raise ValueError('reference prerequisite')
p = struct.unpack_from('<I', b, 0x3c)[0]; opt = struct.unpack_from('<H', b, p+20)[0]
ss = [struct.unpack_from('<IIII', b, p+24+opt+i*40+8)
      for i in range(struct.unpack_from('<H', b, p+6)[0])]
def read(a, n):
    for _, va, rs, ro in ss:
        if C.BASE+va <= a and a+n <= C.BASE+va+rs:
            return b[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
    raise ValueError('unbacked original bytes')
a, n = struct.unpack_from('<II', b, p+24+112+3*8)
pd = list(struct.iter_unpack('<III', read(C.BASE+a, n)))
bodies = []
for target in [0x1d0390, 0x202880, 0x19c5d0, 0x5cc930]:
    rows = [(x+C.BASE, y+C.BASE, u+C.BASE) for x,y,u in pd
            if x+C.BASE <= target < y+C.BASE]
    if len(rows) != 1 or rows[0][0] != target:
        raise ValueError('unique entry-bound normal fragment prerequisite')
    start, end, unwind = rows[0]
    if end-start > 0x2000: raise ValueError('bounded dependency budget exceeded')
    bodies.append(dict(entry=hex(start), end_exclusive=hex(end), unwind=hex(unwind)))
C.RANGES = [(int(x['entry'],16), int(x['end_exclusive'],16)) for x in bodies]
C.main()
out = pathlib.Path(sys.argv[1]); r = json.loads(out.read_text())
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         wrapper_complete=True, normal_fragments=bodies,
         limits='Exact pdata fragments and original bytes; no full EH, alias, omitted-callee effect or constructor-return theorem yet')
out.write_text(json.dumps(r, indent=2)+'\n')
print('CAPTURED four bounded constructor dependencies; effect proof still required')
