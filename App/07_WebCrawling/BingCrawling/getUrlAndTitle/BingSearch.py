# coding:utf-8

import urllib
import requests
import json


class Bing(object):

	def __init__(self, key):

		self.api_key = key


	def web_search(self, query, k, keys=["Url"], skip=0):
	
		url = 'https://api.datamarket.azure.com/Bing/Search/Web?'
	
		max_num = 50
	
		params = {"Query": "'{0}'".format(query),"Market": "'ja-JP'"}

        	request_url = url + urllib.urlencode(params) + "&$format=json"

        	results = []

        	repeat = k / max_num
        
		remainder = k % max_num

        	for i in xrange(repeat):

			result = self._search(request_url, max_num, skip, keys)

        	    	results.extend(result)

            		skip += max_num

        	if remainder:

            		result = self._search(request_url, remainder, skip, keys)

            		results.extend(result)

        	return results


    	def related_search(self, query, keys=["Title"]):

        	url = 'https://api.datamarket.azure.com/Bing/Search/RelatedSearch?'

        	params = {"Query": "'{0}'".format(query),"Market": "'ja-JP'"}

		request_url = url + urllib.urlencode(params) + "&$format=json"
	
	        results = self._search(request_url, 50, 0, keys)
	
	        return results


	def _search(self, request_url, top, skip, keys):

        	final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)

        	response = requests.get(final_url, 
                                auth=(self.api_key, self.api_key), 
                                headers={'User-Agent': 'My API Robot'})
        
        	response = response.json()

        	results = []

        	for item in response["d"]["results"]:

            		result = {}

            		for key in keys:

				result[key] = item[key].encode("utf-8")

            			results.append(result)

        	return results


if __name__ == '__main__':

	#set Microsoft Azure Marketplace key
	key = "fUs4HwRdomanM5cGY/3eblwDfQ7ELAqDi0sHA7WApMM"
	
	#set word
	q = "猿"

	bing = Bing(key)
	
	#the Searchable number is 50
	results = bing.web_search(q, 3, ["Title", "Url"])
		
	#print URL
	print json.dumps(results, indent=2)

	results = bing.related_search(q)

	#print Title
	print json.dumps(results, indent=2)
