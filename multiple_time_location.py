import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import os

path = ('/Users/mac/Desktop/location_label')

# open the sentiment frames(or any list of files) and build a list of frame names
with open('/Users/mac/Desktop/time_list') as f:
    lines = f.readlines()
    location_list = []

    for i in lines:
        location_list.append(i.strip())

    # generate a list of frame name from a folder of frame data
    location_list = [x[:-4] for x in location_list]


def parseXML(path):

    frame_list = [None] * 1
    target_list = []
    final = []

    item = ET.Element("FBL")
    ET.SubElement(item, 'Source').text = 'Multiple_times'

    # read in every file from the full text annotation folder(or other annotation data folder)
    # read in as a tree structure using xml.etree.ElementTree
    for filename in os.listdir(path):
        if not filename.endswith('.xml'):
            continue
        fullname = os.path.join(path, filename)
        tree = ET.parse(fullname)
        tree = tree.getroot()
        t = tostring(tree)
        t = t.lower()
        tree = ET.fromstring(t)


        # read each sentence of each annotation file
        for sentence in tree:
            sent_list = []
            # tag and attribute include "<sentence corpID="195" docID="23692" sentNo="1" paragNo="1" aPos="0" ID="4101168">" this line
            print('text:')
            print(sentence[0].text)

            print('tag:')
            print(sentence.tag)
            print('attribute:')
            print(sentence.attrib)

            for annot in sentence.iter():  # text, annotationSet

                print('tag_annot:')
                print(annot.tag)
                print(annot.attrib)

                for x, y in annot.attrib.items():
                    if x == 'framename':
                        print('FrameName:')
                        print(y)
                        for l in location_list:
                            if l.lower() == y.lower():
                                print('attribute_annot:')
                                print(annot.attrib)
                                frame_list.append(l.lower())

                                if not sent_list: # list is empty
                                    sent_list.append(l.lower())

                                else: # list is not empty, double found
                                    print(sentence.attrib)
                                    target_list.append(sentence[0].text)
                                    annot.append(item)
                                    final.append(filename)


        filename = open('/Users/mac/Desktop/time_label/'+filename, "w")
        filename.write(ET.tostring(tree, encoding="unicode"))

    frame_list = list(dict.fromkeys(frame_list))
    print(frame_list)


    with open('/Users/mac/Desktop/target_list_test_3', 'w') as file_handler:
        for item in target_list:
            file_handler.write("{}\n".format(item))

def main():
    parseXML(path)


if __name__ == "__main__":
    main()
