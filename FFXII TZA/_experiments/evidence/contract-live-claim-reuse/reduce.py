"""Reuse captured live bytes; no new live game or save write."""
import ast, copy, hashlib, importlib.util, json, struct, zlib
import capstone
from pathlib import Path
HERE=Path(__file__).resolve().parent
CAP=HERE.parent/'old-save-start-p'
sha=lambda b:hashlib.sha256(b).hexdigest()
# Original getters establish the coordinate frame, separately from observed
# containment and the existing descriptor semantics.
exe=(HERE.parents[4]/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
assert sha(exe)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',exe,0x3c)[0];opt=pe+24
base=struct.unpack_from('<Q',exe,opt+24)[0];assert base==0x120000
table=opt+struct.unpack_from('<H',exe,pe+20)[0]
sections=[struct.unpack_from('<IIII',exe,table+i*40+8) for i in range(struct.unpack_from('<H',exe,pe+6)[0])]
def image_read(va,n):
    for _,rva,size,offset in sections:
        if rva<=va-base and va-base+n<=rva+size:return exe[offset+va-base-rva:offset+va-base-rva+n]
    raise AssertionError('missing original span')
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
getters=[]
for va,n,expected in [(0x2EF640,8,'488d05394ce701c3'),(0x2EF2B0,20,'4883ec28e8870300004805000200004883c428c3')]:
    body=image_read(va,n);assert body.hex()==expected
    ins=list(md.disasm(body,va));assert sum(i.size for i in ins)==n
    getters.append(dict(address=hex(va),bytes=n,raw=body.hex(),sha256=sha(body),
                        instructions=[dict(address=hex(i.address),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]))
assert 0x2EF647+struct.unpack_from('<i',image_read(0x2EF643,4))[0]==0x2164280
spec=importlib.util.spec_from_file_location('prior_save_check',HERE/'sources/old-save-check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=CAP
decoder=HERE/'sources/save_container_roundtrip.py'
names={'rotl','rc4','key_for','unwrap'}
nodes=[n for n in ast.parse(decoder.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert {n.name for n in nodes}==names
ns=dict(hashlib=hashlib,struct=struct,zlib=zlib,TITLE=b'FINAL FANTASY XII THE ZODIAC AGE')
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(decoder),'exec'),ns)
raw=(CAP/'inputs/old-FFXII_004.bin').read_bytes()
assert sha(raw)=='8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc'
decoded=ns['unwrap'](raw);plain=decoded['plain']
assert len(plain)==0x4E690 and sha(plain)=='9d7314c38ed17619f7abb84ce0e084bbe2cbbca2a9e2dfb040012ff3b06eba38'
legacy=plain[0x2200:0x8200]
regions={'goods_flags':(0x59C8,128),'loot_sold_counters':(0x57C8,512)}
rows=[];inputs={}
for label,n in m.STATES.items():
    p=CAP/(label+'-memory.json');inputs[p.name]=sha(p.read_bytes())
    receipt=json.loads(p.read_text());values=m.memory(receipt,n)
    for index,d in enumerate(values):
        b=d['bound_battle_block'];im=d['active_save_image']
        B=struct.unpack_from('<Q',d['registry_before'],0x70)[0]
        assert B==0x2164280+0x4E68C==0x2164480+0x4E48C
        assert len(im)-0x200==0x56490
        for name,(offset,length) in regions.items():
            payload_offset=0x4E48C+offset;image_offset=0x200+payload_offset
            assert 0<=payload_offset<payload_offset+length<=len(im)-0x200
            span=b[offset:offset+length];saved=legacy[offset:offset+length]
            assert len(span)==length and span==im[image_offset:image_offset+length]
            nz=[(i,v) for i,v in enumerate(span) if v]
            if label.startswith('old-after'):
                assert span==saved and nz
            else:assert not nz and span!=saved
            rows.append(dict(label=label,sample=index,region=name,length=length,
                             battle_offset=hex(offset),payload_offset=hex(payload_offset),
                             image_offset=hex(image_offset),address=hex(B+offset),
                             bytes=span.hex(),sha256=sha(span),nonzero=nz,
                             matches_saved_old=span==saved))
failed=m.load('old-after-current-field-memory.json')
bad=copy.deepcopy(failed['samples'][0]);bad['registry_stable']=True
assert m.reject('invalid-transitional-sample',lambda:m.sample(bad,23))
assert len(rows)==16 and all(len(r['nonzero'])==18 for r in rows if r['region']=='goods_flags' and r['label'].startswith('old-after'))
health=m.load('health.json');cleanup=m.load('cleanup.json')
assert health['fatal_dialog_observed'] is False and health['responsive_menu_and_return'] is True
assert cleanup['status']=='RESTORED' and cleanup['backup_unchanged'] and cleanup['processes']==[]
assert cleanup['files']==m.load('save-before.json')['files'] and len(cleanup['files'])==26
assert m.load('reference-after.json')['sha256']==m.EXE and m.load('reference-after.json')['pc_control_reset']
out=dict(status='BOUNDED_CAPTURE_REUSE_PENDING_CANONICAL_CONSUMPTION',method='A reduction of retained C observations',
         source_commit='8e5c8d4520fa1602aa634a6d28c1e6bb57c6a9ac',source_pid=34844,
         executable_sha256=m.EXE,image_base='0x120000',save_image_base='0x2164280',
         save_image_size='0x56690',payload_base='0x2164480',payload_size='0x56490',battle_base='0x21B290C',
         captured_inputs=inputs,getters=getters,decoded_input_sha256=sha(raw),decoded_plaintext_sha256=sha(plain),
         source_checks={'identity_and_raw_binding_brackets':True,'positive_known_read_and_null_rejection':True,
                        'invalid_transitional_sample_rejected':True,'healthy_responsive_session':True,
                        'restored26files_reference_and_pc_off':True},samples=rows,
         limits=['Sequential, not atomic; existing capture independent review is pending.',
                 'No new sale, bazaar purchase, save operation or on-disk roundtrip was observed.',
                 'Load endpoints do not locate/order transient clearing, rebasing, copy or import writers.',
                 'Old-save modification history is unknown; values are not portable defaults.',
                 'No observation of bazaar menu availability/name mapping; region semantics use cited original-code work.'])
(HERE/'bazaar-observation.json').write_text(json.dumps(out,indent=2)+'\n')
print('8accepted live samples: all128 goods flags and512 sold-counter bytes contained in the captured live image.')
print('Old samples exactly match old-file decoded fields; nonzero counts:',{r['region']:len(r['nonzero']) for r in rows if r['label']=='old-after-current-field-settled' and r['sample']==0})
print('Payload extent56490; invalid transitional sample excluded; live cleanup receipt retained; save-write persistence OPEN.')
