"""Question: does native bit30 admission exclude all FFFF action selectors?
Source + exact retained table fields, with concrete input/claim controls.
python check-special-admission.py RAW_JSON ACTION_RESULT_JSON TABLE_DIR NEW_RESULT
"""
import hashlib,json,pathlib,struct,sys
rawpath,receiptpath,tabledir,out=map(pathlib.Path,sys.argv[1:])
if out.exists():raise ValueError('immutable result exists')
raw=json.loads(rawpath.read_text()); receipts=json.loads(receiptpath.read_text())
ins={int(x['pc'],16):x for r in raw['ranges'] for x in r['instructions']}
expected={0x30ce93:('test','dword ptr [rax + 0xc], 0x40000000'),
          0x30ce9a:('je','0x30cf31'),0x30cf0d:('call','0x306bd0'),
          0x306c4d:('call','0x309230'),0x306c52:('mov','edx, eax'),
          0x306c56:('call','0x32fc30'),0x3092c5:('movzx','eax, word ptr [rbx + 0x24]'),
          0x3092c3:('je','0x3092cb'),0x3092b4:('imul','ecx, edx, 0x113'),
          0x30cec2:('cmp','eax, 0xd0'),0x30ceeb:('cmp','eax, 0xf1')}
if raw['exe_sha256']!='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':raise ValueError('wrong image')
for pc,value in expected.items():
    if (ins[pc]['mnemonic'],ins[pc]['args'])!=value:raise ValueError('code witness mismatch')
if len(raw['controls'])!=3 or any(c['observed']!=c['expected'] for c in raw['controls']):raise ValueError('upstream roles invalid')
if len(receipts['results'])!=9:raise ValueError('missing pack receipt')
def classify(blob):
    if blob[:4]!=b'st2e' or len(blob)<16:raise ValueError('wrong descriptor')
    count,stride,offset=struct.unpack_from('<III',blob,4)
    if count!=543 or stride!=60 or offset+count*stride>len(blob):raise ValueError('incomplete table')
    neg_non_sentinel=[];sentinel_bit30=[]
    for i in range(count):
        selector=struct.unpack_from('<H',blob,offset+i*stride+36)[0]
        flags=struct.unpack_from('<I',blob,offset+i*stride+12)[0]
        if selector!=65535 and ((4*selector+1)&65535)&32768:neg_non_sentinel.append(i)
        if selector==65535 and flags&0x40000000 and i!=0x113:sentinel_bit30.append(i)
    return dict(non_sentinel_negative=neg_non_sentinel,sentinel_with_bit30_ordinary=sentinel_bit30)
results=[]
for rec in receipts['results']:
    lang=rec['path'].split('/test_battle/')[1].split('/')[0]
    p=tabledir/('action_data_'+lang+'.st2e');blob=p.read_bytes()
    if hashlib.sha256(blob).hexdigest()!=rec['table_sha256']:raise ValueError('table changed')
    results.append(dict(language=lang,table_sha256=rec['table_sha256'],**classify(blob)))
if not results or any(r['non_sentinel_negative'] for r in results):raise ValueError('non-sentinel invariant false')
# Claim is specifically the local bit30 predicate, not the whole caller CFG.
controls=[]
last=bytearray(blob);offset=struct.unpack_from('<I',last,12)[0]
struct.pack_into('<H',last,offset+36,0x2000)
if 0 not in classify(last)['non_sentinel_negative']:raise ValueError('negative word detector failed')
controls.append(dict(case='private_row0_selector2000',detected=True))
clear=bytearray(blob)
for i in range(543):
    flags=struct.unpack_from('<I',clear,offset+i*60+12)[0]
    struct.pack_into('<I',clear,offset+i*60+12,flags&~0x40000000)
if classify(clear)['sentinel_with_bit30_ordinary']:raise ValueError('flag-clear discriminator failed')
controls.append(dict(case='private_clear_bit30',removed_all_candidates=True))
try:classify(blob[:-1])
except ValueError:controls.append(dict(case='truncated_table',rejected=True))
else:raise ValueError('truncated input passed')
r=dict(method='A original code + complete nine-pack field predicate',
       raw_sha256=hashlib.sha256(rawpath.read_bytes()).hexdigest(),
       action_receipt_sha256=hashlib.sha256(receiptpath.read_bytes()).hexdigest(),
       driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
       results=results,controls=controls,
       hypothesis_result='REFUTED: bit30 admission alone excludes sentinel selectors',
       consequence='All non-sentinel action words safe under ns8 narrowing; ordinary rows511..534 remain candidates, not natural execution witnesses',
       next_discriminator='command/action eligibility of shipped rows511..534 before30CE10; then metadata/load success and remaining script/field selectors',
       limits='row113 uses type-derived table and needs valid actor type; initialized row/codec/ABI/immutable data premises; no original execution or natural reachability')
out.write_text(json.dumps(r,indent=2)+'\n')
print('VALID non-sentinel invariant; local bit30-only exclusion REFUTED; candidate rows',results[0]['sentinel_with_bit30_ordinary'])
