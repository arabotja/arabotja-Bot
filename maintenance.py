#!/usr/bin/python
#-*- coding: UTF-8 -*-

import re

class Repairman:

	def fixUrl(self, targetUrl):
		targetUrl = re.sub(r'.*?(\d{10})', self.url + r'\1', targetUrl)
		return targetUrl

	def fixList(self, targetList):
		for e in targetList:
			e[1] = re.sub(r'.*?(\d{10})', self.url + r'\1', e[1])
		return targetList
