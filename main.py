from datetime import datetime
import re
from flask import Flask, redirect ,render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer ,primary_key=True)
    content=db.Column(db.String(300) ,nullable=False)
    detail=db.Column(db.String(500) ,nullable=False)
    # date_created = db.Column(db.DateTime ,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.content}"

@app.route("/",methods=['GET','POST'])
def html():
    if request.method=='POST':
        # print("post")
       title=request.form['title']
       desc=request.form['desc']
       todo=Todo(content=title,detail=desc)
       db.session.add(todo)
       db.session.commit()
    alltodo=Todo.query.all()
    return render_template("index.html",allTodo=alltodo)

# @app.route("/show",methods=["GET","POST"])
# def show():
#     alltodo=Todo.query.all()
#     print(alltodo)
    
#     return "this is a show page"








@app.route("/edit/<int:sno>",methods=['GET','POST'])
def edit(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.content=title
        todo.detail=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")



    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)





@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
