"""Read exactly eight qwords at stopped-event RSP. No unwind or caller attribution."""
import ctypes
import struct


def snapshot(api, handle, rsp):
    record = dict(status='INVALID', address=rsp, requested_bytes=64)
    if not isinstance(rsp, int) or not 0 < rsp <= (1 << 64) - 64:
        record['error'] = 'invalid stack range'
        return record
    buffer = ctypes.create_string_buffer(64)
    count = ctypes.c_size_t()
    try:
        ok = api.ReadProcessMemory(handle, rsp, buffer, 64, ctypes.byref(count))
        error = ctypes.get_last_error()
        record.update(api_result=bool(ok), bytes_read=count.value,
                      last_error=error if not ok else None,
                      raw=buffer.raw[:min(count.value, 64)].hex())
        if not ok or count.value != 64:
            record['error'] = 'failed or incomplete stack read'
            return record
        words = list(struct.unpack('<8Q', buffer.raw))
        record.update(status='READ', qwords=words, top_qword=words[0])
    except Exception as error:
        record['error'] = repr(error)
    return record
