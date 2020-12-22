from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
subscribers=[]

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///friends.db'
#initialize the DB
db= SQLAlchemy(app)

#create DB model
class Friends(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #Create a function to add a string when we create something
    def __repr__(self):
        return '<Name %r' % self.id

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete=Friends.query.get_or_404(id)


    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was an error deleting that score"

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    friend_to_update=Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a problem updating that Score"
    else:
        return render_template('update.html',friend_to_update=friend_to_update)

@app.route('/friends', methods=['POST','GET'])
def friends():

    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)

        #push to # # DB
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error....."
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html",friends=friends)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/subscribe')
def subscribe():
    return render_template("subscribe.html")

@app.route('/form', methods=['POST','GET'])
def form():
    first_name= request.form.get("first_name")
    last_name= request.form.get("last_name")
    email=request.form.get("email")

    if not first_name or not last_name or not email:
        error_statement = "Hey.. You missed some of the details....please use your back button to proceed"
        return error_statement

    subscribers.append(f"{first_name} {last_name} | {email}")
    return render_template("form.html",subscribers=subscribers)
