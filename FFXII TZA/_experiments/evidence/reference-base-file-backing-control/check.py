"""Readonly original file-backing/guard checks, not loader or live process execution."""
import hashlib,importlib.util,json,struct
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((W/'result.json').read_text());ref=r['reference']
assert sha((W/'capture.py').read_bytes())==r['driver_sha256']
assert sha((R/'shipping-reader.py').read_bytes())==ref['reader_sha256']=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('retained_reader',R/'shipping-reader.py');rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd)
image,ss=rd.load_image();assert sha(image)==ref['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
h=json.loads((R/'image-header-identity.json').read_text());table=(R/'section-table.bin').read_bytes()
assert sha(table)==h['section_table_sha256']==ref['section_table_sha256'] and len(table)==h['number_of_sections']*40 and image[h['table_file_offset']:h['table_file_offset']+len(table)]==table
sections=[]
for j in range(h['number_of_sections']):
    p=j*40;vs,va,rs,ra=struct.unpack_from('<IIII',table,p+8)
    sections.append(dict(name=table[p:p+8].rstrip(b'\0').decode(),header_file_offset=hex(h['table_file_offset']+p),virtual_size=vs,rva=va,raw_size=rs,raw_offset=ra))
assert sections==r['sections']
b=int(ref['preferred_base'],16);target=int(ref['target'],16);s=ref['target_section'];delta=target-b-s['rva']
assert b==0x120000 and target==0x1F83530 and s in sections and s['name']=='.data'
assert s['raw_size']<=delta and delta+8<=s['virtual_size'] and b+s['rva']+s['raw_size']==int(ref['raw_end'],16)==0x1F7E400
assert b+s['rva']+s['virtual_size']==int(ref['virtual_end'],16)==0x2F97530
assert len(r['positive'])==3 and len(r['negative'])==4
for c in r['positive']:
    data=rd.img_rd(image,ss,int(c['va'],16),c['bytes']);assert data.hex()==c['raw_hex'] and sha(data)==c['sha256']
for c in r['negative']:
    assert c['rejected']
    try:rd.img_rd(image,ss,int(c['va'],16),c['bytes'])
    except KeyError as e:assert str(e)==c['error']
    else:raise AssertionError('Unbacked/straddle read accepted')
u=r['unsafe_formula_control'];fo=s['raw_offset']+delta
assert fo==int(u['file_offset'],16)==0x1E61B30
candidate=(R/'unchecked-candidate.bin').read_bytes()
assert image[fo:fo+8]==candidate==bytes.fromhex('90fb0500bafb0500') and candidate.hex()==u['candidate_hex']
owner=u['actual_file_owner_section'];assert owner in sections and owner['raw_offset']<=fo and fo+8<=owner['raw_offset']+owner['raw_size']
v=b+owner['rva']+fo-owner['raw_offset'];assert v==int(u['actual_owner_va'],16)!=target and rd.img_rd(image,ss,v,8)==candidate
assert (R/'codec-encode.bin').read_bytes().hex()=='2b0d0a4fd7018bc1c3'
assert sha((R/'review-preimage.md').read_bytes())==r['consumer']['sha256'] and 'Cell contents `90 FB 05 00` nonzero' in (R/'review-preimage.md').read_text()
assert 'zero at image load' in (R/'known-base-contract.md').read_text() and 'supported, not proven' in (R/'known-base-contract.md').read_text()
assert r['spec']['source']=='https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers'
if (W/'manifest.json').exists():
    m=json.loads((W/'manifest.json').read_text())['members'];assert m
    for x in m:
        d=(W/x['path']).read_bytes();assert len(d)==x['bytes'] and sha(d)==x['sha256']
print('PASS_FILE_BACKING_CONTROL certifiedPE/raw-virtualboundaries/positive-and-negative-existingreader/filealias-owner/provenancelimits; no actualSPECproducer/cause or livebase proof')
