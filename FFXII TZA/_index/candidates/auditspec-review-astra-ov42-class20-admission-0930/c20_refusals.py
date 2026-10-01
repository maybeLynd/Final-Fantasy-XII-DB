"""c20_refusals.py - SWE2-AUDIT-SPEC: run prove-class20-admission.py on altered COPIES of the packet in a temp tree
(same relative layout, so ROOT/Database/Tools/work/exe resolves to a copy of the certified image). The packet's own
files are never modified. Records exit code and the refusal message per case."""
import hashlib, json, os, shutil, struct, subprocess, sys, tempfile
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
REL = os.path.join("Database", "FFXII TZA", "_experiments", "evidence", "ov42-class20-action-admission")
PKG = os.path.join(ROOT, REL)
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
tmp = tempfile.mkdtemp(prefix="c20_")


def fresh(label):
    root = os.path.join(tmp, label)
    shutil.copytree(PKG, os.path.join(root, REL))
    os.makedirs(os.path.join(root, "Database", "Tools", "work", "exe"))
    shutil.copy(EXE, os.path.join(root, "Database", "Tools", "work", "exe", "FFXII_TZA.exe"))
    return root, os.path.join(root, REL)


def run(label, root, pk):
    out = os.path.join(tmp, label + "_result.json")
    r = subprocess.run([sys.executable, os.path.join(pk, "prove-class20-admission.py"), out], capture_output=True,
                       text=True, cwd=root)
    msg = (r.stderr.strip().splitlines() or [""])[-1] if r.returncode else r.stdout.strip()
    print("%-36s exit=%d  %s" % (label, r.returncode, msg[:140]))


def edit_json(path, fn):
    d = json.load(open(path)); fn(d); json.dump(d, open(path, "w"), indent=2)


root, pk = fresh("baseline"); run("baseline_copy", root, pk)

root, pk = fresh("count"); edit_json(os.path.join(pk, "action-selectors-01", "result.json"),
                                     lambda d: d["results"][3].__setitem__("count", 511))
run("receipt_count_511_in_one_pack", root, pk)

root, pk = fresh("tabcount")
p = os.path.join(pk, "action-selectors-01", "tables", "action_data_us.st2e"); b = bytearray(open(p, "rb").read())
struct.pack_into("<I", b, 4, 511); open(p, "wb").write(b)
run("table_header_count_511", root, pk)


def set_ins(pc, field, value):
    def fn(d):
        for s in d["ranges"]:
            for x in s["instructions"]:
                if x["pc"] == pc:
                    x[field] = value
    return fn


root, pk = fresh("wtext"); edit_json(os.path.join(pk, "action-admission-guards-raw-01.json"),
                                     set_ins("0x323030", "mnemonic", "jb"))
run("witness_323030_text_jl_to_jb", root, pk)

root, pk = fresh("wbytes"); edit_json(os.path.join(pk, "action-admission-guards-raw-01.json"),
                                      set_ins("0x32303b", "bytes", "0f8c4cfcffff"))
run("witness_32303B_bytes_only", root, pk)

root, pk = fresh("caller"); edit_json(os.path.join(pk, "special-admission-callers-raw-01.json"),
                                      set_ins("0x30cc25", "args", "edx, byte ptr [rbx + 0x1c]"))
run("caller_30CC25_width_byte", root, pk)

root, pk = fresh("nocaller"); os.remove(os.path.join(pk, "special-admission-callers-raw-01.json"))
run("caller_raw_missing", root, pk)

root, pk = fresh("role"); edit_json(os.path.join(pk, "action-admission-guards-raw-01.json"),
                                    lambda d: d["controls"][1].__setitem__("observed", "r"))
run("upstream_role_control_failed", root, pk)

root, pk = fresh("exe")
e = os.path.join(root, "Database", "Tools", "work", "exe", "FFXII_TZA.exe"); b = bytearray(open(e, "rb").read())
b[-1] ^= 1; open(e, "wb").write(b)
run("image_one_byte_changed", root, pk)

shutil.rmtree(tmp)
print("temp tree removed:", not os.path.exists(tmp))
