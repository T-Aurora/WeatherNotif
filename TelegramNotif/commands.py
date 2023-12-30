import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from ApiHandler import WeatherCall
import re
import requests
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to WeatherNotify, type /help for assistance.")
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
        "Es. /sub Catania RAIN Tempmax:30 Tempmin:20"
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
                if 'tempmax' in text.lower():
                    temp.append(re.findall(r'\d+', text))
                if 'rain' in text.lower():
                    rain = True
                await context.bot.send_message(chat_id=update.effective_chat.id, text="your sub: "+text)
                content += str(text)+'\n'
            print(update.effective_user.full_name)
            print(update.effective_chat.id)
            print(content)

            # region

            url = 'http://wnotif:5000/add_user'
            data = {
                'nome': update.effective_user.full_name,
                'chat_id': update.effective_chat.id,
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print('gg funza')
            else:
                print('Error info for add:', response.status_code, response.text)

            #2'endpoit

            user_id = requests.post('http://wnotif:5000/find_user', data=data)
            t=re.findall(r'\d+',str(user_id.text))
            sub_data = {
                'user_id': t, #sicuro sbaglio
                'locazione': text_c[0],  #continuo a consider 0 la citta come su check
                't_max': (max(temp)) if temp else None,
                't_min': (min(temp)) if temp else None,
                'w_condition': 'rain' if rain else None #in caso metterne altri
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

            print(str(max(temp))+" "+str(min(temp)))

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
                message += f"- {sub['locazione']}: {sub['t_min']} - {sub['t_max']} - {sub['w_condition']}\n"
        else:
            message = "You have no subscriptions."
    else:
        message = "Failed to retrieve subscriptions."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
