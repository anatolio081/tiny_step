import random
import json
import os
import data.data_provider as data_provider
from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tiny_step.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.String, nullable=False)
    free = db.Column(db.String, nullable=False)


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_time = db.Column(db.String(5), nullable=False)
    client_phone = db.Column(db.String(15), nullable=False)
    goal = db.Column(db.String, nullable=False)


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(15), nullable=False)
    week_day = db.Column(db.String(4), nullable=False)
    time = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")


@app.route('/')
def render_main():
    teacher_profiles = db.session.query(Teacher).filter().limit(6).all()
    for profile in teacher_profiles:
        profile.free = json.loads(profile.free)
        profile.goals = profile.goals.split()
    goals = data_provider.get_goals()
    random.shuffle(teacher_profiles)
    return render_template('index.html',
                           profiles=teacher_profiles,
                           goals=goals)


@app.route('/all/', methods=["POST", "GET"])
def render_all_profiles():
    teacher_profiles = db.session.query(Teacher).all()
    for profile in teacher_profiles:
        profile.free = json.loads(profile.free)
        profile.goals = profile.goals.split()
    if request.method == 'POST':
        sort = int(request.form["sort"])
        return render_template('all.html', profiles=teacher_profiles, sort=sort)
    else:
        return render_template('all.html', profiles=teacher_profiles, sort=1)


@app.route('/goals/<goal>/')
def render_goal(goal):
    teacher_profiles = db.session.query(Teacher).filter(Teacher.goals.contains(goal)).all()
    for profile in teacher_profiles:
        profile.free = json.loads(profile.free)
        profile.goals = profile.goals.split()
    goals = data_provider.get_goals()
    return render_template('goal.html',
                           goal=goal,
                           goals=goals,
                           profiles=teacher_profiles)


@app.route('/profiles/<int:id>/')
def render_profile(id):
    teacher_profile = db.session.query(Teacher).get(id)
    if teacher_profile is not None:
        goals = data_provider.get_goals()
        teacher_profile.free = json.loads(teacher_profile.free)
        teacher_profile.goals = teacher_profile.goals.split()
        return render_template('profile.html',
                               profile=teacher_profile,
                               goals=goals)
    else:
        error_data = "Преподаватель отсутствует в БД"
        return render_template("404.html", error=error_data), 404


@app.route('/request/')
def render_request():
    goals = data_provider.get_goals()
    return render_template('request.html', goals=goals)


@app.route('/request_done/', methods=["POST"])
def render_request_done():
    goals = data_provider.get_goals()
    client_name = request.form["clientName"]
    client_phone = request.form["clientPhone"]
    client_time = request.form["time"]
    goal = request.form["goal"]
    booking_request = Request(client_name=client_name,
                              client_time=client_time,
                              client_phone=client_phone,
                              goal=goal)
    db.session.add(booking_request)
    db.session.commit()
    return render_template('request_done.html',
                           goal=goal,
                           goals=goals,
                           client_name=client_name,
                           client_time=client_time,
                           client_phone=client_phone)


@app.route('/booking/<int:id_teacher>/<day>/<time>/')
def render_booking_form(id_teacher, day, time):
    teacher_profile = db.session.query(Teacher).get(id_teacher)
    teacher_profile.free = json.loads(teacher_profile.free)
    teacher_profile.goals = teacher_profile.goals.split()
    return render_template('booking.html',
                           profile=teacher_profile,
                           day=day,
                           time=time)


@app.route('/booking_done/', methods=["POST"])
def render_booking_done():
    client_name = request.form["clientName"]
    client_phone = request.form["clientPhone"]
    week_day = request.form["clientWeekday"]
    client_time = request.form["clientTime"]
    client_teacher_id = request.form["clientTeacher"]
    booking_data = Booking(client_name=client_name,
                           client_phone=client_phone,
                           week_day=week_day,
                           time=client_time,
                           teacher_id=client_teacher_id)
    db.session.add(booking_data)
    db.session.commit()
    return render_template('booking_done.html',
                           client_name=client_name,
                           day=week_day,
                           time=client_time,
                           phone=client_phone)


@app.errorhandler(404)
def render_not_found(error):
    return render_template("404.html", error=error), 404


@app.errorhandler(404)
def server_error(error):
    return render_template("500.html", error=error), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
