# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from ..items import BldupCrawlerItem

import re
from datetime import datetime

class TauntondeedsSpider(scrapy.Spider):
    name = 'tauntondeeds'
    allowed_domains = ['www.tauntondeeds.com']
    start_urls = ['http://www.tauntondeeds.com/Searches/ImageSearch.aspx/']

    def parse(self, response):
        """
        function which prepare data for scraping
        """
        yield scrapy.FormRequest(
                self.start_urls[0],
                formdata={
                    'ctl00$cphMainContent$txtLCSTartDate$dateInput' : '2020-01-01-00-00-00',
                    'ctl00$cphMainContent$txtLCEndDate$dateInput': '2020-12-31-00-00-00',
                    'ctl00$cphMainContent$ddlLCDocumentType$vddlDropDown':'101627',
                    'ctl00$cphMainContent$btnSearchLC':'Search Land Court',
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                },
                callback=self.parse_results
            )
        
    def parse_results(self, response):
        """
        function that pars site and scraping data`s and goes to next page
        """
        item = BldupCrawlerItem()
        code_streets = ['RD', 'DR', 'AVE', 'ST', 'WAY', 'LANE']
        for rows in [response.css(".gridRow"), response.css(".gridAltRow")]:
            for x in rows:   
                print(x.css('td::text').extract())     
                item['date'] = datetime.strptime(x.css('td::text').extract()[1], '%m/%d/%Y')
                item['type'] = str(x.css('td::text').extract()[2])
                item['book'] = (lambda x: None if x == '\xa0' else x)(str(x.css('td::text').extract()[3]))
                item['page_num'] = (lambda x: None if x == '\xa0' else x)(str(x.css('td::text').extract()[4]))
                item['doc_num'] = str(x.css('td::text').extract()[5])
                item['city'] = str(x.css('td::text').extract()[6])
                item['description'] = str(x.css('td> span::text').extract()[0])

                try:
                    item['cost'] = float(re.split(r'\$', x.css('td> span::text').extract()[0])[-1])
                except ValueError:
                    item['cost'] = None
                part_description = x.css('td> span::text').extract()[0]
                for i in code_streets:
                    try:
                        item['street_address'] = part_description.split(f'{i}')[1]
                        break
                    except IndexError:
                        continue

                try:
                    item['state'] = str(re.search(r'STATE \w+', x.css('td> span::text').extract()[0].upper()).group(0).split('STATE ')[-1])
                except AttributeError:
                    item['state'] = None

                try:
                    item['zip'] = (x.css('td> span::text').extract()[0]).split('SP ')[1].split(' ')[0]
                except IndexError:
                    item['zip'] = None
                yield item

        span_number = response.css('tr>td>span::text').extract()[0]
        page_num = int(span_number) + 1

        js_href = response.css('td>a::attr(href)').extract()
        for i in js_href:
            res = re.search(r'Page\${}'.format(page_num), i)
            if res:
                yield scrapy.FormRequest(
                            self.start_urls[0],
                            formdata={
                                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                                '__EVENTTARGET': 'ctl00$cphMainContent$gvSearchResults',
                                '__EVENTARGUMENT': f'Page${page_num}',
                            },   
                            callback=self.parse_results
                        )
                break

