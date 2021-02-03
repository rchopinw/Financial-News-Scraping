def process_text(t):
    t = t.replace('\n', '')
    return t


def process_compname(t):
    try:
        i2 = t.index('公司')
        i2 = i2 + 2
    except ValueError:
        i2 = 20
    compname = t[0:i2]
    for d in '关于对 ':
        compname = compname.replace(d, '')

    return compname
