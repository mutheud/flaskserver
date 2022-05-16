# creating a Flask web server from the Flask module
from ast import Raise
from flask import Flask, redirect, render_template, url_for,jsonify,json, request
# To access incoming request data and to give access to it.
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from sqlalchemy import true
from wtforms import Form,StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Length,ValidationError

# __name__ means this current file.
app = Flask(__name__)
db = SQLAlchemy(app)
# connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '778c0a53c37b7877e05047af5474b46a'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/", methods = ['POST','GET'])
def home():
   return render_template("about.html")

@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/login/results.json", methods = ['POST','GET'])
def confirm_login():
   if request.method == "POST":
      login_data = request.form
      # serializing
      login_json = json.dumps(login_data)
      login_j = json.loads(login_json)
      print(type(login_j))

      with open("register.json","r") as outfile:
         #Reads the json file and creates a python dictionary
         dyta = json.load(outfile)
         print(type(dyta))
         # iterate through all key,values in the dict:
         if dyta['email'] == login_j.get('email') and dyta['psw'] == login_j.get('psw'):
            return redirect(url_for('home'))
         else:
            return "Incorrect email or password"
   return login_data


@app.route("/register")
def register():
   return render_template("register.html")

@app.route("/register/resultsjson", methods = ['POST','GET'])
def resultsJSON():
   if request.method == 'POST':
      results_data = request.form
      # converting dictionary to json
      data_json = jsonify(results_data)
      # read to register.json file
      with open("register.json","r") as outfile:
         # creating a json object in the form of key/value pair

         account = json.loads(outfile.read())
         for a in account:
            if a.get('email') == data_json.json.get('email'):
               raise ValidationError("User Already Exists")
               # print("User exists")
               break
            else:
               with open("register.json","a+") as f:
                  # import ipdb; ipdb.set_trace()
                  f.write(str(data_json.json))

   return data_json


# @app.route('/success/<name>')
# def success(name):
#    # return value automatically respondss with response status code and json data (jsonify) or text or html templates.
#    return 'welcome %s' % name

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('success',name = user))
#    else:
#       # To access parameters submitted in the URL (?key=value) you can use the args attribute:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

@app.route("/contact")
def contact():
   return render_template("contact.html")

@app.route("/data/",methods = ['POST','GET'])
def data():
   if request.method == 'POST':
      form_data = request.form
      return render_template('data.html',form_data = form_data)



if __name__ == '__main__':
   # This will help us trace the errors.
   app.run(debug = True)
