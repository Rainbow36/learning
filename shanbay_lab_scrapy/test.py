# -*- coding: UTF-8 -*-

mark = {"en": 1, "zh": 2}


def is_zh(c):
    x = ord(c)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True

    # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True

    # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True

    # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True

    # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True

    else:
        return False


def split_zh_en(zh_en_str):
    zh_en_group = []
    zh_gather = ""
    en_gather = ""
    zh_status = False

    for c in zh_en_str:
        if not zh_status and is_zh(c):
            zh_status = True
            if en_gather != "":
                zh_en_group.append([mark["en"], en_gather])
                en_gather = ""
        elif not is_zh(c) and zh_status:
            zh_status = False
            if zh_gather != "":
                zh_en_group.append([mark["zh"], zh_gather])
        if zh_status:
            zh_gather += c
        else:
            en_gather += c
            zh_gather = ""

    if en_gather != "":
        zh_en_group.append([mark["en"], en_gather])
    elif zh_gather != "":
        zh_en_group.append([mark["zh"], zh_gather])

    # return zh_en_group
    sentences = []
    start = 0
    while start < len(zh_en_group):
        en = zh_en_group[start][1]
        cn = zh_en_group[start + 1][1]
        while en[0] in ['?', '!', '.', ',', ' ']:
            en = en[1:]
        sentences.append([en, cn])
        start += 2
    # print(sentences)
    return sentences


# s = "Is she a friend of yours.她是你的朋友吗? That story of yours doesn’t sound very likely.你们说的那件事听来不大可能"
# print(split_zh_en(s))
content = "  呵呵卡卡阿AesddjhsdabxZ"
# while not content[0].encode('UTF-8').isalpha():
#     content = content[1:]
# print(content)
content=content.lstrip(' ')
print(content)
