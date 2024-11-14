from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.database import Users

app = Flask(__name__)

app.secret_key = "1111"
user_db = "katya"
host_ip = "localhost"
host_port = "5432"
database_name = "lab5_rpp"
password = "34567"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'goforaccount'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
@login_required
def main():
    return render_template('main.html', name=current_user.name)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "GET":
        return render_template("registration.html")

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        name = request.form['name']

        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return render_template('registration.html', error="Такой акаунт существует")

        new_user = Users(email=email, password_hash=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/goforaccount')


@app.route('/goforaccount', methods=['GET', 'POST'])
def goforaccount():
    if request.method == 'GET':
        return render_template('goforaccount.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        if not user:
            return render_template('goforaccount.html', error="Пользователь от этого аккаунта не найден")

        if not check_password_hash(user.password_hash, password):
            return render_template('goforaccount.html', error="Неправильный пароль от акаунта")

        login_user(user)
        return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/goforaccount')


if __name__ == '__main__':
    app.run()