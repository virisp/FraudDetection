from flask import Flask, render_template, url_for, redirect, request, jsonify
import pyrebase
import pickle
import pandas as pd

app = Flask(__name__)

loaded_model = pickle.load(open('logistic_model.sav', 'rb'))

firebase = pyrebase.initialize_app('CONFIG_DATABASE')

auth = firebase.auth()

@app.route('/', methods = ['GET', 'POST'])
def index():

    unsuccessful = 'Please check your credentials'
    successful = 'Login Successful'

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('logout.html', s = successful)
        except:
            return render_template('login.html', us = unsuccessful)

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    register_successful = 'Sign in!'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('index'))
    return render_template('register.html', register_successful = register_successful)

@app.route('/verify', methods = ['POST'])
def predict ():
    transaction = pd.DataFrame(request.get_json(),index = [0])
    prediction = str(loaded_model.predict(transaction))
    result ={'prediction':prediction}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug = True)
