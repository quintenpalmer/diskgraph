def printraw(c, color=None):
    """
    Print a character with no space separators nor line break.
    Also allows selecting a color of 'red', 'green', or 'blue'.
    """
    if color != None:
        if color == 'red':
            prefix = "\033[0;31m"
        if color == 'green':
            prefix = "\033[0;32m"
        if color == 'blue':
            prefix = "\033[0;34m"
        reset = "\033[0m"
        print(prefix, c, reset, sep='', end='')
    else:
        print(c, sep='', end='')

def format_bytes(bytes_int):
    """
    Display bytes in a human-friendly format (e.g. KB, MB, GB).
    """
    if bytes_int < 1024:
        return str(int(bytes_int)) + 'B'
    kb = bytes_int / 1024
    if kb < 1024:
        return str(int(kb)) + 'KB'
    mb = kb / 1024
    if mb < 1024:
        return str(int(mb)) + 'MB'
    gb = mb / 1024
    if gb < 1024:
        return str(int(gb)) + 'GB'
    tb = gb / 1024
    # we don't actually print any prefixes larger than terrabytes
    if tb < 10:
        return str('{0:.2f}'.format(tb)) + 'TB'
    else:
        return str(int(tb)) + 'TB'
