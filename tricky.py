# coding:utf-8
# This file is part of Tabida
# This file contains some useful function for data processing.
# contact email: chishui2@gmail.com
import os
def GetFileTags(files, removestrings) :
	''' Get file tag from file name. Remove characteristic strings from file name.

	'''
	tags = []
	for name in files :
		tag = os.path.basename(name).encode('ascii','ignore')
		for removestring in removestrings:
			tag = tag.replace(removestring, "");

		tags.append(tag)

	return tags

def RemoveLines(lines, topLineCount = 0, bottomLineCount = 0) :
	'''remove useless lines on top and bottom and leave lines easy handled
		
	'''
	if topLineCount + bottomLineCount > len(lines) :
		raise AssertionError, '%d + %d > total line count: %d' % (topLineCount, bottomLineCount, len(lines)) 

	lines = lines[topLineCount :]
	lines = lines[:len(lines) - bottomLineCount]
	return lines


def FilterLinesWithStartingRules(lines, startingrules = [], notstartingrules = []) :
	'''find lines which start with some rules or not start with some rules. Either startingrules or notstartingrules, only one parameter needed.

	''' 
	if len(startingrules) > 0 and len(notstartingrules) > 0 :
		raise AssertionError, 'Either startingrules or notstartingrules, only one parameter needed.'

	filterlines = []
	for line in lines:
		for startingrule in startingrules:
			if line.find(startingrule) == 0 :
				filterlines.append(line)
				continue

		breakfalse = True
		for notstartingrule in notstartingrules:
			if line.find(notstartingrule) == 0 :
				breakfalse = False
				break
		if breakfalse :
			filterlines.append(line)

	return filterlines

def GetColumnFromLines(lines, icolumn, spliter='\t', default='') :
	'''get a column from format lines 

	'''
	column = []
	for line in lines:
		col = line.strip('\n').split(spliter)[icolumn]
		if col == '':
			column.append(default)
		else :
			column.append(col)
	return column


if __name__ == '__main__' :
	lines = ['*123', '*456', '\thahah', 'test', '*']
	lines = FilterLinesWithStartingRules(lines, notstartingrules = ['*', 't'])
	print lines
	# lines = ['1 2 3', '4 5 6', '7 8 ']
	# print GetColumnFromLines(lines, 2, spliter=' ', default='0')

	print __file__