from hostessapp import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import current_user
from hostessapp.models import db, Sister, Pnm, Comment, Meta, BumpToPnm, BumpGroup
from flask import flash, redirect, url_for, session, render_template, request
from hostessapp.login import login_user, login_required, current_user, logout_user	


current_pnms = []
num_parties = {1:6, 2:4, 3:3}

@app.route('/', methods=['GET','POST'])
@login_required
def index():

	if "night" not in session:
		session["night"] = Meta.query.first().night
	
	if request.method == 'POST':
		night = int(request.form["night"])
		Meta.query.first().night = night
		db.session.commit()
		session["night"] = Meta.query.first().night

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

    if 'remember' in request.form:
        remember_me = True

    if registered_user is None or not (password == 'redcarnation'):
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    session["username"] = str(current_user)
    flash('Logged in successfully')
    if registered_user.is_crib:
    	session["admin"] = True

    return redirect(request.args.get('next') or url_for('index'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('admin', None)
    flash('Logged out successfully')
    return redirect(url_for('index'))

@app.route('/pnm/<id>')
@login_required
def show_pnm_profile(id):

	return render_template('profile.html', pnm=Pnm.query.get(id))

@app.route('/allpnms')
@login_required
def get_all_pnms():
	Pnm.query.all()
	return render_template('allpnms.html', pnms=Pnm.query.all())

@app.route('/pnmform/<party>', methods=['GET', 'POST'])
@login_required
def pnm_form(party):
	global current_pnms
	if request.method == 'POST':
			
		ans = request.form

		print ans.items()

		pnm = Pnm.query.filter_by(name=ans["name"]).first()

		sis = current_user.username

		c = Comment(ans["comments"], ans["sisters"], pnm.id, current_user.id, sis)

		# Add to sisters comments

		pnm.interests = pnm.interests+", "+ans["interests"]

		db.session.add(c)
		db.session.commit()

	all_pnms = filter(lambda x:x not in current_pnms, Pnm.query.all())

	pnms = current_pnms + all_pnms
	if "night" in session:
		last_round = (int(party) == num_parties[session["night"]])
	else:
		last_round = (int(party) == num_parties[Meta.query.first().night])

	return render_template('pnmform.html', party=int(party), pnms=pnms, last_party=last_round)

@app.route('/mypnms/<party>')
@login_required
def my_pnms(party):
	global current_pnms
	if "night" not in session:
		session["night"] = Meta.query.first().night

	night = session["night"]

	night = 1
	bg = current_user.bump_group

	if night==0:
		return render_template("mypnms.html", notfmr = True)

	else:
		party = int(party)

		pnms = []

		for x in bg.pnms:
			if x.party == party and x.night==night:
				p = x.pnm
				pnms.append(x.pnm)

		current_pnms = pnms

		return render_template("mypnms.html", notfmr = False, pnms=pnms, party=party)

@app.route('/assignpnms', methods=['GET', 'POST'])
@login_required
def assign_pnms():

	bumps = [x.name for x in BumpGroup.query.all()]

	if "night" in request.form:
		night = int(request.form["night"])
		session["assign_night"] = night

	elif "assign_night" not in session:
		night = 1

	else:
		night = session["assign_night"]

	parties = range(1,num_parties[night]+1)

	if request.method == 'GET' or "night" in request.form:
		pnms = Pnm.query.all()
		assigns = []
		for p in pnms:
			match = BumpToPnm.query.filter_by(pnm_id=p.id).filter_by(night=night).first()
			if not match:
				assigns+=[[p.name, 0, "A"]]
			else:
				assigns+=[[p.name, match.party, match.bump_group.name]]

		return render_template("assignpnms.html", pnms=assigns, bumps=bumps, parties=parties)
	
	val_dict = {}

	for k in request.form:
		pnm, v = k.split("+")

		if pnm not in val_dict:
			val_dict[pnm] = {}
		val_dict[pnm][v] = request.form[k]

	print val_dict.items()

	for p in val_dict:

		party = int(val_dict[p]["party"])

		bg = val_dict[p]["bump"]

		pnm = Pnm.query.filter_by(name=p).first()
		bump = BumpGroup.query.filter_by(name=bg).first()

		if party == 0:
			print p

			b = BumpToPnm.query.filter_by(pnm_id=pnm.id).filter_by(bump_id=bump.id).filter_by(night=night).first()
			if b:
				db.session.delete(b)
		else:
			b = BumpToPnm.query.filter_by(pnm_id=pnm.id).filter_by(bump_id=bump.id).filter_by(night=night).first()
			if not b:
				b = BumpToPnm(night, party)
			
			b.pnm = pnm
			b.party = party

			bump.pnms.append(b)

			db.session.add(b)

	db.session.commit()

	pnms = Pnm.query.all()
	assigns = []
	for p in pnms:
		match = BumpToPnm.query.filter_by(pnm_id=p.id).filter_by(night=night).first()

		if not match:
			assigns+=[[p.name, 0, "A"]]
		else:
			assigns+=[[p.name, match.party, match.bump_group.name]]

	return render_template("assignpnms.html", pnms=assigns, bumps=bumps, parties=parties)
