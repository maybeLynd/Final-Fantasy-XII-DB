"""Verify the release document's named historical ZIP, without promotion to current."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
zipfile=Path('Database/Tools/work/dashboard-exports/g20260929T075521Z-fbf2f8.zip')
sidecar=Path(str(zipfile)+'.sha256')
cli=Path('Database/Tools/analysis-kit/gfz-scripts/generation.py')
receipt=W/'historical-export-terminal.json'
assert not receipt.exists(),'Preserve prior receipt'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert zipfile.exists() and sidecar.exists()
want=sidecar.read_text().split()[0];got=sha(zipfile)
argv=[sys.executable,'-B',str(cli),'verify-zip',str(zipfile)]
p=subprocess.run(argv,capture_output=True,text=True)
result={'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,
        'terminal':True,'checker_sha256':sha(cli),'zip_sha256':got,
        'sidecar_sha256':want,'zip_bytes':zipfile.stat().st_size,
        'historical_only':True,
        'limits':'The named 07:55 ZIP cannot prove a matching export for the 18:43 HTTP-captured generation.'}
receipt.write_text(json.dumps(result,indent=2)+'\n')
assert got==want and p.returncode==0 and not p.stderr,(got,want,p.returncode,p.stderr)
print('HISTORICAL_EXPORT_VERIFIED_ONLY',got,p.stdout.strip())
