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
    # print('---------------------------------------')
    # print('中英分组：', end='')
    # print(zh_en_group)

    sentences = []
    start = 0
    while start < len(zh_en_group):
        en = zh_en_group[start][1]
        cn = zh_en_group[start + 1][1]
        if en[-1] == '(':
            en = en[:-1]
            cn = '(' + cn
        num = ''
        while en and en[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','“']:
            num += en[-1]
            en = en[:-1]
        num = num[::-1]
        cn = num + cn

        if sentences == []:
            sentences.append([en, cn])
            # print(sentences)
        else:

            if (')' in en and '(' not in en) and ('(' in sentences[-1][0] and ')' not in sentences[-1][0]):
                sentences[-1][0] += sentences[-1][1] + en
                sentences[-1][1] = cn
            elif en == '':
                # sentences[-1][1] += cn + ')'
                sentences[-1][1] += cn


            elif en in [')', ',', '“', '”', '?', '？']:
                sentences[-1][1] += en + cn
            elif en[0] == ')':
                en = en[1:]
                sentences.append([en, cn])
            elif en[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', ':', '：', '——', '(', '“', ',']:
                sentences[-1][1] += en + cn
            else:
                num = ''
                while en and en[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '“', '"']:
                    num += en[-1]
                    en = en[:-1]
                num = num[::-1]
                cn = num + cn
                sentences.append([en, cn])
        # print(sentences)

        start += 2

    return sentences

if __name__ == '__main__':
    ss=['Stop thief,” cried John as he ran. Others joined him, and soon there was a hue and cry“捉贼,”约翰边奔边喊。', '众人跟着他喊,于是刹那间响起一片喊捉声。']
    # print(ss[0])
    print(split_zh_en(ss[0]))
