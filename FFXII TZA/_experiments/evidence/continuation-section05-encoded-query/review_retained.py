#!/usr/bin/env python3
"""Independently check EXP-143's retained observations; does not rerun its emulator."""
from __future__ import annotations
import argparse, copy, hashlib, json, struct
from pathlib import Path

def require(ok: bool, message: str) -> None:
    if not ok: raise ValueError(message)

def raw_at(image: bytes, address: int, length: int) -> bytes:
    pe=struct.unpack_from('<I',image,0x3c)[0];opt=pe+24
    require(image[pe:pe+4]==b'PE\0\0','PE signature')
    base=struct.unpack_from('<Q',image,opt+24)[0]
    nsec=struct.unpack_from('<H',image,pe+6)[0];sh=opt+struct.unpack_from('<H',image,pe+20)[0]
    for i in range(nsec):
        _,va,size,off=struct.unpack_from('<IIII',image,sh+40*i+8)
        rva=address-base
        if va<=rva and rva+length<=va+size:return image[off+rva-va:off+rva-va+length]
    raise ValueError(f'Unbacked range {address:x}+{length:x}')

def signed(n: int) -> int:
    n &= 0xffffffff
    return n if n<0x80000000 else n-0x100000000

def audit(data: dict, image: bytes) -> dict:
    jt=[hex(0x120000+x) for x in struct.unpack('<32I',raw_at(image,0x323054,128))]
    require(data['jtab']==jt,'jump-table mismatch')
    r=data['results'];require(set(r)=={str(x) for x in range(1,33)}|{'edge'},'class population')
    require(data['summary']=={'cases':173,'failures':[],'faults':[]},'producer summary differs')
    observed=0
    def probe(p, arms, low, high1, subclasses):
        nonlocal observed
        require('fault' not in p,'faulted record')
        obs=p['obs'];require(obs['arm']==arms,'wrong arm trace');require(obs['sub']==subclasses,'wrong subclass trace')
        expected_tail=[] if low is None else [{'low':low,'high1':high1}]
        require(obs['tail']==expected_tail,'wrong observed bounds')
        want=0 if low is None else int(signed(low)<=signed(int(p['id'],0))<=signed(high1-1))
        require(p['v']==want,'return disagrees with original signed-inclusive tail')
        observed+=1
    def bounds(c,count=64):
        if c==19:return 0xe000,0xeffe
        if c==22:return 0,3
        if c==23:return 0,8
        low=(c-5)*0x1000 if 6<=c<=18 else 0xa000 if c in (30,31) else 0
        return low,low+count-1
    for c in range(2,33):
        rec=r[str(c)];lo,hi=bounds(c,26 if c==13 else 64)
        require(rec['bounds']==[lo,hi] and rec['arm']==jt[c-1],'record bounds/arm')
        ps=rec['probes'];require([int(p['id'],0) for p in ps]==[lo-1,lo,hi,hi+1,-1],'boundary inputs')
        for p in ps:probe(p,[jt[c-1]],lo,hi+1,[])
        if c not in (19,22,23):
            require(rec['count']==(26 if c==13 else 64),'fixture count')
            probe(rec['unplanted'],[jt[c-1]],lo,lo,[])
    require(r['13']['partial']=={'sum':23,'v_at_hi':1,'v_at_hi1':0},'partial descriptor sum')
    registry=raw_at(image,0x1eebcc0,15*0x58)
    mapping={format(n,'X'):struct.unpack_from('<I',registry,n*0x58+0x38)[0] for n in range(15)}
    require(r['1']['mapper_table']==mapping,'registry class mapping')
    cases=r['1']['cases'];require(len(cases)==18,'class1 groups')
    require([c['nibble'] for c in cases]==[format(i,'X') for i in range(15)]+['F-nibble','hi-id','neg'],'class1 group identities')
    for k,case in enumerate(cases):
        if k<15:
            lo,hi=bounds(k+5,256 if k==8 else 64)
            require(case['sub']==k+5 and case['bounds']==[lo,hi],'class1 group bounds')
            require([int(x['id'],0) for x in case['probes']]==[lo-1,lo,hi,hi+1],'class1 boundary inputs')
        else:
            require(len(case['probes'])==1,'class1 edge count')
        for p in case['probes']:
            n=(int(p['id'],0)&0xffff)>>12
            if n==15:probe(p,[jt[0]],None,None,[0xffffffff])
            else:
                c=mapping[format(n,'X')];lo,hi=bounds(c,256 if c==13 else 64)
                probe(p,[jt[0],jt[c-1]],lo,hi+1,[c])
    require(r['edge']=={'cls0':{'v':0},'cls33':{'v':0}},'out-of-domain outcomes')
    require(observed==246,'observation population')
    return {'status':'CONSISTENT_RETAINED_RECORDS','traced_probe_records':observed,'additional_untraced_summary_returns':4,
            'producer_mixed_container_counter':173,'all_validator_classes_represented':32,'jump_entries_verified':32,'registry_class_words_verified':15,
            'class19_last_valid':'0xEFFE','class13_missing_one_descriptor_sum':23,
            'limits':['Replay of retained records, not a new emulator execution or live session.','173 is the producer\'s mixed outer-container counter, not the number of individual probe records.','All-class validator evidence does not establish query outputs or shipped-state reachability.']}

def negative_controls(data: dict,image: bytes) -> list[dict]:
    variants=[]
    def add(name,fn):
        d=copy.deepcopy(data);fn(d)
        try:audit(d,image)
        except (ValueError,KeyError,TypeError,IndexError) as e: variants.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise AssertionError(f'Accepted corrupt record: {name}')
    add('wrong_return',lambda d:d['results']['19']['probes'][3].update(v=1))
    add('wrong_tail',lambda d:d['results']['6']['probes'][1]['obs']['tail'][0].update(high1=4161))
    add('missing_class',lambda d:d['results'].pop('12'))
    add('jump_table_changed',lambda d:d['jtab'].__setitem__(11,d['jtab'][1]))
    add('wrong_class_word',lambda d:d['results']['1']['mapper_table'].__setitem__('E',18))
    add('missing_null_descriptor_probe',lambda d:d['results']['2'].pop('unplanted'))
    add('duplicated_boundary',lambda d:d['results']['6']['probes'].__setitem__(4,copy.deepcopy(d['results']['6']['probes'][0])))
    add('wrong_partial_sum',lambda d:d['results']['13']['partial'].update(sum=26))
    return variants

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--exe',type=Path,required=True);a.add_argument('--retained',type=Path,required=True);a.add_argument('--output',type=Path,required=True);n=a.parse_args()
    b=n.exe.read_bytes();require(hashlib.sha256(b).hexdigest()=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8','wrong EXE')
    d=json.loads(n.retained.read_text());out={'review':audit(d,b),'negative_controls':negative_controls(d,b)}
    require(not n.output.exists(),'output already exists');n.output.write_text(json.dumps(out,indent=2)+'\n')
