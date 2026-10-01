def on(m, idx, line):
    nm = NAMES[m]
    return 0 <= idx < len(nm) and re.search(b'(?<![A-Za-z0-9_])' + re.escape(nm[idx]) + b'(?![A-Za-z0-9_])', line) is not None
