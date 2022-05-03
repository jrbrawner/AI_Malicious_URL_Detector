# url features obtained by using external entities
import requests
import whois
from datetime import datetime
from urllib.parse import urlparse
from requests import get
from bs4 import BeautifulSoup
from pyquery import PyQuery
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re


class ExternalFeatures:
    def __init__(self, url):
        self.url = url

        #some provided urls may not start with http or https which causes problems with making requests,
        #if neither is detected, add http by default and we will check for actual scheme used later
        if self.url.startswith('http://') is True or self.url.startswith('https://'):
            self.http = True
        else:
            self.url = 'http://' + self.url
            self.http = False

        try:
            self.whois = whois.whois(str(urlparse(url).hostname))
        except:
            self.whois = None

        try:
            self.response = get(self.url, timeout=10)

            if self.response is not None:
                self.pq = PyQuery(self.response.text)
                self.soup = BeautifulSoup(str(self.response.content), 'html.parser')
            else:
                self.pq = None
                self.soup = None
        except:
            print('Get request error.')
            self.response = None
            self.pq = None
            self.soup = None

    # months since domain was registered, using average days in a month
    def months_since_creation(self):
        try:
            creation_date = self.whois.creation_date[0]
        except AttributeError:
            # couldnt resolve query so no value for creation date
            return 0
        except:
            creation_date = self.whois.creation_date

        formatted_creation_date = str(creation_date)
        formatted_creation_date = formatted_creation_date.split(" ")[0]
        today = str(datetime.today())
        formatted_today = today.split(" ", )[0]
        months = self.months_between(formatted_today, formatted_creation_date) / 30.4
        return months.__round__()

    def months_since_expired(self):
        try:
            expiration_date = self.whois.expiration_date[0]

        except AttributeError:
            # couldnt resolve query so no value for expiration date
            return 0
        except:
            expiration_date = self.whois.expiration_date
        try:
            formatted_expiration_date = str(expiration_date)
            formatted_expiration_date = formatted_expiration_date.split(" ")[0]
            today = str(datetime.today())
            formatted_today = today.split(" ", )[0]
            if formatted_expiration_date > today:
                # domain not expired
                return 0
            months = self.months_between(formatted_today, formatted_expiration_date) / 30.4
            return months.__round__()
        except:
            return 0

    def months_between(self, d1, d2):
        try:
            d1 = datetime.strptime(d1, "%Y-%m-%d")
            d2 = datetime.strptime(d2, "%Y-%m-%d")
            return abs((d2 - d1).days)
        except:
            return 0

    def url_is_live(self):
        if self.response == 200:
            return 1
        else:
            return 0

    def num_redirects(self):
        try:
            if self.response is not None:
                return len(self.response.history)
            else:
                return 0
        except:
            return 0

    def body_length(self):
        try:
            if self.soup is not None:
                return len(self.soup.find('body').text)
        except:
            return 0

    def numImages(self):
        if self.response is not None:
            return len([i for i in self.pq('img').items()])
        else:
            return 0

    def numLinks(self):

        if self.response is not None:
            return len([i for i in self.pq('a').items()])
        else:
            return 0

    def script_length(self):
        if self.response is not None:
            return len(self.pq('script').text())
        else:
            return 0

    def specialCharacters(self):

        if self.response is not None:
            body = self.pq('html').text()
            specialchars = [i for i in body if not i.isdigit() and not i.isalpha()]
            return len(specialchars)
        else:
            return 0

    def scriptToBodyRatio(self):
        bodyLength = self.body_length()
        scriptLength = self.script_length()
        if bodyLength != 0 and scriptLength != 0:
            ratio = scriptLength / bodyLength
            return ratio
        else:
            return 0

    def page_rank(self):
        # rate limited to 1800 requests per hour
        # time.sleep(1)
        domain = urlparse(self.url).hostname
        key = 'soo8scggk4woo0c00o4gsgckgg8wkoowwokcg40g'
        url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + str(domain)
        try:
            request = requests.get(url, headers={'API-OPR': key})
            result = request.json()
            result = result['response'][0]['page_rank_integer']
            if result:
                return result
            else:
                return 0
        except:
            return -1

    def is_https(self):
        if self.http is False:
            #this method of checking scheme takes quite some time, i will try to optimize later
            print('Have to check http scheme.')
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(self.url)
            autoUrl = driver.current_url
            httpScheme = autoUrl[:autoUrl.find(":")]
            if httpScheme == 'https':
                print('We added http to url, the page is using https but wasnt included in url.')
                return 1
            else:
                print('We added http to url, the page is using http but wasnt included in url.')
                return 0

        if self.http is True:
            if self.url.startswith("https://"):
                print('We didnt add http to url, and url is using https')
                return 1
            else:
                print('We didnt add http to url, and url is using http')
                return 0

    def build(self):
        data = [self.months_since_creation(),
                self.months_since_expired(),
                self.url_is_live(),
                self.num_redirects(),
                self.body_length(),
                self.numLinks(),
                self.numImages(),
                self.script_length(),
                self.specialCharacters(),
                self.scriptToBodyRatio(),
                self.page_rank(),
                self.is_https()]

        return data
