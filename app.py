from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentNo = db.Column('student_no', db.String(20), unique=True)
    name = db.Column(db.String(30))

    def __init__(self, studentNo, name):
        self.studentNo = studentNo
        self.name = name

db.create_all()
import time
@app.route('/')
def index():
  studentList = Student.query.all()
  return render_template('index.html', studentList=studentList,time = time.time())

@app.route('/create_student', methods=['GET', 'POST'])
def createStudent():
  if request.method == 'GET':
    return render_template('student_form.html')
  else:
    studentNo = request.form.get('studentNo')
    name = request.form.get('name')
    st = Student(studentNo, name)
    db.session.add(st)
    db.session.commit()
    file = request.files['image']
    if file and file.filename != '':
      file.save('static/'+studentNo+'.jpg')
    return redirect('/')

@app.route('/delete/<int:id>')
def deleteStudent(id):
  st = Student.query.get(id)
  db.session.delete(st)
  db.session.commit()
  return redirect('/')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def editStudent(id):
  if request.method == 'GET':
    st = Student.query.get(id)
    return render_template('student_form.html', 
                            studentNo=st.studentNo,
                            name=st.name)
  else:
    st = Student.query.get(id)
    st.studentNo = request.form.get('studentNo')
    st.name = request.form.get('name')
    db.session.commit()
    file = request.files['image']
    if file and file.filename != '':
      file.save('static/'+st.studentNo+'.jpg')
    return redirect('/')

app.run(debug=True)