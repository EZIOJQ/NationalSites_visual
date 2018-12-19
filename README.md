# Data visualization - NationalSites
(To run this project, you must have a google APIkey, to get a google APIkey, you can check this website for instructions: https://developers.google.com/places/web-service/get-api-key)

## How to run this project?
* Install Python packages BeautifulSoup4 and Plotly. 
```
$ pip3 install bs4 
$ pip3 install plotly
```
* Run "proj2_nps.py", you will see in your terminal as follow:
```
--list <stateabbr>
--exit
--help
Please choose a function:
```
* Input LIST and an abbreviation of one state to see all the national sites in this state.
```
list mi
1) Isle Royale
2) Keweenaw
3) Motor Cities
4) North Country
5) Pictured Rocks
6) River Raisin
7) Sleeping Bear Dunes
Please choose a site to get nearby places or map
```
* Input the index of one national site to see the nearby places.
```
nearby 1
1) South Lake Desor Campground
2) Malone Bay Campground
3) Hatchet Lake Campground
4) Todd Harbor Campground
5) Crystal Cove
6) Ishpeming Point
7) Isle Royale Wilderness
8) Little Todd Campground
9) North Lake Desor Campground
10) Hay Bay Campground
11) Hay Bay Boat Launch
12) Malone Bay Ranger Station
13) Malone Bay Boat Launch
enter map to show the plot
```
* Input "MAP" to see the nearby places around one national site.
![Michigan_Nearby](https://github.com/EZIOJQ/SI508-Project2/raw/master/Sample_Michigan_nearbyplaces.png)

Sample dataset:

| Trace 0, lat | Trace 0, lon | Trace 1, lat | Trace 1, lon | text 
| ------------ | :----------: | :----------: | :----------: | :---------: 
| 47.9958654 | '-88.9092899 | 47.9707203 | 	-88.9714702	| South Lake Desor Campground
|| |47.9851937	| -88.8057275|	Malone Bay Campground
|	|	|48.0212723	| -88.8470217	|Hatchet Lake Campground
|	|	|48.0526305	| -88.8221059	|Todd Harbor Campground
|	|	|47.9942394	| -88.9153876	|Ishpeming Point
|	|	|47.9865521	|-88.8878574	|Isle Royale Wilderness

* Or input "MAP" to see the plot of these national sites.
![Michigan](https://github.com/EZIOJQ/SI508-Project2/raw/master/Sample_Michigan_Nationalsite.png)

Sample dataset:
|lat	| lon	| text
|------------ | :----------: | :----------: 
|47.9958654	|-88.9092899	|800 East Lakeshore Drive, Houghton, MI 49931
|47.2423094	|-88.448106	|25970 Red Jacket Road, Calumet, MI 49913
|42.329549	|-83.0393779	|200 Renaissance Center, Suite 3148, Detroit, MI 48243
|46.5614384	|-86.3213064	|P.O. Box 40, Munising, MI 49862
|41.9112005	|-83.37672649999999	|1403 East Elm Street, Monroe, MI 48162
|44.8757238	|-85.9996747	|9922 Front Street, Empire, MI 49630

* Anytime you want to quit, input "exit". And anytime you need help, just input "help".

## Caching

* "Sample_cache_national_site.json" and "google_cache.json" are the sample cache files.
* Caching files are named. You can change them in line 59-60 in in "proj2_nps.py"
```
CACHE_FNAME = "sample_cache_national_site.json"
CACHE_FNAME_Google = "google_cache.json"
```

## Other files

* "alternate_advanced_caching.py" is a .py script that contains all caching functions and valid time for each cache. 















references:
1. https://www.nps.gov/state/al/index.htm
2. https://developers.google.com/places/web-service/search
3. https://plot.ly/python/scatter-plots-on-maps/
