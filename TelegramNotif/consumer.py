import os
import logging
from venv import logger
from confluent_kafka import Consumer, KafkaError
import json
from telegram import Update, Bot
class WConsumer:
    bot =Bot('6901556645:AAEqTL9k2TeoIosTx9i8li_ItVZpvUqtb3E')
    c = Consumer({'bootstrap.servers': 'kafka',
                  'group.id': os.getenv('GROUP_ID', '1'),
                  'enable.auto.commit': 'true',
                  'auto.offset.reset': 'latest'  # 'auto.offset.reset=earliest' to start reading from the beginning
                  })
    c.subscribe(['WAlerts']) ###NOME DEL TOPIC

    async def k_consumer(self):
        try:
                msg = self.c.poll(timeout=5)
                if msg is None:
                    print("Waiting for message or event/error in poll()")
                    #continue
                #continuo a lasciare in ascolto, errore che indica indica che il consumatore ha raggiunto la fine di una partizione. end of partition"
                elif msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('error: {}'.format(msg.error()))
                        #continue
                    else:
                        logging.error('error: {}'.format(msg.error()))
                        print('error: {}'.format(msg.error()))
                else:
                    # Check for Kafka message
                    chat_id = msg.key()
                    record_value = msg.value()
                    data = json.loads(record_value)
                    cont = ''
                    #da es se la chiave 'count' non è presente nei dati, restituisce 0 come valore predefinito
                    # Invia una risposta al bot
                    if "min_temp" in data:
                        cont += str(data['min_temp'])+'\n'
                    if "max_temp" in data:
                        cont += str(data['max_temp'])+'\n'
                    if "rain" in data:
                        cont += str(data['rain'])+'\n'
                    chat_id_str = chat_id.decode('utf-8') #funzionaaaa
                    logging.info("Consumed record with key {} and value {}".format(chat_id_str, record_value))
                    response_message = "Your info on {} are:\n{}".format(data['city'], cont)

                    print(f"Sending se spera message to chat_id {chat_id_str}: {response_message}")

                    try:
                        await self.bot.send_message(chat_id=chat_id_str, text=response_message)
                        logger.info(f"Message sent to chat_id {chat_id_str}: {response_message}")
                    except Exception as e:
                        logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
                        print(f"FALLIU: {e}")

        except KeyboardInterrupt:
            self.c.close()
        finally:
            pass
            # Leave group and commit final offsets
            #self.c.close()
