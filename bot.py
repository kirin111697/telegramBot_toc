# -*- coding: utf8 -*-
import sys
import telegram	
from flask import Flask, request
from transitions import State
from transitions.extensions import GraphMachine as Machine
from fsm import Engine

app = Flask(__name__)
bot = telegram.Bot(token='496063592:AAH9ux0XtCDTDQm2lANJE7Sg9F3SbQaiPFg')

states = ['startUp','infoPage','input','language','recommendCat', 'actorResult','workResult', 'resultEN', 'resultZH']
transitions = [
		['info', 'startUp', 'infoPage'],
		['search', 'startUp', 'input'],
		['namein', 'input','language'],
		['CH', 'language', 'resultZH'],
		['EN', 'language', 'resultEN'],
		['back', ['resultZH', 'resultEN'], 'input'],
		['recommend', 'startUp', 'recommendCat'],
		['people','recommendCat', 'actorResult'],
		['work', 'recommendCat', 'workResult'],
		['yes', ['actorResult', 'workResult'], 'resultEN'],
		['resumeRecommend', 'resultEN', 'recommendCat'],
		['no', ['actorResult', 'workResult'], 'recommendCat'],
		['restart', '*', 'startUp']
	]


movie_bot = Engine()
machine = Machine(model = movie_bot, states = states, transitions = transitions, initial = 'startUp', ignore_invalid_triggers = True, title = 'movie_search')

def _set_webhook():
	status = bot.set_webhook('https://435325fe.ngrok.io/hook')
	if not status:
		print('webhook set up failed')
		sys.exit(1)

def welcome(update):
	text = 'hello! pick a function please'
	markup = [
		[	
			{'text': 'info', 'callback_data': 'info'},
			{'text': 'search', 'callback_data': 'search'},
			{'text': 'recommend', 'callback_data': 'recommend'}
		]
	]
	keyboard = {'inline_keyboard':markup}
	update.message.reply_text(text, reply_markup = keyboard)

def on_update_recieve(update):

	callback_query = update.callback_query
	if callback_query:
		#print(update)
		id = callback_query.id
		data = callback_query.data
		replyid = callback_query.message.chat.id
		text = 'got cha'
		datacut = data.split('+')
		bot.answerCallbackQuery(id, text)
		if(data == 'info'):
			movie_bot.info(replyid)
			movie_bot.to_startUp()
			text = 'hello! pick a function please'
			markup = [
				[	
					{'text': 'info', 'callback_data': 'info'},
					{'text': 'search', 'callback_data': 'search'},
					{'text': 'recommend', 'callback_data': 'recommend'}
				]
			]
			keyboard = {'inline_keyboard':markup}
			bot.sendMessage(replyid, text, reply_markup = keyboard)
		elif(data == 'search'):
			movie_bot.search(replyid)
		elif(datacut[0] == 'zh'):
			movie_bot.CH(replyid,datacut[1])
			movie_bot.back(replyid)
			#movie_bot.to_input(replyid)
		elif(datacut[0] == 'en'):
			movie_bot.EN(replyid,datacut[1])
			movie_bot.back(replyid)
			#movie_bot.to_input(replyid)
		elif(data == 'recommend'):
			movie_bot.recommend(replyid)
		elif(data == 'actor'):
			movie_bot.people(replyid)
			#movie_bot.to_recommendCat(replyid)
		elif(data == 'work'):
			movie_bot.work(replyid)
			#movie_bot.to_recommendCat(replyid)
		elif(datacut[0] == 'yes'):
			#bot.sendMessage(replyid, datacut[1])
			datacut[1] = datacut[1].replace(' ', '_')
			link = 'en.wikipedia.org/wiki/'+datacut[1]
			movie_bot.yes(replyid, link)
			movie_bot.resumeRecommend(replyid)
		elif(datacut[0] == 'no'):
			movie_bot.no(replyid)
			
	else:
		text = update.message.text
		replyid = update.message.chat.id
		if(text[0:6] == '/start'):
			welcome(update)
		elif(text[0:8] == '/restart'):
			movie_bot.restart()
			welcome(update)
		else:
			movie_bot.namein(replyid, text)


@app.route('/hook', methods=['POST'])
def message():
	if request.method == "POST":
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		on_update_recieve(update)
	return 'ok'

if __name__ == '__main__':
	_set_webhook()
	#print(movie_bot.states)
	machine.on_enter_infoPage('intoInfo')
	machine.on_enter_input('intoInput')
	machine.on_enter_language('intoLangu')
	machine.on_enter_resultZH('intoResultZH')
	machine.on_enter_resultEN('intoResultEN')
	machine.on_enter_recommendCat('intoRecommendCat')
	machine.on_enter_actorResult('intoActorResult')
	machine.on_enter_workResult('intoWorkResult')
	movie_bot.get_graph().draw('fsm.png', prog = 'dot')
	app.run(port = 8888)
