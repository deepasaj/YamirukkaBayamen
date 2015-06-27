from bottle import route, run
import requests
import code
from pyquery import PyQuery
from newspaper import Article
import csv 

result = {}

@route('/hello')
def hello():
	return "Hi Sajani!"

@route('/all_sambavams')
def crimes():
	base_url = "http://timesofindia.indiatimes.com"
	web_page = requests.get(base_url + '/city/chennai?cfmid=2000000')
	parsed_content = PyQuery(web_page.text)
	all_crimes = parsed_content('div.ct1stry h2 a')
	pruneDataSet()
	for crime in all_crimes:
		crime_url = base_url + crime.attrib["href"]
		article = Article(crime_url)
		article.download()
		article.parse()
		article.nlp()
		keywords = article.keywords

def pruneDataSet():
	with open('chennai.csv', 'rt') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			result[row[0]] = row[1]
		print(result)


run(host='localhost', port= 8080, debug=True)
