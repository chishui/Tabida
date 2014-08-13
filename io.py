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
		f.close()

	if removeReturn:
		lines = [line.strip('\r\n').strip('\n') for line in lines ]
	return lines

# return data of ReadColumn is 
# {'header':['header1', 'header2', 'header3', 'header4'], 'header1' : ['C1R1', 'C1R2', 'C1R3'], 'header2' : [...], 'header3' : [...], 'header4' : [...]}
def ReadColumn(filename, spliter='\t', columncount = 0) :
	''' Read file and retrieve column data
	
		return data is map with header as key and list 
		as value
	'''
	lines = ReadLines(filename, removeReturn = True)
	headers = lines[0].split(spliter)
	#remove header line
	lines[0:1] = []
	if columncount > 0 :
		headers[columncount:] = []

	#initialize data buffer
	data = {}
	for header in headers :
		data[header] = []

	#add header tuple
	data[headerkey] = headers

	#splits lines and stores to data
	for line in lines :
		column = line.strip('\n').split(spliter)
		# split line not more than 'columncount' columns
		if columncount > 0 and columncount < len(column) :
#####################################################################################
			column[2 : len(column) - 1] =  [spliter.join(column[2 : len(column) -1]) ]
#####################################################################################
			#column[columncount - 1 :] = [spliter.join(column[columncount - 1 : ]) ]

		for i in range(0, len(column)) :
			key = data[headerkey][i]
			data[key].append(column[i])

	return data



def WriteLines(lines, filename) :
	''' Write line to file 

	''' 
	f = open(filename, "w")
	f.writelines(lines)
	f.close()


def WriteColumn(data, filename) :
	'''write data with column to file
		
		data must have key named "header" which gives column headers
	'''
	f = open(filename, 'w')

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

	f.close()

def AppendLines(lines, filename) :
	''' append data to file

	'''
	with open(filename, 'a') as f:
		for line in lines:
			f.write(line)
		f.close()

def checkLineCount(data) :
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

if __name__ == '__main__':
	# filename = "E:\\taoli\\a"
	#lines = ReadLine(filename)
	#WriteLine(lines, "E:\\apptemp.txt")
	# data = ReadLines(filename)
	# AppendLines(data, "E:\\taoli\\b")

	print ReadLines("Readme.md", removeReturn = False)


	#print(len(data['protein']))
	# data = {}
	# data['header'] = ['1', '2', '3']
	# data['1'] = ['a', 'b', 'c']
	# data['2'] = ['d', 'e', 'f']
	# data['3'] = ['g', 'h', 'i']
	#WriteColumn(data, out)
