import os
import pprint
import xml.etree.ElementTree as ET


def main(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    items = root[0]
    itemlist = []

    for item in root[0]:
        if 'flyaway' in item.attrib and 'coinCost' in item.attrib:
            itemlist.append((item.attrib['flyaway'].title(), int(item.attrib['coinCost'])))
    
    itemlist.sort(key=lambda x:x[1])

    for item in itemlist:
        print(item[0].ljust(30), item[1])



name = '/home/hatten/.data/Steam/steamapps/common/Crypt of the NecroDancer/data/necrodancer.xml'
main(name)
