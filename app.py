from flask import Flask, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user, login_user, logout_user
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime
import hashlib
import models
import forms

load_dotenv()
env = dotenv_values()

app = Flask(__name__)

app.config['SECRET_KEY'] = env['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + env['DB_NAME']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
models.db.init_app(app)

with app.app_context():
    models.db.create_all()

models.login.init_app(app)
models.login.login_view = 'login'

# global vaiablies
the_year = date.today().year
logged_in = False


@app.route('/')
@models.login_required
def index():
    with app.app_context():
        user = models.User.query.all()
        utilities = models.Utility.query.all()
        return render_template('index.html', the_year=the_year, utils=utilities)


@app.route('/view/<int:id>', methods=['POST', 'GET'])
def view(id):
    with app.app_context():
        util = models.db.get_or_404(models.Utility, id)
        return render_template('view.html', the_year=the_year, form_data=util)


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    with app.app_context():
        form = forms.Utils()
        utils = models.db.get_or_404(models.Utility, id)
        if request.method == 'POST':
            utils.util_name = request.form['util_name']
            utils.util_site = request.form['util_site']
            utils.util_acct = request.form['util_acct']
            utils.util_main = request.form['util_main']
            utils.util_alt = request.form['util_alt']
            utils.util_hours = request.form['util_hours']
            utils.util_amt = request.form['util_amt']
            utils.util_bdate = request.form['util_bdate']
            utils.util_ddate = request.form['util_ddate']
            if request.form['util_autopay'] == 'y':
                utils.util_autopay = True
            else:
                utils.util_autopay = False
            models.db.session.commit()
            return redirect(url_for('index'))
        else:
            form.process(formdata=None, obj=utils)
            return render_template('edit.html', the_year=the_year, form_data=form)


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = forms.Utils()
    utils = models.Utility()
    with app.app_context():
        if request.method == 'POST':
            utils.util_name = request.form['util_name']
            utils.util_site = request.form['util_site']
            utils.util_acct = request.form['util_acct']
            utils.util_main = request.form['util_main']
            utils.util_alt = request.form['util_alt']
            utils.util_hours = request.form['util_hours']
            utils.util_amt = request.form['util_amt']
            utils.util_bdate = request.form['util_bdate']
            utils.util_ddate = request.form['util_ddate']
            if request.form['util_autopay'] == 'y':
                utils.util_autopay = True
            else:
                utils.util_autopay = False
            models.db.session.add(utils)
            models.db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('add.html', the_year=the_year, form_data=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        user = models.User.query.filter_by(user_email=email).first()
        print(user.user_name, user.user_pass, request.form['password'])
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html', login_form=form)


@app.route('/logout')
def logout():
    models.logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
