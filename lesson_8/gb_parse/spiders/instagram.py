import json
import re
from urllib.parse import urlencode, urljoin
import scrapy

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    followers = {}

    def __init__(self, login, password, persons, *args, **kwargs):
        self.persons = persons
        self.login = login
        self.password = password
        self.query_hash = 'c76146de99bb02f6415203be841dd25a'
        super().__init__(*args, *kwargs)

    def parse(self, response):
        csrf_token = re.search('\"csrf_token\":\"\\w+\"', response.text).group().split(':').pop().replace(r'"', '')
        yield scrapy.FormRequest(
            'https://www.instagram.com/accounts/login/ajax/',
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.password},
            headers={'X-CSRFToken': csrf_token}
        )

    def parse_users(self, response):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for person in self.persons:
                yield response.follow(urljoin(self.start_urls[0], person), callback=self.parse_user, cb_kwargs={'person': person})

    def parse_user(self, response, user):
        user_id = json.loads(re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % user, response.text).group()).get('id')
        user_vars = self.variables_base
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars), callback=self.parse_folowers,
                              cb_kwargs={'user_vars': user_vars, 'user': user})

    def parse_folowers(self, response, user_vars, user):
        data = json.loads(response.body)
        if self.followers.get(user):
            self.followers[user]['followers'].extend(data.get('data').get('user').get('edge_followed_by').get('edges'))
        else:
            self.followers[user] = {'followers': data.get('data').get('user').get('edge_followed_by').get('edges'),
                                    'count': data.get('data').get('user').get('edge_followed_by').get('count')}
        if data.get('data').get('user').get('edge_followed_by').get('page_info').get('has_next_page'):
            user_vars.update(
                {'after': data.get('data').get('user').get('edge_followed_by').get('page_info').get('end_cursor')})
            next_page = self.make_graphql_url(user_vars)
            yield response.follow(next_page, callback=self.parse_folowers,
                                  cb_kwargs={'user_vars': user_vars, 'user': user})


    def make_graphql_url(self, user_vars):
        result = '{url}query_hash={hash}&{variables}'.format(url=self.graphql_url, hash=self.query_hash,
                                                             variables=urlencode(user_vars))
        return result

