from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');E=Path('Database/FFXII TZA/_experiments/evidence')
s=(W/'spawn_materialization_primary.py').read_text();ns={};exec(compile(s.split('for a in (')[0],'<existing shipping PE reader>','exec'),ns)
records=[]
for a,n in [(0xD23D80,24),(0xD23D98,4)]:
 o=ns['off'](a-ns['ib']);d=ns['raw'][o:o+n]
 records.append(dict(address=hex(a),bytes=n,raw_hex=d.hex(),sha256=hashlib.sha256(d).hexdigest(),dwords=list(struct.unpack('<'+'I'*(n//4),d))))
a=0xD23EB8;o=ns['off'](a-ns['ib']);window=ns['raw'][o:o+128];end=window.index(b'\0')+1;d=window[:end]
records.append(dict(address=hex(a),bytes=len(d),raw_hex=d.hex(),sha256=hashlib.sha256(d).hexdigest(),text=d[:-1].decode('ascii')))
j=dict(exe_sha256=ns['sha'],records=records,limits='Literal load resource descriptors/name only; no path resolution, archive extraction or live binding.')
(W/'spawn-materialization-inputs.json').write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(j,indent=2))
for p in sorted((E/'spawn-widget-retention').glob('*.json')):
 if p.name in ('manifest.json','check.json'):continue
 data=json.loads(p.read_text())
 for b in data.get('bodies',[]):
  if int(b['address'],16) not in (0x3933F0,0x393460):continue
  print(p.as_posix(),b['address'])
  for i in b['instructions']:print(i['address'],i['mnemonic'],i['operands'],i.get('rip_targets',''))
