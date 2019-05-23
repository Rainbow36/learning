import xlrd
import requests
from bs4 import BeautifulSoup
import csv

workbook = xlrd.open_workbook("./datas/单词和短语释义抓取表.xlsx")  # 文件路径
worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows  # 获取该表总列数

col_data = worksheet.col_values(0)[3466:]  # 获取第一列的内容
# print(col_data)

# workbook1 = xlsxwriter.Workbook('yourdictionary.xlsx')
# worksheet1 = workbook1.add_worksheet()
# i, j = 0, 0

# csvfile = open('yourdictionary.csv', 'w', encoding='utf8')
csvfile = open('./datas/yourdictionary.csv', 'a+', encoding='utf8')
writer = csv.writer(csvfile)
# writer.writerow(['word', 'pos', 'definition'])

for word in col_data:
    url = "https://www.yourdictionary.com/{}".format(word)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    licenses = soup.select('div.left')
    # print(licenses)
    for l in licenses:
        l_text = l.get_text()
        # print(l_text)
        if l_text == 'YourDictionary definition and usage example. Copyright © 2018 by LoveToKnow Corp':
            print(word)
            content = soup.select_one('#custom_entry_container')
            pos = content.select('span.custom_entry_pos')
            ol = content.select('ol.sense')

            for item in range(len(pos)):
                # if item == 0:
                #     # worksheet1.write(i, 0, word)

                definitions = ol[item].select('div.custom_entry')
                for d in definitions:
                    print(pos[item].get_text(), end=': ')
                    print(d.get_text())
                    # 存一行数据
                    # worksheet1.append([word, pos[item].get_text(), d.get_text()])
                    # worksheet1.write(i, 1, pos[item].get_text())
                    # worksheet1.write(i, 2, d.get_text())
                    # i += 1
                    if item == 0:
                        # worksheet1.write(i, 0, word)
                        writer.writerow([word, pos[item].get_text(), d.get_text()])
                    else:
                        writer.writerow(["", pos[item].get_text(), d.get_text()])

            print('')

# workbook1.close()
csvfile.close()