from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from gensim.models import word2vec
import gensim
from gensim.test.utils import common_texts, get_tmpfile
from pprint import pprint
from nltk.corpus import framenet as fn
import nltk
import xml.dom.minidom as DM
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import os

path = ('/Users/mac/Desktop/fmdt/fndata-1.7/fulltext_copy')

with open('/Users/mac/Desktop/all_words') as f:
    content = f.read().splitlines()

def nvConflict(path,content):

    all_words = []
    model_2 = Word2Vec([content], size=100, window=5, min_count=1, workers=4)

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
        full_sentence = []

        new_list = []

        final_result_list = []


        # read each sentence of each annotation file
        for sentence in tree:
            each_sentence = []
            each_nvpair = []
            each_sentence.append(filename)
            each_sentence.append("This following is a new sentence: ")
            each_sentence.append(sentence[0].text)
            result_list = []

            for annot in sentence.iter():  # text, annotationSet

                # annot.attrib, e.g. <annotationSet cDate="10/26/2009 04:28:59 PDT Mon" luID="5511" luName="people.n" frameID="304" frameName="People" status="MANUAL" ID="6558815">
                for x, y in annot.attrib.items():
                    # when the phrase type is noun; it's different kind of noun;
                    # please see http://www.surdeanu.info/mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html for details
                    if y == 'nn' or y == 'nns' or y == 'nnp' or y == 'nnps':
                        print('--------------')
                        print('This sentence has the following noun:')
                        start = annot.attrib.get('start')
                        start = int(start)
                        end = annot.attrib.get('end')
                        end = int(end)
                        end = end + 1
                        clause_1 = sentence[0].text[start:end]
                        print(clause_1)
                        each_sentence.append(clause_1)
                        each_sentence.append('This is the type of noun:')
                        each_sentence.append(y)
                        print(y)
                        # slice_list.append(fn.annotations(clause_1))
                        fm1 = fn.frames_by_lemma(clause_1)
                        print(fm1)
                        each_sentence.append('This lemma evoked the following frame:')
                        each_sentence.append(fm1)
                        new_list.append(clause_1)
                        each_nvpair.append(clause_1)
                        all_words.append(clause_1)
                        result_list.append(clause_1)

                    # when the phrase type is verb; it's different kind of verb
                    elif y == 'vvd' or y == 'vb' or y == 'vbd' or y == 'vbg' or y == 'vbn' or y == 'vbp' or y == 'vbz':
                        print('--------------')
                        print(sentence[0].text)
                        print('This sentence has the following verb:')
                        start = annot.attrib.get('start')
                        start = int(start)
                        print(start)
                        end = annot.attrib.get('end')
                        end = int(end)
                        end = end + 1
                        print(sentence[0].text[start:end])
                        clause_2 = sentence[0].text[start:end]
                        each_sentence.append(clause_2)
                        each_sentence.append('This is the type of verb:')
                        each_sentence.append(y)
                        print(y)
                        # slice_list.append(sentence[0].text[start:end])
                        each_sentence.append('This lemma evoked the following frame:')
                        fm2 = fn.frames_by_lemma(clause_2)
                        print(fm2)
                        each_sentence.append(fm2)
                        new_list.append(clause_2)
                        each_nvpair.append(clause_2)
                        all_words.append(clause_2)
                        result_list.append(clause_2)


            full_sentence.append(each_sentence)
            full_sentence.append("\n")


            try:
                sim = []
                avg = 0
                for i in range(len(result_list)):
                    for j in range(i + 1, len(result_list)):
                        print(result_list[i])
                        print(result_list[j])
                        print(model_2.similarity(result_list[i], result_list[j]))
                        sim.append(result_list[i])
                        sim.append(result_list[j])
                        sim.append(model_2.similarity(result_list[i], result_list[j]))
                        avg += model_2.similarity(result_list[i], result_list[j])

                avg = avg/(i*j)
                print(avg)


                result_list.append(sim)
                result_list.append(sentence[0].text)
                result_list.append(avg)


                final_result_list.append(result_list)

                final_result_list.append("\n")

            except:
                pass


    with open('/Users/mac/Desktop/final_testing_3', 'w') as file_handler:
        try:
            for item in final_result_list:
                file_handler.write("{}\n".format(item))
        except:
            pass



def main():
    nvConflict(path, content)



if __name__ == "__main__":
    main()
