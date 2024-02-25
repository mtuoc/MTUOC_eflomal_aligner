#    MTUOC_eflomal_aligner
#    Copyright (C) 2024 Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import eflomal
import codecs
import sys
from itertools import (takewhile,repeat)
import shutil
import os
import glob
import argparse
import io



def rawincount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )

def splitFile(filename,limits):
    entrada=codecs.open(filename,"r",encoding="utf-8")
    cont=1
    suffix="_"+str(cont)+".temp"
    sname=filename+suffix
    sortida=codecs.open(sname,"w",encoding="utf-8")
    contlinia=0
    for linia in entrada:
        linia=linia.rstrip()
        sortida.write(linia+"\n")
        contlinia+=1
        if contlinia>=limits[cont]:
            contlinia=0
            sortida.close()
            cont+=1
            suffix="_"+str(cont)+".temp"
            sname=filename+suffix
            sortida=codecs.open(sname,"w",encoding="utf-8")
    sortida.close()
    entrada.close()
    
def align_corpus(corpusL1,corpusL2,aliFWD,aliREV,inpriorsFILE,outpriorsFILE,limit,cont):
    aligner = eflomal.Aligner()
    sortidaFWD=codecs.open(aliFWD,"w",encoding="utf-8")
    sortidaREV=codecs.open(aliREV,"w",encoding="utf-8")
    for i in range(1,cont+1):
        print("Aligning part",i)
        suffix="_"+str(i)+".temp"
        CL1=corpusL1+suffix
        CL2=corpusL2+suffix
        FWD="FWD"+suffix
        REV="REV"+suffix
        PRIORS="PRIORS"+suffix
        if i==1:
            if inpriorsFILE==None:
                with open(CL1, 'r', encoding='utf-8') as src_data, open(CL2, 'r', encoding='utf-8') as trg_data, open(PRIORS, 'w', encoding='utf-8') as priors_f:
                    aligner.align(src_data, trg_data,links_filename_fwd=FWD, links_filename_rev=REV)
            else:
                with open(CL1, 'r', encoding='utf-8') as src_data, open(CL2, 'r', encoding='utf-8') as trg_data, open(inpriorsFILE, 'r', encoding='utf-8') as priors_data, open(PRIORS, 'w', encoding='utf-8') as priors_f:
                    aligner.align(src_data, trg_data,links_filename_fwd=FWD, links_filename_rev=REV, priors_input=priors_data)
            
            with open(CL1, 'r', encoding='utf-8') as src_data, open(CL2, 'r', encoding='utf-8') as trg_data, open(FWD, 'r', encoding='utf-8') as fwd_links, open(REV, 'r', encoding='utf-8') as rev_links, open(PRIORS, 'w', encoding='utf-8') as priors_f:
                # Estimate priors
                priors_tuple = eflomal.calculate_priors(src_data, trg_data, fwd_links, rev_links)
                # Write priors to file
                eflomal.write_priors(priors_f, *priors_tuple)
        else:
            suffixprev="_"+str(i-1)+".temp"
            PREVPRIORS="PRIORS"+suffixprev
            with open(CL1, 'r', encoding='utf-8') as src_data, open(CL2, 'r', encoding='utf-8') as trg_data, open(PREVPRIORS, 'r', encoding='utf-8') as priors_data, open(PRIORS, 'w', encoding='utf-8') as priors_f:
                aligner.align(src_data, trg_data,links_filename_fwd=FWD, links_filename_rev=REV, priors_input=priors_data)
            with open(CL1, 'r', encoding='utf-8') as src_data, open(CL2, 'r', encoding='utf-8') as trg_data, open(FWD, 'r', encoding='utf-8') as fwd_links, open(REV, 'r', encoding='utf-8') as rev_links, open(PRIORS, 'w', encoding='utf-8') as priors_f:
                # Estimate priors
                priors_tuple = eflomal.calculate_priors(src_data, trg_data, fwd_links, rev_links)
                # Write priors to file
                eflomal.write_priors(priors_f, *priors_tuple)
                # Estimate priors
                priors_tuple = eflomal.calculate_priors(src_data, trg_data, fwd_links, rev_links)
                # Write priors to file
                eflomal.write_priors(priors_f, *priors_tuple)
                
        #concatenating alignments
        entradaFWD=codecs.open(FWD,"r",encoding="utf-8")
        for linia in entradaFWD:
            linia=linia.rstrip()
            sortidaFWD.write(linia+"\n")
        entradaFWD.close()
        
        entradaREV=codecs.open(REV,"r",encoding="utf-8")
        for linia in entradaREV:
            linia=linia.rstrip()
            sortidaREV.write(linia+"\n")
        entradaREV.close()
        os.remove(FWD)
        os.remove(REV)
        if i>1:
            os.remove(PREVPRIORS)
    shutil.copyfile(PRIORS, outpriorsFILE)
    todeletetemp=glob.glob('./*.temp')
    for filename in todeletetemp:
        os.remove(filename)
    

def go_corpus(corpusL1,corpusL2,aliFWD,aliREV,inpriors,outpriors,limit):
    numlinesL1=rawincount(corpusL1)
    numlinesL2=rawincount(corpusL2)
    if not numlinesL1==numlinesL2:
        print("ERROR: corpusL1 and corpusL2 have different number of lines. Exiting.")
        sys.exit()
    limits={}
    parts=numlinesL1//limit
    if parts==0: parts=1
    numlinespart=numlinesL1//parts
    remanent=numlinesL1-numlinespart*parts

    for i in range(1,parts+1):
        limits[i]=numlinespart
        if i==1: limits[i]+=remanent
    splitFile(corpusL1,limits)
    splitFile(corpusL2,limits)
    align_corpus(corpusL1,corpusL2,aliFWD,aliREV,inpriors,outpriors,limit,parts)

def align_sentence(sentenceL1,sentenceL2,priors): 
    aligner = eflomal.Aligner()
    src_data = io.StringIO(sentenceL1)
    trg_data = io.StringIO(sentenceL2)
    priors_data=open(priors,"r")

    aligner.align(src_data, trg_data,links_filename_fwd="FWD.temp", links_filename_rev="REV.temp",priors_input=priors_data)
    aliFWD=open("FWD.temp","r").readline().strip()
    aliREV=open("REV.temp","r").readline().strip()
    os.remove("FWD.temp")
    os.remove("REV.temp")
    return(aliFWD,aliREV)

def go_sentence(sentenceL1,sentenceL2,priors):
    (aliFWD,aligREV)=align_sentence(sentenceL1,sentenceL2,priors)
    return(aliFWD,aligREV)
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MTUOC_eflomal_aligner: command line tool to align a corpus or a pair of sentences using eflomal.')
    parser.add_argument('--cL1', dest='cL1', help='The corpus for language 1 (for corpus mode).', action='store',required=False)
    parser.add_argument('--cL2', dest='cL2', help='The corpus for language 2 (for corpus mode).', action='store',required=False)
    parser.add_argument('--sL1', dest='sL1', help='The sentence for language 1 (for sentence mode).', action='store',required=False)
    parser.add_argument('--sL2', dest='sL2', help='The sentence for language 2 (for sentence mode).', action='store',required=False)
    parser.add_argument('--fwd', dest='fwd', help='The forward alignment.', action='store',required=False)
    parser.add_argument('--rev', dest='rev', help='The reverse alignment.', action='store',required=False)
    parser.add_argument('--inpriors', dest='inpriors', help='The input priors file to use. If not stated, not priors files will be used to start with the alignment. This parameter is compulsory when aligning sentences.', action='store',required=False)
    parser.add_argument('--outpriors', dest='outpriors', help='The output priors file that will be generated after the alignment. If not stated, the priors files will be called eflomal.priors.', action='store',required=False)
    parser.add_argument('--limit', dest='limit', help='The limit of sentences to process.', type=int, action='store',required=False)
    args = parser.parse_args()
    corpusL1=args.cL1
    corpusL2=args.cL2
    sentenceL1=args.sL1
    sentenceL2=args.sL2
    aliFWD=args.fwd
    aliREV=args.rev
    inpriors=args.inpriors
    outpriors=args.outpriors
    if outpriors==None:
        outpriors="eflomal.priors"
    if not args.limit==None:
        limit=int(args.limit)
    else:
        limit=5000000
    if not corpusL1==None and not corpusL2==None:
        go_corpus(corpusL1,corpusL2,aliFWD,aliREV,inpriors,outpriors,limit)
    elif not sentenceL1==None and not sentenceL2==None:
        if inpriors==None:
            print("ERROR: to align sentences a priors file should be used. Use the --inpriors option to set the priors file to use")
            sys.exit()
        (aliFWD,aligREV)=go_sentence(sentenceL1,sentenceL2,inpriors)
        print(aliFWD,"/",aligREV)
        
    
