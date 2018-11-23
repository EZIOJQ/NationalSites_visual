## proj_nps.py
## Skeleton for Project 2, Fall 2018
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup as bsoup
from alternate_advanced_caching import Cache
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username='Jay_C', api_key='N4SLfGx0p5UURNqudSFx')


## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)

#----------------------------------------------------------------START SCRAPPING
def Scrap(items):
    soup = BeautifulSoup(open("index.html"))


class NationalSite():
    def __init__(self, type, name, desc, url, address_street,address_city,address_state,address_zip):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url

        # needs to be changed, obvi.
        self.address_street = address_street
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip
        self.address_string = "{},{}, {}, {}".format(self.address_street,self.address_city,self.address_state,self.address_zip)
        self.adjust_address = self.address_string.replace("\n","")

    def __str__(self):
        # return <name> (<type>): <address string>
        return "{} ({}): {}".format(self.name, self.type, self.adjust_address)
## you can, and should add to and modify this class any way you see fit

## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name,location):
        self.name = name
        self.location =location
    def __str__(self):
        return self.name

    def lat(self):
        return self.location["lat"]
    def lng(self):
        return self.location["lng"]


## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
lst_url = []
# state_abbr = input("Please input a shortcut of the place")
CACHE_FNAME = "sample_cache_national_site.json"
CACHE_FNAME_Google = "google_cache.json"
primary_cache = Cache(CACHE_FNAME)

secondry_cache = Cache(CACHE_FNAME_Google)



def check_cache(lst_url):

    for url in lst_url:
        if primary_cache.get(url) is None:
            data = requests.get(url)
            html_text = data.text
            primary_cache.set(url,html_text,30)


def get_sites_for_state(state_abbr):
    base_url = str("https://www.nps.gov/" + "state/" + state_abbr + "/index.htm")
    lst_url.append(base_url)
    National_site=[]
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
        National_site.append(NationalSite(type, name, desc, base_url, address_name,address_city,address_state,address_zip))
    return National_site


MI = get_sites_for_state("MI")[0]




## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list

def check_cache_google(uni_url,baseurl,pd): 

    if secondry_cache.get(uni_url) is None:
        data = requests.get(baseurl,pd)
        html_text = data.text
        secondry_cache.set(uni_url,html_text,30)




def params_unique_combination(baseurl, params_d, private_keys=["key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def get_lat_lng(national_site):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    pd = {}
    pd["key"] = google_places_key
    pd["query"]= "{},{}".format(national_site.name,national_site.type)
    # pd["query"]= national_site.adjust_address
    uni_url = params_unique_combination(base_url, pd)
    check_cache_google(uni_url,base_url,pd)
    loc = json.loads(secondry_cache.get(uni_url))
    try :
        loc_lat = loc["results"][0]["geometry"]["location"]["lat"]
        loc_lng = loc["results"][0]["geometry"]["location"]["lng"]
        return("{},{}".format(loc_lat,loc_lng))
    except:
        return None

def get_nearby_places_for_site(national_site):
    nearby_site_lst = []
    loc = get_lat_lng(national_site)
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    pd = {}
    pd["key"] = google_places_key
    pd["location"] = loc
    pd["radius"] = 10000
    uni_url = params_unique_combination(base_url,pd)
    check_cache_google(uni_url, base_url,pd)
    results = json.loads(secondry_cache.get(uni_url))
    # print(results)
    for site in results["results"]:
        nearby_site_lst.append(NearbyPlace(site["name"],site["geometry"]["location"]))

    return nearby_site_lst[1:]



# print(get_lat_lng(MI))
# print(get_nearby_places_for_site(MI))

## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## side effects: launches a plotly page in the web browser

def find_max_min(lat_vals, lon_vals):

    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000
    for str_v in lat_vals:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in lon_vals:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v

    lat_axis = [min_lat, max_lat]
    lon_axis = [min_lon, max_lon]

    return [lat_axis,lon_axis]

def find_lat_lon_text(state_abbr):
    lat_vals = []
    lon_vals = []
    text_vals = []
    national_site = get_sites_for_state(state_abbr)
    for site in national_site:
        # print(get_lat_lng(site).split(","))
        if get_lat_lng(site) is not None:
            lat_vals.append(get_lat_lng(site).split(",")[0])
            lon_vals.append(get_lat_lng(site).split(",")[1])
            text_vals.append(site.adjust_address)
    return [lat_vals,lon_vals,text_vals]



def plot_sites_for_state(state_abbr):
    national_site = get_sites_for_state(state_abbr)[0]
    temp1 = find_lat_lon_text(state_abbr)
    lat_vals = temp1[0]
    lon_vals = temp1[1]
    text_vals = temp1[2]
    temp2 = find_max_min(lat_vals, lon_vals)
    lat_axis = temp2[0]
    lon_axis = temp2[1]
    center_lat = (lat_axis[0]+lat_axis[1]) / 2
    center_lon = (lon_axis[0]+lon_axis[1]) / 2
    data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        mode = 'markers',
        marker = dict(
        size = 8,
        symbol = 'star',
        ))]

    layout = dict(
            title = 'NationalSites in {}<br>(Hover for NationalSites address)'.format(state_abbr.upper()),
            geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(100, 217, 217)",
            countrycolor = "rgb(217, 100, 217)",
            lataxis = {'range': lat_axis},
            lonaxis = {'range': lon_axis},
            center= {'lat': center_lat, 'lon': center_lon },
            countrywidth = 3,
            subunitwidth = 3
            ),
        )

    fig = dict(data=data, layout=layout )
    py.plot( fig, validate=False, filename='usa - nationsites' )

# plot_sites_for_state("MI")

# ## Must plot up to 20 of the NearbyPlaces found using the Google Places API
# ## param: the NationalSite around which to search
# ## returns: nothing
# ## side effects: launches a plotly page in the web browser



def plot_nearby_for_site(national_site):
    small_lon_vals =[]
    small_lat_vals = []
    small_text_vals = []


    temp = get_lat_lng(national_site)
    if temp is not None:
        big_lat_vals = [temp.split(",")[0]]
        big_lon_vals = [temp.split(",")[1]]
        big_text_vals = national_site.adjust_address

        nearby_site_lst = get_nearby_places_for_site(national_site)
        for loc in nearby_site_lst:
            small_lon_vals.append(loc.lng())
            small_lat_vals.append(loc.lat())
            small_text_vals.append(loc.name)

        temp2 = find_max_min(small_lat_vals, small_lon_vals)
        lat_axis = temp2[0]
        lon_axis = temp2[1]
        center_lat = (lat_axis[0]+lat_axis[1]) / 2
        center_lon = (lon_axis[0]+lon_axis[1]) / 2



        trace1 = dict(
                type = 'scattergeo',
                locationmode = 'USA-states',
                lon = big_lon_vals,
                lat = big_lat_vals,
                text = big_text_vals,
                mode = 'markers',
                marker = dict(
                    size = 15,
                    symbol = 'star',
                    color = 'red'
                ))
        

        trace2 = dict(
                type = 'scattergeo',
                locationmode = 'USA-states',
                lon = small_lon_vals,
                lat = small_lat_vals,
                text = small_text_vals,
                mode = 'markers',
                marker = dict(
                    size = 8,
                    symbol = 'circle',
                    color = 'blue'
                ))



        data = [trace1, trace2]

        layout = dict(
                title = 'Places near {} <br>(Hover for places names)'.format(national_site.name),
                geo = dict(
                    scope='usa',
                    projection=dict( type='albers usa' ),
                    showland = True,
                    landcolor = "rgb(250, 250, 250)",
                    subunitcolor = "rgb(100, 217, 217)",
                    countrycolor = "rgb(217, 100, 217)",
                    lataxis = {'range': lat_axis},
                    lonaxis = {'range': lon_axis},
                    center= {'lat': center_lat, 'lon': center_lon },
                    countrywidth = 3,
                    subunitwidth = 3
                ),
            )


        fig = dict( data=data, layout=layout )
        py.plot( fig, validate=False, filename='usa-nation-sites-nearby' )


# plot_nearby_for_site(MI)

def options():

    print("--list <stateabbr>")
    print("--exit")
    print("--help")

def main():
    while True:

        options()
        user_input = input("Please choose a function\n")
        if "list" in user_input:
            state_abbr = user_input.split(" ")[1]
            lst = get_sites_for_state(state_abbr)
            for site in lst:
                print("{}) {}".format(lst.index(site)+1,site.name))

            user_input = input("Please choose a site to get nearby places or map\n")

            if user_input == "exit":
                exit()
            elif user_input == "help":
                print ("those command are: nearby <reuslt_number>,exit,map(show up all the national sites in this state")

            elif "nearby" in user_input:
                index = int(user_input.split(" ")[1])
                national_site = lst[index -1]
                nearby = get_nearby_places_for_site(national_site)

                for place in nearby:
                    print("{}) {}".format(nearby.index(place)+1, place.name))
                user_input = input("enter map to show the plot\n")
                if user_input == "map":
                    plot_nearby_for_site(national_site)
                elif user_input == "help":
                    print("those command are: exit,map(show up all the nearby places in plot)")

                else:
                    print("please input valid commend")


            elif user_input == "map":
                
                plot_sites_for_state(state_abbr)
            else:
                print("please input valid commend")



        elif user_input == "exit":
            exit()
        elif user_input == "help":
            print ("those command are: list, exit")
        else:
            print("please input valid commend")


main()

    



