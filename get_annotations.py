from collections import Counter
from app import Database
import argparse

parser = argparse.ArgumentParser(description='get annotations from database')
parser.add_argument('--file', type=str, default='')
args = parser.parse_args()


def get_annotation_form_db():
    db = Database(conf_file="app/db.ini")
    annotations = []
    reanotate_age = []
    reanotate_style = []
    reanotate_gender = []
    image_ids = db.get_images_ids()
    for img in image_ids:
        img_annotations = db.get_annotations_by_img_id(img["id"])
        #img_annotations = db.get_annotations_by_img_id(111)
        annotation_dict, state = filter_one_annotaion(img_annotations)
        if state == 'age':
            reanotate_age.append(str(img_annotations[0]["id"]) + ',' + img_annotations[0]["name"])
        elif state == 'style':
            reanotate_style.append(str(img_annotations[0]["id"]) + ',' + img_annotations[0]["name"])
        elif state == 'gender':
            reanotate_gender.append(str(img_annotations[0]["id"]) + ',' + img_annotations[0]["name"])
        else:
            annotations.append(annotation_dict)


    save_reanotate(reanotate_age, "re_age_" + args.file[:-4] + ".txt")
    save_reanotate(reanotate_gender, "re_gender_" + args.file[:-4] + ".txt")
    save_reanotate(reanotate_style, "re_style_" + args.file[:-4] + ".txt")
    return annotations


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
            return {}, 'gender'
    if len(age_counter.most_common(2)) >1:
        a1 = age_counter.most_common(2)[0][1]
        a2 = age_counter.most_common(2)[1][1]
        if a1 == a2:
            return {}, 'age'
    if len(style_counter.most_common(2)) >1:
        s1 = style_counter.most_common(2)[0][1]
        s2 = style_counter.most_common(2)[1][1]
        if s1 == s2:
            return {}, 'style'

    ann = {"name": all_annotations[0]["name"],
           "gender": g_counter.most_common(1)[0][0],
           "age": age_counter.most_common(1)[0][0],
           "style": style_counter.most_common(1)[0][0]}
    print(ann)
    return ann, ""


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

all_annotations = get_annotation_form_db()
save_annotations(all_annotations, args.file)


