from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson5.gb_parse.spiders.hh import HhSpider
from lesson5.gb_parse import settings

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(HhSpider)
    crawler_proc.start()