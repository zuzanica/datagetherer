import random
from app import Database


class ImageService:

    def __init__(self):
        self.db = Database()
        pass

    def get_img_ids_by_priority(self, priority=0, limit=30):
        return self.db.get_img_ids_by_priority(priority, limit)

    def get_rand_img_by_priority(self, priority):
        imgs = self.db.get_img_ids_by_priority(priority)
        num = random.randrange(1, len(imgs))
        print("Hodnoty z DB:", imgs[num])

        path = imgs[num]["path"]
        image_id = imgs[num]["id"]
        return {"id": image_id, "path": path}

    def get_img_by_id(self, image_id):
        img = self.db.get_image(image_id)

        print("Hodnoty z DB:", img[0]["name"], img[0]["path"], img[0]["priority"])

        path = img[0]["path"]
        priority = img[0]["priority"]
        return {"id": image_id, "path": path, "priority": priority}

    def save_annotation(self, img_id, user_id, gender=None, age=None, style=None, description=None):
        self.db.save_annotation((gender, age, style, img_id, user_id, description))

    def update_image(self, id, clmn_val):
        self.db.update_image(id, clmn_val)

    def next_rnd_id(self):
        #priority = get_random_priority()
        #print("priorita:", priority)
        ids = self.get_img_ids_by_priority()
        i = random.randrange(1, len(ids))
        print("Vybrany img z DB:", ids[i])
        return ids[i]


def get_random_priority():
    num = random.randrange(1, 100)
    # if num > 66:
    #    return 100
    # elif num > 33:
    #    return 50
    return 1
