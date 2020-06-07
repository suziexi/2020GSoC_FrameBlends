import xml.dom.minidom as DM
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import os
from os import walk

path = ('/Users/mac/Desktop/sentience_frames')

# Result: number of files: 51
# number of nodes: around 50 for each frame
def parseFM(path):
    i = 0

    for filename in os.listdir(path):
        print('number of frame files:')
        i = i+1
        print(i)
        if not filename.endswith('.xml'):
            continue
        fullname = os.path.join(path, filename)
        tree = ET.parse(fullname)
        tree = tree.getroot()
        t = tostring(tree)
        t = t.lower()
        tree = ET.fromstring(t)
        print(tree)
        print(tree.attrib)
        print(tree.tag)

    f = []

    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)




        ct1 = 0
        for node in tree:
            print("tag:") # tag includes: fe, frame relation, lexunit
            print(node.tag)

            print("attribute:") # attribute is the line after tag
            for x, y in node.attrib.items():
                if x == 'id':
                    print('id:')
                    print(y)
            print('number of nodes for each file: ')
            ct1 = ct1+1
            print(ct1)


    print(f)

    with open('/Users/mac/Desktop/sen_output', 'w') as file_handler:
        for item in f:
            file_handler.write("{}\n".format(item))



def main():
    parseFM(path)


if __name__ == "__main__":
    main()
