import urllib
import re
import json
import csv

def verifier():

	try:

		url = "https://maps.googleapis.com/maps/api/geocode/json?address="
		key = "key=AIzaSyCk05HoXI0NyBl2dVclxm3NOXNKIn-ck-4"

		'''
		read file
		'''

		fo = open("address.txt", 'r')

		input_file = fo.read().split('\n')

		newurl = url
		pincode_entered = 0

		for i in range(0, len(input_file)):
			x = input_file[i].split(' ')
			if(i==len(input_file)-1):
				pincode_entered = x[0]
				break
			if(i==len(input_file)-2):
				continue
			for j in range(0, len(x)):
				if(j==len(x)-1 and i==len(input_file)-2):
					newurl = newurl + x[j] + "&"
				else:
					newurl = newurl + x[j] + "+"
			

		#print pincode_entered
		newurl = newurl + key
		#print newurl
		#print pincode_entered
		#print len(input_file)
		'''
		mapping pincode to city name
		'''
		city_entered = ""

		with open('pincode.csv') as csvfile:
			readcsv = csv.reader(csvfile, delimiter = ',')
			#print readcsv
			for row in readcsv:
				if(row[0]==pincode_entered):
					city_entered = row[1]
				#print row[0]
		#print city_entered

		'''
		finding correct city using google api
		'''

		htmltext = urllib.urlopen(newurl).read()
		data = json.loads(htmltext.decode('utf8'))

		#print data
		if(data['status'] != "OK"):
			print "Invalid address"
			return 0

		else:
			correct_city_name = "blank"

			for result in data['results']:
				for i in range(0, len(result)):
					#print i, len(result)
					#print i
					if(result['address_components'][i]['types'][0]=="locality"):
						if(correct_city_name == "blank"):
							correct_city_name = result['address_components'][i]['long_name']
							#print correct_city_name
							break

			#print correct_city_name
			#print city_entered
			#print pincode_entered
			if(city_entered == correct_city_name):
				print "Correct Address"
				return 1
			else:
				print "Incorrect Address"
				return 0
			#fo.truncate()

	except Exception, e:
		print str(e)
		pass

x = verifier()
print x
