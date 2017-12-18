# imports
import requests
from bs4 import BeautifulSoup
import csv

# file paths
csv_out = r"C:\Users\tjohnson\Desktop\For OS-Geo\Wendy's\wendy's_scrape.csv"

# storage lists
out_list = []
state_list = []
city_list = []
cities_list = []
store_list = []

# urls
base_url = 'https://locations.wendys.com/'


def build_scraper():
    single_level_scrape(base_url, 'class', 'col', state_list)
    for state in state_list:
        single_level_scrape(base_url + state, 'class', 'col', city_list)
    for city in city_list:
        single_level_scrape(base_url + city, 'itemtype', 'https://schema.org/FastFoodRestaurant', cities_list)
    for item in cities_list:
        data_extract_scrape(base_url + item)    


def single_level_scrape(scrape_url, html_selector, html_selector_name, list_level):
    r = requests.get(scrape_url)
    soup = BeautifulSoup(r.content, 'lxml')

    for item in soup.find_all(attrs={html_selector: html_selector_name}):
        for anchor in item.find_all('a', href=True):
            list_level.append(anchor['href'])
            
            
def single_level_scrape_tag(scrape_url, tag, list_level):
    r = requests.get(scrape_url)
    soup = BeautifulSoup(r.content, 'lxml')

    for item in soup.find_all(tag):
        for anchor in item.find_all('a', href=True):
            list_level.append(anchor['href'])


def data_extract_scrape(scrape_url):
    r = requests.get(scrape_url)
    soup = BeautifulSoup(r.content, 'lxml')

#    try:
    store_num = scrape_url.rsplit('-', 1)[-1].strip()
    
    address = soup.find(attrs={'itemprop': 'streetAddress'}).text.strip()
    city = soup.find(attrs={'itemprop': 'addressLocality'}).text.strip()
    state = soup.find(attrs={'itemprop': 'addressRegion'}).text.strip()
    zipcode = soup.find(attrs={'itemprop': 'postalCode'}).text.strip()

    lat = soup.find(attrs={'itemprop': 'latitude'})['content'].strip()
    lon = soup.find(attrs={'itemprop': 'longitude'})['content'].strip()

    field_list = [store_num, address, city, state, zipcode, lat, lon]
    out_list.append([field_list])
#    except Exception as e:
#        print(scrape_url)
#        print(e)


def csv_write(outfile):
    with open(outfile, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv, delimiter=',')
        writer.writerow(['Store Number', 'Address', 'City', 'State', 'Zipcode', 'Latitude', 'Longitude'])
        for item in out_list:
            writer.writerows(item)


if __name__ == "__main__":
    build_scraper()
    csv_write(csv_out)
