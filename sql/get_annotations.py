from collections import Counter
from app import Database
import argparse

parser = argparse.ArgumentParser(description='get annotations from database')
parser.add_argument('--file', type=str, default='')
args = parser.parse_args()


def get_annotation_form_db():
    db = Database(conf_file="../app/db.ini")
    annotations = []
    reanotate = []
    image_ids = db.get_images_ids()
    for img in image_ids:
        img_annotations = db.get_annotations_by_img_id(img["id"])
        #img_annotations = db.get_annotations_by_img_id(111)
        annotation_dict = filter_one_annotaion(img_annotations)
        if len(annotation_dict) == 0:
            reanotate.append(img_annotations[0]["name"])
        else:
            annotations.append(annotation_dict)

    return annotations, reanotate


def filter_one_annotaion(all_annotations):
    g_counter = Counter()
    age_counter = Counter()
    style_counter = Counter()
    for ann_dict in all_annotations:
        g_counter[int(ann_dict["gender"])] += 1
        age_counter[int(ann_dict["age"])] += 1
        style_counter[int(ann_dict["style"])] += 1

    if len(g_counter.most_common(2)) > 1:
        g1 = g_counter.most_common(2)[0][1]
        g2 = g_counter.most_common(2)[1][1]
        if g1 == g2:
            return {}
    if len(age_counter.most_common(2)) >1:
        a1 = age_counter.most_common(2)[0][1]
        a2 = age_counter.most_common(2)[1][1]
        if a1 == a2:
            return {}
    if len(style_counter.most_common(2)) >1:
        s1 = style_counter.most_common(2)[0][1]
        s2 = style_counter.most_common(2)[1][1]
        if s1 == s2:
            return {}

    ann = {"name": all_annotations[0]["name"],
           "gender": g_counter.most_common(1)[0][0],
           "age": age_counter.most_common(1)[0][0],
           "style": style_counter.most_common(1)[0][0]}
    print(ann)
    return ann


def save_annotations(annotations, file):
    f = open(file, "w")
    f.write("name,gender,age,style\n")
    for a in annotations:
        f.write(a["name"] + "," + str(a["gender"]) + "," + str(a["age"]) + "," + str(a["style"]) + "\n")
    f.close()


def save_reanotate(reannotate, file):
    f1 = open(file, "w")
    for r in reannotate:
        f1.write(r + "\n")
    f1.close()

all_annotations, reanontate = get_annotation_form_db()
save_annotations(all_annotations, args.file)

save_reanotate(reanontate, "re_" + args.file[:-4] + ".txt")
