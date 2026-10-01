import hashlib,json,subprocess,sys,struct
from pathlib import Path
import capstone,unicorn
W=Path(__file__).resolve().parent;P=W/'private-source';P.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0,(a,q.stderr);return q.stdout
source='ced7c61fd';page='f7a5ce0d6';records=[]
for rel,name,c in [('Database/FFXII TZA/_index/candidates/s27-opus-replay-periodic-builder/check.py','check.py',source),('Database/FFXII TZA/_index/candidates/s27-opus-replay-periodic-builder/poison.py','poison.py',source),('Database/FFXII TZA/_index/candidates/s27-opus-replay-periodic-builder/poison_result.json','author-poison-result.json',source),('Database/FFXII TZA/_index/candidates/pkg-gp-status-poison/q6.md','fable-q6.md',page),('Database/FFXII TZA/10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md','status-page.md',page)]:
 b=git('show',c+':'+rel);(P/name).write_bytes(b);current=Path(rel).read_bytes();records.append(dict(path=rel,copy=name,commit=git('rev-parse',c).decode().strip(),blob=git('rev-parse',c+':'+rel).decode().strip(),sha256=sha(b),current_preimage_sha256=sha(current),current_matches=sha(b)==sha(current)))
exe=Path(r'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe');d=exe.read_bytes();assert sha(d)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',d,0x3c)[0];n=struct.unpack_from('<H',d,pe+6)[0];off=pe+24+struct.unpack_from('<H',d,pe+20)[0];sections=[]
for j in range(n):
 vs,rva,size,raw=struct.unpack_from('<IIII',d,off+40*j+8);sections.append((0x120000+rva,size,raw))
def rd(a,z):
 for va,size,raw in sections:
  if va<=a and a+z<=va+size:return d[raw+a-va:raw+a-va+z]
 raise ValueError(hex(a))
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);b=rd(0x386c70,935);(P/'stage2-00386c70.bin').write_bytes(b);ins=[dict(pc=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in cs.disasm(b,0x386c70)];assert sum(len(bytes.fromhex(i['bytes'])) for i in ins)==935
insmap={i['pc']:i for i in ins};assert insmap['0x386f85']['mnemonic']=='jae' and insmap['0x386f85']['operands']=='0x386f95';assert insmap['0x386fd5']['mnemonic']=='jge' and insmap['0x386fd5']['operands']=='0x386fe7'
(P/'stage2-disassembly.json').write_text(json.dumps(ins,indent=2)+'\n')
graph=[]
for name in ['edges.tsv','functions.tsv']:
 p=Path('Database/Tools/work/graph')/name;graph.append(dict(path=p.as_posix(),sha256=sha(p.read_bytes()),size=p.stat().st_size))
mods=[]
for root in [Path(unicorn.__file__).parent,Path(capstone.__file__).parent]:
 for p in sorted(root.rglob('*.dll')):mods.append(dict(path=str(p),sha256=sha(p.read_bytes()),size=p.stat().st_size))
out=dict(records=records,image=dict(path=str(exe),sha256=sha(d),size=len(d),base='0x120000',stage2_bytes_sha256=sha(b)),graph=graph,tools=dict(python=sys.version,python_path=sys.executable,base_python=sys._base_executable,base_python_sha256=sha(Path(sys._base_executable).read_bytes()),unicorn=unicorn.__version__,capstone=capstone.__version__,native_modules=mods),driver_sha256=sha(Path(__file__).read_bytes()))
(W/'source.json').write_text(json.dumps(out,indent=2)+'\n');print('SOURCE_PINNED',len(ins),[r['current_matches'] for r in records],len(mods))
