from pydub import AudioSegment
from pydub.playback import play
import os
import preprocess
from xpinyin import Pinyin
from playsound import playsound
path = './resource/'
ottolist = preprocess.ottoList(path)
controlList = ['！']
nonChinese = {
    'a': 'ei',
    'b': 'bi',
    'c': 'xi',
    'd': 'di',
    'e': 'yi',
    'f': ['ai', 'fu'],
    'g': 'ji',
    'h': ['ai', 'chi'],
    'i': 'ai',
    'j': 'zhei',
    'k': 'kei',
    'l': ['ai', 'lu'],
    'm': ['ai', 'mu'],
    'n': 'en',
    'o': 'ou',
    'p': 'pi',
    'q': 'kiu',
    'r': 'a',
    's': ['ai', 'si'],
    't': 'ti',
    'u': 'you',
    'v': 'wei',
    'w': ['da', 'bu', 'liu'],
    'x': ['ai', 'ke', 'si'],
    'y': 'wai',
    'z': 'zei',
    '0': 'ling',
    '1': 'yi',
    '2': 'er',
    '3': 'san',
    '4': 'si',
    '5': 'wu',
    '6': 'liu',
    '7': 'qi',
    '8': 'ba',
    '9': 'jiu',
    '。': 'juhao',
    '，': 'douhao',
    ',': 'juhao',
    '.': 'douhao'
}


def getOtto(name: str):
    if name+'.wav' in ottolist:
        return AudioSegment.from_wav(path+name+'.wav')
    else:
        print(name+' not found')
        return AudioSegment.empty()


def pinyin2otto(pinyinList: list):
    ottoWav = AudioSegment.empty()
    for i in range(len(pinyinList)):
        if pinyinList[i] in controlList:
            continue
        elif (i != len(pinyinList)-1 and pinyinList[i+1] in controlList):
            if(pinyinList[i+1] == '！'):
                ottoWord = getOtto(pinyinList[i])+20

        else:
            ottoWord = getOtto(pinyinList[i])
        ottoWav = ottoWav+ottoWord

    return ottoWav


def word2pinyin(word: str):
    pinyinList = []
    p = Pinyin()
    for i in word:
        if i in nonChinese:
            if(type(nonChinese.get(i)) is list):
                for j in nonChinese.get(i):
                    pinyinList.append(j)
            else:
                pinyinList.append(nonChinese.get(i))
        elif i in controlList:
            pinyinList.append(i)
        else:
            pinyinList.append(p.get_pinyin(i))
    return pinyinList


if __name__ == '__main__':
    
    word="它的优点在于计算的范围取决于箱子容量。可以计算大树乘法。谢谢大家的观看。"
    
    bing = pinyin2otto(word2pinyin(word))
    bing.export('./output/output.wav', format='wav')

    
