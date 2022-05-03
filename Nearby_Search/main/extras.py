import googlemaps
from urllib.parse import urlencode
import requests

google_api_key = 'AIzaSyCIKytrO-G-U4y7u1b8Zv19rnsJIU2Ykfw'

class GoogleSearchClient(object):
    api_key = None
    lat = None
    long = None
    address_query = None
    text_query = None
    radius = None

    def __init__(self, api_key=None, address=None):
        #super().__init__()
        if api_key == None:
            raise Exception("API Key is required")

        self.api_key = api_key
        self.address_query = address

        if self.address_query != None:
            self.lat, self.long = self.geocode_address()

    def geocode_address(self):
        gmaps = googlemaps.Client(key=self.api_key)

        geocode_result = gmaps.geocode(self.address_query)

        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        return lat, lng

    def search_nearby(self, text_query=None, radius=None):
        self.text_query = text_query
        self.radius = radius

        nearby_search_base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

        params = {
            "key" : self.api_key,
            "location" : f"{self.lat},{self.long}",
            "keyword" : self.text_query,
            "radius" : self.radius
        }
        url_params = urlencode(params)
        url_endpoint = f"{nearby_search_base_url}?{url_params}"
        response = requests.get(url_endpoint)

        return response.json()