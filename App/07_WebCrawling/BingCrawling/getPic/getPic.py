#coding:utf-8
import time 
import os
import requests

class GetPic:

	def _init_(self):
		print "" 

	def bing_get_pic(self,query):
		
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
			print "exist directory<%s>"%query
		else:
			os.mkdir(dirname)
			   
	 
		for item in r.json()['d']['results']:
			time.sleep(3)
			image_url = item['MediaUrl']

			root,ext = os.path.splitext(image_url)

			if ext.lower() == '.jpg':    

				print image_url,

				r = requests.get(image_url)

				fname = "%s/%04d.jpg"%(dirname,count)

				f = open(fname, 'wb')

				f.write(r.content)

				f.close()

				print "...save", fname

				count += 1
			
				#get three pictures (changeabe)	
				if count >= 4:
					break		

	 

	def bing_search(self, word):
		self.bing_get_pic(word)
		
if __name__ == '__main__':

	#set word
	word = "アフリカゾウ"
	gp = GetPic()
	gp.bing_search(word)
