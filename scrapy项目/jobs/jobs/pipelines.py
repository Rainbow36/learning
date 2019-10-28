# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl


class JobsPipeline(object):
    path = "C:\\Users\\Administrator\\PycharmProjects\\Daliywork\\jobs\\output.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Jobs'
    workbook.save(path)

    def process_item(self, item, spider):
        row = [value for value in item.values()]
        self.sheet.append(row)
        self.workbook.save(self.path)
        print("\tStored!")
        return item
