import requests
"""key open meteo: 5a1444c1a11acc778f427f66f87e5eea"""
def WeatherCall(city):
    api_key = "5a1444c1a11acc778f427f66f87e5eea"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    print(data)
    return data



