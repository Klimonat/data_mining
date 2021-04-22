import re

import pymongo
import scrapy

from lesson_6_avito.gb_parse.loaders import AvitoLoader
from lesson_6_avito.gb_parse.spiders.xpaths import AVITO_APARTMENT_XPATH, AVITO_SECTION_XPATH, AVITO_PAGE_XPATH


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["www.avito.ru"]
    start_urls = ["https://www.avito.ru/krasnodar/kvartiry/prodam"]

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {"pagination": self.parse, "apartment": self.apartment_parse}

        for key, xpath in AVITO_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def apartment_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in AVITO_APARTMENT_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()