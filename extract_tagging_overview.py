# will extract all times a certain tag is used in an output file, in CRF or CONLL format, and...
	# report them in alphabetical order,
	# with the number of instances the tag was given to tokens of that type delimited using defined delimiter from the token that was tagged
#usage : 
#python3 extract_tagging_overview.py -p/--prefix <tagOrTagPrefix> -i/--input <inputfile> (-o/--output <outputfile>) (-f/--format <CRF or CONLL>)  (-t/--tag_flag <tagTokenDelimiterInInputFile>) (-d/--delim_output <delimiterInOutputFile) (-e <encoding of input file>)

import optparse
import chardet
import pdb

optparser = optparse.OptionParser()
optparser.add_option("-p", "--prefix", default=False, help="Tag or beginning of tag to report results for")
optparser.add_option("-i", "--input", default=False, help="Location for input file.")
optparser.add_option("-o", "--output", default=False, help="Location for output file.")
optparser.add_option("-t", "--tag_flag", default='\t', help="Token delimiting tag from token in input file.")
optparser.add_option("-f", "--format", default="crf", help="Format of input file. (Currently accepted formats: CRF, CONLL)")
optparser.add_option("-d", "--delim_output", default="\t", help="Delimiter between token and number of times tagged for the output file.")
optparser.add_option("-e", "--encoding", default='utf-8', help="Encoding of the input file, set to false if you want to check for it.")

OPTS, args = optparser.parse_args()

if not OPTS.prefix:
    raise Exception("Usage error: need to specify tag or tag prefix (flag with -p or --p).")
if not OPTS.input:
    raise Exception("Usage error: need to specify input file (flag with -i or --input).")
if not OPTS.output:
    OPTS.output = OPTS.input+"_"+OPTS.prefix+"_summary"
if OPTS.format.lower() not in ["conll", "crf"]:
    raise Exception("Usage error: only accepted formats are CONLL and CRF currently.")
CONLL = OPTS.format.lower() == "conll"

# assumes that the line input is a CRF or CONLL formatted line
def is_target(line):
    tup = line.strip().split(OPTS.tag_flag)
    return tup[CONLL][:len(OPTS.prefix)] == OPTS.prefix

if not OPTS.encoding or OPTS.encoding.lower() == "false":
    #try to troubleshoot any encoding bs.
    fi = open(OPTS.input, 'rb')
    enco = chardet.detect(fi.read())
    fi.close()
    OPTS.encoding = enco['encoding']
    print("Encoding detected : "+OPTS.encoding+" (confidence: "+str(enco['confidence'])+").")

f = open(OPTS.input, encoding=OPTS.encoding)
LINES = [ln.strip() for ln in f.readlines() if OPTS.tag_flag in ln]
f.close()

COUNTS = {}
for ln in [line for line in LINES if is_target(line)]:
    token = ln.split(OPTS.tag_flag)[not CONLL].strip()
    if token not in COUNTS:
        COUNTS[token] = 1
    else:
        COUNTS[token] += 1

if len(COUNTS) == 0:
    raise Exception("Error: the tag (or tag prefix) provided ("+OPTS.prefix+") was never found in the file "+OPTS.input)

pdb.set_trace()

f = open(OPTS.output, mode='w')
f.write(
    "\n".join( [str(ti[0])+OPTS.delim_output+str(ti[1]) for ti in sorted(COUNTS.items())] )
)
f.close()
