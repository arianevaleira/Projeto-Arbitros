from flask import Flask , render_template, url_for, redirect, request

app = Flask(__name__)


#Pagina inicial (login)
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
      return redirect(url_for('home'))
    return render_template('index.html')



#Pagina de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
      return redirect(url_for('index'))
    return render_template('cadastro.html')


#Pagina principal (usuario)
@app.route('/home')
def home():
    return render_template('home.html')