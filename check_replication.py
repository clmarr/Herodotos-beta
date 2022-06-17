import optparse
import numpy as np

# @author: Clayton Marr (cl.st.marr@gmail.com)
# @date: June 17 2022
# check if two output files of tagging for the same text are tagged the same,
# output line by line mismatches to a file suffixed in "-errors.txt"
# output confusion matrix to file suffixed in "-cm.txt"
# checks for files of crf and conll format only at present.

optparser = optparse.OptionParser()
optparser.add_option("-o", "--old", default="", help="Location of older results file")
optparser.add_option("-n", "--new", default="", help="Location of newer results file")
optparser.add_option("--oldFormat", default="crf", help="Old file format")  # else must be conll
optparser.add_option("--newFormat", default="crf", help="New file format")  # else must be conll
optparser.add_option("-p", "--prefix", default="", help="Prefix for output files")
opts, args = optparser.parse_args()
if "" in [opts.old, opts.new]:
    optparser.error("At least one of the two results comparanda not specified!")
if not opts.prefix:
    optparser.error("Prefix for output files must be specified!")
if False in [i in ["crf", "conll"] for i in [opts.oldFormat, opts.newFormat]]:
    optparser.error("The only valid formats are 'crf' and 'conll'!")


def extract_annotation(inp, mode):
    inp = inp.strip().split("\t")
    return inp[mode == "conll"], inp[mode != "conll"]  # tag, token

confusion_matrix = {} # of format: old[new]
errors = []

with open(opts.new) as newF:
    newLines = newF.readlines()
with open(opts.old) as oldF:
    oldLines = oldF.readlines()

li=0
while 0 not in [len(newLines), len(oldLines)]:
    li+=1
    if newLines[0].strip() == "":
        newLines= newLines[1:]; continue
    if oldLines[0].strip() == "":
        oldLines= oldLines[1:]; continue
    if "\t" not in newLines[0] or "\t" not in oldLines[0]:
        raise Exception("Format error: tab delimiter absent!")
        # i.e. a violation of the current basis of both conll and crf formats within this project, both tab delim'd
    ntup, otup = extract_annotation(newLines[0], opts.newFormat), \
                 extract_annotation(oldLines[0], opts.oldFormat) #(tag, token) tuples.
    if ntup[1] != otup[1]:
        raise Exception("Alignment error!: "+ntup[1]+" || "+otup[1])

    #process
    newLines, oldLines = newLines[1:], oldLines[1:]
    if ntup[0] != otup[0]:
        errors += [ otup[0] + "::" + ntup[0] + "\t" + otup[1] ]
        if otup[0] not in confusion_matrix.keys():
            confusion_matrix[otup[0]] = {ntup[0]:1}; continue
        if ntup[0] not in confusion_matrix[otup[0]].keys():
            confusion_matrix[otup[0]][ntup[0]] = 1; continue
        confusion_matrix[otup[0]][ntup[0]] += 1

if len(newLines) or len(oldLines): #i.e. if either one isn't zero.
    old_is_rem = len(oldLines) > len(newLines)
    rem_lines = [newLines, oldLines][old_is_rem] #grabs the one with remaining lines
    while False if len(rem_lines) == 0 else rem_lines[0].strip()=='':
        rem_lines = rem_lines[1:]
    if len(rem_lines) != 0:
        print("Warning: lines remaining in "+["new","old"][old_is_rem]+":\n"
              +"\n".join([newLines,oldLines][old_is_rem]))

if len(errors): #i.e. if there are errors.

    # build confusion matrix array...
    old_err_tags = list(confusion_matrix.keys()) #recall that the "outer" keys are the ones for the 'old' tagging output file
    old_err_tags.sort()

    new_err_tags = []
    for k in old_err_tags:
        for ki in confusion_matrix[k].keys():
            if ki not in new_err_tags:
                new_err_tags+=[ki]
    new_err_tags.sort()

    cm_arr = np.zeros(  # get it? :)
        [len(old_err_tags), len(new_err_tags)])

    # anyhow, new_err_tags and old_err_tags will enforce consistent row and column locations.
    for oi in old_err_tags:
        for ni in confusion_matrix[oi].keys():
            cm_arr[old_err_tags.index(oi)][new_err_tags[ni]] = confusion_matrix[oi][ni]

    # write the files.
    f = open(opts.prefix+"-errors.txt")
    f.write("\n".join(errors))
    f.close()

    f2 = open(opts.prefix+"-cm.txt")
    f2.write(
        "\n".join(
            ["\t".join(["."] + new_err_tags)]
            +
            ["\t".join([old_err_tags[oti]]+ list(cm_arr[oti]))
                for oti in range(len(old_err_tags))])
        )
    f2.close()




