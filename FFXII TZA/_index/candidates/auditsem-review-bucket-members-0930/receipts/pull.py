"""Extract whole VBF entries whose path contains any argv substring into ./ent/ (path '/' -> '__')."""
import os, sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V
VBF = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf"
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "ent"), exist_ok=True)
with open(VBF, "rb") as f:
    names, blocks = V.load_index(f)
    for p in sorted(names):
        if any(s in p for s in sys.argv[1:]) and p.endswith((".bin", ".dat")):
            d = V.read_entry(f, names, blocks, p)
            o = os.path.join(HERE, "ent", p.replace("/", "__"))
            open(o, "wb").write(d)
            print(len(d), d[:32].hex(" "), p)
