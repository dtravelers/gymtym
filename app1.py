# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,render_template,request,redirect,url_for,flash,session,g
from user import user_operation
from admin import admin_operation
import hashlib
import random
from flask_mail import *
import mysql.connector

# Flask constructor takes the name of 
# current module (__name__) as argument.
app1 = Flask(__name__)
app1.secret_key = "yutyu56757guds6ewiu"
 # session
#-------------------mail configuration---------------------------
app1.config["MAIL_SERVER"]='smtp.office365.com'
app1.config["MAIL_PORT"] = '465'
app1.config["MAIL_USERNAME"] = 'kashyapsakshi1229@outlook.com'
app1.config["MAIL_PASSWORD"]= 'Sakshi12@'
app1.config["MAIL_USE_TLS"] = True
app1.config["MAIL_USE_SSL"] = False
mail = Mail(app1)
#----------------------------------------------------


@app1.route('/')
def home():
        return render_template('index.html')

  
@app1.route('/user_registeration')
def user_registeration():
        return render_template('registration.html')


@app1.route('/submit', methods=['POST'])
def submit():
      if request.method=='POST':
               # if(captcha_text!=request.form['captcha']):
                #        flash("Invalid captcha!!")
                 #       return redirect(url_for("/user_registeration"))
     
                name = request.form['name']
                email = request.form['email']
                password = request.form['password']
                  #--- password encryption----------------
                pas = hashlib.md5(password.encode())
                password = pas.hexdigest()

                op = user_operation()   #object
                op.submit(name,email,password)
                
                flash(" You can Login Now!!!")
                return redirect(url_for('user_registeration'))


@app1.route('/user_login_verify',methods=['GET','POST'])
def user_login_verify():
        if request.method=='POST':
                email=request.form['email']
                password=request.form['password']
                    #--- password encryption----------------
                pas = hashlib.md5(password.encode())
                password = pas.hexdigest()

                op = user_operation()  # object create
                r=op.user_login_verify(email,password)
                if (r==0):
                        flash("invalid user email and password!!")
                        return redirect(url_for('user_registeration'))
                else:
                        return render_template("dashboard.html")

@app1.route('/user_logout')
def user_logout():
        session.clear()
        flash("Logged out successfully!!!")
        return redirect(url_for('user_registeration'))

@app1.route('/user_forgotten_password', methods=['GET', 'POST'])
def user_forgotten_password():
    if request.method == 'POST':
        email = request.form['email']

        # Generate a random reset token
        reset_token = str(random.randint(100000, 999999))
        session['reset_token'] = reset_token
        session['reset_email'] = email

        # Send reset token via email
        mail = Mail(app1)  # Ensure flask_mail is properly configured
        msg = Message('Password Reset Token', sender='kashyapsakshi1229@outlook.com', recipients=[email])
        msg.body = f'Your password reset token is: {reset_token}'
        mail.send(msg)

        flash('A password reset token has been sent to your email.')
        return render_template('verify_reset_token.html')  # Page to enter the reset token

    return render_template('forgot_password.html')  # Forgot Password page


@app1.route('/verify_reset_token', methods=['POST'])
def verify_reset_token():
    token = request.form['token']
    if 'reset_token' in session and session['reset_token'] == token:
        return render_template('reset_password_form.html')  # Page to set a new password
    else:
        flash('Invalid or expired reset token.')
        return redirect(url_for('user_forgotten_password'))


@app1.route('/update_password', methods=['POST'])
def update_password():
    if 'reset_email' in session:
        email = session['reset_email']
        password = request.form['password']
        
        # Encrypt the new password
        pas = hashlib.md5(password.encode())
        encrypted_password = pas.hexdigest()

        # Update password in the database
        op = user_operation()
        op.update_password(email, encrypted_password)  # Implement update_password in user_operation

        # Clear session data
        session.pop('reset_token', None)
        session.pop('reset_email', None)

        flash('Your password has been updated successfully.')
        return redirect(url_for('user_registeration'))
    else:
        flash('Unauthorized action. Please start the reset process again.')
        return redirect(url_for('user_forgotten_password'))


@app1.route('/member_insert',methods=['POST','GET'])
def member_insert():
       if 'user_email'in session:
              if request.method=='POST':
                    member_id=request.form["member_id"]
                    plan_name=request.form["plan_name"]
                    address=request.form["address"]
                    charges=request.form["charges"]
                    phone_no=request.form["phone_no"]
                    start_date=request.form["start_date"]
                    end_date=request.form["end_date"]

                    op=user_operation()
                    op.member_insert(member_id,plan_name,address,charges,phone_no,start_date,end_date)
                    flash("Your membership is added successfully!!")
                    return redirect(url_for('dashboard'))
       else:
              flash("You are not logged in.. please login now!!")
              return redirect(url_for('user_registeration'))

@app1.route('/member_list')
def member_list():
        if 'admin_email' in session:
                op=user_operation()
                member_records = op.member_list()
                return render_template("member_list.html",records=member_records)
        else:
                flash("You are not logged in.. please login now!!")
                return redirect(url_for('admin_login'))



@app1.route('/dashboard')
def dashboard():
        if 'user_email' in session:
                op=user_operation()
                return render_template("dashboard.html")
               
        else:
                flash("You are not logged in.. please login now!!")
                return redirect(url_for('user_registeration'))

@app1.route('/membership')
def membership():
        return render_template('membership.html')

@app1.route('/main_layout')
def main_layout():
        return render_template('main_layout.html')

@app1.route('/about')
def about():
        return render_template('about.html')



#-------------------------------------------admin module----------------------------------
 
@app1.route('/admin_registration')
def admin_registration():
        return render_template('admin_registration.html')


@app1.route('/admin_dashboard')
def admin_dashboard():
        return render_template('admin_dashboard.html')

@app1.route('/admin_layout')
def admin_layout():
        return render_template('admin_layout.html')

@app1.route('/dash')
def dash():
        return render_template('dash.html')

@app1.route('/admin_submit', methods=['POST'])
def admin_submit():
      if request.method=='POST':
                name = request.form['name']
                email = request.form['email']
                password = request.form['password']
                  #--- password encryption----------------
                pas = hashlib.md5(password.encode())
                password = pas.hexdigest()

                op = admin_operation()   #object
                op.admin_submit(name,email,password)
                
                flash(" You can Login Now!!!")
                return redirect(url_for('admin_registration'))



@app1.route('/admin_login_verify',methods=['GET','POST'])
def admin_login_verify():
        if request.method=='POST':
                email=request.form['email']
                password=request.form['password']
                  #--- password encryption----------------
                pas = hashlib.md5(password.encode())
                password = pas.hexdigest()

                op = admin_operation()  # object create
                r=op.admin_login_verify(email,password)
                if (r==0):
                        flash("invalid admin email and password!!")
                        return redirect(url_for('admin_registration'))
                else:
                         # Store admin email in session after successful login
                        session['admin_email'] = email
                        return redirect(url_for('admin_layout'))

@app1.route('/admin_logout')
def admin_logout():
        session.clear()
        flash("Logged out successfully!!!")
        return redirect(url_for('admin_registration'))




# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app1.run(debug=True)