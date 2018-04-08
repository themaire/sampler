#!/usr/bin/env python3m
# -*- coding: utf-8 -*-

# By Nicolas ELIE
# twitter : nico@themaire

# 2018/03

##### Modules #####
import locale
locale.setlocale(locale.LC_TIME,'')

from time import sleep

import psutil

from flask import Flask, render_template, request, make_response
app = Flask(__name__)

import os
import pygame.mixer
from pygame.mixer import Sound

from gtts import gTTS # Voice synthetiseur

import wave

from io import StringIO, BytesIO

from utils.m_wifi import quality

# ---->

##### Variables #####
dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'

# ---->

##### Functions #####
def scan(folder='static'):
	"""
	Scan the wave sounds in the 'static' folder.
	
	@param:folder after this script' folder (__file__ constent)
	"""
	samples = {}
	i = 0
	for dirname, dirnames, filenames in os.walk(dir_path + str(folder)):
		for filename in sorted(filenames):
			if (os.path.os.path.splitext(filename)[1] == '.wav'):
				if (os.path.os.path.splitext(filename)[0][0] != '.'):
					samples[filename]=os.path.join(dirname, filename)
# 					print(filename)
	return samples

@app.route('/', methods=['GET', 'POST'])
def sounds():
	templateData = {
		'samplesSorted' : sorted(scan('static'), key=str),
		'samplesSortedKeys' : sorted(scan('static').values(), key=str),
		'lenSamples' : len(sorted(scan('static'), key=str)),
		'samples' : scan('static'),
		'wifi' : quality()[0],
		'last' : '',
		'lastlang' : ''
	}

	if request.method == 'POST':
		if (request.form.get('play')):
			pygame.mixer.quit()

			file = request.form.get('play')

			fileWave = wave.open(file)
			fileFreq = int(fileWave.getframerate())
			fileWave.close()

			pygame.mixer.init(fileFreq, -16, 1, 4096)
			sample = Sound(bytes(file, encoding='utf-8'))
			lastSample = sample

			sample.play()

		elif (request.form.get('say')):
			pygame.mixer.quit()

			templateData['last'] = request.form.get('say')
			tts = gTTS(text=templateData['last'], lang=request.form['lang'], slow=False)
			tts.save("say.mp3")
		
			file = './say.mp3'

			pygame.mixer.init(27000, -16, 1, 4096)
			pygame.mixer.music.load(file)
			pygame.mixer.music.play()
	
		elif (request.form.get('resay')):
			pygame.mixer.quit()

			templateData['last'] = request.form.get('resay')
			print(request.form.get('resay'))
			tts = gTTS(text=templateData['last'], lang=request.form['lang'], slow=False)
			tts.save("say.mp3")
		
			file = './say.mp3'

			pygame.mixer.init(27000, -16, 1, 4096)
			pygame.mixer.music.load(file)
			pygame.mixer.music.play()

	return render_template('list_sounds.html', **templateData)

@app.route('/memory/')
def memory():
	memory = psutil.virtual_memory()
	# Divide from Bytes -> KB -> MB
	available = round(memory.available/1024.0/1024.0,1)
	total = round(memory.total/1024.0/1024.0,1)
	return str(available) + 'MB free / ' + str(total) + 'MB total ( ' + str(memory.percent) + '% )'

@app.route('/disk/')
def disk():
	disk = psutil.disk_usage('/')
	# Divide from Bytes -> KB -> MB -> GB
	free = round(disk.free/1024.0/1024.0/1024.0,1)
	total = round(disk.total/1024.0/1024.0/1024.0,1)
	return str(free) + 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )'

	dump()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=False)
	pygame.mixer.init(44100, -16, 1, 4096)
