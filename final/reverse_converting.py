import glob
import os
import pandas as pd

# address of output data with fbl label, need adding manual annoation as parameters
# Input data
data= '/Users/mac/Desktop/reverse_converting/in_test/Final'


spreadsheet = '/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/converting/spreadsheet/spreadsheet_3.xls'


def convert(data):
    sheet1 = pd.read_excel(spreadsheet, index_col=0)

    for filename in glob.glob(os.path.join(data, '*.seg')):

        output = []
        for line in open(filename, 'r'):

            output.append(line)
            length = len(sheet1)
            print(length)

            for row in (0, length - 1):

                label = sheet1.iloc[row, 0]

                file = str(sheet1.iloc[row, 1])

                tag = str(sheet1.iloc[row, 2])

                if file == filename:
                    if label in line:
                        # build new manual tagging
                        FBL_tag = []
                        FBL_tag.append(line.split('|')[0])
                        FBL_tag.append('|')
                        FBL_tag.append(line.split('|')[1])
                        FBL_tag.append('|')
                        FBL_tag.append('FBL_manual')
                        FBL_tag.append('|')
                        # make change according to nomination methods
                        FBL_tag.append('frame_embedding')
                        FBL_tag.append('|')
                        FBL_tag.append(tag)
                        fbl_str = ''.join(FBL_tag)
                        output.append(fbl_str)
                    else:
                        output.append(line)


            f1 = open(file, "w")
            for item in output:
                f1.write("%s" % item)


def main():
    convert(data)

if __name__ == "__main__":
    main()

