from typing import List, Dict
import json
import urllib.request

def main():

	while True:

		command = input("Enter command:\nSearch\nBook\nBuy\n\n")

		if command == 'info':
			oUrl = urllib.request.urlopen("http://server:5000/test")
			data = json.loads(oUrl.read().decode())
			print(data)


		if command.upper() == 'SEARCH':
			args = input("\nEnter: Source Destination MaxFlights DepartureDay\n\n")
			argsL = args.split()

			if(len(argsL) < 4):
				print("Error: Too few arguments given\n")
				continue

			url = "http://server:5000/getOptimalRoute?s=" + argsL[0] + "&d=" + argsL[1] + "&mF=" + argsL[2] + "&dD=" + argsL[3]

			oUrl = urllib.request.urlopen(url)
			data = json.loads(oUrl.read().decode())

			if data['res'] is None:
				print("No flights were found\n")
				continue

			idList = []
			for d in data['res']:
				idList.append(d[6])				
				print("Flight id: {} |Source: {} |Destination: {} |Departure Day: {} |Hour: {} |Duration: {}".format(d[6], d[0], d[1], d[2], d[3], d[4]))

			print("\nIds list:\n")
			print(idList)
			print("")

		if command.upper() == 'BOOK':
			args = input("\nEnter flights ids:\n\n")
			argsL = args.split()

			if(len(argsL) < 1):
				print("Error: Too few arguments given\n")
				continue

			url = "http://server:5000/bookticket?fId="

			for i in range(len(argsL) -1):
				url += argsL[i] + "|"
			url += argsL[-1]

			oUrl = urllib.request.urlopen(url)
			data = json.loads(oUrl.read().decode())

			if data['Reservation'] == "":
				print("Booking process failed\n")
				continue

			print("Reservation id: {}".format(data['Reservation'][0]))
			print("Flights id:")
			print(data['Reservation'][1])
			print("")

if __name__ == '__main__':
	main()
