"""Round-trip real save files through the documented container transform.

OPUS-REQ-SWE2-ORACLE-SAVE-CONTAINER-ROUNDTRIP. CONTRACT-save-container-transform
section 12 reproduction formula:

    header = 'SAFH' + u32 declared_decompressed_size + u32 rotation n
    B      = rotl('FINAL FANTASY XII THE ZODIAC AGE', n); B[31] = 0
    key    = MD5(B[:31])                    # CryptDeriveKey: hash -> 128-bit RC4
    file   = header + RC4(key, deflate(payload, level=9))

Read direction: RC4 decrypt file[12:], zlib inflate, require len == header+4.
n is taken from header+8 of the file under test (writer picks rand()%32).

Deflate encoder: the game links classic zlib 1.2.11 (contract, ASTRA zlib
evidence). This script must run under a classic-zlib Python (e.g. the repo's
angr-venv, zlib 1.3.2) — a zlib-ng interpreter produces different level-9 bytes
and is rejected up front so a false mismatch cannot be recorded.
"""
import hashlib, json, struct, zlib
from pathlib import Path

assert 'ng' not in zlib.ZLIB_RUNTIME_VERSION, 'zlib-ng build; run under classic zlib (angr-venv)'

TITLE = b'FINAL FANTASY XII THE ZODIAC AGE'
assert len(TITLE) == 32
SAVES = sorted(Path('Database/Tools/work/ASTRA/BU-BINDING-20260913-save-backup')
               .glob('*/FFXII_*'))

def zclassic_compress(data, level=9):
    return zlib.compress(data, level)

def rotl(b, n):
    return b[n:] + b[:n]

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    out = bytearray()
    i = j = 0
    for c in data:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        out.append(c ^ S[(S[i] + S[j]) & 0xFF])
    return bytes(out)

def key_for(n):
    b = bytearray(rotl(TITLE, n))
    b[31] = 0
    return hashlib.md5(bytes(b[:31])).digest()

def unwrap(raw):
    if len(raw) <= 4 or raw[:4] != b'SAFH' or len(raw) <= 12:
        return dict(rejected='admission')
    declared, n = struct.unpack_from('<II', raw, 4)
    if n > 0x1F or declared > 0x100000:
        return dict(rejected='bounds')
    plain = zlib.decompress(rc4(key_for(n), raw[12:]))
    if len(plain) != declared or declared == 0:
        return dict(rejected='length', got=len(plain), want=declared)
    return dict(plain=plain, n=n, declared=declared)

def wrap(plain, n):
    return b'SAFH' + struct.pack('<II', len(plain), n) + rc4(key_for(n), zclassic_compress(plain, 9))

results = []
for path in SAVES:
    raw = path.read_bytes()
    un = unwrap(raw)
    rec = dict(file=str(path), size=len(raw))
    if 'plain' not in un:
        rec.update(status='REJECTED', detail=un)
        results.append(rec)
        print(path.name, path.parent.name, 'REJECTED', un)
        continue
    plain, n, declared = un['plain'], un['n'], un['declared']
    rebuilt = wrap(plain, n)
    rec.update(status='OK' if rebuilt == raw else 'MISMATCH', n=n, declared=declared,
               ciphertext_match=rebuilt == raw,
               first_diff=next((i for i, (a, b) in enumerate(zip(rebuilt, raw)) if a != b), None),
               compressed_len_shipped=len(raw) - 12,
               compressed_len_rebuilt=len(rebuilt) - 12,
               plaintext_sha256=hashlib.sha256(plain).hexdigest(),
               plaintext_head=plain[:16].hex())
    if n != 0:
        rec['neg_wrong_rotation'] = 'differs' if wrap(plain, 0) != raw else 'UNDETECTED'
    bad = bytearray(raw); bad[-1] ^= 0xFF
    try:
        nb = unwrap(bytes(bad))
        rec['neg_corrupt_tail'] = nb.get('rejected', 'UNDETECTED-accepted')
    except zlib.error:
        rec['neg_corrupt_tail'] = 'zlib_error'
    results.append(rec)
    print(path.name, path.parent.name, rec['status'], 'n=%d' % n, 'declared=%d' % declared,
          'first_diff=%s' % rec['first_diff'], 'neg:', rec.get('neg_wrong_rotation'),
          rec.get('neg_corrupt_tail'))

ok = [r for r in results if r.get('status') == 'OK']
neg = all(r.get('neg_corrupt_tail') != 'UNDETECTED-accepted' for r in results)
out = dict(method='documented-container reimplementation vs shipped files; deflate via classic zlib %s level 9' % zlib.ZLIB_RUNTIME_VERSION,
           files_tested=len(results), bit_for_bit=len(ok),
           negative_controls_ok=neg, results=results)
p = Path(__file__).with_name('save-container-roundtrip.json')
p.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Saved', p, '|', len(ok), '/', len(results), 'bit-for-bit | negatives:', neg)
