from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Grocery(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"{self.sno} - {self.food}"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)    

with app.app_context():
    db.create_all()

@app.route("/" ,methods =['GET','POST'])
def signup():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if not email or not password:
            message = "please enter both email and password."
        elif password != repassword:
            message = "passwords do not match!"
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
               # message = "user already exist please enter another email ID"
                return redirect("login")
            else: 
                credentials = User(email = email , password = password)
                db.session.add(credentials)
                db.session.commit()
                return redirect(url_for('login'))
    return render_template('up.html', alert_message=message)    

@app.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "POST":
        food = request.form["food"]
        quantity = request.form["quantity"]
        grocery_item = Grocery(food=food, quantity=quantity)
        db.session.add(grocery_item)
        db.session.commit()
    grocery_items = Grocery.query.all()
    return render_template("menu.html", allgrocery=grocery_items)

@app.route("/login",methods=['GET','POST'])
def login():
    message = None
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            message = "please enter both email and password."
        else:
            user = User.query.filter_by(email=email).first()
            if not user:
                message = "user not found. please sign up."
            elif user.password != password:
                message = "incorrect password."
            else:
                return redirect(url_for('menu'))            
    return render_template('log.html', alert_message=message)
    


@app.route("/order/<int:sno>")
def order(sno):
    # print(f"Order route called with sno: {sno}")
    grocery_item = Grocery.query.filter_by(sno=sno).first()
    return render_template("order.html", grocery=grocery_item)


@app.route("/total_order")
def total_order():
    grocery_items = Grocery.query.all() 
    return render_template("order.html", allgrocery=grocery_items)



@app.route("/delete/<int:sno>", methods=["POST"])
def delete(sno):
    grocery_item = Grocery.query.filter_by(sno=sno).first()
    if grocery_item:
        db.session.delete(grocery_item)
        db.session.commit()
    return redirect(url_for("menu"))


if __name__ == "__main__":
    app.run(debug=True,port=8000)

    #up.html, log.html, order.html, menu.html, base3.html
