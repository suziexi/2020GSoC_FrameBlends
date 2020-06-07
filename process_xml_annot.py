import xml.dom.minidom as DM
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import os

# import full text annotation raw data
# change path to your local directory
path = ('/Users/mac/Desktop/fndata-1.7/fulltext/')

# open the sentiment frames(or any list of files) and build a list of frame names
with open('/Users/mac/Desktop/sen_output') as f:
    lines = f.readlines()
    final_list = []

    for i in lines:
        final_list.append(i.strip())

    # generate a list of frame name from a folder of frame data
    final_list = [x[:-4] for x in final_list]


def parseXML(path):
    frame_list = [None] * 1
    output_list = [None] * 1
    part_text = [None] * 1
    sentence_location = [None]*1

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

            # Print out the actual text of each unit of sentence, "sentence[0].text"
            print('text:')
            print(sentence[0].text)

            # sentence tag and attribute
            # tag and attribute indicate
            # e.g. "<sentence corpID="195" docID="23692" sentNo="1" paragNo="1" aPos="0" ID="4101168">"
            print('tag:')
            print(sentence.tag)
            # e.g. {http://framenet.icsi.berkeley.edu}sentence

            print('attribute:')
            print(sentence.attrib)
            # e.g. {'corpid': '195', 'docid': '25397', 'sentno': '1', 'paragno': '323', 'apos': '0', 'id': '4154645'}

            for annot in sentence.iter():  # text, annotationSet

                print('tag_annot:')
                print(annot.tag)
                # e.g. {http://framenet.icsi.berkeley.edu}label, or {http://framenet.icsi.berkeley.edu}layer
                print('attribute_annot:')
                print(annot.attrib)
                # e.g. {'end': '12', 'start': '0', 'name': 'np'}


                # iterate the annotation set from each sentence
                # annot.attrib, e.g. <annotationSet cDate="10/26/2009 04:28:59 PDT Mon" luID="5511" luName="people.n" frameID="304" frameName="People" status="MANUAL" ID="6558815">
                for x, y in annot.attrib.items():
                    if x == 'framename':
                        print('FrameName:')
                        print(y)
                        # compare the extracted framename with the list of frames generated from frame files
                        for l in final_list:
                            if l.lower() == y.lower():
                                # if found match, append the frame name to frame_list
                                frame_list.append(l.lower())
                                # end = [item['end'] for index1 in annot.attrib.values() for index1 in index1]

                                output_list.append(filename)
                                output_list.append(l.lower())
                                output_list.append(sentence[0].text)

                                # Found the annotationSet line according to matched framename
                                part_text.append(annot.attrib)

                                # Found the sentence ID and append to a list, need manually check the sentence text
                                for key, value in annot.attrib.items():
                                    if key == 'id':
                                        print(key, value)
                                        sentence_location.append(value)
                                        output_list.append(value)

                                output_list.append('\n')


    print('Matched Frame List:')
    frame_list = list(dict.fromkeys(frame_list)) # remove duplicates
    print(frame_list)

    print('Matched Actual text:')
    print( output_list)

    print('Matched Sentence location(ID from annotationSet)')
    # sentence_location = [x[:-4] for x in sentence_location]
    print(sentence_location)


    # # output the matched frame list
    # with open('/Users/mac/Desktop/match_frame', 'w') as file_handler:
    #     for item in frame_list:
    #         file_handler.write("{}\n".format(item))
    #
    # with open('/Users/mac/Desktop/sentence_location', 'w') as file_handler:
    #     for item1 in sentence_location:
    #         file_handler.write("{}\n".format(item1))

    with open('/Users/mac/Desktop/output_list', 'w') as file_handler:
        for item in  output_list:
            file_handler.write("{}\n".format(item))




def main():
    parseXML(path)


if __name__ == "__main__":
    main()

