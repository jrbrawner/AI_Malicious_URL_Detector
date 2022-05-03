# url features obtained by using external entities
import requests
import whois
from datetime import datetime
from urllib.parse import urlparse
from requests import get
from bs4 import BeautifulSoup
from pyquery import PyQuery

class ExternalFeatures:
    def __init__(self, url):
        self.url = url

        try:
            self.whois = whois.whois(str(urlparse(url).hostname))
        except:
            self.whois = None

        try:
            self.response = get(self.url, timeout=10)
            self.pq = PyQuery(self.response.text)
        except:
            print('Get request error.')
            self.response = None
            self.pq = None

        try:
            self.soup = BeautifulSoup(str(self.response.content), 'html.parser')
        except:
            print('Couldnt reach page.')

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
            #couldnt resolve query so no value for expiration date
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
                self.page_rank()]

        return data
