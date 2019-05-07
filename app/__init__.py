import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from configparser import ConfigParser

basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.join(basedir, '..')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(parentdir, 'app.db')

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class QueryCreator:

    def __init__(self):
        self.query = ''

    # list of selected params
    def selectImage(self, values):
        values_str = ''
        for val in values:
            values_str = values_str + val + ","
        self.query = self.query + "SELECT %s FROM IMAGE " % values_str[:-1]
        return self

    def where(self, condition):
        self.query = self.query + "WHERE %s " % condition
        return self

    # def where(self, param, value):
    #    self.query = self.query + "WHERE %s = %s" % param, value
    #    return self

    def _and(self, param, value, operator):
        self.query = self.query + "AND %s %s %s " % (param, operator, value)
        return self

    def order(self, column, order="ASC"):
        self.query = self.query + "ORDER BY %s %s " % (column, order)
        return self

    def limit(self, limit):
        self.query = self.query + "LIMIT %s " % limit
        return self

    def build(self):
        return self.query + ";"


class Database:

    def __init__(self, conf_file="app/db.ini"):
        parser = ConfigParser()
        parser.read(conf_file)

        host = parser.get('mysql', 'host')
        user = parser.get('mysql', 'user')
        password = parser.get('mysql', 'password')
        db = parser.get('mysql', 'db')
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
        self.qc = QueryCreator()

    def save(self, query, args):
        # try:
        self.cur.execute(query, args)
        self.con.commit()
        # except Error as error:
        #    print(error)

    def get_image(self, id):
        self.cur.execute("SELECT name, path, priority FROM IMAGE WHERE id = %s ;", id)
        result = self.cur.fetchall()
        return result

    def get_img_ids_by_priority(self, priority, limit):
        query = self.qc.selectImage(["id"]) \
            .order("priority", "DESC") \
            .limit(limit) \
            .build()
            #.where("priority > %s" % priority) \
        print(query)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def save_annotation(self, values):
        query = "INSERT INTO ANNOTATION(gender, age, style, image_id, user_id, description) VALUES (%s, %s, %s, %s, %s, %s);"
        self.save(query, values)

    def insert_image(self, values):
        query = "INSERT INTO IMAGE(name, path, priority, error_img) VALUES (%s, %s, %s, %s);"
        self.save(query, values)

    def update_image(self, id, column_val_tuple):
        query = "UPDATE IMAGE SET " + column_val_tuple[0] + " = %s WHERE id = %s ;"
        values = (column_val_tuple[1], id)
        self.save(query, values)
        # print ("db - ROW UPDATED.")

    def insert_images(self, images_list):
        for image in images_list:
            self.insert_image((image["name"], image['path'], image["priority"], image["error_img"]))

    def get_images_ids(self):
        query = "SELECT i.id, name, count(*) as count FROM IMAGE i " \
                "INNER JOIN ANNOTATION a on a.image_id = i.id " \
                "WHERE i.error_img = false " \
                "GROUP BY i.id " \
                "HAVING count(*) >= 2; "
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_annotations_by_img_id(self, img_id):
        self.cur.execute("SELECT name, gender, age, style FROM ANNOTATION a JOIN IMAGE i ON a.image_id = i.id WHERE "
                         "i.id = %s; ", img_id)
        result = self.cur.fetchall()
        return result
