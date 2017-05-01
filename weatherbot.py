# -*- coding: utf-8 -*-

import sys
from time import sleep
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
from os import path
import traceback
from pyowm import OWM

"""
Setup the bot
"""
TOKEN = <TOKEN>
OWMKEY = <APIKEY>

def process_message(bot, u):
	keyboard = [['Get Weather']]
	reply_markup = ReplyKeyboardMarkup.create(keyboard)
	if u.message.sender and u.message.text and u.message.chat:
		chat_id = u.message.chat.id
		user = u.message.sender.username
		message = u.message.text
		print chat_id
		print message
		
		"""
		Use a custom keyboard
		"""
		
		
		if message == 'Get Weather':
			bot.send_message(chat_id, 'please send me your location')
		else:
			bot.send_message(chat_id, 'please select an option', reply_markup=reply_markup).wait()
		
		
	elif u.message.location:
		print u.message.location
		chat_id = u.message.chat.id
		owm = OWM(OWMKEY)
		obs = owm.weather_at_coords(u.message.location.latitude, u.message.location.longitude)
		w = obs.get_weather()
		print(w)                      # <Weather - reference time=2013-12-18 09:20,  status=Clouds>
		l = obs.get_location()
		bot.send_message(chat_id, 'Weather Status: ' +str(w.get_detailed_status()) +' At '+str(l.get_name())+' '+str(w.get_reference_time(timeformat='iso'))+' Temperature: '+str(w.get_temperature('celsius').get('temp'))+ 'C')
		bot.send_message(chat_id, 'please select an option', reply_markup=reply_markup).wait()
	else:
		print u
		bot.send_message(chat_id, 'please select an option', reply_markup=reply_markup).wait()
	
bot = TelegramBot(TOKEN)
bot.update_bot_info().wait()
print bot.username
last_update_id = 0
while True:
	updates = bot.get_updates(offset = last_update_id).wait()

	try:
		for update in updates:
            		if int(update.update_id) > int(last_update_id):
                		last_update_id = update.update_id
                		process_message(bot, update)
                		continue
		continue
	except Exception:
        	ex = None
        	print traceback.format_exc()
        	continue
