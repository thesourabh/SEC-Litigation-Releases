import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.sec.gov"
years = {}


def fetch_year_page(year):
	print(BASE_URL + years[year])
	year_request = requests.get(BASE_URL + years[year])
	return year_request.content
	
def create_year_files(year):
	year_file = open("years/" + str(year) + ".html", "wb")
	year_page = fetch_year_page(year)
	year_file.write(year_page)
	year_file.close()
	
def begin_fetch_and_parse():
	main_page = requests.get('https://www.sec.gov/litigation/litreleases.shtml')
	soup = BeautifulSoup(main_page.content, 'html.parser')
	archive_links = soup.find(id='archive-links')
	for link in archive_links.find_all('a'):
		years[int(link.text)] = link.attrs['href']	
	for year in list(years.keys())[::-1]:
		create_year_files(year)
		
if __name__ == "__main__":
	begin_fetch_and_parse()