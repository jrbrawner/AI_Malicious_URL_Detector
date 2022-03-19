# extracts basic features from a full url that can be calculated without contacting external entities on the internet
import re
from urllib.parse import urlparse
import math
from scipy.stats import entropy
from collections import Counter

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
           ]
file_path = 'C:/Users/jrbbr/OneDrive/Desktop/urls.txt'


def file_path(filepath):
    file_path = filepath
    # open file with urls to parse, and add to urlList
    with open(file_path, 'r') as read_obj:
        for line in read_obj:
            urlList.append(line.strip())


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
    params = urlparse(url).params
    count = len(params)
    return count


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


for i in urlList:
    print(count_url_params(i))
