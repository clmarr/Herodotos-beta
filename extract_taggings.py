import sys
import optparse

# at present, this assumes input file is in CRF or CONLL format
# usage: python3 extract_taggings.py <input> <output> (-p prefix) (-c [True if want to report context sentence]) (-s [sentence delimiter token])

optparser = optparse.OptionParser()
optparser.add_option("-p", "--prefix", default=False, help="If you specify a prefix, only tags beginningin the sequence entered will be reported")
optparser.add_option("-c", "--context", default=False, help="If context is specified, the sentence where the tag occured will be reported.")
optparser.add_option("-s", "--sentence_delim", default='\n', help="Sentence delimiter token -- a line equivalent to this token (without stripping) will be considered to mark a sentence boundary.")
optparser.add_option("-t", "--tag_flag", default='\t', help="Token delimiting tag from token in input file.")
optparser.add_option("-f", "--format", default="crf", help="Format of input file. (Currently accepted formats: CRF, CONLL)")

opts, args = optparser.parse_args()

def is_target(line):
	if opts.prefix:
		return line[:len(opts.prefix)] == prefix
	return line[0] != '0'

if opts.format.lower() not in ["conll", "crf"]:
	raise Exception("Usage error: only accepted formats are CONLL and CRF currently.")

CONLL = opts.format.lower() == "conll"

LINES = []
with open(sys.argv[1]) as f:
	LINES = f.readlines()

def get_context_sentence(line_index):
	if not opts.context:
		return ''

	start = line_index - 1
	while False if start < 0 else LINES[start] != opts.sentence_delim:
		start -= 1
	end = line_index + 1
	while False if end >= len(LINES) else LINES[end] != opts.sentence_delim:
		end += 1

	sentence = [ ln.split(opts.tag_flag)[CONLL].strip()
		for ln in LINES[start+1:end] ]

	return " ".join(sentence)

output = ["all lines tagged in '"+opts.prefix+"'...:"]
if not opts.context:
	output = [ln for ln in LINES if ln.strip() != '']
	output = [ln for ln in output if is_target(ln)]
else:
	output += [("Token\tTag" if CONLL else "Tag\tToken") + "\tSentence"]
	for i in range(len(LINES)):
		if is_target(LINES[i]):
			output += [ LINES[i].strip() + get_context_sentence(i) ]
	#output = [("Token\tTag" if CONLL else "Tag\nToken") + "\tSentence"] + [ LINES[i].strip() + get_context_sentence(i) for i in range(len(LINES))]

with open(sys.argv[2], mode='w') as f:
	f.write("\n".join(output))



