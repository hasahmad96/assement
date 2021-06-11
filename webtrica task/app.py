from flask import render_template, Flask, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import DateField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

from flask_mysqldb import MySQL
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash
# Instance
app = Flask(__name__)

mysql = MySQL(app)

# Adding Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aimsol123@localhost/webtrica'

db =SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = "flask task"

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.Date(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Karachi')))

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

@app.route('/user/<name>', methods=['GET', 'POST'])
def show_employee(name):
    employee_name = Employee.query.order_by(Employee.date_added)
    return render_template("user.html",
                           employee_name=employee_name)

class EmployeeForm(FlaskForm):
    id = StringField("ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    birth_date = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/register_employee', methods=['GET', 'POST'])
def register():
    id = None
    name = None
    birth_date = None
    password = None
    pw_to_check = None
    #passed = None

    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(name=form.name.data).first()
        if employee is None:
            hashed_password = generate_password_hash(form.password_hash.data, "sha256")
            employee = Employee(id=form.id.data, name=form.name.data, password_hash=hashed_password, birth_date=form.birth_date.data)
            db.session.add(employee)
            db.session.commit()
        form.id.data = ''
        form.name.data = ''
        form.birth_date.data = ''
        form.password_hash.data = ''

        #passed = check_password_hash(pw_to_check.password_hash, password)

        #flash("Form Submitted successfully")
        #flash("Error creating the account")
    pw_to_check = Employee.query.filter_by(name=name).first()
    return render_template("register.html",
                           id=id,
                           name=name,
                           birth_date=birth_date,
                           password=password,
                           pw_to_check=pw_to_check,
                           form=form)

@app.route('/')
def index():
    first_name = "Hasan"
    stuff = "This is bold text."

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41.5, "civic"]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza = favorite_pizza)

if __name__ == "__main__":
    app.run(debug=True)