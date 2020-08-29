import gensim
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import os
from nltk.corpus import words
from nltk.corpus import wordnet

# Set customized path to frame data

frame_dir_path = ('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/framenet/data/raw_frame/frame')
# frame_dir_path = ('/Users/mac/Desktop/fmdt/fndata-1.7/frame')


manywords = list(words.words()) + list(wordnet.words())


# If use self-defined traning words, use code below:

# with open('/Users/mac/Desktop/frame_embed/full_lu_list') as f:
#     content = f.read().splitlines()

def train_frame(frame_dir_path):
    model_1 = gensim.models.Word2Vec([manywords], size=30, window=5, min_count=1, workers=4)

    for filename in os.listdir(frame_dir_path):
        if not filename.endswith('.xml'):
            continue
        fullname = os.path.join(frame_dir_path, filename)
        tree = ET.parse(fullname)
        tree = tree.getroot()
        t = tostring(tree)
        t = t.lower()
        tree = ET.fromstring(t)
        each_frame = []

        vec_list = []

        for lu in tree:
            print('tag:')
            print(lu.tag)
            print('attribute:')
            print(lu.attrib)

            if lu.tag == '{http://framenet.icsi.berkeley.edu}lexunit':
                # lexunit
                for x, y in list(lu.attrib.items()):
                    if x == 'name':
                        try:
                            # vec_number = vec_number+1
                            y = y[:-2]
                            print(filename)
                            print(y)
                            each_frame.append(y)
                            vector = model_1[y]
                            print(vector)
                            vec_list.append(vector)
                            lu.attrib.update({'vector': vector})
                            print(lu.attrib)
                        except:
                            pass

        final_vect = [0] * 30

        ct = 0
        for i in range(len(vec_list)):
            ct = ct + 1
            for u in range(len(vec_list[i])):
                try:
                    final_vect[u] = final_vect[u] + vec_list[i][u]
                except:
                    pass

        new_result = []
        for i in final_vect:

            try:
                i = i / ct
                new_result.append(i)
            except:
                pass

        print(final_vect)
        print(new_result)

        item = ET.Element("frameEmbedding")
        item_vect = " ".join(str(x) for x in new_result)
        ET.SubElement(item, 'frameVector').text = item_vect
        tree.append(item)

        # Set output path
        file = open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/framenet/data/new_trial_1' + filename, "w")
        # file = open('/Users/mac/Desktop/Frame_Embedding_data/'+filename, "w")
        file.write(ET.tostring(tree, encoding="unicode"))


def main():
    train_frame(frame_dir_path)


if __name__ == "__main__":
    main()


