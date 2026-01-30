import redis
import json
from flask import Flask, render_template, redirect, request, url_for, jsonify
import mysql.connector
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png","jpeg","jpg"}

cache = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)

CACHE_TTL = 60

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

def allowed_filename(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/api/save',methods=['GET','POST'])
def save_data():
    data = request.get_json()  # <-- read JSON from request

    full_name = data.get('full_name')
    mobile = data.get('mobile')
    email = data.get('email')

    if not full_name or not mobile or not email:
        return jsonify({"error": "Missing data"}), 400

    cursor = db.cursor()
    cursor.execute("INSERT into student_data (full_name,mobile,email) VALUES (%s, %s, %s)",(full_name,mobile,email))
    db.commit()
    cache.delete("all_students")  # clear cached list
    return jsonify({"message": "User created successfully"}), 201

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

@app.route("/api/user/<int:id>", methods=["GET"])
def get_user(id):
    cached = cache.get(f"user:{id}")
    if cached:
        return jsonify(json.loads(cached))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student_data WHERE id=%s", (id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        cache.setex(f"user:{id}",CACHE_TTL,json.dumps(user))
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route("/api/edit/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    full_name = data.get("full_name")
    mobile = data.get("mobile")
    email = data.get("email")

    if not full_name or not mobile or not email:
        return jsonify({"error": "Missing data"}), 400

    cursor = db.cursor()
    cursor.execute(
        "UPDATE student_data SET full_name=%s, mobile=%s, email=%s WHERE id=%s",
        (full_name, mobile, email, id)
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "User updated successfully"}), 200

@app.route("/api/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    
    if not id:
        return jsonify({"error": "Missing data"}), 400

    cursor = db.cursor()
    cursor.execute("delete from student_data where id=%s",(id,))
    db.commit()
    cursor.close()

    return jsonify({"message": "User Deleted successfully"}), 200


@app.route("/api/test")
def test_api():
    return {"message": "Flask + React connected"}

@app.route("/api/users")
def api_users():
    cached = cache.get("all_students")
    if cached:
        return jsonify(json.loads(cached))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("Select * from student_data")
    student_data = cursor.fetchall()

    cache.setex("all_students",CACHE_TTL,json.dumps(student_data))
    return jsonify(student_data)

@app.route("/api/user/<int:id>/photo", methods=["PUT"])
def update_user_photo(id):
    file = request.files.get("profile_photo")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    if not allowed_filename(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    import uuid
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    cursor = db.cursor()
    cursor.execute(
        "UPDATE student_data SET profile_photo=%s WHERE id=%s",
        (filename, id)
    )
    db.commit()
    cursor.close()

    # Clear cache
    cache.delete(f"user:{id}")
    cache.delete("all_students")

    return jsonify({
        "message": "Profile photo updated",
        "photo_url": f"/static/uploads/{filename}"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)




