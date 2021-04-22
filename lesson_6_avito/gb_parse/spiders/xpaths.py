AVITO_SECTION_XPATH = {
    "section": '//a[@class="rubricator-list-item-link-12kOm"]/@href'
}

AVITO_PAGE_XPATH = {
    "pagination": '//span[@class="pagination-item-1WyVp"]/@href',
    "apartment": '//div[@class="iva-item-titleStep-2bjuh"]//@href',
}

AVITO_APARTMENT_XPATH = {
    "title": {"xpath": "//span[@class='title-info-title-text'].text()"},
    "price": {"xpath": "//span[@class='js-item-price'].text()"},
    "address": {"xpath": "//div[@itemprop='address']/span.text()"},
    "parameters": {"xpath": "//ul[@class='item-params-list']//text()"},
    "author": {"xpath": "//div[@class='seller-info-name']/text()"},
}