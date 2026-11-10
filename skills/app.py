import sys
sys.path.insert(0,'db/')
from flask import Flask,render_template,request,redirect,url_for,session,flash
from dbhelper import *

app:any = Flask(__name__)
app.secret_key='599b6aa8fc0f4d08a5380df764f95656'


@app.after_request
def after_request(response)->None:
    response.headers['Cache-Control']="no-cache,no-store,must-revalidate"
    return response


@app.route("/logout")
def logout()->None:
    session.pop('email',None)
    session.clear()
    return redirect(url_for('index'))


@app.route("/deletestudent",methods=['GET'])
def deletestudent()->None:
    idno:str = request.args.get('idno')
    ok:bool = deleterecord('students',idno=idno)
    if ok:
        flash("Student Deleted")
        print("Student Deleted")
    else:
        flash("Error Deleting Student")
        print("Error Deleting Student")
    return redirect(url_for('main'))


@app.route("/login",methods=['POST'])
def login()->None:
    email:str = request.form['email']
    password:str = request.form['password']
    user:list = getrecord('users',email=email,password=password)
    if len(user)>0:
        session['email']=email
        flash("Login success")
        return redirect(url_for('main'))
    else:
        flash("Login Failed")
        return redirect(url_for('index'))
    
    
@app.route("/")
def index()->None:
    return render_template("index.html")
    
@app.route("/main")
def main()->None:
    if 'email' in session:
        students:list = getall('students')
        return render_template("main.html",students=students)
    else:
        flash("Login Properly")
        return redirect(url_for('index'))
        
@app.route("/savestudent",methods=['POST'])
def savestudent()->None:
    savetype:str = request.form['savetype']
    idno:str = request.form['idno']
    lastname:str = request.form['lastname']
    firstname:str = request.form['firstname']
    course:str = request.form['course']
    level:str = request.form['level']
    #input validate
    if idno!="" and lastname!="" and firstname!="":
        if savetype=="0":
            ok:bool = addrecord('students',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
            flash("New Student Added")
            return redirect(url_for('main'))
        if savetype=="1":
            ok:bool = updaterecord('students',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
            flash("Student Updated")
            return redirect(url_for('main'))
    else:
        flash("Fill all fields")
        return redirect(url_for('main'))
        


    
if __name__=="__main__":
    app.run(debug=True)