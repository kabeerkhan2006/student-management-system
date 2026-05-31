from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
from flask import send_file

app = Flask(__name__)

# Database Create
def init_db():

    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        semester TEXT,
        branch TEXT,
        email TEXT,
        roll TEXT,
        mobile TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('add.html')

  
# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        semester = request.form['semester']
        branch = request.form['branch']
        email = request.form['email']
        roll = request.form['roll']
        mobile = request.form['mobile']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()

        c.execute(
    "SELECT * FROM students WHERE email=? OR roll=?",
    (email, roll)
)

    existing_student = c.fetchone()

    if existing_student:
        conn.close()
        return "Email ya Roll No. already registered!"

        

        c.execute(
            "INSERT INTO students (name, semester, branch, email, roll, mobile) VALUES (?, ?, ?, ?, ?, ?)",
            (name, semester, branch, email, roll, mobile)
        )

        conn.commit()
        conn.close()

        return """
<h2 style='color:green;text-align:center;'>
Registration Successful ✅
</h2>
"""

    return render_template('add.html')

# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    c.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        semester = request.form['semester']
        branch = request.form['branch']
        email = request.form['email']
        roll = request.form['roll']
        mobile = request.form['mobile']

        c.execute('''
        UPDATE students
        SET name=?, semester=?, branch=?, email=?, roll=?, mobile=?
        WHERE id=?
        ''', (name, semester, branch, email, roll, mobile, id))

        conn.commit()
        conn.close()

        return redirect('/')

    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()

    conn.close()

    return render_template('edit.html', student=student)
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "hod" and password == "hod123":
            return redirect('/admin')

        return "Invalid Username or Password"

    return render_template('admin_login.html')

@app.route('/admin')
def admin():

    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    c.execute("SELECT * FROM students")
    students = c.fetchall()

    total_students = len(students)

    conn.close()

    return render_template(
        'admin_dashboard.html',
        students=students,
        total_students=total_students
    )
@app.route('/export')
def export_excel():

    conn = sqlite3.connect('students.db')

    df = pd.read_sql_query(
        "SELECT name, semester, branch, email, roll, mobile FROM students",
        conn
    )

    conn.close()

    df.index = range(1, len(df) + 1)
    df.index.name = "Sr. No."

    file_name = "students.xlsx"

    df.to_excel(file_name)

    return send_file(
        file_name,
        as_attachment=True
    )
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        roll = request.form['roll']

        conn = sqlite3.connect('students.db')
        c = conn.cursor()

        c.execute(
            "SELECT * FROM students WHERE email=? AND roll=?",
            (email, roll)
        )

        student = c.fetchone()

        conn.close()

        if student:
         return render_template(
        'student_dashboard.html',
        student=student
    )

        return "Invalid Email or Roll No"

    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)
   
   