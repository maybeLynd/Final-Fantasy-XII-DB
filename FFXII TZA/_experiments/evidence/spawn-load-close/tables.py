from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA')
s=(W/'spawn_load_close_controller.py').read_text()
ns={};exec(compile(s.split('for a in (')[0],'<existing shipping PE reader>','exec'),ns)
a=0x27FAD0;n=21*4;o=ns['off'](a-ns['ib']);raw=ns['raw'][o:o+n]
targets=[ns['ib']+v for v in struct.unpack('<21I',raw)]
body=json.loads((W/'spawn-load-close-controller.json').read_text())['bodies'][0]
starts={int(i['address'],16) for i in body['instructions']}
assert len(targets)==21 and all(t in starts for t in targets)
out=dict(exe_sha256=ns['sha'],method='A: original image-relative table; no execution',
 address=hex(a),bytes=n,raw_hex=raw.hex(),sha256=hashlib.sha256(raw).hexdigest(),
 index_rule='message19: unsigned(request-2)<=20; otherwise 0x27fa31',
 rows=[dict(request=i+2,target=hex(t)) for i,t in enumerate(targets)])
(W/'spawn-load-close-tables.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
factory=s.replace('for a in (0x27F5D0,):','for a in (0x27F540,):').replace('spawn-load-close-controller.json','spawn-load-close-factory.json')
assert factory!=s
(W/'spawn_load_close_factory.py').write_text(factory,encoding='utf-8',newline='\n')
