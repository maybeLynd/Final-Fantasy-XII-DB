"""desc_check.py [--self-test] [--page P] [--out J] - the checker SWE2-AUDIT-SPEC's accessor ruling asks for
(2026-10-03, conditions 2 and (1a-c) of its follow-up). For EVERY one of the 747 PObjectAccessor<T>::Get bodies in
phyre-script-object-accessors.md's appendix it gives one disposition:

  verified     the member's distinguishing instruction is the `lea rdx,[rip+X]` feeding the base-chain compare
               (`cmp rcx,rdx` reference form, `cmp rax,rdx` pointer form), and X is named T FROM THE IMAGE;
  unresolved   the compare lea exists but no constructor call names X (core classes built without a name);
  getter-form  no compare lea: the required descriptor comes back from a call (`call G ; mov r9,rax`);
               where G's own rip lea is a named descriptor, that name is recorded (it is the container's element
               type for PArray<E>/PSharray<E>), but this ruling gives these no row;
  mismatch     the compare lea's X is named, and the name is NOT T's leaf - a defect.

Naming X from the image: each class has a descriptor-constructor wrapper W(rcx = descriptor) that loads the class name
into r8 and calls a PClassDescriptor constructor (00632D80 / 00632C90); static initialisers do `lea rcx,[rip+X]` and
call W. Level 1 is a raw E8 scan for calls to the constructors (-> W and its name, or a direct lea rcx X); level 2 a
raw E8 scan for calls to every W (-> lea rcx X).

Rows are emitted for `verified` only. FAILS = mismatches + bodies with no listed size + a failed self-test; the
unresolved and getter-form groups are dispositions, not failures. --self-test: the known pair 00599770 must match and
the same body checked against another class's descriptor must mismatch. Prints FAILS N last."""
import bisect, collections, io, json, re, struct, sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\fable-review-astra-ov42-caller-quotient-bound-1002")
from rvlib import Img  # noqa: E402
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import check_dispositions as cd  # noqa: E402


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


CTORS = {0x00632D80, 0x00632C90}  # PClassDescriptor constructors (phyre-class-parent-chain.tsv header)
P = arg("--page", r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\22-Middleware-PhyreEngine\Script-Object-Accessors\phyre-script-object-accessors.md")
OUT = arg("--out", r"C:\t\accessor_desc.json")
img = Img.load()
sizes = cd.load_functions()
t = io.open(P, encoding="utf-8").read()
app = t[t.index("## Appendix"):t.index("## Audit pass 1")]
rows = re.findall(r"`([0-9A-F]{8})` \| `([^`]+)`", app)
TYPE = dict(rows)


def rip_target(i):
    return i.address + i.size + i.operands[1].mem.disp


def cstr(va):
    b = img.read(va, 256)
    return b[:b.index(b"\0")].decode("ascii", "replace")


def disasm(f):
    return list(img.cs.disasm(img.read(f, sizes[f]), f))


# 1. the compare lea of each accessor
cmp_form, other, nosize = {}, [], []
for a, ty in rows:
    f = int(a, 16)
    if not sizes.get(f):
        nosize.append(a); continue
    ins = disasm(f)
    lea, cmpi = None, None
    for k, i in enumerate(ins):
        if i.mnemonic == "cmp" and i.op_str in ("rcx, rdx", "rax, rdx", "rdx, rcx", "rdx, rax"):
            for j in range(k - 1, max(-1, k - 8), -1):
                J = ins[j]
                if J.mnemonic == "lea" and J.op_str.startswith("rdx, [rip"):
                    lea, cmpi = J, i; break
            if lea:
                break
    if lea:
        cmp_form[a] = (lea.address, rip_target(lea), cmpi.address, cmpi.op_str)
    else:
        other.append(a)

# 2. descriptor -> name, from the image
text = [s for s in img.secs if s[0] == ".text"][0]
_, sva, vs, ra, rs = text
data = img.d[ra:ra + rs]
entries = sorted(sizes)


def sites_to(targets):
    out = set()
    for m in re.finditer(bytes([0xE8]), data):
        o = m.start()
        if o + 5 > len(data):
            break
        tgt = img.base + sva + o + 5 + struct.unpack_from("<i", data, o + 1)[0]
        if tgt in targets:
            site = img.base + sva + o
            k = bisect.bisect_right(entries, site) - 1
            if k >= 0 and entries[k] <= site < entries[k] + sizes[entries[k]]:
                out.add(entries[k])
    return out


def walk(f, targets):
    """yield (target, {reg: rip lea target}) at each direct call to a target inside f."""
    regs = {}
    for i in disasm(f):
        if i.mnemonic == "lea" and "[rip" in i.op_str:
            regs[i.op_str.split(",")[0]] = rip_target(i)
        elif i.mnemonic == "call" and i.op_str.startswith("0x") and int(i.op_str, 16) in targets:
            yield int(i.op_str, 16), dict(regs)
            regs = {}
        elif i.mnemonic in ("call", "ret", "jmp"):
            regs = {}


def name_at(va):
    try:
        s = cstr(va)
    except Exception:
        return None
    return s if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_:<>, ]*", s) else None


names, wrapper_name = collections.defaultdict(set), {}
ctor_callers = sites_to(CTORS)
for f in sorted(ctor_callers):
    for _, regs in walk(f, CTORS):
        s = name_at(regs["r8"]) if "r8" in regs else None
        if not s:
            continue
        if "rcx" in regs:
            names[regs["rcx"]].add(s)
        else:
            wrapper_name[f] = s
for f in sorted(sites_to(set(wrapper_name))):
    for w, regs in walk(f, set(wrapper_name)):
        if "rcx" in regs:
            names[regs["rcx"]].add(wrapper_name[w])
# Route 3 (the core classes: PBase, PClassDescriptor, PCluster, ...): their constructors call neither 00632D80 nor
# 00632C90; each stores its own literal name with `lea rax,[rip+S] ; mov qword ptr [rbx + 0x30], rax` - the same
# descriptor field 00632D80 stores r8 to (`mov qword ptr [rcx + 0x30], r8`) and the accessors' report reads
# (`mov r8, qword ptr [r9 + 0x30]`). Static initialisers pass X with `lea rcx,[rip+X]`.
core_name = {}
for f in sorted(sizes):
    if not (0x00631000 <= f < 0x00633000) or f in CTORS:
        continue
    ins = disasm(f)
    for k, i in enumerate(ins[:-1]):
        if i.mnemonic == "lea" and i.op_str.startswith("rax, [rip") and ins[k + 1].mnemonic == "mov" \
                and ins[k + 1].op_str == "qword ptr [rbx + 0x30], rax":
            s = name_at(rip_target(i))
            if s:
                core_name[f] = s
for f in sorted(sites_to(set(core_name))):
    for c, regs in walk(f, set(core_name)):
        if "rcx" in regs:
            names[regs["rcx"]].add(core_name[c])


def leaf(ty):
    s = ty.rstrip(" &*")
    if s.endswith(" const"):
        s = s[:-6]
    return s.split("::")[-1]


def verdict(a, X):
    got = names.get(X)
    if not got:
        return "unresolved", None
    return ("verified" if leaf(TYPE[a]) in {g.split("::")[-1] for g in got} else "mismatch"), sorted(got)


# 3. the getter form: record what G's descriptor is named, without a row
def getter_of(a):
    f = int(a, 16)
    ins = disasm(f)
    site = None
    for k, i in enumerate(ins[:-1]):
        if i.mnemonic == "call" and i.op_str.startswith("0x") and ins[k + 1].op_str == "r9, rax" \
                and ins[k + 1].mnemonic == "mov":
            site = i
    if not site:
        return None, None, None
    g = int(site.op_str, 16)
    if not sizes.get(g):
        return site.address, g, None
    hits = {rip_target(i) for i in disasm(g) if i.mnemonic == "lea" and "[rip" in i.op_str and rip_target(i) in names}
    return site.address, g, (sorted(names[hits.pop()]) if len(hits) == 1 else None)


fails = 0
if "--self-test" in sys.argv:
    a0 = "00599770"
    r0, _ = verdict(a0, cmp_form[a0][1])
    swap = next(v[1] for k, v in cmp_form.items() if leaf(TYPE[k]) != leaf(TYPE[a0]) and names.get(v[1]))
    r1, _ = verdict(a0, swap)
    print("control: %s with its own descriptor -> %s; with %08X -> %s" % (a0, r0, swap, r1))
    if r0 != "verified" or r1 != "mismatch":
        print("SELF-TEST FAILED"); fails += 1

out, res = {}, collections.Counter()
for a, ty in rows:
    if a in nosize:
        out[a] = {"type": ty, "result": "no-size"}; res["no-size"] += 1; continue
    if a in cmp_form:
        la, X, ca, cop = cmp_form[a]
        r, got = verdict(a, X)
        out[a] = {"type": ty, "result": r, "lea": "%08X" % la, "descriptor": "%08X" % X, "name": got,
                  "cmp": "%08X" % ca, "form": "reference" if cop.startswith("rcx") or cop.endswith("rcx") else "pointer"}
    else:
        site, g, nm = getter_of(a)
        r = "getter-form"
        out[a] = {"type": ty, "result": r, "call": ("%08X" % site) if site else None,
                  "getter": ("%08X" % g) if g else None, "getter_name": nm}
    res[r] += 1
io.open(OUT, "w", encoding="utf-8").write(json.dumps(out, indent=0))
print("appendix rows %d; compare form %d; other shape %d; no size %d" % (len(rows), len(cmp_form), len(other), len(nosize)))
print("constructor callers %d; wrappers %d; core constructors %d %s; descriptors named %d" % (len(ctor_callers), len(wrapper_name), len(core_name), sorted(core_name.values()), len(names)))
print("dispositions: " + ", ".join("%s %d" % kv for kv in sorted(res.items())))
gn = [v for v in out.values() if v["result"] == "getter-form" and v.get("getter_name")]
print("getter form with a named getter descriptor: %d of %d" % (len(gn), res["getter-form"]))
for a, v in out.items():
    if v["result"] in ("mismatch", "unresolved"):
        print("  %s %s %s %s" % (a, v["result"], v.get("descriptor"), v["type"]))
fails += res["mismatch"] + res["no-size"]
print("FAILS %d" % fails)
