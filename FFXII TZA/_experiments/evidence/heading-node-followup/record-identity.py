"""Pin the actual external reference and decoder loaded for this package."""
import hashlib, json, sys
from pathlib import Path
import capstone

sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
P=Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
sys.path.insert(0,str((P/'python-deps').resolve()))
import pefile
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
files={'exe':'Database/Tools/work/exe/FFXII_TZA.exe',
       'python':sys.executable,'capstone':capstone.__file__,
       'capstone_dll':Path(capstone.__file__).parent/'lib/capstone.dll',
       'pefile':pefile.__file__,'policy':P/'retained/reg_tracking.py'}
result={'python_version':sys.version,'capstone_version':capstone.__version__,
        'files':{name:{'path':str(path),'sha256':sha(path)} for name,path in files.items()},
        'method':'Read-only original image source; no native or live execution'}
assert result['files']['exe']['sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
if '--write-result' in sys.argv:
    (W/'tool-identity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
