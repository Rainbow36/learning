# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    page_id = scrapy.Field()
    job_list = scrapy.Field()


class JobsItem(scrapy.Item):
    job_name = scrapy.Field()
    job_salary = scrapy.Field()
    company_name = scrapy.Field()
    company_area = scrapy.Field()
    workage_limit = scrapy.Field()
    degree_required = scrapy.Field()
    job_number = scrapy.Field()
    release_time = scrapy.Field()
    other_req = scrapy.Field()
    welfare_label = scrapy.Field()
    job_infomation = scrapy.Field()
    contact_information = scrapy.Field()
    company_information = scrapy.Field()
