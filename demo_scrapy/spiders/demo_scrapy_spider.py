# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from demo_scrapy.items import DemoScrapyItem


class DemoScrapySpider(CrawlSpider):
    name = "demo_scrapy"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
        "https://stackoverflow.com/questions?pagesize=50&sort=votes"
    ]

    rules = (
        Rule(LinkExtractor(allow=r"questions\?page=[0-5]&sort=newest"),
             callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        questions = response.xpath('//div[@class="summary"]/h3')

        for question in questions:
            question_location = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            full_url = response.urljoin(question_location)
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        item = DemoScrapyItem()
        item["title"] = response.css(
            "#question-header h1 a::text").extract()[0]
        item["url"] = response.url
        item["content"] = response.css(
            ".question .post-text").extract()[0]
        yield item
