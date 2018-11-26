from bs4 import BeautifulSoup as bsoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime




lst_url = []
state_abbr = input("Please input a shortcut of the place")
CACHE_FNAME = "sample_cache_national_site.json"
base_url = str("https://www.nps.gov/" + "state/" + state_abbr + "/index.htm")
primary_cache = Cache(CACHE_FNAME)

# class Scrapy():
# 	def __init__(self,base_url):
# 		self.lst_url = [base_url]

# 	def add_url(url):
# 		return lst_url.append(url)

# 	def check_cache(self):
# 		for url in self.lst_url:
# 			if primary_cache.get(url) is None:
# 			    data = requests.get(url)
# 			    html_text = data.text
# 			    primary_cache.set(url,html_text,30)



# 	def do_scrapy(self,url):
# 		soup = bsoup(primary_cache.get(url), features="html.parser")



	

lst_url.append(base_url)

def check_cache(lst_url):

	for url in lst_url:
		if primary_cache.get(url) is None:
		    data = requests.get(url)
		    html_text = data.text
		    primary_cache.set(url,html_text,30)


check_cache(lst_url)
soup = bsoup(primary_cache.get(base_url), features="html.parser")
list_site = soup.find(id="list_parks").find_all(class_= "clearfix")
for lst in list_site:
	type = lst.find("h2").text
	# print(type)
	name = lst.find("h3").text 
	# print(name)
	desc = lst.find("p").text
	# print(desc)
	address_url = lst.find("ul").find_all("a")[1].get("href")
	address_lst = []
	# print(address_url)
	lst_url.append(address_url)
	check_cache(lst_url)
	soup2 = bsoup(primary_cache.get(address_url), features="html.parser")
	address_name = soup2.find(itemprop ="streetAddress").get_text()
	address_city = soup2.find(itemprop = "addressLocality").get_text()
	address_state = soup2.find(itemprop = "addressRegion").get_text()
	address_zip = soup2.find(itemprop = "postalCode").get_text()

def check_cache_google(uni_url,baseurl,pd): 
	
    if secondry_cache.get(uni_url) is None:
        data = requests.get(baseurl,pd)
        html_text = data.text
        secondry_cache.set(uni_url,html_text,30)



base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
pd = {}
pd["key"] = google_places_key
pd["query"]= national_site
uni_url = params_unique_combination(baseurl, pd)
check_cache_google(uni_url,baseurl,pd)
print(secondry_cache.get(uni_url))







