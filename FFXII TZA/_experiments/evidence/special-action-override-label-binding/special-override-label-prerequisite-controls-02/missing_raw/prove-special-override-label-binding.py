"""Bind original override state to nine literal labels and eight native words.

Only the reached straight-line initializer and exact formatter arm are proved.
No constructor-return, all-writer, alias/lifetime or natural action guarantee.
"""
import hashlib,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('C:\\Users\\Kristian\\source\\repos\\XIIOnline')
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable output exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PIN='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
exe=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe';b=exe.read_bytes()
if sha(exe)!=PIN:raise ValueError('original image prerequisite')
p=struct.unpack_from('<I',b,0x3c)[0];opt=struct.unpack_from('<H',b,p+20)[0]
ss=[struct.unpack_from('<IIII',b,p+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,p+6)[0])]
def read(a,n):
    for _,va,rs,ro in ss:
        if 0x120000+va<=a and a+n<=0x120000+va+rs:return b[ro+a-0x120000-va:ro+a-0x120000-va+n]
    raise ValueError('unbacked original bytes')
records={};inputs=[];captures={}
for name,driver in [('special-override-constructor-dependencies-raw-01.json','capture-special-override-constructor-dependencies.py'),
                    ('special-override-formatting-effects-raw-01.json','capture-special-override-formatting-effects.py'),
                    ('special-override-control-raw-01.json','capture-special-override-control.py')]:
    f=W/name;r=json.loads(f.read_text());captures[name]=r
    if r.get('exe_sha256')!=PIN or r.get('wrapper_complete') is not True:
        raise ValueError('capture completion prerequisite')
    if r.get('driver_sha256')!=sha(W/'capture-index-path.py') or r.get('invocation_driver_sha256')!=sha(W/driver):
        raise ValueError('actual capture driver prerequisite')
    if len(r.get('controls',[]))!=3 or any(c['observed']!=c['expected'] for c in r['controls']):
        raise ValueError('actual access-role prerequisite')
    for s in r['ranges']:
        start=int(s['start'],16);end=int(s['end_exclusive'],16);blob=read(start,end-start)
        if hashlib.sha256(blob).hexdigest()!=s['sha256']:raise ValueError('original span prerequisite')
        cursor=start
        for i in s['instructions']:
            pc=int(i['pc'],16);z=bytes.fromhex(i['bytes'])
            if pc!=cursor or not z or read(pc,len(z))!=z:raise ValueError('original instruction/coverage prerequisite')
            cursor+=len(z)
            if pc in records and records[pc]!=i:raise ValueError('overlapping source disagreement')
            records[pc]=i
        if cursor!=end:raise ValueError('incomplete source coverage')
    inputs.append(dict(path=name,sha256=sha(f),driver=driver,driver_sha256=sha(W/driver)))
required={0x1d03c3:('mov','rdi, rcx'),0x1cd141:('mov','r15, rcx'),
          0x1cd1ba:('lea','eax, [r13 - 1]'),0x1cd1be:('cmp','eax, 0x125'),
          0x1ce9aa:('movsxd','rax, dword ptr [r15 + 0xae0]'),
          0x1ce9b1:('shl','rax, 5'),0x1ce9b5:('lea','rcx, [r15 + 0xae4]'),
          0x1ce9bc:('add','rcx, rax'),0x1ce9bf:('mov','qword ptr [rsp + 0x28], rcx'),
          0x1ce9c4:('jmp','0x1cd57f'),
          0x1cd57f:('lea','r8, [rip + 0x73255a]'),0x1cd586:('jmp','0x1cd4ff'),
          0x1cd4ff:('mov','r9, r14'),0x1cd50a:('mov','edx, 0x100'),
          0x1cd514:('mov','rcx, r12'),0x1cd517:('call','0x19c5d0'),
          0x1d2df2:('mov','ecx, dword ptr [rdi + 0xae0]'),
          0x1d2df8:('dec','ecx'),0x1d2dfa:('call','0x2f7a00'),
          0x2f79e0:('movdqa','xmm0, xmmword ptr [rip + 0xa17ff8]'),
          0x2f79e8:('movdqu','xmmword ptr [rip + 0x1fc6f40], xmm0'),
          0x2f7a00:('mov','dword ptr [rip + 0x1bf40ea], ecx')}
for pc,v in required.items():
    if pc not in records or (records[pc]['mnemonic'],records[pc]['args'])!=v:raise ValueError('label/index source witness changed')
for pc,target,role,size in [(0x2f79e0,'0xd0f9e0','r',16),(0x2f79e8,'0x22be930','w',16),
                            (0x2f7a00,'0x1eebaf0','w',4),(0x1cd57f,'0x8ffae0','addr',8)]:
    m=records[pc]['memory']
    if len(m)!=1 or (m[0]['rip_target'],m[0]['role'],m[0]['size'])!=(target,role,size):
        raise ValueError('native word/index/format identity prerequisite')
fmt=read(0x8ffae0,32).split(b'\0',1)[0]
if not fmt or b'%s' not in fmt:raise ValueError('literal string-format prerequisite')
r=captures['special-override-formatting-effects-raw-01.json'];table=read(0x1cfcec,294*4)
edges=[0x120000+x for x in struct.unpack('<294I',table)]
if r['switch_table']['bytes']!=table.hex() or r['switch_table']['entries']!=294 or r['switch_table']['edges']!=[hex(x) for x in edges]:
    raise ValueError('guard-derived switch data prerequisite')
ids=[j+1 for j,x in enumerate(edges) if x==0x1ce9aa]
if ids!=[182]:raise ValueError('formatter item identity')
fragment=[records[pc] for pc in sorted(records) if 0x1d03e1<=pc<=0x1d04d1]
if not fragment or any(i['mnemonic'].startswith('j') or i['mnemonic'] in ['call','ret'] for i in fragment):
    raise ValueError('initializer is not an uninterrupted straight-line fragment')
labels=[{} for _ in range(9)];writes=[]
families={'rax':'a','eax':'a','ax':'a','al':'a','rcx':'c','ecx':'c','cx':'c','cl':'c','xmm0':'x0'}
for j,i in enumerate(fragment):
    ms=[m for m in i['memory'] if m['base']=='rdi' and 0xae4<=m['displacement']<0xc04 and m['role'] in ['w','rw']]
    if not ms:continue
    if len(ms)!=1 or i['mnemonic'] not in ['mov','movsd'] or ms[0]['role']!='w':raise ValueError('unsupported initializer effect')
    m=ms[0];off=m['displacement']-0xae4;slot,local=divmod(off,32);n=m['size']
    if local+n>32:raise ValueError('cross-slot label store')
    rhs=i['args'].split(', ',1)[1];sources=[]
    if rhs.startswith('0x') or rhs.isdigit():z=(int(rhs,0)&((1<<(8*n))-1)).to_bytes(n,'little')
    else:
        if j==0:raise ValueError('missing literal source')
        prev=fragment[j-1];dst=prev['args'].split(', ',1)[0]
        if families.get(dst)!=families.get(rhs) or families.get(rhs) is None:raise ValueError('literal register binding')
        if prev['mnemonic']=='movabs':z=(int(prev['args'].split(', ',1)[1],0)&((1<<(8*n))-1)).to_bytes(n,'little')
        elif prev['mnemonic'] in ['mov','movzx','movsd']:
            loads=[x for x in prev['memory'] if x['base']=='rip' and x['role']=='r']
            if len(loads)!=1 or loads[0]['size']!=n:raise ValueError('literal original load width')
            a=int(loads[0]['rip_target'],16);z=read(a,n);sources.append(dict(address=hex(a),bytes=z.hex()))
        else:raise ValueError('unsupported literal source; never fabricate zero')
    for k,x in enumerate(z):
        if local+k in labels[slot] and labels[slot][local+k]!=x:raise ValueError('conflicting label byte')
        labels[slot][local+k]=x
    writes.append(dict(pc=i['pc'],slot=slot,local=local,bytes=z.hex(),sources=sources))
rows=[];words=list(struct.unpack('<8H',read(0xd0f9e0,16)))
for slot,d in enumerate(labels):
    data=[]
    for k in range(32):
        if k not in d:raise ValueError('missing terminator/prefix evidence; padding is unknown')
        if d[k]==0:break
        data.append(d[k])
    else:raise ValueError('no original NUL within label slot')
    z=bytes(data);name=z.decode('ascii')
    rows.append(dict(state=slot,display_label=name,label_offset=hex(0xae4+32*slot),native_override_index=slot-1,
                     native_action_word=None if slot==0 else words[slot-1],known_prefix_bytes=(z+b'\0').hex(),
                     remaining_slot_bytes='unproved, not fabricated defaults'))
if rows[0]['display_label']!='OFF':raise ValueError('OFF positive control')
result=dict(question='What exact label representation accompanies initialized special-action override states0..8?',
            hypotheses=['eight arbitrary pointer labels','nine32-byte inline label slots, OFF plus eight native-word-correlated selections'],
            method='A retained original code/constants and explicit straight-line store reduction; no execution',
            exe_sha256=PIN,driver_sha256=sha(pathlib.Path(__file__)),inputs=inputs,formatter_item=182,
            labels=rows,writes=writes,format_literal=dict(address='0x8ffae0',bytes=fmt.hex(),text=fmt.decode('ascii')),
            controls=dict(off_literal=True,guard_bound294=True,valid_index_slot_bounds=all(0xae4<=0xae4+32*x<0xc04 for x in range(9)),
                          first_outside_slot=hex(0xae4+32*9)),
            established='On reaching/completing1D03E1..1D04D1, nine original NUL-terminated ASCII labels are stored atAE4+state*32. Formatter item182 selects with signed stateAE0 and no local index clamp. Control separately writes state-1 to the native override index; word correlation is conditional on unchanged state/table.',
            limits='Labels are original debug display names, not independently proved combat semantics. Unwritten padding is unknown. Full constructor return, intervening writers, aliases, lifetime, runtime binding, natural selection and other producers remain OPEN. R15 is reused in other formatter branches; this result does not claim whole-function object effects. No external review run is counted as our execution.')
out.write_text(json.dumps(result,indent=2)+'\n');print('ESTABLISHED original nine-slot label representation and conditional word correlation')
for x in rows:print(x['state'],x['display_label'],x['native_action_word'])
