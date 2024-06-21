from flask import Flask, render_template, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from datetime import datetime

now = datetime.now()

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://udt3danp6j3fro:p52f53a3f6f1e1da0f620f72b2eb360779df73592d408757bcb76edadd1f1d27d@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d31tirbif2rglf"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "hdjasodjsoaidjsaida"
dorms = [
    {
        "name": "17TH-AVENUE",
        "description": "Built in 2013, the 17th Avenue residence hall has six floors with space for 600 first-year residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/17th%20Ave-University%20ave%20corner.jpg",
        "avgreview": int,
    },
    {
        "name": "BAILEY",
        "description": "Built in 1949, with additions in 1981, Bailey has five floors with space for 500 residents, its own dining hall, and is connected via tunnel to the St. Paul Student Center.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/2021-08/BaileyHall_Sign2%203000%20x%201400.jpg?h=c2125e9a&itok=IXGziMiz",
        "avgreview": int,
    },
    {
        "name": "CENTENNIAL",
        "description": "Built in 1950, Centennial Hall has six floors with 700 first-year and returning residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/imported/CentennialExterior-HallExterior.jpg?h=a7534cac&itok=qp9dF_D1",
        "avgreview": int,
    },
    {
        "name": "COMSTOCK",
        "description": "Built in 1940, Comstock Hall has six floors of rooms for 553 first-year residents and its own dining hall.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/2021-03/Comstock.jpg?h=6cad0671&itok=YR43Z0DN",
        "avgreview": int,
    },
    {
        "name": "FRONTIER",
        "description": "Built in 1959, Frontier Hall has four floors with 735 first-year and returning residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/Frontier.jpg",
        "avgreview": int,
    },
    {
        "name": "MIDDLEBROOK",
        "description": "Built in 1969 (tower) and 2001 (east wing), Middlebrook houses over 900 students, including the Honors Living Learning Community, along with its own dining hall and market.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/Middlebrook_ext_bridge.jpg",
        "avgreview": int,
    },
    {
        "name": "PIONEER",
        "description": "Renovated in 2019, Pioneer Hall has five floors with its own dining hall and 756 first-year and returning residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/imported/PioneerExterior-HallExterior.jpg",
        "avgreview": int,
    },
    {
        "name": "SANFORD",
        "description": "Built in 1910 and renovated in 1970, Sanford has its own dining hall and space for 530 first-year residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/imported/SanfordExterior-HallExterior.jpg?h=9d0cf94b&itok=kWhUliof",
        "avgreview": int,
    },
    {
        "name": "TERRITORIAL",
        "description": "Built in 1958 and expanded in 1999, Territorial Hall has four floors with 695 first-year residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/styles/896x566/public/imported/TerritorialExteriorEntrance-HallExterior.jpg?h=9d0cf94b&itok=jutKY1gI",
        "avgreview": int,
    },
    {
        "name": "YUDOF",
        "description": "Built in 2002, Yudof has six floors of apartments with 507 first-year and returning residents.",
        "image_url": "https://housing.umn.edu/sites/housing.umn.edu/files/2021-03/Yudof.jpg",
        "avgreview": int,
    },
]
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    dorm = db.Column(db.String(255), nullable=False)
    review = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=60)],
        render_kw={"placeholder": "Username"},
    )
    password = StringField(
        "Password",
        validators=[DataRequired(), Length(min=2, max=60)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Signup")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=80)],
        render_kw={"placeholder": "Username"},
    )
    password = StringField(
        "Password",
        validators=[DataRequired(), Length(min=2, max=80)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")


class PostForm(FlaskForm):
    content = TextAreaField(
        "Username",
        validators=[DataRequired(), Length(min=15, max=3000)],
        render_kw={"placeholder": "Your Review"},
    )
    review = SelectField(
        "Review", choices=[(str(i), str(i)) for i in range(1, 6)], coerce=int
    )
    submit = SubmitField("Post Review")


@app.route("/", methods=["GET", "POST"])
def index():
    dorm_reviews = (
        db.session.query(
            Post.dorm,
            func.count(Post.review).label("post_count"),
            func.round(func.avg(Post.review), 1).label("avg_review"),
        )
        .group_by(Post.dorm)
        .all()
    )
    dorm_data = {}
    for dorm, post_count, avg_review in dorm_reviews:
        dorm_data[dorm] = {"post_count": post_count, "avg_review": avg_review}

    title = "RateMyUMNDorm - Home"
    return render_template(
        "index.html",
        dorms=dorms,
        dorm_data=dorm_data,
        title=title,
        dorm_reviews=dorm_reviews,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user_username = User.query.filter_by(
            username=form.username.data
        ).first()
        if existing_user_username:
            flash('"That username already exists"')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            hashed_password = hashed_password.decode("utf-8", "ignore")
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("index"))
    title = "RateMyUMNDorm - Register"
    return render_template("register.html", form=form, title=title)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Incorrect username or password. Please try again.", "info")
    title = "RateMyUMNDorm - Login"
    return render_template("login.html", form=form, title=title)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dorm/<dorm_name>", methods=["GET", "POST"])
def dorm(dorm_name):
    dorm_reviews = (
        db.session.query(
            Post.dorm, func.round(func.avg(Post.review), 1).label("avg_review")
        )
        .group_by(Post.dorm)
        .all()
    )
    dorm_avg_reviews = {dorm: avg_review for dorm, avg_review in dorm_reviews}

    dorm = None
    for dorm_info in dorms:
        if dorm_info["name"] == dorm_name:
            posts = Post.query.filter_by(dorm=dorm_name).all()
            posts.reverse()
            post_count = len(posts)
            dorm = dorm_info
            break
    title = f"RateMyUMNDorm - {dorm_name}"
    return render_template(
        "dorm.html",
        dorm=dorm,
        posts=posts,
        dorm_avg_reviews=dorm_avg_reviews,
        title=title,
        post_count=post_count,
    )


@app.route("/dorm/<dorm_name>/create_post", methods=["GET", "POST"])
@login_required
def create_post(dorm_name):
    dorm = None
    for dorm_info in dorms:
        if dorm_info["name"] == dorm_name:
            dorm = dorm_info
            break
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            dorm=dorm_name,
            content=form.content.data,
            review=form.review.data,
            likes=0,
            date_posted=datetime.utcnow(),
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("dorm", dorm_name=dorm_name))
    title = f"RateMyUMNDorm - Create Review for {dorm_name}"
    return render_template("create_post.html", dorm=dorm, form=form, title=title)


if (__name__) == "__main__":
    app.run(debug=True)
