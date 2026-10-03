"""Complete caller CFG stack accounting, under an explicit normal-ABI premise."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,text):
    if not ok:raise ValueError(text)
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def offsets(graph,index):
    todo=[(graph['entry'],0)];seen={};result={}
    while todo:
        pc,delta=todo.pop()
        if pc in seen:
            need(seen[pc]==delta,'path-dependent stack delta');continue
        seen[pc]=delta;result[pc]=delta
        instruction=index[pc];m,a=instruction['mnemonic'],instruction['args']
        if m=='push':after=delta-8
        elif m=='pop':after=delta+8
        elif m in ('add','sub') and a.startswith('rsp, '):
            value=int(a.split(', ')[1],0);after=delta+(value if m=='add' else -value)
        else:after=delta
        # Opaque calls are modelled ONLY by normal ABI restoration, not effects.
        for successor in graph['edges'][pc]:todo.append((successor,after))
    return result
def main(output,source):
    need(not output.exists(),'fresh output required')
    for tag,driver in [('extents-01','prepare.py'),('capture-01','capture.py')]:
        state=json.loads((source/(tag+'.status.json')).read_text())
        need(state.get('terminal') is True and state.get('exit')==0 and state.get('exception') is None and state.get('driver_sha256')==sha(source/driver)
             and(source/(tag+'.stdout')).read_bytes() and not(source/(tag+'.stderr')).read_bytes(),'required upstream failed: '+tag)
    metadata=json.loads((source/'extents-01.json').read_text())
    raw=json.loads((source/'source-01.json').read_text())
    need(metadata.get('complete') is True and metadata.get('driver_sha256')==sha(source/'prepare.py')
         and raw.get('wrapper_complete') is True and raw.get('invocation_driver_sha256')==sha(source/'capture.py'),'incomplete metadata/wrapper')
    need(raw.get('exe_sha256')=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8','wrong image')
    roles=module('reviewed_roles',W/'validate-title-source-annotations.py').validate(raw)
    expected=[('0x331990','0x3319c4'),('0x378a60','0x378b71')]
    need([(r['start'],r['end_exclusive']) for r in raw['ranges']]==expected,'incomplete body population')
    for captured,body in zip(raw['ranges'],metadata['bodies']):
        bytes_=bytes.fromhex(''.join(i['bytes'] for i in captured['instructions']))
        need(bytes_.hex()==body['physical_bytes'] and hashlib.sha256(bytes_).hexdigest()==body['sha256'],'metadata physical mismatch')
    index={int(i['pc'],16):i for r in raw['ranges'] for i in r['instructions']}
    pins=[(0x331990,'push','rbx'),(0x331992,'sub','rsp, 0x20'),(0x33199d,'xor','r8d, r8d'),
          (0x3319a4,'call','0x378a60'),(0x3319b0,'mov','r8d, 1'),(0x3319ba,'add','rsp, 0x20'),
          (0x3319be,'pop','rbx'),(0x3319bf,'jmp','0x378a60'),(0x378a74,'push','r14'),
          (0x378a76,'sub','rsp, 0x30'),(0x378b2b,'call','0x377dc0'),(0x378b6a,'add','rsp, 0x30'),
          (0x378b6e,'pop','r14'),(0x378b70,'ret','')]
    for pc,m,a in pins:need((index[pc]['mnemonic'],index[pc]['args'])==(m,a),'original stack/call operation changed: '+hex(pc))
    cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
    rsp_writers=[]
    for r in raw['ranges']:
        for instruction in cs.disasm(bytes.fromhex(''.join(i['bytes'] for i in r['instructions'])),int(r['start'],16)):
            if any(instruction.reg_name(reg) in ('rsp','esp','sp','spl') for reg in instruction.regs_access()[1]):
                m,a=instruction.mnemonic,instruction.op_str
                need(m in ('push','pop','call','ret') or (m in ('add','sub') and a.startswith('rsp, ')),'unmodelled stack writer')
                rsp_writers.append(hex(instruction.address))
    helper=W/'prove_owner_reload_order.py'
    need(sha(helper)=='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864','reviewed CFG helper changed')
    G=module('reviewed_cfg',helper)
    caller=G.graph(index,0x331990,0x3319c4,tail='0x378a60');wrapper=G.graph(index,0x378a60,0x378b71)
    need(caller['tails']==[0x3319bf] and not caller['returns'] and wrapper['returns']==[0x378b70],'closed call/tail boundary changed')
    first,second=offsets(caller,index),offsets(wrapper,index)
    need(first[0x3319a4]==-40 and first[0x3319bf]==0 and second[0x378b2b]==-56 and second[0x378b70]==0,'stack accounting changed')
    retained=W/'sd194-copier-limit/retained/source-01.json'
    need(sha(retained)=='2c66378a2f9fb4125671f1f5f5ee4211a7397abf52e904137ba474a07e5a9fa8','retained loader identity changed')
    old=json.loads(retained.read_text());old_ix={int(i['pc'],16):i for r in old['ranges'] for i in r['instructions']}
    need((old_ix[0x377dc0]['mnemonic'],old_ix[0x377dc0]['args'])==('mov','r11, rsp')
         and(old_ix[0x377dc8]['mnemonic'],old_ix[0x377dc8]['args'])==('lea','rbp, [r11 - 0x1a8]')
         and(old_ix[0x377dff]['mnemonic'],old_ix[0x377dff]['args'])==('lea','r8, [rbp + 0x60]'),'retained name input offset changed')
    input_offset=-0x1a8+0x60
    mode0_entry=first[0x3319a4]-8+second[0x378b2b]-8
    mode1_entry=first[0x3319bf]+second[0x378b2b]-8
    input0,input1=mode0_entry+input_offset,mode1_entry+input_offset
    need((mode0_entry,mode1_entry,input0,input1)==(-112,-64,-440,-392) and input1-input0==48,'buffer delta changed')
    result=dict(producer_complete=True,method='A STATIC_ONLY complete original caller CFG/stack proof; no machine-code or game execution',
        driver_sha256=sha(Path(__file__)),source_pins=[dict(path='source-01.json',sha256=sha(source/'source-01.json')),
             dict(path='retained-loader-source-01.json',sha256=sha(retained))],annotation_prerequisite=roles,
        original_bytes=325,operation_pins=len(pins),actual_rsp_writers=rsp_writers,
        premise='Normal return restores opaque-call RSP; valid private stack/noninterference/intact code. Both request legs reach the named377DC0 boundary.',
        relative_to_331990_entry_rsp=dict(mode0_loader_entry=mode0_entry,mode1_loader_entry=mode1_entry,
            mode0_name_input=input0,mode1_name_input=input1,name_input_delta=48),
        admitted_260_byte_name_spans=dict(mode0=[input0,input0+260],mode1=[input1,input1+260],overlap_bytes=212,interval_convention='half-open; admitted successful-lookup capacity, not actual observed contents'),
        semantic_implication='Second mode1 uses a name input48bytes above mode0. Same-address inheritance is refuted under stated normal ABI paths; different buffers are not disjoint spans.',
        limits=['Mode0 can skip request entirely and wrapper has additional gates/opaque calls; both entries are premises, not reachability proof.',
                'Other intervening helpers, former stack use and sequential alias overlap prevent a guarantee of surviving mode0 bytes.',
                'No actual null-slot contents/name/field entry/scheduling/queue acceptance/native effect or game consequence.',
                'Original source and producer controls are not independent acceptance.'])
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(producer_complete=True,original_bytes=325,name_input_delta=48,native_or_live_runs=0)))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);parser.add_argument('--source',type=Path,default=P)
    args=parser.parse_args();main(args.output,args.source)
