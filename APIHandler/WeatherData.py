import requests

api_key = "5a1444c1a11acc778f427f66f87e5eea"
def fetch_weather_data(city):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("City not found", response.status_code)
        return None