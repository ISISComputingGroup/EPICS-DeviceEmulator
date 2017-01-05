def optional_int_string_format(i, as_string, length):
    if as_string:
        return str(i) if length is None else str(i)[:length].zfill(length)
    else:
        return i


def pad_string(s, length, padding_character):
    return s if length is None else s[:length] + (length - len(s))*padding_character