import sys

# usage: checkenco.py <file to check> <encoding to check>

f = open(sys.argv[1], encoding = sys.argv[2])
next = f.readline()
i = 0
while next != '':
	print (str(i) + " : " + next)
	i += 1
	next = f.readline()


