from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import mechanicalsoup

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

data = {
    'username': 'ballaneypranav',
    'password': 'Pza29kgNwLuyyz'
}

browser = mechanicalsoup.StatefulBrowser()

browser.open("https://igem.org/Login2")

browser.select_form('form[method="post"]')

browser.get_current_form().print_summary()

browser["username"] = data["username"]
browser["password"] = data["password"]

response = browser.submit_selected()

print(response.text)

team = 'BITSPilani-Goa_India'
page = ''
pageType = 'Team'
year = '2020'
url = 'https://' + year + '.igem.org/wiki/index.php?title=' + pageType + ':' + team + page + '&action=edit'
print(url)

browser.open(url)

browser.select_form('form')

browser.get_current_form().print_summary()