HH_PAGE_XPATH = {
    "pagination": '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    "vacancy": '//div[contains(@data-qa, "vacancy-serp__vacancy")]//'
    'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
    "company": "//a[@data-qa='vacancy-company-name']/@href",
}

HH_VACANCY_XPATH = {
    "title": '//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]/span/text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "skills": '//div[@class="bloko-tag-list"]//'
    'div[contains(@data-qa, "skills-element")]/'
    'span[@data-qa="bloko-tag__text"]/text()',
    "author": '//a[@data-qa="vacancy-company-name"]/@href',
}

HH_COMPANY_XPATH = {
    "name_company": '//span[@data-qa="bloko-header-2"]/span/text()',
    "link": '//a[@data-qa="sidebar-company-site"]/@href',
    "area": '//div[@sidebar-header-color"]/p/text()',
    "description_company": '//div[@data-qa="company-description-text"]/div/text()',
    "company_vacancies": '//div[@class="company-vacancies]//a[@data-qa="vacancy-serp__vacancy-title"]/text()',
}