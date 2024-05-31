

# from flask import Flask, render_template, url_for, request, redirect
# import hashlib
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from functools import wraps

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '12345'
# # Define multiple binds for your databases
# app.config['SQLALCHEMY_BINDS'] = {
#     'user_db': 'sqlite:///C:/blood line/website/instance/User.db',
#     'donor_db': 'sqlite:///C:/blood line/website/instance/Donor.db',
#     'patient_db': 'sqlite:///C:/blood line/website/instance/Patient.db'
# }
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# # app = Flask(__name__)
# # app.secret_key = 'your_secret_key'

# # # Configure the SQLAlchemy part of the app instance
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# # Create the SQLAlchemy db instance
# db = SQLAlchemy(app)

# # Mock admin credentials
# ADMIN_EMAIL = 'admin@example.com'
# ADMIN_PASSWORD = 'adminpassword'

# # Admin login route
# @app.route('/admin/login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
#             session['admin_logged_in'] = True
#             return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Invalid credentials. Please try again.')
#             return redirect(url_for('admin_login'))
#     return render_template('admin_login.html')

# # Admin logout route
# @app.route('/admin/logout')
# def admin_logout():
#     session.pop('admin_logged_in', None)
#     return redirect(url_for('admin_login'))

# # Admin only decorator
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'admin_logged_in' not in session:
#             flash('You need to be an admin to view this page.')
#             return redirect(url_for('admin_login'))
#         return f(*args, **kwargs)
#     return decorated_function

# # Admin dashboard route (protected)
# @app.route('/admin/dashboard')
# @admin_required
# def admin_dashboard():
#     # Fetch data from the database (mock data for now)
#     data = [
#         {'name': 'John Doe', 'blood_group': 'A+', 'district': 'District 1'},
#         {'name': 'Jane Smith', 'blood_group': 'B+', 'district': 'District 2'},
#     ]
#     return render_template('admin_dashboard.html', data=data)

# # Protected donor route
# @app.route('/admin/donor')
# @admin_required
# def admin_donor():
#     # Fetch donor data from the database (mock data for now)
#     donor_data = [
#         {'name': 'Alice Johnson', 'blood_group': 'O-', 'district': 'District 3'},
#         {'name': 'Bob Brown', 'blood_group': 'AB+', 'district': 'District 4'},
#     ]
#     return render_template('donor.html', donor_data=donor_data)

# # Example route to demonstrate other users can't access admin data
# @app.route('/some_user_route')
# def some_user_route():
#     return 'This is a regular user route. Admins only can view the donor information.'


# # -------signin table-------
# # db = SQLAlchemy(app)

# class User(db.Model):
#     __bind_key__ = 'user_db'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(60), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     date = db.Column(db.DateTime, default=datetime.now())

# # -------donor table------------
# class Donor(db.Model):
#     __bind_key__ = 'donor_db'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(15), nullable=False, unique=True)
#     blood_group = db.Column(db.String(5), nullable=False)
#     district = db.Column(db.String(100), nullable=False)
#     taluk = db.Column(db.String(100), nullable=False)

# # ------patient table-------------
# class Patient(db.Model):
#     __bind_key__ = 'patient_db'
#     id = db.Column(db.Integer, primary_key=True)
#     patient_name = db.Column(db.String(100), nullable=False)
#     hospital_name = db.Column(db.String(100), nullable=False)
#     blood_group1 = db.Column(db.String(10), nullable=False)
#     district = db.Column(db.String(50), nullable=False)
#     taluk = db.Column(db.String(50), nullable=False)

# def create_db():
#     with app.app_context():
#         for bind_key in app.config['SQLALCHEMY_BINDS']:
#             engine = db.get_engine(app, bind=bind_key)
#             if bind_key == 'user_db':
#                 User.metadata.create_all(engine)
#             elif bind_key == 'donor_db':
#                 Donor.metadata.create_all(engine)
#             elif bind_key == 'patient_db':
#                 Patient.metadata.create_all(engine)

# create_db()

# @app.route('/details')
# def admin():
#     users = User.query.all()
#     return render_template('admin.html', users=users)

# # -----login page-----
# @app.route('/login', methods=['POST'])
# def login_post():
#     email = request.form['email']
#     password = request.form['password']

#     user = User.query.filter_by(email=email).first()

#     if user and user.password == hashlib.md5(password.encode()).hexdigest()[:10]:
#         return redirect(url_for('homepage'))
#     else:
#         return "Invalid email or password. Please try again."

# # ------signin---
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             return "Email already exists. Please choose a different one."

#         hashed_password = hashlib.md5(password.encode()).hexdigest()[:10]
#         new_user = User(email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))

#     return render_template('signin.html')

# # ------------------------------------------------------------------------------------------------------------------

# # -----donor page----
# @app.route('/donors')
# def donors():
#     donors = Donor.query.all()
#     return render_template('donated.html', donors=donors)

# @app.route('/donate', methods=['GET', 'POST'])
# def donate():
#     if request.method == 'POST':
#         name = request.form['name']
#         phone = request.form['phone']
#         blood_group = request.form['blood_group']
#         district = request.form['district']
#         taluk = request.form['taluk']

#         existing_donor = Donor.query.filter_by(phone=phone).first()
#         if existing_donor:
#             return "Phone number already exists. Please choose a different one."

#         new_donor = Donor(name=name, phone=phone, blood_group=blood_group, district=district, taluk=taluk)
#         db.session.add(new_donor)
#         db.session.commit()

#         return redirect(url_for('homepage'))
    
# # ------------patient page---------------


# @app.route('/patientdetails')
# def patientdetails():
#     patients = Patient.query.all()
#     return render_template('patientdetails.html', patients=patients)

# @app.route('/patients', methods=['GET', 'POST'])
# def patients():
#     if request.method == 'POST':
#         patient_name = request.form['patient_name']
#         hospital_name = request.form['hospital_name']
#         blood_group1 = request.form['blood_group1']
#         district = request.form['district']
#         taluk = request.form['taluk']

#         # Debugging: Print received data
#         print(f"Received patient data: {patient_name}, {hospital_name}, {blood_group1}, {district}, {taluk}")
#         print(f"Blood group: {blood_group1.split()[0]}, District: {district}")

#         # Create and store patient
#         patient = Patient(
#             patient_name=patient_name,
#             hospital_name=hospital_name,
#             blood_group1=blood_group1,
#             district=district,
#             taluk=taluk
#         )
#         db.session.add(patient)
#         db.session.commit()

#         # Query for matching donors
#         print("Querying for matching donors...")
#         matching_donors = Donor.query.filter_by(blood_group=blood_group1.split()[0].lower(), district=district).all()
#         print(Donor.query.filter_by(blood_group=blood_group1.split()[0], district=district).statement)

#         # Debugging: Print matching donors
#         if matching_donors:
#             for donor in matching_donors:
#                 print(f"Matching donor: {donor.name}, {donor.phone}, {donor.blood_group}, {donor.district}, {donor.taluk}")
#         else:
#             print("No matching donors found.")

#         # Check if the matching_donors list is not empty
#         print(f"Number of matching donors: {len(matching_donors)}")

#         return render_template('matching_donors.html', donors=matching_donors)
#     return render_template("home.html")

# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')

# @app.route('/home')
# def homepage():
#     return render_template('home.html')

# @app.route('/patient')
# def patient():
#     return render_template('patient.html')

# @app.route('/donor')
# def donor():
#     return render_template('donor.html')

# def new_func(app):
#     app.run(debug=True)

# if __name__ == '__main__':
#     new_func(app)




from flask import Flask, render_template, url_for, request, redirect, session, flash
import hashlib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

# Define multiple binds for your databases
app.config['SQLALCHEMY_BINDS'] = {
    'user_db': 'sqlite:///C:/blood line/website/instance/User.db',
    'donor_db': 'sqlite:///C:/blood line/website/instance/Donor.db',
    'patient_db': 'sqlite:///C:/blood line/website/instance/Patient.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Mock admin credentials
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin'

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Admin only decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('You need to be an admin to view this page.')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin dashboard route (protected)
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Fetch data from the database (mock data for now)
    data = [
        {'name': 'John Doe', 'blood_group': 'A+', 'district': 'District 1'},
        {'name': 'Jane Smith', 'blood_group': 'B+', 'district': 'District 2'},
    ]
    return render_template('admin_dashboard.html', data=data)

# Protected donor route
@app.route('/admin/donor')
@admin_required
def admin_donor():
    # Fetch donor data from the database (mock data for now)
    donor_data = [
        {'name': 'Alice Johnson', 'blood_group': 'O-', 'district': 'District 3'},
        {'name': 'Bob Brown', 'blood_group': 'AB+', 'district': 'District 4'},
    ]
    return render_template('donor.html', donor_data=donor_data)

# -------signin table-------
class User(db.Model):
    __bind_key__ = 'user_db'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

# -------donor table------------
class Donor(db.Model):
    __bind_key__ = 'donor_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    blood_group = db.Column(db.String(5), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    taluk = db.Column(db.String(100), nullable=False)

# ------patient table-------------
class Patient(db.Model):
    __bind_key__ = 'patient_db'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    hospital_name = db.Column(db.String(100), nullable=False)
    blood_group1 = db.Column(db.String(10), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    taluk = db.Column(db.String(50), nullable=False)

def create_db():
    with app.app_context():
        for bind_key in app.config['SQLALCHEMY_BINDS']:
            engine = db.get_engine(app, bind=bind_key)
            if bind_key == 'user_db':
                User.metadata.create_all(engine)
            elif bind_key == 'donor_db':
                Donor.metadata.create_all(engine)
            elif bind_key == 'patient_db':
                Patient.metadata.create_all(engine)

create_db()

# Admin-protected route to view user details
@app.route('/admin/details')
@admin_required
def admin_details():
    users = User.query.all()
    return render_template('admin.html', users=users)

# -----login page-----
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.password == hashlib.md5(password.encode()).hexdigest()[:10]:
        return redirect(url_for('homepage'))
    else:
        return "Invalid email or password. Please try again."

# ------signup---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already exists. Please choose a different one."

        hashed_password = hashlib.md5(password.encode()).hexdigest()[:10]
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signin.html')

# -----donor page----
@app.route('/admin/donors')
@admin_required
def admin_donors():
    donors = Donor.query.all()
    return render_template('donated.html', donors=donors)

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        blood_group = request.form['blood_group']
        district = request.form['district']
        taluk = request.form['taluk']

        existing_donor = Donor.query.filter_by(phone=phone).first()
        if existing_donor:
            return "Phone number already exists. Please choose a different one."

        new_donor = Donor(name=name, phone=phone, blood_group=blood_group, district=district, taluk=taluk)
        db.session.add(new_donor)
        db.session.commit()

        return redirect(url_for('homepage'))
    
# ------------patient page---------------
@app.route('/admin/patientdetails')
@admin_required
def admin_patientdetails():
    patients = Patient.query.all()
    return render_template('patientdetails.html', patients=patients)

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        hospital_name = request.form['hospital_name']
        blood_group1 = request.form['blood_group1']
        district = request.form['district']
        taluk = request.form['taluk']

        # Debugging: Print received data
        print(f"Received patient data: {patient_name}, {hospital_name}, {blood_group1}, {district}, {taluk}")
        print(f"Blood group: {blood_group1.split()[0]}, District: {district}")

        # Create and store patient
        patient = Patient(
            patient_name=patient_name,
            hospital_name=hospital_name,
            blood_group1=blood_group1,
            district=district,
            taluk=taluk
        )
        db.session.add(patient)
        db.session.commit()

        # Query for matching donors
        print("Querying for matching donors...")
        matching_donors = Donor.query.filter_by(blood_group=blood_group1.split()[0].lower(), district=district).all()
        print(Donor.query.filter_by(blood_group=blood_group1.split()[0], district=district).statement)

        # Debugging: Print matching donors
        if matching_donors:
            for donor in matching_donors:
                print(f"Matching donor: {donor.name}, {donor.phone}, {donor.blood_group}, {donor.district}, {donor.taluk}")
        else:
            print("No matching donors found.")

        # Check if the matching_donors list is not empty
        print(f"Number of matching donors: {len(matching_donors)}")

        return render_template('matching_donors.html', donors=matching_donors)
    return render_template("home.html")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/patient')
def patient():
    return render_template('patient.html')

@app.route('/donor')
def donor():
    return render_template('donor.html')

@app.route('/admin')
def admin():
    users=User.query.all()
    donors = Donor.query.all()
    patients = Patient.query.all()
    return render_template('admin.html', users=users,donors=donors,patients = patients)

if __name__ == '__main__':
    app.run(debug=True)




    # end of the projec csc
    # ncscnsck,,cccccccccccccccccccccccc
    # cn e c 

