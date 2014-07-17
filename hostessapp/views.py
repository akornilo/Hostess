from hostessapp import app
from flask.ext.sqlalchemy import SQLAlchemy
from hostessapp.models import db, Sister, PNM
from flask import flash, redirect, url_for, session, render_template, request
from hostessapp.login import login_user, login_required, current_user, logout_user	

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/settings")
@login_required
def settings():
    return "ponies"


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = Sister.query.filter_by(username=username).first()

    remember_me = False

    print request.form.items()

    if 'remember' in request.form:
        remember_me = True

    if registered_user is None or not (password == 'redcarnation'):
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    session["username"] = str(current_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    flash('Logged out successfully')
    return redirect(url_for('index'))

@app.route('/pnm/<id>')
def show_pnm_profile(id):
	return render_template('profile.html', pnm=PNM.query.get(id))

@app.route('/allpnms')
def get_all_pnms():
	return render_template('allpnms.html', pnms=PNM.query.all())

@app.route('/pnmform', methods=['GET', 'POST'])
def pnm_form():
	if request.method == 'GET':
		return render_template('pnmform.html')

	print request.form.items()

	return redirect(url_for('index'))