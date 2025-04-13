from flask import Flask, redirect, render_template, url_for, request, flash, session, jsonify
from werkzeug.security import check_password_hash
from models.arbitro import Arbitro
from models.contratante import Contratante
from models.usuario import Usuario
from models.comentario import Comentario
from models.notificacao import Notificacao
from models.solicitacao import Solicitacao
from models.partida import Partida
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import conectar_db
import os 
from datetime import date, datetime

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
            return redirect(url_for('cadastro', erro='email'))

        user = Usuario(nome=nome, email=email, cpf=cpf, telefone=telefone, senha=senha, tipo=tipo)
        user.add_usuario()
        
        if tipo == "contratante":
            Contratante.add_contratante(user.get_id())
        else:
            Arbitro.add_arbitro(user.get_id())
            
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
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M")
    if request.method == 'POST':
        arb_id = request.form['arbitro']
        descricao = request.form['descricao']
        data = request.form['data']
        inicio = request.form['horaInicio']
        fim = request.form['horaFim']
        if data == today:
            if inicio < now:
                return "Não é possível selecionar um horário que já passou"
        con_id = current_user.get_id()
        Solicitacao.criar_solicitacao(data, inicio, fim, descricao, con_id, arb_id)
    return render_template('solicitacao.html', arbitros=arbitros, today=today)

@app.route('/responder_solicitacao', methods=['POST'])
def responder_solicitacao():
    sol_id = request.form['sol_id']
    con_id = request.form['con_id']
    acao = request.form['acao']
    arb_id = request.form['arb_id']
    if acao == "aceitar":
        Notificacao.notificacao_contratante(con_id, arb_id, "aceitou")
        Solicitacao.alterar_status(sol_id, "Aceita")
        Partida.registrar_partida(sol_id, con_id ,arb_id)
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
    user_id = current_user.get_id()
    if session.get('user_tipo') == "contratante":
        partidas = Partida.listar_partidas_contratante(user_id)
    elif session.get('user_tipo') == "arbitro":
        partidas = Partida.listar_partidas_arbitro(user_id)
    else:
        partidas = []
        
    return render_template('partidas.html', partidas=partidas)

@app.route('/cancelar_partida', methods=['POST'])
def cancelar_partida():
    user_id = current_user.get_id()
    user_tipo = session.get('user_tipo')
    par_id = request.form['par_id']
    con_id = request.form['con_id']
    arb_id = request.form['arb_id']
    Partida.cancelar_partida(par_id)
    Notificacao.notificacao_cancelamento(user_tipo, con_id, arb_id, user_id)

    return redirect(url_for('partidas'))


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


@app.route('/salvar_localizacao', methods=['POST'])
@login_required
def salvar_localizacao():
    data = request.json
    lat = data.get('latitude')
    lng = data.get('longitude')

    if not lat or not lng:
        return jsonify({"error": "Latitude e longitude são obrigatórias"}), 400

    # Atualiza a localização do usuário no banco de dados
    Usuario.atualizar_localizacao(current_user.get_id(), lat, lng)
    
    return jsonify({
        "message": "Localização salva com sucesso!",
        "lat": lat,
        "lng": lng,
        "nome": current_user._nome
    }), 200

@app.route('/recuperar_localizacoes', methods=['GET'])
@login_required
def recuperar_localizacoes():
    localizacoes = Usuario.listar_localizacoes()
    return jsonify([{"lat": loc['lat'], "lng": loc['lng'], "nome": loc['nome']} for loc in localizacoes]), 200


@app.route('/update_arbitro', methods=['POST'])
@login_required
def update_arbitro():
    if session.get('user_tipo') != "arbitro":
        return redirect(url_for('configuracoes_con'))
    nome = request.form['nome']
    cep = request.form['cep']
    sobre = request.form['sobre']
    estado = request.form['estado']
    cidade = request.form['cidade']
    arquivo = request.files['certificado']
    caminho_certificado = ""
    if arquivo:
        diretorio_certificados = 'certificados'  
        os.makedirs(diretorio_certificados, exist_ok=True)  
        caminho_certificado = os.path.join(diretorio_certificados, arquivo.filename)
        arquivo.save(caminho_certificado)
        # Atualiza os dados do usuário
        Arbitro.atualizar_usuario(current_user.get_id(), cep, estado, cidade)
        # Atualiza o caminho do certificado
        Arbitro.atualizar_certificado(current_user.get_id(), caminho_certificado)

    flash('Perfil atualizado com sucesso!')
    return redirect(url_for('configuracoes_arb'))

@app.route('/update_contratante', methods=['POST'])
@login_required
def update_contratante():
    nome = request.form['nome']
    cep = request.form['cep']
    estado = request.form['estado']
    cidade = request.form['cidade']
    sobre = request.form['sobre'] #Depois botar essa coluna no banco 


    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tb_usuarios 
        SET usu_nome = %s, usu_cep = %s, usu_estado = %s, usu_cidade = %s 
        WHERE usu_id = %s
    """, (nome, cep, estado, cidade, current_user.get_id()))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Perfil atualizado com sucesso!')
    return redirect(url_for('configuracoes_con'))

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

