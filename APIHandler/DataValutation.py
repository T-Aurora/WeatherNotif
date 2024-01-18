import json
from RedisCache import RedisCache
import requests
#DATA SCRAPING
def process_subs(redis):
    sub_response = requests.get('http://wnotif:5000/all_sub')
    try:
        sub_response.raise_for_status()  #  stato divers da 200
        subs_list = sub_response.json()
        for sub in subs_list:
            cond = False
            sub_city = sub.get('city')
            weather_data = redis.get_cached_weather(sub_city)
            print(weather_data)
            msg_data={'city': sub_city, 'user_id': sub.get('user_id')}
            if sub.w_condition == 'rain' and weather_data['weather'][0]['id'] == 500:
                msg_data['rain'] = "It's gonna rain"
                cond = True
                print(f"Condition 1: {sub.w_condition == 'rain' and weather_data['weather'][0]['id'] == 500}")
            if sub.t_max and sub.t_max <= weather_data['main']['temp_max']:
                msg_data['max_temp'] = 'the temperature is going to get as high as: ' + str(weather_data['main']['temp_max'])
                cond = True
                print(f"Condition 2: {sub.t_max and sub.t_max <= weather_data['main']['temp_max']}")
            if sub.t_min and sub.t_min >= weather_data['main']['temp_min']:
                msg_data['min_temp'] = 'the temperature is going to get as low as: ' + str(weather_data['main']['temp_min'])
                cond = True
                print(f"Condition 3: {sub.t_min and sub.t_min >= weather_data['main']['temp_min']}")
            if cond:
                record_value = json.dumps(msg_data)
                print("record_value", record_value)
                return record_value
                # Pubb il messaggio sul topic
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        print(e.response.status_code)





