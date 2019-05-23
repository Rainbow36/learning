# -*- coding: UTF-8 -*-
import csv
import xlrd


def csv_word_lines(word, file_path):
    csvfile = open(file_path, 'r', encoding='utf8')
    reader = csv.reader(csvfile)

    lines = []
    for item in reader:
        key = item[0]
        if key == word:
            lines.append(item)
            break
    for item in reader:
        key = item[0]
        if key == word:
            lines.append(item)
        if key == " " or key == "":
            lines.append(item)
        elif key != word:
            break
    csvfile.close()
    return lines


workbook = xlrd.open_workbook("./datas/单词和短语释义抓取表.xlsx")  # 文件路径
worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows  # 获取该表总列数

col_data = worksheet.col_values(0)  # 获取第一列的内容

file1 = './datas/yourdictionary.csv'
file2 = './datas/oxford.csv'
csvfile1 = open(file1, 'r', encoding='utf8')
reader1 = csv.reader(csvfile1)
csvfile2 = open(file2, 'r', encoding='utf8')
reader2 = csv.reader(csvfile2)
newfile = open('./datas/merged.csv', 'w', encoding='utf8')
writer = csv.writer(newfile)
writer.writerow(['word', 'pos', 'definition'])

words1 = []
for item in reader1:
    word = item[0]
    if word != " " and word != "":
        words1.append(word)
# print(words1)
words2 = []
for item in reader2:
    word = item[0]
    if word != "":
        words2.append(word)
# print(words2)


for word in col_data:
    if word in words1:
        lines = csv_word_lines(word, file1)
        for l in lines[1:]:
            l[0] = ""
        writer.writerows(lines)
    elif word in words2:
        lines = csv_word_lines(word, file2)
        for l in lines[1:]:
            l[0] = ""
        writer.writerows(lines)
    else:
        writer.writerow([word, '', ''])

csvfile1.close()
csvfile2.close()
newfile.close()
