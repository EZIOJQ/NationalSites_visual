# NationalSites_visual -------- Jieqing Chen
## Use plotly to visualize different naitonal sites in different states(Accept User Input).

### run "proj2_nps.py" and follow the instructions.
### caching files are "sample_cache_national_site.json" and "google_cache.json"
### caching files are named but you can change them by themselves.
### you may need to install BeautifulSoup4 and Plotly packages. You can use "pip3 install bs4" or "pip3 install plotly" to achieve that.
### make sure you have the google api key and add it into "secrets.py".

#### Each files have different functions:
1. alternate_advanced_caching.py is a .py script that contains all caching funcitons and the time of each cache. 
2. secrets.py is a file that needs you to input your google api key. To get a google api key, you can check this website https://developers.google.com/places/web-service/get-api-key  

#### An example to run:
1. run the proj2_nps.py, then choose which state you want to see. You should input like "list mi" or "list ca" for example.
2. It will give you a list of all national sites in this state, and you can simply use "map" command to get the plot of these sites on the map. A new popup website will show up.
3. If you want to get more information about the nearby places of this national site, you can input "nearby < index >". (The index number of which site you want to know more). 
4. it will give you a map contains all nearby places of this site.
5. Anytime you want to quit, input "exit". And anytime you need help, just input "help".















references:
1. https://www.nps.gov/state/al/index.htm
2. https://developers.google.com/places/web-service/search
3. https://plot.ly/python/scatter-plots-on-maps/
