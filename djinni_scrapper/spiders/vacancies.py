import random
import time

import scrapy
from scrapy.http import Response


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]
    download_delay = 3
    processed_job_links = set()  # Змінив назву на більш зрозумілу

    def parse(self, response: Response, **kwargs) -> None:
        # Проходження по всіх посиланнях на вакансії на поточній сторінці
        job_links = response.css("ul.list-unstyled.list-jobs.mb-4 a::attr(href)").getall()
        for job_link in job_links:
            if job_link not in self.processed_job_links:
                self.processed_job_links.add(job_link)
                yield response.follow(job_link, callback=self.parse_job)

        # Знаходження посилання на наступну сторінку та перехід до неї
        next_page_link = response.css(
            "ul.pagination.pagination_with_numbers li.page-item.active + li.page-item a.page-link::attr(href)"
        ).get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    @staticmethod
    def parse_job(response: Response) -> None:
        # Затримка перед обробкою наступного запиту, щоб уникнути блокування
        time.sleep(random.uniform(1, 3))

        # Збір інформації про вакансію
        job_title = response.css(
            "body > div.wrapper > div.page-content > div > header > div.detail--title-wrapper > div > div > h1::text"
        ).get().strip()

        job_technologies = response.css(
            "body > div.wrapper > div.page-content > div > div:nth-child(2) > div.col-sm-4.row-mobile-order-1 > "
            "aside > div > ul:nth-child(3) > li:nth-child(2) > div > div.col.pl-2::text"
        ).get().strip()

        yield {
            "title": job_title,
            "technologies": job_technologies,
        }
