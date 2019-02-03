from flask import Flask, render_template, request, redirect, json
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()

# Password to view submitted applications
password = "admin"

# Database configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'applications'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

yearkey = ['freshman', 'sophomore', 'junior', 'senior', 'grad']

# Homepage
@app.route('/')
def main():
    return render_template('index.html')

# Page containing the application form
@app.route('/application')
def application():
    return render_template('application.html')

# Login to display submitted applications
@app.route('/login', methods = ['POST'])
def login():
    # Simple keyword check, no secure password system is implemented currently
    if request.form['password'] == password:
        # Connect and fetch data
        connect = mysql.connect()
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM applicants ORDER by applicant_id')
        db = cursor.fetchall()
        header = ['First name', 'Last name', 'Preferred name', 'Pronouns', 'Email address', 'Year', 'Major', 'Minor', 'Hours available', 'Experience', "Tech's impact story", "Their impact story", "Other info"]
        rows = []
        # Add data to table to be displayed
        for i in db:
            row = []
            for j in range(1, 6):
                row.append(i[j])
            # Get class year from key
            row.append(yearkey[i[6]-1])
            for j in range(7, len(i)):
                row.append(i[j])
            rows.append(row)
        # Display data
        return render_template('view.html', data = rows, header = header)
    else:
        # "Login failed" page
        return render_template('badlogin.html')
    
# Page stating the application failed to submit because it was incomplete
# Displayed when the submit button is pressed with required fields empty
@app.route('/error')
def error():
    return render_template('error.html')

# "Application submitted successfully" message page
@app.route('/success')
def success():
    return render_template('success.html')

# Executed when 'Submit application' button is pressed
@app.route('/apply', methods = ['POST'])
def apply():

    # Checking for missing info
    goodflag = True
    
    _firstname = request.form['firstname']
    if len(_firstname) < 1:
        goodflag = False
    _lastname = request.form['lastname']
    if len(_lastname) < 1:
        goodflag = False
    _email = request.form['email']
    if len(_email) < 1:
        goodflag = False
    
    pname = request.form['prefname']
    # If no preferred name given, fill with first name
    if pname.strip() == '':
        _preferredname = _firstname
    else:
        _preferredname = pname
        
    pn = request.form['pronouns']
    # Populate with given neo-pronouns if necessary
    if pn == 'other':
        _pronouns = request.form['pronouns2']
    else:
        _pronouns = pn

    # Get number corresponding to year from key
    yr = request.form['gradyear']
    _gradyear = yearkey.index(yr)+1

    # Hours applicant is willing to commit weekly
    _timeavail = request.form['timeavail']
    if _timeavail == "":
        goodflag = False
    else:
        _timeavail = int(_timeavail)
        # Limited to positive, two digit numbers
        if (_timeavail > 99) or (_timeavail < 0):
            goodflag = False

    _major = request.form['major']
    if len(_major) < 1:
        goodflag = False
    _minor = request.form['minor']
    _personalimpact = request.form['personalimpact']
    if len(_personalimpact) < 1:
        goodflag = False
    _techimpact = request.form['techimpact']
    if len(_techimpact) < 1:
        goodflag = False
    _experience = request.form['experience']
    if len(_experience) < 1:
        goodflag = False
    _other = request.form['other']

    # If missing or illegal responses, ask applicant to try again
    if goodflag == False:
        return redirect('/error')
    # Otherwise connect and store application info in database
    else:
        connect = mysql.connect()
        cursor = connect.cursor()
        cursor.callproc('createApplication', (_firstname, _lastname, _preferredname, _pronouns, _email, _gradyear, _major, _minor, _timeavail, _experience, _techimpact, _personalimpact, _other))
        data = cursor.fetchall()
        connect.commit()
        return redirect('/success')


if __name__ == "__main__":
    app.run()
