import shutil
import xml.etree.ElementTree as ET



def getProp(item, attrib):
    if attrib in item.attrib:
        return item.attrib[attrib]
    return None


def adjustChances(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for item in root[0]:
        slot = getProp(item, 'slot')

        if slot != "weapon":
            item.attrib['isGold'] = 'true'




    tree.write(xmlfile)


fromxml = '/home/hatten/.data/Steam/steamapps/common/Crypt of the NecroDancer/data/necrodancer.xml'
toxml = '/home/hatten/.data/Steam/steamapps/common/Crypt of the NecroDancer/mods/remake/necrodancer.xml'


shutil.copyfile(fromxml, toxml)
adjustChances(toxml)
