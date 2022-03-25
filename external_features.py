# url features obtained by using external entities
import requests
import whois
from datetime import datetime
from urllib.parse import urlparse
from requests import get
from bs4 import BeautifulSoup

url = 'http://www.google.com'

urlList = ['http://massfromgrass.com',
           'http://www.crestonwood.com/router.php',
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


def whois_registered_domain():
    return

# months since domain was registered, using average days in a month
def months_since_creation(url):
    url_host = str(urlparse(url).hostname)
    try:
        w = whois.whois(url_host)
    except whois.parser.PywhoisError:
        # registry does not contain domain, domain is expired, or is not .com,.net,.edu?
        return -1
    try:
        creation_date = w.creation_date[0]
    except:
        creation_date = w.creation_date

    formatted_creation_date = str(creation_date)
    formatted_creation_date = formatted_creation_date.split(" ")[0]
    today = str(datetime.today())
    formatted_today = today.split(" ", )[0]
    months = months_between(formatted_today, formatted_creation_date) / 30.4
    return months.__round__()


def months_since_expired(url):
    url_host = str(urlparse(url).hostname)
    try:
        w = whois.whois(url_host)
    except whois.parser.PywhoisError:
        # registry does not contain domain, domain is expired, or is not .com,.net,.edu?
        return -1
    try:
        expiration_date = w.expiration_date[0]
    except:
        expiration_date = w.expiration_date

    formatted_expiration_date = str(expiration_date)
    formatted_expiration_date = formatted_expiration_date.split(" ")[0]
    today = str(datetime.today())
    formatted_today = today.split(" ", )[0]
    if formatted_expiration_date > today:
        # domain not expired
        print(formatted_expiration_date)
        return 0
    months = months_between(formatted_today, formatted_expiration_date) / 30.4
    return months.__round__()


def months_between(d1, d2):
    try:
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    except:
        print(str(d1) + str(d2))
        return 0


def url_is_live(url):
    try:
        request = get(url)
        if request.status_code == 200:
            return 1
    except requests.ConnectionError:
        # cannot access link
        print(str(urlparse(url).hostname) + " Connection Error")
    return 0


def num_redirects(url):
    try:
        request = requests.get(url)
        if request.history:
            print('Request was redirected ' + str(len(request.history)) + ' times.')
            return len(request.history)
    except:
        # some kind of error, url isnt accessible, etc.
        print('Error')
        return -1
    # no redirects
    return 0


def get_html(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        return soup
    except:
        print('Error in reaching page.')


def body_length(url):
    try:
        soup = get_html(url)
        return len(soup.find('body').text)
    except:
        print('body_length Error')
        return 0

def num_titles(url):
    try:
        soup = get_html(url)
        titles = soup.findAll('title')
        return titles
    except:
        print('num_titles Error')
        return 0


print(num_titles(url))
