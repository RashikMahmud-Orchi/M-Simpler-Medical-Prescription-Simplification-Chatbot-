from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
import io
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'xyzsdfg'
app.config['UPLOAD_FOLDER'] = './uploaded_images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://orchi:r9ybSlSOVM5ADl968LrKdBS6p8cftbdx@dpg-cnsjdk8l5elc73fkuo5g-a/user_e3f9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Google API key
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to load OpenAI model and get responses
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Function to save user credentials to the database
def save_user_credentials_to_db(email, password):
    hashed_password = generate_password_hash(password)
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session:
        
        if request.method == 'POST':
            
            if'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            input_prompt = request.form['input_prompt']
            
            # If the user does not select a file, the browser submits an empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Process the image and get response
                image = Image.open(file_path)
                response = get_gemini_response(input_prompt, image)
                
                image_url = url_for('static', filename=filename)
                
                # Pass the response and image URL to the template
                return render_template('index.html', response=response, image_url=image_url)

        # Initial page load or no file uploaded
        return render_template('index.html')
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    app.secret_key = 'xyzsdfg'
    message = request.args.get('message')
    success_message = request.args.get('success_message')  # Retrieve success message from query parameters
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        # For demonstration purposes, checking credentials by querying the database
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['loggedin'] = True
            session['email'] = email
            message = "Logged in successfully!"
            return redirect(url_for('index')) 

        message = "Please enter correct email / password!"

    return render_template('login.html', message=message, success_message=success_message)  # Pass success_message to login template


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        agree = request.form.get('agree')

        # Checking if any form field is empty and if agree checkbox is checked
        if not (name and email and password and agree == 'on'):  # Ensure agree checkbox is checked
            message = 'Please fill in all the fields and agree to the terms and conditions.'
        else:
            # Checking if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                message = 'User already exists. Please login instead.'
            else:
                # Register user
                save_user_credentials_to_db(email, password)
               
                return redirect(url_for('login', success_message='You have successfully registered!'))

    return render_template('register.html', message=message)
if __name__ == "__main__":
    login()
    app.run(debug=True,host="0.0.0.0",port=8000)