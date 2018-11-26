#################################
'''
            ******* CHALLENGE #1 ********
    Polling in Real Time: The 2018 Midterm Elections

Task: Scrape the statistics for the midterms that NYT is currently tracking

0. Set up a cache
1. Get the number of calls made so far
2. Create a list called `current_races`
3. For each race that the NYT is currently tracking save the following in a list:
    1. type string :: Race id
    2. type string :: Race location
    3. type string :: Race summary
    4. type string :: Democratic candidate name
    5. type string :: percent democratic candidate
    6. type string :: Republicam candidate name
    7. type string :: percent republican candidate
    8. type string :: Undecided candidate name
    9. type string :: percent undecided
4. For each list representing (2), append to the `current_races` list
5. Print the following for each element in `current_race`:
    """ DEM:{} {} :: REP: {} {} :: UNDECIDED: {}""".format(
        "democratic candidate", "percent democrat",
        "republican candidate", "percent republican",
        "percent undecided"
    ))
'''
#################################

from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime

##############
# SETTING UP #
##############




def create_id(site, topic):
    return "{}_{}_{}.json".format(site, topic, str(datetime.now()).replace(' ', ''))

def process(response):
    ## use the `response` to create a BeautifulSoup object
    soup = BeautifulSoup( response, 'html.parser')
    sections = soup.find('main', class_="svelte-jghoej").find_all('section')
    #SECTION 1
    #Hear I used the lambda, map, list, and join method to decrease code generation
    # This '\' is used to continue code on a newline without spaces
    counts = int("".join(map(str,list(map(lambda x: x.text,\
     sections[0].find('span', class_="outer").find_all('span'))))))
    # I could have also written it like this:
    '''
    numbers = sections[0].find('span', class_="outer").find_all('span')
    count_list = []
    for i in numbers:
        count.append(i.text)
    count = int("".join(map(str,count)) # Cast as an integer

    '''
    #SECTION 3
    current_races = []
    races = sections[2].find_all('div', class_='race')
    for race in races:
        id = race.find('span', class_='race-link').text
        location = race.find('span', class_='place').text
        summary = race.find('span', class_='summary').text
        dem_can = race.find('div', class_='dem').find('span', class_='candidate').text
        dem_per = race.find('div', class_='dem').find('span', class_='percent').text
        rep_can= race.find('div', class_='rep').find('span', class_='candidate').text
        rep_per = race.find('div', class_='rep').find('span', class_='percent').text
        und_can= race.find('div', class_='und').find('span', class_='candidate').text
        und_per = race.find('div', class_='und').find('span', class_='percent').text
        temp = [id, location,summary, dem_can, dem_per, rep_can, rep_per, und_can, und_per]
        current_races.append(temp)
    for i in current_races:
        print(""" DEM:{} {} :: REP: {} {} :: UNDECIDED: {}""".format(
                i[3], i[4],
                i[5], i[6],
                i[8]
            ))

    #A QUESTION FOR YOU:
    #1. Could you simplify this code? Try it?
###################
#     CONFIG      #
###################
cache_file = "nyt.json"
site="nyt"
topic="polls"
cache = Cache(cache_file)
base = "https://www.nytimes.com/interactive/2018/upshot/elections-polls.html?action=click&module=Spotlight&pgtype=Homepage"


#######################
#     RUN PROGRAM     #
#######################
UID = create_id(site, topic)
response = cache.get(UID)

if response == None:
    response = requests.get(base).text
    cache.set(UID, response, 1)

process(response)
