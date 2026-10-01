"""Finite source/coverage qualification. PASS is not live status semantics."""
import ast,copy,hashlib,json,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
SLOTS=[0x11,0x12,*range(0x14,0x20)]
def reduce(raw,directory,meta):
    assert len(directory)==68 and struct.unpack_from('<I',directory,0x40)[0]==meta['table_file_offset']
    assert len(raw)==1312 and raw[:4]==b'st2e'
    assert struct.unpack_from('<I',raw,4)[0]==32
    assert struct.unpack_from('<H',raw,8)[0]==40
    assert struct.unpack_from('<I',raw,12)[0]==32
    rows=[raw[32+40*i:32+40*(i+1)] for i in range(32)]
    assert all(struct.unpack_from('<H',r)[0]==0x2800+i for i,r in enumerate(rows))
    assert rows[6][9]==100 and rows[2][9]==45 and rows[8][9]==120
    assert struct.unpack_from('<I',rows[3],12)[0]==1<<17
    assert struct.unpack_from('<I',rows[31],12)[0]==0x7FFFFFFC
    sparse=[{'id':i,'offset':s,'value':r[s]} for i,r in enumerate(rows) for s in SLOTS if r[s]!=255]
    assert len(sparse)==42 and all(25<=s['value']<=31 for s in sparse)
    return {'rows':32,'stride':40,'sparse_slots':SLOTS,'positions':448,'non_ff':42,
            'sparse_values':sparse,'name_keys':[hex(struct.unpack_from('<H',r)[0]) for r in rows],
            'controls':'32 complete two-byte name keys; Doom/Petrify/Poison beat values and Stop/X-Zone clear masks'}
def coverage(observation,status,start,width):
    assert 0<=status<32 and width>0 and start>=0 and start+width<=40
    populated=[x['offset'] for x in observation['sparse_values'] if x['id']==status]
    covered=[x for x in populated if start<=x<start+width]
    return {'status_id':status,'start':start,'byte_width':width,'populated_offsets':populated,
            'covered_populated_offsets':covered,'missed_populated_offsets':[x for x in populated if x not in covered],
            'unknown_slots_not_covered':[x for x in SLOTS if not start<=x<start+width],
            'limits':'Pure byte-interval coverage, not hardware watchpoint encoding/alignment qualification.'}
def require_full(observation,status,start,width):
    c=coverage(observation,status,start,width)
    assert c['populated_offsets'] and not c['missed_populated_offsets']
    return c
def main():
    raw=(HERE/'status-table.bin').read_bytes();directory=(HERE/'directory.bin').read_bytes()
    meta=json.loads((HERE/'source.json').read_text())
    assert sha(raw)==meta['table_sha256'] and sha(directory)==meta['directory_sha256']
    observation=reduce(raw,directory,meta)
    fn=json.loads((HERE/'observer.json').read_text())
    tree=ast.parse(fn['set_slots_source'])
    assert len(tree.body)==1 and isinstance(tree.body[0],ast.FunctionDef) and tree.body[0].name=='set_slots'
    # Source statement qualifies current capability, not successful real thread programming.
    assigns=[n for n in ast.walk(tree) if isinstance(n,ast.Assign)]
    assert any(any(isinstance(t,ast.Name) and t.id=='dr7' for t in n.targets) and isinstance(n.value,ast.Constant) and n.value.value==0 for n in assigns)
    writes=[n for n in ast.walk(tree) if isinstance(n,ast.AugAssign) and isinstance(n.target,ast.Name) and n.target.id=='dr7']
    assert len(writes)==1 and ast.unparse(writes[0])=='dr7 |= 1 << i * 2'
    assert any(any(isinstance(t,ast.Attribute) and t.attr=='Dr7' for t in n.targets) and isinstance(n.value,ast.Name) and n.value.id=='dr7' for n in assigns)
    observation['observer']={'capability':'set_slots programs execute conditions only; no data read watch control',
      'whole_source_sha256':fn['whole_source_sha256'],'set_slots_sha256':sha(fn['set_slots_source'].encode()),
      'limits':'Static source qualification; no live SetThreadContext success or read-detection qualification.'}
    observation['coverage']=[coverage(observation,i,0x14,w) for i in (3,6,14,26) for w in (1,4,8)]
    observation['result']='PREPARATION_CORRECTION; NO_LIVE_RESULT'
    observation['claim_limit']='No read seen in one qualified cycle could bound that cycle only; it cannot certify authored-dead/unread universally.'
    (HERE/'observation.json').write_text(json.dumps(observation,indent=2)+'\n')
    tests=[]
    def reject(name,f):
        try:f()
        except (AssertionError,struct.error):tests.append({'name':name,'rejected':True})
        else:raise AssertionError('undetected corruption: '+name)
    def changed(off,data):
        b=bytearray(raw);b[off:off+len(data)]=data;return bytes(b)
    d=bytearray(directory);struct.pack_into('<I',d,0x40,meta['table_file_offset']+4)
    reject('wrong directory target',lambda:reduce(raw,bytes(d),meta))
    reject('wrong count',lambda:reduce(changed(4,struct.pack('<I',31)),directory,meta))
    reject('wrong stride',lambda:reduce(changed(8,struct.pack('<H',39)),directory,meta))
    reject('truncated final row',lambda:reduce(raw[:-1],directory,meta))
    reject('row3 name-key low byte changed to6',lambda:reduce(changed(32+3*40,b'\x06'),directory,meta))
    reject('row3 name-key high byte changed; low-byte join alone accepts',lambda:reduce(changed(32+3*40+1,b'\x29'),directory,meta))
    reject('empty watch budget',lambda:coverage(observation,3,0x14,0))
    reject('Doom row6 proposed populated control',lambda:require_full(observation,6,0x14,8))
    reject('Stop row3 single8B misses1C',lambda:require_full(observation,3,0x14,8))
    assert require_full(observation,3,0x11,15)['covered_populated_offsets']==[0x16,0x17,0x1c]
    receipt={'result':'PASS_PREPARATION_ONLY','cases':len(tests),'controls':tests,
      'positive':'Full15B byte-interval covers all three row3 populated slots; not a hardware watch specification.',
      'semantic_live_closure':[], 'observed_game_process':False}
    (HERE/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS',len(tests),'rejecting controls; row3=3 populated, row6=0; +14 single8B misses1C; NO LIVE RESULT')
if __name__=='__main__':main()
