from models import conectar_db

class Notificacao:
        
 
    @classmethod
    def notificacao_contratante(cls, con_id, arb_id, acao):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select usu_nome from tb_usuarios join tb_arbitros on arb_usu_id = usu_id where arb_usu_id = %s", (arb_id,))
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
    def notificacao_arbitro(cls, con_id, arb_id):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select usu_nome from tb_usuarios join tb_contratantes on con_usu_id = usu_id where con_id = %s", (con_id,))
        nome = cursor.fetchone()
        cursor.execute("select arb_usu_id as id from tb_arbitros where arb_id = %s", (arb_id,))
        id = cursor.fetchone()
        conteudo = f"Você tem uma nova solicitação de {nome['usu_nome']}"
        cursor.execute("INSERT INTO tb_notificacoes(not_usu_id, not_conteudo) VALUES(%s,%s)", (id['id'], conteudo,))
        conn.commit()
        conn.close()
        cursor.close()
        return True

    
    @classmethod
    def listar(cls, usu_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT not_id as id, not_conteudo as conteudo, not_data as data FROM tb_notificacoes where not_usu_id = %s ", (usu_id,))
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
