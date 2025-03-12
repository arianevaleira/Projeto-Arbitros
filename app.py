from flask import Flask, redirect, render_template, url_for, request, flash, session
from werkzeug.security import check_password_hash
from models.arbitro import Arbitro
from models.contratante import Contratante
from models.usuario import Usuario
from models.comentario import Comentario
from models.notificacao import Notificacao
from models.solicitacao import Solicitacao
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()

app = Flask(__name__)

login_manager.init_app(app)

app.config['SECRET_KEY'] = 'muitodificil'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get(int(user_id))


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

        user = Usuario.get_by_email(email)
        if user and check_password_hash(user['usu_senha'], senha):
            if user['usu_tipo'] == "arbitro":
                session['user_tipo'] = "arbitro"
            elif user['usu_tipo'] == "contratante":
                session['user_tipo'] = "contratante"
            login_user(Usuario.get(user['usu_id']))
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

        if Usuario.exists(email):
            return "Email já cadastrado!", 400
        
        else:
            user = Usuario(nome=nome, email=email, cpf=cpf, telefone=telefone, senha=senha, tipo=tipo)
            user.add_usuario()            
            if tipo == "contratante":
                Contratante.add_contratante(user.get_id())
            else:
                Arbitro.add_arbitro(user.get_id())
            # logar o usuário após cadastro
            login_user(user)
            return redirect(url_for('login'))

    return render_template('login.html')


#Pagina principal (usuario)
@app.route('/home', methods=['GET', 'POST'])
@login_required 
def home():
    comentarios = Comentario.listar()
    return render_template('home.html', comentarios=comentarios)


#Pagina sobre (informações)
@app.route('/sobre')
@login_required
def sobre(): 
    return render_template('sobre.html')


#Pagina Sobre (Fora do Login)
@app.route('/sobre_inicial')
def sobre_inicial():
    return render_template('sobre_inicial.html')

#Pagina de solicitação (Cadastrar partidas)
@app.route('/solicitacao', methods=['GET', 'POST'])
@login_required
def solicitacao():
    arbitros = Arbitro.listar()
    if session.get('user_tipo') != "contratante":
        return redirect(url_for('solicitacao_arbitro'))
    if request.method == 'POST':
        arb_id = request.form['arbitro']
        descricao = request.form['descricao']
        data = request.form['data']
        inicio = request.form['inicio']
        fim = request.form['fim']
        con_id = current_user.get_id()
        Solicitacao.criar_solicitacao(data, inicio, fim, descricao, con_id, arb_id)
        Notificacao.notificacao_arbitro(con_id, arb_id)
    return render_template('solicitacao.html', arbitros=arbitros)


@app.route('/responder_solicitacao', methods=['POST'])
def responder_solicitacao():
    sol_id = request.form['sol_id']
    con_id = request.form['con_id']
    acao = request.form['acao']
    arb_id = current_user.get_id()
    if acao == "aceitar":
        Notificacao.notificacao_contratante(con_id, arb_id, "aceitou")
        Solicitacao.alterar_status(sol_id, "Aceita")
    elif acao == "recusar":
        Notificacao.notificacao_contratante(con_id, arb_id, "recusou")
        Solicitacao.alterar_status(sol_id, "Recusada")

    return redirect(url_for('solicitacao_arbitro'))


@app.route('/solicitacao_arbitro')
def solicitacao_arbitro():
    if session.get('user_tipo') != "arbitro":
        return redirect(url_for('solicitacao'))
    arb_id = current_user.get_id()
    solicitacoes = Solicitacao.listar(arb_id)
    return render_template('solicitacao_arbitro.html', solicitacoes=solicitacoes)


@app.route('/comentarios', methods=['POST'])
@login_required
def comentarios():
    conteudo = request.form['conteudo']
    usu_id = current_user.get_id()
    Comentario.add_comentario(conteudo, usu_id)
    return redirect (url_for('home'))


#Pagina onde ficará a galeria (fotos das partidas)
@app.route('/partidas')
@login_required
def partidas():
    return render_template('partidas.html')


@app.route('/configuracoes')
@login_required
def configuracoes_dinamica():
    arbitros = Arbitro.listar()
    if session.get('user_tipo') == "contratante":  # Se o usuário for contratante
        return redirect(url_for('configuracoes_con'))
    elif session.get('user_tipo') == "arbitro":  # Se o usuário for árbitro
        return redirect(url_for('configuracoes_arb', arbitros=arbitros))
    else:
        flash("Tipo de usuário não reconhecido.")
        return redirect(url_for('home'))  


@app.route('/configuracoes_arb', methods=['GET', 'POST'])
@login_required
def configuracoes_arb():
    if session.get('user_tipo') != "arbitro":
        return redirect(url_for('configuracoes_con'))
    
    user_data = Usuario.get(current_user.get_id())
    return render_template('configuracao_arb.html', user=user_data)

@app.route('/configuracoes_con')
@login_required
def configuracoes_con():
    return render_template('configuracao_con.html', user=current_user)

#Pagina onde ficara as notificações do usuario
@app.route('/notificacoes')
@login_required
def notificacoes():
    usu_id = current_user.get_id()
    notificacoes = Notificacao.listar(usu_id)
    return render_template('notificacoes.html', notificacoes=notificacoes)

@app.route('/excluir_notificacoes/<int:id>')
@login_required
def excluir_notificacoes(id):
    Notificacao.delete(id)
    return redirect (url_for('notificacoes'))

@app.route('/saiba-mais')
def saiba_mais():
    return render_template('saiba_mais.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/teste')
def teste():
    return render_template('teste.html')


if __name__ == '__main__':
    app.run(debug=True)
