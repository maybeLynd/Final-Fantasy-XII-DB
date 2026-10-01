"""Exact source for the constructor's remaining formatter effect boundary.

The pdata fragment includes inline switch data. Code ends at verified RET
1CFCEB; the 294-entry table is separate data, derived from CMP125h. Do not
repeat the earlier whole-pdata-as-code capture mistake.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W=pathlib.Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('verified_capture', W/'capture-index-path.py')
C=importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
b=C.EXE.read_bytes()
if hashlib.sha256(b).hexdigest()!=C.SHA: raise ValueError('reference prerequisite')
p=struct.unpack_from('<I',b,0x3c)[0]; opt=struct.unpack_from('<H',b,p+20)[0]
ss=[struct.unpack_from('<IIII',b,p+24+opt+i*40+8) for i in range(struct.unpack_from('<H',b,p+6)[0])]
def read(a,n):
    for _,va,rs,ro in ss:
        if C.BASE+va<=a and a+n<=C.BASE+va+rs:
            return b[ro+a-C.BASE-va:ro+a-C.BASE-va+n]
    raise ValueError('unbacked source')
C.RANGES=[(0x1cd0e0,0x1cfcec)]
C.main()
out=pathlib.Path(sys.argv[1]);r=json.loads(out.read_text());ins={int(i['pc'],16):i for s in r['ranges'] for i in s['instructions']}
for pc,expected in {0x1cd1ba:('lea','eax, [r13 - 1]'),0x1cd1be:('cmp','eax, 0x125'),
                    0x1cd1c3:('ja','0x1cfc86'),0x1cd1cb:('mov','ecx, dword ptr [rsi + rax*4 + 0xafcec]'),
                    0x1cd1d5:('jmp','rcx'),0x1cfceb:('ret','')}.items():
    if (ins[pc]['mnemonic'],ins[pc]['args'])!=expected: raise ValueError('source extent/switch guard prerequisite')
table=read(0x1cfcec,294*4);edges=[C.BASE+x for x in struct.unpack('<294I',table)]
if any(x not in ins for x in edges):raise ValueError('switch edge not in recorded original code')
ids=read(0x8fce00,22*4)
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),wrapper_complete=True,
         switch_table=dict(address='0x1cfcec',entries=294,guard_pc='0x1cd1be',bytes=table.hex(),sha256=hashlib.sha256(table).hexdigest(),edges=[hex(x) for x in edges]),
         constructor_menu_ids=dict(address='0x8fce00',bytes=ids.hex(),sha256=hashlib.sha256(ids).hexdigest(),values=list(struct.unpack('<22I',ids))),
         limits='Bounded static original formatter source and guard-derived data; call effects, alias and constructor completion remain unproved until reducer closure')
out.write_text(json.dumps(r,indent=2)+'\n')
print('CAPTURED formatter code and separate294-entry data table; no constructor-return theorem asserted')
