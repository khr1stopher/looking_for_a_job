import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["http://www.linkedin.com/jobs/search"]

    def parse(self, response):
        pass
