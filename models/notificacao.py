from models import conectar_db

class Notificacao:
        
 
    @classmethod
    def notificacao_contratante(cls, con_id, arb_id, acao):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select usu_nome, usu_email, usu_telefone from tb_usuarios join tb_arbitros on arb_usu_id = usu_id where arb_id = %s", (arb_id,))
        dados = cursor.fetchall()
        dado = dados[0]
        if acao == "aceitou":
            conteudo = f"O árbitro {dado['usu_nome']} aceitou sua solicitação. Entre em contato através do Email: {dado['usu_email']} ou do Telefone: {dado['usu_telefone']}"
        else:
            conteudo = f"O árbitro {dado['usu_nome']} recusou sua solicitação"
        cursor.execute("select con_usu_id as id from tb_contratantes where con_id = %s", (con_id,))
        id = cursor.fetchone()
        cursor.execute("INSERT INTO tb_notificacoes(not_usu_id, not_conteudo) VALUES(%s,%s)", (id['id'], conteudo,))
        conn.commit()
        conn.close()
        cursor.close()
        return True
    

    @classmethod
    def notificacao_arbitro(cls, con_id, arb_id):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select usu_nome, usu_email, usu_telefone from tb_usuarios join tb_contratantes on con_usu_id = usu_id where con_id = %s", (con_id,))
        dados = cursor.fetchall()
        dado = dados[0]
        conteudo = f"Para entrar em contato com o contratante {dado['usu_nome']}, utilize o Email: {dado['usu_email']} ou o Telefone: {dado['usu_telefone']}"
        cursor.execute("select arb_usu_id as id from tb_arbitros where arb_id = %s", (arb_id,))
        id = cursor.fetchone()
        cursor.execute("INSERT INTO tb_notificacoes(not_usu_id, not_conteudo) VALUES(%s,%s)", (id['id'], conteudo,))
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def notificacao_cancelamento(cls, user_tipo, con_id, arb_id, user_id):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usu_nome FROM tb_usuarios where usu_id = %s", (user_id,))
        nome = cursor.fetchone()
        conteudo = f"O {user_tipo} {nome['usu_nome']} cancelou a partida."
        if user_tipo == "contratante":
            cursor.execute("select arb_usu_id as id from tb_arbitros where arb_id = %s", (arb_id,))
            id = cursor.fetchone()
        elif user_tipo == "arbitro":
            cursor.execute("SELECT con_usu_id as id FROM tb_contratantes where con_id = %s", (con_id,))
            id = cursor.fetchone()
        cursor.execute("INSERT INTO tb_notificacoes(not_usu_id, not_conteudo) VALUES(%s,%s)", (id['id'],conteudo,))
        conn.commit()
        conn.close()
        cursor.close()
        return True

        
    @classmethod
    def listar(cls, usu_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT not_id as id, not_conteudo as conteudo, not_data as data FROM tb_notificacoes where not_usu_id = %s order by data desc ", (usu_id,))
        notificacoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return notificacoes
    
    @classmethod
    def delete(cls,id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_notificacoes WHERE not_id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
