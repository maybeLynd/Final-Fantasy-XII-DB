"""T5 / REGFILE-REUSE: can any native store reach ActorStorageRecord +0x64..+0x83 (the VM register file) other than
the interpreter? (FABLE reader, 2026-09-29.)  python t5_regfile.py [HOPS] > t5_regfile_h<HOPS>.out
Model: _index/candidates/rc789-fable-0930/rc8_inverse.py.
  H0 = functions that reach a record pointer: callers of the getter ActorManager_GetRecordByOrdinal 00358940 (raw E8/E9),
       functions with a rip-relative or image-base-relative reference into the manager array 02098E10..02099ABF
       (the pool root is manager+0x08, stride 0x288), and the record initialisers/allocator/release
       (002679F0, 00266530, 00266AD0, 00266BD0, 002693D0) and their callers.
  Hk = H0 plus k hops of direct callees (raw E8/E9 index), which covers a record passed as an argument k times.
  W  = image-wide (every listed function) non-stack stores whose byte range overlaps +0x64..+0x83 through a
       non-rip base (any width, any mnemonic that writes memory), plus rep stos/movs, plus memset/memcpy calls.
Report W & Hk with each store, for reading.
Controls: the interpreter's own register stores (0026161C.. POPI handlers, e.g. 00261624 mov [r15+0x64], eax) must be in
W & Hk; the pool memset 00267A8B (002679F0 -> 00861EC0) must be listed among the bulk calls in Hk."""
import sys, json, os, collections
import tk
from capstone.x86 import X86_OP_MEM
HOPS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
HERE = os.path.dirname(os.path.abspath(tk.__file__))
IDX = json.load(open(os.path.join(HERE, "..", "pub140-scratch", "tools", "rawcalls.json")))
LO, HI = 0x64, 0x84
GETTER = 0x00358940
INIT = [0x002679F0, 0x00266530, 0x00266AD0, 0x00266BD0, 0x002693D0]
BULK = {0x00861EBA: "memcpy", 0x00861EC0: "memset", 0x00861FC8: "memcpy_s"}
callees = collections.defaultdict(set); callers = collections.defaultdict(set)
for tgt, sites in IDX.items():
    t = int(tgt, 16)
    for s in sites:
        o, how = tk.owner(int(s, 16))
        if o is not None and how == "listed":
            callees[o].add(t); callers[t].add(o)
H0 = set(callers[GETTER]) | set(INIT)
for f in INIT: H0 |= callers[f]
h, _ = tk.rip_refs(0x02098E10, 0x02099AC0)
H0 |= {tk.owner(x.address)[0] for x, k, t in h if tk.owner(x.address)[1] == "listed"}
hb, _ = tk.disp_refs(0x02098E10 - 0x120000, 0x02099AC0 - 0x120000)
H0 |= {tk.owner(x.address)[0] for x, k, v in hb}
H = set(H0); fr = set(H0)
for _ in range(HOPS):
    nx = set()
    for f in fr: nx |= {c for c in callees[f] if tk.fsize(c)}
    nx -= H; H |= nx; fr = nx
print("H0 = %d functions (getter callers %d, manager-array referrers %d); H%d = %d functions" %
      (len(H0), len(callers[GETTER]), len({tk.owner(x.address)[0] for x, k, t in h}), HOPS, len(H)))
W = collections.defaultdict(list); BK = collections.defaultdict(list)
for e, sz in tk.flist:
    if sz <= 0 or sz > 0x20000 or not (0x121000 <= e < 0x8C2000): continue
    for x in tk.fdis(e):
        if x.mnemonic.startswith("rep ") and ("stos" in x.mnemonic or "movs" in x.mnemonic):
            BK[e].append("%08X %s" % (x.address, x.mnemonic))
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x") and int(x.op_str, 16) in BULK:
            BK[e].append("%08X %s %s" % (x.address, x.mnemonic, BULK[int(x.op_str, 16)]))
        for k, op in enumerate(x.operands):
            if op.type != X86_OP_MEM or not op.mem.base: continue
            b = x.reg_name(op.mem.base)
            if b in ("rip", "rsp"): continue
            if not tk.is_store(x, k): continue
            lo = op.mem.disp; hi = lo + max(op.size, 1)
            if lo < HI and hi > LO:
                W[e].append("%08X %-8s %-44s base=%s%s" % (x.address, x.mnemonic, x.op_str, b, " idx" if op.mem.index else ""))
WH = sorted(set(W) & H)
print("W = %d functions image-wide; W & H%d = %d functions" % (len(W), HOPS, len(WH)))
for f in WH:
    print("  %s%s" % (tk.fname(f), "  [H0]" if f in H0 else ""))
    for s in W[f]: print("       " + s)
print("\n== bulk operations inside H%d (memset/memcpy calls and rep string ops), for reading:" % HOPS)
for f in sorted(set(BK) & H):
    print("  %s: %s" % (tk.fname(f), BK[f]))
interp = 0x0025E4C0
ok1 = interp in WH and any(s.startswith("00261624") or s.startswith("0026162") for s in W[interp])
print("\nCONTROL interpreter 0025E4C0 in W & H%d with its register stores:" % HOPS, interp in WH, [s.split()[0] for s in W.get(interp, [])][:12])
print("CONTROL pool memset 00267A8B listed in H%d bulk:" % HOPS, any(s.startswith("00267A8B") for s in BK.get(0x002679F0, [])))
