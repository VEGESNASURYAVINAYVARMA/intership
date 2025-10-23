from django.shortcuts import render

# Create your views here.
import requests


def get_weather(request):
    weather_data = None
    forecast_data = None
    if request.method == "POST":
        city = request.POST.get('city')
        api_key = "83ff6e1cee586adc93f48df7654c9a79"

        # Current weather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get('cod') == 200:
            weather_data = {
                'city': city.title(),
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'humidity': response['main']['humidity'],
                'icon': response['weather'][0]['icon']
            }

            
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            forecast_response = requests.get(forecast_url).json()
            forecast_data = forecast_response.get('list', [])[:5]  # Next 5 intervals

    return render(request, 'weather/weather.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data
    })
