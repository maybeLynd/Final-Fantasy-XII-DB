"""ea2_class_name.py - EA-2 (the post-process parameter object's CLASS NAME): the shipped-artefact scan requirement 3
asks for when the residue is a label (FABLE, Claude Opus 5.5, 2026-09-26).

The object is the 0x4A8-byte parameter singleton at 01F7F5F0: no vtable, no reflection registration, and its
constructor 0018CD90 references no string (the row's own reading). A name could still ship in the data that fills it.
  N1 every key at every depth of every map and cutscene JSON under jsondata/ (files that do not parse are read from
     their raw text) is a field name or a section name: the only nested objects are "Common", "Cut N" and "PresetDof N".
     No key contains "class", "type", "struct", "context" or "param".
  N2 the only struct-description files shipped (jsondata/parametersmanager*struct.*) describe two OTHER objects: their
     field names share nothing with the map JSON's post-process keys.
  N3 the exe carries none of the struct-file family names ("ParametersManager" and the like), so the struct files are
     not how the engine names anything.
  N4 control: the scan does see the post-process vocabulary, finding the keys EA-2's own row cites (SAO/HBAO bias
     and radius per scene and character).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import glob, json, os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
J = Path("D:/FFXII_TZA_extract/jsondata")
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
if not J.exists():
    check("extract present", False, str(J)); sys.exit(1)
files = sorted(glob.glob(str(J / "maps" / "*.json"))) + sorted(glob.glob(str(J / "cutscenes" / "**" / "*.json"), recursive=True))
keys, containers, rawonly = set(), set(), 0
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            keys.add(k)
            if isinstance(v, (dict, list)): containers.add(k)
            walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for f in files:
    raw = open(f, encoding="utf-8-sig", errors="replace").read()
    try: walk(json.loads(raw))
    except Exception:
        rawonly += 1                                   # malformed or empty shipped JSON: read its keys from the raw text
        keys |= set(re.findall(r'"([^"]+)"\s*:', raw))
print("json files:", len(files), "read as raw text:", rawonly, "distinct keys (all depths):", len(keys))
TYPEWORD = re.compile(r"(?i)class|type|struct|context|param")
SECTION = re.compile(r"^(Common|Cut \d+|PresetDof \d+)$")
check("N1 every nested object is a section (Common / Cut N / PresetDof N), never a type",
      all(SECTION.match(k) for k in containers), str(sorted(k for k in containers if not SECTION.match(k))[:5]))
check("N1 no key at any depth is a type-like word", not any(TYPEWORD.search(k) for k in keys),
      str(sorted(k for k in keys if TYPEWORD.search(k))[:5]))
sf = sorted(glob.glob(str(J / "parametersmanager*struct.*")))
sv = set()
for f in sf:
    for line in open(f, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip(): continue
        sv.add(line.split(",")[0].strip())
check("N2 the struct files describe other objects", len(sf) == 2 and not (sv & keys), "%s shared=%s" % ([os.path.basename(x) for x in sf], sorted(sv & keys)[:5]))
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
fam = {m.group(0) for m in re.finditer(rb"(?i)parametersmanager\w*|paramsmanager\w*", d)}
check("N3 the exe carries no ParametersManager-family name", fam == set(), str(fam))
check("N4 control: the scan sees the post-process vocabulary", {"mSAORadiusSce", "mHBAOBiasChr", "mSAOBiasSce"} <= keys)
print("FAILS", fails)
sys.exit(1 if fails else 0)
