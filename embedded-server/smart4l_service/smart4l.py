#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "cbarange"
__license__ = "MIT"
__date__ = "11-08-2020"
__version__ = "1.0.0"
__status__ = "Prototype"

# Standard Library
import os
import sys
from threading import Thread
import time
# Custom Modules
sys.path.insert(1, '../sensor_camera-module')
import DHT11 as DHT11
from utils import Message, Status

# Class de gestions du service de mesure temps réelle, et peut-etre aussi pour les mesures enregistrées en base
# C'est peut-etre pas opti de faire deux services qui accèdent aux capteurs, je sais pas... 
class MeasurementService(Thread):
	status = Status.START.value
	def __init__(self):
		super().__init__()

	def run(self):
		while self.status==Status.START.value:
			print(" Run")
			time.sleep(3)

	def stop(self):
		self.status = Status.STOP.value
		# Clean GPIO

# Class des gestions de l'application / service
class Smart4l():
	measurementService = MeasurementService()
	def start(self):
		print("Started !")
		# Si le service le fonctionne pas deja
		# Existance du fichier pid + le pid repond au nom du programme
		#	lancement du process, creation du fichier pid
		# Si le service fonctionne ouvrir un PIPE avec le pid du fichier pid
		# 	envoyer les parametre dans le pipe

		# Run thread
		self.measurementService.start()

		print("Running ...")

	def stop(self):
		print("Cleaning ...")

		# Supprimer le fichier pid

		# Stop Measurement Service Thread
		self.measurementService.stop()

		print("Stopped !")


# execute only if run as a script
if __name__ == "__main__":
	app = Smart4l()
	try:
		app.start()
		# Si on sort de la boucle, l'exception KeyboardInterrupt n'est plus gérée
		#while not input() == Status.STOP.value:
		while True:
			pass
		#app.stop()
	except KeyboardInterrupt:
		app.stop()
else:
	Message().error("smart4l.py : must be run as a script\n")


"""
# Communication inter process via un fichier, pas mal mais peut etre plus opti avec des pipes

import os, time

pipe_path = "/tmp/mypipe"
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)
# Open the fifo. We need to open in non-blocking mode or it will stalls until
# someone opens it for writting
pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
with os.fdopen(pipe_fd) as pipe:
    while True:
        message = pipe.read()
        if message:
            print("Received: '%s'" % message)
        print("Doing other stuff")
        time.sleep(0.5)


echo "your message" > /tmp/mypipe


https://docs.python.org/3/library/os.html
https://docs.python.org/2/library/os.html
"""

"""
# Communication je sais pas comment ^^, par fichier visiblement. Apres un pipe c'est aussi un fichier mais un peut différent quand meme
# MARCHE peut etre ?
import errno, os, sys

try:
    os.mkfifo('some_pipe_name')
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise     # can't open pipe
while True:
    with open('some_pipe_name') as fifo:
        data = fifo.read()
        print data

Client:

import os, sys
pipeout = os.open('some_pipe_name', os.O_WRONLY)
os.write(pipeout, ' '.join(sys.argv[1:]))
"""

"""
# Communication inter process, je sais pas comment ^^
# MARCHE PAS
server.py:

def start_server():
    # create process
    e = receive_messages()
    while true:
        e.wait()
        if e.message == 'quit':
            sys.exit(1)
        # some message handling

And then a client script with this type of function:

client.py:

def send_message(pid):
    pipe = get_pipe_to_process_by_pid(pid)
    pipe.send_message('Hello, World!\n')

"""

