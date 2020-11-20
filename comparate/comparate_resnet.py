import click
import os
import sys
import pickle
import glob
import cv2
import numpy as np
from pdb import set_trace
from distutils.dir_util import copy_tree
import shutil


def generate_video():
    os.chdir(r"../lib/utils/labels/")
    # set_trace()
    os.system("./generates_comparate_pickle_file.sh")
    shutil.copy2(r"labels_comparate.pkl", r"../../../annotations/A3D/")
    os.chdir(r"../../../")
    os.system(r"python3 download_videos.py --load_config comparate/download.yaml")
    os.system(
        r"python3 split_videos2frames.py --load_config comparate/videos2frames.yaml"
    )
    os.system(
        r"python3 extract_short_clips.py --load_config comparate/short_clips.yaml"
    )


def pickle2dict(file):
    file_in = file
    try:
        with open(file_in, "rb") as fi:
            mydict = pickle.load(fi)

    except FileNotFoundError as fnf:
        print("\033[41mError:\033[0m {} \033[31mnot found.\033[0m".format(file))
        sys.exit(1)
    except PermissionError:
        print(
            "\033[41mError:\033[0m {} \033[31mYou don't have permission to open this file.\033[0m".format(
                file
            )
        )
        sys.exit(1)

    return mydict


def classification_images():
    os.system(
        r"python3 comparate/resnet_test.py --load_config comparate/resnet_comparate.yaml"
    )


def reconstroi_videos():
    labels = pickle2dict("annotations/A3D/labels_comparate.pkl")
    if not os.path.isdir("comparate/short_clips/"):
        print("The short_clips directory does not exist! Aborting..\n")
        sys.exit(1)

    if not os.path.isdir("comparate/short_clips_nn_res/"):
        print("The rec_videos directory does not exist! creating..\n")
        os.makedirs("comparate/short_clips_nn_res/")

    in_dir = "comparate/short_clips/"
    out_dir = "comparate/short_clips_nn_res/"
    out_dir2 = "comparate/short_clips_final/"
    copy_tree(in_dir, out_dir)
    copy_tree(in_dir, out_dir2)

    all_short_clips = sorted(
        glob.glob(os.path.join("comparate/short_clips_nn_res/", "*"))
    )

    assert len(all_short_clips) > 0

    print(
        "Total number of short_clips found: \033[1;31m{}\033[0m".format(
            len(all_short_clips)
        )
    )

    num_short_clips = 0
    for clip in all_short_clips:
        path, folder = os.path.split(clip)
        # print(path)
        # print(folder)
        print("\033[1;36m" + "  Processing Short Clip {}..".format(folder) + "\033[0m")

        all_frames = sorted(glob.glob(os.path.join(path, folder, "*")))
        # print(all_frames[0])

        mark = np.load(
            "comparate/saidas_rede_res/short_" + str(num_short_clips) + ".npy"
        )
        for frame in range(len(all_frames)):
            if mark[frame] == 1:
                image = cv2.imread(all_frames[frame])
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                text = "Accident Detected!!"
                text1 = "Resnet"
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (320, 340)
                org1 = (320, 420)
                fontScale = 2.0
                color = (20, 20, 235)
                thickness = 4
                # Using cv2.putText() method
                image = cv2.putText(
                    image,
                    text,
                    org,
                    font,
                    fontScale,
                    color,
                    thickness,
                    cv2.LINE_AA,
                    False,
                )
                image = cv2.putText(
                    image,
                    text1,
                    org1,
                    font,
                    fontScale,
                    color,
                    thickness,
                    cv2.LINE_AA,
                    False,
                )
                cv2.imwrite(all_frames[frame], image)
                # cv2.imshow("Previsao", image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        num_short_clips += 1
        # break
    os.system(
        r"python3 mark_short_clips.py --load_config comparate/mark_short_clips.yaml"
    )
    os.system(r"python3 make_videos.py --load_config comparate/make_videos.yaml")
    print("Number of short clips marked: \033[1;31m{}\033[0m".format(num_short_clips))
    os.system(r"python3 make_videos.py --load_config comparate/make_videos_res.yaml")


def main():
    generate_video()
    classification_images()
    reconstroi_videos()


if __name__ == "__main__":
    main()
