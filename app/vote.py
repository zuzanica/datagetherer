import random
import os
from flask import jsonify, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, TextField, TextAreaField, BooleanField
from wtforms import StringField, SelectMultipleField
from wtforms.validators import Required
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

from app import app
from app.ImageService import ImageService

STORE_DATA = True
USER_ID = 12345


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class FormProject(FlaskForm):
    Code = StringField('Code', [Required(message='Please enter your code')])
    Tasks = MultiCheckboxField('Proses', [Required(message='Please tick your task')],
                               choices=[('female', 'man'), ('female', 'male')])


class DataGethererForm(FlaskForm):
    gender = RadioField(label='Gender',
                        choices=[('0', '<img src="/static/female-icon.png">'),
                                 ('1', '<img src="/static/male-icon.png">')],
                        validators=[DataRequired()]
                        )
    age = RadioField(label='Age',
                     choices=[('0', '<img src="/static/age/child.jpg"> <div class="desc"> 1+ </div>'),
                              ('1', '<img src="/static/age/teen.png"> <div class="desc"> 19+ </div>'),
                              ('2', '<img src="/static/age/youngadult.png"> <div class="desc"> 30+ </div>'),
                              ('3', '<img src="/static/age/adult.jpg"> <div class="desc"> 45+ </div>'),
                              ('4', '<img src="/static/age/retiree.png"> <div class="desc"> 60+ </div>')],
                     validators=[validators.DataRequired("Please select age.")]
                     )

    casualTooltip = '"everyday clothes, jacket, sweatshirt, shirt, jeans, tracksuit, sneakers, sandals, hookers"'
    sportTooltip = '"cyclists, runners, pads, helmet, sportswear, top, jacket, sports leggings, tracksuits, sneakers"'
    rockTooltip = '"chin, glasses, scarves, chains, accessories, dark clothes, leather, print shirts, skulls, big shoes"'
    streetTooltip = '"caps, headphones, chains, T-shirts and trousers, torn, jackets, sneakers,"'
    elegantTooltip = '"manager, clerk, shirt, sweater, jacket, coat, pants, skirt, dress, high heels, boots, stockings, handbag"'
    formalTooltip = '"heels, boots, stockings, jacket, tuxedo, dress, heels, purse"'
    workTooltip = '"soldier, cop, worker, nurse, work clothes, uniform"'
    style = RadioField(label='Mode style',
                       choices=[
                           ('0', '<div data-toggle="tooltip" data-placement="bottom" title= ' + casualTooltip + ' >'
                                                                                                                '<img data-toggle="tooltip" src="/static/modestyle/casual.png"> '
                                                                                                                '<div class="desc">casual</div> '
                                                                                                                '</div>'),
                           ('1', '<div data-toggle="tooltip" data-placement="bottom" title= ' + sportTooltip + ' >'
                                                                                                               '<img src="/static/modestyle/sport.png"> '
                                                                                                               '<div class="desc">sport</div>'
                                                                                                               '</div>'),
                           ('2', '<div data-toggle="tooltip" data-placement="bottom" title= ' + rockTooltip + ' >'
                                                                                                              '<img src="/static/modestyle/rock.png"> '
                                                                                                              '<div class="desc">rock</div>'
                                                                                                              '</div>'),
                           ('3', '<div data-toggle="tooltip" data-placement="bottom" title= ' + streetTooltip + ' >'
                                                                                                                '<img src="/static/modestyle/street.png"> '
                                                                                                                '<div class="desc">street</div>'
                                                                                                                '</div>'),
                           ('4', '<div data-toggle="tooltip" data-placement="bottom" title= ' + elegantTooltip + ' >'
                                                                                                                 '<img data-toggle="tooltip"'
                                                                                                                 'src="/static/modestyle/elegant.png"> <div class="desc">elegant</div>'
                                                                                                                 '</div>'),
                           ('5', '<div data-toggle="tooltip" data-placement="bottom" title= ' + formalTooltip + ' >'
                                                                                                                '<img data-toggle="tooltip"'
                                                                                                                'src="/static/modestyle/formal.png"> <div class="desc">formal</div>'
                                                                                                                '</div>'),
                           ('6', '<div data-toggle="tooltip" data-placement="bottom" title= ' + workTooltip + ' >'
                                                                                                              '<img data-toggle="tooltip"'
                                                                                                              'src="/static/modestyle/worksuit.png"> <div class="desc">work suit</div>'
                                                                                                              '</div>'),
                       ],
                       validators=[validators.DataRequired("Please select style.")]
                       )

    backpack = BooleanField('<img class="attribute" src="/static/attributes/backpack.jpg">', default=False)
    handbag = BooleanField('<img class="attribute" src="/static/attributes/handbag.jpg">', default=False)
    shopping = BooleanField('<img class="attribute" src="/static/attributes/shopping.png">', default=False)
    glasses = BooleanField('<img class="attribute" src="/static/attributes/glasses.jpg">', default=False)
    cap = BooleanField('<img class="attribute" src="/static/attributes/cap.jpg">', default=False)
    description = TextField("Something more? ")


def process_attribudes(form):
    desc = form['description']
    if 'backpack' in form:
        desc += ' backpack'
    if 'handbag' in form:
        desc += ' handbag'
    if 'shopping' in form:
        desc += ' shoppingbag'
    if 'glasses' in form:
        desc += ' glasses'
    if 'cap' in form:
        desc += ' cap'
    return desc


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
    form.gender(class_="my_class")

    selected_img = imageService.get_img_by_id(image_id)
    if os.path.isfile("app/static/clear/" + selected_img["path"]):
        selected_img["resized_image"] = "clear/" + selected_img["path"]
    else:
        selected_img["resized_image"] = selected_img["path"]
    print("id obr:", selected_img["id"])
    if request.method == 'POST':
        if form.validate_on_submit() and request.form['form-type'] == 'Confirm »':
            checked_gender = request.form['gender']
            checked_age = request.form['age']
            checked_style = request.form['style']
            descr = process_attribudes(request.form)
            print("gender:", checked_gender)
            print("age:", checked_age)
            print("style:", checked_style)
            print("description:", descr)
            if (STORE_DATA):
                user_id = request.cookies.get('id')
                print("id user: ", user_id)
                new_priority = round(selected_img["priority"] / 2)
                imageService.update_image(selected_img["id"], ("priority", new_priority))
                imageService.save_annotation(selected_img['id'],
                                             user_id,
                                             int(checked_gender),
                                             int(checked_age),
                                             int(checked_style),
                                             descr)
            next_img_id = imageService.next_rnd_id()
            return redirect(url_for('image', image_id=str(next_img_id["id"])))
        elif request.form['form-type'] == 'Bad image':
            imageService.update_image(selected_img["id"], ("error_img", True))
            next_img_id = imageService.next_rnd_id()
            return redirect(url_for('image', image_id=str(next_img_id["id"])))
        elif request.form['form-type'] == 'Skip »':
            next_img_id = imageService.next_rnd_id()
            return redirect(url_for('image', image_id=str(next_img_id["id"])))

    return render_template('datagetherer.html', form=form, image=selected_img)
    return jsonify({'error': 'Image id not found'}), 200
