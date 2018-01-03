# -*- coding: utf8 -*-
import telegram
import requests
import random
from transitions import State
from transitions.extensions import GraphMachine as mach
from bs4 import BeautifulSoup


bot = telegram.Bot(token='496063592:AAH9ux0XtCDTDQm2lANJE7Sg9F3SbQaiPFg')
actorURL = 'http://www.imdb.com/search/name?gender=male,female&ref_=nv_cel_m_3'
workURL = 'http://www.imdb.com/movies-in-theaters/?ref_=nv_tp_inth_1'

def actorIMDB():
	web = requests.get(actorURL)
	soup = BeautifulSoup(web.text, 'lxml')
	headerList = soup.find_all("h3", {"class": "lister-item-header"})
	picHeaderList = soup.find_all("div", {"class": "lister-item-image"})
	starlist = []
	nameList = []
	picList = []
	for item in headerList:
		starlist.append(item.find('a')['href'])
		temp = item.find('a').string
		nameList.append(temp[1:])
	for item in picHeaderList:
		picList.append(item.a.img['src'])
	return starlist, nameList, picList

def workIMDB():
	web = requests.get(workURL)
	soup = BeautifulSoup(web.text, 'lxml')
	headerList = soup.find_all("h4", {"itemprop": "name"})
	picHeaderList = soup.find_all("div", {"class": "hover-over-image zero-z-index"})
	worklist = []
	nameList = []
	picList = []
	for item in headerList:
		worklist.append(item.find('a')['href'])
		temp = item.find('a')['title']
		# tempcut = temp[1:]
		tempcut = temp.split('(')
		nameList.append(tempcut[0])
	for item in picHeaderList:
		picList.append(item.img['src'])
	return worklist, nameList, picList

class Engine(object):
	def intoInfo(self, replyid):
		infoText = 'hello! this is work_search bot. I can get you the information you want to know. You can find the information you\'re interested in, or i\'ll introduce you an actor or a movie.\nif you want to search by yourself, please use "search"\nif you want me to recommend, please use "recommend"' 
		bot.sendMessage(replyid, infoText)
	def intoInput(self, replyid):
		text = 'please enter the one you want to search'
		bot.sendMessage(replyid, text)
	def intoLangu(self, replyid, name):
		if (name[0] >= u'\u0041' and name[0] <=u'\u005a') or (name[0] >= u'\u0061' and name[0] <=u'\u007a'):
			name = name.replace(' ', '_')
			searchResult = 'en.wikipedia.org/wiki/'+name
			print('!!!!english!!!!')
		else:
			searchResult = 'zh.wikipedia.org/wiki/'+name
			print('!!!!chinese!!!!')
		text = 'Good! Now choose a language'
		markup = [
			[	
				{'text': 'chinese', 'callback_data': 'zh'+'+'+searchResult},
				{'text': 'english', 'callback_data': 'en'+'+'+searchResult}
			]
		]
		keyboard = {'inline_keyboard':markup}
		bot.sendMessage(replyid, text, reply_markup = keyboard)
	def intoResultZH(self, replyid, data):
		if(data[0:2] == 'en'):
			url = 'https://'+data;
			web = requests.get(url)
			soup = BeautifulSoup(web.text, 'lxml')
			temp = soup.find('li', {"class":"interlanguage-link interwiki-zh"})
			newURL = temp.a['href']
		else:
			newURL = 'https://'+data
		html = '<a href="'+newURL+'">'+'there you go</a>'
		bot.sendMessage(replyid, html, parse_mode=telegram.ParseMode.HTML)
	def intoResultEN(self, replyid, data):
		if(data[0:2] == 'zh'):
			url = 'https://'+data;
			web = requests.get(url)
			soup = BeautifulSoup(web.text, 'lxml')
			temp = soup.find('li', {"class":"interlanguage-link interwiki-en"})
			newURL = temp.a['href']
			print(temp)
		else:
			newURL = 'https://'+data
		html = '<a href="'+newURL+'">'+'there you go</a>'
		bot.sendMessage(replyid, html, parse_mode=telegram.ParseMode.HTML)
	def intoRecommendCat(self, replyid):
		text = 'What do you want me to recommend?'
		markup = [
			[	
				{'text': 'actor', 'callback_data': 'actor'},
				{'text': 'work', 'callback_data': 'work'}
			]
		]
		keyboard = {'inline_keyboard':markup}
		bot.sendMessage(replyid, text, reply_markup = keyboard)
	def intoActorResult(self, replyid):
		myUrlList, actorNameList, picList = actorIMDB()
		length = len(myUrlList)
		ran = random.randint(0,length-1)
		picUrl = picList[ran]
		newURL = 'http://www.imdb.com/' + myUrlList[ran]
		html = '<a href="'+newURL+'">'+'there you go</a>'
		bot.sendPhoto(replyid, picUrl)
		bot.sendMessage(replyid, html, parse_mode=telegram.ParseMode.HTML)
		text = 'would you like to take a look at his/hers wiki page?'
		yesCallback = 'yes' + '+' + actorNameList[ran]
		markup = [
			[	
				{'text': 'Yes' , 'callback_data': yesCallback},
				{'text': 'No', 'callback_data': 'no'}
			]
		]
		keyboard = {'inline_keyboard':markup}
		bot.sendMessage(replyid, text, reply_markup = keyboard)
	def intoWorkResult(self, replyid):
		myUrlList, workNameList, picList = workIMDB()
		length = len(myUrlList)
		ran = random.randint(0,length-1)
		picUrl = picList[ran]
		newURL = 'http://www.imdb.com/' + myUrlList[ran]
		html = '<a href="'+newURL+'">'+'there you go</a>'
		bot.sendPhoto(replyid, picUrl)
		bot.sendMessage(replyid, html, parse_mode=telegram.ParseMode.HTML)
		text = 'would you like to take a look at its wiki page?'
		yesCallback = 'yes' + '+' + workNameList[ran]
		markup = [
			[	
				{'text': 'Yes' , 'callback_data': yesCallback},
				{'text': 'No', 'callback_data': 'no'}
			]
		]
		keyboard = {'inline_keyboard':markup}
		bot.sendMessage(replyid, text, reply_markup = keyboard)