from pprint import pprint
from nltk.corpus import framenet as fn
import nltk
import xml.dom.minidom as DM
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import tostring
import os
import zipfile2
import lxml.etree as etree

path = ('/Users/mac/Desktop/fndata-1.7/fulltext')
def metapFilter(path):
    metap_list = [None] * 1
    item = ET.Element("FBL")
    ET.SubElement(item, 'Source').text = 'Metaphor_label'


    for filename in os.listdir(path):
        if not filename.endswith('.xml'):
            continue
        fullname = os.path.join(path, filename)
        tree_0 = ET.parse(fullname)
        tree_1 = tree_0.getroot()
        t = tostring(tree_1)
        t = t.lower()
        tree_2 = ET.fromstring(t)
        for sentence in tree_2:
            for annot in sentence.iter():  # text, annotationSet
                for x, y in annot.attrib.items():

                    if y == 'metaphor':
                        print('Metaphor filter:')
                        print(sentence[0].text)
                        metap_list.append(sentence[0].text)
                        metap_list.append('--------------')
                        annot.append(item)
                        print(filename)

        filename = open('/Users/mac/Desktop/metaphor_label/'+filename, "w")
        filename.write(ET.tostring(tree_2, encoding="unicode"))



def main():
    metapFilter(path)



if __name__ == "__main__":
    main()
