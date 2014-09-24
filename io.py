# io.py
# This file is part of Tabida
# It encapsulates python's basic file read & write functions which conforms "ReadLines" and "WriteLines".
# It can also handle structured data files such as .CSV. "ReadColumn" and "WriteColumn" are such functions. 
# Structured data as below:
#
#	header1 | header2 | header3 | header4
#   --------------------------------------
#	C1R1    | C2R1    | C3R1    | C4R1  
#   --------------------------------------
#	C1R2    | C2R2    | C3R2    | C4R2  
#   --------------------------------------
#	C1R3    | C2R3    | C3R3    | C4R3 
#   --------------------------------------
#
# contact email: chishui2@gmail.com

headerkey = 'header'
def ReadLines(filename, removeReturn = False):
	''' Read line from file 

	''' 
	with open(filename, "r") as f:
		lines = f.readlines()

	if removeReturn:
		lines = [line.strip('\r\n').strip('\n') for line in lines ]
	return lines

# return data of ReadColumn is 
# {'header':['header1', 'header2', 'header3', 'header4'], 'header1' : ['C1R1', 'C1R2', 'C1R3'], 'header2' : [...], 'header3' : [...], 'header4' : [...]}
def ReadColumn(filename, spliter='\t', columncount = 0) :
	''' Read file and retrieve column data
		return data is map with header as key and list as value
		
	'''
	lines = ReadLines(filename, removeReturn = True)
	headers = lines[0].split(spliter)
	#remove header line
	lines[0:1] = []
	if columncount > 0 :
		headers[columncount:] = []

	#remove blank header
	headers = [i for i in headers if i != '']

	#initialize data buffer
	data = {}
	for header in headers :
		data[header] = ['' for line in lines]

	#add header tuple
	data[headerkey] = headers

	#splits lines and stores to data
	for line in lines :
<<<<<<< HEAD
		column = line.strip('\n').split(spliter)[:len(headers)]
=======
		column = line.split(spliter)
>>>>>>> c0ce75939c652d3ba7f129caf44a59a1160fcdf5
		# split line not more than 'columncount' columns
		if columncount > 0 and columncount < len(column) :
#####################################################################################
			column[2 : len(column) - 1] =  [spliter.join(column[2 : len(column) -1]) ]
#####################################################################################
			#column[columncount - 1 :] = [spliter.join(column[columncount - 1 : ]) ]

		for i in range(0, len(headers)) :
			key = data[headerkey][i]
			if i >= len(column) :
				data[key].append('')
			else:
				data[key].append(column[i])

	return data



def WriteLines(lines, filename) :
	''' Write line to file 

	''' 
	with open(filename, "w") as f:
		f.writelines(lines)


def WriteColumn(data, filename) :
	'''write data with column to file
		
		data must have key named "header" which gives column headers
	'''
	with open(filename, 'w') as f:
		#write header
		f.write('\t'.join(data[headerkey]) + '\n')

		#get line count 
		#!!!!! line count may be inconsistent 
		count = len(data[data[headerkey][0]])

		#write lines
		for i in range(0, count) :
			line = ''
			for header in data[headerkey]:
				line += data[header][i]
				line += '\t'
			line = line.strip('\t')
			line += '\n'
			f.write(line)


def AppendLines(lines, filename) :
	''' append data to file

	'''
	with open(filename, 'a') as f:
		for line in lines:
			f.write(line)

def CheckLineCount(data) :
	'''check if data from io.ReadColumn have the same line counts
	
	'''
	count = 0
	lastheader = ''
	for header in data[io.headerkey]:
		if count and count != len(data[header]) :
			print header,lastheader, len(data[header]), len(lastheader)
			return False
		else:
			count = len(data[header])
			lastheader = header
	return True

import copy
def mergeFile(file1, file2, baseHeader, outFile, voidValue='N/A') :
	''' merge file1 and file2 based on column of same header

	'''
	data1 = ReadColumn(file1)
	data2 = ReadColumn(file2)

	outdata = {}
	
	dictOfTwoFile = {}
	for i, data in enumerate(data1[baseHeader]) :
		dictOfTwoFile.setdefault(data, {})
		dictOfTwoFile[data][1] = i

	for i, data in enumerate(data2[baseHeader]) :
		dictOfTwoFile.setdefault(data, {})
		dictOfTwoFile[data][2] = i

	outdata[headerkey] = copy.copy(data1[headerkey])
	outdata[headerkey][len(outdata[headerkey]) :] = [item for item in data2[headerkey] if item not in outdata[headerkey]]
	print outdata[headerkey], dictOfTwoFile
	for header in outdata[headerkey]:
		outdata[header] = []
		for item in dictOfTwoFile:
			index1 = dictOfTwoFile[item].get(1, -1)
			index2 = dictOfTwoFile[item].get(2, -1)
			#print header, item, index1, index2
			value = voidValue
			while True:			
				if header in data1[headerkey] and header in data2[headerkey] :
					if index1 >=0 and index2 >= 0 :
						value = data1[header][index1] if data1[header][index1] != '' else data2[header][index2]
						break
				if header in data1[headerkey] and index1 >= 0:
					value = data1[header][index1]
				elif header in data2[headerkey] and index2 >= 0:
					value = data2[header][index2]
				break
			
			outdata[header].append(value)


	WriteColumn(outdata, outFile)


	# data2[headerkey][len(data2[headerkey]) :] = [item for item in data1[headerkey] if item != baseHeader]
	# for head in data1[headerkey]:
	# 	if head == baseHeader:
	# 		continue
	# 	data2[head] = [voidValue for i in data2[baseHeader]]

	# for i, key in enumerate(data2[baseHeader]):
	# 	if key in dict1:
	# 		index = dict1[key]
	# 		for head in data1[headerkey][1:]:
	# 			if i >= len(data2[head]) or index >= len(data1[head]) :
	# 				print i, len(data2[head]), index, len(data1[head]), len(data1[baseHeader])
	# 			data2[head][i] = data1[head][index]

	# WriteColumn(data2, outFile)


def callLog(func):	
	def _callLog() :
		print 'begin call function:', func.func_name
		func()
		print 'end call function:', func.func_name

	return _callLog

if __name__ == '__main__':
	# filename = "E:\\taoli\\a"
	#lines = ReadLine(filename)
	#WriteLine(lines, "E:\\apptemp.txt")
	# data = ReadLines(filename)
	# AppendLines(data, "E:\\taoli\\b")

	mergeFile('t1.txt', 't2.txt', 'Prey', 'out.txt')

	#print(len(data['protein']))
	# data = {}
	# data['header'] = ['1', '2', '3']
	# data['1'] = ['a', 'b', 'c']
	# data['2'] = ['d', 'e', 'f']
	# data['3'] = ['g', 'h', 'i']
	#WriteColumn(data, out)
	s = 'abcde'
	print s.strip('de')
