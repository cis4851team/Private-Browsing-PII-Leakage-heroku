from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = 'CIS 4851'

@app.route('/', methods=["POST", "GET"]) 
def pii():
    if request.method == "POST":
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['address'] = request.form['address']
        session['email'] = request.form['email']
        session['dob'] = request.form['dob']
        return render_template(
            'index.html', first_name=session["first_name"], last_name=session["last_name"], 
            address=session["address"], email=session["email"], 
            dob=session["dob"])
    else:
        first_name = session['first_name'] if 'first_name' in session else ""
        last_name = session['last_name'] if 'last_name' in session else ""
        address = session['address'] if 'address' in session else ""
        email = session['email'] if 'email' in session else ""
        dob = session['dob'] if 'dob' in session else ""
        return render_template(
            'index.html', first_name=first_name, last_name=last_name, address=address,
            email=email, dob=dob)
