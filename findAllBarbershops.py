from yelpapi import YelpAPI
import geonamescache
import json
import pprint
import csv
def addToCSV(businesses):
    total_businesses = [
                        [
                            business['name'],
                            business['location']['city'],
                            business['location']['state'],
                            business['phone'],
                            business['rating'],
                            business['price']
                        ]
                        for business in businesses
                        ]
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
    for city in US_cities:
        for i in range(1,5):
            search_results = yelp_api.search_query(term='barber shop', location={
                    "city": city
                  }, price=i)
            count += 1
            businesses = search_results['businesses']
            addToCSV(businesses)
            print(count, 'When do i break')


def createCSV():
    with open('barbershps.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'City', 'State', 'PhoneNumber', 'Rating', 'Price'])

if __name__ == '__main__':
    createCSV()
    search_for_barbershops()
