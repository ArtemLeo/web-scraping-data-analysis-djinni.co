BOT_NAME = "scrape_djinny"

SPIDER_MODULES = ["scrape_djinny.spiders"]
NEWSPIDER_MODULE = "scrape_djinny.spiders"

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "vacancies.csv": {
        "format": "csv",
        "overwrite": True,
    },
}
