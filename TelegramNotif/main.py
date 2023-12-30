""""6901556645:AAEqTL9k2TeoIosTx9i8li_ItVZpvUqtb3E
Keep your token secure """
import logging
from telegram.ext import ApplicationBuilder, ContextTypes,JobQueue, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
import commands
import threading
import requests
from aiohttp import web
import asyncio
from consumer import WConsumer
token = '6901556645:AAEqTL9k2TeoIosTx9i8li_ItVZpvUqtb3E'
logging.basicConfig( #modulo di logging per error checking
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
c = WConsumer()
async def k_consumer_job(job_queue):
    await c.k_consumer()
def main():
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', commands.start)
    sub_handler = CommandHandler('sub', commands.sub)
    help_handler = CommandHandler('help', commands.help)
    alert_handler = CommandHandler('alert', commands.alert)
    show_sub_handler = CommandHandler('show_sub', commands.show_sub)
    unknown_handler = MessageHandler(filters.COMMAND, commands.unknown)
    application.add_handler(start_handler)
    application.add_handler(sub_handler)
    application.add_handler(help_handler)
    application.add_handler(alert_handler)
    application.add_handler(show_sub_handler)
    application.add_handler(unknown_handler)
    #application.run_polling()
    job_queue = application.job_queue
    # Aggiungi un job periodico per eseguire il consumatore Kafka
    job_queue.run_repeating(k_consumer_job, 30)
    # Avvia l'applicazione Telegram
    application.run_polling()




if __name__ == '__main__':
    main()
    """
    p = requests.get('http://127.0.0.1:5000/start_producer')
    print("Kafka consumer running in the background...")
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', commands.start)
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), commands.echo)
    sub_handler = CommandHandler('sub',commands.sub)
    help_handler = CommandHandler('help', commands.help)
    alert_handler = CommandHandler('alert', commands.alert)
    unknown_handler = MessageHandler(filters.COMMAND, commands.unknown)
    application.add_handler(start_handler)
    application.add_handler(sub_handler)
    #application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(alert_handler)
    application.add_handler(unknown_handler)
    application.run_polling()

"""
