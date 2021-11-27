from flask import Flask, json, jsonify, request, make_response,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from flask import request,render_template,redirect
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)

class Users(db.Model,UserMixin):
    __tablename__ = "userlist"
    id = db.Column(db.Integer, primary_key=True)
    first_name =db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_name = db.Column(db.String(50),unique = True)
    user_pass = db.Column(db.String(50))

    def __init__(self, user_name, user_pass,first_name,last_name):
        self.user_name = user_name
        self.user_pass = user_pass
        self.first_name = first_name
        self.last_name = last_name

class UserSchema(ma.Schema):
	class Meta:
		fields = ("user_name","user_pass","first_name","last_name")
		
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class RegisterForm(FlaskForm):
    user_name= StringField(validators=[InputRequired(),Length(
        min=4, max=50)],render_kw={"placeholder":"Username"})
    user_pass= PasswordField(validators=[InputRequired(),Length(
        min=4, max=50)],render_kw={"placeholder":"Password"})
    first_name= StringField(validators=[InputRequired(),Length(
        min=4, max=50)],render_kw={"placeholder":"First Name"})
    last_name= StringField(validators=[InputRequired(),Length(
        min=4, max=50)],render_kw={"placeholder":"Last Name"})
    submit = SubmitField("               Register                 " )


    def validate_username(self,user_name):
        existing_user_name= Users.query.filter_by(user_name=user_name.data).first()

        if existing_user_name:
            raise ValidationError("Username Already Exists")

class LoginForm(FlaskForm):
    user_name= StringField(validators=[InputRequired(),Length(
        min=4, max=50)],render_kw={"placeholder":"Username"})
    user_pass= PasswordField(validators=[InputRequired(),Length(
        min=4, max=50)],render_kw={"placeholder":"Password"})
    submit = SubmitField("                 Login                  " )
    

@app.route("/")
def main():
    return render_template("index.html",name=current_user)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hased_password= bcrypt.generate_password_hash(form.user_pass.data)
        new_user = Users(user_name=form.user_name.data,
        user_pass= hased_password, 
        first_name=form.first_name.data, 
        last_name= form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
    return render_template("register.html",form=form)

@app.route("/login", methods = ['GET','POST'] )
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user= Users.query.filter_by(user_name=form.user_name.data).first()
        if user:
            if bcrypt.check_password_hash(user.user_pass,form.user_pass.data):
                login_user(user)
                return redirect(url_for("main"))
            
            else:
                return "ERROR"
    return render_template("login.html",form=form)

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
        logout_user()
        return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)