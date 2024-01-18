import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from ApiHandler import WeatherCall
import re
import requests
from main import user_link

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check= user_link.link_user(update.effective_user.username,update.effective_user.id)
    if check== "200":
        print("User linked: "+update.effective_user.username+" "+str(update.effective_user.id))
    else:
        print("User already linked")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome"+update.effective_user.username+" to WeatherNotify, type /help for assistance.")
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "This bot can help you with the following commands:\n"
        "/start - Start a conversation.\n"
        "/help - Show this help message.\n"
        "/sub - Use this command specifying the city and your alerts\n"
        "/alert - List of possible alerts\n"
        "/show_sub -Shows the list of subscriptions made "
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Possible weather alerts:\n"
        "Rain - alert the user when it's gonna rain\n"
        "Tempmax:value - alert the user when the temp reaches value.\n"
        "Tempmin:value - same as before\n"
        "PSA alerts are not case sensitive\n"
        "Es. /sub Catania Rain Tempmax:30 Tempmin:20"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)
async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_c = context.args
    temp = list()
    rain = False
    content = ''
    if len(text_c) <=4:
        if WeatherCall(text_c[0])['cod'] != '404':
            for text in text_c:
                print("in sub Text city:", text)
                if 'temp' in text.lower():
                    temp.append(re.findall('[0-9]+', text))
                    print("in sub temp",temp)
                if 'rain' in text.lower():
                    rain = True
                await context.bot.send_message(chat_id=update.effective_chat.id, text="your sub: "+text)
                content += str(text)+'\n'
            print("in sub full name",update.effective_user.full_name)
            print("in sub chat.id",update.effective_chat.id)
            print("in sub full name",content)

            # region
            url = 'http://wnotif:5000/add_user'
            data = {
                'nome': update.effective_user.full_name,
                'username': update.message.from_user.username,
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print('status==200')
            else:
                print('Error info for add:', response.status_code)
                # print('Error info for add:', response.status_code, response.text)

            #2'endpoit

            user_id = requests.post('http://wnotif:5000/find_user', data=data)
            t=re.findall(r'\d+',str(user_id.text))
            sub_data = {
                'user_id': t,
                'locazione': text_c[0],
                't_max': (max(temp)) if temp else None,
                't_min': (min(temp)) if temp else None,
                'w_condition': 'rain' if rain else None
            }
            for key, value in sub_data.items():
                if value == '':
                 sub_data[key] = None

            sub_response = requests.post('http://wnotif:5000/add_subb', data=sub_data)
            if sub_response.status_code == 200:
                print('Subscription added')
            else:
                print('Error info for sub:', sub_response.status_code, sub_response.text)

            # endregion
            print(str(max(temp)) + " " + str(min(temp)))
            #key = 'WeatherSubscription from user: '+update.effective_user.full_name

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="city not found!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="too many arguments for the sub command!")





async def show_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(chat_id)
    sub_response = requests.post('http://wnotif:5000/show_sub', data={'chat_id': chat_id})

    if sub_response.status_code == 200:
        subscriptions = sub_response.json()
        if subscriptions:
            message = "Your subscriptions:\n"
            for sub in subscriptions:
                message += f"- {sub['locazione']}: min: {sub['t_min']} - max: {sub['t_max']} - Condition: {sub['w_condition']}\n"
        else:
            message = "You have no subscriptions."
    else:
        message = "Failed to retrieve subscriptions."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

