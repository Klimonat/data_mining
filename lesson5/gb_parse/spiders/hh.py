import scrapy

from lesson5.gb_parse.loaders import HHLoader, AuthorLoader
from lesson5.gb_parse.spiders.xpaths import HH_PAGE_XPATH, HH_VACANCY_XPATH, HH_COMPANY_XPATH

class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113"]

    _xpath_selectors = {
        "vacancy": "//a[@data-qa='vacancy-serp__vacancy-title']/@href",
        "pagination": "//div[contains(@class, 'bloko-gap_top')]"
                      "//a[@class='bloko-button']/@href",
        "company": "//a[@data-qa='vacancy-company-name']/@href",}

    def _get_follow_xpath(self, response, xpath, callback):
        # for link in response.xpath(selector):
        #     yield response.follow(link, callback=callback)
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {
            "pagination": self.parse,
            "vacancy": self.vacancy_parse,
            "company": self.company_parse}

        for key, xpath in HH_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def vacancy_parse(self, response):
        loader = HHLoader(response=response)
        loader.add_value("vacancy_url", response.url)
        loader.add_value("table", "vacancy_table")
        for key, xpath in HH_VACANCY_XPATH.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()

        yield from self._get_follow_xpath(
            response, self._xpath_selectors['company'], self.company_parse
        )

    def company_parse(self, response):
        loader_author = AuthorLoader(response=response)
        loader_author.add_value("author_url", response.url)
        loader_author.add_value("table", "author_table")
        for key, xpath in HH_COMPANY_XPATH.items():
            loader_author.add_xpath(key, xpath)
        yield loader_author.load_item()