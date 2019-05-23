# -*- coding: UTF-8 -*-
import csv
import xml.etree.ElementTree as ET

tree = ET.ElementTree(file='./datas/牛津袖珍释义.xml')
root = tree.getroot()
h = root.findall("./entry/h-g")
for elem in h:
    d = elem.findall("./dr-g")
    for i in d:
        elem.remove(i)
tempfile = './datas/oxford_temp.xml'
tree.write(tempfile, "UTF-8")

csvfile = open('./datas/oxford.csv', 'w', encoding='utf8')
writer = csv.writer(csvfile)
writer.writerow(['word', 'pos', 'definition'])

tree = ET.ElementTree(file=tempfile)
root = tree.getroot()
for elem in tree.iter():
    if elem.tag == 'entry':
        print('---------------------------')
        word_update = 1
        word = elem.attrib['Name']
        # print(elem.attrib['Name'])
    if elem.tag == 'p':
        pos_update = 1
        pos = elem.attrib['p']
        if pos == "n":
            pos = "noun"
        elif pos == "v":
            pos = "verb"
        elif pos == "adj":
            pos = "adjective"
        elif pos == "abbr":
            pos = "abbreviation"
        elif pos == "adv":
            pos = "adverb"
        elif pos == "prep":
            pos = "preposition"
        elif pos == "pron":
            pos = "pronoun"
        elif pos == "conj":
            pos = "conjunction"
        elif pos == "interj":
            pos = "interjection"
        # print(elem.attrib['p'])
    if elem.tag == 'd':
        # t = elem.text
        # while t and t[-1] == " ":
        #     t = t[:-1]
        # defi = t
        defi = elem.text
        print("插入的是：", end='')
        print([word, pos, defi])
        if word_update == 1:
            if pos_update == 0:
                writer.writerow([word, "", defi])
            else:
                writer.writerow([word, pos, defi])
            word_update = 0
            pos_update = 0
        else:
            writer.writerow(["", pos, defi])
    if elem.tag == 'u':
        if elem[0].text:
            defi = elem[0].text + "/"
            # print(elem[0].text, end='/')
        else:
            defi = ""
        print("插入的是：", end='')
        print([word, pos, defi])
        if word_update == 1:
            if pos_update == 0:
                writer.writerow([word, "", defi])
            else:
                writer.writerow([word, pos, defi])
            word_update = 0
            pos_update = 0
        else:
            writer.writerow(["", pos, defi])
    # if elem.tag == 'chn':
    #     if elem.text:
    #         defi += elem.text
    #         print("插入的是：", end='')
    #         print([word, pos, defi])
    #         if word_update == 1:
    #             if pos_update == 0:
    #                 writer.writerow([word, "", defi])
    #             else:
    #                 writer.writerow([word, pos, defi])
    #             word_update = 0
    #             pos_update = 0
    #         else:
    #             writer.writerow(["", pos, defi])
    #     else:
    #         if word_update == 1:
    #             if pos_update == 0:
    #                 writer.writerow([word, "", defi[:-1]])
    #             else:
    #                 writer.writerow([word, pos, defi[:-1]])
    #             word_update = 0
    #             pos_update = 0
    #         else:
    #             writer.writerow(["", pos, defi[:-1]])
csvfile.close()
