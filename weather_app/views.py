from django.shortcuts import render
from django.contrib import messages
import datetime
import requests

# Create your views here.
def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'gujarat'

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=f05928315193f6f8d98caf591e40b00d"
    PARAMS = {'units' : 'metric'}

    API_KEY  = "AIzaSyBy9Dm84C17_3JiuSlqB4gCMibXJmasVyc"
    SEARCH_ENGINE_ID = "63f163dbcbb9c4e37"

    query = f"{city} 1920x1080"
    page = 1
    start = (page-1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url = search_items[1]['link']

    
    try:
        data = requests.get(url,PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'app/index.html', {'description' : description, 'icon' : icon, 'temp' : temp, 'day' : day, 'City' : city,'image_url': image_url, 'exception_occurred':False})

    except KeyError:
        exception_occurred = True
        messages.error(request,'Entered data is not available to API') 

        day = datetime.date.today()

        return render(request, 'app/index.html', {'description' : 'clear sky', 'icon' : '01d', 'temp' : 25, 'day' : day, 'City' : 'Gujarat','image_url': image_url, 'exception_occurred':exception_occurred}) 