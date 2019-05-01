# searching bond on bond.finam.ru
# return url of page with bond's data

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from sys import argv

def is_good_response(resp):
	"""
	Returns True if the response seems to be HTML, False otherwise.
	"""
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200
			and content_type is not None
			and content_type.find('html') > -1)


def log_error(e):
	"""
	It is always a good idea to log errors.
	This function just prints them, but you can
	make it do anything.
	"""
	print(e)


def simple_get(url):
	"""
	Attempts to get the content at `url` by making an HTTP GET request.
	If the content-type of response is some kind of HTML/XML, return the
	text content, otherwise return None.
	"""
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None
	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None


# returns url of main page with bond's data
def find_bond():
	isin = argv[1]
	raw_html = simple_get('https://bonds.finam.ru/issue/search/default.asp?emitterCustomName='+isin)
	soup = BeautifulSoup(raw_html, 'html5lib')
	urls = soup.find_all('a')
	for url in urls:
		href = url.attrs.get('href')
		if href == None:
			continue
		if href.find('details') != -1:
			# URL example: https://bonds.finam.ru/issue/details001D6/default.asp
			return 'https://bonds.finam.ru'+href


# returns direct url of coupon's page
def find_coupons():
	"""Returns direct URL of coupon's page.
	Usage: >python search_bonds.py RU000A1006S9
	where RU000A1006S9  - is ISIN of bond
	Result: string, URL of coupon's page"""
	isin = argv[1]
	raw_html = simple_get('https://bonds.finam.ru/issue/search/default.asp?emitterCustomName='+isin)
	soup = BeautifulSoup(raw_html, 'html5lib')
	urls = soup.find_all('a')
	for url in urls:
		href = url.attrs.get('href')
		if href == None:
			continue
		if href.find('details') != -1:
			# URL example: https://bonds.finam.ru/issue/details001D600002/default.asp
			hlist = href.split('/')
			newHref = '/{}/{}00002/{}'.format(hlist[1],hlist[2],hlist[3])
			return 'https://bonds.finam.ru'+newHref


print(find_coupons())