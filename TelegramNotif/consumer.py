import os
import socket
import sys
import logging
from venv import logger
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from telegram import Update, Bot
from UserLinker import RedisLink

user_link = RedisLink(os.getenv('REDIS_HOST','localhost'),os.getenv('REDIS_PORT','6379'),os.getenv('REDIS_DB','1'))
class WConsumer:
    def __init__(self, token_bot, bootstrap_server, group_id):
        self.token_bot = token_bot
        try:
            self.kafka_consumer = Consumer({'bootstrap.servers': bootstrap_server,
                                                'group.id': os.getenv('GROUP_ID', 1),
                                                'enable.auto.commit': 'true',
                                                'auto.offset.reset': 'latest'  # 'auto.offset.reset=earliest' to start reading from the beginning
                                                })

            self.bot = Bot('6901556645:AAEqTL9k2TeoIosTx9i8li_ItVZpvUqtb3E')

            self.kafka_consumer.subscribe(['WAlerts']) ###NOME TOPIC
        except KafkaException as e:
            if e.args[0].code() in (socket.errno.ECONNREFUSED,):
                print("Connection refused. Please check your Kafka broker.")
                sys.exit(1)
    async def k_consumer(self):
        try:
                msg = self.kafka_consumer.poll(timeout=15)
                if msg is None:
                    print("Waiting for message or event/error in poll()")
                    #continue
                elif msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('error: {}'.format(msg.error()))
                        #continue
                    else:
                        logging.error('error: {}'.format(msg.error()))
                        print('error: {}'.format(msg.error()))
                else:
                    # Check for Kafka message
                    record_value = msg.value()
                    data = json.loads(record_value)
                    print(data)
                    chat_id = user_link.find_user(data['username'])
                    cont = ''
                    #da es se la chiave 'count' non è presente nei dati, restituisce 0 come valore predefinito
                    # Invia una risposta al bot
                    if "min_temp" in data:
                        cont += str(data['min_temp'])+'\n'
                    if "max_temp" in data:
                        cont += str(data['max_temp'])+'\n'
                    if "rain" in data:
                        cont += str(data['rain'])+'\n'
                    #con user_id togliere chat_id
                    chat_id_str = chat_id.decode('utf-8')
                    logging.info("Consumed record with key {} and value {}".format(chat_id_str, record_value))
                    response_message = "Your info on {} are:\n{}".format(data['city'], cont)
                    print(f"Sending message to chat_id {chat_id_str}: {response_message}")
                    try:
                        await self.bot.send_message(chat_id=chat_id_str, text=response_message)
                        logger.info(f"Message sent to chat_id {chat_id_str}: {response_message}")
                    except Exception as e:
                        logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
                        print(f"Fail: {e}")

        except KeyboardInterrupt:
            self.kafka_consumer.close()
        finally:
            pass
            #self.c.close()
