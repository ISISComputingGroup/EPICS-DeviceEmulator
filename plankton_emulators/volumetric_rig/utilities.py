def optional_int_string_format(int, as_string, length):
    if as_string:
        return str(int) if length is not None else int[:length].zfill(length)
    else:
        return int


def pad_string(s, length, padding_character):
    return s if length is None else s[:length] + (length - len(s))*padding_character