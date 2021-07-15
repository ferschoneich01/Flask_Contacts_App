from flask import Flask, render_template, request, redirect, url_for, flash
from flask.wrappers import Request
from flask_mysqldb import MySQL 

app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Fernando'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flaskcontact'

mysql = MySQL(app)

#session

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)

    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['Fullname']
        phone = request.form['Phone']
        email = request.form['Email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',(fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added sucessfully')
        return redirect(url_for('Index'))

@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',(id))   
    data = cur.fetchall()
    return render_template('edit_contacts.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['Fullname'] 
        phone = request.form['Phone'] 
        email = request.form['Email']     
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, phone = %s, email = %s WHERE id = %s',(fullname,phone,email,id))
        mysql.connection.commit()
        flash('Contact Updated Succesfully')
        
        return redirect(url_for('Index'))
       
        

@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed sucessfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 5000, Debug = True)