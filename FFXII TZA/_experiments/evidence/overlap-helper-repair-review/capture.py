import collections, contextlib, hashlib, importlib.util, io, itertools, json, os, shutil, subprocess, sys, traceback
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
R = W / 'run-02'
REPAIR = 'cdbf25a5d711654ccbb883f472309c3f42df290f'
BV_PATH = Path('Database/Tools/dashboard/build_views.py').resolve()
GS = Path('Database/Tools/analysis-kit/gfz-scripts').resolve()
EXE = Path('Database/Tools/work/exe/FFXII_TZA.exe').resolve()

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def dump(p, value):
    p.write_bytes((json.dumps(value, indent=2) + '\n').encode())

def git(*args):
    q = subprocess.run(['git', *args], capture_output=True)
    assert q.returncode == 0 and not q.stderr, (args, q.returncode, q.stderr)
    return q.stdout

def repair_source_matches(committed, checked_out):
    # Python text only; preserve both raw files/hashes. No binary normalization.
    return committed.replace(b'\r\n', b'\n') == checked_out.replace(b'\r\n', b'\n')

def sweep(pop, lo, n):
    events = collections.Counter({lo: 0, lo+n: 0})
    for a, z in pop.items():
        a, b = max(a, lo), min(a+z, lo+n)
        if a < b: events[a] += 1; events[b] -= 1
    depth = unique = extra = 0; last = lo
    for x, d in sorted(events.items()):
        if depth >= 2: unique += x-last; extra += (x-last)*(depth-1)
        depth += d; last = x
    assert depth == 0
    return unique, extra

def main():
    assert not R.exists(), 'Write-once capture: inspect failure rather than replay'
    R.mkdir()
    identity = {'repair': REPAIR, 'head': git('rev-parse', 'HEAD').decode().strip(), 'python': sys.executable, 'version': sys.version, 'driver_sha256': sha(Path(__file__)), 'sources': [], 'providers': [], 'limits': 'Original repository Python with labelled fixtures and only executable adapter enabled; no game code/live/full census/full build/deployment. Original helper path declared; drift control redirects only its input to disposable copy.'}
    for p in [BV_PATH, GS/'generation.py', GS/'uc1_band.py']:
        source = git('show', REPAIR+':'+p.relative_to(Path.cwd()).as_posix())
        current = p.read_bytes()
        assert repair_source_matches(source, current), 'Selected repair Python source changed beyond CRLF/LF'
        cp = R/'source'/p.name; cp.parent.mkdir(exist_ok=True); cp.write_bytes(current)
        committed = R/'committed-source'/p.name; committed.parent.mkdir(exist_ok=True); committed.write_bytes(source)
        assert not repair_source_matches(source, current.replace(b'import os', b'import io', 1)) if b'import os' in current else True
        identity['sources'].append({'path': str(p), 'copy': cp.relative_to(R).as_posix(), 'sha256': sha(cp), 'commit_copy': committed.relative_to(R).as_posix(), 'commit_sha256': sha(committed), 'only_CRLF_LF_equivalent': True})
    identity['preflight_correction'] = 'Run01 failed raw equality for helper before import/control; no semantic tests. Additive diagnostic proves only CRLF/LF difference. Both raw identities retained; Python-only comparison now permits that difference and rejects import-os-to-io mutation; actual loaded checked-out bytes bound unchanged.'
    prior = W.parent/'text-overlap-boundary/run-02'
    pi = json.loads((prior/'identity.json').read_bytes())
    for d in pi['reader_dependencies']:
        src = prior/d['copy']; assert sha(src) == d['sha256']
        target = R/d['copy']; target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, target)
        identity['providers'].append({'copy': target.relative_to(R).as_posix(), 'sha256': sha(target), 'provenance': 'Earlier text-overlap-boundary identity/run; no install'})
    identity['exe'] = {'path': str(EXE), 'sha256': sha(EXE), 'external': True, 'copied': False}
    assert identity['exe']['sha256'] == '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    dump(R/'pre-import-identity.json', identity)
    sys.path.insert(0, str((R/'python-deps').resolve()))
    spec = importlib.util.spec_from_file_location('astra_review_original_build_views', BV_PATH)
    BV = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV)
    import pefile, uc1_band
    assert Path(BV.G.__file__).resolve() == GS/'generation.py'
    assert Path(uc1_band.__file__).resolve() == GS/'uc1_band.py'
    assert Path(pefile.__file__).resolve() == R/'python-deps/pefile.py'
    identity['loaded'] = {'builder': BV.__file__, 'generation': BV.G.__file__, 'helper': uc1_band.__file__, 'pefile': pefile.__file__}
    dump(R/'identity.json', identity)
    pe = pefile.PE(str(EXE), fast_load=True)
    sec = next(s for s in pe.sections if s.Name.rstrip(b'\0') == b'.text')
    lo, n = pe.OPTIONAL_HEADER.ImageBase+sec.VirtualAddress, sec.Misc_VirtualSize; pe.close()
    cases = {'disjoint': {0: 12, 16: 8}, 'double': {0: 12, 4: 8}, 'triple': {0: 12, 4: 8, 8: 4}, 'clipped': {-8: 16, 4: 16, 32: 8, 50: 4}, 'three-real-extents': {0x32E020: 0x21, 0x32E030: 0x21, 0x32E040: 0x26}}
    observations = []
    for name, pop in cases.items():
        origin, size = (0x32E000, 128) if name == 'three-real-extents' else (0, 32)
        oracle = sweep(pop, origin, size)
        for order in itertools.permutations(pop):
            ordered = {a: pop[a] for a in order}
            cls, unique, extra = BV.population_cover(ordered, {order[-1]}, origin, size)
            row = {'case': name, 'order': list(order), 'origin': origin, 'size': size, 'pop': ordered, 'unique': unique, 'extra': extra, 'oracle': oracle, 'class_bytes': list(cls)}
            observations.append(row); dump(R/'population-controls.json', observations)
            assert (unique, extra) == oracle
    # Actual text_intervals -> v_executable, no substituted interval reader.
    for name, offsets in [('disjoint', {0:12,16:8}), ('double', {0:12,4:8}), ('triple', {0:12,4:8,8:4}), ('three-real-extents', cases['three-real-extents'])]:
        d = R/name; d.mkdir()
        pop = offsets if name == 'three-real-extents' else {lo+a:z for a,z in offsets.items()}
        f = d/'functions.tsv'; f.write_bytes(('entry\tname\tsize\n'+''.join('%08X\tCONTROL_%d\t%d\n'%(a,i,z) for i,(a,z) in enumerate(pop.items()))).encode())
        bands=[]
        for i in (1,2):
            p=d/('band%d.tsv'%i);p.write_bytes(b'kind\tstart\tend\n');bands.append(p)
        dims=d/'coverage_dims.md';dims.write_bytes(b'# ASTRA fixture; no coverage measure supplied\n')
        inputs={'functions':{'path':str(f.resolve())},'uc1_1_64':{'path':str(bands[0].resolve())},'uc1_65_256':{'path':str(bands[1].resolve())},'exe':{'path':str(EXE),'snapshot':False},'coverage_dims':{'path':str(dims.resolve())}}
        v=BV.v_executable({k:s['path'] for k,s in inputs.items()}, 'CONTROL_TIME')
        m=next(m for m in v['measures'] if m['id']=='bytes-overlap')
        expected=sweep(pop,lo,n);dump(d/'view.json',v);dump(d/'inputs.json',inputs)
        assert m['numerator']==expected[0] and ('%d additional covers'%expected[1]) in m['limits'] and 'each such byte once' in m['label']
        assert sum(m['numerator'] for m in v['measures'] if m['id'] in ['bytes-'+k for k in ['listed','frontier','funclet','held','fill','unknown']])==n
        if name=='triple': triple_inputs=inputs;triple_view=v
    decl=BV.declare_inputs(str((R/'capture').resolve()));dump(R/'declarations.json',decl)
    assert Path(decl['uc1_band.py']['path']).resolve()==Path(uc1_band.__file__).resolve()
    # Original build invocation; restrict ADAPTERS to real executable only.
    BV.ADAPTERS={'executable':BV.v_executable}
    inputs=dict(triple_inputs);inputs['uc1_band.py']=dict(decl['uc1_band.py']);inputs['build_views.py']={'path':str(BV_PATH)}
    st=BV.G.Store(str((R/'store').resolve()))
    logs=io.StringIO()
    with contextlib.redirect_stdout(logs):gid=BV._build(st,inputs,'CONTROL_TIME','UNUSED_BY_THIS_PATH')
    man,d,probs=st.open_current();assert not probs and man['generation']==gid
    v=json.loads((Path(d)/'outputs/view-executable.json').read_bytes());m=next(x for x in v['measures'] if x['id']=='bytes-overlap')
    assert v['definition']=='v2' and m['direction']=='down' and m['numerator']==8
    assert man['inputs']['uc1_band.py']['sha256']==sha(uc1_band.__file__)
    # A valid original v1 prior isolates definition-change behavior through _build.
    pdir=R/'v1-store';old=BV.G.Store(str(pdir.resolve()));b=old.begin(inputs,{'name':'labelled-v1-prior'})
    oldv=json.loads(json.dumps(v));oldv['definition']='v1'
    next(x for x in oldv['measures'] if x['id']=='bytes-overlap')['numerator']=12
    dump(Path(b.output_path('view-executable.json')),oldv);old.commit(b,['view-executable.json'])
    with contextlib.redirect_stdout(logs):newgid=BV._build(old,inputs,'CONTROL_TIME','UNUSED_BY_THIS_PATH')
    _,nd,probs=old.open_current();assert not probs
    newv=json.loads((Path(nd)/'outputs/view-executable.json').read_bytes());delta=next(x for x in newv['measures'] if x['id']=='bytes-overlap')['delta']
    dump(R/'definition-transition.json',{'current_view':newv,'raw_delta':delta,'labelled_prior_definition':'v1','current_generation':newgid})
    assert delta['na']=='N/A - definition changed' and 'pp' not in delta and delta['old']['numerator']==12 and delta['new']['numerator']==8
    with contextlib.redirect_stdout(logs):BV._build(old,inputs,'CONTROL_TIME','UNUSED_BY_THIS_PATH')
    _,nd,probs=old.open_current();assert not probs
    unchanged=json.loads((Path(nd)/'outputs/view-executable.json').read_bytes())
    same=next(x for x in unchanged['measures'] if x['id']=='bytes-overlap')['delta'];assert same['pp']==0
    dump(R/'same-version-control.json',same)
    h=R/'disposable-helper.py';shutil.copyfile(uc1_band.__file__,h)
    redirected=dict(inputs);redirected['uc1_band.py']={'path':str(h.resolve())}
    controls=[]
    for mode in ['same-size-mid-build-edit','missing-before-begin']:
        before={k:(Path(st.root)/k).read_bytes() for k in [BV.G.CURRENT,BV.G.HISTORY]}
        before_hash=sha(h) if h.exists() else None
        original=BV.v_executable
        if mode=='same-size-mid-build-edit':
            def mutate(inp,t):
                v=original(inp,t);payload=h.read_bytes();assert b'import os' in payload
                h.write_bytes(payload.replace(b'import os',b'import io',1));assert len(payload)==h.stat().st_size
                return v
            BV.ADAPTERS={'executable':mutate}
        else:
            redirected['uc1_band.py']={'path':str((R/'NOT_PRESENT.py').resolve())};BV.ADAPTERS={'executable':original}
        try:
            with contextlib.redirect_stdout(logs):BV._build(st,redirected,'CONTROL_TIME','UNUSED_BY_THIS_PATH')
            exception=None
        except BV.G.GenerationError as e:exception={'type':type(e).__name__,'message':str(e)}
        row={'case':mode,'exception':exception,'current_and_success_history_unchanged':all((Path(st.root)/k).read_bytes()==p for k,p in before.items()),'helper_before_sha256':before_hash,'helper_after_sha256':sha(h),'failure':json.loads((Path(st.root)/BV.G.FAILURE).read_bytes()),'terminal':True}
        controls.append(row);dump(R/'strict-helper-controls.json',controls)
        assert exception and 'uc1_band.py' in exception['message'] and row['current_and_success_history_unchanged']
    BV.ADAPTERS={'executable':BV.v_executable}
    for s in identity['sources']:assert sha(s['path'])==s['sha256']
    assert sha(EXE)==identity['exe']['sha256']
    (R/'build-stdout.txt').write_text(logs.getvalue())
    result={'verdict':'ACCEPT scoped overlap repair and helper declaration at exact cdbf25a5d', 'population_controls':len(observations), 'adapter_cases':4, 'unique_triple':8, 'extra_triple':12, 'three_real_unique':33, 'three_real_extra':34, 'definition_change_delta':delta, 'same_definition_delta':same, 'helper_declared_at_actual_imported_path':True, 'strict_helper_controls':controls, 'original_sources_unchanged':True, 'limits':identity['limits']+' Not every display/deployed module, source-before-import, third-party bindings, all views, whole A05/A23/M3 or L1L2.'}
    dump(R/'result.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':
    try:main()
    except BaseException:
        if R.exists():(R/'failure.txt').write_text(traceback.format_exc())
        raise
