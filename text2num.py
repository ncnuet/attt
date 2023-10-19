# A = 0, B = 1, ..., Z = 25
# => AB = 0*26^1 + 1*26^0 = 1

def text2num(text: str, bin=2):
    text = text.upper()
    tup = ()

    while len(text) != 0:
        samp = text[:bin]
        text = text[bin:]

        val = 0

        l = len(samp)
        for i in range(0, l):
            code = ord(samp[i]) - 65
            val += code*(26**(l-i-1))

        tup = tup + (val,)

    return tup
