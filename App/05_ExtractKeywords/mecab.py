# coding: utf-8

import MeCab
import sys
import codecs


class mecab:

	def __init__(self):
		self.result = ""		

	def analysis(self,input_txt):
		txt = input_txt
		mecab = MeCab.Tagger("")
		result = mecab.parse(txt)
		self.result = unicode(result,'utf-8') 
		print self.result

	def output_noun(self):
		list = []
		list = self.result.split(" ")
		sjis_list = [unicode(s, "utf8").encode("sjis") for s in list]
