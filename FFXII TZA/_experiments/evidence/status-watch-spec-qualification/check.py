import hashlib,json
from pathlib import Path
import capstone
HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 s=json.loads((HERE/'primary.json').read_text());assert s['exe_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
 a=s['aligned_prefix'];raw=bytes.fromhex(a['raw_hex']);assert len(raw)==a['size'] and sha(raw)==a['sha256']
 assert int(a['start'],16)==int(a['containing_runtime_function']['begin'],16) and int(a['end'],16)<int(a['containing_runtime_function']['end'],16)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);ii=list(cs.disasm(raw,int(a['start'],16)))
 selected=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ii if i.address>=0x31E1B4];assert selected==s['selected_instructions']
 known=next(i for i in ii if i.address==0x31E241);assert known.bytes.hex()=='0fb64513' and known.size==4 and known.op_str=='eax, byte ptr [rbp + 0x13]'
 assert next(i for i in ii if i.address==0x31E245).op_str=='byte ptr [rbx + 0x23], al'
 for p in s['refs']:
  b=(HERE/p['retained']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
 assert sha((HERE/'documentation.json').read_bytes())==s['documentation_sha256']
 assert sha((HERE/'retained'/'image-reader.py').read_bytes())==s['reader_sha256']
 prep=(HERE/'retained'/'00-status-sparse-slot-watch-preparation.md').read_text()
 assert 'A hit at RIP `0031E241`' in prep and 'A hit there would mean the detector or the' in prep
 observer=json.loads((HERE/'retained'/'02-observer.json').read_text());assert 'RW = 00 (execute), LEN = 00' in observer['set_slots_source']
 table=(HERE/'retained'/'03-status-table.bin').read_bytes();assert len(table)==1312
 desired={0x11,0x12,*range(0x14,0x20)};windows=[(0x11,1),(0x12,2),(0x14,4),(0x18,8)]
 union=set().union(*(set(range(a,a+n)) for a,n in windows));assert union==set(range(0x11,0x20)) and union-desired=={0x13}
 doom=table[32+6*40:32+7*40];assert int.from_bytes(doom[:2],'little')==0x2806 and all(doom[x]==255 for x in desired)
 # Prospective criterion counterexamples, NOT native events or original FF12 executions.
 def decision(kind,off,width):
  overlap=set(range(off,off+width))&desired
  return 'SPARSE_READ' if kind=='read' and overlap else 'WRITE' if kind=='write' else 'NEIGHBOUR_ONLY'
 witnesses=[{'name':'known-positive','access_pc':'0x31e241','raw_after_access_pc':'0x31e245','kind':'read','offset':0x13,'width':1,
  'result':'POSITIVE_CONTROL_ONLY','reason':'Original known source byte is neighbouring13, outside desired14 bytes; raw context/source PC are different.'},
  {'name':'other-source-only13','kind':'read','offset':0x13,'width':1,'result':decision('read',0x13,1)},
  {'name':'rw-write-not-reader','kind':'write','offset':0x14,'width':1,'result':decision('write',0x14,1)},
  {'name':'empty-doom-value-does-not-invalidate-read','kind':'read','offset':0x14,'width':1,'sampled_byte':doom[0x14],'result':decision('read',0x14,1)}]
 assert witnesses[1]['result']=='NEIGHBOUR_ONLY' and witnesses[2]['result']=='WRITE' and witnesses[3]['result']=='SPARSE_READ'
 out={'original_positive':{'access_pc':hex(known.address),'instruction_bytes':known.bytes.hex(),'width':1,'raw_after_access_pc':hex(known.address+known.size)},
 'watch_union_bytes':sorted(union),'actual_sparse_bytes':sorted(desired),'extra_neighbour':hex(0x13),
 'required_qualification':['Define raw context RIP versus recovered/normalized access PC; native known-load control must relate241 to raw245 for this nonbranching MOVZX.',
  'RW events need opcode/access-kind/effective-address/width and actual overlap with desired span before naming a sparse reader; another13-only access is not one.',
  'AllFF Doom contents do not prove absence of legitimate access. A hit requires diagnosis, not automatic wrong-detector/row verdict.',
  'Watched-window width is not access width; after-access memory is not automatically consumed value. Branch/string data traps need qualified source recovery.'],
 'synthetic_criterion_witnesses':witnesses,
 'live_acceptance':'NOT QUALIFIED: mandatory native data-read detector/positive/coverage controls, exact save/action/removal, fresh binding and healthy bounded restoration remain unprovided. No live test started.',
 'preserved':'Corrected Stop3/Float26/Doom6 resource identity, unchanged prior42 census and cycle-only no-hit limits; no new sparse meaning or actual Doom reader asserted.',
 'limits':s['limits'],'owner_status':'Pending OPUS qualification/independent review'}
 (HERE/'observation.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'validation.json').write_text(json.dumps({'status':'PASS_STATIC_ONLY','class':'Original known-read/overlap and prospective criterion witnesses, no native detector or live qualification','accepted_live_runs':0},indent=2)+'\n')
 print('PASS_STATIC_ONLY source/read-PC and watch predicates; no native data detector or live cycle qualified.')
if __name__=='__main__':main()
