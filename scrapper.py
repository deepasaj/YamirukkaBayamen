from bottle import route, run
import requests
import code
from pyquery import PyQuery
from newspaper import Article
import csv 
import urllib
import json

result = {}
crime_map = {}
start = "/url?q="
end = "&"

@route('/hello')
def hello():
	return "Hi Sajani!"

@route('/all_sambavams')
def crimes():
	base_url = "https://www.google.co.in/search?q=chennai%20accidents&tbm=nws&start=0"
	web_page = requests.get(base_url)
	parsed_content = PyQuery(web_page.text)
	all_crimes = parsed_content('a')
	pruneDataSet()
	for crime in all_crimes:
		crime_url = crime.attrib["href"]
		if '/url?q=' in crime_url:
			article = Article((crime_url.split(start))[1].split(end)[0])
			article.download()
			article.parse()
			article.nlp()
			keywords = article.keywords
			print(keywords)
			area_name = find_location(keywords)
			print("Area = ", area_name)
		

def pruneDataSet():
	with open('chennai.csv', 'rt') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			result[row[0]] = getLatLong(row[0])

def find_location(keywords):
	for key in keywords:
		if key in result:
			return key

def getLatLong(area):
	api_key = 'AIzaSyDOjBGZEBvLCpHXkNvl-bBBxKHhzAeSaqU'
	area = area.replace(" ", "%20")
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+area+'&key='+api_key
	print("Area ==== " + area)
	response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
	if len(response["results"]) > 0:
		co_ord=response["results"][0]["geometry"]["location"]
		latLong = str(co_ord["lat"]) + "," + str(co_ord["lng"])
		print(area + " -------- " + latLong)

run(host='localhost', port= 8080, debug=True)
