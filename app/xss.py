invalid_chars = {
    ' ': '&nbsp',
    "\"": '&quot',
    '>': '&gt',
    '<': '&lt',
    "'": '&apos'
}


def xss(string):
    out = str()
    for character in string:
        token = invalid_chars.get(character, None)
        if token:
            out += token
        else:
            out += character
    return out
