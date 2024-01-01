from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://sql12673992:gbbDgpdFlT@sql12.freesqldatabase.com:3306/sql12673992'
db=SQLAlchemy(app)

class Users(db.Model):
 username=db.Column(db.String(20),nullable=False)
 password=db.Column(db.String(20),nullable=False)
 id=db.Column(db.Integer,primary_key=True)

class Attendance(db.Model):
 register_number=db.Column(db.Integer,primary_key=True)
 result=db.Column(db.String(20))
 password=db.Column(db.String(20))
 student_name=db.Column(db.String(20))

@app.route('/')
@app.route('/home')
def home():
 return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  username=request.form.get('username')
  password=request.form.get('password')
  user=Users.query.filter_by(username=username,password=password).first()
  if user:
   return render_template('attendance.html')
  else:
   return render_template('login.html')
 return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
 if request.method=='POST':
  username=request.form.get('username')
  password=request.form.get('password')
  user=Users.query.filter_by(username=username).first()
  if user:
   return render_template('register.html',exist="USER ALREADY EXIST")
  else:
   new_user=Users(username=username,password=password)
   db.session.add(new_user)
   db.session.commit()
   return render_template('login.html')
 return render_template('register.html')
 

@app.route('/attendance',methods=['GET','POST'])
def attendance():
 if request.method=='POST':
  register_number=request.form.get('register_number')
  result=request.form.get('result')
  check=Attendance.query.filter_by(register_number=register_number).first()
  check.result=result
  db.session.commit()
  return render_template('attendance.html',success="successfully updated",reg_no=register_number,result=result)
 return render_template('attendance.html')

@app.route('/attendance_record',methods=['POST','GET'])
def attendance_record():
  return render_template('attendance_record.html')

@app.route('/loginhome',methods=['GET','POST'])
def loginhome():
   return render_template('loginhome.html')
 

@app.route('/parentlogin',methods=['GET','POST'])
def parentlogin():
   if request.method=='POST':
    register_number=request.form.get('register_number')
    password=request.form.get('password')
    value=Attendance.query.filter_by(register_number=register_number,password=password).first()
  
    if value:
     res=Attendance.query.filter_by(register_number=register_number).first()
     secres=res.result
     student_name=res.student_name
     return render_template('attendance_record.html',record=secres,register_number=register_number,name=student_name)
    else:
     return render_template('parentlogin.html',result="register number or password is incorrect")
   return render_template('parentlogin.html')



if __name__=='__main__':
  app.run(debug=True)
