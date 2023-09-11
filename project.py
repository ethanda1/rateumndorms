from flask import Flask, render_template, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)
app.secret_key = 'hdjasodjsoaidjsaida'
dorms = [
        {
            "name": "17TH AVENUE",
            "description": "Built in 2013, the 17th Avenue residence hall has six floors with space for 600 first-year residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/17th%20Ave-University%20ave%20corner.jpg",
            "avgreview":int
        },
        {
            "name": "BAILEY",
            "description": "Built in 1949, with additions in 1981, Bailey has five floors with space for 500 residents, its own dining hall, and is connected via tunnel to the St. Paul Student Center.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/2021-08/BaileyHall_Sign2%203000%20x%201400.jpg?h=c2125e9a&itok=IXGziMiz",
            "avgreview":int
        },
        {
            "name": "CENTENNIAL",
            "description": "Built in 1950, Centennial Hall has six floors with 700 first-year and returning residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/imported/CentennialExterior-HallExterior.jpg?h=a7534cac&itok=qp9dF_D1",
            "avgreview":int
        },
        {
            "name": "COMSTOCK",
            "description": "Built in 1940, Comstock Hall has six floors of rooms for 553 first-year residents and its own dining hall.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/2021-03/Comstock.jpg?h=6cad0671&itok=YR43Z0DN",
            "avgreview":int
        },
        {
            "name": "FRONTIER",
            "description": "Built in 1959, Frontier Hall has four floors with 735 first-year and returning residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/Frontier.jpg",
            "avgreview":int
        },
        {
            "name": "MIDDLEBROOK",
            "description": "Built in 1969 (tower) and 2001 (east wing), Middlebrook houses over 900 students, including the Honors Living Learning Community, along with its own dining hall and market.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/Middlebrook_ext_bridge.jpg",
            "avgreview":int
        },
        {
            "name": "PIONEER",
            "description": "Renovated in 2019, Pioneer Hall has five floors with its own dining hall and 756 first-year and returning residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/imported/PioneerExterior-HallExterior.jpg",
            "avgreview":int
        },
        {
            "name": "SANFORD",
            "description": "Built in 1910 and renovated in 1970, Sanford has its own dining hall and space for 530 first-year residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/imported/SanfordExterior-HallExterior.jpg?h=9d0cf94b&itok=kWhUliof",
            "avgreview":int
        },
        {
            "name": "TERRITORIAL",
            "description": "Built in 1958 and expanded in 1999, Territorial Hall has four floors with 695 first-year residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/imported/TerritorialExteriorEntrance-HallExterior.jpg?h=9d0cf94b&itok=jutKY1gI",
            "avgreview":int
        },
        {
            "name": "YUDOF",
            "description": "Built in 2002, Yudof has six floors of apartments with 507 first-year and returning residents.",
            "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/Yudof.jpg",
            "avgreview":int
        },
    ]



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)

# class Dorm(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.String(255), nullable=False)
#     image_url = db.Column(db.String(255), nullable=False)
#     avgreview = db.Column(db.Integer, nullable=False)



# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(255), nullable=False)
#     dorm_id = db.Column(db.Integer, db.ForeignKey('dorm.id'), nullable=False)
    
    def __init__(self, text, dorm_id):
        self.text = text
        self.dorm_id = dorm_id

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=60)])
    password = StringField("Username", validators=[DataRequired(), Length(min=2, max=60)])
    submit = SubmitField('Signup')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash('"That username already exists"')
            raise ValidationError("That username already exists")
            

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=60)])
    password = StringField("Username", validators=[DataRequired(), Length(min=2, max=60)])
    submit = SubmitField('Login')


@app.route("/")
def index():
    return render_template("index.html", dorms=dorms)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template("register.html", form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else: 
                flash('Incorrect username or password. Please try again.', 'info')
            
    return render_template("login.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route("/dorm/<int:dormid>", methods=['GET', 'POST'])
# def dorm(dormid):
#     dorm = Dorm.query.get(dormid)
#     if not dorm:
#         flash("Dorm not found", "error")
#         return redirect(url_for('index'))
#     return render_template("dorm.html", dorm=dorm)



if (__name__) == "__main__":
    app.run(debug=True)