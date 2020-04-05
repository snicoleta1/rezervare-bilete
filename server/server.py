from typing import List, Dict
from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

currentRes = 0
resList = []

#Selectia unui zbor din baza de date dupa id

def selectFlight(idF):
	config = {
		'user': 'root',
		'password': 'root',
		'host': 'db',
		'port': '3306',
		'database': 'flightsDatabase'
		}

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	sql = 'SELECT * FROM flights WHERE flightId = %s'
	var = (idF,)	

	cursor.execute(sql, var)

	result = []
	for line in cursor:
		result.append(line)

	cursor.close()
	connection.close()

	return result

#Gasirea tuturor zborurilor posibile dintr-un loc dupa o anumita zi si ora

def getAllFlightsAfter(source, departureDay, departureHour):

	config = {
		'user': 'root',
		'password': 'root',
		'host': 'db',
		'port': '3306',
		'database': 'flightsDatabase'
		}

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	sql = 'SELECT * FROM flights WHERE source = %s AND departureDay > %s OR (departureDay = %s AND departureHour >= %s)'
	var = (source, departureDay, departureDay, departureHour)	

	cursor.execute(sql, var)

	result = []
	for line in cursor:
		result.append(line)

	cursor.close()
	connection.close()

	return result

#Gasirea celei mai bune rute

def getOptimalRoute(source, dest, maxFlight, departureDay):

	routes = []	

	queue = []
	possibleFlights = getAllFlightsAfter(source, departureDay, 0)

	for posFlight in possibleFlights:
		queue.append((None, posFlight, 0))

	while len(queue) > 0:
		#Scoatem un zbor:
		currentFlight = queue.pop(0)

		flight = currentFlight[1]

		if currentFlight[2] > int(maxFlight):
			continue

		if flight[1] == dest:
			routes.append(currentFlight)
			continue

		#Avem un zbor, calculam ziua si data cand ajunge si cautam zborurile care pleaca
		#din data calculata:

		newHour = flight[3] + flight[4]
		newDay = flight[2]

		if newHour > 23:
			newDay = flight[2] + 1
			newHour = newHour - 24

		#Ora si ziua la care ajunge zborul curent
		possibleFlights = getAllFlightsAfter(str(flight[1]), str(newDay), str(newHour))

		for posFlight in possibleFlights:
			queue.append((currentFlight, posFlight, currentFlight[2] + 1))
	

	if len(routes) == 0:
		bestRoute = None
	else:
		bestRoute = routes[0] 
		for r in routes:
			f = r[1]
			if f[2] < bestRoute[1][2]:
				bestRoute = r
			if f[2] == bestRoute[1][2]:
				if f[3] + f[4] < bestRoute[1][3] + bestRoute[1][4]:
					bestRoute = r

	if bestRoute == None:
		return bestRoute

	#Facem lista doar din zboruri:
	parent = bestRoute[0]

	listF = [bestRoute[1]]
	elem = bestRoute	

	while parent != None:

		listF.append(parent[1])
		parent = parent[0]

	return listF[::-1]

#Rezervare zbor

def bookFlight(fId):

	config = {
		'user': 'root',
		'password': 'root',
		'host': 'db',
		'port': '3306',
		'database': 'flightsDatabase'
		}

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()

	sql = 'UPDATE flights SET books = books + 1 WHERE flightId = %s'
	args = (fId,)
	cursor.execute(sql, args)

	connection.commit()
	cursor.close()
	connection.close()

#Rezervarea unui bilet

def bookTicket(flightIds):
	global currentRes
	global resList

	#Atomicitate:
	for idF in flightIds:
		flight = selectFlight(idF)

		#Daca nu exita zborul cu idul curernt:
		if len(flight) == 0:
			return ""

		flight = flight[0]

		#Daca nu mai sunt locuri sau rezervari returnam esec:
		if flight[5] - flight[8] < 0 and flight[7] > flight[5] + 0.1*flight[5] :
			return ""

	#Facem rezervarile daca e totul ok:
	for idF in flightIds:
		#flight = selectFlight(idF)
		bookFlight(idF)
	
	#Actualizam rezervarea curenta si bagam noua rezervare in lista de rezervari
	currentRes += 1
	resList.append((currentRes, flightIds))
	return (currentRes, flightIds)

@app.route('/test')
def f0():
	return jsonify(res="Test")

@app.route('/bookticket')
def f1():
	flightId = request.args.get('fId', default = None, type = str)

	idS = flightId.split("|")

	result = bookTicket(idS)
	return jsonify(Reservation=result)

@app.route('/getOptimalRoute')
def f2():
	source = request.args.get('s', default = None, type = str)
	dest = request.args.get('d', default = None, type = str)
	maxFlight = request.args.get('mF', default = None, type = int)
	departureDay = request.args.get('dD', default = None, type = int)

	result = getOptimalRoute(source, dest, maxFlight, departureDay)
	return jsonify(res=result)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
