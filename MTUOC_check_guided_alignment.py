import codecs
import sys
import shutil
import os

def check(fileL1,fileL2,fileweights,alignmentFWD,alignmentREV):
    shutil.copyfile(fileL1, 'fileL1.temp')
    shutil.copyfile(fileL2, 'fileL2.temp')
    if not fileweights==None:
        shutil.copyfile(fileweights, 'fileweights.temp')
    shutil.copyfile(alignmentFWD, 'alignmentFWD.temp')
    shutil.copyfile(alignmentREV, 'alignmentREV.temp')
    fileL1IN=codecs.open('fileL1.temp',"r",encoding="utf-8")
    fileL2IN=codecs.open('fileL2.temp',"r",encoding="utf-8")
    if not fileweights==None:
        fileweightsIN=codecs.open('fileweights.temp',"r",encoding="utf-8")
    
    alignmentFWDIN=codecs.open('alignmentFWD.temp',"r",encoding="utf-8")
    alignmentREVIN=codecs.open('alignmentREV.temp',"r",encoding="utf-8")    
    fileL1OUT=codecs.open(fileL1,"w",encoding="utf-8")
    fileL2OUT=codecs.open(fileL2,"w",encoding="utf-8")
    if not fileweights==None:
        fileweightsOUT=codecs.open(fileweights,"w",encoding="utf-8",errors="replace")
    alignmentFWDOUT=codecs.open(alignmentFWD,"w",encoding="utf-8",errors="replace")
    alignmentREVOUT=codecs.open(alignmentREV,"w",encoding="utf-8",errors="replace")
    cont=0
    while 1:
        cont+=1
        liniaL1=fileL1IN.readline().rstrip()
        if not liniaL1:
            break
        liniaL2=fileL2IN.readline().rstrip()
        if not fileweights==None:
            liniaweights=fileweightsIN.readline().rstrip()
        liniaalignmentFWD=alignmentFWDIN.readline().rstrip()
        liniaalignmentREV=alignmentREVIN.readline().rstrip()
        if not len(liniaalignmentFWD)==0 and not len(liniaalignmentREV)==0:
            fileL1OUT.write(liniaL1+"\n")
            fileL2OUT.write(liniaL2+"\n")
            if not fileweights==None:
                fileweightsOUT.write(liniaweights+"\n")
            alignmentFWDOUT.write(liniaalignmentFWD+"\n")
            alignmentREVOUT.write(liniaalignmentREV+"\n")
        else:
            print("Deleting line ",cont)
    
    os.remove('fileL1.temp')
    os.remove('fileL2.temp')
    if not fileweights==None:
        os.remove('fileweights.temp')
    os.remove('alignmentFWD.temp')
    os.remove('alignmentREV.temp')

if __name__ == "__main__":
    try:
        fileL1=sys.argv[1]
        fileL2=sys.argv[2]
        fileweights=sys.argv[3]
        print(fileweights,type(fileweights))
        if fileweights=="None": fileweights=None
        print(fileweights,type(fileweights))
        alignmentFWD=sys.argv[4]
        alignmentREV=sys.argv[5]
        print(fileL1,fileL2,fileweights,alignmentFWD,alignmentREV)
        check(fileL1,fileL2,fileweights,alignmentFWD,alignmentREV)
    except:
        print(sys.exc_info())
        print("ERROR: use the following command:")
        print("python3 MTUOC_check_guided_alignment.py fileL1 fileL2 weights alignmentFWD alignmentREV")
        print("If no weights are used, state None for weights file.")
