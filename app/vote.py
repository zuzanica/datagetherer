from app import app, Database
from flask import Flask, jsonify, request, render_template, flash, redirect
from wtforms import Form, TextField, TextAreaField, validators, SubmitField, RadioField

from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import Required

import random

STORE_DATA = False
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

    def get_img_by_priority(self, priority):

        imgs = self.db.get_imgages_by_priority(priority)
        num = random.randrange(1, len(imgs))
        print("Hodnoty z DB:", imgs[num])

        path = imgs[num]["path"]
        image_id = imgs[num]["id"]
        return {"label": image_id, "path": path}

    def get_img_by_id(self, image_id):
        img = self.db.get_image(image_id)

        print("Hodnoty z DB:", img[0]["name"], img[0]["path"])

        path = img[0]["path"]
        return {"label": image_id, "path": path}

    def save_annotation(self, img_id, user_id, gender=None, age=None):
        self.db.save_annotation((gender, age, img_id, user_id))


def get_random_priority():
    num = random.randrange(1, 100)
    #if num > 66:
    #    return 100
    #elif num > 33:
    #    return 50
    return 1


@app.route('/vote/', methods=['GET', 'POST'])
def classification():
    print("*******************************")
    imageService = ImageService()
    priority = get_random_priority()
    print("priorita:", priority)
    selected_img = imageService.get_img_by_priority(priority)

    form = DataGethererForm(request.form)
    if request.method == 'POST':
        checked_gender = request.form['gender']
        checked_age = request.form['age']
        print("gender:", checked_gender)
        print("age:", checked_age)
        if (STORE_DATA):
            imageService.save_annotation(selected_img['label'], USER_ID, int(checked_gender), int(checked_age))
            # return redirect(url_for('success', result_id=result.id))

    return render_template('datagetherer.html', form=form, image=selected_img)
    return jsonify({'error': 'Image id not found'}), 200


@app.route('/test/')
def vote():
    if request.json and 'classification' in request.json:
        return jsonify({'response': classification}), 200
    else:
        return jsonify({'response': 'Not found'}), 404


@app.route('/image/<int:image_id>')
def image(image_id):
    id = random.randrange(1, 100)
    path = "2.jpg"
    return render_template('image.html', image_id=id, image_path=path)
    return jsonify({'error': 'Image id not found'}), 200


