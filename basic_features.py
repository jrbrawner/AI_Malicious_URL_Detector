# extracts basic features from a full url
from urllib.parse import urlparse

urlList = ['url']
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


def is_https(url):
    scheme = urlparse(url).scheme
    if scheme == 'https':
        return 1
    return 0

