import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.join(basedir, '..')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(parentdir, 'app.db')

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

db = SQLAlchemy(app)


class QueryCreator:

    def __init__(self):
        self.query = ''

    # list of selected params
    def selectImage(self, values):
        values_str = ''
        for val in values:
            values_str = values_str + val + ","
        self.query = self.query + "SELECT %s FROM image " % values_str[:-1]
        return self

    def where(self, condition):
        self.query = self.query + "WHERE %s " % condition
        return self

    #def where(self, param, value):
    #    self.query = self.query + "WHERE %s = %s" % param, value
    #    return self

    def _and(self, param, value, operator):
        return "AND %s %s %s" % param, operator, value

    def build(self):
            return self.query + ";"

class Database:

    def __init__(self):
        host = "127.0.0.1"
        user = "zuzka"
        password = "21294"
        db = "datacollector"
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
        self.cur.execute("SELECT name, path FROM image WHERE id = %s ;", id)
        result = self.cur.fetchall()
        return result

    def get_imgages_by_priority(self, priority):
        query = self.qc.selectImage(["id", "name", "path", "priority"])\
            .where("priority = %s" % priority)\
            .build()
        print(query)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def save_annotation(self, values):
        query = "INSERT INTO ANNOTATION(gender, age,  image_id, user_id) VALUES (%s, %s, %s, %s);"
        self.save(query, values)
