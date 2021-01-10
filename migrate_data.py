import json
import data.data_provider as data_provider
from app import Teacher
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tiny_step.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

profiles = data_provider.get_profiles()
for profile in profiles:
    teacher = Teacher(id=profile['id'],
                      name=profile['name'],
                      about=profile['about'],
                      rating=float(profile['rating']),
                      picture=profile['picture'],
                      price=profile['price'],
                      goals=' '.join(profile['goals']),
                      free=str(json.dumps(profile['free']))
                      )
    db.session.add(teacher)
db.session.commit()
