"""OV42: can shipped non-sentinel action +24 words alone narrow negative for ns8?
Retained-data first; cross-check each battle pack against its actual VBF entry.
No live execution or claim that every action takes the special loader.
python check-action-selectors.py FRESH_OUTPUT_DIR
"""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
OUT=pathlib.Path(sys.argv[1])
if OUT.exists():raise ValueError('immutable output exists')
vp=ROOT/'agent_flow/tools/vbfextract.py'
spec=importlib.util.spec_from_file_location('existing_vbfextract',vp)
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
archive=pathlib.Path(r'D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf')
retained=pathlib.Path(r'D:\FFXII_TZA_extract\ps2data\image\ff12\test_battle')
def sha(b):return hashlib.sha256(b).hexdigest()
def examine(blob):
    if len(blob)<0x40:raise ValueError('missing pack directory')
    t=struct.unpack_from('<I',blob,0x3c)[0]
    if t+16>len(blob) or blob[t:t+4]!=b'st2e':raise ValueError('wrong action descriptor')
    count,stride,rows=struct.unpack_from('<III',blob,t+4)
    if count!=543 or stride!=60:raise ValueError('different action-row corpus')
    end=t+rows+count*stride
    if rows<0x10 or end>len(blob):raise ValueError('invalid action row extent')
    values=[struct.unpack_from('<H',blob,t+rows+i*stride+0x24)[0] for i in range(count)]
    negatives=[dict(row=i,selector=v,narrowed=((4*v+1)&0xffff)-0x10000)
               for i,v in enumerate(values) if ((4*v+1)&0xffff)&0x8000]
    return dict(table_start=t,record_offset=rows,count=count,stride=stride,
                negatives=negatives,sentinel_rows=[i for i,v in enumerate(values) if v==0xffff],
                non_sentinel_negative_rows=[x for x in negatives if x['selector']!=0xffff],
                max_non_sentinel=max(v for v in values if v!=0xffff),
                has_flagged_values=any(v&0x8000 and v!=0xffff for v in values)),blob[t:end]

with archive.open('rb') as f:
    head=f.read(16); magic,hsize,nfiles=struct.unpack('<4sIQ',head)
    if magic!=b'SRYK' or not 16<hsize<0x10000000:raise ValueError('invalid archive header')
    f.seek(0); index=f.read(hsize)
    if len(index)!=hsize:raise ValueError('incomplete archive index')
    f.seek(0);names,blocks=V.load_index(f)
    paths=sorted(p for p in names if '/test_battle/' in p and p.endswith('/binaryfile/battle_pack.bin'))
    if len(paths)!=9:raise ValueError('missing battle-pack corpus, not empty proof')
    payload=[]; result=[]
    for path in paths:
        lang=path.split('/test_battle/')[1].split('/')[0]
        raw=(retained/lang/'binaryfile/battle_pack.bin').read_bytes()
        actual=V.read_entry(f,names,blocks,path)
        if actual!=raw:raise ValueError('retained input differs from actual archive entry')
        facts,table=examine(raw)
        result.append(dict(path=path,entry_metadata=names[path],pack_sha256=sha(raw),
                           table_sha256=sha(table),retained_equals_archive=True,**facts))
        payload.append((lang,table))
    # Missing descriptor/extent must reject at the actual analysis path.
    controls=[]
    for label,broken in [('missing',b''),('truncated_directory',raw[:0x3c]),
                         ('wrong_table_pointer',raw[:0x3c]+b'\xff'*4+raw[0x40:])]:
        try:examine(broken)
        except ValueError as e:controls.append(dict(case=label,rejected=True,reason=str(e)))
        else:raise ValueError('required input mutation passed')
    # A private change to one real table word must become a counterexample.
    altered=bytearray(raw); t=struct.unpack_from('<I',raw,0x3c)[0]
    rowoff=struct.unpack_from('<I',raw,t+12)[0]
    struct.pack_into('<H',altered,t+rowoff+0x24,0x2000)
    mutated,_=examine(altered)
    if not any(x['row']==0 and x['selector']==0x2000 for x in mutated['non_sentinel_negative_rows']):
        raise ValueError('detector missed concrete field counterexample')
    controls.append(dict(case='private_action_word_0x2000',rejected_invariant=True,
                         observed=mutated['non_sentinel_negative_rows'][0]))
    f.seek(0)
    if f.read(hsize)!=index:raise ValueError('archive index changed during read')
OUT.mkdir(); (OUT/'tables').mkdir()
for lang,table in payload:(OUT/'tables'/('action_data_'+lang+'.st2e')).write_bytes(table)
r=dict(method='A retained data + direct archive byte comparison + bounded row invariant',
       driver_sha256=sha(pathlib.Path(__file__).read_bytes()),extractor_sha256=sha(vp.read_bytes()),
       archive=str(archive),archive_bytes=archive.stat().st_size,archive_index_bytes=hsize,
       archive_index_sha256=sha(index),whole_archive_sha256='not computed; exact selected entry hashes retained',
       results=result,controls=controls,
       natural_special_loader_reachability='OPEN; sentinel admission and row/actor identity need caller proof')
(OUT/'result.json').write_text(json.dumps(r,indent=2)+'\n')
print('VALID exact nine-pack analysis; non-sentinel negative row counts',
      [len(x['non_sentinel_negative_rows']) for x in result],'; sentinel counts',[len(x['sentinel_rows']) for x in result])
