"""Owner reload local ordering: bounded STATIC_ONLY shipping bytes, no live reachability claim.
Usage: python capture-owner-reload-order.py OUTPUT_JSON. Fresh output required.
The reviewed access-role adapter is imported, identity checked and actually called.
No raw Capstone operand access flags are published as roles.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
import capstone
from capstone.x86_const import X86_OP_MEM

ROOT = pathlib.Path(__file__).resolve().parents[5]
EXE = ROOT / 'Database/Tools/work/exe/FFXII_TZA.exe'
SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ADAPTER = ROOT / 'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
ASH = '5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
BASE = 0x120000
RANGES = [(0x2628b0,0x262f49),(0x330310,0x330497),(0x3304a0,0x3306da),(0x32f850,0x32fa09)]

def main():
    output = pathlib.Path(sys.argv[1])
    if output.exists(): raise ValueError('refused: immutable output already exists')
    raw = EXE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA: raise ValueError('wrong reference image')
    if hashlib.sha256(ADAPTER.read_bytes()).hexdigest() != ASH: raise ValueError('adapter identity changed')
    spec = importlib.util.spec_from_file_location('reviewed_reg_tracking', ADAPTER)
    roles = importlib.util.module_from_spec(spec); spec.loader.exec_module(roles)
    cs = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); cs.detail=True
    pe = struct.unpack_from('<I',raw,0x3c)[0]
    ns = struct.unpack_from('<H',raw,pe+6)[0]; opt = struct.unpack_from('<H',raw,pe+20)[0]
    sections = [struct.unpack_from('<IIII',raw,pe+24+opt+i*40+8) for i in range(ns)]
    def read(a,n):
        for vs,va,rs,ro in sections:
            if BASE+va<=a and a+n<=BASE+va+rs:
                return raw[ro+a-BASE-va:ro+a-BASE-va+n]
        raise ValueError('range not backed by original file bytes')
    def decode(blob,a):
        out=[]
        for ins in cs.disasm(blob,a):
            mem=[]
            for i,op in enumerate(ins.operands):
                if op.type==X86_OP_MEM:
                    m=op.mem; base=ins.reg_name(m.base); index=ins.reg_name(m.index)
                    mem.append(dict(base=base,index=index,scale=m.scale,displacement=m.disp,
                                    size=op.size,role=roles.op_kind(ins,op,i),
                                    rip_target=hex(ins.address+ins.size+m.disp) if base=='rip' else None))
            out.append(dict(pc=hex(ins.address),bytes=ins.bytes.hex(),mnemonic=ins.mnemonic,
                            args=ins.op_str,memory=mem))
        if sum(len(bytes.fromhex(i['bytes'])) for i in out)!=len(blob):
            covered=sum(len(bytes.fromhex(i['bytes'])) for i in out)
            raise ValueError('incomplete decoder span %x: covered %x of %x; next %x' % (a,covered,len(blob),a+covered))
        return out
    # Actual capture invocation path, including the previously misflagged SSE store,
    # address-only LEA and an atomic read/modify/write. A broken role adapter refuses.
    controls=[]
    for blob,expect in [('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:
        rec=decode(bytes.fromhex(blob),0x1000)[0]
        got=rec['memory'][0]['role']; controls.append(dict(bytes=blob,expected=expect,observed=got))
        if got!=expect: raise ValueError('actual capture role control failed')
    result=dict(method='A STATIC_ONLY',exe_sha256=SHA,image_base=hex(BASE),
                adapter_path=str(ADAPTER.relative_to(ROOT)),adapter_sha256=ASH,
                driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                capstone=capstone.__version__,controls=controls,ranges=[])
    for a,b in RANGES:
        blob=read(a,b-a)
        result['ranges'].append(dict(start=hex(a),end_exclusive=hex(b),sha256=hashlib.sha256(blob).hexdigest(),
                                     instructions=decode(blob,a)))
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print('CAPTURED bounded original spans; controls=3; no live/game state or function-extent claim')

if __name__=='__main__': main()
