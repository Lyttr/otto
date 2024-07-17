import wave
import numpy as np
import os
import pandas as pd
from pydub import AudioSegment
from pydub import effects
import math
def ottoList(path):
    wavList=[]
    with os.scandir(path) as files:
        for file in files:
            
            
            wavList.append(file.name)
               
    return wavList
def ottoAnalyse(path):
    ottoInfo=pd.DataFrame(columns=['name','length','amplitude'])
    wavList=ottoList(path)
    for name in wavList:
        ottoWord=AudioSegment.from_wav(path+name)
       
        ottoInfo=ottoInfo._append(pd.DataFrame([[name,ottoWord.duration_seconds,ottoWord.dBFS]],columns=['name','length','amplitude']),ignore_index=True)
       
    ottoInfo.to_excel('otto.xlsx')
def speedSet(input,output,ratio):
    cmd="ffmpeg -y -i %s -filter_complex \"atempo=tempo=%f\" %s" % (input,ratio,output)
    os.system(cmd)
def durationPreprocess(path,min,max):
    
   
    wavList=ottoList(path)
    for name in wavList:
        ottoWord=AudioSegment.from_wav(path+name)
        ratio=min/ottoWord.duration_seconds
        if(math.log2(ratio)>1):
            for i in range(math.floor(math.log2(ratio))+1):
                speedSet(path+name,'./temp/'+'temp.wav',0.5)
                temp=AudioSegment.from_wav('./temp/'+'temp.wav')
                temp.export(path+name,format='wav')
            speedSet('./temp/'+'temp.wav',path+name,temp.duration_seconds/min)
        elif(math.log2(ratio)<=1 and math.log2(ratio)>0):
            speedSet(path+name,'./temp/'+'temp.wav',1.0/ratio)
            temp=AudioSegment.from_wav('./temp/'+'temp.wav')
            temp.export(path+name,format='wav')        

def amplitudePreprocess(path,min,max):
    wavList=ottoList(path)
    for name in wavList:
        ottoWord=AudioSegment.from_wav(path+name)
        if(ottoWord.dBFS<min):
            ottoWord=ottoWord+min-ottoWord.dBFS
            ottoWord.export(path+name,format='wav')
if __name__ == '__main__':
    path='./resource/'
   
    durationPreprocess(path,0.5,1.0)
    #amplitudePreprocess(path,-10,0)
    ottoAnalyse(path)
    