"""Independent selected-record review of EXP-085; no Unicorn or game execution."""
from __future__ import annotations
import copy
import json
from pathlib import Path

EXE_SHA = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
# Predictions derived from the original lifecycle state machine, not its stored pass booleans.
EXPECTED = {
    'p0-run': (['B','P'],1,1,0),
    'p1-run': (['P'],1,1,0),
    'p1-done': (['P','R'],0,0,1),
    'p2-entry': (['R'],0,0,1),
    'p5-entry': (['R'],0,0,1),
    'p0-nopoll': (['B','R'],0,0,1),
    'p0-nobegin': (['P','R'],0,0,1),
    'p0-noresult': (['B','P'],0,0,1),
    'stack-63': (['B','P','R'],0,0,63),
    'stack-62': (['B','P','R'],0,0,63),
    'p0-poll-0x100': (['B','P','R'],0,0,1),
    'p0-poll-3': (['B','P'],1,1,0),
    'begin-eax-ignored': (['B','P'],1,1,0),
    'id-zero': ([],0,0,1),
}

def review(obj: dict) -> dict:
    if obj.get('exe_sha256') != EXE_SHA:
        raise ValueError('wrong original image identity')
    cases = obj.get('cases', [])
    if len(cases) != 35 or len({c.get('name') for c in cases}) != len(cases):
        raise ValueError('changed/duplicate retained population')
    by_name = {c['name']:c for c in cases}
    verified=[]
    for name, (order,eax,phase,depth) in EXPECTED.items():
        row=by_name.get(name)
        if not row or (row.get('order'),row.get('eax'),row.get('phase'),row.get('depth')) != (order,eax,phase,depth):
            raise ValueError('retained lifecycle disagreement: '+name)
        if row.get('fault') is not None or row.get('failures'):
            raise ValueError('retained fault: '+name)
        verified.append(name)
    return {'record_count':len(cases),'selected_consistency_checks':len(verified),'verified':verified,
            'limits':['Checks recorded order/return/phase/depth, not callback semantics or raw game health.',
                      'Original producer/mutant campaign is not rerun; remaining records preserved but not independently accepted here.',
                      'Stored pass booleans and summary counts are not the basis of these checks.']}

def run(database: Path, output: Path) -> dict:
    p=database/'_experiments/evidence/verb-lifecycle-execution/result.json'
    obj=json.loads(p.read_text(encoding='utf-8'))
    result=review(obj)
    corruptions=[]
    specs=[('phase1_rebegins','p1-run','order',['B','P']),('full_stack_overflow','stack-63','depth',64),
           ('completion_stays_running','p1-done','phase',1),('high_poll_byte_treated_busy','p0-poll-0x100','eax',1),
           ('missing_callback_no_default','p0-noresult','depth',0),('empty_id_fabricated_callback','id-zero','order',['R'])]
    for label,name,key,value in specs:
        altered=copy.deepcopy(obj);next(r for r in altered['cases'] if r['name']==name)[key]=value
        try: review(altered)
        except ValueError as exc:corruptions.append({'name':label,'rejected':True,'reason':str(exc)})
        else:raise AssertionError('corrupted record accepted: '+label)
    for label,edit in [('duplicate_case',lambda d:d['cases'].append(copy.deepcopy(d['cases'][0]))),
                       ('wrong_image',lambda d:d.update(exe_sha256='0'*64))]:
        altered=copy.deepcopy(obj);edit(altered)
        try:review(altered)
        except ValueError as exc:corruptions.append({'name':label,'rejected':True,'reason':str(exc)})
        else:raise AssertionError(label)
    (output/'retained_review.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'retained_negative_controls.json').write_text(json.dumps(corruptions,indent=2)+'\n')
    return {'selected_checks':len(EXPECTED),'corruptions_rejected':len(corruptions)}
