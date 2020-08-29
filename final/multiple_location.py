import os
from glob import glob


path = ('/mnt/rds/redhen/gallina/tv/2019/2019-03')

with open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/multiple_location/location_frame_list') as f:
    lines = f.readlines()
    frame_list = []

    for i in lines:
        frame_list.append(i.strip())

    # generate a list of frame name from a folder of frame data
    frame_list = [x[:-4] for x in frame_list]


def word(path):
    final_result_list = []

    rec_list = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.seg'))]
    for filename in rec_list:

        final_result_list.append(filename)

        real_name = filename.split('/')[-1]

        output = []
        eval = []

        for line in open(filename, 'r'):

            output.append(line)

            if 'CC1' in line:
                current_frame_list = []
                key = line


            elif 'FRM_01' in line:

                for f in frame_list:
                    if f.lower() == line.split('|')[5].lower():

                        current_frame_list.append(f.lower())

                        if len(current_frame_list) > 1:  # list is NOT empty before adding 1

                            FBL_label = []
                            FBL_label.append(line.split('|')[0])
                            FBL_label.append('|')
                            FBL_label.append(line.split('|')[1])
                            FBL_label.append('|')
                            FBL_label.append('FBL_01')
                            FBL_label.append('|')
                            FBL_label.append('multiple_location')
                            FBL_label.append('|')
                            FBL_label.append(' '.join(current_frame_list))

                            fbl_str = ''.join(FBL_label)
                            output.append(fbl_str)

                            eval.append(fbl_str)
                            eval.append(key)

        f1 = open(
            '/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/multiple_location/multiple_location_output/trial_2/' + real_name[ :-3] + 'fbl', "w")
        for item in output:
            f1.write("%s" % item)

        f2 = open('/mnt/rds/redhen/gallina/home/wxx170/frameblends_pipeline/nomination_algorithms/multiple_location/multiple_location_eval/trial_2/' + real_name[:-3] + 'txt', "w")
        for item in eval:
            f2.write("%s" % item)


def main():
    word(path)


if __name__ == "__main__":
    main()
