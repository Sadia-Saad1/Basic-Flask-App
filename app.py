from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"
with app.app_context():
    db = SQLAlchemy(app)



#db = SQLAlchemy(app)


# now making a class to define the structure of our db

class FirstApp(db.Model):
    sno = db.Column(db.Integer,primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200),nullable=False)
    

    def __repr__(self):
        return f"{self.sno} - {self.fname}"


@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method=='POST':
         # Check if form fields exist
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        if fname and lname and email:
                    # Create and commit new record to the database
                    firstapp = FirstApp(fname=fname, lname=lname, email=email)
                    db.session.add(firstapp)
                    db.session.commit()
    allpeople = FirstApp.query.all()
    print(allpeople)

    return render_template('index.html',allpeople=allpeople)



@app.route('/show')
def home():

    return 'Welcome to the Home Page'


@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):

    if request.method=='POST':
          # Check if form fields exist
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        if fname and lname and email:
                    # Create and commit new record to the database
                    allpeople = FirstApp.query.filter_by(sno=sno).first()
                    allpeople.fname=fname
                    allpeople.lname=lname
                    db.session.add(allpeople)
                    db.session.commit()
         
    #first fetching the record with sno
    allpeople = FirstApp.query.filter_by(sno=sno).first()

    return render_template('update.html',allpeople=allpeople)

@app.route('/delete/<int:sno>')
def delete(sno):
    #first fetching the record with sno
    allpeople = FirstApp.query.filter_by(sno=sno).first()
    #now deleting the record
    db.session.delete(allpeople)
    db.session.commit()

    return redirect("/")



# writing main function to call the above defined function
# otherwise the program won't do anything
if __name__ == "__main__":
    app.run(debug=True)