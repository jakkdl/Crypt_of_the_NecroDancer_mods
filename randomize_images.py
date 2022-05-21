from PIL import Image
import os
import pprint
import random
import shutil
from tinytag import TinyTag
import xml.etree.ElementTree as ET
import copy



def get_files(directory, nameFilter=None):
    file_paths = []
    images = {}

    for root, directories, files in os.walk(directory):
        for filename in files:
            if nameFilter:
                keep = False
                for i in nameFilter:
                    if i in filename:
                        keep = True
                        break
                if not keep:
                    continue
            filepath = os.path.join(root, filename)
            #file_paths.append(filepath)
            im = Image.open(filepath)
            if im.size not in images:
                images[im.size] = [filename]
            else:
                images[im.size].append(filename)
            
    return images

def sound_get_files(directory):
    images = {}

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            #file_paths.append(filepath)
            #im = Image.open(filepath)
            tag = TinyTag.get(filepath)
            index = round(tag.duration, 1)
            if index not in images:
                images[index] = [filename]
            else:
                images[index].append(filename)
            
    return images


def shuffle(response, fromdir, todir):
    for size in response:
        #print(size, len(response[size]))
        copy = response[size].copy()
        copy = kappa_shuffle(copy)
        for i in range(len(copy)):
            #print(response[size][i], copy[i])
            shutil.copyfile(fromdir + response[size][i], todir + copy[i])
        
def shufflesounds(fromdir, todir):
    i = 'sounds'
    response = sound_get_files(fromdir + i + '/')
    shuffle(response, fromdir + i + '/', todir + i + '/')

def shuffleimages(fromdir, todir):
    targets = ['gui', 'items', 'level', 'particles', 'spells', 'swipes', 'traps']
    for i in targets:
        response = get_files(fromdir + i + '/')
        shuffle(response, fromdir + i + '/', todir + i + '/')
       
def kappa_shuffle(list_of_stuff):
    if len(list_of_stuff) == 1: 
        return list_of_stuff[:] 
    while True: 
        shuffled = random.sample(list_of_stuff, len(list_of_stuff)) 
        for a, b in zip(shuffled, list_of_stuff): 
            if a == b: 
                break 
        else: 
            return shuffled 

def getProp(item, attrib):
    if attrib in item.attrib:
        return item.attrib[attrib]
    return None

def xmlItemShuffle(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    list_of_hints = []
    list_of_flyaways = []

    for item in root[0]:

        list_of_hints.append(     getProp(item, 'hint'))
        list_of_flyaways.append( getProp(item, 'flyaway'))
        #list_of_images.append(    item.text)

    
    list_of_hints = kappa_shuffle(list_of_hints)
    list_of_flyaways = kappa_shuffle(list_of_flyaways)

    for item, hint, flyaway in zip(root[0], list_of_hints,
            list_of_flyaways):

        if hint == None:
            if 'hint' in item.attrib:
                item.attrib.pop('hint')
        else:
            item.attrib['hint'] = hint

        if flyaway == None:
            if 'flyaway' in item.attrib:
                item.attrib.pop('flyaway')
        else:
            item.attrib['flyaway'] = flyaway


    tree.write(xmlfile)



def xmlEnemyShuffle(xmlfile):
    cloneImage = ""
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    dict_of_enemies = {}

    #shuffle enemies
    enemies = root[1]
    
    print("create dict")
    for enemy in enemies:
        numFrames = enemy[0].attrib['numFrames']
        if numFrames in dict_of_enemies:
            dict_of_enemies[numFrames].append(enemy)
        else:
            dict_of_enemies[numFrames] = [enemy]
    
    print("empty enemies element")
    root.remove(root[1])
    ET.SubElement(root, 'enemies')

    print("copy dictionary")
    dict_copy = copy.deepcopy(dict_of_enemies)
    
    print("shuffle dictionary copy")
    for i in dict_copy:
        dict_copy[i] = kappa_shuffle(dict_copy[i])

    print("transfer values from shuffled dict")
    for frameCount in dict_of_enemies:
        for i in range(len(dict_of_enemies[frameCount])):
            enemy1 = dict_of_enemies[frameCount][i]
            enemy2 = dict_copy[frameCount][i]
            
            j = 0
            if enemy1.tag == 'clone':
                for i in enemy2:
                    if i.tag == 'spritesheet':
                        cloneImage = i.text

            while j < len(enemy1):
                if enemy1[j].tag in ['spritesheet', 'frame',
                        'shadow', 'particle']:
                    enemy1.remove(enemy1[j])
                else:
                    j += 1
            for element in enemy2:
                if element.tag in ['spritesheet', 'frame',
                        'shadow', 'particle']:

                    enemy1.append(element)
                


                
    print("Add dict to xml")
    for frame_list in dict_of_enemies.values():
        for enemy in frame_list:
            root[1].append(enemy)
    
    print("write tree")
    tree.write(xmlfile)
    return cloneImage

def fixClone(fromdir, todir, cloneImage):
    newImage = fromdir + cloneImage

    targets = ['aria', 'bard', 'bolt', 'coda', 'dorian', 'dove', 'eli' 'melody', 'monk']
    for i in targets:
        copyTo = todir + 'entities/clone_' + i + '.png'
        shutil.copyfile(newImage, copyTo)

fromdir = '/home/hatten/.data/Steam/SteamApps/common/Crypt of the NecroDancer/data/'
todir = '/home/hatten/.data/Steam/SteamApps/common/Crypt of the NecroDancer/mods/random/'

def swapCharacters(fromdir, todir):
    response = get_files(fromdir + 'entities/', ['heads', 'body'])
    print(response)
    shuffle(response, fromdir + 'entities/', todir + 'entities/')
    return


    heads = []
    bodies = []
    for i in range(1, 10):
        heads.append('entities/char' + str(i) + '_heads.png')
        bodies.append('entities/char' + str(i) + '_armor_body.png')
    shuffled_heads = kappa_shuffle(heads)
    shuffled_bodies = kappa_shuffle(bodies)
    for head, body, shuf_head, shuf_body in zip(heads, bodies, shuffled_heads, shuffled_bodies):
        shutil.copyfile(fromdir + head, todir + shuf_head)
        shutil.copyfile(fromdir + body, todir + shuf_body)

cloneImage = xmlEnemyShuffle(todir + 'necrodancer.xml')
xmlItemShuffle(todir + 'necrodancer.xml')
shufflesounds(fromdir, todir)
shuffleimages(fromdir, todir)
fixClone(fromdir, todir, cloneImage)
swapCharacters(fromdir, todir)
