import os, glob
import gensim 


path = ('/mnt/rds/redhen/gallina/tv')



with open('/mnt/rds/redhen/gallina/Singularity/frameblends/word2vec/hpc_content_1') as f:
    content = f.read().splitlines()

def list_full(d): 
    return [os.path.join(d,'*.seg') for f in os.listdir(d)] 


def word(path, content):

    model_2 = gensim.models.Word2Vec([content], size=100, window=5, min_count=1, workers=4)


    final_result_list = [] 
    
   # for filename in glob.glob('path/**/*.seg',recursive = True): 
   
   # for filename in glob.iglob(path + '**/**.seg', recursive=True):
    for filename in list_full(path): 

        print(filename)
        full_list = []
        verb_list = []
        noun_list = []

       # final_result_list = []
 
        final_result_list.append(filename) 

        print(filename)
        dic = {}
        key = 'inital'

        for line in open(filename, 'r'):
            sent_list = []
            result_list = []
            print(line)
            if 'CC1' in line:
                key = line


            elif 'POS_02' in line:
                dic[key] = line
                print(key)
                print(line)

                for p in line.split('|'):

                    print(p)
                    pair = p.split('/')

                    print(pair[0])
                    print(pair[-1])

                    if pair[-1] == 'NNP' or pair[-1] == 'NNPS' or pair[-1] == 'NNS' or pair[-1] == 'NN':
                        noun_list.append(pair[0])
                        sent_list.append(pair[0])
                        result_list.append(pair[0])

                    elif pair[-1] == 'VVD' or pair[-1] == 'VD' or pair[-1] == 'vbd' or pair[-1] == 'VBG' or pair[-1] == 'VBN' or pair[-1] == 'VBP' or pair[-1] == 'VBZ':
                        verb_list.append(pair[0])
                        sent_list.append(pair[0])
                        result_list.append(pair[0])

            # full_list.append(sent_list)
            # full_list.append("\n")


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
                result_list.append(key)
                result_list.append(avg)


                final_result_list.append(result_list)

                final_result_list.append("\n")

            except:
                pass




        print(verb_list)
        print(noun_list)
        print(full_list)

        with open('/mnt/rds/redhen/gallina/Singularity/frameblends/word2vec/similarity_hpc_2', 'w') as file_handler:
            for item in final_result_list:
                file_handler.write("{}\n".format(item))


def main():
    word(path,content)

if __name__ == "__main__":
    main()

