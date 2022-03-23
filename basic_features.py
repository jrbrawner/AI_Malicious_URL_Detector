# extracts basic features from a full url that can be calculated without contacting external entities on the internet

import re
from urllib.parse import urlparse
import math
from collections import Counter
import ipaddress as ipaddr

urlList = ['url', 'http://www.crestonwood.com/router.php',
           'http://shadetreetechnology.com/V4/validation/a111aedc8ae390eabcfa130e041a10a4',
           'https://support-appleld.com.secureupdate.duilawyeryork.com/ap/89e6a3b4b063b8d/?cmd=_update&dispatch=89e6a3b4b063b8d1b&locale=_',
           'http://rgipt.ac.in',
           'http://www.iracing.com/tracks/gateway-motorsports-park/',
           'http://appleid.apple.com-app.es/',
           'http://www.mutuo.it',
           'http://www.shadetreetechnology.com/V4/validation/ba4b8bddd7958ecb8772c836c2969531',
           'http://vamoaestudiarmedicina.blogspot.com/',
           'https://parade.com/425836/joshwigler/the-amazing-race-host-phil-keoghan-previews-the-season-27-premiere/',
           'https://sura.careervidi.com/mot?fg=Z4Nwk2pibWKclbF2k29kaHd1YKCWjJyepKZdaXy0j2lj/koenig-sandra@online.de',
           'https://magalu-crediarioluiza.com/Produto_20203/produto.php?sku=1962067',
           'https://oki.si/pkginfo/change/sitekeyverification.php?origin=cob&check=yes&destination=authentication',
           'http://www.strykertoyhaulers.com/wp-admin/js/online/order.php?email%5Cu003dabuse@euroflightinternational.com',
           'https://monovative-my.sharepoint.com:443/:o:/g/personal/user_monovative_onmicrosoft_com/EmCzKJnKZgxDtejtstZ67qQBlkNaRN4Da620KjAjE91eWQ?e=5:wesEg8&amp;at=9',
           'http://98.126.214.77/ap/signin?openid.pape.max_auth_age=0&amp;openid.return_to=https://www.amazon.co.jp/?ref_=nav_em_hd_re_signin&amp;openid.identity=http://specs.openid.net/auth/2.0/identifier_select&amp;openid.assoc_handle=jpflex&amp;openid.mode=checkid_setup&amp;key=a@b.c&amp;openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&amp;openid.ns=http://specs.openid.net/auth/2.0&amp;&amp;ref_=nav_em_hd_clc_signin',
           'http://swallowthisbitchpics.com/jpg/www.global.visa.com/myca/oce/emea/action/request_type=un_Activation/visa.html',
           'http://107.180.44.78/login.php?cmd=login_submit&amp;id=d38dd677c4dd931661bdc94df4bafb23d38dd677c4dd931661bdc94df4bafb23&amp;session=d38dd677c4dd931661bdc94df4bafb23d38dd677c4dd931661bdc94df4bafb23',
           'https://bit.ly/2E6D7J1',
           'http://u.to/x9AVFg']


def file_to_list(filepath):
    list = []
    file_path = filepath
    # open file with urls to parse, and add to urlList
    with open(file_path, 'r') as read_obj:
        for line in read_obj:
            list.append(line.strip())
    read_obj.close()
    return list


all_tld_list = file_to_list('data/all_tld.txt')
all_shortener_list = file_to_list('data/url_shorteners.txt')


def count_at(url):
    return url.count('@')


def count_url_length(url):
    return len(url)


def count_host_length(url):
    return len(urlparse(url).hostname)


def count_dots(url):
    return url.count('.')


def count_hyphens(url):
    return url.count('-')


def count_question_marks(url):
    return url.count('?')


def count_and(url):
    return url.count('&')


def count_eq(url):
    return url.count('=')


def count_underscore(url):
    return url.count('_')


def count_tilde(url):
    return url.count('~')


def count_percent(url):
    return url.count('%')


def count_slash(url):
    return url.count('/')


def count_star(url):
    return url.count('*')


def count_colon(url):
    return url.count(':')


def count_comma(url):
    return url.count(',')


def count_semicolon(url):
    return url.count(';')


def count_dollar(url):
    return url.count('$')


def count_space(url):
    return url.count(' ')


def count_www(url):
    return url.count('www')


def count_com(url):
    return url.count('com')


def count_bslash(url):
    return url.count('\\')


def count_digits(url):
    return len(url)


def count_url_params(url):
    list = url.split('?')
    list.remove(list[0])
    params = str(list).split('&')
    if params[0] == "[]":
        params.remove("[]")
    return len(params)


# determines whether the url is using https or http
def is_https(url):
    scheme = urlparse(url).scheme
    if scheme == 'https':
        return 1
    return 0


# returns the ratio of letters in hostname compared to letters in full url
def ratio_hostname_2length(url):
    return len(urlparse(url).hostname) / (len(url))


# shannon formula for calculating entropy of the hostname, high entropy can be indicative of DGA
def url_entropy(url):
    hostname = urlparse(url).hostname
    p, lns = Counter(hostname), float(len(str(hostname)))
    return -sum(count / lns * math.log(count / lns, 2) for count in p.values())


# port number in url
def contains_port(url):
    port = urlparse(url).port
    if port is None:
        return 0
    return 1


# http or https in query segment of url
def http_in_query(url):
    query = urlparse(url).query
    return query.count('http')


# checks for tld in path of url
def tld_in_path(url):
    path = urlparse(url).path.upper()

    for i in all_tld_list:
        if path.count(i) > 0:
            print(i)
            return 1
    return 0


def shortener_url(url):
    for i in all_shortener_list:
        if urlparse(url).hostname == i:
            return 1
    return 0


def is_ip(url):
    hostname = urlparse(url).hostname
    try:
        ipaddr.ip_address(hostname)
        return 1
    except:
        return 0


