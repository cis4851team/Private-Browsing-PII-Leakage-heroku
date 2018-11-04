from flask import Flask, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'CIS 4851'
heroku = Heroku(app)
db = SQLAlchemy(app)


@app.route('/', methods=["POST", "GET"])
def pii():
    if request.method == "POST":
        fn = request.form['first_name']
        ln = request.form['last_name']
        ad = request.form['address']
        em = request.form['email']
        b = request.form['dob']

        user = FormData(fn, ln, ad, em, b)
        log_user = user.__dict__.copy()
        del log_user["_sa_instance_state"]

        try:
            db.session.add(user)
            db.session.commit()
            session['first_name'] = ""
            session['last_name'] = ""
            session['address'] = ""
            session['email'] = ""
            session['dob'] = ""
        except Exception as e:
            print("\n FAILED entry: {}\n".format(json.dumps(log_user)))
            print(e)
            sys.stdout.flush()
            session['first_name'] = fn
            session['last_name'] = ln
            session['address'] = ad
            session['email'] = em
            session['dob'] = b
    return 'PII submitted! To enter more data, <a href="{}">click here!</a>'.format(url_for('return_to_index'))


@app.route('/')
def return_to_index():
    first_name = session['first_name'] if 'first_name' in session else ""
    last_name = session['last_name'] if 'last_name' in session else ""
    address = session['address'] if 'address' in session else ""
    email = session['email'] if 'email' in session else ""
    dob = session['dob'] if 'dob' in session else ""

    return render_template(
        'index.html', first_name=first_name, last_name=last_name,
        address=address, email=email,
        dob=dob)


class FormData(db.Model):
    __tablename__ = "form_data"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text())
    last_name = db.Column(db.Text())
    address = db.Column(db.Text())
    email = db.Column(db.Text())
    dob = db.Column(db.Text())


    def __init__(self, first_name, last_name, address, email, dob):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.dob = dob


if __name__ == '__main__':
    app.debug = True
    app.run()
