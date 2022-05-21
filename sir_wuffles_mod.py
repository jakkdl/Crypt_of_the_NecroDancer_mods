
def dostuff(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for item in root[0]:
        print(item)
        input()

if __name__ == '__main__':
    fromxml = '/home/hatten/Necrodancer/data/necrodancer.xml'
    toxml   = '/home/hatten/Necrodancer/mods/wuffles/necrodancer.xml'

    shutil.copyfile(fromxml, toxml)


    dostuff(toxml)
