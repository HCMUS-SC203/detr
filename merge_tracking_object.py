import glob
import sys
import shutil
from PIL import Image, ImageDraw
import sys
import requests
import random

import matplotlib.pyplot as plt

def getRandomSet(n, k):
    # from 0 to n, choose k numbers
    res = set()
    while (len(res) < k):
        res.add(random.randint(0, n - 1))
    res.sort()
    return res



def add_white_rectangle(img_path, online = False):
    IMAGE_PADDING = 250
    if (online == False):
        img = Image.open(img_path).convert("RGB")
    else:
        img = Image.open(requests.get(img_path, stream=True).raw).convert("RGB")
    # Open the image file

    # Create a new image with the same width and increased height
    new_img = Image.new('RGB', (img.width, img.height + IMAGE_PADDING), color='white')

    # Paste the original image onto the new image
    new_img.paste(img, (0, 0))

    # Draw a white rectangle at the bottom of the new image
    draw = ImageDraw.Draw(new_img)
    draw.rectangle((0, img.height, img.width, img.height + IMAGE_PADDING), fill='white')


    # Return the new image
    return new_img

def read_label_file(label_path):
    f = open(label_path, "r")
    lines = f.readlines()
    f.close()
    label_set = []
    for line in lines:
        line = line.strip()
        line = line.split(" ")
        label_set.append(line)
    return label_set

def contain_pedestrian(label_set):
    for label in label_set:
        if label[0] == "Pedestrian" or label[2] == "Pedestrian":
            return True
    return False


def export_tracking(source_img_path, source_label_path, dest_img_path, dest_label_path):
    OFFSET = 100000
    # chosen_folder = [13, 16, 17, 19]
    chosen_folder = [13, 16, 17]
    img_cnt = OFFSET
    for folder in chosen_folder:
        folder_name = str(str(folder)).zfill(4)
        folder_path = source_img_path + folder_name + "/"
        print("extracting folder " + folder_name)
        print("folder path: " + folder_path)
        img_path_set = glob.glob(folder_path + "*.png") + glob.glob(folder_path + "*.jpg")
        img_path_set.sort()
        label_set = read_label_file(source_label_path + folder_name + ".txt")
        # print("label set:")
        # print(label_set, end="\n")
        l = 0
        for source_single_img_path in img_path_set:
            # copy img to destination
            img_name = str(img_cnt).zfill(6) + ".jpg"
            dest_single_img_path = dest_img_path + img_name
            print("copying " + source_single_img_path + " to " + dest_single_img_path)
            padded_img = add_white_rectangle(source_single_img_path, False)
            padded_img.save(dest_single_img_path)
            # copy label to destination
            while (l < len(label_set) and label_set[l][0] != str(img_cnt - OFFSET)):
                l += 1
            r = l
            while (r < len(label_set) and label_set[r][0] == str(img_cnt - OFFSET)): # same frame
                r += 1
            print(source_single_img_path, img_cnt, l, r)
            single_label_set = label_set[l:r]
            res_label_set = []
            for label in single_label_set:
                if (label[2] == "Pedestrian"):
                    # delete label[0], label[1] and change label[2] to 'person'
                    label.pop(0)
                    label.pop(0)
                    label[0] = "person"
                    res_label_set.append(label)
            l = r
            label_name = str(img_cnt).zfill(6) + ".txt"
            dest_single_label_path = dest_label_path + label_name
            print("formating labels to " + dest_single_label_path)
            print(res_label_set)
            f = open(dest_single_label_path, "w")
            for label in res_label_set:
                f.write(" ".join(label) + "\n")
            f.close()
            img_cnt += 1
            



# def export_detection(source_path, dest_path):
#     img_cnt = 0
#     img_path_set = glob.glob(source_path + "*.png") + glob.glob(source_path + "*.jpg")
#     img_path_set.sort()
#     for source_img_path in img_path_set:
#         # copy file to destination
#         img_name = str(img_cnt).zfill(6) + source_img_path[-4:]
#         img_cnt += 1
#         dest_img_path = dest_path + img_name
#         print("copying " + source_img_path + " to " + dest_img_path)
#         # shutil.copyfile(source_img_path, dest_img_path)
#         padded_img = add_white_rectangle(source_img_path, False)
#         padded_img.save(dest_img_path)

def read_img_list(file_path):
    f = open(file_path, "r")
    img_list = f.readlines()
    f.close()
    return img_list

def write_img_list(res_file_path, file_path_set, n, k):
    # from 0 to n, choose k numbers
    res_set = getRandomSet(n, k)
    f = open(res_file_path, "w")
    for i in res_set:
        f.write(file_path_set[i] + "\n")
    f.close()

def export_detection(source_img_path, source_label_path, dest_root_path):
    img_cnt = {"train": 0, "val": 0}
    img_path_set = glob.glob(source_img_path + "*.png") + glob.glob(source_img_path + "*.jpg")
    train_img_list = read_img_list("img_list.txt")
    print("train img list: ")
    print(train_img_list)
    
    # for source_img_path in img_path_set:
    #     img_name = source_img_path.split("/")[-1]
    #     task = ""
    #     if source_img_path in train_img_list:
    #         task = "train"
    #     else:
    #         task = "val"
    #     dest_root_task_path = dest_root_path + task + "/"

    #     # read label
    #     label_set = read_label_file(source_label_path + img_name[:-4] + ".txt")
    #     res_label_set = []
    #     cyclist_cnt = 0
    #     for label in label_set:
    #         if label[0] == "Pedestrian":
    #             label[0] = "person"
    #             res_label_set.append(label)
    #         elif label[0] == "Cyclist":
    #             cyclist_cnt += 1
    #     if len(res_label_set) == 0 and cyclist_cnt == 0:
    #         continue
    #     # copy label to destination
    #     label_name = str(img_cnt[task]).zfill(6) + ".txt"
    #     single_dest_label_path = dest_root_task_path + "labels/" + label_name
    #     print("formating labels to " + single_dest_label_path)
    #     print(res_label_set)
    #     f = open(single_dest_label_path, "w")
    #     for label in res_label_set:
    #         f.write(" ".join(label) + "\n")
    #     f.close()
    #     # copy img to destination
    #     img_name = str(img_cnt[task]).zfill(6) + ".jpg"
    #     single_dest_img_path = dest_root_task_path + "images/" + img_name
    #     print("copying " + source_img_path + " to " + single_dest_img_path)
    #     # shutil.copyfile(source_img_path, dest_img_path)
    #     padded_img = add_white_rectangle(source_img_path, False)
    #     padded_img.save(single_dest_img_path)
    #     img_cnt[task] = img_cnt[task] + 1

# def export(source_path, dest_path, type):
#     if type == "Tracking":
#         export_tracking(source_path, dest_path)
#     elif type == "Detection":
#         export_detection(source_path, dest_path)
#     else:
#         print("Wrong type")

def export(source_img_path, source_label_path, dest_img_path, dest_label_path, type):
    if type == "Tracking":
        export_tracking(source_img_path, source_label_path, dest_img_path, dest_label_path)
    elif type == "Detection":
        export_detection(source_img_path, dest_img_path, source_label_path, dest_label_path)
    else:
        print("Wrong type")

for arg in sys.argv:
    print(arg, len(arg))

if len(sys.argv) != 5:
    print("Usage: python merge_tracking_object.py source_img_path source_label_path dest_img_path dest_label_path type")
    sys.exit(1)

source_img_path = sys.argv[1]
source_label_path = sys.argv[2]
dest_root_path = sys.argv[3]

type = sys.argv[4]

if source_img_path[-1] != "/":
    source_img_path += "/"
if source_label_path[-1] != "/":
    source_label_path += "/"
if dest_root_path[-1] != "/":
    dest_root_path += "/"

if (type == "Detection"):
    img_path_set = glob.glob(source_img_path + "*.png") + glob.glob(source_img_path + "*.jpg")
    num_train_img = 1000
    num_val_img = len(img_path_set) - num_train_img
    write_img_list("img_list.txt", img_path_set, len(img_path_set), num_val_img)
    export_detection(source_img_path, source_label_path, dest_root_path)

# py merge_tracking_object.py "D:/kitti_tracking_pedestrian/training/images" "D:/kitti_tracking_pedestrian/training/labels" "C:/APCS/Scientific Method/Midterm Presentation/Merged_KITTI/images" "C:/APCS/Scientific Method/Midterm Presentation/Merged_KITTI/labels" "Tracking"