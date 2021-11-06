from django.shortcuts import get_object_or_404, redirect, render
import requests
from decouple import config
from .models import City
from pprint import pprint
from django.contrib import messages

def index(request):
    cities = City.objects.all()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    
    g_city = request.GET.get('name')
    print('g_city:',g_city)
    if g_city:
        response = requests.get(url.format(g_city, config('API_KEY')))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            a_city = content['name']
            if City.objects.filter(name =a_city):
                messages.warning(request,"City already exists")
            else:
                City.objects.create(name = a_city)
                messages.success(request,'Successfully added')
        else:
            messages.warning(request,'City doesnt exist!')
        return redirect('home')
    city_data = []
    for city in cities:
        # print(city)
        response = requests.get(url.format(city, config('API_KEY')))
        content = response.json()
        pprint(content)
        data = {
            "city":city,
            "temp": content["main"]["temp"],
            "desc": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"],
        }
        city_data.append(data)
    context = {
            "city_data":city_data
            }
        
        
    # print(city_data)
    return render(request, 'weather_app/index.html', context)

def delete_city(request, id):
    city = get_object_or_404(City, id =id)
    city.delete()
    return redirect('home')