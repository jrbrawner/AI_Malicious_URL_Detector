# extracts basic features from a full url that can be calculated without contacting external entities on the internet

import re
from urllib.parse import urlparse
import math
from collections import Counter
import ipaddress as ipaddr


phishingHints = ['wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js', 'alibaba', 'css', 'myaccount',
                 'dropbox', 'themes', 'plugins', 'signin', 'view']


def file_to_list_filepath(filepath):
    list = []
    file_path = filepath
    # open file with urls to parse, and add to urlList
    with open(file_path, 'r') as read_obj:
        for line in read_obj:
            list.append(line.strip())
    read_obj.close()
    return list


all_tld_list = file_to_list_filepath('data/all_tld.txt')
all_shortener_list = file_to_list_filepath('data/url_shorteners.txt')


class BasicFeatures:
    def __init__(self, url):
        self.url = url
        self.all_tld_list = file_to_list_filepath('data/all_tld.txt')
        self.all_shortener_list = file_to_list_filepath('data/url_shorteners.txt')

    def count_at(self):
        return self.url.count('@')

    def count_url_length(self):
        return len(self.url)

    def count_host_length(self):
        try:
            return len(urlparse(self.url).hostname)
        except:
            return 0

    def count_dots(self):
        return self.url.count('.')

    def count_hyphens(self):
        return self.url.count('-')

    def count_question_marks(self):
        return self.url.count('?')

    def count_and(self):
        return self.url.count('&')

    def count_eq(self):
        return self.url.count('=')

    def count_underscore(self):
        return self.url.count('_')

    def count_tilde(self):
        return self.url.count('~')

    def count_percent(self):
        return self.url.count('%')

    def count_slash(self):
        return self.url.count('/')

    def count_star(self):
        return self.url.count('*')

    def count_colon(self):
        return self.url.count(':')

    def count_comma(self):
        return self.url.count(',')

    def count_semicolon(self):
        return self.url.count(';')

    def count_dollar(self):
        return self.url.count('$')

    def count_space(self):
        return self.url.count(' ')

    def count_www(self):
        return self.url.count('www')

    def count_com(self):
        return self.url.count('com')

    def count_bslash(self):
        return self.url.count('\\')

    # this is a copy of url length?
    def count_digits(self):
        return len(self.url)

    def count_url_params(self):
        list = self.url.split('?')
        list.remove(list[0])
        params = str(list).split('&')
        if params[0] == "[]":
            params.remove("[]")
        return len(params)

    # determines whether the url is using https or http
    def is_https(self):
        scheme = urlparse(self.url).scheme
        if scheme == 'https':
            return 1
        return 0

    # returns the ratio of letters in hostname compared to letters in full url
    def ratio_hostname_2length(self):
        try:
            return len(urlparse(self.url).hostname) / (len(self.url))
        except:
            return 0

    # shannon formula for calculating entropy of the hostname, high entropy can be indicative of DGA
    def url_entropy(self):
        hostname = urlparse(self.url).hostname
        p, lns = Counter(hostname), float(len(str(hostname)))
        return -sum(count / lns * math.log(count / lns, 2) for count in p.values())

    # port number in url
    def contains_port(self):
        port = urlparse(self.url).port
        if port is None:
            return 0
        return 1

    # http or https in query segment of url
    def http_in_query(self):
        query = urlparse(self.url).query
        return query.count('http')

    # checks for tld in path of url
    def tld_in_path(self):
        path = urlparse(self.url).path.upper()

        for i in self.all_tld_list:
            if path.count(i) > 0:
                return 1
        return 0

    def shortener_url(self):
        for i in all_shortener_list:
            if urlparse(self.url).hostname == i:
                return 1
        return 0

    def is_ip(self):
        hostname = urlparse(self.url).hostname
        try:
            ipaddr.ip_address(hostname)
            return 1
        except:
            return 0

    ### add to build dataset list
    def url_length_suspicious(self):
        if len(self.url) > 75:
            return 1
        else:
            return 0

    def sus_extension_type(self):
        if self.url.endswith('.txt') or self.url.endswith('php'):
            return 1
        else:
            return 0

    def phish_hints(self):
        count = 0
        for i in phishingHints:
            if i in self.url:
                count += 1

        return count

    def count_fragment(self):
        fragments = self.url.split('#')
        return len(fragments) - 1

    def build(self):
        data = []

        data.append(self.count_at())
        data.append(self.count_url_length())
        data.append(self.count_host_length())
        data.append(self.count_dots())
        data.append(self.count_hyphens())
        data.append(self.count_question_marks())
        data.append(self.count_and())
        data.append(self.count_eq())
        data.append(self.count_underscore())
        data.append(self.count_tilde())
        data.append(self.count_percent())
        data.append(self.count_slash())
        data.append(self.count_star())
        data.append(self.count_colon())
        data.append(self.count_slash())
        data.append(self.count_star())
        data.append(self.count_colon())
        data.append(self.count_comma())
        data.append(self.count_semicolon())
        data.append(self.count_dollar())
        data.append(self.count_space())
        data.append(self.count_www())
        data.append(self.count_com())
        data.append(self.count_bslash())
        data.append(self.count_digits())
        data.append(self.count_url_params())
        data.append(self.is_https())
        data.append(self.ratio_hostname_2length())
        data.append(self.url_entropy())
        data.append(self.contains_port())
        data.append(self.http_in_query())
        data.append(self.tld_in_path())
        data.append(self.shortener_url())
        data.append(self.is_ip())

        return data
