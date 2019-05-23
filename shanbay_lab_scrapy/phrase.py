# -*- coding: UTF-8 -*-
import csv

from mdict.readmdict import MDX
import xml.etree.ElementTree as ET


def simplify_mdx_phrase(file_path, new_file):
    f = open(new_file, 'w')
    f.write("<a>")
    mdx = MDX(file_path)
    items = mdx.items()
    for i in items.__iter__():
        a = i[1]
        s1 = str(a, encoding='utf-8')
        if '@' not in s1 and 'class="phrase' in s1 and ' href="ecd.css" />' in s1:
            f.write(s1)
    f.write("</a>")
    f.close()


if __name__ == '__main__':
    raw_file = "./datas/英汉大词典第二版.mdx"
    new_file = "./datas/phrase.xml"
    # new_file = "./datas/s1.xml"
    # 解析及简化词典，保留有短语的
    # simplify_mdx_phrase(raw_file, new_file)
    #
    file = "./datas/phrases.csv"
    csv_file = open(file, 'w', encoding='utf8')  # 以读方式打开文件
    writer = csv.writer(csv_file)
    writer.writerow(['phrase', 'definition', 'sentence_en', 'sentence_cn'])

    tree = ET.ElementTree(file=new_file)
    root = tree.getroot()
    for elem in tree.iter():
        elems = elem.findall("div[@class='phrase']")

        for child in elems:
            ph = child.find("span[@class='l']")
            phrase = ph.text
            phrase_update = 1
            print("phrase: " + phrase)

            se2 = child.findall("div[@class='se2']")
            for se in se2:
                df = se.find("span[@class='df']")
                if df != None and df.text != None:
                    definition = df.text
                    definition_update = 1
                    print("df: " + df.text)

                is_writed = 0
                egs = se.findall("div[@class='eg']")
                for eg in egs:
                    en_cn = ""
                    for e in eg.itertext():
                        en_cn += e
                    # print("eg: " + en_cn)
                    # 取英文
                    ex = eg.find("span[@class='ex']")
                    en = ""
                    for e in ex.itertext():
                        en += e
                    cn = en_cn.lstrip(en)

                    en = en.replace("  ", "").replace("\n", "")
                    print("en: " + en)
                    print("cn: " + cn)

                    if phrase_update == 1:
                        writer.writerow([phrase, definition, en, cn])
                    else:
                        if definition_update == 1:
                            writer.writerow(["", definition, en, cn])
                        else:
                            writer.writerow(["", "", en, cn])
                    is_writed = 1
                    phrase_update = 0
                    definition_update = 0
                if is_writed == 0:
                    writer.writerow([phrase, definition, "", ""])
    csv_file.close()
