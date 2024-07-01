BOT_NAME = "djinni_scrapper"

SPIDER_MODULES = ["djinni_scrapper.spiders"]
NEWSPIDER_MODULE = "djinni_scrapper.spiders"

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
