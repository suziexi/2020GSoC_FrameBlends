# 2020GSoC_FrameBlends
This GSoC project "AI Recognizers of Frame Blends, Especially in Conversations About the Future" is contributed by Wenyue Xi (Suzie) with Red Hen Lab. 

## First Code uploading: 
A brief instruction:

Step 1:

Run ‘read_senti_frames.py” to get a list of frame names with indicated features
In this case, it read in a folder of manually selected frames with relation to sentience
To run locally, please remember to change to “path” at the beginning to the local directory address*
After running ‘read_senti_frames.py”, it generates a file called “sen_output”, it’s a text file including indicated file names with line break
Step 2:

Run “process_xml_annot.py”
This file read in the “sen_output” file and a folder of “fulltext”
This code will detect the cases when the evoked frame names match with the frame names in “sen_output”
This code will generate a text file “output_list”, it includes four kinds of information:


## Second Code uploading: 
- The file detect_metaphor.py can be used to detect metaphor labels from full text annotation data; and also add the following annotation tag "<FBL><Source>Metaphor_label</Source></FBL>" to the original data file 
- The file multiple_time_location.py can be used to detect the cases when different clauses in a sentence envoke multiple location frames, or multiple time frames, as potential frame blends candidates; and also add the annotation tag like "<FBL><Source>Multiple_locations</Source></FBL>" to the original data file 
- Both detect_metaphor.py and multiple_time_location.py work fine after testing, and have successfully added the FBL tags to all full-text annotation data based on the two methods above 

- metap_sentence_list is an output file that include all the sentences that are tagged with "metaphor label" by FrameNet 
