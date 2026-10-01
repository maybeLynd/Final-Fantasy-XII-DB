from pathlib import Path
import hashlib,json
W=Path('Database/Tools/work/ASTRA');ns={}
exec((W/'spawn_save_container_primary.py').read_text().split('for a in (')[0],ns)
rows=[]
for a,n,enc in [(0x1CCFCF8,33,'ascii'),(0x1CCFD20,38,'utf-16-le'),(0x1CCFD90,92,'utf-16-le'),(0x1CC73A4,7,'ascii')]:
 o=ns['off'](a-ns['ib']);unit=2 if enc=='utf-16-le' else 1
 for k in range(0,256,unit):
  if ns['raw'][o+k:o+k+unit]==bytes(unit):break
 else:raise AssertionError('No terminator within bound')
 n=k+unit;b=ns['raw'][o:o+n]
 t=b.decode(enc);assert t.endswith('\0') and '\0' not in t[:-1]
 rows.append(dict(address=hex(a),bytes=n,raw_hex=b.hex(),sha256=hashlib.sha256(b).hexdigest(),text=t[:-1],encoding=enc))
out=dict(exe_sha256=ns['sha'],constants=rows,method='A original data only; prior broad spans retained separately, not string lengths')
(W/'spawn-save-container-literals.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print([(r['address'],r['text'],r['bytes']) for r in rows])
