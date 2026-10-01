"""Reduce retained selected VBF blocks; no archive access or execution."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib

E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()


def decode(raw,expected):
    if len(raw)==expected:return raw
    d=zlib.decompressobj();out=d.decompress(raw,expected+1)
    assert d.eof and not d.unused_data and not d.unconsumed_tail
    assert len(out)==expected
    return out


def header(data,size,path):
    assert len(data)>=0x60 and data[:4]==b'sabf'
    assert data[4]==2 and data[8]==4
    assert struct.unpack_from('<I',data,12)[0]==size
    name=data[16:16+data[9]].decode('ascii')
    assert data[16+data[9]]==0 and path.rsplit('/',1)[1].startswith(name)
    directory=((16+data[9])&0xf0)+struct.unpack_from('<H',data,6)[0]
    chunks=[struct.unpack_from('<4sIII',data,directory+i*16) for i in range(4)]
    assert [c[0] for c in chunks]==[b'snd ',b'seq ',b'trk ',b'mtrl']
    assert all(c[1]==0x100000 and directory+64<=c[2]<=size and c[3]==0 for c in chunks)
    assert all(b[2]>a[2] for a,b in zip(chunks,chunks[1:]))
    return dict(bank_name=name,word_0a=struct.unpack_from('<H',data,10)[0],directory=directory,
                chunks=[dict(tag=c[0].decode(),offset=c[2],trailing_word_0c=c[3]) for c in chunks])


def rejected(label,fn):
    try:fn()
    except (AssertionError,ValueError,zlib.error,struct.error):return label
    raise AssertionError('invalid control accepted: '+label)


def collect():
    c=json.loads((E/'capture.json').read_text())
    assert c['status']=='BOUNDED_AUTHORED_OBSERVATIONS' and 'error' not in c
    assert c['source_sha256']==sha((E/'capture.py').read_bytes())
    assert c['index_reader_sha256']==sha((E/'index-reader.py').read_bytes())
    assert c['executable_sha256']=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
    assert c['before']==c['after'] and len(c['entries'])==len(c['paths'])==3
    index=c['archive_index'];magic,length,count=struct.unpack('<4sIQ',bytes.fromhex(index['prefix_hex']))
    assert magic==b'SRYK' and length==index['header_size'] and count==index['entry_count']
    entry_base=16+count*16;string_base=entry_base+count*32
    string_size=struct.unpack('<I',bytes.fromhex(index['string_size_hex']))[0]
    assert string_size==index['string_size'] and index['block_base']==string_base+string_size
    rows=[];controls=[]
    for i,e in enumerate(c['entries']):
        assert e['path']==c['paths'][i] and 0<=e['index']<count
        sb,sb2,size,offset,noff=struct.unpack('<IIQQQ',bytes.fromhex(e['record_hex']))
        assert e['record_offset']==entry_base+32*e['index']
        assert e['name_offset_in_archive']==string_base+4+noff
        assert bytes.fromhex(e['name_hex'])==e['path'].encode()+b'\0'
        assert e['block_size_offset']==index['block_base']+sb*2
        assert e['block_size_offset']+2<=length
        csize=struct.unpack('<H',bytes.fromhex(e['block_size_hex']))[0] or 65536
        assert csize==e['compressed_size'] and offset==e['block_offset'] and size==e['entry_size']
        assert length<=offset and offset+csize<=c['before']['size']
        raw=(E/e['raw_file']).read_bytes();decoded=(E/e['decoded_file']).read_bytes()
        assert len(raw)==csize and sha(raw)==e['raw_sha256']
        assert decode(raw,min(size,65536))==decoded
        assert sha(decoded)==e['decoded_sha256'] and len(decoded)==e['decoded_size']
        assert decoded[:16].hex()==e['header_hex']
        h=header(decoded,size,e['path'])
        assert h['bank_name']==e['bank_name'] and h['word_0a']==e['param_word']
        rows.append(dict(path=e['path'],entry_size=size,header=h,raw_sha256=e['raw_sha256'],
                         matches_value_one=h['word_0a']==1))
        if i==0:
            controls.append(rejected('truncated compressed block rejected',lambda:decode(raw[:-1],65536)))
            bad=bytearray(decoded);bad[0]^=1
            controls.append(rejected('wrong magic rejected',lambda:header(bad,size,e['path'])))
            controls.append(rejected('wrong logical size rejected',lambda:header(decoded,size+1,e['path'])))
            changed=bytearray(decoded);struct.pack_into('<H',changed,10,0)
            assert h['word_0a']==1 and header(changed,size,e['path'])['word_0a']==0
            controls.append('labelled value-one to zero mutation changes discriminator without inventing shipping data')
    assert [r['header']['word_0a'] for r in rows]==[1,1,0]
    return dict(method='A: selected first blocks from designated reference VBF',
                archive_index_sha256=index['sha256'],rows=rows,controls=controls,
                established='Two specifically identified authored bank entries carry word+0A=1; the selected contrast carries 0.',
                unresolved='Whole-corpus distribution, semantic field name, runtime class/binding, scene reachability and audible output are not established.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();result=collect()
    if a.write:
        with (E/'observation.json').open('x') as out:json.dump(result,out,indent=2)
    elif (E/'observation.json').exists():assert result==json.loads((E/'observation.json').read_text())
    if (E/'manifest.json').exists():
        for name,h in json.loads((E/'manifest.json').read_text()).items():assert sha((E/name).read_bytes())==h,name
    print(json.dumps(result,indent=2))
