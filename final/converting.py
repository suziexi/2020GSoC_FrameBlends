import glob
import os
import xlwt
from xlwt import Workbook

path = '/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/multiple_location/multiple_location_eval' 

def convert(path):
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    print('1')

    for filename in glob.glob(os.path.join(path, '*.txt')):
        # if not filename.endswith('.xml'):
        #     continue
        number = -1
        name = filename.split('/')[-1]
        for line in open(filename, 'r'):
            if 'CC1' in line:
                case = []
                number = number + 1
                st = str(number)
                case.append('\n')
                case.append(line)


            else:
                case.append(line)
                # case.append('\n')
                print('Case:')
                print(case)

            print(filename)
            print(name)
            print(st)

            name = name.split('.')[0]



            address = '/Users/mac/Desktop/converting_algorithm/pair_output/' + name + '_' + st + '.txt'
            f1 = open(address, "w+")

            for item in case:
                f1.write("%s" % item)

            print(address)

            try:
                sheet1.write(number, 0, st)
                sheet1.write(number, 1, case)
                sheet1.write(number, 2, address)
            except:
                continue

    wb.save('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/spreadsheet/spreadsheet_1')



def main():
    convert(path)



if __name__ == "__main__":
    main()

