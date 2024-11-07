
from flask import Flask, redirect, render_template, url_for, request, flash
from werkzeug.security import check_password_hash
from models import User
from flask_login import LoginManager, login_user, login_required, logout_user
import mysql.connector

login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)

app.config['SECRET_KEY'] = 'muitodificil'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


#primeira pagina (de abertura)
@app.route('/')
def inicial():
    return render_template('index.html')


#Pagina inicial (login)
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']   
        user = User.get_by_email(email)

        if user and check_password_hash(user['usu_senha'], senha):
            login_user(User.get(user['usu_id']))
            return redirect(url_for('home'))
        
        else:
            flash("Email ou senha inválidos")
    return render_template('login.html')


#Pagina de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        senha = request.form['senha']
        tipo = request.form['tipo']

        if not User.exists(email):
            user = User(nome=nome, email=email, cpf=cpf, telefone=telefone, senha=senha, tipo=tipo)
            user.add_usuario()            
            # logar o usuário após cadatro
            login_user(user)
            return redirect(url_for('login'))
        
        else:
            flash("Email já cadastrado")

    return render_template('login.html')


#Pagina principal (usuario)
@app.route('/home', methods=['GET', 'POST'])
#@login_required lembrar de apagar  
def home():
    return render_template('home.html')


#Pagina sobre (informações)
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


#Pagina de solicitação (Cadastrar partidas)
@app.route('/solicitacao')
def solicitacao():
    return render_template('solicitacao.html')


#Pagina onde ficará a galeria (fotos das partidas)
@app.route('/partidas')
def partidas():
    return render_template('partidas.html')

#Pagina onde sera o chat (mensagens)
@app.route('/chat')
def chat():
    return render_template('mensagem.html')

#Pagina onde ficara a alteração de dados do usurio (editar)
@app.route('/configuracoes')
def configuracoes():
    return render_template('configuracao.html')


#Pagina onde ficara as notificações do usuario
@app.route('/notificacoes')
def notificacoes():
    return render_template('notificacoes.html')
if __name__ == '__main__':
    app.run(debug=True)
