"""OV29 source discriminator: watcher creation/attachment and common free.

Selected verified original bytes. This does not establish full resource-service
effects or natural title departure. Reuse central access-role invocation controls.
Usage: python capture-title-watcher-attachment.py FRESH_OUTPUT_JSON
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W = pathlib.Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location('verified_capture', W/'capture-index-path.py')
C = importlib.util.module_from_spec(s); s.loader.exec_module(C)
C.RANGES = [(0x2493d0,0x249409),(0x24a440,0x24a477),
            (0x2487a0,0x248a89),(0x2473b0,0x2473e7),
            (0x2482e0,0x24840e),(0x2fa560,0x2fa73c),
            (0x1b1960,0x1b1a16)]
C.main()
p=pathlib.Path(sys.argv[1]);r=json.loads(p.read_text())
# The controller dispatch has exactly19 entries: decrement message then CMP12h.
# Record data as data; never decode the trailing .pdata region as instructions.
d=C.EXE.read_bytes();pe=struct.unpack_from('<I',d,0x3c)[0]
opt=struct.unpack_from('<H',d,pe+20)[0];ns=struct.unpack_from('<H',d,pe+6)[0]
def read(va,n):
    for i in range(ns):
        vs,sva,rs,ro=struct.unpack_from('<IIII',d,pe+24+opt+i*40+8)
        if C.BASE+sva<=va and va+n<=C.BASE+sva+rs:
            return d[ro+va-C.BASE-sva:ro+va-C.BASE-sva+n]
    raise ValueError('unbacked table')
if read(0x58288e,3)!=bytes.fromhex('83f812') or read(0x582889,2)!=bytes.fromhex('ffc8'):
    raise ValueError('controller table guard identity')
table=read(0x582f54,19*4)
edges=[C.BASE+x for x in struct.unpack('<19I',table)]
if any(not 0x582860<=x<0x582f51 for x in edges):
    raise ValueError('controller table edge outside selected code')
r.update(invocation_driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    wrapper_complete=True,
    controller_message_table=dict(address='0x582f54',bytes=table.hex(),sha256=hashlib.sha256(table).hexdigest(),
        guard_pc='0x58288e',entries=19,edges=[hex(x) for x in edges],message18=hex(edges[17])),
    limits='selected original normal-code spans and guard-derived table; no live state, no complete transitive helper effects, no all-caller or natural-lifetime closure')
p.write_text(json.dumps(r,indent=2)+'\n')
