"""Mandatory shipping-byte/annotation gate before accepted legacy reduction.

Usage: SOURCE_DIRECTORY FRESH_RESULT. Repair independent acceptance pending.
No native execution, class census, initialized-array or lifetime certification.
"""
import hashlib, importlib.util, json, pathlib, subprocess, sys
W = pathlib.Path(__file__).resolve().parent
ROOT = next((p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/disasm_fn.py').is_file()), None)
if ROOT is None:raise ValueError('reference repository unavailable')
KIT = ROOT/'Database/Tools/analysis-kit/gfz-scripts'
SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
IMAGE_SHA = '0c5207a9392df6bea7e193aaaab3066fd6e9f58fb4bebce919cba543d80e0efa'
LEGACY_SHA = '672a2358f6ec16839466cb45058fbf0051438e67470b7e4d3de44ea3f0cffd18'
SOURCES = ['softedges-elements-callback-source-01/original-code.json', 'softedges-member-assignment-code-01.json',
           'softedges-member-resolution-code-01.json', 'softedges-member-resolution-continuation-code-01.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def qualify_sources(source,names):
    source=pathlib.Path(source).resolve()
    if not names or len(set(names))!=len(names):raise ValueError('missing/duplicate required source set')
    if sha(KIT/'disasm_fn.py')!=IMAGE_SHA:raise ValueError('reference reader changed')
    sys.path.insert(0,str(KIT));from disasm_fn import Image
    image=Image(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe')
    if hashlib.sha256(image.d).hexdigest()!=SHA or image.base!=0x120000:raise ValueError('wrong reference image')
    s=importlib.util.spec_from_file_location('required_annotations',W/'validate-title-source-annotations.py')
    A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
    checks=[]
    for name in names:
        p=source/name;v=json.loads(p.read_text())
        if v.get('exe_sha256')!=SHA or v.get('wrapper_complete') is not True:raise ValueError('unchecked source '+name)
        agreement=A.validate(v);ranges=[]
        for q in v['ranges']:
            a,b=int(q['start'],16),int(q['end_exclusive'],16)
            # The existing reader bounds the start. Bound the whole range in a
            # raw section before invoking it; no read across section/padding.
            if not any(image.base+va<=a<b<=image.base+va+rs for sn,va,vs,ro,rs in image.secs):raise ValueError('whole source span not raw backed')
            original=image.read(a,b-a);recorded=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))
            if original is None or len(original)!=b-a or original!=recorded:raise ValueError('source differs from shipping bytes at '+q['start'])
            ranges.append(dict(start=q['start'],end_exclusive=q['end_exclusive'],original_sha256=hashlib.sha256(original).hexdigest()))
        checks.append(dict(path=name,source_sha256=sha(p),annotations=agreement,shipping_ranges=ranges))
    if len(checks)!=len(names) or not all(q['shipping_ranges'] for q in checks):raise ValueError('missing/zero prerequisites')
    return checks
def main():
    if len(sys.argv)!=3:raise ValueError('source and fresh result required')
    source,out=pathlib.Path(sys.argv[1]).resolve(),pathlib.Path(sys.argv[2])
    legacy_out=pathlib.Path(str(out)+'.legacy-result.json');receipt=pathlib.Path(str(out)+'.upstream-status.json')
    if any(p.exists() for p in [out,legacy_out,receipt]):raise ValueError('immutable prior output exists')
    checks=qualify_sources(source,SOURCES)
    legacy=W/'check-softedges-member-boundaries-legacy-02.py'
    if sha(legacy)!=LEGACY_SHA:raise ValueError('accepted legacy reducer changed')
    argv=[sys.executable,str(legacy),str(source),str(legacy_out)]
    r=subprocess.run(argv,capture_output=True,timeout=45,cwd=ROOT)
    for suffix,z in [('.upstream.stdout',r.stdout),('.upstream.stderr',r.stderr)]:
        with pathlib.Path(str(out)+suffix).open('xb') as f:f.write(z)
    write_new(receipt,dict(argv=argv,exit=r.returncode,legacy_sha256=LEGACY_SHA))
    if r.returncode:raise RuntimeError('required upstream reduction failed; no final result')
    v=json.loads(legacy_out.read_text())
    if v.get('producer_complete') is not True or len(v.get('established',[]))!=3:raise ValueError('missing/incomplete/zero upstream result')
    if any(sha(source/q['path'])!=q['source_sha256'] for q in checks):raise ValueError('source moved across checked reduction')
    v.update(checker_sha256=sha(pathlib.Path(__file__)),entrypoint_sha256=sha(W/'check-softedges-member-boundaries.py'),
             accepted_legacy_checker_sha256=LEGACY_SHA,source_qualification=checks,image_tool_sha256=IMAGE_SHA,
             image_tool_dependencies={'kit_paths.py':sha(KIT/'kit_paths.py')},annotation_validator_sha256=sha(W/'validate-title-source-annotations.py'),
             qualification_status='PRODUCER_REPAIR_CHECKED_INDEPENDENT_PENDING',
             limits=v['limits']+' All source ranges now match shipping file bytes and decoded operations/memory roles before required reduction. No new native/live, initialized state or independent acceptance.')
    write_new(out,v)
    print('Shipping-byte/annotation prerequisites passed; independently accepted three bounded claims unchanged')
if __name__=='__main__':main()
