def run(tag, bits, width, depth=1, mutated=False):
    u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    for a, n in [(LO & ~4095, 4096), (2543616, 4096), (1073741824, 4096), (1610612736, 8192)]:
        u.mem_map(a, n)
    body = bytearray(code)
    if mutated:
        body[2522956 - LO + 2] = 45
    u.mem_write(LO, bytes(body))
    u.mem_write(2544944, store)
    u.mem_write(2545140, table)
    ram = bytearray(b'\xa5' * 4096)
    struct.pack_into('<i', ram, STACK - 1073741824, depth)
    ram[STACK - 1073741824 + 4] = tag
    struct.pack_into('<I', ram, STACK - 1073741824 + 388, bits)
    u.mem_write(1073741824, bytes(ram))
    u.mem_write(1610616832, b'\xa7' * 4096)
    rec = bytearray(b'\xa6' * 48)
    struct.pack_into('<Q', rec, 16, DEST)
    struct.pack_into('<I', rec, 24, width << 28)
    struct.pack_into('<i', rec, 28, 0)
    u.mem_write(REC, bytes(rec))
    u.reg_write(UC_X86_REG_RBX, STACK)
    u.reg_write(UC_X86_REG_RSP, RSP)
    u.reg_write(UC_X86_REG_MXCSR, 8064)
    u.reg_write(UC_X86_REG_EFLAGS, 2)
    visits = []
    reads = []
    writes = []
    phase = 'conversion'
    actual = {i.address: i for i in cs.disasm(body, LO)}
    store_rsp = RSP - 8

    def visit(uc, pc, size, _):
        i = actual[pc] if phase == 'conversion' else si[pc]
        assert i.size == size
        assert pc in allowed if phase == 'conversion' else pc in si
        assert i.mnemonic != 'call', 'Unexpected original call: never stub'
        visits.append(dict(phase=phase, pc=hex(pc), hex=i.bytes.hex()))

    def read(uc, typ, address, size, value, _):
        legal = address == STACK and size == 4 or (address == STACK + 4 and size == 1) or (address == STACK + 388 and size == 4) if phase == 'conversion' else REC <= address and address + size <= REC + 48 or (2545140 <= address and address + size <= 2545164) or (address == store_rsp and size == 8)
        assert legal, ('Unexpected read', phase, hex(address), size)
        reads.append(dict(phase=phase, pc=hex(uc.reg_read(UC_X86_REG_RIP)), address=hex(address), size=size, hex=bytes(uc.mem_read(address, size)).hex()))

    def write(uc, typ, address, size, value, _):
        legal = address in [STACK, REC + 32] and size == 4 if phase == 'conversion' else address == DEST and size in [1, 2, 4]
        assert legal, ('Unexpected write', phase, hex(address), size)
        writes.append(dict(phase=phase, pc=hex(uc.reg_read(UC_X86_REG_RIP)), address=hex(address), size=size, hex=(value & (1 << 8 * size) - 1).to_bytes(size, 'little').hex()))
    u.hook_add(unicorn.UC_HOOK_CODE, visit)
    u.hook_add(unicorn.UC_HOOK_MEM_READ, read)
    u.hook_add(unicorn.UC_HOOK_MEM_WRITE, write)
    u.emu_start(ENTRY, STOP, count=32)
    assert u.reg_read(UC_X86_REG_RIP) == STOP and u.reg_read(UC_X86_REG_RSP) == RSP
    conversion = dict(pc=hex(u.reg_read(UC_X86_REG_RIP)), rsp=hex(u.reg_read(UC_X86_REG_RSP)), depth=struct.unpack('<i', u.mem_read(STACK, 4))[0], value_bits=bytes(u.mem_read(REC + 32, 4)).hex(), record=bytes(u.mem_read(REC, 48)).hex(), ram=bytes(u.mem_read(1073741824, 4096)).hex(), mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)))
    phase = 'store'
    u.reg_write(UC_X86_REG_RCX, REC)
    u.reg_write(UC_X86_REG_RSP, store_rsp)
    u.mem_write(store_rsp, struct.pack('<Q', SENT))
    u.emu_start(2544944, SENT, count=64)
    assert u.reg_read(UC_X86_REG_RIP) == SENT and u.reg_read(UC_X86_REG_RSP) == RSP
    after = dict(pc=hex(u.reg_read(UC_X86_REG_RIP)), rsp=hex(u.reg_read(UC_X86_REG_RSP)), record=bytes(u.mem_read(REC, 48)).hex(), ram=bytes(u.mem_read(1073741824, 4096)).hex(), running_popv=bytes(u.mem_read(LO, 256)).hex(), store=bytes(u.mem_read(2544944, 194)).hex(), table=bytes(u.mem_read(2545140, 24)).hex(), return_sentinel=bytes(u.mem_read(store_rsp, 8)).hex(), mxcsr=hex(u.reg_read(UC_X86_REG_MXCSR)))
    return dict(tag=tag, input_bits=f'{bits:08x}', width=width, depth=depth, mutated=mutated, running_hex=bytes(body).hex(), initial=dict(ram=bytes(ram).hex(), record=bytes(rec).hex(), rsp=hex(RSP), store_rsp=hex(store_rsp), return_sentinel=hex(SENT), mxcsr='0x1f80', entry=hex(ENTRY), stop=hex(STOP)), conversion=conversion, after=after, visits=visits, reads=reads, writes=writes)
