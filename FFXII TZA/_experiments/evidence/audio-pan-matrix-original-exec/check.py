"""Validate retained execution receipts; --replay optionally executes original code again."""
import argparse,copy,hashlib,json,math,struct
from pathlib import Path
import run
E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

def validate(raw):
    expected=run.cases();rows=raw['rows'];assert len(rows)==len(expected)==23
    assert [r['case'] for r in rows]==expected
    by_id={r['case']['id']:r for r in rows};assert len(by_id)==len(rows)
    for row in rows:
        assert row['valid'] and row['reached_return'] and not row['errors']
        assert row['stack_restored'] and row['nonvolatile_restored'] and row['canaries_intact']
        assert row['mutation'] is None and row['return_value']==0 and row['writes']
        assert 0<row['instructions']==len(row['trace'])<row['budget']
        assert row['trace'][0]=='007B8430' and row['trace'][-1]=='007B8B96'
        assert row['calls'].count('00808C40')==1
        final=bytearray(b'\xA5'*8)
        for write in row['writes']:
            pos=int(write['address'],16)-run.OUT;n=write['size'];assert 0<=pos and pos+n<=8
            final[pos:pos+n]=int(write['value']).to_bytes(n,'little')
        assert [f'{x:08X}' for x in struct.unpack('<2I',final)]==row['gain_bits']
        assert list(struct.unpack('<2f',final))==row['gains']
        assert all(math.isfinite(x) for x in row['gains'])
    gains=lambda key:by_id[key]['gains']
    assert abs(gains('mono-front-center')[0]-gains('mono-front-center')[1])<1e-6
    assert gains('mono-output1-control')[1]>.99 and abs(gains('mono-output1-control')[0])<1e-6
    assert gains('mono-output0-control')[0]>.99 and abs(gains('mono-output0-control')[1])<1e-6
    assert gains('mono-at-listener-control')==[.5,.5]
    assert gains('mono-udpan-control')==gains('mono-front-center')
    for n in [215,240,250]:assert gains(f'mono-byte-{n}')[1]>gains(f'mono-byte-{n}')[0]
    assert gains('mono-byte-240-mirror-input')[0]>gains('mono-byte-240-mirror-input')[1]
    assert gains('mono-byte-127')[1]>.99 and gains('mono-byte-128')[0]>.99
    for ch in (0,1):
        assert gains(f'stereo-byte-240-spread--1-ch-{ch}')==gains(f'stereo-byte-240-spread-0-ch-{ch}')
        assert gains(f'stereo-byte-240-spread-1-ch-{ch}')==gains('mono-byte-240')
        assert gains(f'stereo-byte-240-spread-2-ch-{ch}')==gains(f'stereo-byte-240-spread-0-ch-{1-ch}')
    stereo=[gains(f'stereo-byte-240-spread-0-ch-{ch}') for ch in (0,1)]
    assert stereo[0][1]>stereo[0][0] and stereo[1][0]>stereo[1][1]
    equal_input_outputs=[sum(row[i] for row in stereo) for i in (0,1)]
    assert abs(equal_input_outputs[0]-equal_input_outputs[1])<2e-6
    controls=raw['controls'];assert len(controls)==2
    exhausted,mutated=controls
    assert exhausted['budget']==1 and not exhausted['valid'] and not exhausted['reached_return']
    assert mutated['mutation']=='suppress-rear-half-turn' and mutated['valid']
    assert mutated['gains'][0]>mutated['gains'][1] # contradicts the observed original side
    return dict(mono_byte_240=gains('mono-byte-240'),mirror_input=gains('mono-byte-240-mirror-input'),
                stereo_spread_zero=stereo,equal_stereo_input_linear_mix=equal_input_outputs,
                stereo_spread_one=[gains(f'stereo-byte-240-spread-1-ch-{i}') for i in (0,1)],
                interpretation='Numeric output coefficients only. Equal stereo-input mixing is a calculation from measured rows, not rendered audio.',
                controls='Mono center/axes and listener-origin positives; source-order/spread discriminators; incomplete run rejected; mutated half-turn changes side.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--write-summary',action='store_true');p.add_argument('--replay',action='store_true');a=p.parse_args()
    raw=json.loads((E/'full.json').read_text());im=run.Image(run.R/'Database/Tools/work/exe/FFXII_TZA.exe');current=run.provenance(im)
    for k in ('executable_sha256','image_base','bodies','entry_abi'):assert current[k]==raw['identity'][k],k
    pre=json.loads((E/'pre-full.json').read_text());assert pre['harness_sha256']==sha((E/'run.py').read_bytes())
    assert pre['feasibility_sha256']==sha((E/'feasibility.json').read_bytes())
    feasibility=json.loads((E/'feasibility.json').read_text());assert feasibility['rows']==raw['rows'][:3]
    for row in raw['rows']+raw['controls']:
        for read in row['image_reads']:assert im.read(int(read['address'],16),read['size']).hex()==read['raw']
    result=validate(raw)
    # Receipt faults are introduced only into disposable reducer inputs, not raw evidence.
    malformed=[]
    for name,edit in [('empty',lambda x:x.update(rows=[])),('missing_return',lambda x:x['rows'][0].update(reached_return=False)),('wrong_source_population',lambda x:x['rows'][0]['case'].update(sources=2)),('wrong_channel_bits',lambda x:x['rows'][1]['gain_bits'].reverse()),('missing_output_write',lambda x:x['rows'][0].update(writes=[]))]:
        fixture=copy.deepcopy(raw);edit(fixture)
        try:validate(fixture)
        except (AssertionError,KeyError,ValueError):malformed.append(name)
        else:raise AssertionError('Malformed receipt passed: '+name)
    result['rejected_malformed_receipts']=malformed
    if a.replay:
        for old in raw['rows']:
            new=run.execute(im,old['case']);assert new==old,old['case']['id']
        print('Fresh original-code replay matches all retained normal rows; no game process.')
    if a.write_summary:
        with (E/'normalized.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    else:assert result==json.loads((E/'normalized.json').read_text())
    print('Retained original-code rows, raw writes, original read bytes, ABI restoration, controls and falsification verified. No audible/live claim.')
if __name__=='__main__':main()
