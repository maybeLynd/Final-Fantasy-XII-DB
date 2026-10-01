"""A: one reference-cell file-backing witness, not a loader or running-game observation."""
import datetime,hashlib,importlib.util,json,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,detail=team.board_status(team.BOARD);assert ok,detail
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-REFERENCE-BASE-FILE-BACKING-CONTROL')
assert t['status']=='ACTIVE' and t['agent']=='ASTRA' and not (W/'result.json').exists()
rp=Path('Database/FFXII TZA/_experiments/evidence/license-check-exec/check.py')
assert sha(rp.read_bytes())=='4dfa511d2b92c41473e88dd535f900ac9bdc0c34f7c51ec54807652ac0f30e32'
sp=importlib.util.spec_from_file_location('reader',rp);rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd);image,ss=rd.load_image()
assert sha(image)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
review=Path('Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-CKPT10R2-EXECUTED.md');review_bytes=review.read_bytes()
assert 'Cell contents `90 FB 05 00` nonzero' in review_bytes.decode()
pe=struct.unpack_from('<I',image,0x3C)[0];nsec=struct.unpack_from('<H',image,pe+6)[0];optsz=struct.unpack_from('<H',image,pe+20)[0]
assert struct.unpack_from('<H',image,pe+24)[0]==0x20B
base=struct.unpack_from('<Q',image,pe+24+24)[0];assert base==0x120000
table_offset=pe+24+optsz;section_bytes=image[table_offset:table_offset+nsec*40]
sections=[]
for j in range(nsec):
    p=table_offset+j*40;vs,va,rs,ra=struct.unpack_from('<IIII',image,p+8)
    sections.append(dict(name=image[p:p+8].rstrip(b'\0').decode(),header_file_offset=hex(p),virtual_size=vs,rva=va,raw_size=rs,raw_offset=ra))
target=0x1F83530;rva=target-base
sec=next(s for s in sections if s['rva']<=rva and rva+8<=s['rva']+s['virtual_size'])
assert sec['name']=='.data' and sec['virtual_size']==0x11A7530 and sec['rva']==0x1CD0000 and sec['raw_size']==0x18E400 and sec['raw_offset']==0x1CCE600
raw_end=base+sec['rva']+sec['raw_size'];assert raw_end==0x1F7E400 and target>=raw_end
virtual_end=base+sec['rva']+sec['virtual_size'];assert virtual_end==0x2F97530
positive=[]
for label,a,n in [('one-constant',0x1CEBBA8,4),('encoder-source',0x20E620,9),('last-backed-eight',raw_end-8,8)]:
    data=rd.img_rd(image,ss,a,n)
    assert len(data)==n
    positive.append(dict(label=label,va=hex(a),bytes=n,raw_hex=data.hex(),sha256=sha(data),method='Actual existing guarded shipping-reader file read'))
assert positive[0]['raw_hex']=='0000803f'
old_encode=Path('Database/FFXII TZA/_experiments/evidence/image-reference-roundtrip-domain/retained/encode.bin').read_bytes()
assert bytes.fromhex(positive[1]['raw_hex'])==old_encode==bytes.fromhex('2b0d0a4fd7018bc1c3')
negative=[]
for label,a,n in [('base-dword',target,4),('base-qword',target,8),('first-unbacked',raw_end,8),('straddle-backed-end',raw_end-4,8)]:
    try:rd.img_rd(image,ss,a,n)
    except KeyError as e:negative.append(dict(label=label,va=hex(a),bytes=n,rejected=True,error=str(e),method='Actual existing guarded shipping-reader refusal, not observed zero bytes'))
    else:raise AssertionError((label,'unbacked read accepted'))
# Labelled unsafe formula control: deliberately ignores SizeOfRawData. Not SPEC's identified producer.
file_offset=sec['raw_offset']+rva-sec['rva'];assert file_offset==0x1E61B30
candidate=image[file_offset:file_offset+8];assert candidate.hex()=='90fb0500bafb0500'
owner=next(s for s in sections if s['raw_offset']<=file_offset and file_offset+8<=s['raw_offset']+s['raw_size'])
owner_va=base+owner['rva']+file_offset-owner['raw_offset']
assert owner_va!=target and rd.img_rd(image,ss,owner_va,8)==candidate
R=W/'retained';R.mkdir(exist_ok=False)
for name,data in [('section-table.bin',section_bytes),('shipping-reader.py',rp.read_bytes()),('unchecked-candidate.bin',candidate),('codec-encode.bin',old_encode),('review-preimage.md',review_bytes)]:
    (R/name).write_bytes(data)
(R/'image-header-identity.json').write_text(json.dumps(dict(pe_file_offset=pe,number_of_sections=nsec,optional_header_bytes=optsz,optional_magic='020B',preferred_base=hex(base),table_file_offset=table_offset,section_table_sha256=sha(section_bytes)),indent=2)+'\n')
prior=Path('Database/FFXII TZA/_experiments/evidence/image-reference-roundtrip-domain/retained/encoded-id-contract.md')
(R/'known-base-contract.md').write_bytes(prior.read_bytes())
spec=dict(source='https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers',section='Section Table: VirtualSize/SizeOfRawData/PointerToRawData',paraphrase='A virtual region extending beyond initialized bytes is zero-filled during image mapping. Raw offsets apply to the serialized bytes, not arbitrary addresses throughout VirtualSize.',limits='Source image mapping rule, not observation after loader callbacks/game initialization/writes')
result=dict(question='Provenance of SPEC42 nonzero-cell bytes: valid raw cell read versus injection/live versus unbacked raw-offset alias',method='A originalPEsection/header and existingguarded-reader positive/negative controls; zero original/native/emulator/live execution',
    reference=dict(exe_sha256=sha(image),reader_sha256=sha(rp.read_bytes()),preferred_base=hex(base),target=hex(target),target_bytes=8,raw_end=hex(raw_end),virtual_end=hex(virtual_end),target_section=sec,section_table_sha256=sha(section_bytes)),tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes())),driver_sha256=sha(Path(__file__).read_bytes()),spec=spec,sections=sections,positive=positive,negative=negative,
    unsafe_formula_control=dict(formula='raw_offset + (targetVA - preferred_base - sectionRVA), checked only against VirtualSize',file_offset=hex(file_offset),candidate_hex=candidate.hex(),quoted_low4_match=True,actual_file_owner_section=owner,actual_owner_va=hex(owner_va),owner_guarded_read_matches=True,limits='Deliberately unsafe host address calculation, NOT demonstrated actual SPEC invocation or runtime cell value'),
    consumer=dict(path=review.as_posix(),sha256=sha(review_bytes),retained='review-preimage.md',quoted='Cell contents90FB0500 nonzero',needed='Identify actual input/producer/mapping method or explicit injected/live provenance; preserve original plus additive correction, repair demonstrated producer/procedure and inventory only its dependent claims'),
    interpretation='01F83530 is within virtual.data but outside serializedrawbytes. A file-backed nonzero-cell sample cannot be read there through valid original file mapping. Existingguardedreader correctlyrefuses4/8B; knownloadzero finding reused. Deliberatelyuncheckedformula reproducesquotedlow4 atfileoff1E61B30, bytesbelongelsewhere. This demonstratesafailurehypothesis notactualcause/SPECpath. Independentcodecmodularproof42 valid; no nativebaseorprocess-lifetimezero inferred.',
    limits='No new discovery of priorBSSloadzero/writer census, no newloader/classifier/index regeneration, no actualSPECproduceridentity or defect inventory yet, no injectedmemory or livesample, processvalue/initpostcallbacks/lifetime/basewriters unknown. Quotedreviewprovenance must be corrected/labelled byowner; do not retract unrelatedacceptedsource/domain/control evidence.',
    cleanup='Read-only certifiedimage/retainedconsumer/source/context; no game/input/process/instrument/save/config/reference/peerwrites. FF12 process inventory returnednone; PC OFF, S19spentunapproved/DBGOALNOT_MET. Owneractualpath/provenance repair and independent acceptance pending.')
(W/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('Confirmed unbackedbase cell/guardpositive-negative and matchingunsafe-filealias; actualSPECproducer/cause unassigned, not livecell evidence',flush=True)
