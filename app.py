from datetime import timedelta

import os
import re
from flask import Flask, session, url_for, redirect,render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gotham'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "cepdatabase.db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin,db.Model):

    __tablename__ = 'tab_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Cep(db.Model):

    __tablename__ = 'tab_cep'
    cep_id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(80), unique=True, nullable=False)
    cidade = db.Column(db.String(80), nullable=False)
    
    def __init__(self,cep,cidade):
        self.cep = str(cep)
        self.cidade = cidade
        self.step1 = False
        self.step2 = False
    
    def validaCep(self):

        if re.match(r'^([1-9][\d]{5})$',self.cep):
            self.step1 = True
            
        if (self.cep[0] != self.cep[2] 
        and self.cep[1] != self.cep[3] 
        and self.cep[2] != self.cep[4] 
        and self.cep[3] != self.cep[5]):
            self.step2 = True

#db.drop_all()
#db.create_all()
#user = User(username='admin', password='masterkey')
#db.session.add(user)
#db.session.commit()

@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(id)
    except:
        return None

@app.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.form:
        cep = Cep(request.form['cep'],request.form['cidade'])
        if request.form['cidade'] != '':
            cep.validaCep()
            if (cep.step1 == True) & (cep.step2 == True):
                try:
                    db.session.add(cep)
                    db.session.commit()
                    flash('CEP cadastrado com sucesso')
                except:
                    flash('CEP já cadastrado')
            else:
	            flash('Não foi possível realizar o cadastro. CEP com formato inválido!')
        else:
            flash('O campo Cidade não pode ser vazio.')
    return render_template('index.html')

@app.route('/lista_db')
@login_required
def lista_db():
    col_db = ['Cep','Cidade']
    db_cep = Cep.query.all()
    return render_template('lista_db.html',
                           col_db=col_db,
                           db_cep=db_cep)
                           
@app.route('/login', methods=['GET','POST'])
def login():
    if request.form:
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or user.password != request.form['passw']:
            flash('Usuário não cadastrado!')
            return redirect(url_for('login'))
        login_user(user)
        app.permanent_session_lifetime = timedelta(minutes=3)
        return redirect(url_for('index'))
    return render_template('login.html')                        

if __name__ == '__main__':
    app.run(debug=True)
