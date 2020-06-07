A brief instruction: 

Step 1: 
- Run ‘read_senti_frames.py” to get a list of frame names with indicated features 
- In this case, it read in a folder of manually selected frames with relation to sentience
- To run locally, please remember to change to “path” at the beginning to the local directory address* 
- After running ‘read_senti_frames.py”, it generates a file called “sen_output”, it’s a text file including indicated file names with  line break  

Step 2: 
- Run “process_xml_annot.py”  
- This file read in the “sen_output” file and a folder of “fulltext” 
- This code will detect the cases when the evoked frame names match with the frame names in “sen_output” 
- This code will generate a text file “output_list”, it includes four kinds of information: 
- (1) name of the annotation text file (2) evoked frame name (3) actual text (4) sentence ID 
