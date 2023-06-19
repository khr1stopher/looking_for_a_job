from datetime import datetime
import scrapy

class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["www.linkedin.com"]
    keywords = 'developer'
    location = 'United%20kingdom'
    start_urls = [
        f"https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&position=1&pageNum=0"
    ]

    custom_settings = {
            'FEEDS': {
                'linkedin.json': {
                    'format': 'json',
                    'encoding': 'utf8',
                    'store_empty': False,
                    'fields': None,
                    'indent': 4,
                    'item_export_kwargs': {
                        'export_empty_fields': True,
                    },
                },
            },
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'FEED_EXPORT_ENCODING': 'utf-8'
        }

    def __init__(self, *args, **kwargs):
        super(LinkedinSpider, self).__init__(*args, **kwargs)

    # def _parse(self, response, **kwargs):
    #     pass

    def parse_next_posts(self, response, **kwargs):
        jobs_post = response.xpath('//a[contains(@class, "base-card__full-link")]/@href').getall()
        
        if len(jobs_post) + len(kwargs['jobs']) <= self.post_count:
            link = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={self.keywords}&location={self.location}&position=1&pageNum=0&start={len(jobs_post)+len(kwargs["jobs"])+25}'
            yield response.follow(link, callback=self.parse_next_posts, cb_kwargs={
                'jobs': jobs_post + kwargs['jobs']
            })
        else:
            yield {
                'jobs': jobs_post + kwargs['jobs']
            }


    def parse(self, response, **kwargs):

        # Update the FEED_URI setting with the dynamic file name
        jobs_count = response.xpath('//h1[@class="results-context-header__context"]/span[@class="results-context-header__job-count"]/text()').get()
        jobs_post = response.xpath('//a[contains(@class, "base-card__full-link")]/@href').getall()
        self.post_count = int(jobs_count.replace(",", "").replace("+", ""))

        yield {
            'counter': jobs_count,
            'length': len(jobs_post),
        }

        if len(jobs_post) <= self.post_count:
            link = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={self.keywords}&location={self.location}&position=1&pageNum=0&start={len(jobs_post)+25}'
            yield response.follow(link, callback=self.parse_next_posts, cb_kwargs={
                'jobs': jobs_post,
            })