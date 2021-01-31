#!/usr/python

from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from flask import url_for, redirect, request
from flask import flash # for msg

# create Flask obj
app = Flask(__name__)

# MySQL CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "NiShAnTh@007"
app.config["MYSQL_DB"] = "tutorjoes_flask_crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


# Loading Home Page
@app.route("/")
def home():
    #return "<h1> Hello World </h1>"
    con = mysql.connection.cursor()
    # Query
    sql = "SELECT * FROM users";
    con.execute(sql)
    res = con.fetchall()
    return render_template("home.html",datas=res)

# New User Insert
@app.route("/addUsers",methods=["GET","POST"])
def addUsers():
    if request.method == "POST":
        name = request.form["name"]
        city = request.form["city"]
        age = request.form["age"]

        # intialize the connection
        con = mysql.connection.cursor()

        sql = "INSERT INTO users (NAME , CITY , AGE) value (%s , %s , %s)"
        con.execute(sql, [name, city, age])
        mysql.connection.commit()
        con.close()
        flash("User Details Added")
        return redirect(url_for("home"))
    return render_template("addUsers.html")

# Update users
# <string:id> = here we get the id
@app.route("/editUser/<string:id>",methods=["GET","POST"])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form["name"]
        city = request.form["city"]
        age = request.form["age"]
        sql = "update users set NAME=%s , CITY=%s , AGE=%s  where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash("User Details Updated")
        return redirect(url_for("home"))

    sql = "select * from users where ID=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    return render_template("editUser.html",datas=res)

# Delete Users
@app.route("/deleteUser/<string:id>", methods=["GET", "POST"])
def deleteUser(id):
    con = mysql.connection.cursor()
    sql = "delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash("User Details Deleted")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.secret_key="abc123" # for display the flash in home page
    app.run(debug=True)
