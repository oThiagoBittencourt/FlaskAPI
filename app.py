# pip isntall Flask-SQLAlchemy

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'livraria.db')
db = SQLAlchemy(app)

# cria tabela

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text)
    autor = db.Column(db.Text)
    editora = db.Column(db.Text)
    valor = db.Column(db.Float)

    def __init__(self, titulo, autor, editora, valor):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.valor = valor

    def __repr__(self) -> str:
        return f'{self.titulo} ({self.autor})'
    
@app.route('/')
def index():
    #db.create_all()
    livros = Livro.query.all()
    return render_template('index.html')

@app.route('/adicionar', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        editora = request.form['editora']
        valor = request.form['valor']
        livro = Livro(titulo, autor, editora, valor)
        db.session.add(livro)
        db.session.commit()
        return redirect(url_for('insert'))
    else:
        return render_template('adicionar.html')

@app.route('/excluir/<int:id>')
def delete(id):
    livro = Livro.query.get(id)
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('list'))

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        new_titulo = request.form['titulo']
        new_autor = request.form['autor']
        new_editora = request.form['editora']
        new_valor = request.form['valor']
        livro = Livro.query.get(id)
        livro.titulo = new_titulo
        livro.autor = new_autor
        livro.editora = new_editora
        livro.valor = new_valor
        db.session.commit()
        return redirect(url_for('list'))
    else:
        livro = Livro.query.get(id)
        return render_template('atualiza.html', livro = livro)
    
@app.route('/procurar', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        titulo = request.form['titulo']
        livros = Livro.query.filter(Livro.titulo.like(f'%{titulo}%')).all()
        return render_template('procurar.html', livros = livros)
    else:
        return render_template('procurar.html')

if __name__ == '__main__':
    app.run(debug=True)