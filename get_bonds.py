from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json

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
		log_error('Error during requests to {0} : {1}'.format(url,str(e)))
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
	
raw_html = simple_get('https://bonds.finam.ru/issue/details001D600002/default.asp')
w = len(raw_html)
print(w)

results = [] #array of arrays

html = BeautifulSoup(raw_html, 'html.parser')
for i, t in enumerate(html.select('table')):

	if t.text.find("КупоныПогашение") != -1:
		print ("000000000000000000000")
	else:
		continue
		
	#print(i, t.text)
	
	count = 0
	rows = t.find_all('tr')
	print(len(rows))
	for row in rows:
		#print (row.text)
		count+=1
		#print(count)
		#if count==10:
		#	break		
		
		cols = row.find_all('td')

		oneRow = []
		for col in cols:
			#print (col.text)

			oneRow.append(col.text)
			oneRow.append(',')
		
		results.append(oneRow)

#print(results)
filename = 'table.json'
wfile = open(filename, mode='w', encoding='UTF-8')
json.dump(results, wfile, indent=4, ensure_ascii=False)
wfile.close()