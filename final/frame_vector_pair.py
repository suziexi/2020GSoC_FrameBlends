import os, glob
import gensim
from nltk.corpus import words
from nltk.corpus import wordnet
import numpy as np
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from scipy import spatial

manywords = list(words.words()) + list(wordnet.words())

model_1 = gensim.models.Word2Vec([manywords], size=30, window=5, min_count=1, workers=4)

frame_path = ('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/framenet/data/frame_data_with_vector')

# master = ('/Users/mac/Desktop/RES')
#
# m_list = []
# for i in open(master):
#     m_list.append(i)
# v1 = m_list[0]
# v2 = m_list[-1]


# Choose input data file
path = ('/mnt/rds/redhen/gallina/tv/2019/2019-03/2019-03-07')


# Choose protype vector pair
# Maybe change to pprotypy frame (names)
i1 = '-3.8204238210580244e-05 -0.00012068518351173094 -0.0006129946442732555 -0.0008558550962334266 0.0002949998200684994 -0.0006221613275556592 -0.00032903482445232967 0.00030931733103248656 0.0006840797968184883 0.0003942507246392779 0.00015643958691466002 -0.0013355727920887667 0.00014512935662683697 0.0017800145971185494 -0.0005077605918424004 -9.460474949004752e-05 -0.0005682072423951467 -9.683988537290134e-06 0.001366813203666035 0.0002447762760441817 -0.0010271692761827061 0.001481821783110198 -0.0004206796654346233 0.0006407014712164839 -0.0007836522649670639 0.00157225152798495 0.00018982067799048048 -0.00018317711822289442 0.00029548206071743674 -0.0001756639795920429'
i2 = '-0.010495552327483892 0.0005354168824851513 0.0038443304365500808 -0.004005289287306368 -0.013078329619020224 0.010259466944262385 0.004672517068684101 0.0012825443409383297 0.0030857077799737453 -0.0026780678890645504 0.004381922160973772 0.004154692345764488 0.0071547862607985735 -0.007611311273649335 0.0021558406751864823 -0.0033992459066212177 0.0005512693896889687 0.014350167475640774 -0.0035095831844955683 0.006088046240620315 -0.002887505921535194 -0.004078927857335657 0.011955561581999063 0.0014049840392544866 0.0018145828507840633 0.0012108900118619204 0.008948366856202483 0.004117053002119064 -0.0033572628162801266 0.0015180050395429134'

v1 = i1.split(' ')
v2 = i2.split(' ')


def word(input):
    result = []
    output = []

    ct = 0

    # for filename in glob.glob(os.path.join(input, '*.seg')):

    rec_list = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.seg'))]
    for filename in rec_list:
        fbl = []
        real_name = filename.split('/')[-1]

        for line in open(filename, 'r'):
            dic = {}
            fbl.append(line)
            if 'CC1' in line:
                key = line
                combo = []
                l1 = ''

            elif ('FRM_01' in line) and (ct != 0) and (l1 != ''):
                try:
                    dic[key].append(line)
                except:
                    pass
                try:
                    dic[key] = line
                except:
                    pass

                frame = line.split('|')[5]
                for filename in os.listdir(frame_path):
                    if frame.lower() == filename[:-4].lower():
                        avg2 = 0.0
                        fullname = os.path.join(frame_path, filename)
                        tree = ET.parse(fullname)
                        tree = tree.getroot()
                        t = tostring(tree)
                        t = t.lower()
                        tree = ET.fromstring(t)
                        for lu in tree:
                            if lu.tag == 'frameembedding':
                                print('FRAME2')

                                a2 = v2
                                try:
                                    a_floats2 = [float(item) for item in a2]
                                except:
                                    pass
                                print(a_floats2)


                                b2 = lu[0].text
                                try:
                                    b_floats2 = [float(item) for item in b2.split()]
                                except:
                                    pass
                                print(b_floats)

                                cosine_similarity2 = 1 - spatial.distance.cosine(a_floats2, b_floats2)

                                avg2 = avg2 + cosine_similarity2
                                if avg2 >= 0.5:
                                    output.append(key)
                                    output.append('avg1')
                                    output.append(avg1)
                                    output.append(l1)
                                    output.append(a_floats)
                                    output.append(b_floats)

                                    output.append('avg2')
                                    output.append(avg2)
                                    output.append(line)
                                    output.append(a_floats2)
                                    output.append(b_floats2)

                                    output.append('\n')

                                    # add fbl label
                                    FBL_label = []
                                    FBL_label.append(line.split('|')[0])
                                    FBL_label.append('|')
                                    FBL_label.append(line.split('|')[1])
                                    FBL_label.append('|')
                                    FBL_label.append('FBL_01')
                                    FBL_label.append('|')
                                    FBL_label.append('frame_embedding')
                                    FBL_label.append('|')
                                    FBL_label.append(str(avg1))
                                    FBL_label.append('|')
                                    FBL_label.append(str(avg2))
                                    fbl_str = ''.join(FBL_label)
                                    fbl.append(fbl_str)


            elif ('FRM_01' in line):
                try:
                    dic[key].append(line)
                except:
                    pass
                try:
                    dic[key] = line
                except:
                    pass

                frame = line.split('|')[5]
                for filename in os.listdir(frame_path):
                    if frame.lower() == filename[:-4].lower():
                        avg1 = 0.0
                        fullname = os.path.join(frame_path, filename)
                        tree = ET.parse(fullname)
                        tree = tree.getroot()
                        t = tostring(tree)
                        t = t.lower()
                        tree = ET.fromstring(t)
                        for lu in tree:
                            if lu.tag == 'frameembedding':
                                print('FRAME1')
                                a = v1
                                try:
                                    a_floats = [float(item) for item in a]
                                except:
                                    pass
                                print(a_floats)

                                b = lu[0].text
                                try:
                                    b_floats = [float(item) for item in b.split()]
                                except:
                                    pass

                                print(b_floats)
                                cosine_similarity = 1 - spatial.distance.cosine(a_floats, b_floats)

                                avg1 = avg1 + cosine_similarity

                                if avg1 >= 0.5:
                                    combo.append(lu[0].text)
                                    result.append(key)
                                    result.append(combo)
                                    result.append(len(combo))

                                    try:
                                        ct = len(combo)
                                        l1 = line

                                    except:
                                        pass


        # Output
        f1 = open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/frame_vector_pair/frame_vector_pair_output/trial_1' + real_name[ :-3] + 'fbl', "w")
        for item in fbl:
            f1.write("%s" % item)

        # Eval
        eval = output
        f2 = open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/frame_vector_pair/frame_vector_pair_eval/trial_1/' + real_name[:-3] + 'txt', "w")
        for item in eval:
            f2.write("%s" % item)


    # with open('/Users/mac/Desktop/trans_test/test_f19', 'w') as file_handler:
    #     for item in result:
    #         file_handler.write("{}\n".format(item))

    # with open('/mnt/rds/redhen/gallina/home/wxx170/frameblends/frame_vector_pair/hpc_result', 'w') as file_handler:
    #    for item in output:
    #        file_handler.write("{}\n".format(item))


def main():
    word(input)


if __name__ == "__main__":
    main()

