"""Qualify retained original bodies and capture only missing spawn binding code.

No native/live execution. Retained records remain immutable; every new memory
annotation uses the reviewed shared adapter through the actual invocation path.
"""
import hashlib, importlib.util, json, pathlib, re, sys
import capstone
from capstone.x86_const import X86_OP_MEM
W = pathlib.Path(__file__).resolve().parent

def module(name, file):
    s = importlib.util.spec_from_file_location(name, W / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

C = module('spawn_capture', 'capture-index-path.py')
S = module('spawn_annotations', 'validate-title-source-annotations.py')
INPUT_MANIFEST = '2534bc9eea8804fb2335c742cfa85f5db27a99d868d7f945a013099c1836a334'
NEW = [(0x25ad10,0x25adf5), (0x25af60,0x25afb4), (0x263d40,0x263dc7),
       (0x269860,0x2699cc), (0x34fa70,0x34fb07), (0x2640c0,0x2640c8),
       (0x3dbb60,0x3dbbd8)]
OLD = ['0025DF00', '0025E4C0', '00358940']
SECTION = ['00263FF0','003587C0','00358A00','003DB6E0','003DB7A0','003DBCF0','003DBDC0']
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out = pathlib.Path(sys.argv[1])
    if out.exists(): raise ValueError('immutable source exists')
    inputs = W / 'regfile-spawn-record-inputs-01'
    if sha(inputs/'manifest.json') != INPUT_MANIFEST: raise ValueError('retained input manifest changed')
    manifest = json.loads((inputs/'manifest.json').read_text())
    for x in manifest['members']:
        p = inputs/x['path']
        if p.stat().st_size != x['bytes'] or sha(p) != x['sha256']:
            raise ValueError('retained input changed')
    C.RANGES = NEW; C.main(); v = json.loads(out.read_text())
    spec = importlib.util.spec_from_file_location('retained_roles', C.ADAPTER)
    roles = importlib.util.module_from_spec(spec); spec.loader.exec_module(roles)
    cs = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); cs.detail = True
    def qualify(a,z,origin):
        records=[]
        for i in cs.disasm(z,a):
            memory=[]
            for k,op in enumerate(i.operands):
                if op.type != X86_OP_MEM: continue
                m=op.mem; base=i.reg_name(m.base)
                memory.append(dict(base=base,index=i.reg_name(m.index),scale=m.scale,
                    displacement=m.disp,size=op.size,role=roles.op_kind(i,op,k),
                    rip_target=hex(i.address+i.size+m.disp) if base=='rip' else None))
            records.append(dict(pc=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,memory=memory))
        if sum(len(bytes.fromhex(i['bytes'])) for i in records)!=len(z):
            raise ValueError('retained decode incomplete')
        return dict(start=hex(a),end_exclusive=hex(a+len(z)),sha256=hashlib.sha256(z).hexdigest(),instructions=records,origin=origin)
    old=json.loads((inputs/'regfile-observation.json').read_text())
    if old['executable_sha256'] != C.SHA: raise ValueError('retained reference changed')
    for k in OLD:
        q=old['bodies'][k];z=bytes.fromhex(q['raw_hex'])
        if len(z)!=q['bytes'] or hashlib.sha256(z).hexdigest()!=q['sha256']:
            raise ValueError('retained original body incomplete')
        v['ranges'].append(qualify(int(k,16),z,'retained regfile-observation:'+k))
    section=json.loads((inputs/'section12-original-body-manifest.json').read_text())
    if section['exe_sha256'] != C.SHA: raise ValueError('SECTION12 reference changed')
    dis=(inputs/'section12-original-disassembly.txt').read_text()
    for k in SECTION:
        q=next(q for q in section['bodies'] if q['entry']==k)
        block=re.search(r'^=== '+k+r' .*?\n(.*?)(?=^=== |\Z)',dis,re.M|re.S)
        if not block: raise ValueError('retained disassembly missing')
        rows=re.findall(r'^([0-9A-F]{8})\s+([0-9a-f]+)\s',block.group(1),re.M)
        z=bytes.fromhex(''.join(h for _,h in rows));a=int(k,16);cursor=a
        for pc,h in rows:
            if int(pc,16)!=cursor: raise ValueError('retained disassembly gap')
            cursor+=len(bytes.fromhex(h))
        if len(z)!=q['length'] or hashlib.sha256(z).hexdigest()!=q['sha256']:
            raise ValueError('retained SECTION12 body changed')
        v['ranges'].append(qualify(a,z,'retained SECTION12:'+k))
    v.update(wrapper_complete=True,invocation_driver_sha256=sha(pathlib.Path(__file__)),
        retained_input_manifest_sha256=INPUT_MANIFEST,
        annotation_prerequisite=S.validate(v),new_bytes=sum(b-a for a,b in NEW),
        limits='Retained source qualification plus seven missing bounded spans; no repeated census/native/live run. Interpreter prefix is not its complete body.')
    out.write_text(json.dumps(v,indent=2)+'\n')
    print('Qualified ten retained bodies and seven missing spans with reviewed access roles; no game')

if __name__=='__main__': main()
