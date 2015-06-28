from bottle import route, run
import requests
import code
from pyquery import PyQuery
from newspaper import Article
import csv 
import urllib
import json
import sys
import pycps

result = []
crime_map = {}
start = "/url?q="
end = "&"
final1 = []

@route('/all_sambavams')
def crimes():
	pruneDataSet()
	for i in range(0,99):
		scrap(i*10)
	print("=================================================")
	groupByArea([x for x in final1 if x is not None])
	rest_json = constructJson(crime_map)
	print(rest_json)
	return rest_json


def constructJson(crime_map):
	rest_json = []
	for map in crime_map:
		temp = {}
		temp["name"] = map
		print(map)
		print(getLatLong(map))
		latLong = getLatLong(map).split(',')
		if len(latLong) > 0:
			temp["lattitude"] = latLong[0]
			temp["longitude"] = latLong[1]
		temp["sambavams"] = crime_map[map]
		rest_json.append(temp)
	return json.dumps(rest_json) 

def groupByArea(final_crimes):
	for crime in final_crimes:
		if crime in crime_map:
			crime_map[crime] += 1
		else:
			crime_map[crime] = 0

def scrap(index):
	base_url = "https://www.google.co.in/search?q=chennai%20accidents&tbm=nws&start="+str(index)
	web_page = requests.get(base_url)
	parsed_content = PyQuery(web_page.text)
	all_crimes = parsed_content('a')
	for crime in all_crimes:
		crime_url = crime.attrib["href"]
		if '/url?q=' in crime_url:
			try:
				article = Article((crime_url.split(start))[1].split(end)[0])
				article.download()
				article.parse()
				article.nlp()
				keywords = article.keywords
				area_name = findLocation(keywords)
				final1.append(area_name)
			except Exception:
				pass

def pruneDataSet():
	with open('chennai.csv', 'rt') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			result.append(row[0].lower())

def findLocation(keywords):
	for key in keywords:
		for res in result:
			for word in res.split():
				if key == word:
					return res

def getLatLong(area):
	api_key = 'AIzaSyDOjBGZEBvLCpHXkNvl-bBBxKHhzAeSaqU'
	area = area.replace(" ", "%20")
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+area+'%20chennai&key='+api_key
	response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
	if len(response["results"]) > 0:
		co_ord=response["results"][0]["geometry"]["location"]
		latLong = str(co_ord["lat"]) + "," + str(co_ord["lng"])
		return latLong

def exportData():
	con = pycps.Connection('tcp://cloud-eu-0.clusterpoint.com:9007', 'Vibathu', 'deepasaj@thoughtworks.com', 'admin123', '100643')
	con.insert(crime_map)

run(host='localhost', port= 8080, debug=True)
