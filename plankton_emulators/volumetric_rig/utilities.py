def optional_int_string_format(i, as_string, length):
    if as_string:
        return str(i) if length is None else str(i)[:length].zfill(length)
    else:
        return i


def optional_float_string_format(f, as_string):
    return "{0:.2f}".format(f).zfill(5) if as_string else f


def pad_string(s, length, padding_character):
    return s if length is None else s[:length] + (length - len(s))*padding_character


def convert_raw_to_int(raw):
    from types import StringType, IntType
    if type(raw) == IntType:
        return raw
    elif type(raw) == StringType:
        return int(raw.zfill(1))
    else:
        return 0