# Necessary import

from lxml import html
import requests
import datetime
import json
import time

# Load html page
page = requests.get('https://www.lci.fr/emission/le-13h/')
tree = html.fromstring(page.content)

# Get all header link
hrefs = tree.xpath('//a[@class="medium-3col-article-block-article-link"]//@href')

index = 0
oldTick = 0

# For each current title
for href in hrefs:
	
	# Load current title page
	hrefs = tree.xpath('//a[@class="medium-3col-article-block-article-link"]//@href')

	# Get it's relative HTML
	currentPage = requests.get("https://www.lci.fr" + href)
	currentTree = html.fromstring(currentPage.content)

	# Parse data
	data = currentTree.xpath('//script[contains(., "uploadDate")]/text()')

	# Get JSON
	djson = json.loads(data[0].encode('utf-8'))

	# Get current date
	currentDay=djson.get("uploadDate")

	# Convert date to timestamp
	tick = time.mktime(datetime.datetime.strptime(currentDay,'%Y-%m-%dT%H:%M:%S.%fZ').timetuple())

	if (oldTick==tick):
		index = index + 1
	else:
		index = 0
		oldTick = tick

	# Push timestamp into JSON
	djson['timestamp'] = int(round(tick)) * 1000000 + index

	# Print formatted JSON
	json_string = json.dumps(djson, ensure_ascii=False).encode('utf8').replace("&#39;","\'")
	
	#print json_string

	print djson.get('timestamp')