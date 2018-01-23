import requests
import os
import re
import time
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
	try:
		year_request = requests.get(BASE_URL + relative_path)
	except:
		time.sleep(30)
		year_request = requests.get(BASE_URL + relative_path)		
	return year_request.content
	
def get_pdf_from_case(release_soup, file_name, year):
	sec_complaint = release_soup.find('a', string=re.compile('SEC Complaint'))
	if (not sec_complaint):
		sec_complaint = release_soup.find('a', href=re.compile('\.pdf'))
	if (sec_complaint):
		pdf_href = sec_complaint.attrs['href']
		print("PDF:", pdf_href)
		try:
			pdf = fetch_page(pdf_href)
			pdf_file_name = file_name[:file_name.rfind('.')] + '-' + pdf_href[pdf_href.rfind('/') + 1:]
			pdf_file = open('cases/' + year + "/" + pdf_file_name, "wb")
			pdf_file.write(pdf)
			pdf_file.close()
		except:
			return
		
def get_matched_case(raw_page, href, year):
	string_page = str(raw_page)
	res = re.compile('|'.join(PHRASES), re.IGNORECASE).search(string_page)
	if (res):
		file_name = href[href.rfind('/') + 1:]
		print(file_name, res)
		file = open('cases/' + year + "/" + file_name, "wb")
		file.write(raw_page)
		file.close()
		release_soup = BeautifulSoup(raw_page, 'html.parser')
		get_pdf_from_case(release_soup, file_name, year)
	
	
def parse_year_file(year_file_path):
	year_file = open(BASE_YEAR_DIRECTORY + year_file_path, "r").read()
	soup = BeautifulSoup(year_file, 'html.parser')
	litigation_releases = soup.find_all('a', string=re.compile('^LR-'))
	year = year_file_path[:4]
	try:
		int(year)
	except:
		return
	print("Now processing cases for the year", year)
	os.makedirs("cases/" + year, exist_ok=True)
	for release in litigation_releases:
		print(release.string)
		href = release.attrs['href']
		raw_page = fetch_page(href)
		get_matched_case(raw_page, href, year)
	
def parse_pages_by_year():
	files = [f for f in os.listdir('years') if f.endswith('.html')]
	print(files)
	for year_file_path in files:
		parse_year_file(year_file_path)
		#break
		
if __name__ == "__main__":
	parse_pages_by_year()