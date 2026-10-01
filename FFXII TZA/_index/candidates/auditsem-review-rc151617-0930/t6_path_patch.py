import shutil
SRC = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\rc151617-fable-0930\t6_regfile_loads.py"
DST = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\SWE2-AUDIT-SEM\rc1517\t6run\t6_regfile_loads.py"
s = open(SRC, encoding="utf-8").read()
old = 'os.path.join(HERE, "..", "pub140-scratch", "tools", "rawcalls.json")'
new = 'r"C:\\Users\\Kristian\\source\\repos\\XIIOnline\\Database\\Tools\\work\\FABLE\\pub140-scratch\\tools\\rawcalls.json"'
assert old in s
open(DST, "w", encoding="utf-8").write(s.replace(old, new))
print("patched only the rawcalls.json path")
