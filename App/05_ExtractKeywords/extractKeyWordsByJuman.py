#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cJuman
import types


class juman:

	PARSE_TEXT_ENCODING = 'utf-8'
	### Functions
	def __init__(self):
		print ""

	def extractKeyWords(self, txt, category):
		cJuman.init(['-B', '-e2'])
		node = self.parse(txt)
		print "**Parse**"
		print node
		print "**Category**"
		print category
		print "**Keyword**"
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
			print keywordList[0]
			return keywordList[0]
		else:
			print "None"
			return None

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
		
		
### Execute                                                   
txt = "テナガザルが好きなんだ"
category = "動物"
j = juman()
j.extractKeyWords(txt,category)
