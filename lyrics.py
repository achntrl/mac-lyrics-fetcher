#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
from search import *
from bs4 import BeautifulSoup
import requests
import time
import codecs

song_playing = ""
while True:
	# Apple script that gives info on the song currently playing
	raw_data = os.popen('osascript itunes.scpt').read().split('\n')

	# Pre-treatmeant of data
	if raw_data[0] != '-1':
		raw_data[2] = raw_data[2].replace(',', '.') # Convert time from French to US notation
		raw_data[3] = raw_data[3].replace(',', '.')
		raw_data [4] = float(raw_data[2])/float(raw_data[3])
	else:
		print "No song playing"
		exit(0)

	# Scrape Genius.com to retrieve lyrics
	title=raw_data[0]
	artist= raw_data[1]
	progression = raw_data[4] # To be used to display the right portion of the screen
	search_terms = artist + " " + title

	if song_playing != search_terms:
		# To avoid looking for lyrics everytime we store them offline in a textfile 
		FILENAME = "offline/"+search_terms+".txt"
		if os.path.isfile(FILENAME):
			with open(FILENAME, 'r') as file:
				print file.read()
		else:
			client_id, client_secret, client_access_token = load_credentials()
			song_url = search(search_terms, client_access_token)
			response = requests.get(song_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
			soup = BeautifulSoup(response.text, "lxml")
			html = soup.find(class_="lyrics").find_all('p')
			# Sometimes, there is something above or below the lyrics
			# We retrieve the longest string as we can guess it's the lyrics
			index_maxlen = 0
			tmp = 0
			for index in range(len(html)):
				if len(html) > tmp:
					tmp = len(html[index].get_text())
					index_maxlen = index
			lyrics = html[index_maxlen].get_text()
			print lyrics
			with codecs.open(FILENAME, 'ab', encoding='utf8') as file:
				file.write(lyrics)

		song_playing = search_terms
		print "\n\n---------- END OF SONG LYRICS ------------\n\n\n"

	time.sleep(5)



