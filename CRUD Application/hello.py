from flask import render_template, Flask, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz  # 3rd party: $ pip install pytz
from flask_migrate import Migrate, MigrateCommand
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import func

# Create Flask Instance
app = Flask(__name__)

mysql = MySQL(app)
# Add Database
#SQLit DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
#MYSQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aimsol123@localhost/employee'
#initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#secret key
app.config['SECRET_KEY'] = "my secret key "

#Create Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    field = db.Column(db.String(200), nullable=False)
    #date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Karachi')))

    # Create a String -------- put name on the screen
    def __repr__(self):
        return '<Name %r>' % self.name

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute")

    # convert pass into hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    '''db creation will be done from terminal
        winpty python
        from hello import db
        db.create_all()
        exit()
    '''
@app.route('/employees/details', methods=['GET', 'POST'])
def show_employee():
    our_employees = Employee.query.order_by(Employee.date_added)
    # will display all students in the db
    rows = db.session.query(Employee).count()
    print(rows)
    return render_template("add_employee.html",
                           our_employees=our_employees,
                           rows=rows)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Employee.query.get_or_404(id)
    name = None
    form = EmployeeForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(user_to_delete.name + "'s record deleted successfully")

        our_employees = Employee.query.order_by(Employee.date_added)
        return show_employee()

    except:
        flash("oopps, there was an error deleting the user")
        return render_template("add_employee.html",
                               name=name,
                               form=form,
                               our_employees=our_employees)

class EmployeeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    field = StringField("Field", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Update
#update db records
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = EmployeeForm()
    name_to_update = Employee.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.field = request.form['field']
        name_to_update.field = request.form['field']
        try:
            db.session.commit()
            flash(name_to_update.name + "'s record updated successfully")
            return show_employee()
        except:
            flash("Error! Looks like there was a problem .... Try again")
            return show_employee()

    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


# Add
@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    name = None
    form = EmployeeForm()
    if form.validate_on_submit():
        # checking if there any student with similar email
        employee = Employee.query.filter_by(email=form.email.data).first()

        if employee is None:
            #hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            employee = Employee(name=form.name.data, email=form.email.data, field=form.field.data, password_hash=hashed_pw)
            db.session.add(employee)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.field.data = ''
        form.password_hash.data = ''
        flash("Employee (" + name +  ") added successfully")
        return show_employee()

    return render_template("add.html",
                           form=form,
                           name=name)




class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a Form Class (first make secret key)
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a Form Class (first make secret key)
class PasswordForm(FlaskForm):
    email = StringField("What's your Email?", validators=[DataRequired()])
    password_hash = PasswordField("What's your Password?", validators=[DataRequired()])
    submit = SubmitField("Submit")

    #BooleanField, DateField, DateTimeField, DecimalField, FileField, HiddenField
    #MultipleField, FieldList, FloatField, FormField, IntegerField, PasswordField
    #RadioField, SelectField, SelectMultipleField, SubmitField, StringField, TextAreaField

    ##Validators
    #DataRequired, Email, EqualTo, InputRequired, IPAddress, Length, MacAddress, NumberRange
    #Optional, Regexp, URL, UUID, AnyOf, NoneOf
# priniting with jinja

# FILTERS !!!!
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
        flash("User added successfully.")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           name=name,
                           form=form,
                           our_users=our_users)

@app.route('/')
def index():
    first_name = "Hasan"
    stuff = "This is bold text."

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41.5, "civic"]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza = favorite_pizza)


#127.0.0.1:5000/user/hasan'

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# end # priniting with jinja

# custom error pages

# 1. Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# 2. Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
# end custom error page

#Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None

    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #to clear the form
        form.email.data = ''
        form.password_hash.data = ''

        #Lookup user by email address
        pw_to_check = Employee.query.filter_by(email=email).first()

        #check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)

        #flash("Form Submitted successfully")
    return render_template("test_pw.html",
                           email = email,
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed,
                           form = form)

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")
    return render_template("name.html",
                           name = name,
                           form = form)

if __name__ == "__main__":
    app.run(debug=True)