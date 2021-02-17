from flask import render_template, url_for, flash, redirect, request, jsonify
from mentor import app, db, bcrypt
from mentor.forms import RegistrationForm, LoginForm,RegistrationFormMentor
from mentor.models import User, Usermentor,Jobfield,Jobtitle
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
       status=current_user.status

       return render_template('home.html',status=status)


    else:
        return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    form.jobfield.choices =[(job.id,job.name)for job in Jobfield.query.order_by(Jobfield.name)]
    form.jobtitle.choices = [(title.id, title.name) for title in Jobtitle.query.filter_by(jobfield_id=1).all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        jfname=Jobfield.query.filter_by(id=form.jobfield.data).first()
        jf1=jfname.name
        jtname=Jobtitle.query.filter_by(id=form.jobtitle.data).first()
        jt1=jtname.name
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password,desiredfield=jf1,job=jt1,status='Mentee')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/register-mentor", methods=['GET', 'POST'])
def registermentor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationFormMentor()
    form.jobfield.choices = [(job.id, job.name) for job in Jobfield.query.order_by(Jobfield.name)]
    form.jobtitle.choices = [(title.id, title.name) for title in Jobtitle.query.filter_by(jobfield_id=1).all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        jfname = Jobfield.query.filter_by(id=form.jobfield.data).first()
        jf1 = jfname.name
        jtname = Jobtitle.query.filter_by(id=form.jobtitle.data).first()
        jt1 = jtname.name

        user = Usermentor(username=form.username.data, email=form.email.data,
                          password=hashed_password,field=jf1,job=jt1,status='Mentor',
                          experience=form.experience.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registermentor.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.stat.data == 'Mentee':
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            user = Usermentor.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/jobtitle/<jfield>", methods=['GET', 'POST'])
def jobtitle(jfield):
    jobtitles=Jobtitle.query.filter_by(jobfield_id=jfield).all()
    titlearray=[]
    for title in jobtitles:
        titleObj={}
        titleObj['id'] = title.id
        titleObj['name'] = title.name
        titlearray.append(titleObj)
    return jsonify({'jobtitles': titlearray})

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
