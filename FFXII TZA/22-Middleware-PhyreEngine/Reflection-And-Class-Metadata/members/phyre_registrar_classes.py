"""UQ-290 / UQ-291: which class does each Phyre registrar register?

A registrar is a caller of 006388C0 (register the descriptor in rcx by the name at its +0x30). The name is
stored by the base constructors 00632C90 / 00632D80 from r8. This joins
    registrar site -> descriptor (a static object, or the return value of a getter)
                   -> the constructor call made on that descriptor -> the name string in r8.
Every hop is a linear backward walk of at most WIN instructions inside one listed function; a hop that does
not resolve is reported as unresolved, never guessed.
"""
import struct, collections, bisect, json, sys
import capstone

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work"
EXE = ROOT + r"\exe\FFXII_TZA.exe"
FUNCS = ROOT + r"\graph\functions.tsv"
BASE = 0x120000
BASECTORS = {0x00632C90, 0x00632D80}
REGISTER = 0x006388C0
WIN = 16

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vs, ro, rs))
    o += 40


def off(va):
    rva = va - BASE
    for a, s, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


def cstr(va):
    so = off(va)
    return d[so:so + 256].split(b"\0")[0].decode("latin1") if so is not None else None


funcs = []
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        funcs.append((int(p[0], 16), int(p[2])))
    except (ValueError, IndexError):
        pass
funcs.sort()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
_cache = {}


def body(a, n):
    if a not in _cache:
        _cache[a] = list(md.disasm(d[off(a):off(a) + n], a))
    return _cache[a]


def callers_of(targets):
    """yield (func, ins_list, index, target) for every direct call/jmp to a target."""
    for a, n in funcs:
        fo = off(a)
        if fo is None:
            continue
        code = d[fo:fo + n]
        hit = False
        for i in range(len(code) - 4):
            if code[i] in (0xE8, 0xE9) and a + i + 5 + struct.unpack_from("<i", code, i + 1)[0] in targets:
                hit = True
                break
        if not hit:
            continue
        ins = body(a, n)
        for k, x in enumerate(ins):
            if x.mnemonic in ("call", "jmp"):
                try:
                    t = int(x.op_str, 16)
                except ValueError:
                    continue
                if t in targets:
                    yield a, ins, k, t


def riptarget(y):
    return y.address + y.size + y.operands[1].mem.disp


def last_write(ins, k, regs):
    for y in reversed(ins[max(0, k - WIN):k]):
        if y.op_str.split(",")[0].strip() in regs:
            return y
    return None


R64 = {"rcx": ("rcx", "ecx"), "rbx": ("rbx", "ebx"), "rsi": ("rsi", "esi"), "rdi": ("rdi", "edi"),
       "rbp": ("rbp", "ebp"), "r14": ("r14", "r14d"), "r15": ("r15", "r15d"), "r12": ("r12", "r12d"),
       "r13": ("r13", "r13d"), "rax": ("rax", "eax")}


def this_of(ins, k):
    """('obj', va) | ('ret', callee) | ('arg', None) | None for the rcx of the call at index k."""
    y = last_write(ins, k, R64["rcx"])
    hops = 0
    while y is not None and hops < 3:
        ops = [s.strip() for s in y.op_str.split(",")]
        if y.mnemonic == "lea" and "rip" in y.op_str:
            return ("obj", riptarget(y))
        if y.mnemonic == "mov" and len(ops) == 2 and ops[1] in R64:
            src = ops[1]
            idx = ins.index(y)
            if src == "rax":
                # nearest preceding call supplies rax
                for z in reversed(ins[max(0, idx - WIN):idx]):
                    if z.mnemonic == "call":
                        try:
                            return ("ret", int(z.op_str, 16))
                        except ValueError:
                            return None
                return None
            y2 = None
            for z in reversed(ins[max(0, idx - 48):idx]):
                if z.op_str.split(",")[0].strip() in R64[src]:
                    y2 = z
                    break
            if y2 is None:
                return ("arg", None) if src == "rcx" or idx < 12 else None
            y = y2
            hops += 1
            continue
        return None
    return ("arg", None) if y is None else None


# 1. base-constructor sites: name, and the descriptor when it is visible in the same function
ctor_name = {}                 # constructor function -> name   (this == the function's own rcx)
obj_name = {}                  # static descriptor -> name
getter_obj = {}                # template getter -> descriptor  (name arrives through the getter's rcx)
for f, ins, k, t in callers_of(BASECTORS):
    nm = None
    y = last_write(ins, k, ("r8", "r8d"))
    if y is not None and y.mnemonic == "lea" and "rip" in y.op_str:
        nm = cstr(riptarget(y))
    th = this_of(ins, k)
    if nm is not None and th and th[0] == "obj":
        obj_name[th[1]] = nm
    elif nm is not None:
        ctor_name[f] = nm
    elif th and th[0] == "obj":
        getter_obj[f] = th[1]

# 2. constructors are applied to statics by their callers; getters get their name from theirs
for f, ins, k, t in callers_of(set(ctor_name)):
    th = this_of(ins, k)
    if th and th[0] == "obj":
        obj_name.setdefault(th[1], ctor_name[t])
getter_name = collections.defaultdict(set)
for f, ins, k, t in callers_of(set(getter_obj)):
    y = last_write(ins, k, R64["rcx"])
    if y is None or "rip" not in y.op_str:
        continue
    if y.mnemonic == "lea":
        nm = cstr(riptarget(y))
    elif y.mnemonic == "mov":
        so = off(riptarget(y))
        nm = cstr(struct.unpack_from("<Q", d, so)[0]) if so is not None else None
    else:
        nm = None
    if nm:
        getter_name[t].add(nm)
for g, names in getter_name.items():
    if len(names) == 1:
        obj_name.setdefault(getter_obj[g], next(iter(names)))

# functions that return a named descriptor (a getter, or a lazy accessor around a static)
ret_name = {g: next(iter(n)) for g, n in getter_name.items() if len(n) == 1}

# 3. the registrars
reg = collections.defaultdict(list)      # registrar -> [(site, name or None, how)]
for f, ins, k, t in callers_of({REGISTER}):
    th = this_of(ins, k)
    nm, how = None, "unresolved"
    if th and th[0] == "obj":
        nm, how = obj_name.get(th[1]), "static %08X" % th[1]
    elif th and th[0] == "ret":
        nm, how = ret_name.get(th[1]), "returned by %08X" % th[1]
        if nm is None:
            # an accessor that itself constructs a static descriptor
            for a, n in funcs[bisect.bisect_left(funcs, (th[1], 0)):][:1]:
                if a == th[1]:
                    for y in body(a, n):
                        if y.mnemonic == "lea" and "rip" in y.op_str and riptarget(y) in obj_name:
                            nm = obj_name[riptarget(y)]
                            break
    elif th and th[0] == "arg":
        how = "descriptor is the registrar's own argument"
    if nm is None and f in getter_obj and (th is None or th[0] != "ret"):
        # a template getter registering the one descriptor it constructed, from a callee-saved register
        nm, how = obj_name.get(getter_obj[f]), "own static %08X (template getter)" % getter_obj[f]
    reg[f].append((ins[k].address, nm, how))

sites = sum(len(v) for v in reg.values())
named = sum(1 for v in reg.values() for s in v if s[1])
full = sum(1 for v in reg.values() if all(s[1] for s in v))
print("# named descriptors %d (constructors %d, template getters %d with one name)"
      % (len(obj_name), len(ctor_name), len(ret_name)))
print("# registrars %d  registration sites %d  sites named %d  registrars with every site named %d"
      % (len(reg), sites, named, full))
try:
    j = json.load(open(ROOT + r"\h78\phyre_class_registrars.json"))
    keys = {int(k, 16) for k in j}
    sl = {int(k, 16) for k, v in j.items() if not v.get("strings")}
    print("# against the 315 of the registrar census: present here %d; string-less %d, of which every site named %d"
          % (len(keys & set(reg)), len(sl), sum(1 for r in sl if r in reg and all(s[1] for s in reg[r]))))
except OSError:
    pass
print("registrar\tsites\tnamed\tclasses")
for f in sorted(reg):
    v = reg[f]
    print("%08X\t%d\t%d\t%s" % (f, len(v), sum(1 for s in v if s[1]),
                                 " | ".join(sorted({s[1] for s in v if s[1]}))))
if "--unnamed" in sys.argv:
    c = collections.Counter(s[2].split(" ")[0] for v in reg.values() for s in v if not s[1])
    print("# unnamed by route:", dict(c))
    for f in sorted(reg):
        for s in reg[f]:
            if not s[1]:
                print("# unnamed\t%08X\t%08X\t%s" % (f, s[0], s[2]))
