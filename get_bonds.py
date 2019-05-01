# grab coupons from bond.finam.ru
# put the data into json as a result

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
from sys import argv
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


def get_array_with_accruals(row, t):
	results = []  # array of arrays

	rows = t.find_all('tr')

	count = 0
	for row in rows:

		if len(row.contents) != 7:
			continue

		count += 1
		cols = row.find_all('td')
		oneRow = []
		for col in cols:
			oneRow.append( col.text.strip() )

		if len(oneRow) != 0:
			results.append(oneRow)
			#print('one row: ' + str(oneRow))

	else:
		print("no more rows")

	print('total rows count: ' + str(count))
	return results

#raw_html = simple_get('https://bonds.finam.ru/issue/details001D600002/default.asp')
#soup = BeautifulSoup(raw_html, 'html5lib')
#soup = BeautifulSoup(raw_html, 'html.parser')

# читаем из файла (для отладки)
# html5lib читает все таблицы хорошо
# soup = BeautifulSoup(open('saved_html_pages/russia-2030.html'), 'html5lib')
# html.parser не может прочитать таблицу купонов до конца, прерывается на 39-м купоне для Russia-30
# soup = BeautifulSoup(open('saved_html_pages/russia-2030.html'), 'html.parser')

BondSearch = BondSearch()
couponsURL = BondSearch.find_coupons(argv[1])
raw_html = simple_get(couponsURL)
soup = BeautifulSoup(raw_html, 'html5lib')

results = []

for i, t in enumerate(soup.select('table')):
	row = t.find('tr')

	# print('row text: ' + row.text)
	col = row.find('th')
	if col != None:

		# Если таблица не имеет родителя, то пропускаем.
		# Это корневая таблица, на базе которой построена разметка страницы
		if t.find_parent('table') == None:
			continue

		if col.text == 'Купоны':
			print("ok")
			results = get_array_with_accruals(row, t)
			break
	else:
		print("fail")
		continue

# print(results)
filename = 'table.json'
wfile = open(filename, mode='w', encoding='UTF-8')
json.dump(results, wfile, indent=4, ensure_ascii=False)
wfile.close()

# filename = 'raw.html'
# wfile = open(filename, mode='w', encoding='UTF-8')
# wfile.write(str(raw_html))
# wfile.close()

print (argv)
