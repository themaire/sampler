#!/usr/bin/python3.5m
# -*- coding: utf-8 -*-

##### Modules #####
from subprocess import getstatusoutput
import re

##### Fonctions #####

def quality():
        iwconfig = str(getstatusoutput("iwconfig"))
        result = re.findall("(level=[0-9]{2,3}/[0-9]{2,3}|Quality=[0-9]{2,3}/[0-9]{2,3})",iwconfig)[0]
        qualRef = int(result.split("=")[1].split("/")[1])
        qual = int(result.split("=")[1].split("/")[0])
        
        if(qualRef == 100):
                return (int(qual),str(qual) + '/' + str(qualRef))
        elif(qualRef == 70):
                return (int((int(qual)/70)*100),str(qual) + '/' + str(qualRef))
        elif(qualRef == 70 and qual == 70):
                return 100

# test des deux fonctions
if __name__ == "__main__":

	from time import sleep

	def testWifi(nb):
		total = 0
		print("Qualité du signal")
		for i in range(nb):
			qual = quality()[0]
			print("Test numéro ", i+1, " : ", qual)
			total = total + qual
			sleep(1)
		moy = round((total / nb),0)
		print("Moyenne de qualité : ", moy)

	testWifi(6)

#	qual = re.findall("(Link Quality=[0-9]{2})",str(getstatusoutput("iwconfig")))[0]
