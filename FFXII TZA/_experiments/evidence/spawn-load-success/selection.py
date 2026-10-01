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

a=0x57FE80;code_end=0x5807B8;end=0x580834;o=ns['off'](a-ib);data=raw[o:o+code_end-a]
ins=list(ns['md'].disasm(data,a));assert sum(i.size for i in ins)==len(data)
index={i.address:i for i in ins};tables=[]
for table,count,bias,jump in [(0x5807B8,18,1,0x57FEAF),(0x580800,13,2,0x58064F)]:
 q=ns['off'](table-ib);d=raw[q:q+4*count];targets=[ib+x for x in struct.unpack('<'+'I'*count,d)]
 assert all(t in index for t in targets)
 tables.append(dict(address=hex(table),raw_hex=d.hex(),sha256=hashlib.sha256(d).hexdigest(),count=count,input_bias=bias,jump_site=hex(jump),targets=[dict(input=i+bias,address=hex(t)) for i,t in enumerate(targets)]))
assert tables[0]['targets'][1]['address']=='0x580356'
# Original branch targets, two original indexed tables, fallthroughs; calls retained as external effects.
jumps={int(t['jump_site'],16):[int(x['address'],16) for x in t['targets']] for t in tables}
seen=set();todo=[a];exits=[];edges=[]
while todo:
 p=todo.pop()
 if p in seen:continue
 assert p in index,hex(p)
 seen.add(p);i=index[p];n=p+i.size;successors=[]
 if i.mnemonic in ('ret','retf'):pass
 elif i.mnemonic=='jmp':
  if p in jumps:successors=jumps[p]
  elif i.op_str.startswith('0x'):
   t=int(i.op_str,16)
   if a<=t<code_end:successors=[t]
   else:exits.append(dict(site=hex(p),target=hex(t)))
  else:raise AssertionError(('unresolved indirect jump',hex(p),i.op_str))
 elif i.mnemonic.startswith('j'):successors=[n,int(i.op_str,16)]
 else:successors=[n]
 for t in successors:assert t in index,(hex(p),hex(t));edges.append((p,t));todo.append(t)
items=[]
for i in ins:
 item=dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)
 targets=[]
 for op in i.operands:
  if op.type==ns['capstone'].x86.X86_OP_MEM and op.mem.base==ns['capstone'].x86.X86_REG_RIP:
   target=i.address+i.size+op.mem.disp;targets.append(dict(address=hex(target),import_name=ns['slots'].get(target)))
 if targets:item['rip_targets']=targets
 items.append(item)
b=dict(address=hex(a),name=ns['f'][a][0],bytes=len(data),catalog_body_bytes=ns['f'][a][1],sha256=hashlib.sha256(data).hexdigest(),instructions=items,
 extent_proof=dict(code_end_exclusive=hex(code_end),registered_end_exclusive=hex(end),records=records,tables=tables,
 reachable_instruction_count=len(seen),reachable_instruction_bytes=sum(index[p].size for p in seen),unreached_in_span=[hex(i.address) for i in ins if i.address not in seen],external_tail_exits=exits,
 limits='All original instruction starts reachable from the entry under original direct branches and two checked table target sets are resolved. Calls are external effect boundaries; CFG reachability is conditional, not path feasibility or execution. There are no unresolved in-span instruction starts after the original table targets are included. The2360-byte code span disagrees with the catalog2105; the mismatch is preserved rather than used as a gate. Registered trailing bytes are two tables, not instructions. Catalog body-set count is not a contiguous extent.'))
assert len(seen)>0 and sum(index[p].size for p in seen)==len(data)
assert len(data)+sum(4*t['count'] for t in tables)==end-a
assert all(i.mnemonic in ('nop','int3') for i in ins if i.address not in seen)
out=dict(exe_sha256=ns['sha'],image_base=hex(ib),method='A only; no original instructions executed',capstone_version=ns['capstone'].__version__,bodies=[b],
 format_reference='https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64?view=msvc-170#chained-unwind-info-structures',
 rejected_attempts=['spawn-load-success-extent-correction.json','spawn-load-success-unwind-rejection.json','spawn-load-success-catalog-mismatch.json'])
(W/'spawn-load-success-selection.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in b.items() if k!='instructions'},indent=2))
for i in items:print(i['address'],i['mnemonic'],i['operands'],i.get('rip_targets',''))
