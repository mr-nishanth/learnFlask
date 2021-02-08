from datetime import datetime
from flask import Flask # Flask is module
from flask import render_template # render_template  is func
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is object
from flask import request , redirect , abort
from flask import abort # abort func for redirect 404 pages


app = Flask(__name__) # __name__ refer the module name


# Create database path (/// is releative path = crt working dir)  and (////is releative path = system root dir)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'


# SQLAlchemy object vaitchu database object ah create pannanuim na
# SQLAlchemy object ikku namaa create panna app ah pass pannanuim
db = SQLAlchemy(app=app)

# Here Todo(db.Model): class is inherit on db.Model obj , Todo is table
class Todo(db.Model):
    # Todo is table
    #  now  we  Craete column
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)

# Read
@app.route('/',methods=["GET"])
def index():

    # Now fetch the  all value from db and pass the frontend (index.html)
    todos = Todo.query.all()

    return render_template("index.html",title='TODO Web Application', todos=todos)


#Inert
@app.route("/add/", methods=["POST"])
def add():
    data = request.form['task']
    #print(data)

    todo = Todo(task=data, date=datetime.now())
    db.session.add(todo)
    db.session.commit()
    return redirect("/")


# Update
@app.route("/update/<id>/", methods=["GET", "POST"])
def update(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "POST":
        #print(request.form)

        # Assign the new upadte
        todo.task = request.form['task']
        db.session.commit()
        return redirect("/")
    else:

        todos = Todo.query.all()
        return render_template("index.html",title='TODO Web Application', todos=todos,update_todo=todo)



# Delete
# <int:id> = url arg from form eg:  localhost:5000/delete/1 or 2 or 3 /
@app.route("/delete/<int:id>/")
def delete(id):
    #print(id)

    try:
        # now fetch the particular id
        # Todo is class la irruakra id specific ah get pandra or select pandra and (_or_404) suppose wrong ah id send panna 404 page redirect yakanuim
        # eg: 3 task tha irruku , 3 id only but 4 inu pass panna 404-page redirect pannauim , there many method avalable , (use try except block , incrt id means call abort func) , and get_or_404(id)
        todo = Todo.query.get_or_404(id)

        # now delete that row
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")

    except Exception as ex:
        print(ex)
        # status code 404 is not fount , 403 is permission deined
        return abort(404)




if __name__ == "__main__":
    app.run(debug=True)
