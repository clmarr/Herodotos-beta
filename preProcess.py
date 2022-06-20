import sys
import string
import optparse
import nltk
from nltk.tokenize import word_tokenize

####
# modified version of preProcess.py of the 2016 Herodotos GitHub repo by @clmarr
# usage: python3 preProcess.py <inputFile> > <outputFile>
####

optparser = optparse.OptionParser()
optparser.add_option("--nltk", default="", help="Prefix for output files")
opts, args = optparser.parse_args()
USE_NLTK = opts.nltk # i.e. True if "--nltk" is called at all, else False.

CW = (open(sys.argv[1]).read().splitlines())
#CW = sys.argv[1].splitlines()

def removePunct(word, punct):
	if word[0] in string.punctuation:
		print ('0	'+word[0])
		w = word[1:]
		removePunct(w, punct)
	else:
		if word[-1] in string.punctuation:
			punct = [word[-1]] + punct #punct.append(word[-1])
			w = word[0:-1]
			removePunct(w, punct)
		else:
			### Abbreviations ###
			if len(punct) == 1 and punct[0] == '.' and len(word) < 5 and word[0].isupper():
				print ('0	'+word+'.')
			elif len(punct) == 1 and punct[0] == '.' and len(word) < 4:
				print ('0	'+word+'.')
			#####################
			else:
				print ('0	'+word)
				for pct in punct:
					if pct == ':':
						print ('0	<COLON>')
					else:
						print ('0	'+pct)
				if '.' in punct:
					print ()
				elif '!' in punct:
					print ()
				elif '?' in punct:
					print ()
				elif ';' in punct:
					print ()
i = 0
for line in CW:
	# bees = []
	# b = -1
	# for t in line:
		# b += 1
		# if t == '\xe2':
			# bees.append(b)
			# bees.append(b+1)
			# bees.append(b+2)
	# b = -1
	# lin = ''
	# for t in line:
		# b += 1
		# if b not in bees:
			# lin += t
		# if b in bees and b-1 not in bees:
			# lin += '"'
	# line = lin

	for w in line.split() if not USE_NLTK else word_tokenize(line):
		rt = []	# does this actually do anything?
		for ch in w:
			if ch in ['0','1','2','3','4','5','6','7','8','9','0']:
				w = w.replace(ch,'')
		if len(w) > 0:
			### just print words that only consist of punctuation
			c = 0 # content characters.
			p = 0 # punctuation
			for ch in w:
				if ch in string.punctuation:
					p = 1
				else:
					c = 1
			if c == 0:	# all punctuation.
				print ('0	'+w)
				if '.' in w:
					print ()
				elif '!' in w:
					print ()
				elif '?' in w:
					print ()
				elif ';' in w:
					print ()
			### remove punctuation
			elif p == 1:
				#NLTK should probably be already handling most of this if using it, but no reason to remove... yet?
				punct = []
				root = ''
				removePunct(w, punct)
			else:
				print ('0	'+w)
		i += 1
