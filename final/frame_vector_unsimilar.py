import os, glob
import gensim
from nltk.corpus import words
from nltk.corpus import wordnet
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import numpy as np
from scipy import spatial
import nltk

nltk.download('wordnet')
nltk.download('words')

manywords = list(words.words()) + list(wordnet.words())

path = ('/mnt/rds/redhen/gallina/tv/2019/2019-03/2019-03-07')

model_2 = gensim.models.Word2Vec([manywords], size=30, window=5, min_count=1, workers=4)

frame_path = ('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/framenet/data/frame_data_with_vector')


def getFrameVec(frame_path, each_frame):

    # rec_list = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.seg'))]
    # for filename in rec_list:
    for filename in glob.glob(os.path.join(path, '*.seg')):
        print('filename')
        print(filename)
        print(filename[:-4])
        print('each_frame')
        print(each_frame)

        if each_frame.lower() == filename[:-4].lower():
            fullname = os.path.join(frame_path, filename)
            tree = ET.parse(fullname)
            tree = tree.getroot()
            t = tostring(tree)
            t = t.lower()
            tree = ET.fromstring(t)
            for lu in tree:
                print('tag:')
                print(lu.tag)
                print('attribute:')
                print(lu.attrib)

                if lu.tag == 'frameembedding':
                    # lexunit
                    print(lu[0].text)
                    return lu[0].text



def word(path):

    for filename in glob.glob(os.path.join(path, '*.seg')):
        output = []


        real_name = filename.split('/')[-1]

        #Changed all "test" to "eval"
        eval = []
        sim_list = []

        # -------------------------------------------------------- Part1: Calculate the smallest similar rate as a cute-off value ---------------------------------------------------------------------

        t = 'initial'
        #dic = {}

        for line in open(filename, 'r'):
            if 'CC1' in line and line != 'CC1|ENG\n':
                key = line
                each_sentence_frame = []
                t = 'changed'

            elif 'FRM_01' in line and 'Source_Program=FrameNet 1.5, Semafor 3.0-alpha4, FrameNet-06.py' not in line:
                frame = line.split('|')[5]
                frameVec = getFrameVec(frame_path, frame)
                # eval.append(frameVec)
                each_sentence_frame.append(frameVec)

            if t != 'initial':
                # eval.append(filename)
                frame_vector_pairs = [(p1, p2) for p1 in each_sentence_frame for p2 in each_sentence_frame]
                # eval.append([(p1, p2) for p1 in each_sentence_frame for p2 in each_sentence_frame if p1 != p2])

                avg = 0.0

                for i in range(len(frame_vector_pairs)):
                    a, b = frame_vector_pairs[i]

                    try:
                        a_floats = [float(item) for item in a.split()]
                        b_floats = [float(item) for item in b.split()]

                        # eval.append(a)
                        # eval.append(b)

                        cosine_similarity = 1 - spatial.distance.cosine(a_floats, b_floats)
                        print('cosine_similarity')
                        print(cosine_similarity)
                        # eval.append(cosine_similarity)
                        avg = avg + cosine_similarity
                    except:
                        pass

                try:
                    eval.append('cosine_similarity')
                    eval.append(cosine_similarity)
                    eval.append(avg)
                except:
                    pass
            else:
                continue

            try:
                avg = avg/len(frame_vector_pairs)

                eval.append(filename)
                eval.append('average')

                eval.append(avg)
                sim_list.append(avg)
            except:
                pass




        sorted_list = sorted(sim_list)

        # eval.append('add sorted list')
        # eval.append(sorted_list)


        re = []
        for s in sorted_list:
            if s == 0.0:
                continue
            re.append(s)

        small_list = re[:10]

        # eval.append(re[:10])

        # -------------------------------------------------------- Part2: Append Label if a case is smallest ---------------------------------------------------------------------

        dic_1 = {}

        for line in open(filename, 'r'):
            output.append(line)
            t1 = 'initial'

            if 'CC1' in line and line != 'CC1|ENG\n':
                key = line
                each_sentence_frame_1= []

                t1 = 'changed'

            elif 'FRM_01' in line and 'Source_Program=FrameNet 1.5, Semafor 3.0-alpha4, FrameNet-06.py' not in line:

                frame = line.split('|')[5]
                if dic_1.__contains__(key):
                    frameVec_1= getFrameVec(frame_path, frame)
                    dic_1[key] = dic_1[key].append(frameVec_1)
                    each_sentence_frame_1.append(frameVec_1)

                print(line)


            if t1 != 'initial' and dic_1.__contains__(key):
                frame_vector_pairs = [(p1, p2) for p1 in each_sentence_frame_1 for p2 in each_sentence_frame_1]


                avg = 0.0
                for j in frame_vector_pairs:
                    a, b = frame_vector_pairs[j]
                    avg = avg + np.sum(a * b) / (np.linalg.norm(a) * np.linalg.norm(b))

                avg = avg/len(frame_vector_pairs)

                if avg in small_list:
                    FBL_label = []
                    FBL_label.append(line.split('|')[0])
                    FBL_label.append('|')
                    FBL_label.append(line.split('|')[1])
                    FBL_label.append('|')
                    FBL_label.append('FBL_01')
                    FBL_label.append('|')
                    FBL_label.append('frame_embedding_unsimilar')
                    FBL_label.append('|')
                    FBL_label.append(str(a))
                    FBL_label.append(' ')
                    FBL_label.append(str(b))
                    fbl_str = ''.join(FBL_label)
                    output.append(fbl_str)
                    eval.append(key)
                    eval.append(fbl_str)
            else:
                pass


        f1 = open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/frame_vector_unsimilar/frame_vector_unsimilar_output/trial1/' + real_name[ :-3] + 'fbl', "w+")
        for item in output:
            f1.write("%s" % item)

        f2 = open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/frame_vector_unsimilar/frame_vector_unsimilar_eval/trial1/'+ real_name[:-3] + 'txt', "w+")
        for i in eval:
            f2.write("%s\n" % i)



def main():
    word(path)


if __name__ == "__main__":
    main()
