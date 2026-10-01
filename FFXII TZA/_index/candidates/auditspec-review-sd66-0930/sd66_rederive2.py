"""sd66_rederive2.py - SWE2-AUDIT-SPEC (2026-09-30): classify the five statics the raw sweep found (sd66_rederive.out)
by a route other than the author's: every `lea rcx, [rip -> G]` followed by a direct call; in the callee (first 40
instructions) a `lea reg, [rip -> VT]` then `mov qword ptr [rcx|rbx|rdi], reg`; RTTI of VT. Also the owners of the
19 sites."""
import sys, re, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import tk
import retool as T

for g in (0x02CF8370, 0x02CF8580, 0x02CF8680, 0x02CF8880, 0x02CF9530):
    hits, raw = tk.rip_refs(g, g + 1)
    found = set(); loads = collections.Counter()
    for x, k, t in hits:
        if x.mnemonic == "mov" and not tk.is_store(x, k): loads[tk.fname(x.address)] += 1
        if x.mnemonic != "lea" or not x.op_str.startswith("rcx,"): continue
        nxt = tk.dis(x.address, x.address + 40)[1:6]
        call = next((y for y in nxt if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x")), None)
        if not call: continue
        f = int(call.op_str, 16)
        body = tk.dis(f, f + 0x120)[:40]
        for i, y in enumerate(body):
            m = re.match(r"(\w+), \[rip", y.op_str) if y.mnemonic == "lea" else None
            if m and any(z.mnemonic == "mov" and re.fullmatch(r"qword ptr \[r(cx|bx|di)\], " + m.group(1), z.op_str) for z in body[i + 1:i + 4]):
                vt = y.address + y.size + y.operands[1].mem.disp
                try: found.add(("%08X" % f, "%08X" % vt, T.rtti_class(vt)))
                except Exception: pass
    print("%08X  ctor/vtable/RTTI: %s" % (g, sorted(found)))
    print("          loaded (mov reg, [G]) in: %s" % dict(loads))
