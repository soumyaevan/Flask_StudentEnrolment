from application import app, db, api
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import User, Course, Enrolment
from application.forms import LoginForm, RegistrationForm
from flask_restplus import Resource
from application.course_list import course_list
list_of_course = [{"courseID": "1111", "title": "PHP 101", "description": "Intro to PHP", "credits": 3, "term": "Fall, Spring"},
                  {"courseID": "2222", "title": "Java 1",
                      "description": "Intro to Java Programming", "credits": 4, "term": "Spring"},
                  {"courseID": "3333", "title": "Adv PHP 201",
                      "description": "Advanced PHP Programming", "credits": 3, "term": "Fall"},
                  {"courseID": "4444", "title": "Angular 1",
                   "description": "Intro to Angular", "credits": 3, "term": "Fall, Spring"},
                  {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": 4, "term": "Fall"}]

##############################################

@api.route('/api','/api/')
class GetAndPost(Resource):
   def get(self):
      return jsonify(User.objects.all())

   def post(self):
      data = api.payload
      user = User(user_id=data['user_id'], email=data['email'],
                  first_name=data['first_name'], last_name=data['last_name'])
      user.set_password(data['password'])
      user.save()
      return jsonify(User.objects(user_id=data['user_id']))

   
@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
   def get(self,idx):
      return jsonify(User.objects(user_id=idx))

   def put(self, idx):
      data = api.payload
      User.objects(user_id=idx).update(**data)
      return jsonify(User.objects(user_id=data['user_id']))

   def delete(self,idx):
      User.objects(user_id=idx).delete()
      return jsonify('User is deleted')



##############################################

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html", title="Home", index=True)


@app.route('/courses/')
@app.route('/courses/<terms>')
def courses(term=None):
    if term is None:
        term = "Spring 2020"
    classes = Course.objects.order_by("+courseID")

    return render_template("courses.html", course_list=classes, title="Courses", courses=True, term=term)


@app.route('/register', methods=['GET', 'POST'])
def register():
   if session.get('username'):
      return redirect(url_for('index'))
   form = RegistrationForm()
   if form.validate_on_submit():
      user_id = User.objects.count()
      user_id += 1
      email = form.email.data
      password = form.password.data
      first_name = form.first_name.data
      last_name = form.last_name.data

      user = User(user_id=user_id, email=email,
                  first_name=first_name, last_name=last_name)
      user.set_password(password)
      user.save()
      flash('You have successfully registered', 'success')
      return redirect(url_for('login'))
   return render_template("register.html", register=True, title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
   if session.get('username'):
      return redirect(url_for('index'))
   form = LoginForm()
   if form.validate_on_submit():
      email = form.email.data
      password = form.password.data
      user = User.objects(email=email).first()
      if user and user.get_password(password):
         flash(f'{user.first_name}, You have successfully logged in', 'success')
         session['user_id'] = user.user_id
         session['username'] = user.first_name
         return redirect(url_for('index'))
      else:
         flash('Sorry, your credential is not correct. Try again', 'danger')
   return render_template("login.html", title="Login", form=form, login=True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session['user_id']=False
   session.pop('username',None)
   return redirect(url_for('index'))

@app.route('/enrolment', methods=['GET', 'POST'])
def enrolment():
   if not session.get('username'):
      flash('You have to login first','warning')
      return redirect(url_for('login'))
   courseID = request.form.get('course_id')
   courseTitle = request.form.get('title')
   user_id = session.get('user_id')

   if courseID:
      if Enrolment.objects(user_id=user_id, courseID=courseID):
         flash(
               f"Oops! You have already enrolled in {courseTitle}", "danger")
         return redirect(url_for('courses'))
      else:
         Enrolment(user_id=user_id, courseID=courseID).save()
         flash(
               f"You have successfully enrolled in {courseTitle}", "success")
   classes = course_list(user_id)
   
   return render_template("enrolment.html", title="Enrolment", enrolment=True, classes=classes)


# @app.route('/api/courseid/')
# @app.route('/api/courseid/<idx>')
# def api(idx=None):
#     jsonData = None
#     if not (idx):
#         jsonData = list_of_course
#     else:
#         for item in list_of_course:
#             if item['courseID'] == idx:
#                 jsonData = item
#                 break
#     return Response(json.dumps(jsonData), mimetype="application/json")


@app.route("/user")
def user():
    # User(user_id=1, first_name="Soumya", last_name="Sen", email="soumya.sen@sta.com", password="12345").save()
    # User(user_id=2, first_name="Arup", last_name="Biswas", email="arup.biswas@sta.com", password="98765").save()
    users = User.objects.all()
    return render_template("user.html", title="User List", users=users)
