"""Reuse retained SECTION09 bodies; verify shipping identity and actual reviewed roles.
All selected bytes are already retained. No native/live execution.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import sys
import capstone
from capstone.x86_const import X86_OP_MEM

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
UP=ROOT/'Database/FFXII TZA/_experiments/evidence/continuation-section09-owner-producer'
MSHA='23785132366d8f1464b42ccfec0e1d9d4cbec05a04d733b212270f867a7e9de8'
DSHA='9cb269e7008618d928cb575d5f65a05c544b56da14ac031ffe972182aa0a7304'
ESHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
ASHA='5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38'
ENTRIES=[0x3dd4c0,0x32f240]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main(out,up):
    if out.exists():raise ValueError('immutable source exists')
    if sha(up/'original_body_manifest.json')!=MSHA or sha(up/'original_disassembly.txt')!=DSHA:
        raise ValueError('retained source identity changed')
    if sha(ADAPTER)!=ASHA:raise ValueError('reviewed adapter changed')
    spec=importlib.util.spec_from_file_location('reviewed_queue_order_roles',ADAPTER)
    roles=importlib.util.module_from_spec(spec);spec.loader.exec_module(roles)
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    data=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(data).hexdigest()!=ESHA:raise ValueError('wrong original image')
    pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0]
    secs=[struct.unpack_from('<IIII',data,pe+32+opt+40*k) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
    def read(a,n):
        for vs,rva,size,offset in secs:
            if 0x120000+rva<=a and a+n<=0x120000+rva+size:return data[offset+a-0x120000-rva:offset+a-0x120000-rva+n]
        raise ValueError('unbacked original bytes')
    def decode(blob,start):
        records=[]
        for ins in cs.disasm(blob,start):
            mem=[]
            for k,op in enumerate(ins.operands):
                if op.type==X86_OP_MEM:
                    m=op.mem;base=ins.reg_name(m.base)
                    mem.append(dict(base=base,index=ins.reg_name(m.index),scale=m.scale,displacement=m.disp,
                                    size=op.size,role=roles.op_kind(ins,op,k),
                                    rip_target=hex(ins.address+ins.size+m.disp) if base=='rip' else None))
            records.append(dict(pc=hex(ins.address),bytes=ins.bytes.hex(),mnemonic=ins.mnemonic,args=ins.op_str,memory=mem))
        if not records or sum(len(bytes.fromhex(i['bytes'])) for i in records)!=len(blob):raise ValueError('incomplete decode')
        return records
    controls=[]
    for blob,expected in [('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:
        got=decode(bytes.fromhex(blob),0x1000)[0]['memory'][0]['role']
        if got!=expected:raise ValueError('actual shared-role control failed')
        controls.append(dict(bytes=blob,expected=expected,observed=got))
    text=(up/'original_disassembly.txt').read_text()
    manifest=json.loads((up/'original_body_manifest.json').read_text())
    ranges=[]
    for entry in ENTRIES:
        f=next(f for f in manifest['functions'] if int(f['entry'],16)==entry)
        if len(f['ranges'])!=1:raise ValueError('selected manifest boundary changed')
        lo=int(f['ranges'][0]['start'],16);hi=int(f['ranges'][0]['end'],16)+1
        heading=re.search(r'^FUNCTION '+format(entry,'08X')+r' .*$',text,re.M)
        if not heading:raise ValueError('missing retained body')
        end=text.find('\nFUNCTION ',heading.end());body=text[heading.end():end if end>=0 else None]
        lines=re.findall(r'^([0-9A-F]{8})  ([0-9a-f]+)\s+([^\n]*)$',body,re.M)
        cursor=lo;retained=b'';boundaries=[]
        for pc,hx,annotation in lines:
            if int(pc,16)!=cursor:raise ValueError('retained disassembly has missing/overlapping bytes')
            blob=bytes.fromhex(hx);retained+=blob;boundaries.append((cursor,hx));cursor+=len(blob)
        if cursor!=hi or len(retained)!=f['bytes'] or hashlib.sha256(retained).hexdigest()!=f['sha256']:
            raise ValueError('retained body population/hash changed')
        if retained!=read(lo,hi-lo):raise ValueError('retained body differs from original EXE')
        instructions=decode(retained,lo)
        if [(int(i['pc'],16),i['bytes']) for i in instructions]!=boundaries:raise ValueError('retained instruction boundaries changed')
        ranges.append(dict(start=hex(lo),end_exclusive=hex(hi),sha256=f['sha256'],instructions=instructions))
    extra=[]
    for folder,name,pin,entry,end,body_sha in [
      ('bts-index-binding','index-path-raw-02.json','aa1325dd3ada5ca52a7c6173215c973031fc5ee9f38b9ef4f22bfd5f808f0e12',0x32ed80,0x32f16a,'2191ab4f7437185e353212dea4fa6ac2970fffaa641952775907011d1c613aae'),
      ('owner-reload-order','owner-reload-order-source-01.json','e581b090e37f559144f18ab9c8e73dcbc6d9787fc8f92b78b02faa183244e9ec',0x32f850,0x32fa09,None)]:
        path=ROOT/'Database/FFXII TZA/_experiments/evidence'/folder/name
        if sha(path)!=pin:raise ValueError('retained producer dependency changed')
        raw=json.loads(path.read_text());q=next(q for q in raw['ranges'] if int(q['start'],16)==entry)
        blob=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
        if int(q['end_exclusive'],16)!=end or blob!=read(entry,end-entry):raise ValueError('retained producer range identity changed')
        digest=hashlib.sha256(blob).hexdigest()
        if digest!=q['sha256']:raise ValueError('retained producer body hash changed')
        if entry==0x32ed80 and digest!=body_sha:raise ValueError('original reset hash changed')
        ranges.append(dict(start=hex(entry),end_exclusive=hex(end),sha256=digest,instructions=decode(blob,entry)))
        extra.append(dict(path=str(path.relative_to(ROOT)),sha256=pin,selected_range=hex(entry),body_sha256=digest))
    result=dict(method='A RETAINED_PRODUCER_GATE_SOURCE_QUALIFICATION',
      exe_sha256=ESHA,image_base='0x120000',adapter_sha256=ASHA,adapter_path=str(ADAPTER.relative_to(ROOT)),
      capstone=capstone.__version__,driver_sha256=sha(Path(__file__)),controls=controls,ranges=ranges,
      dependency=dict(path=str(up.relative_to(ROOT)) if up.is_relative_to(ROOT) else str(up),manifest_sha256=MSHA,disassembly_sha256=DSHA),
      retained_extra=extra,
      limits='Identity/annotations only; no synthetic execution, natural initialization, live queue observations or independent semantic acceptance')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('QUALIFIED_RETAINED_PRODUCER_GATE_BODIES:'+str(len(ranges))+'; all retained bytes; role controls3; native/game0')


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]) if len(sys.argv)>2 else UP)
