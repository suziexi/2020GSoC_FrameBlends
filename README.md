# 2020GSoC_FrameBlends
This GSoC project "AI Recognizers of Frame Blends, Especially in Conversations About the Future" is contributed by Wenyue Xi (Suzie) with Red Hen Lab. 

## First Code Uploading: 
A brief instruction:

- Step 1:

Run ‘read_senti_frames.py” to get a list of frame names with indicated features
In this case, it read in a folder of manually selected frames with relation to sentience
To run locally, please remember to change to “path” at the beginning to the local directory address*
After running ‘read_senti_frames.py”, it generates a file called “sen_output”, it’s a text file including indicated file names with line break

- Step 2:

Run “process_xml_annot.py”
This file read in the “sen_output” file and a folder of “fulltext”
This code will detect the cases when the evoked frame names match with the frame names in “sen_output”
This code will generate a text file “output_list”, it includes four kinds of information:


## Second Code Uploading: 
- The file [detect_metaphor.py](detect_metaphor.py) can be used to detect metaphor labels from full text annotation data; and also add the following annotation tag "<FBL><Source>Metaphor_label</Source></FBL>" to the original data file 
- The file [metap_sentence_list](metap_sentence_list) is an output file that include all the sentences that are tagged with "metaphor label" by FrameNet 
- The file [multiple_time_location.py](multiple_time_location.py) can be used to detect the cases when different clauses in a sentence envoke multiple location frames, or multiple time frames, as potential frame blends candidates; and also add the annotation tag like "<FBL><Source>Multiple_locations</Source></FBL>" to the original data file 
- Both [detect_metaphor.py](detect_metaphor.py and [multiple_time_location.py](metap_sentence_list) work fine after testing, and have successfully added the FBL tags to all full-text annotation data based on the two methods above 
- The file [find_nv_conflict.py](find_nv_conflict.py) is used to generate verb and noun phrase type and evoked frames in each sentence; please see [nv_ANC__chapter1_911report.xml](nv_ANC__chapter1_911report.xml) for sample output 


## Third Code Uploading: 
- Uploaded [word2vector_test.py](word2vector_test.py). This code has also been uploded to Gallina, and the verb-noun list will be extracted from tv tree data in the further step. 
1. This algorithm use Gensim python package to generates semantic vectors of each element in the verb-noun list
2. Train the model with those input words 
3. For all the verbs and nouns in each sentence, computer similarity between each pair of extracted words in the sentence 
4. Compute the average similarity 
5. Theoretically, when the average similarity is smaller, there will be more likely to include semantic conflict inside this sentence, and have a larger possibility of frame blends 
- Uploaded [word2vec_similarity](word2vec_similarity). This text file is the output of [word2vector_test.py](word2vector_test.py). 


## Final Code Uploading 
This submission is a simple backup of FrameBlends Pipeline code on HPC. The full structure and experiment data are stored in the HPC pipeline. 

