from functools import wraps
from flask import Flask,render_template, request,url_for,redirect,flash,session
from flask_mysqldb import MySQL
from flask_login import login_required
import os

app = Flask('__name__')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='studentsystem'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route("/",methods=['GET','POST'])
@app.route("/registeration",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        choice=request.form['choose']
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('''insert into login(Username,Password,Type) values(%s,%s,%s)''',(username,password,choice))
        mysql.connection.commit()
        cursor.close()
        flash('Registration Successfull')
        return redirect(url_for('login'))
    return render_template("registeration.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        choice=request.form['choose']
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('''select Username,Password,Type from login where Username = %s and Password = %s and Type = %s''',(username,password,choice))
        result = cursor.fetchall()
        if len(result)== 1 :
           session['logged_in'] = True
           session['username'] = username
           if choice == 'professor':
                return redirect(url_for('professor'))
           else:
                return redirect(url_for('mark'))
    return render_template("login.html")

def login_required(route_function):
    @wraps(route_function)
    def decorated_route(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('login')
        return route_function(*args, **kwargs)
    return decorated_route

@app.route("/professor",methods=['GET','POST'])
@login_required
def professor():
    if request.method == 'POST':
        Name=request.form['name']
        Rollno=request.form['rollno']
        Mark1=request.form['mark1']
        Mark2=request.form['mark2']
        Mark3=request.form['mark3']
        Mark4=request.form['mark4']
        Mark5=request.form['mark5']
        Total=request.form['total']
        Average=request.form['average']
        cursor=mysql.connection.cursor()
        cursor.execute(''' insert into table1(Name,Rollno,Mark1,Mark2,Mark3,Mark4,Mark5,Total,Average) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(Name,Rollno,Mark1,Mark2,Mark3,Mark4,Mark5,Total,Average))
        mysql.connection.commit()
        cursor.close()
    return render_template('table.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/mark',methods=['GET','POST'])
@login_required
def mark():
    cursor=mysql.connection.cursor()
    cursor.execute('''select * from table1 ''')
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template("mark.html", datas= result)


if (__name__ == '__main__'):
   app.secret_key="123"
   app.run(debug = True)
