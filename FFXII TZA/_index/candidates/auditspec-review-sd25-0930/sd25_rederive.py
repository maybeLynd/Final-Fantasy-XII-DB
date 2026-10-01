"""sd25_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-25 (2026-09-30), not through retool.
(1) Parse the PE import directory: every IAT slot whose import name is rand / rand_s / srand (any DLL).
(2) Raw rip-relative census of each such slot (tk.rip_refs, all .text) -> referencing functions; also any jmp-thunk.
(3) My own direct-call closure of the thread body 007A5400 (E8 calls + E9 jumps to a listed start, linear decode of
    listed functions) -> which rand users are inside; is the stepper 007BD120 inside.
(4) Indirect-call sites through +0x150 (slot 42) and +0x68 (slot 13) inside that closure (evidence for the virtual
    roots' thread, not proof)."""
import sys, struct, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
d = tk.d; pe = struct.unpack_from("<I", d, 0x3C)[0]
imp_rva = struct.unpack_from("<I", d, pe + 24 + 112 + 8)[0]      # PE32+: data directory 1 at optional header + 112 + 8
slots = {}
o = tk.off(tk.BASE + imp_rva)
while True:
    ilt, _, _, name_rva, iat = struct.unpack_from("<IIIII", d, o)
    if not name_rva: break
    dll = d[tk.off(tk.BASE + name_rva):].split(b"\0")[0].decode()
    k = 0
    while True:
        e = struct.unpack_from("<Q", d, tk.off(tk.BASE + (ilt or iat)) + 8 * k)[0]
        if not e: break
        if not (e >> 63):
            nm = d[tk.off(tk.BASE + (e & 0x7FFFFFFF)) + 2:].split(b"\0")[0].decode()
            if nm in ("rand", "rand_s", "srand"): slots[tk.BASE + iat + 8 * k] = (dll, nm)
        k += 1
    o += 20
print("rand-family imports:", {("%08X" % a): v for a, v in slots.items()})
users = {}
for a, (dll, nm) in slots.items():
    refs, raw = tk.rip_refs(a, a + 8)
    fs = sorted(set(tk.owner(x.address)[0] or 0 for x, k, t in refs))
    users[nm] = fs
    print("%s %08X: %d rip refs, %d raw-only, %d functions" % (nm, a, len(refs), len(raw), len(fs)))
def calls_of(f):
    out = set()
    try: body = tk.fdis(f)
    except Exception: return out
    for x in body:
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if t in tk.names and t != f: out.add(t)
    return out
seen, todo = {0x007A5400}, [0x007A5400]
while todo:
    f = todo.pop()
    for t in calls_of(f):
        if t not in seen: seen.add(t); todo.append(t)
print("closure of 007A5400: %d functions; stepper 007BD120 in: %s; 007BDFA0 in: %s" % (len(seen), 0x007BD120 in seen, 0x007BDFA0 in seen))
for nm, fs in users.items():
    ins_ = [f for f in fs if f in seen]
    print("%s users inside closure: %s; outside: %d" % (nm, " ".join("%08X" % f for f in ins_), len(fs) - len(ins_)))
print("outside-closure rand users:", " ".join("%08X" % f for f in users.get("rand", []) if f not in seen))
vc = {0x150: [], 0x68: []}
for f in sorted(seen):
    for x in tk.fdis(f):
        if x.mnemonic == "call":
            m = re.match(r"qword ptr \[r\w+ \+ (0x150|0x68)\]$", x.op_str)
            if m: vc[int(m.group(1), 16)].append(x.address)
for k, v in vc.items():
    print("closure call [reg + %#x]: %d sites %s" % (k, len(v), " ".join("%08X" % a for a in v[:12])))
# (5) the audio-range rand users outside the direct closure: where are they stored (vtable slots), and does the
#     closure hold an indirect call through that slot offset?
def rtti(vt):
    col = tk.u64(vt - 8)
    if not col or tk.off(col) is None or tk.u32(col) != 1: return None
    o = tk.off(tk.BASE + tk.u32(col + 0x0C) + 0x10)
    return d[o:o + 120].split(b"\0")[0].decode("latin1") if o else None
def vt_start(p):
    q = p
    while q > p - 0x800:
        if rtti(q): return q
        q -= 8
    return None
for f in [f for f in users.get("rand", []) if f not in seen and 0x007A0000 <= f < 0x00800000]:
    rl = tk.reloc_ptrs(f, f + 1)
    desc = []
    for ptr, tgt in rl:
        vs = vt_start(ptr)
        if vs:
            slot = (ptr - vs) // 8
            pat = re.compile(r"qword ptr \[r\w+ \+ %#x\]$" % (slot * 8))
            n = sum(1 for g in sorted(seen) for x in tk.fdis(g) if x.mnemonic == "call" and pat.match(x.op_str)) if slot else 0
            desc.append("%s slot %d (closure call sites through %#x: %d)" % (rtti(vs), slot, slot * 8, n))
        else:
            desc.append("stored at %08X" % ptr)
    print("%08X: %s; direct callers %s" % (f, "; ".join(desc) or "no reloc", [s for s in __import__("json").load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json")).get("%X" % f, [])][:5]))
# (6) the closure's call sites through the select slots, and the srand users
for off_ in (0x140, 0x150, 0x158):
    pat = re.compile(r"qword ptr \[r\w+ \+ %#x\]$" % off_)
    print("closure call sites through %#x: %s" % (off_, " ".join("%08X/%08X" % (x.address, g) for g in sorted(seen) for x in tk.fdis(g) if x.mnemonic == "call" and pat.match(x.op_str))))
for a in slots:
    refs, raw = tk.rip_refs(a, a + 8)
    print("%s refs: %s" % (slots[a][1], " ".join("%08X/%08X %s" % (x.address, tk.owner(x.address)[0] or 0, x.mnemonic) for x, k, t in refs if slots[a][1] == "srand")))
