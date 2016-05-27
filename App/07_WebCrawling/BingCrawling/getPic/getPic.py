#coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
import time 
import os
import requests
import shutil

TEXT_ENCODING = "utf-8"
app = Flask(__name__)
class GetPic:

	def _init_(self):
		print "" 

	def bing_get_pic(self,query):
		urlList = []
		#set URL
		bing_url = 'https://api.datamarket.azure.com/Bing/Search/Image'

		#set Microsoft Azure Marketplacec
		MS_ACCTKEY = 'fUs4HwRdomanM5cGY/3eblwDfQ7ELAqDi0sHA7WApMM'

		#set parameter
		payload = { '$format': 'json','Query': "'"+query+"'",}

		#GET request
		r = requests.get(bing_url, params=payload, auth=('', MS_ACCTKEY))

		#count the number of pictures
		count = 1
	
			
		#make directory to save pictures
		dirname = "./%s"%query
		check = os.path.exists(dirname)
		if check:
			shutil.rmtree(dirname)
			print "exist directory<%s>"%query
		
		os.mkdir(dirname)
		   
	 
		for item in r.json()['d']['results']:
			time.sleep(3)
			image_url = item['MediaUrl']

			root,ext = os.path.splitext(image_url)

			if ext.lower() == '.jpg':    

				#print image_url,

				urlList.append(image_url)

				r = requests.get(image_url)

				fname = "%s/%04d.jpg"%(dirname,count)

				f = open(fname, 'wb')

				f.write(r.content)

				f.close()

				print "...save", fname
				
				count += 1
			
				#get three pictures (changeabe)	
				if count >= 3:
					break		
		return urlList

	def bing_search(self, word):
		l = []
		url = ""
		l = self.bing_get_pic(word)
		for i in range(len(l)):
			url += l[i]
			url += ","
		return url

@app.route('/entry/<string:txt>')
def index(txt):
	url = ""
        txt = txt.encode(TEXT_ENCODING)
	url = gp.bing_search(txt)
	return url	

if __name__ == '__main__':
	gp = GetPic()
	app.run(host='0.0.0.0')
