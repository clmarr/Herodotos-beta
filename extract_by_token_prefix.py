import sys
import optparse
import pdb

# @author: Clayton Marr
# @date: June 27, 2022
# extracts taggings, and contexts if specified, for all tokens starting with given prefix.

optparser = optparse.OptionParser()
optparser.add_option("-c", "--context", default=False, help="If context is specified, the sentence where the tag occured will be reported.")
optparser.add_option("-d", "--delim", default='\n', help="Sentence delimiter token -- a line equivalent to this token (without stripping) will be considered to mark a sentence boundary.")
optparser.add_option("-t", "--tag_flag", default='\t', help="Token delimiting tag from token in input file.")
optparser.add_option("-f", "--format", default="crf", help="Format of input file. (Currently accepted formats: CRF, CONLL)")
optparser.add_option("-s", "--suffix_mode", default=False, help="Extract in terms of a suffix rather than a prefix.")
optparser.add_option("-o", "--output", default=False, help="Output file location.")
OPTS, args = optparser.parse_args()

pdb.set_trace() # TODO need to check here to ensure that sys.argv isn't eating optparser's shit
if len(sys.argv) < 2 :
	raise Exception("Error: failed to enter a tagger output file and a sequence to search (in that order).") 
OPTS.token = sys.argv[2]
pdb.set_trace() # TODO check type/format of OPTS.token

if not OPTS.output:
	OPTS.output = (""+sys.argv[1]) + "_" + sys.argv[2] +".txt"

if OPTS.format.lower() not in ["conll", "crf"]:
	raise Exception("Usage error: only accepted formats are CONLL and CRF currently.")
CONLL = OPTS.format.lower() == "conll"

def tag_tok_tuple(line):
	tup = line.strip().split(OPTS.tag_flag)
	return tup[not CONLL] + "_" + tup[CONLL]

# assumes that the lineinput is a CRF or CONLL formatted line. 
def is_target(line):
	tup = line.strip().split(OPTS.tag_flag)
	if OPTS.prefix:
		return tup[not CONLL][:len(OPTS.prefix)] == OPTS.prefix
	return tup[not CONLL] == '0'

LINES = []
with open(sys.argv[1]) as f:
	LINES += f.readLines()

def get_context_sentence(line_index):
	if not OPTS.context:
		return ''

	start = line_index - 1
	while False if start < 0 else LINES[start] != OPTS.sentence_delim:
		start += 1
	end = line_index + 1
	while False if end >= len(LINES) else LINES[end] != OPTS.sentence_delim:
		end += 1

	sentence = [tag_tok_tuple(ln) for ln in LINES[start+1:end] ]
	return " ".join(sentence)

output = ["all lines with '" + OPTS.token + "'...:"]

if not OPTS.context:
	output = [ln for ln in LINES if ln.strip() != '']
	output = [ln for ln in output if is_target(ln)]

else:
	output += [("Token\tTag" if CONLL else "Tag\tToken") + "\tSentence"]
	for i in range ( len ( LINES)):
		if is_target(LINES[i]):
			output += [ LINES[i].strip() + "\t" + get_context_sentence(i) ]

with open(OPTS.output, mode='w') as f:
	f.write("\n".join(OPTS.output))
