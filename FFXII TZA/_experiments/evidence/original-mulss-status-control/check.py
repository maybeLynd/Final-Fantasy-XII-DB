"""Read-only bounded native/guest status evidence; never re-executes a code page."""
import hashlib,importlib.util,json,struct,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());pre=json.loads((W/'native-preflight.json').read_text());source=raw['source'];ref=source['reference']
assert raw['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())==pre['driver_sha256'] and source==pre['source'] and raw['tools']==pre['tools']
parent=(R/'parent237.bin').read_bytes();op=(R/'original4.bin').read_bytes();code=(R/'wrapper.bin').read_bytes()
assert len(parent)==237 and sha(parent)==ref['parent237_sha256'] and op==parent[0x46912E-0x4690B0:0x469132-0x4690B0]==bytes.fromhex('f30f59d2') and ref['original_entry']=='0x46912e' and ref['original_bytes']==op.hex() and ref['original_bytes_count']==4
assert sha((R/'parent-manifest.json').read_bytes())==ref['parent_manifest_sha256']
praw=json.loads((R/'parent-raw.json').read_text());assert praw['source']['reference']['body_sha256']==ref['parent237_sha256']
sp=importlib.util.spec_from_file_location('rd',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image();assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8' and parent==rd.img_rd(image,ss,0x4690B0,237) and op==rd.img_rd(image,ss,0x46912E,4)
assert code.hex()==source['wrapper_hex'] and sha(code)==source['wrapper_sha256'] and code[source['original_offset']:source['original_offset']+4]==op
assert code==bytes.fromhex('4883ec180fae1c24c7442404801f00000fae542404660f6ed1f30f59d2660f7ed00fae1a448b0424448942040fae14240fae5a084883c418c3')
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);seq=list(cs.disasm(code,0x1000));assert len(seq)==14 and sum(i.size for i in seq)==len(code)
assert [dict(pc=hex(i.address),bytes=i.bytes.hex(),op=i.mnemonic,args=i.op_str) for i in seq]==source['instructions']
assert not any(i.mnemonic=='call' or i.mnemonic.startswith('j') for i in seq)
cases=raw['cases'];assert len(cases)==3 and cases==json.loads((W/'in-progress-cases.json').read_text())
observations=[]
for c,name,inp,result_bits,status in zip(cases,['exact-five','next-above-five','private-omit-mul'],['40a00000','40a00001','40a00001'],['41c80000','41c80003','40a00001'],[0x1F80,0x1FA0,0x1F80]):
 assert c['name']==name and c['mutated']==(name=='private-omit-mul')
 running=bytearray(code)
 if c['mutated']:running[source['original_offset']:source['original_offset']+4]=b'\x90'*4
 assert c['running_hex']==running.hex() and (running[source['original_offset']:source['original_offset']+4]==op)!=c['mutated']
 native,guest=c['native'],c['guest'];assert native['input_bits']==guest['input_bits']==inp and native['result_bits']==guest['result_bits']==result_bits
 assert native['running_sha256']==guest['running_sha256']==sha(running)
 assert native['before_output_words']==guest['before_output_words']==['a5a5a5a5']*4
 n=[int(x,16) for x in native['after_output_words']];g=[int(x,16) for x in guest['after_output_words']]
 assert n[0]==status and n[1]==n[2] and n[3]==0xA5A5A5A5 and g==[0x1F80,0x1FA0,0x1FA0,0xA5A5A5A5]
 assert native['freed'] and native['after_free_state']=='0x10000'
 assert guest['failure'] is None and guest['stop_pc']=='0x10000' and guest['rsp']=='0x60001810' and guest['initial_mxcsr']==guest['after_mxcsr']=='0x1fa0'
 actual_seq=list(cs.disasm(running,0x1000));assert guest['visits']==[hex(i.address) for i in actual_seq] and 0<len(guest['visits'])<64 and actual_seq[-1].mnemonic=='ret'
 expected_writes=[('0x1004','0x600017f0',4,0x1FA0),('0x1008','0x600017f4',4,0x1F80),('0x1021','0x40000100',4,0x1F80),('0x1028','0x40000104',4,0x1FA0),('0x1030','0x40000108',4,0x1FA0)]
 assert [(x['pc'],x['address'],x['size'],x['value']) for x in guest['writes']]==expected_writes
 observations.append(dict(name=name,input_bits=inp,result_bits=result_bits,native_controlled_status=f'{n[0]:08x}',guest_controlled_status=f'{g[0]:08x}',native_precision_bit=bool(n[0]&0x20),guest_precision_bit=bool(g[0]&0x20),status_equal=n[0]==g[0],result_equal=True,native_original_mxcsr=f'{n[1]:08x}',native_restored_mxcsr=f'{n[2]:08x}',mutated=c['mutated'],cleanup_verified=True))
assert observations[0]['status_equal'] and not observations[1]['status_equal'] and observations[2]['status_equal']
assert observations[1]['native_precision_bit'] and not observations[1]['guest_precision_bit']
for x in raw['tools']['providers']:assert sha(Path(x['path']).read_bytes())==x['sha256'] and Path(x['path']).stat().st_size==x['bytes']
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256']
result=dict(method=raw['method'],reference=ref,observations=observations,interpretation='For this original MULSS and next-above5 input under masked round-nearest1F80, nativehost and Unicorn agree on result41C80003 but native controlled status is1FA0 (bit5 set), guest1F80 (bit5 absent). Exact5 baseline and privateomit-MUL matchstatus1F80. Save/restore and output sentinel/cleanup controls pass. Demonstrated bounded backend precision-status limitation, not a general result-bit failure or live FF12 state claim. Unchanged emulator status cannot establish native absence of precision/exception effects.',affected_claims='55 raw next-radius after.mxcsr=1F80 is emulator-only; its original published README already disclaims native status/exception proof and finite return claims do not depend on status parity. RNG scaled-range producer checks control bits while explicitly excluding status/native exception semantics. Matrix and other status-dependent consumers require their actual claims/provider identities to be reviewed; no blanket retraction or parity certification. Preserve published inputs; additive control is the correction record.',limits=raw['limits'],cleanup=raw['cleanup'])
if (W/'result.json').exists():assert json.loads((W/'result.json').read_text())==result
else:(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if (W/'manifest.json').exists():
 for x in json.loads((W/'manifest.json').read_text())['members']:
  b=(W/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
print('PASS_STATUS_CONTROL57 nativeoriginal4B/Win64statewrapper/exact-inexact-NOP controls/source/guest paths+stores/MXCSRrestoration/free verified; native1FA0 vs guest1F80 for bounded inexact square, not live/fullFP parity')
