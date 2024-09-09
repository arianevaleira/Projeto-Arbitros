from flask import Flask , render_template, url_for, redirect 

app = Flask(__name__)


#Pagina inicial (login)
@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')


#Pagina de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    return render_template('cadastro.html')


#Pagina principal (usuario)
@app.route('/home')
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