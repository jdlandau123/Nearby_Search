from django.shortcuts import render
from .forms import MainForm
from .extras import GoogleSearchClient
from django.http import HttpResponseRedirect
import json

google_api_key = 'AIzaSyCIKytrO-G-U4y7u1b8Zv19rnsJIU2Ykfw'

# Create your views here.
def home(request):
    search_results = "No Search"

    if request.method == 'POST':
        form = MainForm(request.POST)

        if form.is_valid():
            a = form.cleaned_data['address']
            s = form.cleaned_data['search_query']

            client = GoogleSearchClient(api_key=google_api_key, address=a)

            searched_lat = client.lat
            searched_long = client.long

            search_results = client.search_nearby(text_query=s, radius=8000)

            geojs={
                "type": "FeatureCollection",
                "features":[
                    {
                            "type":"Feature",
                            "geometry": {
                                "type":"Point",
                                "coordinates":[res["geometry"]["location"]['lng'], res["geometry"]["location"]['lat']],
                            },
                            "properties":{
                                "name" : res["name"],
                                "rating" : res["rating"],
                                "vicinity" : res["vicinity"],
                                "business_status" : res["business_status"]
                            },
                    
                    } for res in search_results['results']
                ]
            }

            #return HttpResponseRedirect('map')
            return render(request, 'map.html', {
                "results" : search_results['results'], 
                "geojson" : json.dumps(geojs), 
                "searched_lat" : searched_lat,
                "searched_long" : searched_long
                }
            )

    else:
        form = MainForm()

    return render(request, 'home.html', {"results" : search_results, "form" : form})


def map(request):
    return render(request, 'map.html', {})