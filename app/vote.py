import random
from flask import jsonify, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import StringField, SelectMultipleField
from wtforms.validators import Required
from wtforms.widgets import ListWidget, CheckboxInput

from app import app, Database
STORE_DATA = True
USER_ID = 12345

gender = {"men", "female"}
age = {"child", "teen", "adult", "retire"}


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class FormProject(FlaskForm):
    Code = StringField('Code', [Required(message='Please enter your code')])
    Tasks = MultiCheckboxField('Proses', [Required(message='Please tick your task')],
                               choices=[('female', 'man'), ('female', 'male')])


class DataGethererForm(FlaskForm):
    gender = RadioField('Gender', choices=[('0', 'male'), ('1', 'female')])
    age = RadioField('Gender', choices=[('0', 'child'), ('1', 'teen'), ('2', 'adoult'), ('3', 'retiree')])


class ImageService:

    def __init__(self):
        self.db = Database()
        pass

    def get_img_ids_by_priority(self, priority):
        return self.db.get_img_ids_by_priority(priority)

    def get_rand_img_by_priority(self, priority):
        imgs = self.db.get_img_ids_by_priority(priority)
        num = random.randrange(1, len(imgs))
        print("Hodnoty z DB:", imgs[num])

        path = imgs[num]["path"]
        image_id = imgs[num]["id"]
        return {"id": image_id, "path": path}

    def get_img_by_id(self, image_id):
        img = self.db.get_image(image_id)

        print("Hodnoty z DB:", img[0]["name"], img[0]["path"])

        path = img[0]["path"]
        return {"id": image_id, "path": path}

    def save_annotation(self, img_id, user_id, gender=None, age=None):
        self.db.save_annotation((gender, age, img_id, user_id))

    def next_rnd_id(self):
        priority = get_random_priority()
        print("priorita:", priority)
        ids = self.get_img_ids_by_priority(priority)
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


'''
@app.route('/test/')
def vote():
    if request.json and 'classification' in request.json:
        return jsonify({'response': classification}), 200
    else:
        return jsonify({'response': 'Not found'}), 404
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imageService = ImageService()
        next_img_id = imageService.next_rnd_id()
        return redirect(url_for('image', image_id=str(next_img_id["id"])))

    return render_template('index.html')


@app.route('/image/<int:image_id>', methods=['GET', 'POST'])
def image(image_id):
    print("*******************************")
    imageService = ImageService()
    form = DataGethererForm(request.form)

    selected_img = imageService.get_img_by_id(image_id)
    print("id obr:", selected_img["id"])

    # id = random.randrange(1, 100)
    # path = "2.jpg"
    if request.method == 'POST':
        checked_gender = request.form['gender']
        checked_age = request.form['age']
        print("gender:", checked_gender)
        print("age:", checked_age)
        if (STORE_DATA):
            imageService.save_annotation(selected_img['id'], USER_ID, int(checked_gender), int(checked_age))

        next_img_id = imageService.next_rnd_id()
        return redirect(url_for('image', image_id=str(next_img_id["id"])))
    else:
        print("Ina metoda.")

    return render_template('datagetherer.html', form=form, image=selected_img)
    return jsonify({'error': 'Image id not found'}), 200
