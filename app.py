from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,RadioField,IntegerField,validators
from wtforms.validators import InputRequired, Length,AnyOf
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SECRET_KEY']='abcd'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:tiger@localhost/MyApp'
db=SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Organisation_Name=db.Column(db.String(120))
    name=db.Column(db.String(120))
    Email=db.Column(db.String(120),unique=True)
    contact=db.Column(db.BigInteger,unique=True)
    group=db.Column(db.String(20))

    def __init__(self,Organisation_Name,name,Email,contact,group):
        self.Organisation_Name=Organisation_Name
        self.name=name
        self.Email=Email
        self.contact=contact
        self.group=group
    def __repr__(self):
        return '<User %r>' % self.Email
class RegistrationForm(FlaskForm):
    Organisation_Name=StringField('Organisation Name',validators=[InputRequired(message='Field Required'),Length(min=3 ,max=50,message='between 3 and 10')])
    name=StringField('Contact Name',validators=[InputRequired(message='Field Required'),Length(min=3 ,max=50,message='between 3 and 10')])
    Email=StringField('Email Address',validators=[InputRequired(message='Field Required'),Length(min=3 ,max=50,message='between 3 and 10')])
    contact=IntegerField('Mobile no')
    group=RadioField('Group',choices=[('marketing','marketing'),('technical','technical'),('management','management')])
@app.route('/form', methods=['GET','POST'])
def form():
        form=RegistrationForm()
        if form.validate_on_submit():
            user=User(request.form['Organisation_Name'],request.form['name'],request.form['Email'],request.form['contact'],request.form['group'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('form'))
        return render_template('form.html',form=form)
@app.route('/admin')
def admin():
    user=User.query.all()
    return render_template('admin.html',user=user)
if __name__=='__main__':
    app.run(debug=True)
