#!/bin/python3
import numpy, os, subprocess, imagesize, pandas
"""
Tristan Anderson
tanderson@vt.edu
https://github.com/Tristan-Anderson/PRLWordCountCalculator

FORTUNE:

Blessed is he who expects nothing, for he shall never be disappointed.
		-- Alexander Pope
"""
############ EDIT HERE ##############
docpath = "/home/kb/nlnl/env/"
texpath = docpath+"mainPRL.tex"
####################################
"""
    Now, don't touch anything else.
"""
#################################
texcountpath = "/usr/bin/texcount"

encoding = "utf-8"
try:
    p = subprocess.Popen([texcountpath,texpath],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    TCout, err = p.communicate()
except Exception as e:
    print(e)
    print("It is likely you don't have texcount installed in '/usr/bin/texcount', see https://app.uio.no/ifi/texcount/")


p = subprocess.Popen("ls "+docpath+"*.png",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
EXout, err = p.communicate()


EXout = EXout.decode(encoding)
TCout = TCout.decode(encoding)

words = ["Words in text:", "Words outside text"]
math = ["Number of math displayed:"]
ton = TCout.split('\n')
eon = EXout.split('\n')

#GET WORDS
W = 0
M = 0

for line in ton:
    if any(m in line for m in words):
        tl = line.split(":")
        W +=int(tl[-1])
    if any(m in line for m in math):
        tl = line.split(":")
        M += int(tl[-1])
fr = {}
for line in eon:
    if line == '':
        continue
    w,h = imagesize.get(line)
    aspect = w/h
    d = 300 / (0.5 * aspect) + 40
    s = d/2
    fr[line] = {"aspect": aspect, "double":d, "single":s}
df = pandas.DataFrame(fr).transpose()

decs = ["d", "s", "x"]
mp = [1,2, 3]
uc = dict(zip(decs,mp))
FIGS = 0
for index,row in df.iterrows():
    print("#"*25)
    print("Filename\t","Double\t","Single\t")
    print(index, row["double"], row["single"])
    choice = 'z'
    while choice.lower() not in decs:
        choice = input("Double (d), Single (s), Exclude (x): ")
    match uc[choice]:
        case 1:
            FIGS += row["double"]
        case 2:
            FIGS += row["single"]
        case 3:
            continue

M = M*16 # Each mathematical line counts as 16 words.
print("RAW WORDS:", W, "MATH WC:", M, "FIGURES:",FIGS)
print("TOTAL:",W+M+FIGS)
