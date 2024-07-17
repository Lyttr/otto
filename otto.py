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
    #word='大家好 我是里铁 我是承德土皇帝'
   # f=
    word="它的优点在于计算的范围取决于箱子容量。可以计算大树乘法。谢谢大家的观看。"
    #word = "下面我简单介绍一下工作原理。通过使用肉斗和侦车器。第一个箱子每输出一次，第二个箱子输出全部物品。再通过弹射置物台返回箱子。再由一个侦车器负责计数和保存结果。"
    # word='差不多得了,屁大点事都要拐上原神，原神一没招你惹你，二没干伤天害理的事情，到底怎么你了让你一直无脑抹黑，米哈游每天费尽心思的文化输出弘扬中国文化，你这种喷子只会在网上敲键盘诋毁良心公司，中国游戏的未来就是被你这种人毁掉的'
    bing = pinyin2otto(word2pinyin(word))
    bing.export('./output/output6.wav', format='wav')

    # playsound('./output/output.wav')
