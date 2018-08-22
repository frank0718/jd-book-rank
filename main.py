#!/usr/bin/python
#coding=utf8
import requests

import json 
import os
import sys
import time 
import re


Headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Referer": "http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10003-1", # 1-5
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}

def getContent() :
	for i in xrange(5): 
		url = 'http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10003-' + str(i+1) +'#comfort'
		r = requests.get(url,headers=Headers)
		# print r.text
		rr = re.compile('href="//(item.jd.com/\d+.html)"') 
		reObj = rr.findall(r.text)
		# print reObj

		filterList = list(set(reObj))

		for item in filterList :
			isbn =  itemContent("http://"+ item)
			getDoubanRate(isbn)
			print "\t\t\t" + item
		time.sleep(2) 


def itemContent(url) : 
	# print url 
	r = requests.get(url,headers=Headers)
	# print type(r.text) # unicode 

	rr = re.compile(u'ISBN\uff1a(\d+)') ## ： 转Unicode 
	reObj = rr.findall(r.text)
	if len(reObj) > 0 :
		return  (reObj[0]).encode("utf8")
	else :
		return 0

## douban 限速了。。。 {"msg":"rate_limit_exceeded2: 111.202.166.3","code":112,"request":"GET \/v2\/book\/isbn\/9787508660752"}%
def getDoubanRate(isbn):
	if isbn == 0 :
		print "isbn 异常" 
		return 
	url = 'https://api.douban.com/v2/book/isbn/' 
	r = requests.get(url+isbn,headers=Headers)
	data = json.loads(r.text)
	if data.has_key("title"):
		print data["title"], data["rating"]["average"], 

def main():
	getContent()

if __name__ == '__main__':
	main()