from app import Database
import argparse

parser = argparse.ArgumentParser(description='insert images')
parser.add_argument('--import_file', type=str, default='BUT_dataset.txt')
args = parser.parse_args()


def create_images_from_file(file):
    db = Database()
    img_list = []
    f = open(file, "r")
    img_names = f.readlines()
    for img in img_names:
        img_list.append({"name": img[:-1], "path": ("dataset/" + img[:-1]), "priority": 100, "error_img": False})

    for img_dict in img_list:
        print(img_dict)

    db.insert_images(img_list)
    f.close()


create_images_from_file(args.import_file)
