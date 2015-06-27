from bottle import route, run
import requests
import code
from pyquery import PyQuery
from newspaper import Article
import csv 

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
			result[row[0]] = row[1]

def find_location(keywords):
	for key in keywords:
		if key in result:
			return key

run(host='localhost', port= 8080, debug=True)
