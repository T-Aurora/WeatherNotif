import json
import os

from RedisCache import RedisCache
import requests
#DATA SCRAPING
def process_subs(redis):
    'http://wnotif:5000/all_sub'
    sub_response = requests.get('http://'+os.getenv('APIHOST','localhost')+':5000/all_sub')
    if sub_response.status_code==200:
        #sub_response.raise_for_status()    stato divers da 200
        try:
            subs_list = sub_response.json()
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None
        for sub in subs_list:
            cond = False
            sub_city = sub.get('city')
            weather_data = redis.get_cached_weather(sub_city)
            print(weather_data)
            msg_data={'city': sub_city, 'user_id': sub.get('user_id')}
            w_condition = sub.get('w_condition') # così se è assente lo prende come none
            main_weather = weather_data.get('weather', [{}])[0].get('main','').lower() #uso main cosi che volendo almeno su doc possiamo gestire altri costr
            if w_condition == 'rain' and main_weather == 'rain':#??? mette sia id che testo, posso cambiare cmq
                msg_data['rain'] = "It's gonna rain"
                cond = True
                print(f"Condition 1: {w_condition == 'rain' and main_weather == 'rain'}") #boh non capisco sto controllo perché controlli due cose che prendi dalla stessa cosa
            temp_max = sub.get('t_max')
            temp_min = sub.get('t_min')
            if temp_max is not None and 'temp_max' in weather_data.get('main', {}):
                if temp_max <= weather_data['main']['temp_max']:
                    msg_data['max_temp'] = 'the temperature is going to get as high as: ' + str(weather_data['main']['temp_max'])
                    cond = True
                    print(f"Condition 2: {temp_max and temp_max <= weather_data['main']['temp_max']}")
            if temp_min is not None and 'temp_min' in weather_data.get('main', {}):
                if temp_min >= weather_data['main']['temp_min']:
                    msg_data['min_temp'] = 'the temperature is going to get as low as: ' + str(weather_data['main']['temp_min'])
                    cond = True
                    print(f"Condition 3: {temp_min and temp_min >= weather_data['main']['temp_min']}")
            if cond:
                record_value = json.dumps(msg_data)
                print("record_value", record_value)
                return record_value
                # Pubb il messaggio sul topic
            else:
                return None
    else:
        print(f"Error during request:", sub_response.status_code)


"""msg_data={'city': sub_city, 'user_id': sub.get('user_id')}
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
                # Pubb il messaggio sul topic"""


"""   msg_data={'city': sub_city, 'user_id': sub.get('user_id')}

            w_condition = sub.get('w_condition') # così se è assente lo prende come none
            #and weather_data['weather'][0]['id'] == 500:
            if w_condition == 'rain' and weather_data.get('weather', [{}])[0].get('id') == 500:
                msg_data['rain'] = "It's gonna rain"
                cond = True
                print(f"Condition 1: {sub.w_condition == 'rain' and weather_data['weather'][0]['id'] == 500}")
           #sub.t_max<= weather_data['main']['temp_max']:
            if sub.get('t_max') and sub.get('t_max') <= weather_data.get('main', {}).get('temp_max'):
                #msg_data['max_temp'] = 'the temperature is going to get as high as: ' + str(weather_data['main']['temp_max'])
                msg_data['max_temp'] = 'the temperature is going to get as high as: ' + str(weather_data.get('main', {}).get('temp_max'))
                cond = True
                print(f"Condition 2: {sub.get('t_max') and sub.get('t_max') <= weather_data.get('main', {}).get('temp_max')}")

            #print(f"Condition 2: {sub.t_max and sub.t_max <= weather_data['main']['temp_max']}")
            #if sub.t_min and sub.t_min >= weather_data['main']['temp_min']:
            if sub.get('t_min') and sub.get('t_min') >= weather_data.get('main', {}).get('temp_min'):
                #msg_data['min_temp'] = 'the temperature is going to get as low as: ' + str(weather_data['main']['temp_min'])
                msg_data['min_temp'] = 'the temperature is going to get as low as: ' + str(weather_data.get('main', {}).get('temp_min'))
                cond = True
                #print(f"Condition 3: {sub.t_min and sub.t_min >= weather_data['main']['temp_min']}")
                print(f"Condition 3: {sub.get('t_min') and sub.get('t_min') >= weather_data.get('main', {}).get('temp_min')}")

            if cond:
                record_value = json.dumps(msg_data)
                print("record_value", record_value)
                return record_value
                # Pubb il messaggio sul topic"""