# This script:
# 1)grabs coupons from bonds.finam.ru
# 2)puts the data into json as a result
# Result filename: ISIN_coupons.json, where ISIN
#   is substituted to real ISIN from the first parameter
# Parameters
# 1. ISIN - string - ISIN code of bond, like XS0114288789
# 2. Output dir - string - path to output directory (optional).
#    Dir name must not ends with '\'
#    If dir name contains spaces, it must be enclosed in quotes

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from json import dump
from sys import argv
from os import sep
from search_bonds import BondSearch


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


def is_good_response(resp):
	"""
	Returns True if the response seems to be HTML,
	False otherwise.
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


def get_array_with_coupons(ISIN):
	"""
	Collects coupons to an array.
	"""
	
	# Let's find URL of coupons page by ISIN.
	couponsURL = BondSearch().find_coupons(ISIN)
	
	# Retrieve page with coupons.
	raw_html = simple_get(couponsURL)
	couponsURL = None
	
	# Parse HTML and get 'soup' object.
	soup = BeautifulSoup(raw_html, 'html5lib')
	raw_html = None
	
	# Process the 'soup' object and find table with coupons.
	results = []
	for i, t in enumerate(soup.select('table')):
		row = t.find('tr')
		col = row.find('th')
		if col == None:
			continue

		# If the table has no parent - skip it, because it is root table for the page.
		if t.find_parent('table') == None:
			continue

		# If first column contains text 'Купоны' - this is needed table.
		if col.text == 'Купоны':
			rows = t.find_all('tr')
			count = 0
			for row in rows:
				# We know there is 7 columns in needed table.
				# And there is only one such table on the page.
				if len(row.contents) != 7:
					continue
				count += 1
				cols = row.find_all('td')
				oneRow = []
				for col in cols:
					oneRow.append(col.text.strip())
				if len(oneRow) != 0:
					results.append(oneRow)
			break
	return results


def make_json_with_coupons(ISIN, output_dir = ''):
	"""
	Flushes array with coupons to file.
	Filename: ISIN_coupons.json, where ISIN is
	substituted to real ISIN from first parameter
	"""

	if output_dir == '':
		filename = ISIN + '_coupons.json'
	else:
		filename = output_dir + sep + ISIN + '_coupons.json'

	coupons_array = get_array_with_coupons(ISIN)
	
	with open(filename, mode='w', encoding='UTF-8') as wfile:
		dump(coupons_array, wfile, indent=4, ensure_ascii=False)
		wfile.close()


############################# MAIN PROGRAM #############################



# читаем из файла (для отладки)
# html5lib читает все таблицы хорошо
# soup = BeautifulSoup(open('saved_html_pages/russia-2030.html'), 'html5lib')
# html.parser не может прочитать таблицу купонов до конца, прерывается на 39-м купоне для Russia-30
# soup = BeautifulSoup(open('saved_html_pages/russia-2030.html'), 'html.parser')

# First arg (argv[0]) - the name of the script (feature of python)
# User's args start from the second position, so if we have only 1 arg here - this is error
if len(argv) < 2:
	raise RuntimeError("not enough parameters")

# we always have ISIN in 2nd parameter
ISIN = argv[1].strip()

# we may have output directory in 3rd parameter
output_dir = ''
if len(argv) > 2:
	output_dir = argv[2].strip()

# run script
make_json_with_coupons(ISIN, output_dir)
