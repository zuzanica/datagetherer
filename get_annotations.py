from collections import Counter
from app import Database
import argparse

cap_attr = ["cap", "hat", "helmet", "helmed", "hemet"]
backpack_attr = ["backpack", "student"]
handbag_attr = ["handbag", "purse", "notebookbag", "hanbag"]
shopping_attr = ["shoppingbag", "shopping", " bag"]
headphones_attr = ["headphones"]
scarf_attr = ["scarf"]
glasses_attr = ["glasses", "sunglasses"]
cycle_attr = ["cicling", "bicyckle", "bike", "cycle", "bicycle", "cyclist"]

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
        # img_annotations = db.get_annotations_by_img_id(111)
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


def check_attr(attr_specification, desc_list):
    for desc in desc_list:
        if desc in attr_specification:
            return 1

    return 0


'''
Vytvara slovnik vyskytu atributov. 
Ak sa v hociktorej z anotácií nachádza niektoré klúčové slovo pre známi atribút, nastaví sa jeho hodnota na 1
'''


def process_description(all_annotations):
    attr_dict = { "cap" :0, "backpack" :0, "handbag" :0, "shoppingbag" :0, "headphones" :0, "scarf" :0, "glasses" :0, "cycle" :0,}
    for ann_dict in all_annotations:
        # vsetko lower case a odstranuju sa '#' a ',', potom sa delia slova podla medzery
        desc_list = ann_dict["description"].lower().replace('#', '').replace(",", '').split(' ')
        attr_dict["cap"] = 1 if attr_dict["cap"] else check_attr(cap_attr, desc_list)
        attr_dict["backpack"] = 1 if attr_dict["backpack"] else check_attr(backpack_attr, desc_list)
        attr_dict["handbag"] = 1 if attr_dict["handbag"] else check_attr(handbag_attr, desc_list)
        attr_dict["shoppingbag"] = 1 if attr_dict["shoppingbag"] else check_attr(shopping_attr, desc_list)
        attr_dict["headphones"] = 1 if attr_dict["headphones"] else check_attr(headphones_attr, desc_list)
        attr_dict["scarf"] = 1 if attr_dict["scarf"] else check_attr(scarf_attr, desc_list)
        attr_dict["glasses"] = 1 if attr_dict["glasses"] else check_attr(glasses_attr, desc_list)
        attr_dict["cycle"] = 1 if attr_dict["cycle"] else check_attr(cycle_attr, desc_list)
    return attr_dict


def filter_one_annotaion(all_annotations):
    g_counter = Counter()
    age_counter = Counter()
    style_counter = Counter()
    for ann_dict in all_annotations:
        g_counter[int(ann_dict["gender"])] += 1
        age_counter[int(ann_dict["age"])] += 1
        style_counter[int(ann_dict["style"])] += 1

    '''
    if len(g_counter.most_common(2)) > 1:
        g1 = g_counter.most_common(2)[0][1]
        g2 = g_counter.most_common(2)[1][1]
        if g1 == g2:
            return {}, 'gender'
    if len(age_counter.most_common(2)) > 1:
        a1 = age_counter.most_common(2)[0][1]
        a2 = age_counter.most_common(2)[1][1]
        if a1 == a2:
            return {}, 'age'
    if len(style_counter.most_common(2)) > 1:
        s1 = style_counter.most_common(2)[0][1]
        s2 = style_counter.most_common(2)[1][1]
        if s1 == s2:
            return {}, 'style'
    '''
    main_attr = {"name": all_annotations[0]["name"],
           "age": age_counter.most_common(1)[0][0],
           "style": style_counter.most_common(1)[0][0],
           "gender": g_counter.most_common(1)[0][0]}
    other_attrs = process_description(all_annotations)
    all_attr_lbls = {**main_attr, **other_attrs}
    print(all_attr_lbls)
    return all_attr_lbls, ""


def save_annotations(annotations, file):
    f = open(file, "w")
    f.write("name,age,style,gender,cap,backpack,handbag,shoppingbag,headphones,scarf,glasses,cycle \n")
    backpack = 0
    cap = 0
    handbag = 0
    for a in annotations:
        if a["backpack"] == 1:
            backpack = backpack + 1
        if a["cap"] == 1:
            cap = cap + 1
        if a["handbag"] == 1:
            handbag = handbag + 1
        f.write(a["name"] + "," + str(a["age"]) + "," + str(a["style"]) + "," + str(a["gender"]) + "," +
                str(a["cap"]) + "," + str(a["backpack"]) + "," + str(a["handbag"]) + "," + str(a["shoppingbag"])  + "," +
                str(a["headphones"]) + "," + str(a["scarf"]) + "," + str(a["glasses"]) + "," + str(a["cycle"]) +
                "\n")
    f.close()
    print(backpack)
    print(cap)
    print(handbag)

def save_reanotate(reannotate, file):
    f1 = open(file, "w")
    for r in reannotate:
        f1.write(r + "\n")
    f1.close()

all_annotations = get_annotation_form_db()
save_annotations(all_annotations, args.file)


