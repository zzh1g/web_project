import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user

user_name = ''
user_school = ''
user_email = ''
a = ''
ph = [10, 20, 30, 40]
ph2 = []
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///client.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
articles = [("dsadsadsadsad", "jjjjjjjjjjjjj"), ("klkklkljklj", "nmnmnnm")]
login = LoginManager(app)
app.secret_key = "mjdfkjQWS###@$dsfY12345UgYUGgK23143214523"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    mail = db.Column(db.Text, unique=True, nullable=False)
    psw = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, unique=True, nullable=False)
    scool = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    old = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Users {self.id}>'


db.create_all()


class UserLogin():
    def fromDB(self, user_id, dab):
        print(dab.session.query(Users).all())
        self.__user = dab.session.query(Users).all()
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])


@app.route('/register', methods=("POST", "GET"))
def register():
    if request.method == "POST":
        print("ok")
        try:
            shash = generate_password_hash(request.form["psw"])
            print(shash)
            u = Users(mail=request.form['mail'], psw=shash, name=request.form['name'], old=int(request.form['old']),
                      scool=request.form['scool'], score=0)
            print(type(shash))
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
    return render_template("register.html", title="Регистрация")


@login.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)


def getUserByEmail(e):
    res = Users.query.filter_by(mail=e).all()
    return res


@app.route("/login", methods=["POST", "GET"])
def login():
    global a
    if request.method == "POST":
        global user_email
        user = getUserByEmail(request.form['email'])
        user_email = request.form['email']
        if user[0] and check_password_hash(user[0].psw, request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            a = 1
            return redirect(url_for("ma"))


    return render_template("login.html", title="Авторизация")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if a:
        global user_name, user_school
        con = sqlite3.connect('instance/client.db')
        cur = con.cursor()
        user_name = ((cur.execute("SELECT name FROM users WHERE mail = ?", (user_email,)).fetchall())[0])[0]
        user_school = ((cur.execute("SELECT scool FROM users WHERE mail = ?", (user_email,)).fetchall())[0])[0]
    return render_template("profile.html", title="Мой кабинет", name=user_name, school=user_school, email=user_email)


@app.route('/')
def ma():
    return render_template("main.html", title="Пользователи")


if __name__ == "__main__":
    app.run(debug=True)
