from flask import (
    Flask,
    flash,
    render_template,
    request,
    url_for,
    redirect,
    send_from_directory,
    session,
)
from werkzeug.utils import secure_filename
from multiprocessing import Manager
from sqlalchemy import create_engine, text

app = Flask(__name__)
engine = create_engine("mysql+pymysql://tree:ChangeMe01!@10.0.1.76/solar")

app.config["UPLOAD_FOLDER"] = "uploads"

app.secret_key = "private"
admin_user = "plank"

users = {
    "bob": "sjhd76eww!",
    "clem": "khsd54#h",
    "alicia": "jhsjhsd222!",
    "sue": "76shshs63!",
    "plank": "5!ys!hhsds",
}

submissions = [["", "", "", ""], ["", "", "",  ""], ["", "", "", ""], ["", "", "", ""]]


@app.route("/")
def main():
    with engine.connect() as conn:
        results = conn.execute(text("SELECT arrayID, solarStatus, arrayVoltage, arrayCurrent FROM SOLAR_ARRAYS;"))
    
    solar_arrays = []
    power_generation = []

    for result in results:
        solar_arrays.append((result["arrayID"],result["solarStatus"]))
        power_generation.append((result["arrayID"],str(int(result["arrayCurrent"])*int(result["arrayVoltage"]))+" W"))
    return render_template("main.html", solarArrays=solar_arrays, powerGen=power_generation)


@app.route("/manufacturing")
def manufacturing():
    return render_template("manufacturing.html")


@app.route("/contact", methods=("GET", "POST"))
def contact():
    global submissions
    if request.method == "POST":
        if "file" not in request.files:
            flash("File required")
            return redirect(url_for("contact"))
        file = request.files.get("file", None)
        if not file or not file.filename:
            flash("File required")
            return redirect(url_for("contact"))
        if file:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            filename = secure_filename(file.filename)
            file.save("uploads/" + filename)

            submissions.pop()
            submissions = [[name, email, phone, filename]] + submissions
            flash("Submission successful")
            return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/solargen")
def solargen():
    return render_template("solargen.html")


@app.route("/admin")
def admin():
    global submissions
    if not session["loggedIn"]:
        return redirect(url_for("main"))

    files = []
    emails = []
    for sub in submissions:
        emails.append(", ".join(sub) if any(sub) else "")
        files.append(sub[-1])
    return render_template("admin.html", emails=emails, files=files)


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None

        if not username:
            error = "Username required."
        elif not password:
            error = "Password required"
        elif username not in users or users[username] != password:
            error = "Authentication failure, please check your username and password."

        if error:
            flash(error)
            return redirect(url_for("login"))
        if username == admin_user:
            session["loggedIn"] = True
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            flash("Login successful.")
            session["loggedIn"] = True
            return redirect(url_for("main"))


@app.route("/logout")
def logout():
    session["loggedIn"] = False
    session["admin"] = False
    return redirect(url_for("main"))
