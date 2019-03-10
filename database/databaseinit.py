from app import Database
import os

file_name = "BUT_dataset.txt"


def create_images_from_file(file):
    db = Database()
    img_list = []
    f = open(file, "r")
    img_names = f.readlines()
    for img in img_names:
        img_list.append({"name": img[:-1], "path": ("dataset/" + img[:-1]), "priority": 5})

    for img_dict in img_list:
        print (img_dict)
    f.close()

   #db.insert_images(img_list)


create_images_from_file(file_name)
