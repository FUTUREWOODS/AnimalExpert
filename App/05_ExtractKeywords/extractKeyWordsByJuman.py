#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import types
import cJuman

TEXT_ENCODING = "utf-8"
app = Flask(__name__)
	
class juman:
	
	def __init__(self):
		cJuman.init(['-B', '-e2'])

	def extractKeyWords(self, txt, category):
		node = self.parse(txt)
		wordsList = []
		keywordList = []
		categoryList = []
		wikiword = ""
		wordsList = node.split("\n")
		for i in range(len(wordsList)):
			if "カテゴリ" in wordsList[i]:
				keywordList = self.categoryParse(wordsList[i],category)
					
			elif "Wikipedia上位語:" in wordsList[i]:
				keywordList = self.wikiWordsParse(wordsList[i],category)
		
		if len(keywordList) != 0:
			return keywordList[0]
		else:
			return "0"

	def parse(self, txt):
		node = cJuman.parse_opt([txt], cJuman.SKIP_NO_RESULT)
		return node

	def categoryParse(self, jumantxt,category):
		keywordlist = []
		categorylist = []
		if "カテゴリ" in jumantxt:
			categorylist = jumantxt.split("カテゴリ:")
			categorylist = categorylist[1].split("\"")
			if categorylist[0] == category:
				categorylist = jumantxt.split(" ")
				keywordlist.append(categorylist[0])
		return keywordlist

	def wikiWordsParse(self, jumantxt,category):
		keywordlist = []
		categorylist = []
		wikilist = []
		wikiword = ""
		if "Wikipedia上位語:" in jumantxt:
			categorylist = jumantxt.split("Wikipedia上位語:")
			categorylist = categorylist[1].split("\"")
			categoryList = categorylist[0].split("/")
			wikiword = categorylist[0]
			wikiword = self.parse(wikiword)
			wikilist = self.categoryParse(wikiword,category)
			if len(wikilist) != 0:
				categorylist = jumantxt.split(" ")
				keywordlist.append(categorylist[0])
		return keywordlist

@app.route('/entry/<string:txt>')
def index(txt):
        txt = txt.encode(TEXT_ENCODING)
        category = "動物"
        message = j.extractKeyWords(txt,category)
        return message

if __name__ == '__main__':
        j = juman()
        app.run(host='0.0.0.0') 
