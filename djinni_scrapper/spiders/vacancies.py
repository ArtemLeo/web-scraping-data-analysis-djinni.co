import random
import time

import scrapy
from scrapy.http import Response


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]
    download_delay = 3
    processed_urls = set()

    def parse(self, response: Response, **kwargs) -> None:
        for job_link in response.css(
            "ul.list-unstyled.list-jobs.mb-4 a::attr(href)"
        ).getall():
            if job_link not in self.processed_urls:
                self.processed_urls.add(job_link)
                yield response.follow(job_link, callback=self.parse_job)

        next_page = response.css(
            "ul.pagination.pagination_with_numbers li.page-item.active + li.page-item a.page-link::attr(href)"
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_job(response: Response) -> None:
        time.sleep(random.uniform(1, 3))
        yield {
            "title": response.css(
                "body > div.wrapper > div.page-content > div > header > div.detail--title-wrapper > div > div > "
                "h1::text"
            )
            .get()
            .strip(),
            "technologies": response.css(
                "body > div.wrapper > div.page-content > div > div:nth-child(2) > div.col-sm-4.row-mobile-order-1 > "
                "aside > div > ul:nth-child(3) > li:nth-child(2) > div > div.col.pl-2::text"
            )
            .get()
            .strip(),
        }
