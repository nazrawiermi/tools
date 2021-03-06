"""
A module with a handful of utility functions for dealing with
file I/O
"""

import codecs
import sys
import io
import os

COLCOUNT=10
ID,FORM,LEMMA,CPOSTAG,POSTAG,FEATS,HEAD,DEPREL,DEPS,MISC=range(COLCOUNT)
COLNAMES=u"ID,FORM,LEMMA,CPOSTAG,POSTAG,FEATS,HEAD,DEPREL,DEPS,MISC".split(u",")


def in_out(args):
    """
    Open the input/output data streams.
    """
    #Decide where to get the data from
    if args.input is None or args.input=="-": #Stdin
        inp=codecs.getreader("utf-8")(os.fdopen(0,"U")) #Switched universal newlines on
    else: #File name given
        inp_raw=open(args.input,"U")
        inp=codecs.getreader("utf-8")(inp_raw)
    #inp is now an iterator over lines, giving unicode strings

    if args.output is None or args.output=="-": #stdout
        out=codecs.getreader("utf-8")(sys.stdout)
    else: #File name given
        out=codecs.open(args.output,"w","utf-8")
    return inp,out

def print_tree(comments,tree,out):
    if comments:
        print >> out, u"\n".join(comments)
    for cols in tree:
        print >> out, u"\t".join(cols)
    print >> out

def trees(inp):
    """
    `inp` a file-like object yielding lines as unicode
    
    Yields the input a tree at a time.
    """
    comments=[] #List of comment lines to go with the current tree
    lines=[] #List of token/word lines of the current tree
    for line_counter, line in enumerate(inp):
        line=line.rstrip()
        if not line: #empty line
            if lines: #Sentence done, yield. Skip otherwise.
                yield comments, lines
                comments=[]
                lines=[]
        elif line[0]==u"#":
            comments.append(line)
        elif line[0].isdigit():
            cols=line.split(u"\t")
            if len(cols)!=COLCOUNT:
                warn(u"Line %d: The line has %d columns, but %d are expected. Giving up."%(line_counter+1,len(cols),COLCOUNT))
                sys.exit(1)
            lines.append(cols)
        else: #A line which is not a comment, nor a token/word, nor empty. That's bad!
            #TODO warn!
            sys.exit(1) #Give a non-zero exit code
    else: #end of file
        if comments or lines: #Looks like a forgotten empty line at the end of the file, well, okay...
            yield comments, lines

