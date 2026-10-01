"""SWE2-AUDIT-SEM independent RC-30 attack (own code; no producer helper).
Enumerate every direct rel32 E8 (call) / E9 (jmp) / 0F 8x (jcc) whose target is a request API entry, found by a raw
byte sweep of .text (function-list independent), then decode each site's preceding 24 instructions (linear, from a
back-aligned start that re-synchronises on the site) and take the LAST writer of the kind and id registers before it.

API set (verified by disassembly in this review):
  pool  (rdx = kind, r8 = id): 00249180 00249210 002493D0 00249350 00249320 00249380
  path  (rcx = kind, rdx = id): 0032E400 0032E620 002DF980 002DF880
Classification of the id register's last writer:
  CONST  mov reg, imm / lea reg,[rip] etc. -> value
  BASE+X add reg, imm / lea reg,[r + imm] after a zero-extending byte/word load -> base range
  OTHER  anything else (argument pass-through, memory load) -> printed.
The attack: which non-constant kind-7-or-unknown-kind sites have a base range that can include 0xE2..0xE4, and are
they all in DATA's committed lists (1261e2044 cl2_requests S2 + 39d08c02f rc30_bounds A/B/C)?
Controls: P1 the Loca.mrp constant 0xBF at 004040FE->00404107 is classified CONST 0xBF;
          P2 the 0x142+byte site 003C1FF6 (in DATA's list) is found as BASE+X base 0x142;
          N1 a random non-API rel32 target (0x00249200, mid-function) yields 0 sites.
"""
import struct, re, sys
import img

POOL = [0x00249180, 0x00249210, 0x002493D0, 0x00249350, 0x00249320, 0x00249380]
PATH = [0x0032E400, 0x0032E620, 0x002DF980, 0x002DF880]
API = {a: ("edx", "r8d") for a in POOL}
API.update({a: ("ecx", "edx") for a in PATH})
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0

def sweep(targets):
    sites = []
    for i in range(len(text) - 5):
        b = text[i]
        if b in (0xE8, 0xE9):
            tgt = va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0]
            if tgt in targets:
                sites.append((va0 + i, "call" if b == 0xE8 else "jmp", tgt))
        if b == 0x0F and 0x80 <= text[i + 1] <= 0x8F:
            tgt = va0 + i + 6 + struct.unpack_from("<i", text, i + 2)[0]
            if tgt in targets:
                sites.append((va0 + i, "jcc", tgt))
    return sites

ALIAS = {"edx": ("edx", "rdx", "dx", "dl"), "r8d": ("r8d", "r8", "r8w", "r8b"), "ecx": ("ecx", "rcx", "cx", "cl"),
         "r9d": ("r9d", "r9"), "ebx": ("ebx", "rbx"), "edi": ("edi", "rdi"), "esi": ("esi", "rsi"), "ebp": ("ebp", "rbp")}

def window(site):
    # find a start 60..160 bytes back that decodes cleanly onto the site
    for back in range(160, 20, -1):
        s = site - back
        ins = list(img.md.disasm(img.rd(s, back + 8), s))
        addrs = [x.address for x in ins]
        if site in addrs:
            return ins[:addrs.index(site)]
    return []

def last_writer(ins, reg):
    names = ALIAS[reg]
    for x in reversed(ins):
        ops = x.op_str.split(", ")
        if not ops or not ops[0]:
            continue
        dst = ops[0]
        if x.mnemonic.startswith(("cmp", "test", "push", "j", "call")) and x.mnemonic != "call":
            continue
        if x.mnemonic == "call":
            return x, "CALL-CLOBBER"
        if dst in names:
            return x, None
    return None, "NO-WRITER-IN-WINDOW"

def classify(ins, reg):
    x, why = last_writer(ins, reg)
    if x is None or why:
        return why, None, x
    m = x.mnemonic
    ops = x.op_str.split(", ")
    if m == "mov" and re.fullmatch(r"(0x[0-9a-f]+|\d+)", ops[1]):
        return "CONST", int(ops[1], 0), x
    if m == "xor" and ops[0] == ops[1]:
        return "CONST", 0, x
    if m in ("add", "lea", "inc", "or", "sub"):
        mm = re.search(r"\+ (0x[0-9a-f]+|\d+)\]$", x.op_str) if m == "lea" else None
        if m == "add" and re.fullmatch(r"(0x[0-9a-f]+|\d+)", ops[1]):
            return "BASE+X", int(ops[1], 0), x
        if mm:
            base_reg = re.search(r"\[(\w+)", x.op_str).group(1)
            # fold the compiler idiom mov edx, 7 / lea r8d, [rdx + k]: base register holding a constant
            rest = ins[:ins.index(x)]
            for key, al in ALIAS.items():
                if base_reg in al:
                    bc, bv, bx = classify(rest, key)
                    if bc == "CONST":
                        return "CONST", bv + int(mm.group(1), 0), x
            return "BASE+X", int(mm.group(1), 0), x
        if m == "inc":
            return "BASE+X", 1, x
        return "OTHER", None, x
    return "OTHER", None, x

def owner_hint(a):
    return "%08X" % a

sites = sweep(set(API))
print("direct rel32 sites into the API set:", len(sites))
rows = []
for s, kind_op, tgt in sites:
    ins = window(s)
    kreg, ireg = API[tgt]
    kc, kv, kx = classify(ins, kreg)
    ic, iv, ix = classify(ins, ireg)
    rows.append((s, kind_op, tgt, kc, kv, ic, iv, ix))

cand = []
for s, op, tgt, kc, kv, ic, iv, ix in rows:
    k7 = (kc == "CONST" and kv == 7) or kc != "CONST"
    if not k7:
        continue
    if ic == "CONST":
        if 0xE2 <= iv <= 0xE4:
            cand.append((s, tgt, "CONST-HIT", iv, ix))
        continue
    if ic == "BASE+X":
        # a zero-extended byte index reaches base..base+255; the loca ids are reachable iff base <= 0xE4 and base+255 >= 0xE2
        if iv <= 0xE4:
            cand.append((s, tgt, "BASE%s" % ("" if kc == "CONST" else "?kind"), iv, ix))
        continue
    cand.append((s, tgt, ic + ("" if kc == "CONST" else "?kind"), iv, ix))

print("\nkind-7 (or non-constant kind) sites whose id is not a constant outside 0xE2..0xE4:")
for s, tgt, c, v, x in cand:
    print("  %08X -> %08X  %-14s %-8s  %s" % (s, tgt, c, "" if v is None else hex(v),
                                             "" if x is None else "%08X %s %s" % (x.address, x.mnemonic, x.op_str)))
print("count:", len(cand))

# DATA's committed lists (sites or their id-arithmetic instruction addresses)
DATA_LISTED = {0x002CEB01, 0x003C9988, 0x003C1DC2, 0x003C1EB1, 0x003C1FF6, 0x00380120, 0x00577019, 0x00575C73,
               0x0057A2DF}
print("\nBASE+X sites with base <= 0xE4 and kind 7 that are NOT in DATA's committed computed-id list:")
miss = [(s, v, x) for s, tgt, c, v, x in cand if c == "BASE" and x is not None and x.address not in DATA_LISTED]
for s, v, x in miss:
    print("  %08X base %s  id-writer %08X %s %s" % (s, hex(v), x.address, x.mnemonic, x.op_str))

FAILS = 0
def check(n, ok, d=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + n + (" - " + d if d else ""))
    FAILS += 0 if ok else 1
r = {s: (kc, kv, ic, iv, ix) for s, op, tgt, kc, kv, ic, iv, ix in rows}
check("P1 Loca.mrp 00404107 id CONST 0xBF", r.get(0x00404107, (0, 0, 0, 0))[2:4] == ("CONST", 0xBF))
check("P2 003C1FF6 0x142+byte found", any(x is not None and x.address == 0x003C1FF6 for s, t, c, v, x in cand) or
      any(ix is not None and ix.address == 0x003C1FF6 for s, op, tgt, kc, kv, ic, iv, ix in rows))
check("N1 non-entry target 00249200 has no direct site", len(sweep({0x00249200})) == 0)
print("FAILS", FAILS)
