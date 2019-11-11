import os
import re
from flask import Flask, session, url_for, redirect,render_template, request, flash
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gothan'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "cepdatabase.db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Cep(db.Model):

    __tablename__ = 'tab_cep'
    cep = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
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

db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    if request.form:
        cep = Cep(request.form['cep'],request.form['cidade'])
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
    
    return render_template('index.html')

@app.route('/lista_db')
def lista_db():
    col_db = ['Cep','Cidade']
    db_cep = Cep.query.all()

    return render_template('lista_db.html',
                           col_db=col_db,
                           db_cep=db_cep)

if __name__ == '__main__':
    app.run(debug=True)
