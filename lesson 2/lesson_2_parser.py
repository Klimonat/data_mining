import requests
from urllib.parse import urljoin
import bs4
import pymongo
import datetime


class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client["klimova_db"]
        self.collection = db["magnit"]

    def _get_response(self, url, *args, **kwargs):
        return requests.get(url, *args, **kwargs)

    def _get_soup(self, url, *args, **kwargs):
        return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    @property
    def _template(self):
        return {
            "product_name": lambda tag: tag.find("div", attrs={"class": "card-sale__title"}).text,
            "url": lambda tag: urljoin(self.start_url, tag.attrs.get("href", "")),
        }

    def processing_error_promo_name(self, product_tag):
        try:
            return product_tag.find("div", attrs={"class": "card-sale__name"}).text
        except:
            return ""

    def processing_error_price(self, product_tag, name_class):
        try:
            price_div = product_tag.find("div", attrs={"class": name_class})
            price_product_integer = price_div.find("span", attrs={"class": "label__price-integer"}).text
            price_product_decimal = price_div.find("span", attrs={"class": "label__price-decimal"}).text
            price_product = float(f"{price_product_integer}.{price_product_decimal}")
            price_product_correct = float('{:.2f}'.format(price_product))
            return price_product_correct
        except:
            return ""

    def processing_error_date(self, product_tag, dict_for_translating_months):
        try:
            date_promo = product_tag.find("div", attrs={"class": "card-sale__date"})
            date_promo_full = date_promo.find_all('p')
            length_date = len(date_promo_full)
            if length_date == 2:
                date_start, date_finish = date_promo_full[0].text, date_promo_full[1].text
            else:
                date_start = date_promo_full[0].text
                date_finish = date_promo_full[0].text

            date_start = date_start.split()
            date_finish = date_finish.split()
            day_start = date_start[1]
            day_finish = date_finish[1]
            month_start = dict_for_translating_months[date_start[2]]
            month_finish = dict_for_translating_months[date_finish[2]]
            year = '2021'
            date_start = datetime.datetime(year=int(year), month=int(month_start), day=int(day_start))
            date_finish = datetime.datetime(year=int(year), month=int(month_finish), day=int(day_finish))
            return date_start, date_finish
        except:
            return "", ""


    def _parse(self, url):
        soup = self._get_soup(url)
        catalog_main = soup.find("div", attrs={"class": "сatalogue__main"})
        product_tags = catalog_main.find_all("a", recursive=False)
        for product_tag in product_tags:
            product = {}
            product_url = product_tag['href']
            product_name = product_tag.find("div", attrs={"class": "card-sale__title"}).text
            image_product = product_tag.find("img", attrs={"class": "lazy"})
            image_product_url = str(image_product["data-src"])
            dict_for_translating_months = {'января': "01",
                                           'февраля': "02",
                                           'марта': "03",
                                           'апреля': "04",
                                           'мая': "05",
                                           'июня': "06",
                                           'июля': "07",
                                           'августа': "08",
                                           'сентября': "09",
                                           'октября': "10",
                                           'ноября': "11",
                                           'декабря': "12"
                                           }

            promo_name = self.processing_error_promo_name(product_tag)
            old_price_product = self.processing_error_price(product_tag, "label__price_old")
            new_price_product = self.processing_error_price(product_tag, "label__price_new")
            date_start, date_finish = self.processing_error_date(product_tag, dict_for_translating_months)

            product_info = {"url": product_url,
                            "promo_name": promo_name,
                            "product_name": product_name,
                            "old_price": old_price_product,
                            "new_price": new_price_product,
                            "image_url": image_product_url,
                            "date_from": date_start,
                            "date_to": date_finish
                            }

            yield product_info


    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == "__main__":
    url = "https://magnit.ru/promo/"
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(url, db_client)
    parser.run()

"""
for itm in collection.find({'product_name': {"$regex": r".*говяд"}}, {"url":1}):
    print(itm)
"""