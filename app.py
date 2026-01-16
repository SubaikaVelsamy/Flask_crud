from flask import Flask, render_template, redirect, request, url_for
import mysql.connector

app = Flask(__name__)


db =    mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        db="schooldb"
    )

@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("Select * from student_data")
    student_data = cursor.fetchall()
    return render_template("index.html", student_data=student_data)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        full_name = request.form['full_name']
        mobile = request.form['mobile']
        email = request.form['email']

        cursor = db.cursor()
        cursor.execute("INSERT into student_data (full_name,mobile,email) VALUES (%s, %s, %s)",(full_name,mobile,email))
        db.commit()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route('/delete/<int:id>/')
def delete(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("delete from student_data where id=%s",(id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>/',methods=['GET','POST'])
def edit(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        full_name = request.form['full_name']
        mobile = request.form['mobile']
        email = request.form['email']

        cursor.execute("Update student_data set full_name=%s,mobile=%s,email=%s where id=%s",(full_name,mobile,email,id,))
        db.commit()
        return redirect(url_for('index'))
    
    cursor.execute("select * from student_data where id=%s",(id,))
    student_data = cursor.fetchone()
    return render_template("edit.html",student_data=student_data)


if __name__ == "__main__":
    app.run(debug=True)




