import sys
import os
import optparse
# import pdb

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

if False if len(sys.argv) < 2 else sys.argv[2][0] == '-':
	raise Exception("Error: failed to enter a tagger output file and a sequence to search (in that order). "
					"Option flags (with '-') must only come afterward.")
OPTS.token = sys.argv[2]

if not OPTS.output:
	OPTS.output = (""+sys.argv[1]) + "_" + sys.argv[2] +".txt"

if OPTS.format.lower() not in ["conll", "crf"]:
	raise Exception("Usage error: only accepted formats are CONLL and CRF currently.")
CONLL = OPTS.format.lower() == "conll"

def tag_tok_tuple(line):
	tup = line.strip().split(OPTS.tag_flag)
	return tup[not CONLL] + "_" + tup[CONLL]

# assumes that the line input is a CRF or CONLL formatted line.
def is_target(line):
	if OPTS.tag_flag not in line:
		return False
	tok = line.strip().split(OPTS.tag_flag)[not CONLL]
	if len(tok) < len(OPTS.token):
		return False
	if OPTS.suffix_mode:
		return tok[len(tok) - len(OPTS.token) :].lower() == OPTS.token.lower()
	return OPTS.token.lower() == tok[:len(OPTS.token)].lower()

LINES = []
with open(os.path.normpath(sys.argv[1])) as f:
	LINES += f.readlines()

def get_context_sentence(line_index):
	if not OPTS.context:
		return ''

	start = line_index - 1
	while False if start < 0 else LINES[start] != OPTS.delim:
		start -= 1
	end = line_index + 1
	while False if end >= len(LINES) else LINES[end] != OPTS.delim:
		end += 1

	sentence = [tag_tok_tuple(ln) for ln in LINES[start+1:end] ]
	return " ".join(sentence)

out_text = ["all lines with '" + OPTS.token + "'...:"]

if not OPTS.context:
	out_text = [ln for ln in LINES if ln.strip() != '']
	out_text = [ln for ln in out_text if is_target(ln)]

else:
	out_text += [("Token\tTag" if CONLL else "Tag\tToken") + "\tSentence"]
	for i in range ( len ( LINES)):
		if is_target(LINES[i]):
			out_text += [ LINES[i].strip() + "\t" + get_context_sentence(i) ]

with open(os.path.normpath(OPTS.output), mode='w') as f:
	f.write("\n".join(out_text))
