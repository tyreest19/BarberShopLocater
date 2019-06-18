from yelpapi import YelpAPI
import geonamescache
import json
import pprint
import csv
import requests
from  geopy.geocoders import Nominatim
geolocator = Nominatim()
def addToCSV(businesses, price):
    total_businesses = []
    for i in range(len(businesses['response']['groups'][0]['items'])):
        business = [
                      businesses['response']['groups'][0]['items'][i]['venue']['name'],
                      businesses['response']['groups'][0]['items'][i]['venue']['location']['formattedAddress'],
                      businesses['response']['groups'][0]['items'][i]['venue']['contact'],
                      '$'*price
                     ]
        total_businesses.append(business)
    print(total_businesses)
    for business in total_businesses:
        with open('barbershps.csv','a') as fd:
            wr = csv.writer(fd)
            wr.writerow(business)

def search_for_barbershops():
    count = 0
    gc = geonamescache.GeonamesCache()
    c = gc.get_cities()
    US_cities = [c[key]['name'] for key in list(c.keys())
                 if c[key]['countrycode'] == 'US']
    MY_API_KEY = "QAidGECI2mDDbvq4GFMttBHXbDn2oKtLx9EObssDfDroHh3KYKAp7VsMsHYvhLaITKsTI8lfFBd-SHNc5L1r9r5jFZzJi4QgVB2WN4r4ZydAmfg1XjV8eu1rNfYGXXYx" #  Replace this with your real API key
    yelp_api = YelpAPI(MY_API_KEY)
    US_longs = [c[key]['longitude'] for key in list(c.keys())
            if c[key]['countrycode'] == 'US']
    US_latts = [c[key]['latitude'] for key in list(c.keys())
            if c[key]['countrycode'] == 'US']
    cordinates = []
    for i in range(len(US_longs)):
        cordinates.append(str(US_latts[i]) + ', ' + str(US_longs[i]))
    for cordinate in cordinates:
        for price in range(1,5):
            url = 'https://api.foursquare.com/v2/venues/explore'
            # city =city
            # country ="US"
            # loc = geolocator.geocode(city+','+ country)
            params = dict(
              client_id='EMHDD2F3YG33S5YB045KVN4KWUWXKT44RWNYXTXNPRQ5CYW5',
              client_secret='NNML0EDYKT0TC50YDUHBENI04PL3WZLAYNIKL3QTSJHCY3SK',
              v='20180323',
              ll= cordinate,
              query='barbershop',
              # limit=20,
              price=str(price)
            )
            resp = requests.get(url=url, params=params)
            data = json.loads(resp.text)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(data)
            addToCSV(data, price)

def createCSV():
    with open('barbershps.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'Address', 'Contact', 'Price'])

if __name__ == '__main__':
    createCSV()
    search_for_barbershops()
