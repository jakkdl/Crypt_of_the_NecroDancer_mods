#!/usr/bin/python
import os
import os.path
import sys
import math
import re

NECRODIR = '/home/hatten/Necrodancer/'
MUSICDIR = os.path.join(NECRODIR, 'data', 'music')
MODDIR = os.path.join(NECRODIR, 'mods')

def getBpm(path):
    if re.match('(cutscene|credits|intro|main_menu).*', path):
        return None
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
    if 'zone5_1' in path:
        return 130
    if 'zone5_2' in path:
        return 140
    if 'zone5_3' in path:
        return 155

    if 'lobby' in path:
        return 130
    if 'training' in path:
        return 120
    if 'tutorial' in path:
        return 100


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
    if 'boss_6' in path and 'a.' in path:
        return 160
    #cadence necrodance stage 1
    if 'boss_6' in path:
        return 140
    if 'boss_7' in path:
        return 'boss7'
    #godlen lute
    if 'boss_8' in path:
        return 120
    #fortissimole
    if 'boss_9' in path:
        return 150

    raise Exception('unknown path: {}'.format(path))


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


def getMax(data):
    return int(data.split(',')[-1])

def getCount(data):
    return data.count(',')+1

def getOffset(data, bpm):
    incr = 1/(bpm/60/1000)
    return int(data.split(',')[1])-incr

def writeToFile(path, content, join=','):
    content_str = join.join(content)
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


def generate_boss7(data, new, old=4):
    def func(x, a, b, c):
        return -(a*x)**2 + b*x + c
    #gcd = math.gcd(new, old)
    #if gcd > 1:
        #new //= gcd
        #old //= gcd
        #print(new, old)
    
    
    #everything's strings
    #data = [float(x) for x in data]
    data = data.split('\n')
    old_beat_count = len(data) #145
    last = float(data[-1]) #59.0832

    #-(a * x)**2 + b*x + c
    a = 0.02089021301949791 #TODO:calculate anew with precision
    b = 0.471579
    c = 0.142619


    calc_beat_count = math.ceil(old_beat_count*new/old) #TODO: +-1
    new_beat_count = min(calc_beat_count, 145)
    ratio = old/new
    newa = a*ratio
    newb = b*ratio
    newc = c*ratio
    
    return [str(func(x, newa, newb, newc))
            for x in range(new_beat_count)]


   #beat = float(data[0])
   #result = [str(beat)]
   #beats = 1
   #diff = 0
    #while beat < last:
        #beats += 1
        #beat += 60 / (124.786 + 0.317161 * (beats-4))# * old / new) 
        #diff += beat - float(data[beats])
        #result.append(str(beat))

#a               = -0.000436401     +/- 2.019e-06    (0.4626%)
#b               = 0.471579         +/- 0.0003004    (0.0637%)
#c               = 0.142619         +/- 0.009361     (6.564%)

   #for i in range(0, len(data)-old, old):
   #    step = (data[i+old]-data[i]) / new
   #    for j in range(new):
   #        tmp = data[i] + step*j
   #        result.append(str(round(tmp)))
   #print(data[-1], result[-1])

    return result


def fixConga(data, skip, length):
    result = []
    for i in range(len(data)):
        skip_this = False
        for j in skip:
            if i % length == j:
                skip_this = True
                break
        if skip_this:
            continue
        result.append(data[i])
    return result

soundtrack_names = {'': 'dannyb',
        '1': 'a-rival',
        '2': 'jules',
        '3': 'virt',
        '4': 'GFR',
        '4a': 'GFR',
        '4b': 'GFR',
        'ocr': 'oc remix'
        }

def getSoundtrackKey(filename):

    base = filename.split('.')[0]

    if re.match('(cutscene|credits|intro|main_menu).*', base):
        return None

    #necrodancer 1 phase 2
    if 'boss_6' in base and base[-1] == 'a':
        base = base[:-1]

    key = re.sub('(boss_.|zone._.|training|tutorial|lobby)_?', '', base)

    #hot/cold
    key = re.sub('[ch]$', '', key)

    return key

def process_file(from_file, to_file, track, new_beats_per_measure, congaskip,
                 beats_per_minute):
    old = 4
    ratio = new_beats_per_measure/old
    bpm = getBpm(track)

    with open(from_file, 'r') as f:
        raw_data = f.read()

    data = convertToMs(raw_data)
    length = getMax(data)
    count = getCount(data)

    if 'boss_1' in track: #KC
        count = int(count*8/7)

    if bpm == 'boss7': #ND2
        res = generate_boss7(raw_data, new=new_beats_per_measure, old=old)
        writeToFile(to_file, res, join='\n')
        return
    else:
        offset = getOffset(data, bpm)
        res = generateFile(bpm*ratio,
                math.ceil(count*ratio), offset)

    if 'boss_1' in track:
        res = fixConga(res, skip=congaskip, length=new_beats_per_measure*2)

    writeToFile(to_file, res)

def tempo_up_process_file(from_file, to_file, track, speedup):
    bpm = getBpm(track)
    if not isinstance(bpm, int):
        return
    bpm = bpm*speedup

    with open(from_file, 'r') as f:
        raw_data = f.read()

    data = convertToMs(raw_data)
    length = getMax(data)/speedup
    count = getCount(data)

    if 'boss_1' in track: #KC
        count = int(count*8/7)

    if bpm == 'boss7': #ND2
        res = generate_boss7(raw_data, new=new_beats_per_measure, old=old)
        writeToFile(to_file, res, join='\n')
        return
    else:
        offset = getOffset(data, bpm)/speedup
        res = generateFile(bpm,
                math.ceil(count), offset)

    if 'boss_1' in track:
        res = fixConga(res, skip=[7], length=8)

    writeToFile(to_file, res)

def get_all_tracks(extension = None):
    files = os.listdir(os.path.join(NECRODIR, 'data', 'music'))
    if extension:
        pattern = '.*' + extension + '$'
        files = [f for f in files if re.match(pattern, f)]
    return files


conga_skip_dict = {
        1: [],
        2: [],
        3: [5],
        4: [7],
        5: [9],
        6: [10, 11],
        7: [12, 13],
        8: [13, 15],
        9: [15, 17]
        }
def tempo_up(name, multiplier):
    tracks = get_all_tracks('txt')
    todir = os.path.join(MODDIR, name, 'music')
    if not os.path.exists(todir):
        os.makedirs(todir)
    
    for track in tracks:
        from_file = os.path.join(MUSICDIR, track)
        to_file = os.path.join(todir, track)
        bpm = getBpm(track)
        if bpm is None:
            continue
        tempo_up_process_file(from_file, to_file, track, speedup=multiplier)

def multi_tempo(name, mult_dict):
    tracks = get_all_tracks('txt')
    todir = os.path.join(MODDIR, name, 'music')
    if not os.path.exists(todir):
        os.makedirs(todir)
    
    for track in tracks:
        from_file = os.path.join(MUSICDIR, track)
        to_file = os.path.join(todir, track)
        key = getSoundtrackKey(track)
        if key is None:
            continue
        mult = mult_dict[key]
        conga_skip = conga_skip_dict[mult]
        print(track, mult, conga_skip)
        process_file(from_file, to_file, track, mult, conga_skip)


def shrine_of_rhythm(name):
    todir = os.path.join(MODDIR, name, 'music')
    if not os.path.exists(todir):
        os.makedirs(todir)

    tracks = get_all_tracks('txt')
    for track in tracks:
        from_file = os.path.join(MUSICDIR, track)
        to_file = os.path.join(todir, track)

        bpm = getBpm(track)
        if not bpm:
            continue

        with open(from_file, 'r') as f:
            raw_data = f.read()

        data = convertToMs(raw_data)
        data = data.split(',')
        if 'boss_1' in track:
            writeToFile(to_file, data)
            continue

        res = []
        for i in range(len(data)):
            if i%8 != 7:
                res.append(data[i])



        writeToFile(to_file, res)



if __name__ == '__main__':
    mult_dict = {
            ''   : 2,#'dannyb',
            '1'  : 3,#'a-rival',
            '2'  : 5,#'jules',
            '3'  : 6,#'virt',
            '4'  : 7,#'GFR',
            '4a' : 7,#'GFR',
            '4b' : 7,#'GFR',
            'ocr': 8,#'oc remix'
            }
    #main_quarter_triplet()
    #main(get_all_tracks('txt'), 5, [])
    #main_quintet()
    #multi_tempo('multi_tempo', mult_dict)
    #shrine_of_rhythm('shrine_of_rhythm')
    tempo_up('tempo_up', 1.125)


###I'm a wuss so I'm not deleting these [just yet]
def dbl_boss7(data):
    result = ['0']
    data = data.split(',')
    for i in range(len(data)-1):
        result.append(str(round((int(data[i]) + int(data[i+1]))/2)))
        result.append(str(data[i+1]))
    return result

def quarter_triplet_boss7(data):
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
'''
Grimy - Today at 10:07 PM
So I just do:
f(x) = a*x*x + b*x + c
fit f(x) 'boss_7.txt' via a,b,c
(edited)
And it spits out:
a               = -0.000436401     +/- 2.019e-06    (0.4626%)
b               = 0.471579         +/- 0.0003004    (0.0637%)
c               = 0.142619         +/- 0.009361     (6.564%)
a is negative so that’s good
The song is speeding up, so the deltas should be getting smaller
So then I do
plot 'boss_7.txt', -0.000436401*x*x + 0.471579*x + 0.142619
And it draws
'''
