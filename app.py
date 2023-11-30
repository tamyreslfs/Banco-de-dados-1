from flask import Flask, render_template, request, redirect, url_for
import sqlite3

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Substitua pelo caminho do seu banco de dados SQLite

# Crie uma instância do SQLAlchemy vinculada ao aplicativo Flask
db = SQLAlchemy(app)

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    conn.row_factory = sqlite3.Row
    return conn

# Rotas para adicionar setor, cargo e funcionário
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/adicionar_setor', methods=['GET', 'POST'])
def adicionar_setor():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        nome = request.form['nome']
        cursor.execute('INSERT INTO setor (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('setor.html')

@app.route('/adicionar_cargo', methods=['GET', 'POST'])
def adicionar_cargo():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        nome = request.form['nome']
        id_setor = request.form['id_setor']
        cursor.execute('INSERT INTO cargos (nome, id_setor) VALUES (?, ?)', (nome, id_setor))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cargo.html')

@app.route('/adicionar_funcionario', methods=['GET', 'POST'])
def adicionar_funcionario():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form.get('status_funcionario')
        id_setor = request.form['id_setor']
        id_cargo = request.form['id_cargo']
        cursor.execute('INSERT INTO funcionarios (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_setor, id_cargo) VALUES (?, ?, ?, ?, ?, ?)',
                       (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_setor, id_cargo))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('funcionario.html')

# Rota para exibir tabelas
@app.route('/visualizar_tabelas')
def visualizar_tabelas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM setor')
    setores = cursor.fetchall()
    cursor.execute('SELECT * FROM cargos')
    cargos = cursor.fetchall()
    cursor.execute('SELECT * FROM funcionarios')
    funcionarios = cursor.fetchall()
    conn.close()
    return render_template('visualizar_tabelas.html', setores=setores, cargos=cargos, funcionarios=funcionarios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



