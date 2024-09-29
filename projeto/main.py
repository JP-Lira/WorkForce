from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy  # pip install flask-SQLAlchemy


app = Flask(__name__)

# Fazendo a conexão com o banco de dados através do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:darc147@localhost/workforce'
print('Banco de dados CONECTADO')

db = SQLAlchemy(app)  # Instanciando a aplicação para o SQLAlchemy


# Criando classe para as informações das tabelas

class Departamentos(db.Model):
    __tablename__ = 'departamentos'

    id_departamento = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    nome_departamento = db.Column(db.String(100))
    id_gerente = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return '<Name %r>' % self.name


class Cargos(db.Model):
    __tablename__ = 'cargos'

    id_cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cargo = db.Column(db.String(100))

    def __repr__(self):
        return '<Name %r>' % self.name


class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'

    id_func = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_func = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100))
    tel1 = db.Column(db.String(15), nullable=False)
    tel2 = db.Column(db.String(15))
    data_contratacao = db.Column(db.Date, nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    status_func = db.Column(
        db.Enum('EFETIVO', 'FERIAS', 'DEMITIDO', 'ATESTADO'))

    # Criando as foreign key da tabela
    fk_id_cargo = db.Column(db.Integer, db.ForeignKey(
        'cargos.id_cargo'), nullable=False)
    fk_id_departamento = db.Column(db.Integer, db.ForeignKey(
        'departamentos.id_departamento'), nullable=False)

    # Criando as relações entre as tabelas
    cargo = db.relationship('Cargos', backref='funcionarios')
    departamento = db.relationship('Departamentos', backref='funcionarios')

    def __repr__(self):
        return '<Name %r>' % self.name


class Folha_pagamento(db.Model):
    __tablename__ = 'folha_pagamento'

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_pagamento = db.Column(db.Date, nullable=False)
    salario_base = db.Column(db.Numeric(10, 2), nullable=False)
    deducoes = db.Column(db.Numeric(10, 2), nullable=False)
    salario_liquido = db.Column(db.Numeric(10, 2), nullable=False)

    # Criando a Foreign Key da tabela
    fk_id_func = db.Column(db.Integer, db.ForeignKey(
        'funcionarios.id_func'), nullalbe=False)

    # Criando a relação da tabela 'folha_pagamento' com 'funcionarios'
    funcionario = db.relationship('Funcionarios', backref='folha_pagamentos')

    def __repr__(self):
        return '<Name %r>' % self.name

# OBS: o db.Numeric é o equivalente ao Decimal do SQL. Esse é o tipo correspondente no SQLAlchemy.


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lista')
def lista_de_funcionario():
    lista_func = Funcionarios.query.order_by(Funcionarios.id_func)
    return render_template('lista.html', lista_func=lista_func, titulo="Lista de Funcionários")


@app.route('/cadastro')
def cadastro_funcionario():
    return render_template('cadastro.html')


@app.route('/criando')
def criando():
    # Requisitando as informações do fórmulario:
    nome = request.form['nome_func']
    email = request.form['email']
    tel1 = request.form['tel1']
    tel2 = request.form['tel2']
    data_nascimento = request.form['birthdate']
    salario = request.form['salary']


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
