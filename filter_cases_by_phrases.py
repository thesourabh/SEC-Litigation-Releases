import requests
import os
import re
from bs4 import BeautifulSoup


BASE_URL = "https://www.sec.gov"
BASE_YEAR_DIRECTORY = "years/"


PHRASES = [
"insider trading",
"inside trade",
"inside trading",
"illegal trade",
"illegal trading",
"section 16 insider"
]

years = {}


def fetch_page(relative_path):
	print(BASE_URL + relative_path)
	year_request = requests.get(BASE_URL + relative_path)
	return year_request.content
	
def parse_year_file(year_file_path):
	year_file = open(BASE_YEAR_DIRECTORY + year_file_path, "r").read()
	soup = BeautifulSoup(year_file, 'html.parser')
	litigation_releases = soup.find_all('a', string=re.compile('^LR-'))
	for release in litigation_releases:
		print(release.string)
		href = release.attrs['href']
		raw_page = fetch_page(href)
		string_page = str(raw_page)
		res = re.compile('|'.join(PHRASES), re.IGNORECASE).search(string_page)
		if (res):
			file_name = href[href.rfind('/') + 1:]
			print(file_name, res)
			file = open('cases/' + file_name, "wb")
			file.write(raw_page)
			file.close()
			#break
		#print(release.string, )
	# print(len(litigation_releases))
	
	
def parse_pages_by_year():
	files = [f for f in os.listdir('years')]
	for year_file_path in files[-2::-1]:
		parse_year_file(year_file_path)
		break
		
if __name__ == "__main__":
	parse_pages_by_year()