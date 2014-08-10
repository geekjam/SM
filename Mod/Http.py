#!/usr/bin/python
#-*-coding:utf-8-
import sys
import gzip
import urllib2
from cStringIO import StringIO
import cookielib

class HttpClient():
	Url = ""
	Method    = "GET"
	PostData  = None
	UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
	Reponse   = None

	def ToUtf8(self, text):
		try:
			return text.decode("utf-8")
		except Exception, e:
			return text.decode("gbk")

	def GetString(self):
		retString = ""
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		if self.Method == "POST":
			req = urllib2.Request(self.Url,self.PostData)
		else:
			req = urllib2.Request(self.Url)

		req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp")
		req.add_header('Accept-Encoding', "*")
		req.add_header('User-Agent', self.UserAgent)
		self.Reponse = urllib2.urlopen(req, timeout=15)
		contentEncoding =  self.Reponse.headers.get('Content-Encoding')
		if  contentEncoding == 'gzip':
			compresseddata = self.Reponse.read()
			compressedstream = StringIO(compresseddata)
			gzipper = gzip.GzipFile(fileobj=compressedstream)
			retString = gzipper.read()
		else:
			retString = self.Reponse.read()
		
		retString = self.ToUtf8(retString)
		return retString



	def __init__(self, url):
		self.Url = url

def Init():
    pass



