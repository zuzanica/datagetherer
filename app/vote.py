import random
from flask import jsonify, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, TextField, TextAreaField
from wtforms import StringField, SelectMultipleField
from wtforms.validators import Required
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

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

    style = RadioField(label='Mode style',
                       choices=[('0', '<img src="/static/modestyle/casual.png"> <div class="desc">casual</div>'),
                                ('1', '<img src="/static/modestyle/sport.png"> <div class="desc">sport</div>'),
                                ('2', '<img src="/static/modestyle/rock.png"> <div class="desc">rock</div>'),
                                ('3', '<img src="/static/modestyle/street.png"> <div class="desc">street</div>'),
                                ('4', '<img src="/static/modestyle/elegant.png"> <div class="desc">elegant</div>'),
                                ('5', '<img src="/static/modestyle/formal.png"> <div class="desc">formal</div>'),
                                ('6', '<img src="/static/modestyle/worksuit.png"> <div class="desc">work suit</div>'),
                                ],
                       validators=[validators.DataRequired("Please select style.")]
                       )
    description = TextField("Something more? ")


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
    print("priority:", selected_img["priority"])
    # id = random.randrange(1, 100)
    # path = "2.jpg"
    if request.method == 'POST':
        if form.validate_on_submit() and request.form['form-type'] == 'Confirm »':
            checked_gender = request.form['gender']
            checked_age = request.form['age']
            checked_style = request.form['style']
            descr = request.form['description']
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

    #else:
        #print("Ina metoda.")

    return render_template('datagetherer.html', form=form, image=selected_img)
    return jsonify({'error': 'Image id not found'}), 200
