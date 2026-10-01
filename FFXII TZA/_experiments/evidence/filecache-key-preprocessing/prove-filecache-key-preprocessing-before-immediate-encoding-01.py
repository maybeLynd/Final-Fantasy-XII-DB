"""Exact source/CFG proof; C-ASCII illustrations are neither native nor live."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ESHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def normal_ascii(path):
    """Interpret the proved loops under an explicit C-ASCII toupper premise."""
    if not path or len(path) >= 256 or any(x >= 128 or x == 0 for x in path):
        raise ValueError('illustration outside nonempty bounded ASCII domain')
    k = next((i for i,c in enumerate(path) if (0x61<=c<=0x7a or
                                              0x30<=c<=0x39 or 0x41<=c<=0x5a)),len(path))
    value = path[k:].replace(b'/',b'\\')
    while b'\\\\' in value:
        value = value.replace(b'\\\\',b'\\')
    return bytes(c-32 if 97<=c<=122 else c for c in value).rstrip(b' ')


def original_hash_recurrence(value):
    h = 0x1505
    for c in value:
        h = (h*33 + (c if c < 128 else c-256)) & 0xffffffff
    return h & 0x7fffffff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs',type=Path,default=W)
    ap.add_argument('--out',type=Path,required=True)
    args = ap.parse_args(); src = args.inputs
    if args.out.exists():
        raise ValueError('immutable result exists')
    # Original statuses are prerequisites, including the older physical-only capture.
    for prefix,driver in [('filecache-key-boundaries-capture-01','capture-filecache-key-boundaries-before-normalizer-closure-01.py'),
                          ('filecache-key-boundaries-capture-02','capture-filecache-key-boundaries.py')]:
        s=json.loads((src/(prefix+'.status.json')).read_text())
        if s.get('exit')!=0 or s.get('terminal') is not True or s.get('driver_sha256')!=sha(src/driver):
            raise ValueError('required upstream capture failed/stale: '+prefix)
        if not (src/(prefix+'.stdout')).read_bytes().strip() or (src/(prefix+'.stderr')).read_bytes():
            raise ValueError('required upstream output missing/error: '+prefix)
    old=json.loads((src/'filecache-key-boundaries-source-01.json').read_text())
    full=json.loads((src/'filecache-key-boundaries-source-02.json').read_text())
    h=json.loads((src/'filecache-hash-loop-source-01.json').read_text())
    hs=json.loads((src/'filecache-hash-loop-capture-01.status.json').read_text())
    if hs.get('exit')!=0 or not (src/'filecache-hash-loop-capture-01.stdout').read_bytes().strip() or (src/'filecache-hash-loop-capture-01.stderr').read_bytes():
        raise ValueError('retained hash capture failed/missing')
    if h.get('driver_sha256')!=sha(src/'capture-index-path.py') or h.get('invocation_driver_sha256')!=sha(src/'capture-filecache-hash-loop.py'):
        raise ValueError('retained actual capture invocation changed')
    for z in [old,full,h]:
        if z.get('exe_sha256')!=ESHA:
            raise ValueError('wrong original executable identity')
        load('key_reviewed_roles',src/'validate-title-source-annotations.py').validate(z)
    if sha(src/'prove_owner_reload_order.py')!='43263d8faec92292904c9508ef9148cbc3a33248e7fc96b489b08e9b3615e864':
        raise ValueError('reviewed CFG helper changed')
    G=load('key_original_cfg',src/'prove_owner_reload_order.py')
    ranges={int(q['start'],16):q for z in [old,full,h] for q in z['ranges']}
    norm=ranges[0x20c440]
    if int(norm['end_exclusive'],16)!=0x20c551:
        raise ValueError('normalizer semantic boundary incomplete')
    ix={int(i['pc'],16):i for q in ranges.values() for i in q['instructions']}
    graphs={}
    for lo in [0x20c440,0x20be50,0x20c1b0,0x1d6b40,0x1d6d20,0x674a00]:
        q=ranges[lo]
        g=G.graph(ix,lo,int(q['end_exclusive'],16))
        graphs[hex(lo)]={'visited':sorted(g['visited']),'calls':g['calls'],'returns':g['returns']}
    pins={0x20c497:'49b8ff03e0ffff070000',0x20c4a6:'761d',0x20c4b8:'720b',
          0x20c4c8:'488bf9',0x20c4f4:'0fbec8',0x20bf02:'e839050000',
          0x20c213:'e828020000',0x1d6b54:'e8f7520300',0x1d6d55:'e856540300',
          0x674a10:'6bc021',0x674a17:'0fbed2',0x674a23:'0fbaf01f'}
    # Pins are checked from actual captured bytes, never a patched model input.
    for pc,body in pins.items():
        if ix[pc]['bytes']!=body:
            raise ValueError('required original instruction pin mismatch: '+hex(pc))
    literals=full.get('prefix_literals',[])
    expected=[(0x905ec0,b'/hostapp/'),(0x905ecc,b'/app0/'),(0x905ed4,b'/host/')]
    if len(literals)!=3 or [(int(x['va'],16),bytes.fromhex(x['bytes'])) for x in literals]!=[(a,b+b'\0') for a,b in expected]:
        raise ValueError('exact original prefix literal prerequisite failed')
    imports=json.loads((src/'filecache-import-declarations-01.json').read_text())
    if (imports.get('complete') is not True or imports.get('exe_sha256')!=ESHA or
        {x['iat_va']:x['name'] for x in imports['imports']}!={'0x8c2ff0':'toupper','0x8c2ff8':'strncmp'}):
        raise ValueError('exact static import declarations missing')
    classified=[]
    for c in range(256):
        d=(c-0x30)&255
        stop=((c-0x61)&255)<=25 or (d<=42 and ((0x7fffffe03ff>>d)&1)!=0)
        expected_stop=(97<=c<=122 or 48<=c<=57 or 65<=c<=90)
        if stop!=expected_stop:
            raise ValueError('original byte classifier equivalence failed')
        classified.append({'byte':c,'stops_leading_scan':bool(stop)})
    paths=[b'PS2Data/sample.phyre',b'/hostapp/PS2Data/sample.phyre',
           b'/app0/PS2Data/sample.phyre',b'/host/PS2Data/sample.phyre',
           b'/HOSTAPP/PS2Data/sample.phyre',b'C:\\sample.phyre',
           b'.\\C:\\sample.phyre']
    examples=[]
    for value in paths:
        prefix=next((p for _,p in expected if value.startswith(p)),b'')
        gate_input=value[len(prefix):]
        gate_key=normal_ascii(gate_input);direct_key=normal_ascii(value)
        examples.append({'input_ascii':value.decode('ascii'),'gate_stripped_prefix':prefix.decode('ascii'),
                         'gate_normalizer_input':gate_input.decode('ascii'),
                         'direct_normalizer_input':value.decode('ascii'),
                         'gate_key_C_ASCII':gate_key.decode('ascii'),'direct_key_C_ASCII':direct_key.decode('ascii'),
                         'gate_hash_C_ASCII':original_hash_recurrence(gate_key),
                         'direct_hash_C_ASCII':original_hash_recurrence(direct_key),
                         'key_equal':gate_key==direct_key})
    if [x['key_equal'] for x in examples]!=[True,False,False,False,True,True,True]:
        raise ValueError('prefix distinguishing controls failed')
    if not all(x['direct_key_C_ASCII'].startswith('C:') for x in examples[-2:]):
        raise ValueError('drive-prefix countermodel failed')
    result={'method':'A verified original source/CFG and explicitly conditional C-ASCII integer illustrations',
            'producer_complete':True,'driver_sha256':sha(Path(__file__)),
            'source_pins':{name:sha(src/name) for name in ['filecache-key-boundaries-source-01.json',
                 'filecache-key-boundaries-source-02.json','filecache-hash-loop-source-01.json',
                 'filecache-import-declarations-01.json']},
            'graphs':graphs,'first_byte_classification':classified,'illustrations':examples,
            'claims':['Leading scanner stops at ASCII drive letter, so generic drive-prefix removal is not established',
                      'Gate0020BE50 strips three exact prefixes; direct lookup0020C1B0 does not',
                      'Prefix comparison import is strncmp; case-insensitive comparison hypothesis rejected',
                      'Same key-function call does not guarantee same key for every raw path'],
            'limits':'No native/game/CRT execution, cache population, archive collision census, natural issue/eviction or whole E2 closure. Values assume nonaliasing valid bounded ASCII inputs, normal named external contracts/C-ASCII toupper. Static IAT names are not loaded targets/locale proof.'}
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'producer_complete':True,'claims':len(result['claims']),'byte_classes':256,
                      'illustrations':7,'native_game_runs':0}))


if __name__=='__main__': main()
