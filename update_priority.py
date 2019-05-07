from app import Database
import argparse

parser = argparse.ArgumentParser(description='insert images')
parser.add_argument('--import_file', type=str, default='test.txt')
args = parser.parse_args()


def create_images_from_file(file):
    db = Database()
    img_list = []
    f = open(file, "r")
    img_names = f.readlines()
    for img in img_names:
        img_id = img.split(',')[0]
        db.update_image(img_id, ("priority", 120))

    f.close()


create_images_from_file(args.import_file)