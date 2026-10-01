"""Scoped x64 staging/observation, never a replacement for the measured FF12 code.

Staging supplies the already-formatted ID at the original helper's return tail.
The original caller fragment, formatter, options getter and cookie check execute
at their shipping addresses. No Steam, logging, directory or game initialization.
"""
import struct

p32 = lambda n: struct.pack('<I', n)
p64 = lambda n: struct.pack('<Q', n)
SENTINEL = 0x5A17C0DE


def copy_qwords(n):
    # R10 = source, R11 = destination. Only volatile RAX changes; no stack use.
    assert n > 0 and n % 8 == 0
    return b''.join(b'\x49\x8b\x82'+p32(i)+b'\x49\x89\x83'+p32(i)
                    for i in range(0, n, 8))


def absolute_jump(a):
    return b'\xff\x25\x00\x00\x00\x00'+p64(a)


def make(code, data, crt, stable):
    # The actual caller requires a 16-aligned RSP and its writable prefix at +30.
    driver = bytearray(bytes.fromhex('41 54 48 81 ec 40 08 00 00 49 89 cc'))
    driver += bytes.fromhex('49 89 64 24 08')  # save caller RSP
    driver += bytes.fromhex('4d 8d 94 24')+p32(0x100)
    driver += bytes.fromhex('4c 8d 5c 24 30')+copy_qwords(64)
    driver += b'\x48\xb8'+p64(code+0x2000)+b'\xff\xd0'
    driver += bytes.fromhex('49 89 04 24 49 89 c2')
    driver += bytes.fromhex('4d 8d 9c 24')+p32(0x400)+copy_qwords(512)
    driver += (bytes.fromhex('49 8d 84 24')+p32(0x200) if stable
               else bytes.fromhex('49 8b 04 24'))
    driver += absolute_jump(0x197f7a)

    continuation = bytearray(bytes.fromhex('41 89 44 24 10 4d 8b 14 24'))
    continuation += bytes.fromhex('4d 8d 9c 24')+p32(0x800)+copy_qwords(512)
    continuation += bytes.fromhex('4c 8d 54 24 30 4d 8d 9c 24')+p32(0xa00)
    continuation += copy_qwords(1024)
    continuation += bytes.fromhex('48 81 c4 40 08 00 00 41 5c b8')+p32(SENTINEL)+b'\xc3'

    seed = bytearray(bytes.fromhex('48 81 ec 48 02 00 00 4d 8d 94 24')+p32(0x200))
    seed += bytes.fromhex('4c 8d 5c 24 30')+copy_qwords(512)
    seed += b'\x48\xb8'+p64(0x1f44830)
    seed += bytes.fromhex('48 8b 00 48 31 e0 48 89 84 24 30 02 00 00')
    seed += absolute_jump(0x1f3f52)

    # Tail-call shim: no push/pop/call or RSP write. Capture the second vararg.
    shim = bytearray(b'\x49\xbb'+p64(data))
    shim += bytes.fromhex('4c 8b 54 24 30 4d 89 53 18 4d 8b 52 08 4d 89 53 20')
    shim += bytes.fromhex('49 89 63 28 49 89 4b 30')
    shim += b'\x49\xbb'+p64(data+0x600)+copy_qwords(512)
    shim += absolute_jump(crt)
    parts = {0: bytes(driver), 0x1000: bytes(continuation),
             0x2000: bytes(seed), 0x3000: bytes(shim)}
    assert all(0 < len(b) < 0x1000 for b in parts.values())
    return parts
