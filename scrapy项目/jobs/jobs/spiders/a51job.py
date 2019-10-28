# -*- coding: utf-8 -*-
import re

import openpyxl
import scrapy

from jobs.items import JobsItem


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']

    detail_count = 0

    start_urls = []
    # for page in range(1, 109):
    for page in range(100, 109):
        start_urls.append(
            'https://search.51job.com/list/070200,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(
                str(page)))

    def parse(self, response):
        job_list = []
        for element in response.xpath('//div[@class="el"]'):
            job_url = element.xpath('p/span/a/@href').extract()
            if job_url:
                job_url = job_url[0]
                job_list.append(job_url)
                yield scrapy.Request(job_url, callback=self.detail_parse)

    # job_ids = ['109376197', '115632089', '112897298', '105771981', '117393569', '111764863', '117984762', '116568081',
    #            '112900198', '114394065', '117474408', '116000490', '110190589', '117284521', '117843319', '117539341',
    #            '76393718', '100305577', '113029929', '117993431', '108104271']
    # start_urls = []
    # for id in job_ids:
    #     start_urls.append("https://jobs.51job.com/nanjing-jyq/{}.html?s=01&t=0".format(id))

    def detail_parse(self, response):
        # print(
        #     "-------------------------------------------------detail-------------------------------------------------\n" + response.url)
        try:
            # html = response.body.decode(response.encoding)
            item = JobsItem()
            for key in ['job_name', 'job_salary', 'company_name', 'company_area', 'workage_limit', 'degree_required',
                        'job_number', 'release_time', 'other_req', 'welfare_label', 'job_infomation',
                        'contact_information', 'company_information']:
                item[key] = ""

            job_header = response.xpath('//div[@class="tHeader tHjob"]/div/div')[0]
            item['job_name'] = job_header.xpath('h1/@title')[0].extract()
            if job_header.xpath('strong/text()'):
                item['job_salary'] = job_header.xpath('strong/text()')[0].extract()
            else:
                item['job_salary'] = "面议"
            item['company_name'] = job_header.xpath('p[@class="cname"]/a/@title')[0].extract()

            # 灰色小字
            part1 = job_header.xpath('p[@class="msg ltype"]/@title')[0].extract().split('\xa0\xa0|\xa0\xa0')
            item['company_area'] = part1[0]
            for content in part1[1:]:
                if "年" in content or content == "无工作经验":
                    item['workage_limit'] = content
                elif content in ["初中及以下", "中技", "中专", "高中", "本科", "硕士", "大专", "博士"]:
                    item['degree_required'] = content
                elif "招" in content:
                    item['job_number'] = content
                elif "发布" in content:
                    item['release_time'] = content
                else:
                    item['other_req'] = content

            item['welfare_label'] = str(job_header.xpath('div/div/span/text()').extract())

            # 详细信息
            company_main = response.xpath('//div[@class="tCompany_main"]/div[@class="tBorderTop_box"]')
            for com in company_main:
                h = com.xpath("h2/span/text()")[0].extract()
                if h == "职位信息":
                    info = com.xpath("div//text()").extract()
                    item['job_infomation'] = ("".join(info[:info.index('微信分享')])).replace("\r\n", "").replace("  ",
                                                                                                              "").replace(
                        "\xa0", "")
                elif h == "联系方式":
                    item['contact_information'] = "".join(com.xpath("div/p//text()").extract())
                elif h == "公司信息":
                    item['company_information'] = ("".join(com.xpath("div//text()").extract())).replace("\r\n",
                                                                                                        "").replace(
                        "\xa0", "").replace("\u3000", "").replace("  ", "")
            self.detail_count += 1
            print(str(self.detail_count) + ": Crawled " + response.url + " finished!")

            yield item
        except Exception as e:
            print("Crawled " + response.url + " failed!")
            print(e)
            with open("C:\\Users\\Administrator\\PycharmProjects\\Daliywork\\jobs\\failed", "a+") as f:
                f.writelines(response.url)
                f.writelines("\n")

