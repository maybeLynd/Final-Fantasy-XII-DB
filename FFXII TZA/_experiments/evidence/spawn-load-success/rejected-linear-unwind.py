from pathlib import Path
import hashlib,json,struct
W=Path('Database/Tools/work/ASTRA');s=(W/'spawn_load_success_helpers.py').read_text();ns={}
exec(compile(s.split('for a in (')[0],'<existing shipping PE reader>','exec'),ns)
pd=next(x for x in ns['sections'] if x['name']=='.pdata');raw=ns['raw'];ib=ns['ib'];rows=[]
for k in range(0,pd['raw_bytes']-11,12):
 r=struct.unpack_from('<III',raw,pd['disk_offset']+k)
 if r[0] and r[0]<r[1]:rows.append(r)
memo={};unsupported=[]
def root(r,seen=()):
 if r in memo:return memo[r]
 assert r not in seen,('cycle',r)
 u=ns['off'](r[2]);v=raw[u]&7;flags=raw[u]>>3;count=raw[u+2]
 if v!=1:raise ValueError(('unwind version',v,r))
 if flags&4:
  assert not flags&3
  c=u+4+2*((count+1)&~1);parent=struct.unpack_from('<III',raw,c)
  value=root(parent,seen+(r,))
 else:value=r
 memo[r]=value;return value
chosen=[]
for r in rows:
 try:q=root(r)
 except (ValueError,AssertionError) as e:unsupported.append(str(e));continue
 if ib+q[0]==0x57FE80:chosen.append(r)
assert not unsupported,unsupported
chosen.sort();assert [(ib+r[0],ib+r[1]) for r in chosen]==[(0x57FE80,0x57FEB1),(0x57FEB1,0x57FEB6),(0x57FEB6,0x58011E),(0x58011E,0x580181),(0x580181,0x580834)]
records=[]
for r in chosen:
 u=ns['off'](r[2]);count=raw[u+2];n=4+2*((count+1)&~1)+(12 if raw[u]>>3&4 else 0)
 records.append(dict(start=hex(ib+r[0]),end_exclusive=hex(ib+r[1]),unwind=hex(ib+r[2]),
  runtime_function_raw=struct.pack('<III',*r).hex(),unwind_raw=raw[u:u+n].hex(),root=[hex(ib+x) for x in root(r)]))
a=0x57FE80;end=0x580834;o=ns['off'](a-ib);data=raw[o:o+end-a];ins=list(ns['md'].disasm(data,a))
assert sum(i.size for i in ins)==len(data)
out=dict(exe_sha256=ns['sha'],address=hex(a),end_exclusive=hex(end),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
 catalog_body_bytes=ns['f'][a][1],decoded_extent_bytes=sum(i.size for i in ins),runtime_function_records_scanned=len(rows),unsupported_records=unsupported,records=records,
 method='A: shipping .pdata/.xdata chained procedure extent; all registered fragments resolving to this primary entry found and byte-checked. No execution.',
 format_reference='https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64?view=msvc-170#chained-unwind-info-structures',
 limits='2484-byte registered extent is not the catalog2105-byte body-set count. Do not treat body-set size as contiguous length or claim every byte is reachable. Original rejected extraction and its script are retained.')
(W/'spawn-load-success-unwind-extent.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,indent=2))
collector=(W/'spawn_load_close_controller.py').read_text().replace('for a in (0x27F5D0,):','for a in (0x57FE80,):').replace('spawn-load-close-controller.json','spawn-load-success-selection.json')
addition='''    if a==0x57FE80:
        proof_path=Path('Database/Tools/work/ASTRA/spawn-load-success-unwind-extent.json')
        extent_proof=json.loads(proof_path.read_text())
        assert extent_proof['exe_sha256']==sha and extent_proof['catalog_body_bytes']==catalog_n
        assert extent_proof['address']==hex(a) and extent_proof['end_exclusive']=='0x580834'
        for row in extent_proof['records']:
            u=off(int(row['unwind'],16)-ib);data=bytes.fromhex(row['unwind_raw'])
            assert raw[u:u+len(data)]==data
        n=extent_proof['bytes']
        assert hashlib.sha256(raw[off(a-ib):off(a-ib)+n]).hexdigest()==extent_proof['sha256']
        out['upstream_sources'][proof_path.as_posix()]=hashlib.sha256(proof_path.read_bytes()).hexdigest()
'''
collector=collector.replace('    if a==0x26C8C0:',addition+'    if a==0x26C8C0:')
(W/'spawn_load_success_selection.py').write_text(collector,encoding='utf-8',newline='\n')
