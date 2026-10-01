from pathlib import Path
import json,struct,hashlib
W=Path('Database/Tools/work/ASTRA');ns={}
s=(W/'spawn_load_success_helpers.py').read_text();exec(compile(s.split('for a in (')[0],'<existing PE reader>','exec'),ns)
out=dict(exe_sha256=ns['sha'],method='A: raw original indexed tables; no execution',tables=[])
for a,n,bias in [(0x580B0C,13,2),(0x581268,15,0),(0x582FA0,8,2)]:
 o=ns['off'](a-ns['ib']);d=ns['raw'][o:o+4*n]
 out['tables'].append(dict(address=hex(a),count=n,input_bias=bias,raw_hex=d.hex(),sha256=hashlib.sha256(d).hexdigest(),targets=[dict(input=i+bias,address=hex(v+ns['ib'])) for i,v in enumerate(struct.unpack('<'+'I'*n,d))]))
(W/'spawn-load-success-state-tables.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
