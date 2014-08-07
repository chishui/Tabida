#coding:utf-8
# This file is part of TLDataUtil
# It can list specific files you want to handle.
#
# contact email: chishui2@gmail.com

import os

def ListFileStartWith(rootDir, startwith, ext=None) :
	''' list all files with name start with 'startwith'

	retrieve all files with extension 'ext' is 'ext' is not none 
	'''
	allfiles = []
	for root,dirs,files in os.walk(rootDir):
		for filespath in files:
			if filespath.find(startwith) == 0 :
				if ext and filespath[-len(ext):] != ext:
					continue
				allfiles.append(os.path.join(root,filespath))

	return allfiles

def ListFileEndWith(rootDir, endwith) :
	''' list all files with name end with 'endwith'

	'''
	allfiles = []
	for root,dirs,files in os.walk(rootDir):
		for filespath in files:
			if endwith and filespath[-len(endwith):] == endwith:
				allfiles.append(os.path.join(root,filespath))

	return allfiles


if __name__ == '__main__':
	files = ListFileEndWith(unicode('E:\\taoli', 'utf8'), ".xls_newout.xls")
	print files