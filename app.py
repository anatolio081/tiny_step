from flask import Flask, render_template, request
from data.data_provider import DataProvider
import random

app = Flask(__name__)


@app.route('/')
def render_main():
    profiles = DataProvider.get_profiles()
    goals = DataProvider.get_goals()
    random.shuffle(profiles)
    return render_template('index.html',
                           profiles=profiles,
                           goals=goals)


@app.route('/all/', methods=["POST", "GET"])
def render_all_profiles():
    profiles = DataProvider.get_profiles()
    random.shuffle(profiles)
    if request.method == 'POST':
        sort = int(request.form["sort"])
        return render_template('all.html', profiles=profiles, sort=sort)
    else:
        return render_template('all.html', profiles=profiles, sort=1)


@app.route('/goals/<goal>/')
def render_goal(goal):
    profiles = DataProvider.get_profiles()
    goals = DataProvider.get_goals()
    return render_template('goal.html',
                           goal=goal,
                           goals=goals,
                           profiles=profiles)


@app.route('/profiles/<int:id>/')
def render_profile(id):
    profiles = DataProvider.get_profiles()
    goals = DataProvider.get_goals()
    return render_template('profile.html',
                           profile=profiles[id],
                           goals=goals)


@app.route('/request/')
def render_request():
    goals = DataProvider.get_goals()
    return render_template('request.html', goals=goals)


@app.route('/request_done/', methods=["POST"])
def render_request_done():
    goals = DataProvider.get_goals()
    client_name = request.form["clientName"]
    client_phone = request.form["clientPhone"]
    client_time = request.form["time"]
    goal = request.form["goal"]
    DataProvider.add_request(client_name, client_phone, client_time, goal)
    return render_template('request_done.html',
                           goal=goal,
                           goals=goals,
                           client_name=client_name,
                           client_time=client_time,
                           client_phone=client_phone)


@app.route('/booking/<int:id_teacher>/<day>/<time>/')
def render_booking_form(id_teacher, day, time):
    profiles = DataProvider.get_profiles()
    return render_template('booking.html',
                           profile=profiles[id_teacher],
                           day=day,
                           time=time)


@app.route('/booking_done/', methods=["POST"])
def render_booking_done():
    client_name = request.form["clientName"]
    client_phone = request.form["clientPhone"]
    week_day = request.form["clientWeekday"]
    client_time = request.form["clientTime"]
    client_teacher = request.form["clientTeacher"]
    DataProvider.add_order(client_name, client_phone, week_day, client_time, client_teacher)
    return render_template('booking_done.html',
                           client_name=client_name,
                           day=week_day,
                           time=client_time,
                           phone=client_phone)


@app.errorhandler(404)
def render_not_found(error):
    return render_template("404.html").format(error), 404


@app.errorhandler(404)
def server_error(error):
    return render_template("500.html").format(error), 500


if __name__ == '__main__':
    app.run()
