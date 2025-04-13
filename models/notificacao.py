from models import conectar_db

class Notificacao:
        
 
    @classmethod
    def notificacao_contratante(cls, con_id, arb_id, acao):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select usu_nome from tb_usuarios join tb_arbitros on arb_usu_id = usu_id where arb_id = %s", (arb_id,))
        nome = cursor.fetchone()
        conteudo = f"O árbitro {nome['usu_nome']} {acao} sua solicitação"
        cursor.execute("select con_usu_id as id from tb_contratantes where con_id = %s", (con_id,))
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

    # @classmethod
    # def notificacao_arbitro(cls, con_id, arb_id):
    #     conn = conectar_db()  
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute("SELECT usu_nome FROM tb_usuarios JOIN tb_contratantes ON con_usu_id = usu_id WHERE con_id = %s", (con_id,))
    #     nome = cursor.fetchone()
    #     cursor.execute("SELECT arb_usu_id AS id FROM tb_arbitros WHERE arb_id = %s", (arb_id,))
    #     id = cursor.fetchone()
    #     # if not nome or 'usu_nome' not in nome:
    #     #     print(f"DEBUG: Nenhum contratante encontrado para con_id={con_id}")
    #     #     conn.close()
    #     #     return False  # ou lançar uma exceção
    #     # if not id or 'id' not in id:
    #     #     print(f"DEBUG: Nenhum árbitro encontrado para arb_id={arb_id}")
    #     #     conn.close()
    #     #     return False  # ou lançar uma exceção
    #     conteudo = f"Você tem uma nova solicitação de {nome['usu_nome']}"
    #     cursor.execute("INSERT INTO tb_notificacoes(not_usu_id, not_conteudo) VALUES(%s, %s)", (id['id'], conteudo))

    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    #     return True

    
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
