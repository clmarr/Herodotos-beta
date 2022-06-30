import sys
import optparse

# at present, this assumes input file is in CRF or CONLL format
# usage: python3 extract_taggings.py <input> <output> (-p prefix) (-c [True if want to report context sentence]) (-s [sentence delimiter token])

optparser = optparse.OptionParser()
optparser.add_option("-p", "--prefix", default=False, help="If you specify a prefix, only tags beginning in the sequence entered will be reported")
optparser.add_option("-c", "--context", default=False, help="If context is specified, the sentence where the tag occured will be reported.")
optparser.add_option("-t", "--tag_flag", default='\t', help="Token delimiting tag from token in input file.")
optparser.add_option("-s", "--sentence_delim", default='\n', help="Sentence delimiter token -- a line equivalent to this token (without stripping) will be considered to mark a sentence boundary.")
optparser.add_option("-f", "--format", default="crf", help="Format of input file. (Currently accepted formats: CRF, CONLL)")

OPTS, args = optparser.parse_args()

if OPTS.format.lower() not in ["conll", "crf"]:
	raise Exception("Usage error: only accepted formats are CONLL and CRF currently.")
CONLL = OPTS.format.lower() == "conll"

def tag_tok_tuple(line):
	tup = line.strip().split(OPTS.tag_flag)
	return tup[not CONLL] + "_" + tup[CONLL]

# assumes that the line input is a CRF or CONLL formatted line
def is_target(line):
	tup = line.strip().split(OPTS.tag_flag)
	if OPTS.prefix:
		return tup[CONLL][:len(OPTS.prefix)] == OPTS.prefix
	return tup[CONLL] == '0'

LINES = []
with open(sys.argv[1]) as f:
	LINES += f.readlines()

def get_context_sentence(line_index):
	if not OPTS.context:
		return ''

	start = line_index - 1
	while False if start < 0 else LINES[start] != OPTS.sentence_delim:
		start -= 1
	end = line_index + 1
	while False if end >= len(LINES) else LINES[end] != OPTS.sentence_delim:
		end += 1

	sentence = [ tag_tok_tuple(ln) for ln in LINES[start+1:end] ]

	return " ".join(sentence)

output = ["all lines tagged in '" + OPTS.prefix + "'...:"]
if not OPTS.context:
	output = [ln for ln in LINES if ln.strip() != '']
	output = [ln for ln in output if is_target(ln)]
else:
	output += [("Token\tTag" if CONLL else "Tag\tToken") + "\tSentence"]
	for i in range(len(LINES)):
		if is_target(LINES[i]):
			output += [ LINES[i].strip() + "\t" + get_context_sentence(i) ]
	#output = [("Token\tTag" if CONLL else "Tag\nToken") + "\tSentence"] + [ LINES[i].strip() + get_context_sentence(i) for i in range(len(LINES))]

with open(sys.argv[2], mode='w') as f:
	f.write("\n".join(output))



