import random
from flask import jsonify, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import StringField, SelectMultipleField
from wtforms.validators import Required
from wtforms.widgets import ListWidget, CheckboxInput

from app import app
from app.ImageService import ImageService

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
    gender = RadioField(label='Gender',
                        choices=[('0', '<img src="/static/female-icon.png">'),
                                 ('1', '<img src="/static/male-icon.png">')])
    age = RadioField(label='Age',
                     choices=[('0', '<img src="/static/age/child.jpg">'),
                              ('1', '<img src="/static/age/teen.png">'),
                              ('2', '<img src="/static/age/youngadult'
                                    '.png">'),
                              ('3', '<img src="/static/age/adult.jpg">'),
                              ('4', '<img src="/static/age/retiree.png">')])

    style = RadioField(label='Mode style',
                       choices=[('0', '<img src="/static/modestyle/casual.png"> <div class="desc">casual</div>'),
                                ('1', '<img src="/static/modestyle/sport.png"> <div class="desc">sport</div>'),
                                ('2', '<img src="/static/modestyle/rock.png"> <div class="desc">rock</div>'),
                                ('3', '<img src="/static/modestyle/street.png"> <div class="desc">street</div>'),
                                ('4', '<img src="/static/modestyle/elegant.png"> <div class="desc">elegant</div>'),
                                ('5', '<img src="/static/modestyle/formal.png"> <div class="desc">formal</div>'),
                                ('6', '<img src="/static/modestyle/worksuit.png"> <div class="desc">work suit</div>')]
                       )


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
    print("id obr:", selected_img["id"])

    # id = random.randrange(1, 100)
    # path = "2.jpg"
    if request.method == 'POST':
        if request.form['form-type'] == 'Next »':
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
