#!/usr/bin/python
from tinytag import TinyTag
import os
import sys
import math



def generateFile(bpm, count, offset=0):
    curbeat = offset
    result = ['0']

    #beats per milisecond
    bpms = bpm/60/1000
    #length in milliseconds

    incr = 1/bpms
    curbeat = offset + incr
    for i in range(count-1):
        result.append(str(round(curbeat)))
        curbeat += incr
    return result


def getLength(path):
    tag = TinyTag.get(path)
    return tag.duration

def getMax(data):
    return int(data.split(',')[-1])

def getCount(data):
    return data.count(',')+1

def getBpm(path):
    if 'zone1_1' in path:
        return 115
    if 'zone1_2' in path:
        return 130
    if 'zone1_3' in path:
        return 140
    if 'zone2_1' in path:
        return 130
    if 'zone2_2' in path:
        return 140
    if 'zone2_3' in path:
        return 150
    if 'zone3_1' in path:
        return 135
    if 'zone3_2' in path:
        return 145
    if 'zone3_3' in path:
        return 155
    if 'zone4_1' in path:
        return 130
    if 'zone4_2' in path:
        return 145
    if 'zone4_3' in path:
        return 160

    #conga
    if 'boss_1' in path:
        return 120
    if 'boss_2' in path:
        return 175
    if 'boss_3' in path:
        return 123
    if 'boss_4' in path:
        return 126
    #dead ringer
    if 'boss_5' in path:
        return 140
    #cadence necrodancer stage 2
    if 'boss_6' in path and 'a.ogg' in path:
        return 160
    #cadence necrodance stage 1
    if 'boss_6' in path:
        return 140
    if 'boss_7' in path:
        return 'boss7'
    #godlen lute
    if 'boss_8' in path:
        return 120



    return None

def getOffset(data, bpm):
    incr = 1/(bpm/60/1000)
    return int(data.split(',')[1])-incr

def writeToFile(path, content):
    content_str = ','.join(content)
    with open(path, 'w') as f:
        f.write(content_str)

def convertToMs(data):
    if '.' not in data:
        return data
    content = data.split('\n')
    if '' in content:
        content.remove('')
    for i in range(len(content)): 
        content[i] = str(int(float(content[i])*1000))
    content_str = ','.join(content)

    return content_str

def dbl_boss7(data):
    result = ['0']
    data = data.split(',')
    for i in range(len(data)-1):
        result.append(str(round((int(data[i]) + int(data[i+1]))/2)))
        result.append(str(data[i+1]))
    return result

def compound_boss7(data):
    result = []
    data = data.split(',')
    print(data)

    for i in range(0, len(data)-1, 2):
        step = (int(data[i+2])-int(data[i]))/3
        result.append(data[i])
        result.append(str(round(int(data[i])+step)))
        result.append(str(round(int(data[i])+step*2)))
    print(result)
    return result



def fixConga(data, skip1, skip2, length):
    result = []
    for i in range(len(data)):
        if (i)%length == skip1 or (i)%length == skip2:
            continue
        result.append( data[i])
    return result



if len(sys.argv) < 2:
    sys.exit("GIVE FILE PLOX")

for i in range(1, len(sys.argv)):
    k = sys.argv[i]
    bpm = getBpm(k)
    if bpm is None:
        continue


    print(k)
    #beatFile = os.path.abspath('old/' + k)
    beatFile = os.path.join('/home/hatten/.data/Steam/steamapps/common/Crypt of the NecroDancer/data/music', k)
    with open(beatFile, 'r') as f:
        data = f.read()

    data = convertToMs(data)

    
    length = getMax(data)
    count = getCount(data)
    if 'boss_1' in k:
        count = int(count*8/7)
    if bpm == 'boss7':
        #res = dbl_boss7(data)
        res = compound_boss7(data)
    else:
        offset = getOffset(data, bpm)
        res = generateFile(bpm*3/2, math.ceil(count*3/2), offset)

    if 'boss_1' in k:
        #res = fixConga(res, 13, 15, 16)
        res = fixConga(res, 10, 11, 12)
    writeToFile(k, res)


