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
@app.route('/home', methods=['GET', 'POST'])
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

@app.route('/chat')
def chat():
    return render_template('mensagem.html')

if __name__ == '__main__':
    app.run(debug=True)