from flask import Flask, render_template, request, redirect, json
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'applications'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

password = "H4I@BU"
yearkey = ['freshman', 'sophomore', 'junior', 'senior', 'grad']

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/application')
def application():
    return render_template('application.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.form['password'] == password:
        connect = mysql.connect()
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM applicants ORDER by applicant_id')
        db = cursor.fetchall()
        header = ['First name', 'Last name', 'Preferred name', 'Pronouns', 'Email address', 'Year', 'Major', 'Minor', 'Hours available', 'Experience', "Tech's impact story", "Their impact story", "Other info"]
        rows = []
        for i in db:
            row = []
            for j in range(1, 6):
                row.append(i[j])
            row.append(yearkey[i[6]-1])
            for j in range(7, len(i)):
                row.append(i[j])
            rows.append(row)
        return render_template('view.html', data = rows, header = header)
    else:
        return render_template('badlogin.html')
    
@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/apply', methods = ['POST'])
def apply():
    
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
    if pname.strip() == '':
        _preferredname = _firstname
    else:
        _preferredname = pname

        
    pn = request.form['pronouns']
    if pn == 'other':
        _pronouns = request.form['pronouns2']
    else:
        _pronouns = pn


    yr = request.form['gradyear']
    _gradyear = yearkey.index(yr)+1


    _timeavail = request.form['timeavail']
    if _timeavail == "":
        goodflag = False
    else:
        _timeavail = int(_timeavail)
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


    if goodflag == False:
        return redirect('/error')
    else:
        connect = mysql.connect()
        cursor = connect.cursor()
        cursor.callproc('createApplication', (_firstname, _lastname, _preferredname, _pronouns, _email, _gradyear, _major, _minor, _timeavail, _experience, _techimpact, _personalimpact, _other))
        data = cursor.fetchall()
        connect.commit()
        return redirect('/success')



if __name__ == "__main__":
    app.run()
